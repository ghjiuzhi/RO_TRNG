#!/usr/bin/env python3
"""Windowed dynamics analysis for captured TDC pair runs.

Offline-only: this script reads existing packet CSV files or raw UART binary
dumps. It does not access hardware, Vivado, COM, JTAG, or hw_server.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "tdc_pairs"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_pair_dynamics"
DEFAULT_CSV = DEFAULT_OUT_DIR / "tdc_pair_dynamics_20260514.csv"
DEFAULT_MD = DEFAULT_OUT_DIR / "tdc_pair_dynamics_20260514.md"
DEFAULT_DOC = ROOT / "doc" / "tdc_pair_dynamics_interpretation_20260514.md"

PACKET_FIELDS = ["seq", "coarse_lsb", "bin_a", "bin_b", "flags"]
RESULT_FIELDS = [
    "run",
    "source",
    "source_format",
    "window_index",
    "packet_start",
    "packet_end",
    "packets",
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


def decode_packets(data: bytes, max_packets: int | None = None) -> list[dict[str, int]]:
    packets: list[dict[str, int]] = []
    i = 0
    while i + 8 <= len(data):
        if data[i] != 0xA5:
            i += 1
            continue
        frame = data[i : i + 8]
        packets.append(
            {
                "seq": frame[1] | (frame[2] << 8),
                "coarse_lsb": frame[3] | (frame[4] << 8),
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
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            packets.append({field: int(row[field]) for field in PACKET_FIELDS})
            if max_packets is not None and len(packets) >= max_packets:
                break
    return packets


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_packets(path: Path, fmt: str, max_packets: int | None) -> tuple[list[dict[str, int]], str]:
    if fmt == "csv" or (fmt == "auto" and path.suffix.lower() == ".csv"):
        return read_packet_csv(path, max_packets), "csv"
    return decode_packets(path.read_bytes(), max_packets), "raw"


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


def infer_bin_count(packets: list[dict[str, int]], requested: int | None) -> int:
    if requested:
        return requested
    max_code = max((max(packet["bin_a"], packet["bin_b"]) for packet in packets), default=0)
    bins = 1
    while bins <= max_code:
        bins <<= 1
    return max(2, bins)


def read_metrics_metadata(input_path: Path) -> tuple[int | None, float | None]:
    metrics_path: Path | None = None
    if input_path.suffix.lower() == ".csv" and input_path.name.endswith(".tdc_packets.csv"):
        metrics_path = input_path.with_name(input_path.name.replace(".tdc_packets.csv", ".tdc_metrics.csv"))
    elif input_path.suffix.lower() == ".bin":
        analysis_dir = input_path.parent / f"analysis_{input_path.stem}"
        candidate = analysis_dir / f"{input_path.stem}.tdc_metrics.csv"
        if candidate.exists():
            metrics_path = candidate
    if not metrics_path or not metrics_path.exists():
        return None, None
    rows = read_csv(metrics_path)
    if not rows:
        return None, None
    row = rows[0]
    bins = int(float(row["bins"])) if row.get("bins") else None
    clock = float(row["clock_period_ps"]) if row.get("clock_period_ps") else None
    return bins, clock


def code_density_phase_lookup(values: list[int], bins: int, clock_period_ps: float) -> dict[int, float]:
    counts = Counter(v for v in values if 0 <= v < bins)
    total = sum(counts.values())
    cumulative_width_ps = 0.0
    lookup: dict[int, float] = {}
    for code in range(bins):
        width_ps = (counts.get(code, 0) / total * clock_period_ps) if total else 0.0
        lookup[code] = cumulative_width_ps + 0.5 * width_ps
        cumulative_width_ps += width_ps
    return lookup


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


def analyze_run(
    input_path: Path,
    fmt: str,
    window_packets: int,
    lag_min: int,
    lag_max: int,
    bins_arg: int | None,
    clock_period_ps_arg: float | None,
    max_packets: int | None,
) -> list[dict[str, Any]]:
    packets, source_format = read_packets(input_path, fmt, max_packets)
    if not packets:
        return []
    meta_bins, meta_clock = read_metrics_metadata(input_path)
    bins = bins_arg or meta_bins or infer_bin_count(packets, None)
    clock_period_ps = clock_period_ps_arg or meta_clock or 5000.0

    run = input_path.name.replace(".tdc_packets.csv", "") if input_path.name.endswith(".tdc_packets.csv") else input_path.stem
    bin_a = [packet["bin_a"] for packet in packets]
    bin_b = [packet["bin_b"] for packet in packets]
    phase_a_lookup = code_density_phase_lookup(bin_a, bins, clock_period_ps)
    phase_b_lookup = code_density_phase_lookup(bin_b, bins, clock_period_ps)
    phases_a_all = [phase_a_lookup.get(v, 0.0) for v in bin_a]
    phases_b_all = [phase_b_lookup.get(v, 0.0) for v in bin_b]

    rows: list[dict[str, Any]] = []
    for window_index, start in enumerate(range(0, len(packets), window_packets)):
        end = min(start + window_packets, len(packets))
        if end - start < 2:
            continue
        win_a = phases_a_all[start:end]
        win_b = phases_b_all[start:end]
        diff_ps = [a - b for a, b in zip(win_a, win_b)]
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
                "packets": end - start,
                "clock_period_ps": clock_period_ps,
                "bins": bins,
                "phase_pearson_r": pearson(win_a, win_b),
                "bin_pearson_r": pearson(bin_a[start:end], bin_b[start:end]),
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


def discover_inputs(input_dir: Path) -> list[Path]:
    csv_inputs = sorted(input_dir.glob("analysis_*/*.tdc_packets.csv"))
    if csv_inputs:
        return csv_inputs
    return sorted(input_dir.glob("*.bin"))


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


def summarize_by_run(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_run: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_run.setdefault(str(row["run"]), []).append(row)
    summary: list[dict[str, Any]] = []
    for run, run_rows in sorted(by_run.items()):
        phase_rs = [float(row["phase_pearson_r"]) for row in run_rows]
        best_lag_abs = [float(row["best_lag_abs_phase_pearson_r"]) for row in run_rows]
        diff_stds = [float(row["diff_std_ps"]) for row in run_rows]
        diff_means = [float(row["diff_mean_ps"]) for row in run_rows]
        drift_span = max(diff_means) - min(diff_means) if diff_means else math.nan
        summary.append(
            {
                "run": run,
                "windows": len(run_rows),
                "packets": sum(int(row["packets"]) for row in run_rows),
                "phase_r_mean": statistics.fmean(phase_rs),
                "phase_r_max_abs": max(abs(v) for v in phase_rs),
                "best_lag_abs_r_max": max(best_lag_abs),
                "diff_std_ps_mean": statistics.fmean(diff_stds),
                "diff_mean_ps_span": drift_span,
                "diff_mean_ps_slope_per_window": float(run_rows[0]["run_diff_mean_ps_slope_per_window"]),
                "strong_lock_windows": sum(int(row["strong_lock_window"]) for row in run_rows),
            }
        )
    return summary


def write_markdown(path: Path, rows: list[dict[str, Any]], summary: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# TDC Pair Dynamics 20260514\n\n")
        f.write("Offline post-analysis of completed TDC pair captures. No hardware, Vivado, COM, JTAG, or hw_server access was used.\n\n")
        f.write("## Method\n\n")
        f.write("- Prefer existing `.tdc_packets.csv`; fall back to raw `.bin` only when packet CSVs are absent.\n")
        f.write("- Build one code-density phase lookup per lane from the full run, then compute windowed dynamics with the same phase scale.\n")
        f.write("- `strong_lock_window` is a conservative flag: max absolute lagged phase correlation >= 0.5 within the requested lag range.\n\n")
        f.write("## Run Summary\n\n")
        f.write("| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | slope ps/window | strong lock windows |\n")
        f.write("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for row in summary:
            f.write(
                f"| {row['run']} | {row['windows']} | {row['packets']} | {float(row['phase_r_mean']):.6g} | "
                f"{float(row['best_lag_abs_r_max']):.6g} | {float(row['diff_std_ps_mean']):.6g} | "
                f"{float(row['diff_mean_ps_span']):.6g} | {float(row['diff_mean_ps_slope_per_window']):.6g} | "
                f"{row['strong_lock_windows']} |\n"
            )
        f.write("\n## Interpretation\n\n")
        if any(int(row["strong_lock_windows"]) for row in summary):
            f.write("At least one window crosses the conservative lag-correlation screen. Treat it as a candidate that needs repeated-run confirmation before claiming locking.\n")
        else:
            f.write("No window crosses the conservative lag-correlation screen. The current data should be described as showing no strong pair locking under this measurement condition.\n")
        f.write("\n## Output\n\n")
        f.write("- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`\n")
        f.write("- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`\n")


def write_interpretation_doc(path: Path, summary: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    max_lag = max((float(row["best_lag_abs_r_max"]) for row in summary), default=math.nan)
    max_phase = max((float(row["phase_r_max_abs"]) for row in summary), default=math.nan)
    strong_windows = sum(int(row["strong_lock_windows"]) for row in summary)
    with path.open("w", encoding="utf-8") as f:
        f.write("# TDC Pair Dynamics Interpretation 20260514\n\n")
        f.write("This note is based only on completed offline TDC pair data in `data/hardware/20260511_fpga1_board1/tdc_pairs/analysis_*`.\n\n")
        f.write("## Key Result\n\n")
        f.write(f"- Maximum absolute zero-lag window phase correlation: `{max_phase:.6g}`.\n")
        f.write(f"- Maximum absolute small-lag window phase correlation: `{max_lag:.6g}`.\n")
        f.write(f"- Conservative strong-lock windows (`|r| >= 0.5` after small-lag scan): `{strong_windows}`.\n\n")
        f.write("The present captures do not support a strong locking claim. "
                "The paper should state that the selected RO pairs were monitored with TDC phase readout, "
                "but the observed windowed phase correlations remained near zero and the differential phase spread stayed "
                "consistent with weakly coupled or effectively independent sampling under this setup.\n\n")
        f.write("## Suggested Paper Wording\n\n")
        f.write("> We did not observe evidence of strong phase locking in the tested TDC pair captures. "
                "Across fixed-size time windows, zero-lag and small-lag phase correlations stayed low, while the "
                "differential phase standard deviation remained on the order expected for two broadly distributed phase samples. "
                "Therefore, these data are treated as a negative or null observation for strong synchronization, not as proof "
                "that coupling cannot occur under other placements, supply conditions, or longer observation windows.\n\n")
        f.write("## Reporting Guidance\n\n")
        f.write("- Use this as mechanism-validation evidence, not as a positive locking result.\n")
        f.write("- Report window size, lag search range, and the fact that full-run code-density calibration was reused for all windows.\n")
        f.write("- Avoid phrases such as `locked`, `synchronized`, or `entrained` unless repeated captures show sustained high correlation and reduced differential phase variance.\n")
        f.write("- A defensible claim is: `No strong TDC-level pair locking was detected in the tested 2 MiB captures.`\n\n")
        f.write("## Source Tables\n\n")
        f.write("- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`\n")
        f.write("- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--input", type=Path, action="append", default=None, help="Specific packet CSV or raw bin. May be repeated.")
    parser.add_argument("--format", choices=["auto", "csv", "raw"], default="auto")
    parser.add_argument("--window-packets", type=int, default=16384)
    parser.add_argument("--lag-min", type=int, default=-8)
    parser.add_argument("--lag-max", type=int, default=8)
    parser.add_argument("--bins", type=int, default=None)
    parser.add_argument("--clock-period-ps", type=float, default=None)
    parser.add_argument("--max-packets", type=int, default=None)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    args = parser.parse_args()

    if args.window_packets < 2:
        raise SystemExit("--window-packets must be at least 2")
    if args.lag_min > args.lag_max:
        raise SystemExit("--lag-min must be <= --lag-max")

    inputs = args.input or discover_inputs(args.input_dir)
    if not inputs:
        raise SystemExit(f"No TDC pair packet CSV or raw bin inputs found under {args.input_dir}")

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
            )
        )
    if not rows:
        raise SystemExit("No window rows produced.")

    summary = summarize_by_run(rows)
    write_csv(args.csv, rows, RESULT_FIELDS)
    write_markdown(args.md, rows, summary)
    write_interpretation_doc(args.doc, summary)

    print(f"Wrote {args.csv}")
    print(f"Wrote {args.md}")
    print(f"Wrote {args.doc}")
    print(f"runs={len(summary)}, windows={len(rows)}, strong_lock_windows={sum(int(row['strong_lock_window']) for row in rows)}")


if __name__ == "__main__":
    main()
