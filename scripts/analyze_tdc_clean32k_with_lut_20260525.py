#!/usr/bin/env python3
"""Re-analyze clean32k reset-aligned TDC captures with fixed calibration LUTs.

This is an offline-only sensitivity check. It does not replace the raw-bin
startup-diffusion tables; it asks whether the hard-lock exclusion still looks
reasonable after mapping bins to code-density phase-center estimates.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Any

import analyze_tdc_uart as tdc_uart


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = (
    ROOT
    / "data"
    / "experiments"
    / "tdc_reset_aligned_clean32k_all_20260525"
    / "tdc_reset_aligned_clean32k_all_20260525.summary.csv"
)
DEFAULT_CAL_DIR = ROOT / "data" / "experiments" / "tdc_code_density_cal_20260525"
DEFAULT_LUT_A = DEFAULT_CAL_DIR / "tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv"
DEFAULT_LUT_B = DEFAULT_CAL_DIR / "tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_clean32k_lut_reanalysis_20260525"


SUMMARY_FIELDS = [
    "label",
    "source",
    "lut_a",
    "lut_b",
    "packets",
    "seq_gaps",
    "phase_period_ps",
    "phase_diff_mean_ps",
    "phase_diff_std_ps",
    "early_phase_diff_std_ps",
    "first_window_phase_diff_std_ps",
    "later_phase_diff_std_ps",
    "first_minus_later_phase_diff_mean_ps",
    "phase_diff_autocorr_lag1",
    "phase_a_b_pearson_r",
    "raw_diff_entropy",
    "raw_same_diff_transition_ratio",
    "raw_longest_same_diff_bin_run",
]

WINDOW_FIELDS = [
    "label",
    "source",
    "window_index",
    "packet_start",
    "packet_end",
    "packets",
    "phase_diff_mean_ps",
    "phase_diff_std_ps",
    "phase_diff_autocorr_lag1",
    "raw_diff_entropy",
    "raw_same_diff_transition_ratio",
    "raw_longest_same_diff_bin_run",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_lut(path: Path) -> dict[int, float]:
    rows = read_csv_rows(path)
    return {int(row["bin"]): float(row["phase_center_ps_nominal"]) for row in rows}


def seq_gaps(packets: list[dict[str, int]]) -> int:
    gaps = 0
    for prev, cur in zip(packets, packets[1:]):
        if cur["seq"] != ((prev["seq"] + 1) & 0xFFFF):
            gaps += 1
    return gaps


def entropy(values: list[int]) -> float:
    if not values:
        return math.nan
    total = len(values)
    return -sum((n / total) * math.log2(n / total) for n in Counter(values).values())


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def sample_std(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def pearson(xs: list[float], ys: list[float]) -> float:
    n = min(len(xs), len(ys))
    if n < 2:
        return math.nan
    x = xs[:n]
    y = ys[:n]
    mx = mean(x)
    my = mean(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else math.nan


def signed_phase_diff(a_ps: float, b_ps: float, period_ps: float) -> float:
    half = period_ps / 2.0
    return ((a_ps - b_ps + half) % period_ps) - half


def signed_bin_diff(a: int, b: int, bins: int) -> int:
    half = bins // 2
    return ((a - b + half) % bins) - half


def same_ratio(values: list[int]) -> float:
    return (
        sum(1 for prev, cur in zip(values, values[1:]) if prev == cur) / (len(values) - 1)
        if len(values) > 1
        else math.nan
    )


def longest_run(values: list[int]) -> int:
    if not values:
        return 0
    longest = 1
    current = 1
    for prev, cur in zip(values, values[1:]):
        if prev == cur:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def fmt(value: Any) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field, "")) for field in fields})


def unique_clean_sources(summary_csv: Path) -> list[dict[str, str]]:
    rows = read_csv_rows(summary_csv)
    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        label = row.get("label", "")
        source = row.get("source", "")
        if not label or not source or label in seen:
            continue
        if row.get("warmup_start") != "0":
            continue
        selected.append({"label": label, "source": source})
        seen.add(label)
    return selected


def analyze_capture(
    label: str,
    source: Path,
    lut_a: dict[int, float],
    lut_b: dict[int, float],
    lut_a_path: Path,
    lut_b_path: Path,
    bins: int,
    period_ps: float,
    early_packets: int,
    window_packets: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    packets = tdc_uart.decode_packets(source.read_bytes(), None)
    if not packets:
        raise ValueError(f"No TDC packets decoded from {source}")
    bin_a = [p["bin_a"] for p in packets]
    bin_b = [p["bin_b"] for p in packets]
    phase_a = [lut_a.get(v, math.nan) for v in bin_a]
    phase_b = [lut_b.get(v, math.nan) for v in bin_b]
    valid = [
        (a_bin, b_bin, a_ps, b_ps)
        for a_bin, b_bin, a_ps, b_ps in zip(bin_a, bin_b, phase_a, phase_b)
        if not math.isnan(a_ps) and not math.isnan(b_ps)
    ]
    raw_diff = [signed_bin_diff(a_bin, b_bin, bins) for a_bin, b_bin, _, _ in valid]
    diff_ps = [signed_phase_diff(a_ps, b_ps, period_ps) for _, _, a_ps, b_ps in valid]
    phase_a_valid = [a_ps for _, _, a_ps, _ in valid]
    phase_b_valid = [b_ps for _, _, _, b_ps in valid]
    first = diff_ps[:window_packets]
    later = diff_ps[window_packets:]

    summary = {
        "label": label,
        "source": str(source),
        "lut_a": str(lut_a_path),
        "lut_b": str(lut_b_path),
        "packets": len(valid),
        "seq_gaps": seq_gaps(packets),
        "phase_period_ps": period_ps,
        "phase_diff_mean_ps": mean(diff_ps),
        "phase_diff_std_ps": sample_std(diff_ps),
        "early_phase_diff_std_ps": sample_std(diff_ps[:early_packets]),
        "first_window_phase_diff_std_ps": sample_std(first),
        "later_phase_diff_std_ps": sample_std(later),
        "first_minus_later_phase_diff_mean_ps": mean(first) - mean(later) if later else math.nan,
        "phase_diff_autocorr_lag1": pearson(diff_ps[:-1], diff_ps[1:]),
        "phase_a_b_pearson_r": pearson(phase_a_valid, phase_b_valid),
        "raw_diff_entropy": entropy(raw_diff),
        "raw_same_diff_transition_ratio": same_ratio(raw_diff),
        "raw_longest_same_diff_bin_run": longest_run(raw_diff),
    }

    windows = []
    for window_index, start in enumerate(range(0, len(diff_ps), window_packets)):
        end = min(start + window_packets, len(diff_ps))
        if end - start < 2:
            continue
        diff_window = diff_ps[start:end]
        raw_window = raw_diff[start:end]
        windows.append(
            {
                "label": label,
                "source": str(source),
                "window_index": window_index,
                "packet_start": start,
                "packet_end": end - 1,
                "packets": len(diff_window),
                "phase_diff_mean_ps": mean(diff_window),
                "phase_diff_std_ps": sample_std(diff_window),
                "phase_diff_autocorr_lag1": pearson(diff_window[:-1], diff_window[1:]),
                "raw_diff_entropy": entropy(raw_window),
                "raw_same_diff_transition_ratio": same_ratio(raw_window),
                "raw_longest_same_diff_bin_run": longest_run(raw_window),
            }
        )
    return summary, windows


def write_markdown(path: Path, summaries: list[dict[str, Any]], lut_a: Path, lut_b: Path) -> None:
    lines = [
        "# Clean32k TDC LUT Reanalysis 20260525",
        "",
        "## Calibration LUTs",
        "",
        f"- lane A LUT: `{lut_a}`",
        f"- lane B LUT: `{lut_b}`",
        "",
        "## Summary",
        "",
        "| label | packets | seq gaps | diff std ps | early diff std ps | autocorr | A/B Pearson r | raw same ratio | raw longest run |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summaries:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["label"]),
                    str(row["packets"]),
                    str(row["seq_gaps"]),
                    fmt(row["phase_diff_std_ps"]),
                    fmt(row["early_phase_diff_std_ps"]),
                    fmt(row["phase_diff_autocorr_lag1"]),
                    fmt(row["phase_a_b_pearson_r"]),
                    fmt(row["raw_same_diff_transition_ratio"]),
                    fmt(row["raw_longest_same_diff_bin_run"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This table applies one fixed code-density LUT pair to the existing clean32k captures; it is a sensitivity check, not a full metrological calibration of every placement-specific TDC build.",
            "- The calibrated phase-difference autocorrelation remains close to zero and the raw same-differential-bin residence indicators remain short, so the earlier conclusion against simple pairwise hard locking is not overturned by the first LUT-based reanalysis.",
            "- The absolute `diff std ps` values should be written cautiously because the LUTs were generated on a dedicated calibration top, not interleaved immediately before and after every clean32k run.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--lut-a", type=Path, default=DEFAULT_LUT_A)
    parser.add_argument("--lut-b", type=Path, default=DEFAULT_LUT_B)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--bins", type=int, default=65)
    parser.add_argument("--period-ps", type=float, default=5000.0)
    parser.add_argument("--early-packets", type=int, default=512)
    parser.add_argument("--window-packets", type=int, default=4096)
    args = parser.parse_args()

    lut_a = load_lut(args.lut_a)
    lut_b = load_lut(args.lut_b)
    summaries: list[dict[str, Any]] = []
    windows: list[dict[str, Any]] = []
    for item in unique_clean_sources(args.summary):
        summary, run_windows = analyze_capture(
            item["label"],
            ROOT / item["source"],
            lut_a,
            lut_b,
            args.lut_a,
            args.lut_b,
            args.bins,
            args.period_ps,
            args.early_packets,
            args.window_packets,
        )
        summaries.append(summary)
        windows.extend(run_windows)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "tdc_clean32k_lut_reanalysis_20260525.summary.csv", summaries, SUMMARY_FIELDS)
    write_csv(args.out_dir / "tdc_clean32k_lut_reanalysis_20260525.windows.csv", windows, WINDOW_FIELDS)
    write_markdown(args.out_dir / "tdc_clean32k_lut_reanalysis_20260525.md", summaries, args.lut_a, args.lut_b)
    print(f"Wrote {args.out_dir}")


if __name__ == "__main__":
    main()
