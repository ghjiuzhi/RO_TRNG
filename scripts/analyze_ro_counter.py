#!/usr/bin/env python3
"""Estimate RO frequency and count-derived jitter from UART counter dumps."""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path


def parse_windows(values: str | None, files: list[Path], default_ns: float) -> dict[str, float]:
    if not values:
        return {path.name: default_ns for path in files}
    items = [item.strip() for item in values.split(",") if item.strip()]
    if all("=" in item for item in items):
        result = {path.name: default_ns for path in files}
        for item in items:
            name, value = item.split("=", 1)
            result[name.strip()] = float(value)
        return result
    numbers = [float(item) for item in items]
    result = {}
    for idx, path in enumerate(files):
        result[path.name] = numbers[idx] if idx < len(numbers) else numbers[-1]
    return result


def read_counts(path: Path, max_samples: int | None, reject_delta: float | None) -> list[int]:
    data = path.read_bytes()
    if max_samples is not None:
        data = data[:max_samples]
    counts = list(data)
    if reject_delta is None or len(counts) < 2:
        return counts
    mean = sum(counts) / len(counts)
    return [count for count in counts if abs(count - mean) <= reject_delta]


def entropy(counts: list[int]) -> tuple[float, float]:
    if not counts:
        return 0.0, 0.0
    total = len(counts)
    probs = [value / total for value in Counter(counts).values()]
    return -sum(p * math.log2(p) for p in probs), -math.log2(max(probs))


def analyze(path: Path, window_ns: float, max_samples: int | None, reject_delta: float | None) -> dict[str, str | float | int]:
    counts = read_counts(path, max_samples, reject_delta)
    raw_samples = min(path.stat().st_size, max_samples) if max_samples else path.stat().st_size
    samples = len(counts)
    if samples == 0:
        mean = variance = freq_mhz = jitter_ps = 0.0
    else:
        mean = sum(counts) / samples
        variance = sum((count - mean) ** 2 for count in counts) / (samples - 1) if samples > 1 else 0.0
        freq_mhz = mean / window_ns * 1000.0 if window_ns else 0.0
        jitter_ps = math.sqrt(variance * (window_ns / (mean * mean)) ** 2) * 1000.0 if mean else 0.0
    shannon, min_ent = entropy(counts)
    return {
        "file": str(path),
        "name": path.name,
        "window_ns": window_ns,
        "raw_samples": raw_samples,
        "kept_samples": samples,
        "mean_count": mean,
        "count_variance": variance,
        "ro_freq_mhz": freq_mhz,
        "jitter_std_ps": jitter_ps,
        "shannon_entropy_count": shannon,
        "min_entropy_count": min_ent,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path, help="Counter files or directories")
    parser.add_argument("--glob", default="RO*.DAT")
    parser.add_argument("--windows-ns", default=None, help="Comma list, or name=value pairs")
    parser.add_argument("--default-window-ns", type=float, default=500.0)
    parser.add_argument("--max-samples", type=int, default=50000)
    parser.add_argument("--reject-delta", type=float, default=10.0)
    parser.add_argument("--out", type=Path, default=Path("data/ro_counter_summary.csv"))
    args = parser.parse_args()

    files: list[Path] = []
    for item in args.inputs:
        if item.is_dir():
            files.extend(sorted(item.glob(args.glob)))
        elif item.is_file():
            files.append(item)
    files = sorted(dict.fromkeys(files))
    if not files:
        raise SystemExit("No counter files found.")

    windows = parse_windows(args.windows_ns, files, args.default_window_ns)
    rows = [analyze(path, windows[path.name], args.max_samples, args.reject_delta) for path in files]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.out}")
    for row in rows:
        print(
            f"{row['name']}: freq={row['ro_freq_mhz']:.3f} MHz, "
            f"jitter={row['jitter_std_ps']:.2f} ps, Hmin_count={row['min_entropy_count']:.3f}"
        )


if __name__ == "__main__":
    main()
