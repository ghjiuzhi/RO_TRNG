#!/usr/bin/env python3
"""Merge TRNG placement metrics with offline RO-frequency mechanism features.

This script is intentionally offline-only. It reads existing Markdown/CSV
analysis outputs and writes a case-comparison table for random1/random3.
With only two placements, the output is mechanism evidence for comparison,
not a statistically meaningful correlation analysis.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRNG = ROOT / "data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md"
DEFAULT_RO_DIR = ROOT / "data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib"
DEFAULT_OUT_CSV = ROOT / "data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv"
DEFAULT_OUT_MD = ROOT / "data/experiments/correlation/20260513_random1_random3_mechanism_correlation.md"


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return float(value)


def fmt(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(cell.replace("-", "").replace(":", "").strip() == "" for cell in cells):
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def trng_formal_features(path: Path, placements: set[str]) -> dict[str, dict[str, object]]:
    rows = parse_markdown_table(path)
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        placement = row.get("placement", "")
        if placement not in placements or row.get("sample_role") != "formal":
            continue
        result[placement] = {
            "placement": placement,
            "trng_sample_role": row.get("sample_role"),
            "trng_target_bytes": to_float(row.get("target_bytes")),
            "trng_p1": to_float(row.get("p1_mean")),
            "trng_abs_bias": to_float(row.get("abs_bias_mean")),
            "trng_bit_min_entropy": to_float(row.get("bit_min_entropy_mean")),
            "trng_monobit_p": to_float(row.get("monobit_p_mean")),
            "trng_runs_p": to_float(row.get("runs_p_mean")),
            "trng_adjacent_equal_ratio": to_float(row.get("adjacent_equal_ratio_mean")),
            "trng_byte_min_entropy": to_float(row.get("byte_min_entropy_mean")),
        }
    return result


def frequency_features(summary_path: Path, placements: set[str]) -> dict[str, dict[str, object]]:
    rows = read_csv(summary_path)
    result: dict[str, dict[str, object]] = {}
    for placement in placements:
        all_on = [
            row for row in rows
            if row["family"] == placement and row["mode"] == "all_on" and row["target_name"].startswith("data")
        ]
        sample = [
            row for row in rows
            if row["family"] == placement and row["mode"] == "all_on" and row["target_name"] == "sample"
        ]
        freqs = [to_float(row["freq_mean_mhz"]) for row in all_on]
        freqs_f = [freq for freq in freqs if freq is not None]
        result[placement] = {
            "ro_data_count": len(freqs_f),
            "ro_data_mean_freq_mhz": mean(freqs_f) if freqs_f else None,
            "ro_data_std_freq_mhz": pstdev(freqs_f) if len(freqs_f) > 1 else None,
            "ro_data_min_freq_mhz": min(freqs_f) if freqs_f else None,
            "ro_data_max_freq_mhz": max(freqs_f) if freqs_f else None,
            "ro_data_span_mhz": (max(freqs_f) - min(freqs_f)) if freqs_f else None,
            "ro_sample_all_on_freq_mhz": to_float(sample[0]["freq_mean_mhz"]) if sample else None,
        }
    return result


def pairwise_features(pairwise_path: Path, placements: set[str]) -> dict[str, dict[str, object]]:
    rows = read_csv(pairwise_path)
    result: dict[str, dict[str, object]] = {}
    for placement in placements:
        data_pairs = [
            row for row in rows
            if row["family"] == placement and row["mode"] == "all_on" and row["relation"] == "data_data"
        ]
        sample_pairs = [
            row for row in rows
            if row["family"] == placement and row["mode"] == "all_on" and row["relation"] == "data_sample"
        ]
        data_pairs.sort(key=lambda row: float(row["abs_delta_f_mhz"]))
        sample_pairs.sort(key=lambda row: float(row["abs_delta_f_mhz"]))
        nearest = data_pairs[0] if data_pairs else None
        second = data_pairs[1] if len(data_pairs) > 1 else None
        nearest_sample = sample_pairs[0] if sample_pairs else None
        result[placement] = {
            "ro_min_data_data_delta_mhz": to_float(nearest["abs_delta_f_mhz"]) if nearest else None,
            "ro_min_data_data_pair": f"{nearest['a_name']}/{nearest['b_name']}" if nearest else "",
            "ro_min_data_data_beat_ns": to_float(nearest["beat_period_ns"]) if nearest else None,
            "ro_second_data_data_delta_mhz": to_float(second["abs_delta_f_mhz"]) if second else None,
            "ro_second_data_data_pair": f"{second['a_name']}/{second['b_name']}" if second else "",
            "ro_close_data_data_pairs_le_1mhz": sum(float(row["abs_delta_f_mhz"]) <= 1.0 for row in data_pairs),
            "ro_close_data_data_pairs_le_3mhz": sum(float(row["abs_delta_f_mhz"]) <= 3.0 for row in data_pairs),
            "ro_nearest_data_sample_delta_mhz": to_float(nearest_sample["abs_delta_f_mhz"]) if nearest_sample else None,
            "ro_nearest_data_sample_pair": f"{nearest_sample['a_name']}/{nearest_sample['b_name']}" if nearest_sample else "",
            "ro_nearest_data_sample_beat_ns": to_float(nearest_sample["beat_period_ns"]) if nearest_sample else None,
        }
    return result


def pulling_features(pulling_path: Path, placements: set[str]) -> dict[str, dict[str, object]]:
    rows = read_csv(pulling_path)
    result: dict[str, dict[str, object]] = {}
    for placement in placements:
        data_rows = [row for row in rows if row["family"] == placement and row["target_name"].startswith("data")]
        sample_rows = [row for row in rows if row["family"] == placement and row["target_name"] == "sample"]
        data_shift_mhz = [float(row["shift_mhz"]) for row in data_rows]
        data_shift_ppm = [float(row["shift_ppm_vs_single"]) for row in data_rows]
        sample = sample_rows[0] if sample_rows else None
        result[placement] = {
            "ro_data_mean_shift_mhz": mean(data_shift_mhz) if data_shift_mhz else None,
            "ro_data_mean_abs_shift_ppm": mean(abs(v) for v in data_shift_ppm) if data_shift_ppm else None,
            "ro_data_max_abs_shift_ppm": max(abs(v) for v in data_shift_ppm) if data_shift_ppm else None,
            "ro_sample_shift_mhz": to_float(sample["shift_mhz"]) if sample else None,
            "ro_sample_shift_ppm": to_float(sample["shift_ppm_vs_single"]) if sample else None,
            "ro_sample_abs_shift_ppm": abs(float(sample["shift_ppm_vs_single"])) if sample else None,
        }
    return result


def merge_rows(*feature_sets: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    placements = sorted(set().union(*(features.keys() for features in feature_sets)))
    rows: list[dict[str, object]] = []
    for placement in placements:
        row: dict[str, object] = {}
        for features in feature_sets:
            row.update(features.get(placement, {}))
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def diff_line(rows: list[dict[str, object]], key: str) -> str:
    by_name = {row["placement"]: row for row in rows}
    a = by_name.get("random1", {}).get(key)
    b = by_name.get("random3", {}).get(key)
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return ""
    return f"| `{key}` | {fmt(a)} | {fmt(b)} | {fmt(a - b)} |"


def write_markdown(path: Path, rows: list[dict[str, object]], sources: dict[str, Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = len(rows)
    lines = [
        "# random1/random3 TRNG vs RO-frequency mechanism case comparison",
        "",
        "Generated by `scripts/merge_trng_ro_freq_features.py` from existing offline analysis files only.",
        "",
        "## Scope and limitation",
        "",
        f"- Samples merged: {n} placement cases (`random1`, `random3`).",
        "- Because this has only two placement cases, it is a case comparison, not a statistically significant correlation analysis.",
        "- Do not report Pearson/Spearman p-values or regression significance from this table. Add more placement cases before making statistical correlation claims.",
        "- The RO-frequency features are mechanism clues from run01 fixed-frequency counters; they do not prove causality for TRNG bias.",
        "",
        "## Input files",
        "",
    ]
    for label, source in sources.items():
        lines.append(f"- {label}: `{source.relative_to(ROOT).as_posix()}`")
    lines.extend([
        "",
        "## Merged feature table",
        "",
    ])

    columns = [
        "placement",
        "trng_p1",
        "trng_abs_bias",
        "trng_bit_min_entropy",
        "trng_adjacent_equal_ratio",
        "trng_byte_min_entropy",
        "ro_min_data_data_pair",
        "ro_min_data_data_delta_mhz",
        "ro_min_data_data_beat_ns",
        "ro_sample_shift_ppm",
        "ro_data_mean_abs_shift_ppm",
        "ro_close_data_data_pairs_le_1mhz",
        "ro_close_data_data_pairs_le_3mhz",
    ]
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(column)) for column in columns) + " |")

    lines.extend([
        "",
        "## Direct random1 - random3 differences",
        "",
        "| metric | random1 | random3 | random1 - random3 |",
        "| --- | ---: | ---: | ---: |",
    ])
    for key in [
        "trng_abs_bias",
        "trng_bit_min_entropy",
        "trng_byte_min_entropy",
        "ro_min_data_data_delta_mhz",
        "ro_sample_shift_ppm",
        "ro_sample_abs_shift_ppm",
        "ro_data_mean_abs_shift_ppm",
        "ro_close_data_data_pairs_le_1mhz",
        "ro_close_data_data_pairs_le_3mhz",
    ]:
        line = diff_line(rows, key)
        if line:
            lines.append(line)

    lines.extend([
        "",
        "## Interpretation guardrails",
        "",
        "- Supported: a paper table/figure that places TRNG quality metrics beside close-pair and pulling metrics for random1/random3.",
        "- Supported: a mechanism-evidence statement that random1 combines strong TRNG bias with a very close data-data pair and a large positive sample-RO shift in run01.",
        "- Not supported: claiming that close-frequency pairs alone explain the bias, because random3 also has a close pair while its TRNG output is near ideal.",
        "- Not supported: claiming statistically significant correlation until more placements have matched TRNG and RO-frequency mechanism features.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trng", type=Path, default=DEFAULT_TRNG)
    parser.add_argument("--ro-dir", type=Path, default=DEFAULT_RO_DIR)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument("--placements", default="random1,random3")
    args = parser.parse_args()

    placements = {item.strip() for item in args.placements.split(",") if item.strip()}
    summary_path = args.ro_dir / "random1_random3_fixed_run01_2mib_summary.csv"
    pairwise_path = args.ro_dir / "random1_random3_fixed_run01_2mib_pairwise_all_on.csv"
    pulling_path = args.ro_dir / "random1_random3_fixed_run01_2mib_pulling.csv"

    rows = merge_rows(
        trng_formal_features(args.trng, placements),
        frequency_features(summary_path, placements),
        pairwise_features(pairwise_path, placements),
        pulling_features(pulling_path, placements),
    )
    write_csv(args.out_csv, rows)
    write_markdown(
        args.out_md,
        rows,
        {
            "TRNG placement metrics": args.trng,
            "RO frequency summary": summary_path,
            "RO all-on pairwise metrics": pairwise_path,
            "RO pulling metrics": pulling_path,
        },
    )
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")
    if len(rows) <= 2:
        print("Only two placement cases are present; treat output as case comparison, not statistical correlation.")


if __name__ == "__main__":
    main()
