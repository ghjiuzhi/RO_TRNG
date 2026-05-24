#!/usr/bin/env python3
"""Build a placement-level evidence table for mechanism hypotheses.

This is an offline table builder only. It reads existing CSV artifacts and
does not touch hardware, Vivado, JTAG, UART, or capture flows.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from statistics import mean
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_POSITION_STRUCTURE = (
    ROOT / "data/experiments/position_structure_20260523/position_structure_summary.csv"
)
DEFAULT_TRNG_REPEATS = (
    ROOT / "data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.csv"
)
DEFAULT_RESTART = (
    ROOT / "data/experiments/restart_summary_20260515/restart_result_summary_20260522.csv"
)
DEFAULT_RO_CORRELATION = (
    ROOT / "data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv"
)
DEFAULT_TDC = (
    ROOT / "data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.csv"
)
DEFAULT_SAMPLER_ISLAND = (
    ROOT / "data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv"
)
DEFAULT_OUT_DIR = ROOT / "data/experiments/mechanism_hypothesis_20260523"

OUT_CSV_NAME = "mechanism_hypothesis_evidence_by_placement.csv"

BASE_COLUMNS = [
    "placement",
    "failure_mode_guess",
    "evidence_note",
    "continuous_source",
    "continuous_bytes",
    "continuous_p1",
    "continuous_abs_bias",
    "continuous_bit_min_entropy",
    "continuous_adjacent_equal",
    "continuous_lag1_phi",
    "repeat_summary_source",
    "repeat_summary_rows",
    "repeat_best_sample_role",
    "repeat_best_target_bytes",
    "repeat_best_p1_mean",
    "repeat_best_abs_bias_mean",
    "repeat_best_bit_min_entropy_mean",
    "repeat_best_adjacent_equal_ratio_mean",
    "repeat_best_byte_min_entropy_mean",
    "restart_source",
    "restart_rows",
    "restart_pass_count",
    "restart_fail_count",
    "restart_statuses",
    "restart_warmup_bytes_observed",
    "restart_min_passing_warmup_bytes",
    "restart_max_failing_warmup_bytes",
    "restart_warmup_transition",
    "restart_worst_x_max",
    "restart_worst_x_row",
    "restart_worst_warmup_bytes",
    "restart_worst_bit_order",
    "restart_worst_byte_index",
    "restart_worst_bit_index",
    "restart_worst_msb_expanded_column",
    "restart_worst_lsb_expanded_column",
    "restart_worst_p1",
]

RO_FIELDS = [
    "trng_sample_role",
    "trng_target_bytes",
    "trng_p1",
    "trng_abs_bias",
    "trng_bit_min_entropy",
    "trng_monobit_p",
    "trng_runs_p",
    "trng_adjacent_equal_ratio",
    "trng_byte_min_entropy",
    "ro_data_count",
    "ro_data_mean_freq_mhz",
    "ro_data_std_freq_mhz",
    "ro_data_min_freq_mhz",
    "ro_data_max_freq_mhz",
    "ro_data_span_mhz",
    "ro_sample_all_on_freq_mhz",
    "ro_min_data_data_delta_mhz",
    "ro_min_data_data_pair",
    "ro_min_data_data_beat_ns",
    "ro_second_data_data_delta_mhz",
    "ro_second_data_data_pair",
    "ro_close_data_data_pairs_le_1mhz",
    "ro_close_data_data_pairs_le_3mhz",
    "ro_nearest_data_sample_delta_mhz",
    "ro_nearest_data_sample_pair",
    "ro_nearest_data_sample_beat_ns",
    "ro_data_mean_shift_mhz",
    "ro_data_mean_abs_shift_ppm",
    "ro_data_max_abs_shift_ppm",
    "ro_sample_shift_mhz",
    "ro_sample_shift_ppm",
    "ro_sample_abs_shift_ppm",
]

TDC_NUMERIC_FIELDS = [
    "phase_r_mean",
    "phase_r_max_abs",
    "best_lag_abs_r_max",
    "diff_std_ps_mean",
    "diff_mean_ps_span",
    "diff_mean_ps_slope_per_window",
    "strong_lock_windows",
]

TDC_COLUMNS = [
    "tdc_available",
    "tdc_pair_count",
    "tdc_runs",
    *[f"tdc_{field}_avg" for field in TDC_NUMERIC_FIELDS],
    *[f"tdc_{field}_max" for field in TDC_NUMERIC_FIELDS],
    "tdc_claim_readings",
]

SAMPLER_COLUMNS = [
    "sampler_ablation_available",
    "sampler_ablation_rows",
    "sampler_ablation_best_experiment",
    "sampler_ablation_best_bytes",
    "sampler_ablation_best_p1",
    "sampler_ablation_best_abs_bias",
    "sampler_ablation_best_bit_min_entropy",
    "sampler_ablation_best_adjacent_equal",
    "sampler_ablation_best_sample_shift_ppm",
    "sampler_ablation_best_xadc_before_c",
    "sampler_ablation_best_xadc_after_c",
    "sampler_ablation_claim",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fmt(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def group_by_placement(rows: Iterable[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        placement = row.get("placement", "").strip()
        if placement:
            grouped.setdefault(placement, []).append(row)
    return grouped


def best_continuous_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped = group_by_placement(rows)
    out: dict[str, dict[str, str]] = {}
    for placement, placement_rows in grouped.items():
        placement_rows.sort(key=lambda row: to_float(row.get("bytes")) or -1, reverse=True)
        out[placement] = placement_rows[0]
    return out


def best_repeat_rows(rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, int]]:
    grouped = group_by_placement(rows)
    out: dict[str, dict[str, str]] = {}
    counts: dict[str, int] = {}
    for placement, placement_rows in grouped.items():
        counts[placement] = len(placement_rows)
        preferred = [
            row
            for row in placement_rows
            if row.get("sample_role") == "repeat" and row.get("target_bytes") == "20971520"
        ]
        candidates = preferred or placement_rows
        candidates.sort(
            key=lambda row: (
                to_float(row.get("target_bytes")) or -1,
                to_float(row.get("bytes_mean")) or -1,
            ),
            reverse=True,
        )
        out[placement] = candidates[0]
    return out, counts


def summarize_restart(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for placement, placement_rows in group_by_placement(rows).items():
        statuses = [row.get("ea_status", "").strip() for row in placement_rows]
        pass_count = sum(1 for status in statuses if status == "passed")
        fail_count = sum(1 for status in statuses if status == "failed")
        warmups = sorted(
            {
                int(value)
                for value in (row.get("warmup_bytes", "") for row in placement_rows)
                if value.strip().isdigit()
            }
        )
        pass_warmups = [
            int(row["warmup_bytes"])
            for row in placement_rows
            if row.get("ea_status") == "passed" and row.get("warmup_bytes", "").isdigit()
        ]
        fail_warmups = [
            int(row["warmup_bytes"])
            for row in placement_rows
            if row.get("ea_status") == "failed" and row.get("warmup_bytes", "").isdigit()
        ]
        worst_row = max(
            placement_rows,
            key=lambda row: to_float(row.get("worst_x")) or to_float(row.get("x_max")) or -1,
        )
        worst_x = to_float(worst_row.get("worst_x")) or to_float(worst_row.get("x_max"))

        min_pass = min(pass_warmups) if pass_warmups else None
        max_fail = max(fail_warmups) if fail_warmups else None
        if fail_count and pass_count and max_fail is not None and min_pass is not None:
            transition = f"failed <= {max_fail} bytes; passed >= {min_pass} bytes"
        elif fail_count and not pass_count:
            transition = "no passing warmup observed"
        elif pass_count and not fail_count:
            transition = "all observed warmups passed"
        else:
            transition = "no restart status observed"

        out[placement] = {
            "restart_rows": str(len(placement_rows)),
            "restart_pass_count": str(pass_count),
            "restart_fail_count": str(fail_count),
            "restart_statuses": ";".join(sorted({status for status in statuses if status})),
            "restart_warmup_bytes_observed": ";".join(str(value) for value in warmups),
            "restart_min_passing_warmup_bytes": fmt(min_pass),
            "restart_max_failing_warmup_bytes": fmt(max_fail),
            "restart_warmup_transition": transition,
            "restart_worst_x_max": fmt(worst_x),
            "restart_worst_x_row": worst_row.get("worst_x", "") or worst_row.get("x_max", ""),
            "restart_worst_warmup_bytes": worst_row.get("warmup_bytes", ""),
            "restart_worst_bit_order": worst_row.get("bit_order", ""),
            "restart_worst_byte_index": worst_row.get("worst_byte_index", ""),
            "restart_worst_bit_index": worst_row.get("worst_bit_index", ""),
            "restart_worst_msb_expanded_column": worst_row.get("worst_msb_expanded_column", ""),
            "restart_worst_lsb_expanded_column": worst_row.get("worst_lsb_expanded_column", ""),
            "restart_worst_p1": worst_row.get("worst_p1", ""),
        }
    return out


def ro_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["placement"]: row for row in rows if row.get("placement")}


def tdc_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        match = re.search(r"tdc_pair_([^_]+)_", row.get("run", ""))
        if match:
            grouped.setdefault(match.group(1), []).append(row)

    out: dict[str, dict[str, str]] = {}
    for placement, placement_rows in grouped.items():
        summary: dict[str, str] = {
            "tdc_available": "yes",
            "tdc_pair_count": str(len(placement_rows)),
            "tdc_runs": ";".join(row.get("run", "") for row in placement_rows),
            "tdc_claim_readings": ";".join(
                sorted({row.get("claim_reading", "") for row in placement_rows if row.get("claim_reading")})
            ),
        }
        for field in TDC_NUMERIC_FIELDS:
            values = [to_float(row.get(field)) for row in placement_rows]
            values = [value for value in values if value is not None]
            if values:
                summary[f"tdc_{field}_avg"] = fmt(mean(values))
                summary[f"tdc_{field}_max"] = fmt(max(values))
        out[placement] = summary
    return out


def sampler_ablation_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    random1_rows = [
        row
        for row in rows
        if row.get("experiment", "").startswith("random1_")
        and "baseline" not in row.get("experiment", "")
    ]
    if not random1_rows:
        return {}

    def score(row: dict[str, str]) -> tuple[float, float]:
        hmin = to_float(row.get("bit_min_entropy")) or -1.0
        size = to_float(row.get("bytes")) or -1.0
        return hmin, size

    best = max(random1_rows, key=score)
    p1 = to_float(best.get("p1"))
    return {
        "random1": {
            "sampler_ablation_available": "yes",
            "sampler_ablation_rows": str(len(random1_rows)),
            "sampler_ablation_best_experiment": best.get("experiment", ""),
            "sampler_ablation_best_bytes": best.get("bytes", ""),
            "sampler_ablation_best_p1": best.get("p1", ""),
            "sampler_ablation_best_abs_bias": fmt(abs(p1 - 0.5)) if p1 is not None else "",
            "sampler_ablation_best_bit_min_entropy": best.get("bit_min_entropy", ""),
            "sampler_ablation_best_adjacent_equal": best.get("adjacent_equal_ratio", ""),
            "sampler_ablation_best_sample_shift_ppm": best.get("sample_shift_ppm_vs_single", ""),
            "sampler_ablation_best_xadc_before_c": best.get("xadc_before_c", ""),
            "sampler_ablation_best_xadc_after_c": best.get("xadc_after_c", ""),
            "sampler_ablation_claim": "fixed data-RO placement; sampler-side relocation improves random1 output",
        }
    }


def guess_failure_mode(row: dict[str, str]) -> tuple[str, str]:
    p1 = to_float(row.get("continuous_p1"))
    bit_h = to_float(row.get("continuous_bit_min_entropy"))
    lag1 = abs(to_float(row.get("continuous_lag1_phi")) or 0.0)
    fail_count = int(row.get("restart_fail_count") or 0)
    pass_count = int(row.get("restart_pass_count") or 0)
    has_restart = bool(row.get("restart_rows"))
    has_continuous = bool(row.get("continuous_source"))
    has_repeat = bool(row.get("repeat_summary_source"))
    has_ro = row.get("rofreq_available") == "yes"
    has_tdc = row.get("tdc_available") == "yes"

    continuous_bias = False
    if p1 is not None and abs(p1 - 0.5) >= 0.005:
        continuous_bias = True
    if bit_h is not None and bit_h < 0.99:
        continuous_bias = True

    if continuous_bias:
        return (
            "continuous_bias",
            "Continuous stream already shows material p1/min-entropy deviation.",
        )
    if not has_continuous and has_repeat and not has_restart and not has_ro and not has_tdc:
        return "repeat_summary_only", "Only the repeat summary table contributes evidence for this placement."
    if fail_count and pass_count:
        return (
            "warmup_sensitive_restart_bias",
            "Restart failures and passes both appear; warmup changes the restart outcome.",
        )
    if fail_count:
        note = "Restart sanity failure despite near-balanced continuous stream."
        if lag1 >= 0.001:
            note += " Lag-1 correlation is also elevated."
        return "restart_state_bias", note
    if has_restart and pass_count:
        return "no_restart_failure_observed", "Observed restart rows passed."
    if has_ro or has_tdc:
        return "mechanism_features_only", "RO_FREQ/TDC mechanism fields exist, but restart rows are absent."
    return "continuous_only_no_restart", "Continuous evidence exists, but no restart/RO/TDC rows are available."


def build_rows(
    position_rows: list[dict[str, str]],
    repeat_rows: list[dict[str, str]],
    restart_rows: list[dict[str, str]],
    ro_rows: list[dict[str, str]],
    tdc_rows: list[dict[str, str]],
    sampler_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    continuous = best_continuous_rows(position_rows)
    repeats, repeat_counts = best_repeat_rows(repeat_rows)
    restarts = summarize_restart(restart_rows)
    ro = ro_by_placement(ro_rows)
    tdc = tdc_by_placement(tdc_rows)
    sampler = sampler_ablation_by_placement(sampler_rows)

    placements = sorted(set(continuous) | set(repeats) | set(restarts) | set(ro) | set(tdc) | set(sampler))
    rows: list[dict[str, str]] = []
    for placement in placements:
        row: dict[str, str] = {column: "" for column in BASE_COLUMNS}
        row["placement"] = placement

        cont = continuous.get(placement, {})
        if cont:
            row.update(
                {
                    "continuous_source": "position_structure_summary.csv",
                    "continuous_bytes": cont.get("bytes", ""),
                    "continuous_p1": cont.get("p1", ""),
                    "continuous_abs_bias": cont.get("abs_bias", ""),
                    "continuous_bit_min_entropy": cont.get("bit_min_entropy", ""),
                    "continuous_adjacent_equal": cont.get("adjacent_equal", ""),
                    "continuous_lag1_phi": cont.get("lag1_phi", ""),
                }
            )

        repeat = repeats.get(placement, {})
        if repeat:
            row.update(
                {
                    "repeat_summary_source": "trng_repeats_by_placement.csv",
                    "repeat_summary_rows": str(repeat_counts.get(placement, 0)),
                    "repeat_best_sample_role": repeat.get("sample_role", ""),
                    "repeat_best_target_bytes": repeat.get("target_bytes", ""),
                    "repeat_best_p1_mean": repeat.get("p1_mean", ""),
                    "repeat_best_abs_bias_mean": repeat.get("abs_bias_mean", ""),
                    "repeat_best_bit_min_entropy_mean": repeat.get("bit_min_entropy_mean", ""),
                    "repeat_best_adjacent_equal_ratio_mean": repeat.get("adjacent_equal_ratio_mean", ""),
                    "repeat_best_byte_min_entropy_mean": repeat.get("byte_min_entropy_mean", ""),
                }
            )

        restart = restarts.get(placement, {})
        if restart:
            row["restart_source"] = "restart_result_summary_20260522.csv"
            row.update(restart)

        ro_row = ro.get(placement, {})
        row["rofreq_available"] = "yes" if ro_row else "no"
        for field in RO_FIELDS:
            row[f"rofreq_{field}"] = ro_row.get(field, "")

        tdc_row = tdc.get(placement, {})
        row.update({column: "" for column in TDC_COLUMNS})
        row["tdc_available"] = "yes" if tdc_row else "no"
        row.update(tdc_row)

        sampler_row = sampler.get(placement, {})
        row.update({column: "" for column in SAMPLER_COLUMNS})
        row["sampler_ablation_available"] = "yes" if sampler_row else "no"
        row.update(sampler_row)

        guess, note = guess_failure_mode(row)
        row["failure_mode_guess"] = guess
        row["evidence_note"] = note
        rows.append(row)
    return rows


def write_readme(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["failure_mode_guess"]] = counts.get(row["failure_mode_guess"], 0) + 1

    lines = [
        "# Mechanism Hypothesis Evidence Table",
        "",
        "Offline placement-level evidence chain assembled from existing CSV artifacts.",
        "",
        "## Outputs",
        "",
        f"- `{OUT_CSV_NAME}`: one row per placement with continuous TRNG, restart, RO_FREQ, and TDC evidence where available.",
        "- `README.md`: this summary.",
        "",
        "## Inputs",
        "",
        f"- `{rel(args.position_structure)}`",
        f"- `{rel(args.trng_repeats)}`",
        f"- `{rel(args.restart)}`",
        f"- `{rel(args.ro_correlation)}`",
        f"- `{rel(args.tdc)}`",
        f"- `{rel(args.sampler_island)}`",
        "",
        "## Notes",
        "",
        "- Continuous fields come from `position_structure_summary.csv`: `bit_min_entropy`, `p1`, `adjacent_equal`, and `lag1_phi`.",
        "- Restart fields are placement summaries: fail/pass counts, observed warmups, warmup transition text, and the row with the largest `worst_x`/`x_max`.",
        "- RO_FREQ fields are prefixed with `rofreq_` and are present only for placements covered by the correlation table.",
        "- TDC fields are grouped by parsing `tdc_pair_<placement>_...` from run names.",
        "- Sampler-ablation fields summarize the `random1` sampler-side causal experiment.",
        "- `failure_mode_guess` is a heuristic label for triage, not a statistical proof.",
        "- This script is offline-only and does not start hardware, Vivado, UART, JTAG, or capture jobs.",
        "",
        "## Failure Mode Guess Counts",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--position-structure", type=Path, default=DEFAULT_POSITION_STRUCTURE)
    parser.add_argument("--trng-repeats", type=Path, default=DEFAULT_TRNG_REPEATS)
    parser.add_argument("--restart", type=Path, default=DEFAULT_RESTART)
    parser.add_argument("--ro-correlation", type=Path, default=DEFAULT_RO_CORRELATION)
    parser.add_argument("--tdc", type=Path, default=DEFAULT_TDC)
    parser.add_argument("--sampler-island", type=Path, default=DEFAULT_SAMPLER_ISLAND)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(
        read_csv(args.position_structure),
        read_csv(args.trng_repeats),
        read_csv(args.restart),
        read_csv(args.ro_correlation),
        read_csv(args.tdc),
        read_csv(args.sampler_island),
    )
    columns = [
        *BASE_COLUMNS,
        "rofreq_available",
        *[f"rofreq_{field}" for field in RO_FIELDS],
        *TDC_COLUMNS,
        *SAMPLER_COLUMNS,
    ]
    out_csv = args.out_dir / OUT_CSV_NAME
    out_readme = args.out_dir / "README.md"
    write_csv(out_csv, rows, columns)
    write_readme(out_readme, rows, args)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_readme}")


if __name__ == "__main__":
    main()
