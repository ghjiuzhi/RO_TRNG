#!/usr/bin/env python3
"""Profile packed restart outputs by row/byte/bit position.

This script is meant for mechanism analysis of the SP800-90B restart input
files emitted by RO_TRNG_restart_auto_top. It does not run ea_restart; it
summarizes where the packed restart matrix is biased.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path


def entropy_binary(p1: float) -> tuple[float, float]:
    if p1 <= 0.0 or p1 >= 1.0:
        return 0.0, 0.0
    p0 = 1.0 - p1
    h = -(p0 * math.log2(p0) + p1 * math.log2(p1))
    hmin = -math.log2(max(p0, p1))
    return h, hmin


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def infer_label(path: Path) -> str:
    return path.stem


def infer_warmup(label: str) -> int | None:
    match = re.search(r"warmup(\d+)", label)
    if match:
        return int(match.group(1))
    return None


def summarize_file(path: Path, restart_count: int, row_bytes: int, label: str) -> dict[str, object]:
    data = path.read_bytes()
    expected = restart_count * row_bytes
    if len(data) != expected:
        raise ValueError(f"{path}: expected {expected} bytes, got {len(data)}")

    total_bits = expected * 8
    total_ones = sum(byte.bit_count() for byte in data)
    overall_p1 = total_ones / total_bits
    _, overall_min_h = entropy_binary(overall_p1)

    byte_rows: list[dict[str, object]] = []
    bit_rows: list[dict[str, object]] = []
    byte_phase_rows: list[dict[str, object]] = []
    row_ones: list[int] = []
    byte_ones = [0] * row_bytes
    bit_ones = [[0] * 8 for _ in range(row_bytes)]
    phase_ones = [[0] * 8 for _ in range(8)]
    phase_counts = [[0] * 8 for _ in range(8)]

    for row_idx in range(restart_count):
        row = data[row_idx * row_bytes : (row_idx + 1) * row_bytes]
        row_ones_count = 0
        for byte_idx, value in enumerate(row):
            ones = value.bit_count()
            row_ones_count += ones
            byte_ones[byte_idx] += ones
            for bit_idx in range(8):
                bit = (value >> bit_idx) & 1
                bit_ones[byte_idx][bit_idx] += bit
                phase = byte_idx % 8
                phase_ones[phase][bit_idx] += bit
                phase_counts[phase][bit_idx] += 1
        row_ones.append(row_ones_count)

    row_mean = sum(row_ones) / len(row_ones)
    row_std = math.sqrt(sum((x - row_mean) ** 2 for x in row_ones) / len(row_ones))

    worst_bit = None
    for byte_idx in range(row_bytes):
        p1 = byte_ones[byte_idx] / (restart_count * 8)
        h, hmin = entropy_binary(p1)
        byte_rows.append(
            {
                "label": label,
                "byte_index": byte_idx,
                "byte_phase_mod8": byte_idx % 8,
                "ones": byte_ones[byte_idx],
                "zeros": restart_count * 8 - byte_ones[byte_idx],
                "p1": f"{p1:.9f}",
                "abs_bias": f"{abs(p1 - 0.5):.9f}",
                "entropy": f"{h:.9f}",
                "min_entropy": f"{hmin:.9f}",
            }
        )
        for bit_idx in range(8):
            ones = bit_ones[byte_idx][bit_idx]
            p1b = ones / restart_count
            hb, hminb = entropy_binary(p1b)
            x = max(ones, restart_count - ones)
            bit_row = {
                "label": label,
                "byte_index": byte_idx,
                "byte_phase_mod8": byte_idx % 8,
                "bit_index": bit_idx,
                "ones": ones,
                "zeros": restart_count - ones,
                "p1": f"{p1b:.9f}",
                "abs_bias": f"{abs(p1b - 0.5):.9f}",
                "x": x,
                "entropy": f"{hb:.9f}",
                "min_entropy": f"{hminb:.9f}",
            }
            bit_rows.append(bit_row)
            if worst_bit is None or x > int(worst_bit["x"]):
                worst_bit = bit_row

    for phase in range(8):
        for bit_idx in range(8):
            count = phase_counts[phase][bit_idx]
            ones = phase_ones[phase][bit_idx]
            p1 = ones / count if count else math.nan
            h, hmin = entropy_binary(p1) if count else (math.nan, math.nan)
            byte_phase_rows.append(
                {
                    "label": label,
                    "byte_phase_mod8": phase,
                    "bit_index": bit_idx,
                    "samples": count,
                    "ones": ones,
                    "zeros": count - ones,
                    "p1": f"{p1:.9f}",
                    "abs_bias": f"{abs(p1 - 0.5):.9f}",
                    "entropy": f"{h:.9f}",
                    "min_entropy": f"{hmin:.9f}",
                }
            )

    assert worst_bit is not None
    return {
        "summary": {
            "label": label,
            "input": str(path),
            "restart_count": restart_count,
            "row_bytes": row_bytes,
            "warmup_bytes": infer_warmup(label),
            "overall_p1": f"{overall_p1:.9f}",
            "overall_abs_bias": f"{abs(overall_p1 - 0.5):.9f}",
            "overall_min_entropy": f"{overall_min_h:.9f}",
            "row_ones_mean": f"{row_mean:.9f}",
            "row_ones_std": f"{row_std:.9f}",
            "worst_byte_index": worst_bit["byte_index"],
            "worst_bit_index": worst_bit["bit_index"],
            "worst_x": worst_bit["x"],
            "worst_p1": worst_bit["p1"],
        },
        "byte_rows": byte_rows,
        "bit_rows": bit_rows,
        "byte_phase_rows": byte_phase_rows,
    }


def write_markdown(path: Path, summary_rows: list[dict[str, object]], phase_rows: list[dict[str, object]]) -> None:
    lines = [
        "# Formal Restart Output Profile",
        "",
        f"- rows: `{len(summary_rows)}`",
        "",
        "## Summary",
        "",
        "| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['label']} | {row['warmup_bytes']} | {row['overall_p1']} | "
            f"{row['overall_min_entropy']} | {row['row_ones_std']} | "
            f"{row['worst_byte_index']}.{row['worst_bit_index']} | {row['worst_x']} | {row['worst_p1']} |"
        )
    lines.extend(
        [
            "",
            "## Byte-Phase Aggregate",
            "",
            "This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.",
            "",
            "| label | phase | bit | samples | p1 | min-H |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in phase_rows:
        if float(row["abs_bias"]) >= 0.02:
            lines.append(
                f"| {row['label']} | {row['byte_phase_mod8']} | {row['bit_index']} | "
                f"{row['samples']} | {row['p1']} | {row['min_entropy']} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", type=Path, default=[])
    parser.add_argument("inputs", nargs="*", type=Path)
    parser.add_argument("--restart-count", type=int, default=1000)
    parser.add_argument("--row-bytes", type=int, default=125)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--prefix", default="formal_restart_output_profile")
    args = parser.parse_args()

    inputs = [*args.inputs, *args.input]
    if not inputs:
        raise SystemExit("no input files")

    out_dir = args.out_dir
    summary_rows: list[dict[str, object]] = []
    byte_rows: list[dict[str, object]] = []
    bit_rows: list[dict[str, object]] = []
    phase_rows: list[dict[str, object]] = []
    for input_path in inputs:
        label = infer_label(input_path)
        result = summarize_file(input_path, args.restart_count, args.row_bytes, label)
        summary_rows.append(result["summary"])
        byte_rows.extend(result["byte_rows"])
        bit_rows.extend(result["bit_rows"])
        phase_rows.extend(result["byte_phase_rows"])

    write_csv(
        out_dir / f"{args.prefix}_summary.csv",
        summary_rows,
        [
            "label",
            "input",
            "restart_count",
            "row_bytes",
            "warmup_bytes",
            "overall_p1",
            "overall_abs_bias",
            "overall_min_entropy",
            "row_ones_mean",
            "row_ones_std",
            "worst_byte_index",
            "worst_bit_index",
            "worst_x",
            "worst_p1",
        ],
    )
    write_csv(
        out_dir / f"{args.prefix}_byte.csv",
        byte_rows,
        ["label", "byte_index", "byte_phase_mod8", "ones", "zeros", "p1", "abs_bias", "entropy", "min_entropy"],
    )
    write_csv(
        out_dir / f"{args.prefix}_byte_bit.csv",
        bit_rows,
        [
            "label",
            "byte_index",
            "byte_phase_mod8",
            "bit_index",
            "ones",
            "zeros",
            "p1",
            "abs_bias",
            "x",
            "entropy",
            "min_entropy",
        ],
    )
    write_csv(
        out_dir / f"{args.prefix}_byte_phase.csv",
        phase_rows,
        ["label", "byte_phase_mod8", "bit_index", "samples", "ones", "zeros", "p1", "abs_bias", "entropy", "min_entropy"],
    )
    write_markdown(out_dir / f"{args.prefix}.md", summary_rows, phase_rows)
    print(f"Wrote {out_dir / (args.prefix + '.md')}")


if __name__ == "__main__":
    main()
