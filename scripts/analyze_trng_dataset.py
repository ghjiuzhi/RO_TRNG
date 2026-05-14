#!/usr/bin/env python3
"""Batch statistics for raw TRNG byte streams.

The script intentionally uses only the Python standard library so it can run in
the bundled Codex runtime or a plain Vivado Python environment.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from datetime import datetime
from pathlib import Path


def iter_files(inputs: list[Path], pattern: str) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        if item.is_dir():
            files.extend(sorted(item.glob(pattern)))
        elif item.is_file():
            files.append(item)
    return sorted(dict.fromkeys(files))


def byte_entropy(data: bytes) -> tuple[float, float]:
    if not data:
        return 0.0, 0.0
    counts = Counter(data)
    total = len(data)
    probs = [count / total for count in counts.values()]
    shannon = -sum(p * math.log2(p) for p in probs if p > 0.0)
    min_entropy = -math.log2(max(probs))
    return shannon, min_entropy


def build_byte_table() -> list[dict[str, int]]:
    table = []
    for byte in range(256):
        bits = [(byte >> shift) & 1 for shift in range(7, -1, -1)]
        runs = 1
        adjacent_equal = 0
        longest = [0, 0]
        current = bits[0]
        current_len = 1
        for bit in bits[1:]:
            if bit == current:
                adjacent_equal += 1
                current_len += 1
            else:
                runs += 1
                longest[current] = max(longest[current], current_len)
                current = bit
                current_len = 1
        longest[current] = max(longest[current], current_len)
        leading_len = 1
        for bit in bits[1:]:
            if bit == bits[0]:
                leading_len += 1
            else:
                break
        trailing_len = 1
        for bit in reversed(bits[:-1]):
            if bit == bits[-1]:
                trailing_len += 1
            else:
                break
        table.append(
            {
                "ones": byte.bit_count(),
                "first": bits[0],
                "last": bits[-1],
                "runs": runs,
                "adjacent_equal": adjacent_equal,
                "longest_zero": longest[0],
                "longest_one": longest[1],
                "leading_len": leading_len,
                "trailing_len": trailing_len,
            }
        )
    return table


BYTE_TABLE = build_byte_table()


def bit_stats(data: bytes) -> dict[str, float | int]:
    n = len(data) * 8
    if n == 0:
        return {
            "bits": 0,
            "zeros": 0,
            "ones": 0,
            "p1": 0.0,
            "bit_min_entropy": 0.0,
            "monobit_z": 0.0,
            "monobit_p": 0.0,
            "runs": 0,
            "runs_p": 0.0,
            "adjacent_equal_ratio": 0.0,
            "longest_zero_run": 0,
            "longest_one_run": 0,
        }

    ones = sum(byte.bit_count() for byte in data)
    zeros = n - ones
    p1 = ones / n
    p0 = zeros / n
    bit_min_entropy = -math.log2(max(p0, p1)) if max(p0, p1) else 0.0
    monobit_z = (ones - zeros) / math.sqrt(n)
    monobit_p = math.erfc(abs(monobit_z) / math.sqrt(2.0))

    prev_last: int | None = None
    runs = 0
    adjacent_equal = 0
    longest = [0, 0]
    boundary_run_bit: int | None = None
    boundary_run_len = 0

    for byte in data:
        item = BYTE_TABLE[byte]
        runs += item["runs"]
        adjacent_equal += item["adjacent_equal"]
        longest[0] = max(longest[0], item["longest_zero"])
        longest[1] = max(longest[1], item["longest_one"])

        first = item["first"]
        last = item["last"]
        if prev_last is not None:
            if first == prev_last:
                runs -= 1
                adjacent_equal += 1
        prev_last = last

        leading_bit = first
        leading_len = item["leading_len"]
        trailing_len = item["trailing_len"]

        if boundary_run_bit == leading_bit:
            longest[leading_bit] = max(longest[leading_bit], boundary_run_len + leading_len)
        if byte in (0x00, 0xFF):
            boundary_run_bit = last
            boundary_run_len += 8
        else:
            boundary_run_bit = last
            boundary_run_len = trailing_len

    if abs(p1 - 0.5) >= 2.0 / math.sqrt(n):
        runs_p = 0.0
    else:
        denom = 2.0 * math.sqrt(2.0 * n) * p1 * (1.0 - p1)
        runs_p = math.erfc(abs(runs - 2.0 * n * p1 * (1.0 - p1)) / denom) if denom else 0.0

    return {
        "bits": n,
        "zeros": zeros,
        "ones": ones,
        "p1": p1,
        "bit_min_entropy": bit_min_entropy,
        "monobit_z": monobit_z,
        "monobit_p": monobit_p,
        "runs": runs,
        "runs_p": runs_p,
        "adjacent_equal_ratio": adjacent_equal / (n - 1) if n > 1 else 0.0,
        "longest_zero_run": longest[0],
        "longest_one_run": longest[1],
    }


def analyze_file(path: Path, max_bytes: int | None) -> dict[str, str | float | int]:
    data = path.read_bytes()
    if max_bytes is not None:
        data = data[:max_bytes]
    shannon_byte, min_byte = byte_entropy(data)
    stats = bit_stats(data)
    return {
        "file": str(path),
        "name": path.name,
        "bytes": len(data),
        **stats,
        "shannon_entropy_byte": shannon_byte,
        "min_entropy_byte": min_byte,
    }


def write_markdown(rows: list[dict[str, str | float | int]], out_path: Path) -> None:
    headers = [
        "name",
        "bytes",
        "p1",
        "bit_min_entropy",
        "monobit_p",
        "runs_p",
        "shannon_entropy_byte",
        "min_entropy_byte",
    ]
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# TRNG Dataset Summary\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in rows:
            cells = []
            for key in headers:
                value = row[key]
                if isinstance(value, float):
                    cells.append(f"{value:.6g}")
                else:
                    cells.append(str(value))
            f.write("| " + " | ".join(cells) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path, help="Input files or directories")
    parser.add_argument("--glob", default="*.DAT", help="Glob used for directory inputs")
    parser.add_argument("--out-dir", type=Path, default=None, help="Directory for CSV/Markdown output")
    parser.add_argument("--max-bytes", type=int, default=None, help="Analyze only the first N bytes per file")
    args = parser.parse_args()

    files = iter_files(args.inputs, args.glob)
    if not files:
        raise SystemExit("No input files found.")

    rows = [analyze_file(path, args.max_bytes) for path in files]

    out_dir = args.out_dir or Path("data") / ("analysis_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "trng_summary.csv"
    md_path = out_dir / "trng_summary.md"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_markdown(rows, md_path)

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
