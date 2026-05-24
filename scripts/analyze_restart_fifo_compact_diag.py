#!/usr/bin/env python3
"""Decode compact restart FIFO diagnostic captures."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--x-cutoff", type=int, default=0)
    args = parser.parse_args()

    label = args.label or args.input.stem
    data = args.input.read_bytes()
    if len(data) < 16 or data[:4] != b"FDIC":
        raise ValueError(f"{args.input} does not start with compact FDIC header")

    header = {
        "version": data[4],
        "restart_count": data[5] | (data[6] << 8),
        "row_bytes": data[7] | (data[8] << 8),
        "warmup_bytes": data[9] | (data[10] << 8),
        "total_bytes": data[11] | (data[12] << 8) | (data[13] << 16) | (data[14] << 24),
        "marker": data[15],
    }
    expected = 16 + header["total_bytes"]
    if len(data) != expected:
        raise ValueError(f"size mismatch: expected {expected}, got {len(data)}")

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    packed = out_dir / f"{label}.send_packed.bin"
    packed.write_bytes(data[16:])

    restart_count = int(header["restart_count"])
    row_bytes = int(header["row_bytes"])
    rows = []
    total_ones = 0
    row_ones = []
    worst = {"byte_index": "", "bit_index": "", "ones": 0, "zeros": 0, "x": -1, "p1": ""}
    for row_idx in range(restart_count):
        row = data[16 + row_idx * row_bytes : 16 + (row_idx + 1) * row_bytes]
        count = sum(value.bit_count() for value in row)
        row_ones.append(count)
        total_ones += count

    for byte_idx in range(row_bytes):
        for bit_idx in range(8):
            ones = 0
            for row_idx in range(restart_count):
                value = data[16 + row_idx * row_bytes + byte_idx]
                ones += (value >> bit_idx) & 1
            zeros = restart_count - ones
            x = max(ones, zeros)
            p1 = ones / restart_count if restart_count else 0.0
            rows.append(
                {
                    "byte_index": byte_idx,
                    "bit_index": bit_idx,
                    "ones": ones,
                    "zeros": zeros,
                    "p1": f"{p1:.9f}",
                    "x": x,
                    "msb_expanded_column": byte_idx * 8 + (7 - bit_idx),
                    "lsb_expanded_column": byte_idx * 8 + bit_idx,
                }
            )
            if x > int(worst["x"]):
                worst = {
                    "byte_index": byte_idx,
                    "bit_index": bit_idx,
                    "ones": ones,
                    "zeros": zeros,
                    "x": x,
                    "p1": f"{p1:.9f}",
                }

    total_bits = restart_count * row_bytes * 8
    p1 = total_ones / total_bits if total_bits else 0.0
    mean = total_ones / restart_count if restart_count else 0.0
    var = sum((value - mean) ** 2 for value in row_ones) / restart_count if restart_count else 0.0
    summary = {
        "label": label,
        **header,
        "input": str(args.input.resolve()),
        "input_sha256": sha256(args.input),
        "send_packed_bin": str(packed.resolve()),
        "send_packed_sha256": sha256(packed),
        "overall_p1": f"{p1:.9f}",
        "overall_abs_bias": f"{abs(p1 - 0.5):.9f}",
        "row_ones_mean": f"{mean:.9f}",
        "row_ones_std": f"{var ** 0.5:.9f}",
        "row_ones_min": min(row_ones) if row_ones else 0,
        "row_ones_max": max(row_ones) if row_ones else 0,
        "worst_byte_index": worst["byte_index"],
        "worst_bit_index": worst["bit_index"],
        "worst_x": worst["x"],
        "worst_p1": worst["p1"],
    }
    write_csv(out_dir / f"{label}.summary.csv", [summary], list(summary.keys()))
    write_csv(
        out_dir / f"{label}.raw_byte_bit_p1.csv",
        rows,
        ["byte_index", "bit_index", "ones", "zeros", "p1", "x", "msb_expanded_column", "lsb_expanded_column"],
    )

    md = [
        f"# Compact Restart FIFO Diagnostic: {label}",
        "",
        f"- input: `{summary['input']}`",
        f"- input SHA256: `{summary['input_sha256']}`",
        f"- header: `{header}`",
        f"- send packed bin: `{summary['send_packed_bin']}`",
        f"- send packed SHA256: `{summary['send_packed_sha256']}`",
        f"- matrix: `{restart_count} x {row_bytes}` bytes",
        f"- overall p1: `{summary['overall_p1']}`",
        f"- row ones mean/std/min/max: `{summary['row_ones_mean']}` / `{summary['row_ones_std']}` / `{summary['row_ones_min']}` / `{summary['row_ones_max']}`",
        f"- worst bit: byte `{summary['worst_byte_index']}`, bit `{summary['worst_bit_index']}`, p1 `{summary['worst_p1']}`, x `{summary['worst_x']}`",
        "",
        "## Column Analysis Command",
        "",
        "```powershell",
        f"python scripts\\analyze_restart_matrix_columns.py --input {packed} --restart-count {restart_count} --bytes-per-restart {row_bytes} --label {label} --out-dir {out_dir / (label + '.column_analysis')}",
        "```",
    ]
    (out_dir / f"{label}.summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {out_dir / (label + '.summary.md')}")
    print(f"Summary: {restart_count}x{row_bytes}, p1={summary['overall_p1']}, worst x={summary['worst_x']}")


if __name__ == "__main__":
    main()
