#!/usr/bin/env python3
"""Decode RO_TDC_sysclk_top UART packets and extract TDC metrics.

The script supports raw 8-byte UART frames emitted by tdc_uart_packetizer and
packet CSV files previously produced by this script.  It writes packet, bin
calibration, metric CSV, and Markdown summaries using only the Python standard
library.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Iterable


PACKET_FIELDS = ["seq", "coarse_lsb", "bin_a", "bin_b", "flags"]
METRIC_FIELDS = [
    "run",
    "source",
    "packets",
    "seq_gaps",
    "seq_wraps",
    "clock_period_ps",
    "bins",
    "lane_a_mean_bin",
    "lane_a_std_bin",
    "lane_a_shannon_bin",
    "lane_a_min_entropy_bin",
    "lane_a_used_bins",
    "lane_a_dead_bins",
    "lane_a_max_dnl_lsb",
    "lane_a_min_dnl_lsb",
    "lane_a_peak_abs_inl_lsb",
    "lane_a_mean_phase_ps",
    "lane_a_std_phase_ps",
    "lane_b_mean_bin",
    "lane_b_std_bin",
    "lane_b_shannon_bin",
    "lane_b_min_entropy_bin",
    "lane_b_used_bins",
    "lane_b_dead_bins",
    "lane_b_max_dnl_lsb",
    "lane_b_min_dnl_lsb",
    "lane_b_peak_abs_inl_lsb",
    "lane_b_mean_phase_ps",
    "lane_b_std_phase_ps",
    "diff_mean_bin",
    "diff_std_bin",
    "diff_mean_ps",
    "diff_std_ps",
    "bin_pearson_r",
    "phase_pearson_r",
    "coarse_lsb_std",
    "flag_nonzero_ratio",
]


def decode_packets(data: bytes, max_packets: int | None = None) -> list[dict[str, int]]:
    packets: list[dict[str, int]] = []
    i = 0
    while i + 8 <= len(data):
        if data[i] != 0xA5:
            i += 1
            continue
        frame = data[i:i + 8]
        seq = frame[1] | (frame[2] << 8)
        coarse = frame[3] | (frame[4] << 8)
        packets.append(
            {
                "seq": seq,
                "coarse_lsb": coarse,
                "bin_a": frame[5],
                "bin_b": frame[6],
                "flags": frame[7],
            }
        )
        if max_packets is not None and len(packets) >= max_packets:
            break
        i += 8
    return packets


def read_packet_csv(path: Path, max_packets: int | None = None) -> list[dict[str, int]]:
    packets: list[dict[str, int]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            packets.append({field: int(row[field]) for field in PACKET_FIELDS})
            if max_packets is not None and len(packets) >= max_packets:
                break
    return packets


def read_packets(path: Path, fmt: str, max_packets: int | None) -> list[dict[str, int]]:
    if fmt == "csv" or (fmt == "auto" and path.suffix.lower() == ".csv"):
        return read_packet_csv(path, max_packets)
    return decode_packets(path.read_bytes(), max_packets)


def mean(values: list[float] | list[int]) -> float:
    return sum(values) / len(values) if values else 0.0


def sample_std(values: list[float] | list[int]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def entropy(values: list[int]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    total = len(values)
    probs = [count / total for count in Counter(values).values()]
    return -sum(p * math.log2(p) for p in probs), -math.log2(max(probs))


def pearson(x_values: list[float] | list[int], y_values: list[float] | list[int]) -> float:
    n = min(len(x_values), len(y_values))
    if n < 2:
        return 0.0
    xs = [float(v) for v in x_values[:n]]
    ys = [float(v) for v in y_values[:n]]
    mx = mean(xs)
    my = mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx and sy else 0.0


def signed_bin_diff(a: int, b: int, bins: int) -> int:
    half = bins // 2
    return ((a - b + half) % bins) - half


def infer_bin_count(packets: list[dict[str, int]], requested: int | None) -> int:
    if requested:
        return requested
    max_code = 0
    for packet in packets:
        max_code = max(max_code, packet["bin_a"], packet["bin_b"])
    bins = 1
    while bins <= max_code:
        bins <<= 1
    return max(2, bins)


def code_density(values: list[int], bins: int, clock_period_ps: float) -> list[dict[str, float | int]]:
    counts = Counter(v for v in values if 0 <= v < bins)
    total = sum(counts.values())
    ideal_count = total / bins if bins else 0.0
    ideal_width_ps = clock_period_ps / bins if bins else 0.0
    rows: list[dict[str, float | int]] = []
    cumulative_width_ps = 0.0
    cumulative_dnl = 0.0
    for code in range(bins):
        count = counts.get(code, 0)
        width_ps = (count / total * clock_period_ps) if total else 0.0
        dnl_lsb = (count / ideal_count - 1.0) if ideal_count else 0.0
        phase_center_ps = cumulative_width_ps + 0.5 * width_ps
        cumulative_dnl += dnl_lsb
        rows.append(
            {
                "bin": code,
                "count": count,
                "probability": count / total if total else 0.0,
                "width_ps": width_ps,
                "ideal_width_ps": ideal_width_ps,
                "dnl_lsb": dnl_lsb,
                "inl_lsb": cumulative_dnl,
                "phase_center_ps": phase_center_ps,
            }
        )
        cumulative_width_ps += width_ps
    return rows


def phase_lookup(calibration: list[dict[str, float | int]]) -> dict[int, float]:
    return {int(row["bin"]): float(row["phase_center_ps"]) for row in calibration}


def lane_metrics(name: str, values: list[int], calibration: list[dict[str, float | int]]) -> dict[str, float | int]:
    shannon, hmin = entropy(values)
    phases_by_bin = phase_lookup(calibration)
    phases = [phases_by_bin.get(v, 0.0) for v in values]
    dnl = [float(row["dnl_lsb"]) for row in calibration]
    inl = [float(row["inl_lsb"]) for row in calibration]
    used = sum(1 for row in calibration if int(row["count"]) > 0)
    return {
        f"{name}_mean_bin": mean(values),
        f"{name}_std_bin": sample_std(values),
        f"{name}_shannon_bin": shannon,
        f"{name}_min_entropy_bin": hmin,
        f"{name}_used_bins": used,
        f"{name}_dead_bins": len(calibration) - used,
        f"{name}_max_dnl_lsb": max(dnl) if dnl else 0.0,
        f"{name}_min_dnl_lsb": min(dnl) if dnl else 0.0,
        f"{name}_peak_abs_inl_lsb": max((abs(v) for v in inl), default=0.0),
        f"{name}_mean_phase_ps": mean(phases),
        f"{name}_std_phase_ps": sample_std(phases),
    }


def sequence_metrics(packets: list[dict[str, int]]) -> tuple[int, int]:
    gaps = 0
    wraps = 0
    for prev, cur in zip(packets, packets[1:]):
        expected = (prev["seq"] + 1) & 0xFFFF
        if cur["seq"] == 0 and prev["seq"] == 0xFFFF:
            wraps += 1
        elif cur["seq"] != expected:
            gaps += 1
    return gaps, wraps


def summarize(
    packets: list[dict[str, int]],
    source: Path,
    run: str,
    bins: int,
    clock_period_ps: float,
) -> tuple[dict[str, str | float | int], list[dict[str, float | int]], list[dict[str, float | int]]]:
    bin_a = [p["bin_a"] for p in packets]
    bin_b = [p["bin_b"] for p in packets]
    coarse = [p["coarse_lsb"] for p in packets]
    flags = [p["flags"] for p in packets]

    cal_a = code_density(bin_a, bins, clock_period_ps)
    cal_b = code_density(bin_b, bins, clock_period_ps)
    phase_a = phase_lookup(cal_a)
    phase_b = phase_lookup(cal_b)
    phases_a = [phase_a.get(v, 0.0) for v in bin_a]
    phases_b = [phase_b.get(v, 0.0) for v in bin_b]
    diff_bins = [signed_bin_diff(a, b, bins) for a, b in zip(bin_a, bin_b)]
    diff_ps = [a - b for a, b in zip(phases_a, phases_b)]
    seq_gaps, seq_wraps = sequence_metrics(packets)

    metrics: dict[str, str | float | int] = {
        "run": run,
        "source": str(source),
        "packets": len(packets),
        "seq_gaps": seq_gaps,
        "seq_wraps": seq_wraps,
        "clock_period_ps": clock_period_ps,
        "bins": bins,
        **lane_metrics("lane_a", bin_a, cal_a),
        **lane_metrics("lane_b", bin_b, cal_b),
        "diff_mean_bin": mean(diff_bins),
        "diff_std_bin": sample_std(diff_bins),
        "diff_mean_ps": mean(diff_ps),
        "diff_std_ps": sample_std(diff_ps),
        "bin_pearson_r": pearson(bin_a, bin_b),
        "phase_pearson_r": pearson(phases_a, phases_b),
        "coarse_lsb_std": sample_std(coarse),
        "flag_nonzero_ratio": sum(1 for flag in flags if flag) / len(flags) if flags else 0.0,
    }

    return metrics, cal_a, cal_b


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    metrics: dict[str, str | float | int],
    cal_a: list[dict[str, float | int]],
    cal_b: list[dict[str, float | int]],
) -> None:
    rows = [
        ("packets", metrics["packets"]),
        ("seq_gaps", metrics["seq_gaps"]),
        ("lane_a_std_phase_ps", metrics["lane_a_std_phase_ps"]),
        ("lane_b_std_phase_ps", metrics["lane_b_std_phase_ps"]),
        ("diff_std_ps", metrics["diff_std_ps"]),
        ("bin_pearson_r", metrics["bin_pearson_r"]),
        ("phase_pearson_r", metrics["phase_pearson_r"]),
        ("lane_a_peak_abs_inl_lsb", metrics["lane_a_peak_abs_inl_lsb"]),
        ("lane_b_peak_abs_inl_lsb", metrics["lane_b_peak_abs_inl_lsb"]),
    ]
    with path.open("w", encoding="utf-8") as f:
        f.write("# TDC Calibration and Metrics\n\n")
        f.write(f"- run: `{metrics['run']}`\n")
        f.write(f"- source: `{metrics['source']}`\n")
        f.write(f"- clock_period_ps: {float(metrics['clock_period_ps']):.6g}\n")
        f.write(f"- bins: {metrics['bins']}\n\n")
        f.write("| metric | value |\n")
        f.write("| --- | ---: |\n")
        for key, value in rows:
            if isinstance(value, float):
                f.write(f"| {key} | {value:.6g} |\n")
            else:
                f.write(f"| {key} | {value} |\n")
        f.write("\n## Code-Density Extremes\n\n")
        f.write("| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |\n")
        f.write("| --- | ---: | ---: | ---: | ---: |\n")
        for lane, cal in [("A", cal_a), ("B", cal_b)]:
            dnl = [float(row["dnl_lsb"]) for row in cal]
            inl = [float(row["inl_lsb"]) for row in cal]
            dead = sum(1 for row in cal if int(row["count"]) == 0)
            f.write(
                f"| {lane} | {dead} | {min(dnl, default=0.0):.6g} | "
                f"{max(dnl, default=0.0):.6g} | {max((abs(v) for v in inl), default=0.0):.6g} |\n"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Raw UART dump or packet CSV")
    parser.add_argument("--format", choices=["auto", "raw", "csv"], default="auto")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--prefix", default=None)
    parser.add_argument("--run", default=None, help="Run label stored in metrics")
    parser.add_argument("--clock-period-ps", type=float, default=10000.0)
    parser.add_argument("--bins", type=int, default=None, help="TDC code count; default infers power of two")
    parser.add_argument("--max-packets", type=int, default=None)
    args = parser.parse_args()

    packets = read_packets(args.input, args.format, args.max_packets)
    if not packets:
        raise SystemExit("No TDC packets decoded.")

    bins = infer_bin_count(packets, args.bins)
    run = args.run or args.input.stem
    out_dir = args.out_dir or args.input.parent
    prefix = args.prefix or args.input.stem

    metrics, cal_a, cal_b = summarize(packets, args.input, run, bins, args.clock_period_ps)
    packet_csv = out_dir / f"{prefix}.tdc_packets.csv"
    bin_csv = out_dir / f"{prefix}.tdc_bins.csv"
    metrics_csv = out_dir / f"{prefix}.tdc_metrics.csv"
    md_path = out_dir / f"{prefix}.tdc_summary.md"

    write_csv(packet_csv, packets, PACKET_FIELDS)
    bin_rows: list[dict[str, float | int | str]] = []
    for lane, rows in [("a", cal_a), ("b", cal_b)]:
        for row in rows:
            bin_rows.append({"run": run, "lane": lane, **row})
    write_csv(
        bin_csv,
        bin_rows,
        ["run", "lane", "bin", "count", "probability", "width_ps", "ideal_width_ps", "dnl_lsb", "inl_lsb", "phase_center_ps"],
    )
    write_csv(metrics_csv, [metrics], METRIC_FIELDS)
    write_markdown(md_path, metrics, cal_a, cal_b)

    print(f"Wrote {packet_csv}")
    print(f"Wrote {bin_csv}")
    print(f"Wrote {metrics_csv}")
    print(f"Wrote {md_path}")
    print(
        f"{run}: packets={metrics['packets']}, "
        f"diff_std_ps={float(metrics['diff_std_ps']):.3f}, "
        f"phase_r={float(metrics['phase_pearson_r']):.4f}"
    )


if __name__ == "__main__":
    main()
