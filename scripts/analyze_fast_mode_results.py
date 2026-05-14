#!/usr/bin/env python3
"""Aggregate fast-mode post-capture analysis into one reproducible report.

Offline-only: this script reads existing analysis CSV files and never touches
hardware, Vivado, COM, JTAG, or hw_server.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "data" / "experiments" / "fast_mode" / "hardware_queue_20260513.csv"
DEFAULT_HARDWARE = ROOT / "data" / "hardware" / "20260511_fpga1_board1"
DEFAULT_RO_ANALYSIS = ROOT / "data" / "experiments" / "ro_freq_analysis"
DEFAULT_CSV = ROOT / "data" / "experiments" / "fast_mode" / "fast_mode_results_20260514.csv"
DEFAULT_MD = ROOT / "data" / "experiments" / "fast_mode" / "fast_mode_results_20260514.md"
DEFAULT_DOC = ROOT / "doc" / "fast_mode_results_summary_20260514.md"

RESULT_FIELDS = [
    "section",
    "evidence_class",
    "comparison_scope",
    "item",
    "run",
    "metric",
    "value",
    "unit",
    "n",
    "baseline",
    "delta",
    "interpretation",
    "source_file",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], key: str, default: float = math.nan) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return default
    try:
        return float(value)
    except ValueError:
        return default


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def mean_std(values: list[float]) -> tuple[float, float]:
    clean = [value for value in values if not math.isnan(value)]
    if not clean:
        return math.nan, math.nan
    if len(clean) == 1:
        return clean[0], math.nan
    return statistics.fmean(clean), statistics.stdev(clean)


def add_result(
    rows: list[dict[str, Any]],
    section: str,
    evidence_class: str,
    comparison_scope: str,
    item: str,
    run: str,
    metric: str,
    value: Any,
    unit: str = "",
    n: Any = "",
    baseline: Any = "",
    delta: Any = "",
    interpretation: str = "",
    source_file: Path | str = "",
) -> None:
    rows.append(
        {
            "section": section,
            "evidence_class": evidence_class,
            "comparison_scope": comparison_scope,
            "item": item,
            "run": run,
            "metric": metric,
            "value": value,
            "unit": unit,
            "n": n,
            "baseline": baseline,
            "delta": delta,
            "interpretation": interpretation,
            "source_file": str(source_file),
        }
    )


def load_queue_runs(queue_path: Path) -> set[str]:
    return {row["run"] for row in read_csv(queue_path) if row.get("enabled") == "1"}


def placement_family(run: str) -> str:
    for suffix in ("_run01_10mib", "_repeat02_5mib", "_run01", "_run02", "_run03"):
        if run.endswith(suffix):
            return run[: -len(suffix)]
    return run


def aggregate_trng(rows: list[dict[str, Any]], hardware_dir: Path, queue_runs: set[str]) -> None:
    path = hardware_dir / "trng" / "trng_repeats_by_run.csv"
    run_rows = read_csv(path)
    if not run_rows:
        add_result(rows, "TRNG", "case_comparison", "missing_input", "trng_repeats_by_run", "", "status", "missing", source_file=path)
        return

    formal = [row for row in run_rows if row.get("sample_role") == "formal" and row.get("placement") != "original_fpga1"]
    by_metric = {
        "bit_min_entropy": "higher is better",
        "abs_bias": "lower is better",
        "runs_p": "larger p-value is less suspicious",
        "byte_min_entropy": "higher is better",
    }
    for metric, note in by_metric.items():
        values = [f(row, metric) for row in formal]
        mean, std = mean_std(values)
        if math.isnan(mean):
            continue
        sorted_rows = sorted(formal, key=lambda row: f(row, metric))
        low = sorted_rows[0]
        high = sorted_rows[-1]
        add_result(
            rows,
            "TRNG",
            "statistical_comparison",
            "placement_matrix_formal_10mib",
            "all_non_original_placements",
            "",
            f"{metric}_mean",
            mean,
            n=len(values),
            delta=f"std={fmt(std)}; min={low['placement']}:{fmt(f(low, metric))}; max={high['placement']}:{fmt(f(high, metric))}",
            interpretation=note,
            source_file=path,
        )

    for row in run_rows:
        run = row.get("run", "")
        is_fast_original = run in queue_runs or row.get("placement") == "original_fpga1"
        if not is_fast_original:
            continue
        evidence = "case_comparison" if row.get("placement") == "original_fpga1" else "statistical_comparison"
        scope = "original_fpga1_baseline" if row.get("placement") == "original_fpga1" else "fast_queue_trng_repeat"
        for metric in ("bytes", "p1", "abs_bias", "bit_min_entropy", "monobit_p", "runs_p", "adjacent_equal_ratio", "byte_min_entropy"):
            add_result(
                rows,
                "TRNG",
                evidence,
                scope,
                row.get("placement", placement_family(run)),
                run,
                metric,
                row.get(metric, ""),
                n=1,
                interpretation="single captured run; do not treat as placement-wide statistics" if evidence == "case_comparison" else "",
                source_file=path,
            )

    included_runs = {row.get("run", "") for row in run_rows}
    for run in sorted(queue_runs):
        if not run.startswith("original_fpga1_") or run in included_runs:
            continue
        summary_path = hardware_dir / "trng" / f"analysis_{run}" / "trng_summary.csv"
        summary_rows = read_csv(summary_path)
        if not summary_rows:
            add_result(
                rows,
                "TRNG",
                "case_comparison",
                "original_fpga1_baseline",
                "original_fpga1",
                run,
                "status",
                "missing_summary",
                n=0,
                interpretation="single baseline case could not be summarized because its trng_summary.csv was not found",
                source_file=summary_path,
            )
            continue
        summary = summary_rows[0]
        for metric, source_key in (
            ("bytes", "bytes"),
            ("p1", "p1"),
            ("abs_bias", "p1"),
            ("bit_min_entropy", "bit_min_entropy"),
            ("monobit_p", "monobit_p"),
            ("runs_p", "runs_p"),
            ("adjacent_equal_ratio", "adjacent_equal_ratio"),
            ("byte_min_entropy", "min_entropy_byte"),
        ):
            value: Any = summary.get(source_key, "")
            if metric == "abs_bias":
                value = abs(f(summary, "p1") - 0.5)
            add_result(
                rows,
                "TRNG",
                "case_comparison",
                "original_fpga1_baseline",
                "original_fpga1",
                run,
                metric,
                value,
                n=1,
                interpretation="single captured baseline run; do not treat as placement-wide statistics",
                source_file=summary_path,
            )


def ro_input_dirs(ro_root: Path) -> list[tuple[Path, str, str]]:
    """Return selected RO_FREQ analyses as (directory, prefix, run_label)."""
    selected: list[tuple[Path, str, str]] = []
    specs = [
        ("20260513_random1_random3_fixed_run01_2mib", "random1_random3_fixed_run01_2mib", "run01"),
        ("20260513_ro_freq_run02", "ro_freq_run02", "run02"),
        ("20260513_ro_freq_run03", "ro_freq_run03", "run03"),
        ("20260513_random1_fixed_partial5mib", "random1_ro_freq_fixed_run01_partial5mib", "run01_5mib"),
        ("20260513_ro_freq_run01_5mib", "ro_freq_run01_5mib", "run01_5mib"),
    ]
    for dirname, prefix, label in specs:
        ro_dir = ro_root / dirname
        if (ro_dir / f"{prefix}_pairwise_all_on.csv").exists():
            selected.append((ro_dir, prefix, label))
    return selected


def aggregate_ro_freq(rows: list[dict[str, Any]], ro_root: Path) -> None:
    run_dirs = ro_input_dirs(ro_root)
    if not run_dirs:
        add_result(rows, "RO_FREQ", "case_comparison", "missing_input", "ro_freq_analysis", "", "status", "missing", source_file=ro_root)
        return

    closest_by_family: dict[str, list[float]] = defaultdict(list)
    sample_pull_by_family: dict[str, list[float]] = defaultdict(list)
    run_labels_by_family: dict[str, list[str]] = defaultdict(list)
    pull_labels_by_family: dict[str, list[str]] = defaultdict(list)

    for ro_dir, prefix, label in run_dirs:
        pair_path = ro_dir / f"{prefix}_pairwise_all_on.csv"
        pull_path = ro_dir / f"{prefix}_pulling.csv"
        pair_rows = [row for row in read_csv(pair_path) if row.get("mode") == "all_on" and row.get("relation") == "data_data"]
        pull_rows = read_csv(pull_path)
        for family in sorted({row.get("family", "") for row in pair_rows if row.get("family")}):
            family_pairs = sorted([row for row in pair_rows if row.get("family") == family], key=lambda row: f(row, "abs_delta_f_mhz"))
            if not family_pairs:
                continue
            best = family_pairs[0]
            value = f(best, "abs_delta_f_mhz")
            closest_by_family[family].append(value)
            run_labels_by_family[family].append(label)
            evidence = "statistical_comparison" if label in {"run01", "run02", "run03"} else "case_comparison"
            add_result(
                rows,
                "RO_FREQ",
                evidence,
                "closest_all_on_data_data_beat",
                family,
                label,
                "closest_abs_delta_f_mhz",
                value,
                "MHz",
                n=1,
                delta=f"{best.get('a_name')}/{best.get('b_name')}; beat_period_ns={fmt(f(best, 'beat_period_ns'))}",
                interpretation="single 5MiB case" if evidence == "case_comparison" else "per-run observation included in run01/run02/run03 repeat statistics",
                source_file=pair_path,
            )
        for row in pull_rows:
            if row.get("target_name") != "sample":
                continue
            family = row.get("family", "")
            value = f(row, "shift_ppm_vs_single")
            sample_pull_by_family[family].append(value)
            pull_labels_by_family[family].append(label)
            evidence = "statistical_comparison" if label in {"run01", "run02", "run03"} else "case_comparison"
            add_result(
                rows,
                "RO_FREQ",
                evidence,
                "sample_all_on_vs_single_on_pulling",
                family,
                label,
                "sample_shift_ppm_vs_single",
                value,
                "ppm",
                n=1,
                interpretation="single 5MiB case" if evidence == "case_comparison" else "per-run observation included in run01/run02/run03 repeat statistics",
                source_file=pull_path,
            )

    for family, values in sorted(closest_by_family.items()):
        statistical_values = [
            value
            for value, label in zip(values, run_labels_by_family[family])
            if label in {"run01", "run02", "run03"}
        ]
        if statistical_values:
            mean, std = mean_std(statistical_values)
            add_result(
                rows,
                "RO_FREQ",
                "statistical_comparison",
                "run01_run02_run03_repeat",
                family,
                "run01/run02/run03",
                "closest_abs_delta_f_mhz_mean",
                mean,
                "MHz",
                n=len(statistical_values),
                delta=f"std={fmt(std)}",
                interpretation="repeat statistic across the three 2MiB RO_FREQ runs",
                source_file=ro_root,
            )
    for family, values in sorted(sample_pull_by_family.items()):
        labels = pull_labels_by_family.get(family, [])
        statistical_values = [value for value, label in zip(values, labels) if label in {"run01", "run02", "run03"}]
        if statistical_values:
            mean, std = mean_std(statistical_values)
            add_result(
                rows,
                "RO_FREQ",
                "statistical_comparison",
                "run01_run02_run03_repeat",
                family,
                "run01/run02/run03",
                "sample_shift_ppm_vs_single_mean",
                mean,
                "ppm",
                n=len(statistical_values),
                delta=f"std={fmt(std)}",
                interpretation="repeat statistic across the three 2MiB RO_FREQ runs",
                source_file=ro_root,
            )


def aggregate_tdc(rows: list[dict[str, Any]], hardware_dir: Path) -> None:
    tdc_dir = hardware_dir / "tdc"
    metric_rows: list[dict[str, str]] = []
    for path in sorted(tdc_dir.glob("analysis_tdc_*/*.tdc_metrics.csv")):
        for row in read_csv(path):
            row["_source_file"] = str(path)
            metric_rows.append(row)
    if not metric_rows:
        add_result(rows, "TDC", "case_comparison", "missing_input", "tdc_metrics", "", "status", "missing", source_file=tdc_dir)
        return

    for row in metric_rows:
        run = row.get("run", "")
        if not re.match(r"^tdc_(near|far)_run\d+", run):
            continue
        side = "near" if "_near_" in run else "far"
        for metric, unit in (("packets", ""), ("seq_gaps", ""), ("diff_std_ps", "ps"), ("phase_pearson_r", ""), ("lane_a_used_bins", ""), ("lane_b_used_bins", "")):
            add_result(
                rows,
                "TDC",
                "statistical_comparison",
                "near_far_repeat_runs",
                side,
                run,
                metric,
                row.get(metric, ""),
                unit,
                n=1,
                interpretation="per-run TDC repeat metric",
                source_file=row.get("_source_file", ""),
            )

    for side in ("near", "far"):
        side_rows = [row for row in metric_rows if f"tdc_{side}_run" in row.get("run", "")]
        for metric, unit in (("diff_std_ps", "ps"), ("phase_pearson_r", ""), ("seq_gaps", "")):
            values = [f(row, metric) for row in side_rows]
            if not values:
                continue
            mean, std = mean_std(values)
            add_result(
                rows,
                "TDC",
                "statistical_comparison",
                "near_far_repeat_runs",
                side,
                "all_repeats",
                f"{metric}_mean",
                mean,
                unit,
                n=len(values),
                delta=f"std={fmt(std)}",
                interpretation=f"{side} TDC repeat statistic",
                source_file=tdc_dir,
            )


def write_results_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field, "")) for field in RESULT_FIELDS})


def write_table(path: Path, rows: list[dict[str, Any]], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("Offline aggregate generated from existing analysis CSVs only. No hardware/Vivado/COM/JTAG/hw_server access is used.\n\n")
        f.write("| " + " | ".join(RESULT_FIELDS) + " |\n")
        f.write("| " + " | ".join(["---"] * len(RESULT_FIELDS)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(fmt(row.get(field, "")) for field in RESULT_FIELDS) + " |\n")


def select_metric(rows: list[dict[str, Any]], section: str, metric: str, item: str = "") -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row.get("section") == section
        and row.get("metric") == metric
        and (not item or row.get("item") == item)
    ]


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    statistical = [row for row in rows if row.get("evidence_class") == "statistical_comparison"]
    cases = [row for row in rows if row.get("evidence_class") == "case_comparison"]

    lines = [
        "# Fast Mode Results Summary 20260514",
        "",
        "This is an offline post-analysis summary. It reads existing CSV/bin-derived analysis outputs only; it does not access hardware, Vivado, COM, JTAG, or hw_server.",
        "",
        "## Evidence labels",
        "",
        "- `statistical_comparison`: repeated-run or placement-matrix aggregates where the table reports mean/std or a repeated observation set.",
        "- `case_comparison`: single-run baseline/case observations, including the original fpga1 baseline and the RO_FREQ 5MiB case. These should not be written as population statistics.",
        "",
        "## One-command rerun",
        "",
        "```powershell",
        "python scripts\\analyze_fast_mode_results.py",
        "```",
        "",
        "The fast hardware queue also calls this script during post-analysis after its existing RO_FREQ/TRNG refresh steps.",
        "",
        "## Statistical comparisons",
        "",
    ]
    for row in statistical:
        if row.get("metric", "").endswith("_mean"):
            lines.append(
                f"- {row['section']} `{row['comparison_scope']}` `{row['item']}` `{row['metric']}` = {fmt(row['value'])} {row['unit']} (n={row['n']}; {row['delta']})."
            )
    lines.extend(["", "## Case comparisons", ""])
    for row in cases:
        if row.get("metric") in {"bit_min_entropy", "abs_bias", "closest_abs_delta_f_mhz", "sample_shift_ppm_vs_single"}:
            lines.append(
                f"- {row['section']} `{row['comparison_scope']}` `{row['item']}` `{row['run']}` `{row['metric']}` = {fmt(row['value'])} {row['unit']}."
            )

    original_h = select_metric(rows, "TRNG", "bit_min_entropy", "original_fpga1")
    if original_h:
        lines.extend(["", "## Original fpga1 baseline", ""])
        for row in original_h:
            lines.append(f"- `{row['run']}` bit min-entropy = {fmt(row['value'])} (case comparison).")

    lines.extend(
        [
            "",
            "## Output files",
            "",
            "- `data/experiments/fast_mode/fast_mode_results_20260514.csv`",
            "- `data/experiments/fast_mode/fast_mode_results_20260514.md`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-csv", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--hardware-dir", type=Path, default=DEFAULT_HARDWARE)
    parser.add_argument("--ro-analysis-dir", type=Path, default=DEFAULT_RO_ANALYSIS)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--summary-md", type=Path, default=DEFAULT_DOC)
    args = parser.parse_args()

    queue_runs = load_queue_runs(args.queue_csv)
    rows: list[dict[str, Any]] = []
    aggregate_trng(rows, args.hardware_dir, queue_runs)
    aggregate_ro_freq(rows, args.ro_analysis_dir)
    aggregate_tdc(rows, args.hardware_dir)
    rows.sort(key=lambda row: (str(row["section"]), str(row["evidence_class"]), str(row["comparison_scope"]), str(row["item"]), str(row["run"]), str(row["metric"])))

    write_results_csv(args.out_csv, rows)
    write_table(args.out_md, rows, "Fast Mode Results 20260514")
    write_summary(args.summary_md, rows)
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")
    print(f"Wrote {args.summary_md}")
    print(f"Rows: {len(rows)}; statistical={sum(1 for row in rows if row['evidence_class'] == 'statistical_comparison')}; case={sum(1 for row in rows if row['evidence_class'] == 'case_comparison')}")


if __name__ == "__main__":
    main()
