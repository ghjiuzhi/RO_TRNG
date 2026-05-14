#!/usr/bin/env python3
"""Build the 2026-05-14 paper evidence artifact pack.

Offline-only: this script reads already-produced fast-mode and TDC pair
analysis outputs, then writes compact CSV/Markdown/SVG tables for paper use.
It does not access hardware, Vivado, COM, JTAG, or hw_server.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAST_DIR = ROOT / "data" / "experiments" / "fast_mode" / "offline_figures_20260513"
DEFAULT_TDC_DYNAMICS = ROOT / "data" / "experiments" / "tdc_pair_dynamics" / "tdc_pair_dynamics_20260514.csv"
DEFAULT_TDC_DYNAMICS_MD = ROOT / "data" / "experiments" / "tdc_pair_dynamics" / "tdc_pair_dynamics_20260514.md"
DEFAULT_OUT = ROOT / "data" / "experiments" / "paper_artifacts_20260514"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_cell(row.get(key, "")) for key in fields})


def format_cell(value: object) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def format_markdown_cell(value: object) -> str:
    return format_cell(value).replace("|", "\\|")


def as_float(row: dict[str, str], key: str, default: float = math.nan) -> float:
    value = row.get(key, "")
    if value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def as_int(row: dict[str, str], key: str, default: int = 0) -> int:
    value = as_float(row, key)
    return default if math.isnan(value) else int(value)


def markdown_table(path: Path, title: str, rows: list[dict[str, object]], fields: list[str], note: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        if note:
            f.write(note.rstrip() + "\n\n")
        f.write("| " + " | ".join(fields) + " |\n")
        f.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(format_markdown_cell(row.get(field, "")) for field in fields) + " |\n")


def copy_table(src_csv: Path, src_md: Path, out_csv: Path, out_md: Path, title: str) -> list[dict[str, str]]:
    rows = read_csv(src_csv)
    fields = list(rows[0].keys()) if rows else []
    write_csv(out_csv, rows, fields)
    if src_md.exists():
        text = src_md.read_text(encoding="utf-8")
        out_md.write_text(text, encoding="utf-8")
    else:
        markdown_table(out_md, title, rows, fields)
    return rows


def summarize_tdc_pair_dynamics(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_run: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_run[row["run"]].append(row)

    summary: list[dict[str, object]] = []
    for run, run_rows in sorted(by_run.items()):
        phase_r = [as_float(row, "phase_pearson_r") for row in run_rows]
        best_lag_abs = [as_float(row, "best_lag_abs_phase_pearson_r") for row in run_rows]
        diff_std = [as_float(row, "diff_std_ps") for row in run_rows]
        diff_mean = [as_float(row, "diff_mean_ps") for row in run_rows]
        best_idx = max(range(len(run_rows)), key=lambda i: best_lag_abs[i])
        summary.append(
            {
                "run": run,
                "windows": len(run_rows),
                "packets": sum(as_int(row, "packets") for row in run_rows),
                "phase_r_mean": statistics.fmean(phase_r),
                "phase_r_max_abs": max(abs(v) for v in phase_r),
                "best_lag_abs_r_max": best_lag_abs[best_idx],
                "best_lag_at_window": as_int(run_rows[best_idx], "window_index"),
                "best_lag_packets": as_int(run_rows[best_idx], "best_lag_packets"),
                "diff_std_ps_mean": statistics.fmean(diff_std),
                "diff_mean_ps_span": max(diff_mean) - min(diff_mean),
                "diff_mean_ps_slope_per_window": as_float(run_rows[0], "run_diff_mean_ps_slope_per_window"),
                "strong_lock_windows": sum(as_int(row, "strong_lock_window") for row in run_rows),
                "claim_reading": "no strong pair locking detected",
            }
        )
    return summary


def make_claims_table(
    trng_rows: list[dict[str, str]],
    ro_pull_rows: list[dict[str, str]],
    tdc_summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    formal_rows = [row for row in trng_rows if row.get("role") == "formal"]
    repeat_rows = [row for row in trng_rows if row.get("role") == "repeat"]
    formal_min_h = min(as_float(row, "bit_min_entropy_mean") for row in formal_rows)
    formal_max_bias = max(as_float(row, "abs_bias_mean") for row in formal_rows)
    repeat_max_delta = 0.0
    by_placement: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in trng_rows:
        by_placement[row["placement"]][row["role"]] = row
    for roles in by_placement.values():
        if "formal" in roles and "repeat" in roles:
            delta = abs(as_float(roles["formal"], "bit_min_entropy_mean") - as_float(roles["repeat"], "bit_min_entropy_mean"))
            repeat_max_delta = max(repeat_max_delta, delta)

    max_sample_pull_ppm = max(abs(as_float(row, "sample_shift_ppm")) for row in ro_pull_rows)
    max_data_abs_ppm = max(as_float(row, "data_mean_abs_ppm") for row in ro_pull_rows)
    max_lag_r = max(float(row["best_lag_abs_r_max"]) for row in tdc_summary)
    strong_windows = sum(int(row["strong_lock_windows"]) for row in tdc_summary)

    return [
        {
            "claim": "Placement changes TRNG quality under fast-mode captures",
            "evidence_table": "table_placement_trng_repeats.csv/md",
            "key_number": f"formal bit_min_entropy_mean min={formal_min_h:.6g}; max abs_bias_mean={formal_max_bias:.6g}",
            "status": "supported, with weak placements explicitly visible",
            "caveat": "fast-mode dataset; not a substitute for full SP800-90B certification",
        },
        {
            "claim": "Repeat captures are broadly consistent at placement level",
            "evidence_table": "table_placement_trng_repeats.csv/md",
            "key_number": f"max formal-repeat bit_min_entropy_mean delta={repeat_max_delta:.6g}",
            "status": "supported for available repeats",
            "caveat": "some placements have repeat-only rows and are excluded from paired delta",
        },
        {
            "claim": "All-on operation measurably pulls RO frequencies",
            "evidence_table": "table_ro_freq_pulling_summary.csv/md",
            "key_number": f"max |sample_shift_ppm|={max_sample_pull_ppm:.6g}; max data_mean_abs_ppm={max_data_abs_ppm:.6g}",
            "status": "supported",
            "caveat": "summarizes random1/random3 RO_FREQ run only",
        },
        {
            "claim": "The six monitored TDC RO pairs do not show strong phase locking",
            "evidence_table": "table_tdc_pair_dynamics_summary.csv/md",
            "key_number": f"max small-lag |r|={max_lag_r:.6g}; strong_lock_windows={strong_windows}",
            "status": "negative/null evidence for strong locking",
            "caveat": "does not rule out coupling under other placements, voltage, temperature, or longer captures",
        },
    ]


def bar_svg(path: Path, rows: list[dict[str, object]], value_key: str, title: str) -> None:
    width, height = 960, 420
    margin_left, margin_right, margin_top, margin_bottom = 86, 30, 52, 122
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    values = [float(row[value_key]) for row in rows]
    max_v = max(values) if values else 1.0
    bar_gap = 14
    bar_w = max(24, (plot_w - bar_gap * max(0, len(rows) - 1)) / max(1, len(rows)))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2:.1f}" y="30" text-anchor="middle" font-family="Arial" font-size="18">{title}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#333"/>',
    ]
    for i, row in enumerate(rows):
        value = float(row[value_key])
        x = margin_left + i * (bar_w + bar_gap)
        h = value / max_v * plot_h if max_v else 0.0
        y = margin_top + plot_h - h
        label = str(row["run"]).replace("tdc_pair_", "").replace("_run01_2mib", "")
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{max(h, 1):.1f}" fill="#2f6f73"/>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" font-family="Arial" font-size="11">{value:.4g}</text>')
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{height - 92}" transform="rotate(42 {x + bar_w / 2:.1f},{height - 92})" '
            f'text-anchor="start" font-family="Arial" font-size="11">{label}</text>'
        )
    parts.append("</svg>\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def write_readme(
    out_dir: Path,
    tdc_summary: list[dict[str, object]],
    claims: list[dict[str, object]],
    source_fast_dir: Path,
    source_tdc_csv: Path,
) -> None:
    max_lag = max(float(row["best_lag_abs_r_max"]) for row in tdc_summary)
    strong_windows = sum(int(row["strong_lock_windows"]) for row in tdc_summary)
    lines = [
        "# Paper Artifacts 20260514",
        "",
        "Offline evidence pack generated from existing analysis outputs only.",
        "",
        "## Sources",
        "",
        f"- `{source_fast_dir}`",
        f"- `{source_tdc_csv}`",
        "",
        "## Required Tables",
        "",
        "- `table_placement_trng_repeats.csv/md`",
        "- `table_ro_freq_pulling_summary.csv/md`",
        "- `table_tdc_pair_dynamics_summary.csv/md`",
        "- `claims_vs_evidence.csv/md`",
        "",
        "## Figures",
        "",
        "- `fig_tdc_pair_best_lag_abs_r.svg`",
        "",
        "## Quick Read",
        "",
        f"- Six pair-specific TDC dynamic runs are included; max small-lag `|r|` is `{max_lag:.6g}`.",
        f"- Conservative strong-lock windows across all TDC pair windows: `{strong_windows}`.",
        f"- Claims table entries: `{len(claims)}`.",
    ]
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast-dir", type=Path, default=DEFAULT_FAST_DIR)
    parser.add_argument("--tdc-dynamics-csv", type=Path, default=DEFAULT_TDC_DYNAMICS)
    parser.add_argument("--tdc-dynamics-md", type=Path, default=DEFAULT_TDC_DYNAMICS_MD)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    trng_rows = copy_table(
        args.fast_dir / "table_trng_repeat_by_placement.csv",
        args.fast_dir / "table_trng_repeat_by_placement.md",
        out_dir / "table_placement_trng_repeats.csv",
        out_dir / "table_placement_trng_repeats.md",
        "Placement/TRNG Repeat Table",
    )
    ro_pull_rows = copy_table(
        args.fast_dir / "table_ro_freq_pulling_summary.csv",
        args.fast_dir / "table_ro_freq_pulling_summary.md",
        out_dir / "table_ro_freq_pulling_summary.csv",
        out_dir / "table_ro_freq_pulling_summary.md",
        "RO_FREQ Pulling Summary",
    )

    tdc_rows = read_csv(args.tdc_dynamics_csv)
    tdc_summary = summarize_tdc_pair_dynamics(tdc_rows)
    tdc_fields = [
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
    write_csv(out_dir / "table_tdc_pair_dynamics_summary.csv", tdc_summary, tdc_fields)
    markdown_table(
        out_dir / "table_tdc_pair_dynamics_summary.md",
        "TDC Pair Dynamics Summary",
        tdc_summary,
        tdc_fields,
        "Six pair-specific TDC dynamic captures summarized from windowed analysis.",
    )
    copy_table(
        args.tdc_dynamics_csv,
        args.tdc_dynamics_md,
        out_dir / "table_tdc_pair_dynamics_windows.csv",
        out_dir / "table_tdc_pair_dynamics_windows.md",
        "TDC Pair Dynamics Windows",
    )
    bar_svg(out_dir / "fig_tdc_pair_best_lag_abs_r.svg", tdc_summary, "best_lag_abs_r_max", "TDC pair max small-lag absolute phase correlation")

    claims = make_claims_table(trng_rows, ro_pull_rows, tdc_summary)
    claim_fields = ["claim", "evidence_table", "key_number", "status", "caveat"]
    write_csv(out_dir / "claims_vs_evidence.csv", claims, claim_fields)
    markdown_table(out_dir / "claims_vs_evidence.md", "Claims vs Evidence", claims, claim_fields)
    write_readme(out_dir, tdc_summary, claims, args.fast_dir, args.tdc_dynamics_csv)

    print(f"Wrote paper artifacts to {out_dir}")
    print(f"tdc_pair_runs={len(tdc_summary)}")
    print(f"strong_lock_windows={sum(int(row['strong_lock_windows']) for row in tdc_summary)}")


if __name__ == "__main__":
    main()
