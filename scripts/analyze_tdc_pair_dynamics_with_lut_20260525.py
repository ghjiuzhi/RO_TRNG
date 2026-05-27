#!/usr/bin/env python3
"""Re-analyze pair-specific TDC dynamics with fixed code-density LUTs.

The original pair-dynamics script builds a code-density phase lookup from each
run itself. This script is an offline sensitivity check that instead applies a
fixed external LUT pair from the dedicated TDC calibration captures.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Any, Iterable

import analyze_tdc_pair_dynamics as pair_dyn


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "tdc_pairs"
DEFAULT_CAL_DIR = ROOT / "data" / "experiments" / "tdc_code_density_cal_20260525"
DEFAULT_LUT_A = DEFAULT_CAL_DIR / "tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv"
DEFAULT_LUT_B = DEFAULT_CAL_DIR / "tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_pair_dynamics_lut_reanalysis_20260525"


WINDOW_FIELDS = [
    "run",
    "source",
    "source_format",
    "window_index",
    "packet_start",
    "packet_end",
    "packets",
    "lut_a",
    "lut_b",
    "clock_period_ps",
    "bins",
    "phase_pearson_r",
    "bin_pearson_r",
    "diff_mean_ps",
    "diff_std_ps",
    "diff_mean_delta_from_first_ps",
    "diff_mean_delta_from_run_mean_ps",
    "run_diff_mean_ps_slope_per_window",
    "lag_min",
    "lag_max",
    "lag0_phase_pearson_r",
    "best_lag_packets",
    "best_lag_phase_pearson_r",
    "best_lag_abs_phase_pearson_r",
    "strong_lock_window",
    "source_file",
]

SUMMARY_FIELDS = [
    "run",
    "windows",
    "packets",
    "phase_r_mean",
    "phase_r_max_abs",
    "best_lag_abs_r_max",
    "best_lag_at_window",
    "best_lag_packets",
    "diff_std_ps_mean",
    "diff_mean_ps_span",
    "diff_mean_ps_slope_per_window",
    "strong_lock_windows",
    "claim_reading",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_lut(path: Path) -> dict[int, float]:
    return {int(row["bin"]): float(row["phase_center_ps_nominal"]) for row in read_csv_rows(path)}


def mean(values: list[float] | list[int]) -> float:
    return sum(values) / len(values) if values else math.nan


def sample_std(values: list[float] | list[int]) -> float:
    if len(values) < 2:
        return math.nan
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def pearson(x_values: list[float] | list[int], y_values: list[float] | list[int]) -> float:
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


def linear_slope(y_values: list[float]) -> float:
    clean = [(i, y) for i, y in enumerate(y_values) if not math.isnan(y)]
    if len(clean) < 2:
        return math.nan
    xs = [float(i) for i, _ in clean]
    ys = [y for _, y in clean]
    mx = mean(xs)
    my = mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom if denom else math.nan


def signed_phase_diff(a_ps: float, b_ps: float, period_ps: float) -> float:
    half = period_ps / 2.0
    return ((a_ps - b_ps + half) % period_ps) - half


def lagged_correlations(
    phases_a: list[float],
    phases_b: list[float],
    lag_min: int,
    lag_max: int,
) -> dict[str, float | int]:
    best_lag = 0
    best_r = pearson(phases_a, phases_b)
    lag0 = best_r
    for lag in range(lag_min, lag_max + 1):
        if lag == 0:
            r = lag0
        elif lag > 0:
            r = pearson(phases_a[lag:], phases_b[:-lag])
        else:
            r = pearson(phases_a[:lag], phases_b[-lag:])
        if math.isnan(best_r) or (not math.isnan(r) and abs(r) > abs(best_r)):
            best_lag = lag
            best_r = r
    return {
        "lag0_phase_pearson_r": lag0,
        "best_lag_packets": best_lag,
        "best_lag_phase_pearson_r": best_r,
        "best_lag_abs_phase_pearson_r": abs(best_r) if not math.isnan(best_r) else math.nan,
    }


def discover_inputs(input_dir: Path) -> list[Path]:
    csv_inputs = sorted(input_dir.glob("analysis_*/*.tdc_packets.csv"))
    if csv_inputs:
        return csv_inputs
    return sorted(input_dir.glob("*.bin"))


def analyze_run(
    input_path: Path,
    fmt: str,
    window_packets: int,
    lag_min: int,
    lag_max: int,
    bins_arg: int | None,
    clock_period_ps: float,
    max_packets: int | None,
    lut_a: dict[int, float],
    lut_b: dict[int, float],
    lut_a_path: Path,
    lut_b_path: Path,
) -> list[dict[str, Any]]:
    packets, source_format = pair_dyn.read_packets(input_path, fmt, max_packets)
    if not packets:
        return []
    bins = bins_arg or pair_dyn.infer_bin_count(packets, None)
    run = input_path.name.replace(".tdc_packets.csv", "") if input_path.name.endswith(".tdc_packets.csv") else input_path.stem
    bin_a = [packet["bin_a"] for packet in packets]
    bin_b = [packet["bin_b"] for packet in packets]
    phases_a_all = [lut_a.get(v, math.nan) for v in bin_a]
    phases_b_all = [lut_b.get(v, math.nan) for v in bin_b]

    rows: list[dict[str, Any]] = []
    for window_index, start in enumerate(range(0, len(packets), window_packets)):
        end = min(start + window_packets, len(packets))
        if end - start < 2:
            continue
        valid = [
            (a_bin, b_bin, a_ps, b_ps)
            for a_bin, b_bin, a_ps, b_ps in zip(
                bin_a[start:end], bin_b[start:end], phases_a_all[start:end], phases_b_all[start:end]
            )
            if not math.isnan(a_ps) and not math.isnan(b_ps)
        ]
        if len(valid) < 2:
            continue
        win_bin_a = [v[0] for v in valid]
        win_bin_b = [v[1] for v in valid]
        win_a = [v[2] for v in valid]
        win_b = [v[3] for v in valid]
        diff_ps = [signed_phase_diff(a, b, clock_period_ps) for a, b in zip(win_a, win_b)]
        lag = lagged_correlations(win_a, win_b, lag_min, lag_max)
        best_abs = float(lag["best_lag_abs_phase_pearson_r"])
        rows.append(
            {
                "run": run,
                "source": str(input_path),
                "source_format": source_format,
                "window_index": window_index,
                "packet_start": start,
                "packet_end": end - 1,
                "packets": len(valid),
                "lut_a": str(lut_a_path),
                "lut_b": str(lut_b_path),
                "clock_period_ps": clock_period_ps,
                "bins": bins,
                "phase_pearson_r": pearson(win_a, win_b),
                "bin_pearson_r": pearson(win_bin_a, win_bin_b),
                "diff_mean_ps": mean(diff_ps),
                "diff_std_ps": sample_std(diff_ps),
                "diff_mean_delta_from_first_ps": math.nan,
                "diff_mean_delta_from_run_mean_ps": math.nan,
                "run_diff_mean_ps_slope_per_window": math.nan,
                "lag_min": lag_min,
                "lag_max": lag_max,
                **lag,
                "strong_lock_window": int(best_abs >= 0.5),
                "source_file": str(input_path),
            }
        )

    diff_means = [float(row["diff_mean_ps"]) for row in rows]
    first = diff_means[0] if diff_means else math.nan
    run_mean = statistics.fmean(diff_means) if diff_means else math.nan
    slope = linear_slope(diff_means)
    for row in rows:
        value = float(row["diff_mean_ps"])
        row["diff_mean_delta_from_first_ps"] = value - first
        row["diff_mean_delta_from_run_mean_ps"] = value - run_mean
        row["run_diff_mean_ps_slope_per_window"] = slope
    return rows


def summarize_by_run(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_run: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_run.setdefault(str(row["run"]), []).append(row)
    summary: list[dict[str, Any]] = []
    for run, run_rows in sorted(by_run.items()):
        phase_rs = [float(row["phase_pearson_r"]) for row in run_rows]
        best_lag_abs = [float(row["best_lag_abs_phase_pearson_r"]) for row in run_rows]
        best_index = max(range(len(run_rows)), key=lambda i: best_lag_abs[i])
        diff_stds = [float(row["diff_std_ps"]) for row in run_rows]
        diff_means = [float(row["diff_mean_ps"]) for row in run_rows]
        strong = sum(int(row["strong_lock_window"]) for row in run_rows)
        summary.append(
            {
                "run": run,
                "windows": len(run_rows),
                "packets": sum(int(row["packets"]) for row in run_rows),
                "phase_r_mean": statistics.fmean(phase_rs),
                "phase_r_max_abs": max(abs(v) for v in phase_rs),
                "best_lag_abs_r_max": max(best_lag_abs),
                "best_lag_at_window": run_rows[best_index]["window_index"],
                "best_lag_packets": run_rows[best_index]["best_lag_packets"],
                "diff_std_ps_mean": statistics.fmean(diff_stds),
                "diff_mean_ps_span": max(diff_means) - min(diff_means) if diff_means else math.nan,
                "diff_mean_ps_slope_per_window": float(run_rows[0]["run_diff_mean_ps_slope_per_window"]),
                "strong_lock_windows": strong,
                "claim_reading": (
                    "strong-lock candidate after fixed-LUT reanalysis"
                    if strong
                    else "no strong pair locking detected after fixed-LUT reanalysis"
                ),
            }
        )
    return summary


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
            writer.writerow({key: fmt(row.get(key, "")) for key in fieldnames})


def write_markdown(path: Path, summary: list[dict[str, Any]], lut_a: Path, lut_b: Path) -> None:
    max_lag = max((float(row["best_lag_abs_r_max"]) for row in summary), default=math.nan)
    strong = sum(int(row["strong_lock_windows"]) for row in summary)
    lines = [
        "# Fixed-LUT TDC Pair Dynamics Reanalysis 20260525",
        "",
        "## Calibration LUTs",
        "",
        f"- lane A LUT: `{lut_a}`",
        f"- lane B LUT: `{lut_b}`",
        "",
        "## Run Summary",
        "",
        "| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | strong lock windows |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["run"]),
                    str(row["windows"]),
                    str(row["packets"]),
                    fmt(row["phase_r_mean"]),
                    fmt(row["best_lag_abs_r_max"]),
                    fmt(row["diff_std_ps_mean"]),
                    fmt(row["diff_mean_ps_span"]),
                    str(row["strong_lock_windows"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Maximum fixed-LUT small-lag `|r|`: `{fmt(max_lag)}`.",
            f"- Strong-lock windows at threshold `|r| >= 0.5`: `{strong}`.",
            "- This is a calibration sensitivity check. It uses one external LUT pair for all pair-specific captures, so the absolute ps spread is more comparable than per-run self-calibration, but it is still not a full per-run metrology calibration.",
            "- If the strong-lock count remains zero, the pair-specific TDC evidence continues to support the negative-control claim against simple pairwise RO hard locking.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--input", type=Path, action="append", default=None)
    parser.add_argument("--format", choices=["auto", "csv", "raw"], default="auto")
    parser.add_argument("--window-packets", type=int, default=16384)
    parser.add_argument("--lag-min", type=int, default=-8)
    parser.add_argument("--lag-max", type=int, default=8)
    parser.add_argument("--bins", type=int, default=65)
    parser.add_argument("--clock-period-ps", type=float, default=5000.0)
    parser.add_argument("--max-packets", type=int, default=None)
    parser.add_argument("--lut-a", type=Path, default=DEFAULT_LUT_A)
    parser.add_argument("--lut-b", type=Path, default=DEFAULT_LUT_B)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    if args.window_packets < 2:
        raise SystemExit("--window-packets must be at least 2")
    if args.lag_min > args.lag_max:
        raise SystemExit("--lag-min must be <= --lag-max")

    lut_a = load_lut(args.lut_a)
    lut_b = load_lut(args.lut_b)
    inputs = args.input or discover_inputs(args.input_dir)
    if not inputs:
        raise SystemExit(f"No TDC pair inputs found under {args.input_dir}")

    rows: list[dict[str, Any]] = []
    for input_path in inputs:
        rows.extend(
            analyze_run(
                input_path,
                args.format,
                args.window_packets,
                args.lag_min,
                args.lag_max,
                args.bins,
                args.clock_period_ps,
                args.max_packets,
                lut_a,
                lut_b,
                args.lut_a,
                args.lut_b,
            )
        )
    if not rows:
        raise SystemExit("No window rows produced")

    summary = summarize_by_run(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "tdc_pair_dynamics_lut_reanalysis_20260525.windows.csv", rows, WINDOW_FIELDS)
    write_csv(args.out_dir / "tdc_pair_dynamics_lut_reanalysis_20260525.summary.csv", summary, SUMMARY_FIELDS)
    write_markdown(args.out_dir / "tdc_pair_dynamics_lut_reanalysis_20260525.md", summary, args.lut_a, args.lut_b)
    print(f"Wrote {args.out_dir}")
    print(f"runs={len(summary)}, windows={len(rows)}, strong_lock_windows={sum(int(row['strong_lock_window']) for row in rows)}")


if __name__ == "__main__":
    main()
