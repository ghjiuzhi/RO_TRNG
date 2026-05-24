#!/usr/bin/env python3
"""Convert restart FIFO diagnostic frames into a packed restart matrix.

Input is the ``*.frames.csv`` produced by ``analyze_restart_fifo_diag.py``.
The script keeps only send-phase frames, orders them by ``row_index`` and
``event_index``, writes a row-major packed-byte ``.bin``, and emits summary
tables that can be compared with formal SP800-90B restart captures.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: object, field: str, row_num: int) -> int:
    try:
        return int(str(value).strip(), 0)
    except Exception as exc:  # pragma: no cover - defensive parse detail
        raise ValueError(f"bad integer in row {row_num}, field {field}: {value!r}") from exc


def is_send_frame(row: dict[str, str]) -> bool:
    phase = str(row.get("phase", "")).strip()
    phase_name = str(row.get("phase_name", "")).strip().lower()
    return phase == "2" or phase_name == "send"


def load_send_frames(path: Path) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"row_index", "event_index", "fifo_byte"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing required column(s): {', '.join(sorted(missing))}")
        for row_num, row in enumerate(reader, start=2):
            if not is_send_frame(row):
                continue
            value = parse_int(row.get("fifo_byte"), "fifo_byte", row_num)
            if value < 0 or value > 255:
                raise ValueError(f"fifo_byte out of range in row {row_num}: {value}")
            rows.append(
                {
                    "source_row": row_num,
                    "seq": parse_int(row.get("seq", len(rows)), "seq", row_num) if "seq" in row else len(rows),
                    "row_index": parse_int(row.get("row_index"), "row_index", row_num),
                    "event_index": parse_int(row.get("event_index"), "event_index", row_num),
                    "fifo_byte": value,
                }
            )
    if not rows:
        raise ValueError(f"{path} contains no send-phase frames")
    return rows


def infer_shape(rows: list[dict[str, int]], restart_count: int | None, bytes_per_restart: int | None) -> tuple[int, int]:
    inferred_restart_count = max(row["row_index"] for row in rows) + 1
    inferred_bytes_per_restart = max(row["event_index"] for row in rows) + 1
    return restart_count or inferred_restart_count, bytes_per_restart or inferred_bytes_per_restart


def build_matrix(
    rows: list[dict[str, int]],
    restart_count: int,
    bytes_per_restart: int,
    *,
    strict: bool,
) -> tuple[list[bytearray], list[dict[str, object]]]:
    matrix = [bytearray([0] * bytes_per_restart) for _ in range(restart_count)]
    seen: dict[tuple[int, int], dict[str, int]] = {}
    issues: list[dict[str, object]] = []

    for row in sorted(rows, key=lambda x: (x["row_index"], x["event_index"], x["seq"])):
        key = (row["row_index"], row["event_index"])
        if row["row_index"] < 0 or row["row_index"] >= restart_count:
            issues.append({"kind": "row_out_of_range", **row})
            continue
        if row["event_index"] < 0 or row["event_index"] >= bytes_per_restart:
            issues.append({"kind": "event_out_of_range", **row})
            continue
        if key in seen:
            issues.append(
                {
                    "kind": "duplicate",
                    "row_index": row["row_index"],
                    "event_index": row["event_index"],
                    "first_seq": seen[key]["seq"],
                    "duplicate_seq": row["seq"],
                    "first_fifo_byte": seen[key]["fifo_byte"],
                    "duplicate_fifo_byte": row["fifo_byte"],
                }
            )
            if strict:
                continue
        seen[key] = row
        matrix[row["row_index"]][row["event_index"]] = row["fifo_byte"]

    for row_idx in range(restart_count):
        for byte_idx in range(bytes_per_restart):
            if (row_idx, byte_idx) not in seen:
                issues.append({"kind": "missing", "row_index": row_idx, "event_index": byte_idx})

    fatal_kinds = {"missing", "row_out_of_range", "event_out_of_range"}
    if strict and any(str(issue["kind"]) in fatal_kinds for issue in issues):
        counts = defaultdict(int)
        for issue in issues:
            counts[str(issue["kind"])] += 1
        detail = ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
        raise ValueError(f"incomplete or out-of-range matrix in strict mode: {detail}")
    return matrix, issues


def summarize_matrix(matrix: list[bytearray], label: str, input_path: Path, bin_path: Path, issues: list[dict[str, object]]) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    restart_count = len(matrix)
    bytes_per_restart = len(matrix[0]) if matrix else 0
    total_bytes = restart_count * bytes_per_restart
    total_bits = total_bytes * 8

    row_ones = [sum(value.bit_count() for value in row) for row in matrix]
    total_ones = sum(row_ones)
    row_mean = total_ones / restart_count if restart_count else 0.0
    row_var = sum((value - row_mean) ** 2 for value in row_ones) / restart_count if restart_count else 0.0

    byte_rows: list[dict[str, object]] = []
    bit_rows: list[dict[str, object]] = []
    raw_bit_rows: list[dict[str, object]] = []
    worst_bit: dict[str, object] | None = None
    for byte_idx in range(bytes_per_restart):
        byte_ones = sum(matrix[row_idx][byte_idx].bit_count() for row_idx in range(restart_count))
        byte_bits = restart_count * 8
        byte_rows.append(
            {
                "byte_index": byte_idx,
                "ones": byte_ones,
                "zeros": byte_bits - byte_ones,
                "p1": f"{(byte_ones / byte_bits) if byte_bits else 0.0:.9f}",
                "abs_bias": f"{abs((byte_ones / byte_bits) - 0.5) if byte_bits else 0.0:.9f}",
            }
        )
        for bit_idx in range(8):
            ones = sum((matrix[row_idx][byte_idx] >> bit_idx) & 1 for row_idx in range(restart_count))
            zeros = restart_count - ones
            p1 = ones / restart_count if restart_count else 0.0
            row = {
                "byte_index": byte_idx,
                "bit_index": bit_idx,
                "ones": ones,
                "zeros": zeros,
                "p1": f"{p1:.9f}",
                "abs_bias": f"{abs(p1 - 0.5):.9f}",
                "x": max(ones, zeros),
                "msb_expanded_column": byte_idx * 8 + (7 - bit_idx),
                "lsb_expanded_column": byte_idx * 8 + bit_idx,
            }
            raw_bit_rows.append(row)
            bit_rows.append({"bit_order": "msb", "expanded_column": row["msb_expanded_column"], **row})
            bit_rows.append({"bit_order": "lsb", "expanded_column": row["lsb_expanded_column"], **row})
            if worst_bit is None or int(row["x"]) > int(worst_bit["x"]):
                worst_bit = row

    bit_rows.sort(key=lambda r: (str(r["bit_order"]), int(r["expanded_column"])))
    raw_bit_rows.sort(key=lambda r: (int(r["byte_index"]), int(r["bit_index"])))
    issue_counts = defaultdict(int)
    for issue in issues:
        issue_counts[str(issue["kind"])] += 1

    summary = {
        "label": label,
        "input_frames_csv": str(input_path.resolve()),
        "packed_bin": str(bin_path.resolve()),
        "packed_bin_sha256": sha256_file(bin_path),
        "restart_count": restart_count,
        "bytes_per_restart": bytes_per_restart,
        "packed_bytes": total_bytes,
        "expanded_bits": total_bits,
        "total_ones": total_ones,
        "overall_p1": f"{(total_ones / total_bits) if total_bits else 0.0:.9f}",
        "row_ones_mean": f"{row_mean:.9f}",
        "row_ones_std": f"{math.sqrt(row_var):.9f}",
        "row_ones_min": min(row_ones) if row_ones else 0,
        "row_ones_max": max(row_ones) if row_ones else 0,
        "worst_byte_index": worst_bit["byte_index"] if worst_bit else "",
        "worst_bit_index": worst_bit["bit_index"] if worst_bit else "",
        "worst_ones": worst_bit["ones"] if worst_bit else "",
        "worst_zeros": worst_bit["zeros"] if worst_bit else "",
        "worst_x": worst_bit["x"] if worst_bit else "",
        "worst_p1": worst_bit["p1"] if worst_bit else "",
        "worst_msb_expanded_column": worst_bit["msb_expanded_column"] if worst_bit else "",
        "worst_lsb_expanded_column": worst_bit["lsb_expanded_column"] if worst_bit else "",
        "issue_count": len(issues),
        "missing_count": issue_counts["missing"],
        "duplicate_count": issue_counts["duplicate"],
        "out_of_range_count": issue_counts["row_out_of_range"] + issue_counts["event_out_of_range"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return summary, byte_rows, bit_rows, raw_bit_rows


def write_markdown(
    path: Path,
    summary: dict[str, object],
    byte_rows: list[dict[str, object]],
    raw_bit_rows: list[dict[str, object]],
    column_analysis_command: str,
) -> None:
    top_bytes = sorted(byte_rows, key=lambda r: float(r["abs_bias"]), reverse=True)[:8]
    top_bits = sorted(raw_bit_rows, key=lambda r: int(r["x"]), reverse=True)[:8]
    lines = [
        f"# Restart FIFO Diagnostic Send Matrix: {summary['label']}",
        "",
        f"- input frames: `{summary['input_frames_csv']}`",
        f"- packed bin: `{summary['packed_bin']}`",
        f"- SHA256: `{summary['packed_bin_sha256']}`",
        f"- matrix: `{summary['restart_count']} x {summary['bytes_per_restart']}` packed bytes",
        f"- overall p1: `{summary['overall_p1']}`",
        f"- row ones mean/std/min/max: `{summary['row_ones_mean']}` / `{summary['row_ones_std']}` / `{summary['row_ones_min']}` / `{summary['row_ones_max']}`",
        f"- worst bit position: byte `{summary['worst_byte_index']}`, bit `{summary['worst_bit_index']}`, p1 `{summary['worst_p1']}`, x `{summary['worst_x']}`",
        f"- issues: total `{summary['issue_count']}`, missing `{summary['missing_count']}`, duplicate `{summary['duplicate_count']}`, out-of-range `{summary['out_of_range_count']}`",
        "",
        "## Most Biased Byte Positions",
        "",
        "| byte_index | p1 | abs_bias | ones | zeros |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in top_bytes:
        lines.append(f"| {row['byte_index']} | {row['p1']} | {row['abs_bias']} | {row['ones']} | {row['zeros']} |")

    lines.extend(
        [
            "",
            "## Most Biased Bit Positions",
            "",
            "| byte_index | bit_index | p1 | x | msb_col | lsb_col |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in top_bits:
        lines.append(
            f"| {row['byte_index']} | {row['bit_index']} | {row['p1']} | {row['x']} | "
            f"{row['msb_expanded_column']} | {row['lsb_expanded_column']} |"
        )

    lines.extend(
        [
            "",
            "## Compatible Column Analysis",
            "",
            "The packed bin is row-major and can be passed directly to `scripts/analyze_restart_matrix_columns.py`:",
            "",
            "```powershell",
            column_analysis_command,
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="*.frames.csv from analyze_restart_fifo_diag.py")
    parser.add_argument("--out-dir", type=Path, default=Path("data/experiments/restart_fifo_diag_20260524"))
    parser.add_argument("--label", default="", help="Output label; defaults to input stem without .frames")
    parser.add_argument("--restart-count", type=int, default=None)
    parser.add_argument("--bytes-per-restart", type=int, default=None)
    parser.add_argument("--non-strict", action="store_true", help="Allow missing/out-of-range cells and fill missing bytes with 0")
    args = parser.parse_args()

    input_path = args.input.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    label = args.label or input_path.name.removesuffix(".frames.csv")

    rows = load_send_frames(input_path)
    restart_count, bytes_per_restart = infer_shape(rows, args.restart_count, args.bytes_per_restart)
    matrix, issues = build_matrix(rows, restart_count, bytes_per_restart, strict=not args.non_strict)

    bin_path = out_dir / f"{label}.send_packed.bin"
    with bin_path.open("wb") as f:
        for row in matrix:
            f.write(row)

    summary, byte_rows, bit_rows, raw_bit_rows = summarize_matrix(matrix, label, input_path, bin_path, issues)
    summary_csv = out_dir / f"{label}.summary.csv"
    byte_csv = out_dir / f"{label}.byte_position_p1.csv"
    bit_csv = out_dir / f"{label}.bit_position_p1.csv"
    raw_bit_csv = out_dir / f"{label}.raw_byte_bit_p1.csv"
    issues_csv = out_dir / f"{label}.issues.csv"
    summary_md = out_dir / f"{label}.summary.md"

    write_csv(summary_csv, [summary], list(summary.keys()))
    write_csv(byte_csv, byte_rows, ["byte_index", "ones", "zeros", "p1", "abs_bias"])
    write_csv(
        bit_csv,
        bit_rows,
        [
            "bit_order",
            "expanded_column",
            "byte_index",
            "bit_index",
            "ones",
            "zeros",
            "p1",
            "abs_bias",
            "x",
            "msb_expanded_column",
            "lsb_expanded_column",
        ],
    )
    write_csv(
        raw_bit_csv,
        raw_bit_rows,
        ["byte_index", "bit_index", "ones", "zeros", "p1", "abs_bias", "x", "msb_expanded_column", "lsb_expanded_column"],
    )
    if issues:
        fieldnames = sorted({key for issue in issues for key in issue.keys()})
        write_csv(issues_csv, issues, fieldnames)

    column_cmd = (
        "python scripts\\analyze_restart_matrix_columns.py "
        f"--input {bin_path} "
        f"--restart-count {restart_count} "
        f"--bytes-per-restart {bytes_per_restart} "
        f"--out-dir {out_dir / (label + '.column_analysis')} "
        f"--label {label}"
    )
    write_markdown(summary_md, summary, byte_rows, raw_bit_rows, column_cmd)

    print(f"Wrote {bin_path}")
    print(f"Wrote {summary_csv}")
    print(f"Wrote {summary_md}")
    print(
        "Summary: "
        f"{restart_count}x{bytes_per_restart}, p1={summary['overall_p1']}, "
        f"row_std={summary['row_ones_std']}, "
        f"worst=byte{summary['worst_byte_index']}/bit{summary['worst_bit_index']} "
        f"p1={summary['worst_p1']} x={summary['worst_x']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
