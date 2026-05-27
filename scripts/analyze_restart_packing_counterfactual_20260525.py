#!/usr/bin/env python3
"""Restart packing/bit-order counterfactual analysis.

This script does not create new entropy data. It reinterprets existing packed
restart matrices under several row-preserving output mappings so that the
physical byte/bit hotspot can be separated from the SP800-90B expanded column
number.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESTART_DIR = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "restart"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "restart_packing_counterfactual_20260525"


SUMMARY_FIELDS = [
    "label",
    "input_file",
    "input_sha256",
    "restart_count",
    "bytes_per_restart",
    "overall_p1",
    "row_ones_mean",
    "row_ones_std",
    "worst_byte",
    "worst_bit_lsb_index",
    "worst_ones",
    "worst_zeros",
    "worst_x",
    "worst_p1",
    "msb_column",
    "lsb_column",
    "bitrev_msb_column",
    "byte_reverse_msb_column",
    "byte_reverse_lsb_column",
    "cyclic_shift1_msb_column",
    "cyclic_shift4_msb_column",
]

TOP_FIELDS = [
    "label",
    "rank",
    "byte_index",
    "bit_lsb_index",
    "ones",
    "zeros",
    "x",
    "p1",
    "abs_bias",
    "msb_column",
    "lsb_column",
    "bitrev_msb_column",
    "byte_reverse_msb_column",
    "byte_reverse_lsb_column",
    "cyclic_shift1_msb_column",
    "cyclic_shift4_msb_column",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def infer_label(path: Path) -> str:
    name = path.name
    name = name.removesuffix(".bin")
    return name


def discover_inputs(root: Path) -> list[Path]:
    candidates = []
    for path in sorted(root.glob("*.bin")):
        name = path.name
        if "_bps1_" in name:
            continue
        if ".tmp" in name:
            continue
        if "1000x125" not in name:
            continue
        candidates.append(path)
    return candidates


def mean(values: list[int] | list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def std_population(values: list[int] | list[float]) -> float:
    if not values:
        return float("nan")
    m = mean(values)
    return (sum((v - m) ** 2 for v in values) / len(values)) ** 0.5


def column_maps(byte_index: int, bit_lsb: int, bytes_per_restart: int) -> dict[str, int]:
    # bit_lsb is the physical bit index used by packed byte arithmetic.
    bit_msb_pos = 7 - bit_lsb
    byte_rev = bytes_per_restart - 1 - byte_index
    return {
        "msb_column": byte_index * 8 + bit_msb_pos,
        "lsb_column": byte_index * 8 + bit_lsb,
        "bitrev_msb_column": byte_index * 8 + bit_lsb,
        "byte_reverse_msb_column": byte_rev * 8 + bit_msb_pos,
        "byte_reverse_lsb_column": byte_rev * 8 + bit_lsb,
        "cyclic_shift1_msb_column": byte_index * 8 + ((bit_msb_pos + 1) % 8),
        "cyclic_shift4_msb_column": byte_index * 8 + ((bit_msb_pos + 4) % 8),
    }


def analyze_one(path: Path, restart_count: int, bytes_per_restart: int, label: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = path.read_bytes()
    expected = restart_count * bytes_per_restart
    if len(data) != expected:
        raise ValueError(f"{path}: expected {expected} bytes, got {len(data)}")

    counts = [[0 for _ in range(8)] for _ in range(bytes_per_restart)]
    row_ones: list[int] = []
    total_ones = 0
    for row_idx in range(restart_count):
        row = data[row_idx * bytes_per_restart : (row_idx + 1) * bytes_per_restart]
        ones_in_row = 0
        for byte_idx, value in enumerate(row):
            bit_count = value.bit_count()
            ones_in_row += bit_count
            total_ones += bit_count
            for bit in range(8):
                counts[byte_idx][bit] += (value >> bit) & 1
        row_ones.append(ones_in_row)

    top_rows: list[dict[str, Any]] = []
    for byte_idx in range(bytes_per_restart):
        for bit in range(8):
            ones = counts[byte_idx][bit]
            zeros = restart_count - ones
            p1 = ones / restart_count
            maps = column_maps(byte_idx, bit, bytes_per_restart)
            top_rows.append(
                {
                    "label": label,
                    "byte_index": byte_idx,
                    "bit_lsb_index": bit,
                    "ones": ones,
                    "zeros": zeros,
                    "x": max(ones, zeros),
                    "p1": p1,
                    "abs_bias": abs(p1 - 0.5),
                    **maps,
                }
            )
    top_rows.sort(key=lambda r: (int(r["x"]), float(r["abs_bias"])), reverse=True)
    for rank, row in enumerate(top_rows, start=1):
        row["rank"] = rank

    worst = top_rows[0]
    summary = {
        "label": label,
        "input_file": str(path),
        "input_sha256": sha256_file(path),
        "restart_count": restart_count,
        "bytes_per_restart": bytes_per_restart,
        "overall_p1": total_ones / (restart_count * bytes_per_restart * 8),
        "row_ones_mean": mean(row_ones),
        "row_ones_std": std_population(row_ones),
        "worst_byte": worst["byte_index"],
        "worst_bit_lsb_index": worst["bit_lsb_index"],
        "worst_ones": worst["ones"],
        "worst_zeros": worst["zeros"],
        "worst_x": worst["x"],
        "worst_p1": worst["p1"],
        "msb_column": worst["msb_column"],
        "lsb_column": worst["lsb_column"],
        "bitrev_msb_column": worst["bitrev_msb_column"],
        "byte_reverse_msb_column": worst["byte_reverse_msb_column"],
        "byte_reverse_lsb_column": worst["byte_reverse_lsb_column"],
        "cyclic_shift1_msb_column": worst["cyclic_shift1_msb_column"],
        "cyclic_shift4_msb_column": worst["cyclic_shift4_msb_column"],
    }
    return summary, top_rows[:32]


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.9g}"
    return str(value)


def write_markdown(path: Path, summaries: list[dict[str, Any]]) -> None:
    lines = [
        "# Restart Packing Counterfactual 20260525",
        "",
        "## Main Summary",
        "",
        "| label | p1 | worst byte.bit | x | worst p1 | MSB col | LSB col | byte-rev MSB col | row std |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summaries:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["label"]),
                    fmt(row["overall_p1"]),
                    f"{row['worst_byte']}.{row['worst_bit_lsb_index']}",
                    str(row["worst_x"]),
                    fmt(row["worst_p1"]),
                    str(row["msb_column"]),
                    str(row["lsb_column"]),
                    str(row["byte_reverse_msb_column"]),
                    fmt(row["row_ones_std"]),
                ]
            )
            + " |"
        )

    movement = Counter()
    for row in summaries:
        if row["msb_column"] != row["lsb_column"]:
            movement["msb_lsb_column_moves"] += 1
        if row["msb_column"] != row["byte_reverse_msb_column"]:
            movement["byte_reverse_column_moves"] += 1

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Runs where MSB and LSB expansion place the same physical hotspot in different columns: `{movement['msb_lsb_column_moves']}` / `{len(summaries)}`.",
            f"- Runs where byte-order reversal moves the hotspot column: `{movement['byte_reverse_column_moves']}` / `{len(summaries)}`.",
            "- A column-number change under MSB/LSB or byte-order reinterpretation does not create or remove the physical hotspot; it only moves how the same packed byte/bit position appears in the expanded SP800-90B matrix.",
            "- Therefore, if the same raw `byte.bit` remains the hotspot while expanded columns move, the mechanism should be described as fixed sampled-position bias exposed by packing, not as an intrinsic property of a particular column number.",
            "- If different warmups/repeats move to different raw `byte.bit` hotspots, the safer wording is a startup window with multiple biased fixed positions rather than a single immutable bad column.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def filter_inputs(paths: list[Path], regex: str | None) -> list[Path]:
    if not regex:
        return paths
    pattern = re.compile(regex)
    return [path for path in paths if pattern.search(path.name)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_RESTART_DIR)
    parser.add_argument("--filter-regex", default=r"random3|sample_ro|sampler_regs_only")
    parser.add_argument("--restart-count", type=int, default=1000)
    parser.add_argument("--bytes-per-restart", type=int, default=125)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    inputs = args.input or discover_inputs(args.input_dir)
    inputs = filter_inputs(inputs, args.filter_regex)
    if not inputs:
        raise SystemExit("No matching packed restart inputs found")

    summaries: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for path in inputs:
        label = infer_label(path)
        try:
            summary, top = analyze_one(path, args.restart_count, args.bytes_per_restart, label)
        except Exception as exc:  # noqa: BLE001 - batch analysis should preserve skip reasons.
            skipped.append({"input_file": str(path), "reason": str(exc)})
            continue
        summaries.append(summary)
        top_rows.extend(top)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "restart_packing_counterfactual_summary.csv", summaries, SUMMARY_FIELDS)
    write_csv(args.out_dir / "restart_packing_counterfactual_top_positions.csv", top_rows, TOP_FIELDS)
    if skipped:
        write_csv(args.out_dir / "restart_packing_counterfactual_skipped.csv", skipped, ["input_file", "reason"])
    write_markdown(args.out_dir / "restart_packing_counterfactual_summary.md", summaries)
    (args.out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "inputs": [str(path) for path in inputs],
                "summary_rows": len(summaries),
                "top_position_rows": len(top_rows),
                "skipped": skipped,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.out_dir}")
    print(f"summary_rows={len(summaries)} skipped={len(skipped)}")


if __name__ == "__main__":
    main()
