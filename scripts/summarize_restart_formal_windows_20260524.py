#!/usr/bin/env python3
"""Summarize byte-window bias in formal restart captures."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def label_warmup(path: Path) -> str:
    match = re.search(r"warmup(\d+)", path.name)
    return match.group(1) if match else ""


def summarize_window(data: bytes, restart_count: int, row_bytes: int, start: int, length: int) -> dict[str, object]:
    end = min(row_bytes, start + length)
    if start < 0 or start >= row_bytes or end <= start:
        raise ValueError(f"bad window start={start} length={length} row_bytes={row_bytes}")
    ones = 0
    row_ones: list[int] = []
    for row_idx in range(restart_count):
        row = data[row_idx * row_bytes + start : row_idx * row_bytes + end]
        count = sum(value.bit_count() for value in row)
        row_ones.append(count)
        ones += count
    bits = restart_count * (end - start) * 8
    p1 = ones / bits if bits else 0.0
    mean = ones / restart_count if restart_count else 0.0
    var = sum((x - mean) ** 2 for x in row_ones) / restart_count if restart_count else 0.0
    return {
        "window_start": start,
        "window_end_exclusive": end,
        "window_bytes": end - start,
        "ones": ones,
        "zeros": bits - ones,
        "p1": f"{p1:.9f}",
        "abs_bias": f"{abs(p1 - 0.5):.9f}",
        "row_ones_mean": f"{mean:.9f}",
        "row_ones_std": f"{var ** 0.5:.9f}",
        "row_ones_min": min(row_ones) if row_ones else 0,
        "row_ones_max": max(row_ones) if row_ones else 0,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", type=Path, required=True)
    parser.add_argument("--restart-count", type=int, default=1000)
    parser.add_argument("--row-bytes", type=int, default=125)
    parser.add_argument("--windows", default="0:32,32:32,64:32,96:29,0:125")
    parser.add_argument("--out-csv", type=Path, default=Path("data/experiments/restart_fifo_diag_20260524/formal_restart_window_summary_20260524.csv"))
    parser.add_argument("--out-md", type=Path, default=Path("data/experiments/restart_fifo_diag_20260524/formal_restart_window_summary_20260524.md"))
    args = parser.parse_args()

    windows = []
    for item in args.windows.split(","):
        start, length = item.split(":")
        windows.append((int(start), int(length)))

    rows: list[dict[str, object]] = []
    expected = args.restart_count * args.row_bytes
    for path in args.inputs:
        data = path.read_bytes()
        if len(data) != expected:
            raise ValueError(f"{path}: expected {expected} bytes, got {len(data)}")
        for start, length in windows:
            row = summarize_window(data, args.restart_count, args.row_bytes, start, length)
            row.update({"label": path.stem, "warmup": label_warmup(path), "input": str(path)})
            rows.append(row)

    fields = [
        "label",
        "warmup",
        "window_start",
        "window_end_exclusive",
        "window_bytes",
        "p1",
        "abs_bias",
        "row_ones_mean",
        "row_ones_std",
        "row_ones_min",
        "row_ones_max",
        "ones",
        "zeros",
        "input",
    ]
    write_csv(args.out_csv, rows, fields)

    lines = [
        "# Formal Restart Byte-Window Summary - 2026-05-24",
        "",
        "| warmup | label | window | bytes | p1 | abs_bias | row std |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['warmup']} | {row['label']} | {row['window_start']}..{row['window_end_exclusive']} | "
            f"{row['window_bytes']} | {row['p1']} | {row['abs_bias']} | {row['row_ones_std']} |"
        )
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
