#!/usr/bin/env python3
"""Summarize second held-out warmup/aperture sweep raw restart captures.

This is analysis-only glue for future hardware queues. It scans raw UART binary
captures that already exist, writes explicit missing rows for the configured
expected sweep grid, and derives conservative warmup transition points only
from valid observed captures. It never invokes Vivado or capture scripts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DIR = (
    ROOT
    / "data"
    / "hardware"
    / "20260529_fpga1_board2"
    / "restart_reduced_xor_second_heldout_sampler_20260530"
)
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "second_heldout_warmup_aperture_sweep_20260530"

BOARD = "z7020_b02"
DEFAULT_CONTEXT = "second_heldout_sample_ro_local"
DEFAULT_WARMUPS = [4, 5, 8, 10, 11, 12, 16]
RESTART_COUNT = 1000
ROW_BYTES = 125
HEADER_BYTES = 8
SYNC_HEADER = bytes.fromhex("A55A")
DATE_TAG = "20260530"

RAW_RE = re.compile(
    r"^restart_reduced_xor_random1_(?P<context>.+?)"
    r"_warmup(?P<warmup>\d+)_"
    r"(?P<variant>all640|data_ro\d+|except_data_ro\d+)_"
    r"(?P<run_id>[^_]+)_"
    r"(?P<restart_count>\d+)x(?P<row_bytes>\d+)_strict_"
    r"(?P<date_tag>\d{8})\.bin$"
)


def expected_conditions(condition_set: str) -> list[tuple[str, str]]:
    if condition_set == "anchors":
        return [("all640", "all"), ("data_ro", "0"), ("data_ro", "4")]
    rows = [("all640", "all")]
    rows.extend(("data_ro", str(i)) for i in range(8))
    rows.extend(("except_data_ro", str(i)) for i in range(8))
    return rows


def variant_name(kind: str, index: str) -> str:
    return "all640" if kind == "all640" else f"{kind}{index}"


def expected_file(raw_dir: Path, context: str, warmup: int, kind: str, index: str, run_id: str) -> Path:
    variant = variant_name(kind, index)
    name = (
        f"restart_reduced_xor_random1_{context}_warmup{warmup}_{variant}_"
        f"{run_id}_{RESTART_COUNT}x{ROW_BYTES}_strict_{DATE_TAG}.bin"
    )
    return raw_dir / name


def parse_warmups(text: str) -> list[int]:
    out: list[int] = []
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        out.append(int(item))
    return sorted(set(out))


def parse_run_ids(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def parse_variant(variant: str) -> tuple[str, str]:
    if variant == "all640":
        return "all640", "all"
    m = re.fullmatch(r"(data_ro|except_data_ro)(\d+)", variant)
    if not m:
        raise ValueError(f"Cannot parse variant: {variant}")
    return m.group(1), m.group(2)


def entropy_binary(p1: float) -> float:
    q = max(p1, 1.0 - p1)
    return -math.log2(q) if q > 0.0 else 0.0


def fmt(value: float | None, digits: int = 9) -> str:
    if value is None or math.isnan(value):
        return ""
    return f"{value:.{digits}f}"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def capture_start_time(meta: dict[str, Any]) -> str:
    value = meta.get("start_time", "")
    return str(value) if value is not None else ""


def aperture_class(abs_bias: float | None) -> str:
    if abs_bias is None or math.isnan(abs_bias):
        return ""
    if abs_bias <= 0.001:
        return "balanced"
    if abs_bias <= 0.01:
        return "near_balanced"
    if abs_bias <= 0.05:
        return "mild_bias"
    if abs_bias <= 0.15:
        return "moderate_bias"
    return "strong_bias"


def summarize_payload(path: Path, restart_count: int, row_bytes: int) -> dict[str, Any]:
    data = path.read_bytes()
    expected_bytes = HEADER_BYTES + restart_count * row_bytes
    header_ok = len(data) >= HEADER_BYTES and data[:2] == SYNC_HEADER
    if len(data) != expected_bytes:
        return {
            "status": "invalid_size",
            "status_detail": f"expected {expected_bytes} bytes, got {len(data)}",
            "raw_bytes": len(data),
            "payload_bytes": max(len(data) - HEADER_BYTES, 0),
            "header_ok": header_ok,
        }
    if not header_ok:
        return {
            "status": "invalid_header",
            "status_detail": "sync header A55A not found at byte 0",
            "raw_bytes": len(data),
            "payload_bytes": len(data) - HEADER_BYTES,
            "header_ok": False,
        }

    payload = data[HEADER_BYTES:]
    total_bits = len(payload) * 8
    ones = sum(byte.bit_count() for byte in payload)
    p1 = ones / total_bits

    worst_abs_bias = -1.0
    worst_x = -1
    worst_p1 = math.nan
    for byte_idx in range(row_bytes):
        for bit_idx in range(8):
            bit_ones = 0
            for row_idx in range(restart_count):
                value = payload[row_idx * row_bytes + byte_idx]
                bit_ones += (value >> bit_idx) & 1
            bit_p1 = bit_ones / restart_count
            bit_abs_bias = abs(bit_p1 - 0.5)
            if bit_abs_bias > worst_abs_bias:
                worst_abs_bias = bit_abs_bias
                worst_x = byte_idx * 8 + bit_idx
                worst_p1 = bit_p1

    row_ones = []
    for row_idx in range(restart_count):
        start = row_idx * row_bytes
        row = payload[start : start + row_bytes]
        row_ones.append(sum(byte.bit_count() for byte in row))

    return {
        "status": "ok",
        "status_detail": "",
        "p1": p1,
        "signed_bias": p1 - 0.5,
        "abs_bias": abs(p1 - 0.5),
        "min_entropy": entropy_binary(p1),
        "worst_x": worst_x,
        "worst_p1": worst_p1,
        "worst_abs_bias": worst_abs_bias,
        "row_ones_mean": mean(row_ones),
        "row_ones_std": pstdev(row_ones) if len(row_ones) > 1 else 0.0,
        "raw_bytes": len(data),
        "payload_bytes": len(payload),
        "header_ok": header_ok,
    }


def discover_raw_rows(raw_dir: Path, metadata_dir: Path) -> dict[tuple[int, str, str, str], dict[str, Any]]:
    rows: dict[tuple[int, str, str, str], dict[str, Any]] = {}
    if not raw_dir.exists():
        return rows

    for path in sorted(raw_dir.glob("*.bin")):
        match = RAW_RE.match(path.name)
        if not match:
            continue
        fields = match.groupdict()
        kind, index = parse_variant(fields["variant"])
        warmup = int(fields["warmup"])
        run_id = fields["run_id"]
        restart_count = int(fields["restart_count"])
        row_bytes = int(fields["row_bytes"])
        meta_path = metadata_dir / f"{path.stem}.json"
        meta = read_json(meta_path)
        stats = summarize_payload(path, restart_count, row_bytes)
        p1 = stats.get("p1")
        abs_bias = stats.get("abs_bias")
        key = (warmup, kind, index, run_id)
        rows[key] = {
            "board": str(meta.get("board_id", BOARD)),
            "context": str(meta.get("context", fields["context"])),
            "warmup": warmup,
            "run_id": run_id,
            "kind": kind,
            "index": index,
            "status": stats["status"],
            "status_detail": stats["status_detail"],
            "p1": fmt(p1),
            "signed_bias": fmt(stats.get("signed_bias")),
            "abs_bias": fmt(abs_bias),
            "min_entropy": fmt(stats.get("min_entropy")),
            "aperture_class": aperture_class(abs_bias),
            "worst_x": stats.get("worst_x", ""),
            "worst_p1": fmt(stats.get("worst_p1")),
            "worst_abs_bias": fmt(stats.get("worst_abs_bias")),
            "row_ones_mean": fmt(stats.get("row_ones_mean"), 6),
            "row_ones_std": fmt(stats.get("row_ones_std"), 6),
            "raw_bytes": stats.get("raw_bytes", ""),
            "payload_bytes": stats.get("payload_bytes", ""),
            "header_ok": stats.get("header_ok", ""),
            "restart_count": restart_count,
            "row_bytes": row_bytes,
            "file": rel(path),
            "metadata_file": rel(meta_path) if meta_path.exists() else "",
            "output_sha256": str(meta.get("output_sha256") or sha256_file(path)),
            "bitstream_sha256": str(meta.get("bitstream_sha256", "")),
            "capture_start_time": capture_start_time(meta),
            "date_tag": fields["date_tag"],
        }
    return rows


def build_sweep_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    raw_dir = args.raw_dir or (args.run_dir / "raw")
    metadata_dir = args.metadata_dir or (args.run_dir / "metadata")
    observed = discover_raw_rows(raw_dir, metadata_dir)

    warmups = sorted(set(args.warmups) | {key[0] for key in observed})
    run_ids = sorted(set(args.run_ids))
    conditions = expected_conditions(args.condition_set)

    rows: list[dict[str, Any]] = []
    expected_keys: set[tuple[int, str, str, str]] = set()
    for warmup in warmups:
        for run_id in run_ids:
            for kind, index in conditions:
                key = (warmup, kind, index, run_id)
                expected_keys.add(key)
                if key in observed:
                    rows.append(observed[key])
                    continue
                path = expected_file(raw_dir, args.context, warmup, kind, index, run_id)
                rows.append(
                    {
                        "board": BOARD,
                        "context": args.context,
                        "warmup": warmup,
                        "run_id": run_id,
                        "kind": kind,
                        "index": index,
                        "status": "missing",
                        "status_detail": "expected raw capture not found",
                        "p1": "",
                        "signed_bias": "",
                        "abs_bias": "",
                        "min_entropy": "",
                        "aperture_class": "",
                        "worst_x": "",
                        "worst_p1": "",
                        "worst_abs_bias": "",
                        "row_ones_mean": "",
                        "row_ones_std": "",
                        "raw_bytes": "",
                        "payload_bytes": "",
                        "header_ok": "",
                        "restart_count": RESTART_COUNT,
                        "row_bytes": ROW_BYTES,
                        "file": rel(path),
                        "metadata_file": "",
                        "output_sha256": "",
                        "bitstream_sha256": "",
                        "capture_start_time": "",
                        "date_tag": DATE_TAG,
                    }
                )
    for key, row in observed.items():
        if key not in expected_keys:
            rows.append(row)
    return sorted(rows, key=row_sort_key)


def row_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    kind_order = {"all640": 0, "data_ro": 1, "except_data_ro": 2}
    index = -1 if str(row["index"]) == "all" else int(row["index"])
    return int(row["warmup"]), kind_order[str(row["kind"])], index, str(row["run_id"])


def to_float(text: Any) -> float | None:
    try:
        if text == "" or text is None:
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def build_transition_rows(rows: list[dict[str, Any]], balanced_abs_bias: float) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("status") == "ok":
            groups[(str(row["context"]), str(row["kind"]), str(row["index"]))].append(row)

    out: list[dict[str, Any]] = []
    expected_warmups = sorted({int(row["warmup"]) for row in rows})
    for (context, kind, index), items in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        by_warmup: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for item in items:
            by_warmup[int(item["warmup"])].append(item)

        summary = []
        for warmup in sorted(by_warmup):
            p1s = [to_float(row["p1"]) for row in by_warmup[warmup]]
            p1s = [value for value in p1s if value is not None]
            if not p1s:
                continue
            p1_mean = mean(p1s)
            summary.append(
                {
                    "warmup": warmup,
                    "n": len(p1s),
                    "p1_mean": p1_mean,
                    "signed_bias_mean": p1_mean - 0.5,
                    "abs_bias_mean": abs(p1_mean - 0.5),
                }
            )

        if not summary:
            continue

        balanced = [item for item in summary if item["abs_bias_mean"] <= balanced_abs_bias]
        first_balanced = balanced[0] if balanced else None
        before = [item for item in summary if first_balanced and item["warmup"] < first_balanced["warmup"]]
        last_unbalanced_before = next(
            (item for item in reversed(before) if item["abs_bias_mean"] > balanced_abs_bias),
            None,
        )
        if first_balanced and last_unbalanced_before:
            bracket = f"{last_unbalanced_before['warmup']}->{first_balanced['warmup']}"
        elif first_balanced and first_balanced["warmup"] == summary[0]["warmup"]:
            bracket = "balanced_at_first_observed"
        elif first_balanced:
            bracket = f"first_balanced_warmup{first_balanced['warmup']}"
        else:
            bracket = "no_observed_balanced_point"

        adjacent = []
        for left, right in zip(summary, summary[1:]):
            delta = right["p1_mean"] - left["p1_mean"]
            adjacent.append((abs(delta), delta, left["warmup"], right["warmup"]))
        largest_delta = max(adjacent, default=(math.nan, math.nan, "", ""))

        signs = [sign(item["signed_bias_mean"]) for item in summary]
        sign_changes = sum(1 for a, b in zip(signs, signs[1:]) if a and b and a != b)
        strongest = max(summary, key=lambda item: item["abs_bias_mean"])
        weakest = min(summary, key=lambda item: item["abs_bias_mean"])
        observed_warmups = [item["warmup"] for item in summary]
        missing_warmups = [warmup for warmup in expected_warmups if warmup not in observed_warmups]

        out.append(
            {
                "context": context,
                "kind": kind,
                "index": index,
                "observed_warmups": ",".join(str(w) for w in observed_warmups),
                "missing_warmups": ",".join(str(w) for w in missing_warmups),
                "valid_warmup_count": len(summary),
                "balanced_abs_bias_threshold": fmt(balanced_abs_bias, 6),
                "first_balanced_warmup": first_balanced["warmup"] if first_balanced else "",
                "last_unbalanced_before_first_balanced": last_unbalanced_before["warmup"] if last_unbalanced_before else "",
                "transition_bracket": bracket,
                "strongest_abs_bias_warmup": strongest["warmup"],
                "strongest_abs_bias": fmt(strongest["abs_bias_mean"]),
                "min_abs_bias_warmup": weakest["warmup"],
                "min_abs_bias": fmt(weakest["abs_bias_mean"]),
                "largest_adjacent_delta_from_warmup": largest_delta[2],
                "largest_adjacent_delta_to_warmup": largest_delta[3],
                "largest_adjacent_delta_p1": fmt(largest_delta[1]),
                "bias_sign_changes": sign_changes,
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]], fields: list[str], limit: int | None = None) -> list[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    shown = rows[:limit] if limit else rows
    for row in shown:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    if limit and len(rows) > limit:
        lines.append("| " + " | ".join(["..."] * len(fields)) + " |")
    return lines


def write_markdown(path: Path, rows: list[dict[str, Any]], transitions: list[dict[str, Any]]) -> None:
    ok_rows = [row for row in rows if row.get("status") == "ok"]
    missing_rows = [row for row in rows if row.get("status") == "missing"]
    invalid_rows = [row for row in rows if str(row.get("status", "")).startswith("invalid")]
    by_warmup: dict[int, dict[str, int]] = defaultdict(lambda: {"ok": 0, "missing": 0, "invalid": 0})
    for row in rows:
        bucket = by_warmup[int(row["warmup"])]
        status = str(row.get("status", ""))
        if status == "ok":
            bucket["ok"] += 1
        elif status == "missing":
            bucket["missing"] += 1
        else:
            bucket["invalid"] += 1

    coverage_rows = [
        {
            "warmup": warmup,
            "ok": counts["ok"],
            "missing": counts["missing"],
            "invalid": counts["invalid"],
        }
        for warmup, counts in sorted(by_warmup.items())
    ]

    snapshot_fields = ["warmup", "kind", "index", "run_id", "status", "p1", "abs_bias", "aperture_class"]
    transition_fields = [
        "kind",
        "index",
        "observed_warmups",
        "missing_warmups",
        "transition_bracket",
        "strongest_abs_bias_warmup",
        "min_abs_bias_warmup",
        "bias_sign_changes",
    ]
    lines = [
        "# Second Held-Out Warmup Aperture Sweep",
        "",
        "Analysis-only summary over raw restart captures already present on disk. Missing future captures are retained as rows with `status=missing`; no hardware capture is run by this script.",
        "",
        "## Coverage",
        "",
        f"- Valid captures: {len(ok_rows)}",
        f"- Missing expected captures: {len(missing_rows)}",
        f"- Invalid captures: {len(invalid_rows)}",
        "",
        *md_table(coverage_rows, ["warmup", "ok", "missing", "invalid"]),
        "",
        "## Observed Snapshot",
        "",
        *md_table([row for row in rows if row.get("status") == "ok"], snapshot_fields, limit=32),
        "",
        "## Transition Points",
        "",
        *md_table(transitions, transition_fields, limit=32),
        "",
        "## Boundary",
        "",
        "Transition rows are descriptive brackets over observed warmups only. A missing warmup is treated as pending data, not as a pass, fail, or interpolation point.",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--raw-dir", type=Path, default=None)
    parser.add_argument("--metadata-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--context", default=DEFAULT_CONTEXT)
    parser.add_argument("--warmups", type=parse_warmups, default=DEFAULT_WARMUPS)
    parser.add_argument("--run-ids", type=parse_run_ids, default=["run01"])
    parser.add_argument(
        "--condition-set",
        choices=["anchors", "full-map"],
        default="anchors",
        help="Expected capture grid. Existing extra observations are still included.",
    )
    parser.add_argument("--balanced-abs-bias", type=float, default=0.001)
    args = parser.parse_args()

    rows = build_sweep_rows(args)
    transitions = build_transition_rows(rows, args.balanced_abs_bias)

    sweep_fields = [
        "board",
        "context",
        "warmup",
        "run_id",
        "kind",
        "index",
        "status",
        "status_detail",
        "p1",
        "signed_bias",
        "abs_bias",
        "min_entropy",
        "aperture_class",
        "worst_x",
        "worst_p1",
        "worst_abs_bias",
        "row_ones_mean",
        "row_ones_std",
        "raw_bytes",
        "payload_bytes",
        "header_ok",
        "restart_count",
        "row_bytes",
        "file",
        "metadata_file",
        "output_sha256",
        "bitstream_sha256",
        "capture_start_time",
        "date_tag",
    ]
    transition_fields = [
        "context",
        "kind",
        "index",
        "observed_warmups",
        "missing_warmups",
        "valid_warmup_count",
        "balanced_abs_bias_threshold",
        "first_balanced_warmup",
        "last_unbalanced_before_first_balanced",
        "transition_bracket",
        "strongest_abs_bias_warmup",
        "strongest_abs_bias",
        "min_abs_bias_warmup",
        "min_abs_bias",
        "largest_adjacent_delta_from_warmup",
        "largest_adjacent_delta_to_warmup",
        "largest_adjacent_delta_p1",
        "bias_sign_changes",
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "second_heldout_warmup_aperture_sweep.csv", rows, sweep_fields)
    write_csv(args.out_dir / "warmup_transition_points.csv", transitions, transition_fields)
    write_markdown(args.out_dir / "second_heldout_warmup_aperture_sweep.md", rows, transitions)
    print(f"Wrote {args.out_dir / 'second_heldout_warmup_aperture_sweep.csv'}")
    print(f"Wrote {args.out_dir / 'warmup_transition_points.csv'}")
    print(f"Wrote {args.out_dir / 'second_heldout_warmup_aperture_sweep.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
