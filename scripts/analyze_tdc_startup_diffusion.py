#!/usr/bin/env python3
"""Offline startup-diffusion analysis for existing TDC UART captures.

This script reads the same raw 8-byte UART frames or packet CSV files handled by
analyze_tdc_uart.py. It computes reset/warmup startup diffusion indicators from
the decoded A/B TDC bins and their signed differential bin sequence.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import analyze_tdc_uart as tdc_uart


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_startup_diffusion_20260523"

SUMMARY_FIELDS = [
    "label",
    "run",
    "source",
    "source_format",
    "tdcr_header_found",
    "tdcr_version",
    "tdcr_pair_id",
    "tdcr_family_id",
    "tdcr_warmup_packets",
    "tdcr_capture_packets",
    "tdcr_sample_div",
    "packets",
    "seq_gaps",
    "seq_wraps",
    "enable_edge_index",
    "pre_enable_packets",
    "post_enable_packets",
    "bins",
    "warmup_start",
    "early_packets",
    "window_packets",
    "lag",
    "entropy_a",
    "entropy_b",
    "entropy_diff",
    "min_entropy_a",
    "min_entropy_b",
    "min_entropy_diff",
    "early_entropy_a",
    "early_entropy_b",
    "early_entropy_diff",
    "early_min_entropy_a",
    "early_min_entropy_b",
    "early_min_entropy_diff",
    "transition_entropy_diff",
    "transition_min_entropy_diff",
    "same_diff_transition_ratio",
    "residence_runs",
    "residence_mean_len",
    "residence_median_len",
    "residence_p95_len",
    "longest_same_diff_bin_run",
    "autocorr_diff_lag",
    "autocorr_a_lag",
    "autocorr_b_lag",
    "first_window_packets",
    "later_window_packets",
    "first_entropy_a",
    "first_entropy_b",
    "first_entropy_diff",
    "later_entropy_a",
    "later_entropy_b",
    "later_entropy_diff",
    "first_minus_later_entropy_a",
    "first_minus_later_entropy_b",
    "first_minus_later_entropy_diff",
    "first_later_tvd_a",
    "first_later_tvd_b",
    "first_later_tvd_diff",
    "first_diff_mean_bin",
    "later_diff_mean_bin",
    "first_minus_later_diff_mean_bin",
    "warmup_packets",
    "warmup_entropy_a",
    "warmup_entropy_b",
    "warmup_entropy_diff",
    "warmup_transition_entropy_diff",
    "warmup_same_diff_transition_ratio",
    "warmup_longest_same_diff_bin_run",
    "warmup_autocorr_diff_lag",
]

WINDOW_FIELDS = [
    "label",
    "run",
    "source",
    "window_index",
    "packet_start",
    "packet_end",
    "packets",
    "entropy_a",
    "entropy_b",
    "entropy_diff",
    "min_entropy_a",
    "min_entropy_b",
    "min_entropy_diff",
    "transition_entropy_diff",
    "same_diff_transition_ratio",
    "longest_same_diff_bin_run",
    "autocorr_diff_lag",
    "diff_mean_bin",
    "diff_std_bin",
]


def read_packets(path: Path, fmt: str, max_packets: int | None) -> tuple[list[dict[str, int]], str]:
    if fmt == "csv" or (fmt == "auto" and path.suffix.lower() == ".csv"):
        return tdc_uart.read_packet_csv(path, max_packets), "csv"
    return tdc_uart.decode_packets(path.read_bytes(), max_packets), "raw"


def read_tdcr_header(path: Path, fmt: str) -> dict[str, Any]:
    fields = {
        "tdcr_header_found": 0,
        "tdcr_version": "",
        "tdcr_pair_id": "",
        "tdcr_family_id": "",
        "tdcr_warmup_packets": "",
        "tdcr_capture_packets": "",
        "tdcr_sample_div": "",
    }
    if fmt == "csv" or (fmt == "auto" and path.suffix.lower() == ".csv"):
        return fields
    data = path.read_bytes()[:16]
    if len(data) < 16 or data[:4] != b"TDCR" or data[15] != 0x52:
        return fields
    fields.update(
        {
            "tdcr_header_found": 1,
            "tdcr_version": data[4],
            "tdcr_pair_id": data[5] | (data[6] << 8),
            "tdcr_family_id": data[7] | (data[8] << 8),
            "tdcr_warmup_packets": data[9] | (data[10] << 8),
            "tdcr_capture_packets": data[11] | (data[12] << 8),
            "tdcr_sample_div": data[13] | (data[14] << 8),
        }
    )
    return fields


def read_metrics_metadata(input_path: Path) -> tuple[int | None, float | None]:
    metrics_path: Path | None = None
    if input_path.suffix.lower() == ".csv" and input_path.name.endswith(".tdc_packets.csv"):
        metrics_path = input_path.with_name(input_path.name.replace(".tdc_packets.csv", ".tdc_metrics.csv"))
    elif input_path.suffix.lower() == ".bin":
        candidate = input_path.parent / f"analysis_{input_path.stem}" / f"{input_path.stem}.tdc_metrics.csv"
        if candidate.exists():
            metrics_path = candidate
    if not metrics_path or not metrics_path.exists():
        return None, None
    with metrics_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None, None
    row = rows[0]
    bins = int(float(row["bins"])) if row.get("bins") else None
    clock = float(row["clock_period_ps"]) if row.get("clock_period_ps") else None
    return bins, clock


def entropy(values: list[int]) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    total = len(values)
    probs = [count / total for count in Counter(values).values()]
    return -sum(p * math.log2(p) for p in probs), -math.log2(max(probs))


def mean(values: list[int] | list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def sample_std(values: list[int] | list[float]) -> float:
    if len(values) < 2:
        return math.nan
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def percentile(values: list[int], pct: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    pos = (len(ordered) - 1) * pct
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(ordered[lo])
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def pearson(x_values: list[int] | list[float], y_values: list[int] | list[float]) -> float:
    n = min(len(x_values), len(y_values))
    if n < 2:
        return math.nan
    xs = [float(v) for v in x_values[:n]]
    ys = [float(v) for v in y_values[:n]]
    mx = mean(xs)
    my = mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx and sy else math.nan


def signed_bin_diff(a: int, b: int, bins: int) -> int:
    half = bins // 2
    return ((a - b + half) % bins) - half


def transition_values(values: list[int]) -> list[int]:
    if len(values) < 2:
        return []
    return [((prev & 0xFFFF) << 16) | (cur & 0xFFFF) for prev, cur in zip(values, values[1:])]


def residence_lengths(values: list[int]) -> list[int]:
    if not values:
        return []
    lengths: list[int] = []
    current = values[0]
    run_len = 1
    for value in values[1:]:
        if value == current:
            run_len += 1
        else:
            lengths.append(run_len)
            current = value
            run_len = 1
    lengths.append(run_len)
    return lengths


def total_variation_distance(left: list[int], right: list[int]) -> float:
    if not left or not right:
        return math.nan
    left_counts = Counter(left)
    right_counts = Counter(right)
    keys = set(left_counts) | set(right_counts)
    left_n = len(left)
    right_n = len(right)
    return 0.5 * sum(abs(left_counts.get(k, 0) / left_n - right_counts.get(k, 0) / right_n) for k in keys)


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


def find_enable_edge(packets: list[dict[str, int]]) -> int | None:
    prev_enabled = bool(packets[0]["flags"] & 0x01) if packets else False
    if prev_enabled:
        return 0
    for index, packet in enumerate(packets[1:], start=1):
        enabled = bool(packet["flags"] & 0x01)
        if enabled and not prev_enabled:
            return index
        prev_enabled = enabled
    return None


def run_name(input_path: Path) -> str:
    if input_path.name.endswith(".tdc_packets.csv"):
        return input_path.name.replace(".tdc_packets.csv", "")
    return input_path.stem


def format_label(input_path: Path, labels: list[str] | None, index: int) -> str:
    if labels and index < len(labels):
        return labels[index]
    if labels and len(labels) == 1:
        return labels[0]
    return run_name(input_path)


def basic_sequence_metrics(values: list[int], lag: int) -> dict[str, float | int]:
    shannon, hmin = entropy(values)
    transitions = transition_values(values)
    trans_entropy, trans_hmin = entropy(transitions)
    residences = residence_lengths(values)
    same_ratio = sum(1 for prev, cur in zip(values, values[1:]) if prev == cur) / (len(values) - 1) if len(values) > 1 else math.nan
    autocorr = pearson(values[:-lag], values[lag:]) if lag > 0 and len(values) > lag else math.nan
    return {
        "entropy": shannon,
        "min_entropy": hmin,
        "transition_entropy": trans_entropy,
        "transition_min_entropy": trans_hmin,
        "same_transition_ratio": same_ratio,
        "residence_runs": len(residences),
        "residence_mean_len": mean(residences),
        "residence_median_len": statistics.median(residences) if residences else math.nan,
        "residence_p95_len": percentile(residences, 0.95),
        "longest_run": max(residences, default=0),
        "autocorr": autocorr,
    }


def window_row(
    label: str,
    run: str,
    source: Path,
    window_index: int,
    start: int,
    bin_a: list[int],
    bin_b: list[int],
    diff_bins: list[int],
    lag: int,
) -> dict[str, Any]:
    end = start + len(diff_bins)
    ha, hmina = entropy(bin_a)
    hb, hminb = entropy(bin_b)
    hd, hmind = entropy(diff_bins)
    diff_stats = basic_sequence_metrics(diff_bins, lag)
    return {
        "label": label,
        "run": run,
        "source": str(source),
        "window_index": window_index,
        "packet_start": start,
        "packet_end": end - 1,
        "packets": len(diff_bins),
        "entropy_a": ha,
        "entropy_b": hb,
        "entropy_diff": hd,
        "min_entropy_a": hmina,
        "min_entropy_b": hminb,
        "min_entropy_diff": hmind,
        "transition_entropy_diff": diff_stats["transition_entropy"],
        "same_diff_transition_ratio": diff_stats["same_transition_ratio"],
        "longest_same_diff_bin_run": diff_stats["longest_run"],
        "autocorr_diff_lag": diff_stats["autocorr"],
        "diff_mean_bin": mean(diff_bins),
        "diff_std_bin": sample_std(diff_bins),
    }


def analyze_one(
    input_path: Path,
    label: str,
    fmt: str,
    early_packets: int,
    window_packets: int,
    lag: int,
    bins_arg: int | None,
    max_packets: int | None,
    warmup_start: int,
    predecoded: tuple[list[dict[str, int]], str, dict[str, Any], int | None] | None = None,
    include_windows: bool = True,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if predecoded is None:
        packets, source_format = read_packets(input_path, fmt, max_packets)
        tdcr_header = read_tdcr_header(input_path, fmt)
        meta_bins, _ = read_metrics_metadata(input_path)
    else:
        packets, source_format, tdcr_header, meta_bins = predecoded
    if not packets:
        raise ValueError(f"No TDC packets decoded from {input_path}")

    bins = bins_arg or meta_bins or tdc_uart.infer_bin_count(packets, None)
    seq_gaps, seq_wraps = sequence_metrics(packets)
    enable_edge = find_enable_edge(packets)
    align_index = enable_edge if enable_edge is not None else 0
    run = run_name(input_path)
    aligned_packets = packets[align_index:]
    bin_a = [packet["bin_a"] for packet in aligned_packets]
    bin_b = [packet["bin_b"] for packet in aligned_packets]
    diff_bins = [signed_bin_diff(a, b, bins) for a, b in zip(bin_a, bin_b)]

    ha, hmina = entropy(bin_a)
    hb, hminb = entropy(bin_b)
    hd, hmind = entropy(diff_bins)
    early_n = min(early_packets, len(packets))
    early_a = bin_a[:early_n]
    early_b = bin_b[:early_n]
    early_d = diff_bins[:early_n]
    eha, ehmina = entropy(early_a)
    ehb, ehminb = entropy(early_b)
    ehd, ehmind = entropy(early_d)

    diff_stats = basic_sequence_metrics(diff_bins, lag)
    autocorr_a = pearson(bin_a[:-lag], bin_a[lag:]) if lag > 0 and len(bin_a) > lag else math.nan
    autocorr_b = pearson(bin_b[:-lag], bin_b[lag:]) if lag > 0 and len(bin_b) > lag else math.nan

    first_n = min(window_packets, len(aligned_packets))
    first_a = bin_a[:first_n]
    first_b = bin_b[:first_n]
    first_d = diff_bins[:first_n]
    later_a = bin_a[first_n:]
    later_b = bin_b[first_n:]
    later_d = diff_bins[first_n:]
    fha, _ = entropy(first_a)
    fhb, _ = entropy(first_b)
    fhd, _ = entropy(first_d)
    lha, _ = entropy(later_a)
    lhb, _ = entropy(later_b)
    lhd, _ = entropy(later_d)
    selected_warmup_start = min(warmup_start, len(diff_bins))
    warmup_end = min(selected_warmup_start + early_packets, len(diff_bins))
    warmup_a = bin_a[selected_warmup_start:warmup_end]
    warmup_b = bin_b[selected_warmup_start:warmup_end]
    warmup_d = diff_bins[selected_warmup_start:warmup_end]
    wha, _ = entropy(warmup_a)
    whb, _ = entropy(warmup_b)
    whd, _ = entropy(warmup_d)
    warmup_stats = basic_sequence_metrics(warmup_d, lag)

    summary = {
        "label": label,
        "run": run,
        "source": str(input_path),
        "source_format": source_format,
        **tdcr_header,
        "packets": len(packets),
        "seq_gaps": seq_gaps,
        "seq_wraps": seq_wraps,
        "enable_edge_index": enable_edge if enable_edge is not None else "",
        "pre_enable_packets": align_index,
        "post_enable_packets": len(aligned_packets),
        "bins": bins,
        "warmup_start": selected_warmup_start,
        "early_packets": early_n,
        "window_packets": window_packets,
        "lag": lag,
        "entropy_a": ha,
        "entropy_b": hb,
        "entropy_diff": hd,
        "min_entropy_a": hmina,
        "min_entropy_b": hminb,
        "min_entropy_diff": hmind,
        "early_entropy_a": eha,
        "early_entropy_b": ehb,
        "early_entropy_diff": ehd,
        "early_min_entropy_a": ehmina,
        "early_min_entropy_b": ehminb,
        "early_min_entropy_diff": ehmind,
        "transition_entropy_diff": diff_stats["transition_entropy"],
        "transition_min_entropy_diff": diff_stats["transition_min_entropy"],
        "same_diff_transition_ratio": diff_stats["same_transition_ratio"],
        "residence_runs": diff_stats["residence_runs"],
        "residence_mean_len": diff_stats["residence_mean_len"],
        "residence_median_len": diff_stats["residence_median_len"],
        "residence_p95_len": diff_stats["residence_p95_len"],
        "longest_same_diff_bin_run": diff_stats["longest_run"],
        "autocorr_diff_lag": diff_stats["autocorr"],
        "autocorr_a_lag": autocorr_a,
        "autocorr_b_lag": autocorr_b,
        "first_window_packets": first_n,
        "later_window_packets": len(later_d),
        "first_entropy_a": fha,
        "first_entropy_b": fhb,
        "first_entropy_diff": fhd,
        "later_entropy_a": lha,
        "later_entropy_b": lhb,
        "later_entropy_diff": lhd,
        "first_minus_later_entropy_a": fha - lha if not math.isnan(lha) else math.nan,
        "first_minus_later_entropy_b": fhb - lhb if not math.isnan(lhb) else math.nan,
        "first_minus_later_entropy_diff": fhd - lhd if not math.isnan(lhd) else math.nan,
        "first_later_tvd_a": total_variation_distance(first_a, later_a),
        "first_later_tvd_b": total_variation_distance(first_b, later_b),
        "first_later_tvd_diff": total_variation_distance(first_d, later_d),
        "first_diff_mean_bin": mean(first_d),
        "later_diff_mean_bin": mean(later_d),
        "first_minus_later_diff_mean_bin": mean(first_d) - mean(later_d) if later_d else math.nan,
        "warmup_packets": len(warmup_d),
        "warmup_entropy_a": wha,
        "warmup_entropy_b": whb,
        "warmup_entropy_diff": whd,
        "warmup_transition_entropy_diff": warmup_stats["transition_entropy"],
        "warmup_same_diff_transition_ratio": warmup_stats["same_transition_ratio"],
        "warmup_longest_same_diff_bin_run": warmup_stats["longest_run"],
        "warmup_autocorr_diff_lag": warmup_stats["autocorr"],
    }

    windows: list[dict[str, Any]] = []
    if include_windows:
        for window_index, start in enumerate(range(0, len(aligned_packets), window_packets)):
            end = min(start + window_packets, len(aligned_packets))
            if end - start < 2:
                continue
            windows.append(
                window_row(
                    label,
                    run,
                    input_path,
                    window_index,
                    align_index + start,
                    bin_a[start:end],
                    bin_b[start:end],
                    diff_bins[start:end],
                    lag,
                )
            )
    return summary, windows


def fmt(value: Any) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field, "")) for field in fieldnames})


def write_markdown(path: Path, summaries: list[dict[str, Any]], windows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# TDC Startup Diffusion Summary\n\n")
        f.write("Offline analysis of existing TDC UART captures. No RTL, Vivado, COM, JTAG, or hardware queue access is used.\n\n")
        f.write("## Method\n\n")
        f.write("- Decode raw TDC UART frames with the same 8-byte `0xA5` packet format used by `scripts/analyze_tdc_uart.py`, or read existing `.tdc_packets.csv` files.\n")
        f.write("- Compute entropy on lane A bins, lane B bins, and signed wrapped `A-B` differential bins.\n")
        f.write("- Treat the first `--early-packets` packets as the startup slice, and the first `--window-packets` packets as the first-window comparator against all later packets.\n")
        f.write("- `warmup H(diff)` is computed from each requested `--warmup-starts` offset after the enable edge, using the same `--early-packets` window length.\n")
        f.write("- Transition entropy is measured on consecutive differential-bin pairs; residence metrics summarize consecutive runs of identical differential bins.\n\n")
        f.write("## Run Summary\n\n")
        f.write("| label | run | enable edge | post packets | warmup start | H(diff) | early H(diff) | warmup H(diff) | transition H(diff) | warmup transition H(diff) | same diff ratio | warmup same ratio | longest diff run | warmup longest run | diff autocorr | first-later H(diff) | first-later TVD(diff) |\n")
        f.write("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for row in summaries:
            f.write(
                f"| {row['label']} | {row['run']} | {row.get('enable_edge_index', '')} | {row.get('post_enable_packets', '')} | "
                f"{row.get('warmup_start', '')} | {float(row['entropy_diff']):.6g} | {float(row['early_entropy_diff']):.6g} | "
                f"{float(row['warmup_entropy_diff']):.6g} | {float(row['transition_entropy_diff']):.6g} | "
                f"{float(row['warmup_transition_entropy_diff']):.6g} | "
                f"{float(row['same_diff_transition_ratio']):.6g} | {float(row['warmup_same_diff_transition_ratio']):.6g} | "
                f"{row['longest_same_diff_bin_run']} | {row['warmup_longest_same_diff_bin_run']} | "
                f"{float(row['autocorr_diff_lag']):.6g} | {float(row['first_minus_later_entropy_diff']):.6g} | "
                f"{float(row['first_later_tvd_diff']):.6g} |\n"
            )
        f.write("\n## Window Output\n\n")
        f.write(f"- summary rows: `{len(summaries)}`\n")
        f.write(f"- window rows: `{len(windows)}`\n")
        f.write("- CSV files are written next to this Markdown file in the selected `--out-dir`.\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", required=True, help="Raw UART .bin or .tdc_packets.csv. May be repeated.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--label", action="append", default=None, help="Optional label for an input. May be repeated in input order.")
    parser.add_argument("--format", choices=["auto", "raw", "csv"], default="auto")
    parser.add_argument("--early-packets", type=int, default=1024)
    parser.add_argument("--window-packets", type=int, default=16384)
    parser.add_argument(
        "--warmup-starts",
        default="12",
        help="Comma-separated packet offsets after the enable edge for warmup-window analysis.",
    )
    parser.add_argument("--lag", type=int, default=1, help="Positive packet lag for small-lag autocorrelation.")
    parser.add_argument("--bins", type=int, default=None)
    parser.add_argument("--max-packets", type=int, default=None)
    parser.add_argument("--prefix", default="tdc_startup_diffusion")
    args = parser.parse_args()

    if args.early_packets < 2:
        raise SystemExit("--early-packets must be at least 2")
    if args.window_packets < 2:
        raise SystemExit("--window-packets must be at least 2")
    if args.lag < 1:
        raise SystemExit("--lag must be at least 1")
    if args.label and len(args.label) not in (1, len(args.input)):
        raise SystemExit("--label may be supplied once for all inputs or once per --input")
    try:
        warmup_starts = [int(text.strip()) for text in args.warmup_starts.split(",") if text.strip() != ""]
    except ValueError as exc:
        raise SystemExit("--warmup-starts must be a comma-separated list of non-negative integers") from exc
    if not warmup_starts:
        raise SystemExit("--warmup-starts must contain at least one value")
    if any(value < 0 for value in warmup_starts):
        raise SystemExit("--warmup-starts values must be non-negative")

    summaries: list[dict[str, Any]] = []
    windows: list[dict[str, Any]] = []
    for index, input_path in enumerate(args.input):
        label = format_label(input_path, args.label, index)
        packets, source_format = read_packets(input_path, args.format, args.max_packets)
        predecoded = (
            packets,
            source_format,
            read_tdcr_header(input_path, args.format),
            read_metrics_metadata(input_path)[0],
        )
        for warmup_index, warmup_start in enumerate(warmup_starts):
            summary, run_windows = analyze_one(
                input_path,
                label,
                args.format,
                args.early_packets,
                args.window_packets,
                args.lag,
                args.bins,
                args.max_packets,
                warmup_start,
                predecoded=predecoded,
                include_windows=(warmup_index == 0),
            )
            summaries.append(summary)
            windows.extend(run_windows)

    summary_csv = args.out_dir / f"{args.prefix}.summary.csv"
    window_csv = args.out_dir / f"{args.prefix}.windows.csv"
    md_path = args.out_dir / f"{args.prefix}.summary.md"
    write_csv(summary_csv, summaries, SUMMARY_FIELDS)
    write_csv(window_csv, windows, WINDOW_FIELDS)
    write_markdown(md_path, summaries, windows)

    print(f"Wrote {summary_csv}")
    print(f"Wrote {window_csv}")
    print(f"Wrote {md_path}")
    print(f"runs={len(summaries)}, windows={len(windows)}, packets={sum(int(row['packets']) for row in summaries)}")


if __name__ == "__main__":
    main()
