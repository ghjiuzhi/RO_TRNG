#!/usr/bin/env python3
"""Audit and export the offline restart mechanism-correlation tables.

This script reads existing offline artifacts only. It does not touch hardware,
capture flows, Vivado, JTAG, or COM ports.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_EXISTING_LINK = ROOT / "data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.csv"
DEFAULT_RESTART = ROOT / "data/experiments/restart_summary_20260515/restart_result_summary_20260522.csv"
DEFAULT_TRNG = ROOT / "data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.csv"
DEFAULT_RO_CORRELATION = ROOT / "data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv"
DEFAULT_TDC = ROOT / "data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.csv"
DEFAULT_OUT_DIR = ROOT / "data/experiments/mechanism_correlation_20260523"

REQUIRED_EXISTING_GROUPS = {
    "restart worst columns": [
        "restart_worst_byte",
        "restart_worst_bit",
        "restart_worst_x",
        "restart_worst_p1",
        "restart_worst_msb_column",
        "restart_worst_lsb_column",
    ],
    "TRNG entropy": [
        "trng_bit_min_entropy_mean",
        "trng_byte_min_entropy_mean",
        "trng_abs_bias_mean",
    ],
    "RO_FREQ": [
        "rofreq_ro_min_data_data_delta_mhz",
        "rofreq_ro_min_data_data_pair",
        "rofreq_ro_sample_shift_ppm",
    ],
    "TDC": [
        "tdc_pair_count",
        "tdc_phase_r_max_abs_max",
        "tdc_best_lag_abs_r_max_max",
    ],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
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
        return f"{value:.9g}"
    return str(value)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def best_trng_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_placement: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        placement = row.get("placement", "")
        if placement:
            by_placement.setdefault(placement, []).append(row)

    out: dict[str, dict[str, str]] = {}
    for placement, placement_rows in by_placement.items():
        formal = [row for row in placement_rows if row.get("role") == "formal"]
        candidates = formal or placement_rows
        candidates.sort(key=lambda row: to_float(row.get("bytes_mean")) or -1, reverse=True)
        out[placement] = candidates[0]
    return out


def summarize_tdc_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        run = row.get("run", "")
        placement = ""
        for candidate in ("random1", "random3"):
            if f"tdc_pair_{candidate}_" in run:
                placement = candidate
                break
        if placement:
            grouped.setdefault(placement, []).append(row)

    numeric_fields = [
        "phase_r_mean",
        "phase_r_max_abs",
        "best_lag_abs_r_max",
        "diff_std_ps_mean",
        "diff_mean_ps_slope_per_window",
        "strong_lock_windows",
    ]
    out: dict[str, dict[str, str]] = {}
    for placement, placement_rows in grouped.items():
        result: dict[str, str] = {"tdc_pair_count": str(len(placement_rows))}
        for field in numeric_fields:
            values = [to_float(row.get(field)) for row in placement_rows]
            values_f = [value for value in values if value is not None]
            if not values_f:
                continue
            result[f"tdc_{field}_mean"] = fmt(mean(values_f))
            result[f"tdc_{field}_max"] = fmt(max(values_f))
        out[placement] = result
    return out


def audit_existing_table(path: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    header = list(rows[0].keys()) if rows else []
    out: list[dict[str, str]] = []
    for group, columns in REQUIRED_EXISTING_GROUPS.items():
        present = [column for column in columns if column in header]
        missing = [column for column in columns if column not in header]
        populated_cells = 0
        total_cells = len(rows) * len(present)
        for row in rows:
            populated_cells += sum(1 for column in present if row.get(column, "").strip())
        out.append(
            {
                "source": rel(path),
                "group": group,
                "required_columns": str(len(columns)),
                "present_columns": str(len(present)),
                "missing_columns": ";".join(missing),
                "rows": str(len(rows)),
                "populated_cells": str(populated_cells),
                "total_cells": str(total_cells),
                "coverage": fmt(populated_cells / total_cells if total_cells else None),
            }
        )
    return out


def build_restart_mechanism_rows(
    restart_rows: list[dict[str, str]],
    trng_by_placement: dict[str, dict[str, str]],
    ro_by_placement: dict[str, dict[str, str]],
    tdc_by_placement: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    for row in restart_rows:
        placement = row.get("placement", "")
        trng = trng_by_placement.get(placement, {})
        ro = ro_by_placement.get(placement, {})
        tdc = tdc_by_placement.get(placement, {})
        merged.append(
            {
                "placement": placement,
                "warmup_bytes": row.get("warmup_bytes", ""),
                "repeat_tag": row.get("repeat_tag", ""),
                "bit_order": row.get("bit_order", ""),
                "ea_status": row.get("ea_status", ""),
                "restart_h_i": row.get("h_i", ""),
                "restart_x_cutoff": row.get("x_cutoff", ""),
                "restart_x_max": row.get("x_max", ""),
                "restart_min_h": row.get("min_h", ""),
                "restart_overall_p1": row.get("overall_p1", ""),
                "restart_positions_over_x_cutoff": row.get("positions_over_x_cutoff", ""),
                "restart_worst_byte": row.get("worst_byte_index", ""),
                "restart_worst_bit": row.get("worst_bit_index", ""),
                "restart_worst_x": row.get("worst_x", ""),
                "restart_worst_msb_column": row.get("worst_msb_expanded_column", ""),
                "restart_worst_lsb_column": row.get("worst_lsb_expanded_column", ""),
                "trng_role": trng.get("role", ""),
                "trng_bytes_mean": trng.get("bytes_mean", ""),
                "trng_p1_mean": trng.get("p1_mean", ""),
                "trng_abs_bias_mean": trng.get("abs_bias_mean", ""),
                "trng_bit_min_entropy_mean": trng.get("bit_min_entropy_mean", ""),
                "trng_runs_p_mean": trng.get("runs_p_mean", ""),
                "trng_byte_min_entropy_mean": trng.get("byte_min_entropy_mean", ""),
                "rofreq_available": "yes" if ro else "no",
                "rofreq_ro_min_data_data_delta_mhz": ro.get("ro_min_data_data_delta_mhz", ""),
                "rofreq_ro_min_data_data_pair": ro.get("ro_min_data_data_pair", ""),
                "rofreq_ro_close_data_data_pairs_le_1mhz": ro.get("ro_close_data_data_pairs_le_1mhz", ""),
                "rofreq_ro_close_data_data_pairs_le_3mhz": ro.get("ro_close_data_data_pairs_le_3mhz", ""),
                "rofreq_ro_sample_shift_ppm": ro.get("ro_sample_shift_ppm", ""),
                "tdc_available": "yes" if tdc else "no",
                **tdc,
            }
        )
    return merged


def summarize_merged(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    placements = sorted({row.get("placement", "") for row in rows if row.get("placement")})
    for placement in placements:
        placement_rows = [row for row in rows if row.get("placement") == placement]
        failed = sum(1 for row in placement_rows if row.get("ea_status") == "failed")
        passed = sum(1 for row in placement_rows if row.get("ea_status") == "passed")
        x_values = [to_float(row.get("restart_x_max")) for row in placement_rows]
        x_values_f = [value for value in x_values if value is not None]
        h_values = [to_float(row.get("restart_min_h")) for row in placement_rows]
        h_values_f = [value for value in h_values if value is not None]
        first = placement_rows[0]
        out.append(
            {
                "placement": placement,
                "restart_rows": str(len(placement_rows)),
                "restart_failed_rows": str(failed),
                "restart_passed_rows": str(passed),
                "restart_x_max_mean": fmt(mean(x_values_f) if x_values_f else None),
                "restart_x_max_std": fmt(pstdev(x_values_f) if len(x_values_f) > 1 else None),
                "restart_min_h_mean_passed_only": fmt(mean(h_values_f) if h_values_f else None),
                "trng_bit_min_entropy_mean": first.get("trng_bit_min_entropy_mean", ""),
                "trng_abs_bias_mean": first.get("trng_abs_bias_mean", ""),
                "rofreq_available": first.get("rofreq_available", ""),
                "rofreq_ro_min_data_data_delta_mhz": first.get("rofreq_ro_min_data_data_delta_mhz", ""),
                "rofreq_ro_min_data_data_pair": first.get("rofreq_ro_min_data_data_pair", ""),
                "tdc_available": first.get("tdc_available", ""),
                "tdc_pair_count": first.get("tdc_pair_count", ""),
            }
        )
    return out


def write_markdown(
    path: Path,
    sources: dict[str, Path],
    audit_rows: list[dict[str, str]],
    merged_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> None:
    lines = [
        "# Mechanism Correlation Audit 20260523",
        "",
        "Offline-only audit of existing restart mechanism-correlation artifacts.",
        "",
        "## Inputs",
        "",
    ]
    for label, source in sources.items():
        lines.append(f"- {label}: `{rel(source)}`")

    lines.extend(
        [
            "",
            "## Existing table coverage",
            "",
            "| group | present / required columns | missing columns | populated cells | coverage |",
            "| --- | ---: | --- | ---: | ---: |",
        ]
    )
    for row in audit_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["group"],
                    f"{row['present_columns']} / {row['required_columns']}",
                    row["missing_columns"],
                    f"{row['populated_cells']} / {row['total_cells']}",
                    row["coverage"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Normalized restart summary",
            "",
            f"- Rows exported: `{len(merged_rows)}` restart rows.",
            f"- Placements exported: `{', '.join(row['placement'] for row in summary_rows)}`.",
            "- TRNG placement metrics are available for all exported placements.",
            "- RO_FREQ and TDC mechanism metrics are currently matched for `random1` and `random3` only.",
            "",
            "| placement | restart rows | failed | passed | x_max mean | TRNG bit Hmin | RO min delta MHz | TDC pairs |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["placement"],
                    row["restart_rows"],
                    row["restart_failed_rows"],
                    row["restart_passed_rows"],
                    row["restart_x_max_mean"],
                    row["trng_bit_min_entropy_mean"],
                    row["rofreq_ro_min_data_data_delta_mhz"],
                    row["tdc_pair_count"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "- The existing `table_restart_mechanism_link.csv` already combines restart worst-column fields, TRNG entropy fields, RO_FREQ features, and TDC summaries.",
            "- Its current populated rows cover `random1`/`random3`; the normalized export keeps the broader restart-summary rows and makes missing RO_FREQ/TDC coverage explicit.",
            "- Treat the combined evidence as a case-comparison table, not a statistically significant correlation analysis.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--existing-link", type=Path, default=DEFAULT_EXISTING_LINK)
    parser.add_argument("--restart", type=Path, default=DEFAULT_RESTART)
    parser.add_argument("--trng", type=Path, default=DEFAULT_TRNG)
    parser.add_argument("--ro-correlation", type=Path, default=DEFAULT_RO_CORRELATION)
    parser.add_argument("--tdc", type=Path, default=DEFAULT_TDC)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    existing_rows = read_csv(args.existing_link)
    restart_rows = read_csv(args.restart)
    trng_rows = read_csv(args.trng)
    ro_rows = read_csv(args.ro_correlation)
    tdc_rows = read_csv(args.tdc)

    if not existing_rows:
        raise SystemExit(f"missing or empty existing mechanism table: {args.existing_link}")
    if not restart_rows:
        raise SystemExit(f"missing or empty restart summary: {args.restart}")
    if not trng_rows:
        raise SystemExit(f"missing or empty TRNG table: {args.trng}")

    trng_by_placement = best_trng_by_placement(trng_rows)
    ro_by_placement = {row["placement"]: row for row in ro_rows if row.get("placement")}
    tdc_by_placement = summarize_tdc_by_placement(tdc_rows)

    audit_rows = audit_existing_table(args.existing_link, existing_rows)
    merged_rows = build_restart_mechanism_rows(restart_rows, trng_by_placement, ro_by_placement, tdc_by_placement)
    summary_rows = summarize_merged(merged_rows)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    audit_csv = args.out_dir / "existing_mechanism_table_audit.csv"
    merged_csv = args.out_dir / "restart_mechanism_correlation_rows.csv"
    summary_csv = args.out_dir / "restart_mechanism_correlation_by_placement.csv"
    readme = args.out_dir / "README.md"

    write_csv(audit_csv, audit_rows)
    write_csv(merged_csv, merged_rows)
    write_csv(summary_csv, summary_rows)
    write_markdown(
        readme,
        {
            "existing restart mechanism link": args.existing_link,
            "restart result summary": args.restart,
            "TRNG placement metrics": args.trng,
            "RO_FREQ random1/random3 features": args.ro_correlation,
            "TDC pair dynamics summary": args.tdc,
        },
        audit_rows,
        merged_rows,
        summary_rows,
    )

    print(f"Wrote {audit_csv}")
    print(f"Wrote {merged_csv}")
    print(f"Wrote {summary_csv}")
    print(f"Wrote {readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
