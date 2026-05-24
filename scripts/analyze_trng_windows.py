#!/usr/bin/env python3
"""Windowed bit statistics for a raw TRNG byte stream."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_size(text: str) -> int:
    value = text.strip().lower()
    units = {
        "b": 1,
        "kib": 1024,
        "mib": 1024**2,
        "gib": 1024**3,
        "kb": 1000,
        "mb": 1000**2,
        "gb": 1000**3,
    }
    for suffix, mult in sorted(units.items(), key=lambda item: -len(item[0])):
        if value.endswith(suffix):
            return int(value[: -len(suffix)]) * mult
    return int(value)


def min_entropy(p1: float) -> float:
    pmax = max(p1, 1.0 - p1)
    if pmax <= 0.0:
        return 0.0
    return -math.log2(pmax)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--window-bytes", default="1MiB")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    window_bytes = parse_size(args.window_bytes)
    data = args.input.read_bytes()
    rows = []
    prev_last = None
    for start in range(0, len(data), window_bytes):
        chunk = data[start : start + window_bytes]
        if not chunk:
            continue
        ones = sum(byte.bit_count() for byte in chunk)
        bits = len(chunk) * 8
        p1 = ones / bits
        adjacent_equal = 0
        total_pairs = 0
        last = prev_last
        for byte in chunk:
            for shift in range(7, -1, -1):
                bit = (byte >> shift) & 1
                if last is not None:
                    adjacent_equal += int(bit == last)
                    total_pairs += 1
                last = bit
        prev_last = last
        rows.append(
            {
                "window_index": len(rows),
                "byte_start": start,
                "byte_end_exclusive": start + len(chunk),
                "bytes": len(chunk),
                "p1": f"{p1:.12f}",
                "bit_min_entropy": f"{min_entropy(p1):.12f}",
                "adjacent_equal_ratio": f"{(adjacent_equal / total_pairs):.12f}" if total_pairs else "",
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
