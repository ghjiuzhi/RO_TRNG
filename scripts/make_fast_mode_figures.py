#!/usr/bin/env python3
"""Build fast-mode offline paper table/figure data from existing CSVs.

This script is intentionally offline-only.  It reads already-produced TRNG,
RO_FREQ, and TDC CSV analysis files and writes derived CSV/Markdown/SVG files.
It does not touch COM ports, JTAG, hw_server, or Vivado.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "experiments" / "fast_mode" / "offline_figures_20260513"
DEFAULT_TRNG_FORMAL = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "trng" / "trng_formal_all_10mib_ranked.csv"
DEFAULT_TRNG_REPEATS = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "trng" / "trng_repeats_by_placement.csv"
DEFAULT_RO_FREQ = ROOT / "data" / "experiments" / "ro_freq_analysis" / "20260513_random1_random3_fixed_run01_2mib"
DEFAULT_TDC_COMPARE = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "tdc" / "tdc_near_far_compare.csv"
DEFAULT_TDC_ROOT = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "tdc"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str, default: float = 0.0) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return default
    try:
        return float(value)
    except ValueError:
        return default


def short_float(value: object, digits: int = 6) -> str:
    if isinstance(value, float):
        return f"{value:.{digits}g}"
    return str(value)


def markdown_table(path: Path, title: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        out.write("| " + " | ".join(fields) + " |\n")
        out.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
        for row in rows:
            out.write("| " + " | ".join(short_float(row.get(field, "")) for field in fields) + " |\n")


def bar_svg(
    path: Path,
    rows: list[dict[str, object]],
    label_key: str,
    value_key: str,
    title: str,
    width: int = 920,
    height: int = 420,
    color: str = "#3465a4",
) -> None:
    margin_left, margin_right, margin_top, margin_bottom = 80, 30, 46, 96
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    values = [float(row[value_key]) for row in rows]
    max_v = max(values) if values else 1.0
    min_v = min(0.0, min(values) if values else 0.0)
    span = max(max_v - min_v, 1e-12)
    bar_gap = 4
    bar_w = max(4, (plot_w - bar_gap * max(0, len(rows) - 1)) / max(1, len(rows)))
    zero_y = margin_top + plot_h - ((0.0 - min_v) / span) * plot_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2:.1f}" y="26" text-anchor="middle" font-family="Arial" font-size="18">{title}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_h:.1f}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h:.1f}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{zero_y:.1f}" x2="{margin_left + plot_w}" y2="{zero_y:.1f}" stroke="#999" stroke-dasharray="4 4"/>',
    ]
    for i, row in enumerate(rows):
        value = float(row[value_key])
        x = margin_left + i * (bar_w + bar_gap)
        y = margin_top + plot_h - ((value - min_v) / span) * plot_h
        if value >= 0:
            rect_y = y
            rect_h = zero_y - y
        else:
            rect_y = zero_y
            rect_h = y - zero_y
        label = str(row[label_key])
        parts.append(f'<rect x="{x:.1f}" y="{rect_y:.1f}" width="{bar_w:.1f}" height="{max(rect_h, 1):.1f}" fill="{color}"/>')
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{height - 62}" transform="rotate(45 {x + bar_w / 2:.1f},{height - 62})" '
            f'text-anchor="start" font-family="Arial" font-size="11">{label}</text>'
        )
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{rect_y - 4 if value >= 0 else rect_y + rect_h + 13:.1f}" text-anchor="middle" font-family="Arial" font-size="10">{value:.3g}</text>')
    parts.append("</svg>\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def line_svg(
    path: Path,
    rows: list[dict[str, object]],
    x_key: str,
    series: list[tuple[str, str]],
    title: str,
    width: int = 920,
    height: int = 420,
) -> None:
    margin_left, margin_right, margin_top, margin_bottom = 76, 28, 48, 54
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    xs = [float(row[x_key]) for row in rows]
    vals = [float(row[key]) for key, _ in series for row in rows]
    if not xs or not vals:
        path.write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"/>\n", encoding="utf-8")
        return
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(vals), max(vals)
    x_span = max(max_x - min_x, 1e-12)
    y_span = max(max_y - min_y, 1e-12)

    def sx(x: float) -> float:
        return margin_left + (x - min_x) / x_span * plot_w

    def sy(y: float) -> float:
        return margin_top + plot_h - (y - min_y) / y_span * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2:.1f}" y="27" text-anchor="middle" font-family="Arial" font-size="18">{title}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#333"/>',
    ]
    for key, color in series:
        points = " ".join(f"{sx(float(row[x_key])):.1f},{sy(float(row[key])):.1f}" for row in rows)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        for row in rows:
            parts.append(f'<circle cx="{sx(float(row[x_key])):.1f}" cy="{sy(float(row[key])):.1f}" r="2.5" fill="{color}"/>')
        parts.append(f'<text x="{margin_left + 8}" y="{margin_top + 16 + 18 * series.index((key, color))}" font-family="Arial" font-size="12" fill="{color}">{key}</text>')
    parts.append("</svg>\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def make_trng_tables(formal_path: Path, repeats_path: Path, out_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    formal_rows = read_csv(formal_path)
    trng_rows = []
    for row in formal_rows:
        name = row["run"]
        placement = name.rsplit("_", 1)[0]
        trng_rows.append(
            {
                "placement": placement,
                "run": name,
                "bytes": int(f(row, "bytes")),
                "p1": f(row, "p1"),
                "abs_bias": abs(f(row, "p1") - 0.5),
                "bit_min_entropy": f(row, "bit_min_entropy"),
                "monobit_p": f(row, "monobit_p"),
                "runs_p": f(row, "runs_p"),
                "adjacent_equal_ratio": f(row, "adjacent_equal_ratio"),
                "adjacent_dev": abs(f(row, "adjacent_equal_ratio") - 0.5),
                "byte_min_entropy": f(row, "byte_min_entropy"),
            }
        )
    trng_rows.sort(key=lambda row: float(row["bit_min_entropy"]))
    trng_fields = [
        "placement",
        "run",
        "p1",
        "abs_bias",
        "bit_min_entropy",
        "monobit_p",
        "runs_p",
        "adjacent_equal_ratio",
        "byte_min_entropy",
    ]
    write_csv(out_dir / "table_trng_formal_fast_metrics.csv", trng_rows, trng_fields)
    markdown_table(out_dir / "table_trng_formal_fast_metrics.md", "TRNG Formal Fast Metrics", trng_rows, trng_fields)

    repeat_rows = []
    for row in read_csv(repeats_path):
        repeat_rows.append(
            {
                "placement": row["placement"],
                "role": row["sample_role"],
                "bytes_mean": f(row, "bytes_mean"),
                "p1_mean": f(row, "p1_mean"),
                "abs_bias_mean": f(row, "abs_bias_mean"),
                "bit_min_entropy_mean": f(row, "bit_min_entropy_mean"),
                "runs_p_mean": f(row, "runs_p_mean"),
                "adjacent_equal_ratio_mean": f(row, "adjacent_equal_ratio_mean"),
                "byte_min_entropy_mean": f(row, "byte_min_entropy_mean"),
            }
        )
    repeat_fields = list(repeat_rows[0].keys()) if repeat_rows else []
    write_csv(out_dir / "table_trng_repeat_by_placement.csv", repeat_rows, repeat_fields)
    markdown_table(out_dir / "table_trng_repeat_by_placement.md", "TRNG Repeat by Placement", repeat_rows, repeat_fields)

    bar_svg(out_dir / "fig_trng_bit_min_entropy.svg", trng_rows, "placement", "bit_min_entropy", "10MiB TRNG bit min-entropy", color="#2f7d32")
    bar_svg(out_dir / "fig_trng_abs_bias.svg", sorted(trng_rows, key=lambda row: float(row["abs_bias"]), reverse=True), "placement", "abs_bias", "10MiB TRNG absolute bit bias", color="#9a3412")
    bar_svg(out_dir / "fig_trng_adjacent_deviation.svg", sorted(trng_rows, key=lambda row: float(row["adjacent_dev"]), reverse=True), "placement", "adjacent_dev", "Adjacent-equal deviation from 0.5", color="#5b4b8a")
    return trng_rows, repeat_rows


def make_ro_freq_tables(ro_dir: Path, out_dir: Path, top_n: int) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    prefix = ro_dir.name.split("20260513_", 1)[-1]
    pairwise_path = ro_dir / f"{prefix}_pairwise_all_on.csv"
    pulling_path = ro_dir / f"{prefix}_pulling.csv"
    summary_path = ro_dir / f"{prefix}_summary.csv"
    if not pairwise_path.exists():
        pairwise_path = next(ro_dir.glob("*_pairwise_all_on.csv"))
    if not pulling_path.exists():
        pulling_path = next(ro_dir.glob("*_pulling.csv"))
    if not summary_path.exists():
        summary_path = next(ro_dir.glob("*_summary.csv"))

    pair_rows = [
        row
        for row in read_csv(pairwise_path)
        if row.get("mode") == "all_on" and row.get("relation") == "data_data"
    ]
    pair_rows.sort(key=lambda row: f(row, "abs_delta_f_mhz"))
    closest = []
    per_family_counts: dict[str, int] = {}
    for row in pair_rows:
        family = row["family"]
        per_family_counts[family] = per_family_counts.get(family, 0)
        if per_family_counts[family] >= top_n:
            continue
        per_family_counts[family] += 1
        closest.append(
            {
                "family": family,
                "pair": f"{row['a_name']}/{row['b_name']}",
                "freq_a_mhz": f(row, "freq_a_mhz"),
                "freq_b_mhz": f(row, "freq_b_mhz"),
                "abs_delta_f_mhz": f(row, "abs_delta_f_mhz"),
                "beat_period_ns": f(row, "beat_period_ns"),
            }
        )
    closest_fields = list(closest[0].keys()) if closest else []
    write_csv(out_dir / "table_ro_freq_closest_beats.csv", closest, closest_fields)
    markdown_table(out_dir / "table_ro_freq_closest_beats.md", "RO_FREQ Closest All-On Data/Data Beats", closest, closest_fields)
    bar_svg(out_dir / "fig_ro_freq_closest_beats.svg", closest, "pair", "abs_delta_f_mhz", "Closest data/data RO_FREQ beat deltas", color="#26667f")

    pulls = read_csv(pulling_path)
    by_family: dict[str, list[dict[str, str]]] = {}
    for row in pulls:
        by_family.setdefault(row["family"], []).append(row)
    pull_summary = []
    for family, rows in sorted(by_family.items()):
        data_rows = [row for row in rows if row["target_name"].startswith("data")]
        sample_rows = [row for row in rows if row["target_name"] == "sample"]
        shifts = [f(row, "shift_mhz") for row in data_rows]
        ppms = [abs(f(row, "shift_ppm_vs_single")) for row in data_rows]
        sample = sample_rows[0] if sample_rows else {}
        pull_summary.append(
            {
                "family": family,
                "data_shift_min_mhz": min(shifts) if shifts else 0.0,
                "data_shift_max_mhz": max(shifts) if shifts else 0.0,
                "data_shift_mean_mhz": sum(shifts) / len(shifts) if shifts else 0.0,
                "data_mean_abs_ppm": sum(ppms) / len(ppms) if ppms else 0.0,
                "sample_shift_mhz": f(sample, "shift_mhz") if sample else 0.0,
                "sample_shift_ppm": f(sample, "shift_ppm_vs_single") if sample else 0.0,
            }
        )
    pull_fields = list(pull_summary[0].keys()) if pull_summary else []
    write_csv(out_dir / "table_ro_freq_pulling_summary.csv", pull_summary, pull_fields)
    markdown_table(out_dir / "table_ro_freq_pulling_summary.md", "RO_FREQ All-On vs Single-On Pulling", pull_summary, pull_fields)
    bar_svg(out_dir / "fig_ro_freq_sample_pulling_ppm.svg", pull_summary, "family", "sample_shift_ppm", "RO_FREQ sample pulling ppm", color="#9b2c2c")

    summary_rows = read_csv(summary_path)
    write_csv(out_dir / "figure_data_ro_freq_summary_all_on.csv", [row for row in summary_rows if row.get("mode") == "all_on"])
    return closest, pull_summary


def make_tdc_tables(tdc_compare_path: Path, tdc_root: Path, out_dir: Path) -> list[dict[str, object]]:
    metrics = []
    for row in read_csv(tdc_compare_path):
        metrics.append(
            {
                "run": row["run"],
                "packets": int(f(row, "packets")),
                "seq_gaps": int(f(row, "seq_gaps")),
                "lane_a_std_phase_ps": f(row, "lane_a_std_phase_ps"),
                "lane_b_std_phase_ps": f(row, "lane_b_std_phase_ps"),
                "diff_std_ps": f(row, "diff_std_ps"),
                "bin_pearson_r": f(row, "bin_pearson_r"),
                "phase_pearson_r": f(row, "phase_pearson_r"),
                "lane_a_shannon_bin": f(row, "lane_a_shannon_bin"),
                "lane_b_shannon_bin": f(row, "lane_b_shannon_bin"),
                "lane_a_min_entropy_bin": f(row, "lane_a_min_entropy_bin"),
                "lane_b_min_entropy_bin": f(row, "lane_b_min_entropy_bin"),
                "lane_a_used_bins": int(f(row, "lane_a_used_bins")),
                "lane_b_used_bins": int(f(row, "lane_b_used_bins")),
            }
        )
    fields = list(metrics[0].keys()) if metrics else []
    write_csv(out_dir / "table_tdc_diff_phase_metrics.csv", metrics, fields)
    markdown_table(out_dir / "table_tdc_diff_phase_metrics.md", "TDC diff_std / phase_r metrics", metrics, fields)
    bar_svg(out_dir / "fig_tdc_diff_std_ps.svg", metrics, "run", "diff_std_ps", "TDC phase-difference std", color="#31572c")
    bar_svg(out_dir / "fig_tdc_phase_pearson_r.svg", metrics, "run", "phase_pearson_r", "TDC phase Pearson r", color="#6d597a")

    density_rows = []
    for bins_path in sorted(tdc_root.glob("analysis_tdc_*/*.tdc_bins.csv")):
        for row in read_csv(bins_path):
            if row.get("run") in {str(metric["run"]) for metric in metrics}:
                density_rows.append(
                    {
                        "run": row["run"],
                        "lane": row["lane"],
                        "bin": int(f(row, "bin")),
                        "count": int(f(row, "count")),
                        "probability": f(row, "probability"),
                        "width_ps": f(row, "width_ps"),
                        "dnl_lsb": f(row, "dnl_lsb"),
                        "inl_lsb": f(row, "inl_lsb"),
                        "phase_center_ps": f(row, "phase_center_ps"),
                    }
                )
    density_fields = list(density_rows[0].keys()) if density_rows else []
    write_csv(out_dir / "figure_data_tdc_code_density.csv", density_rows, density_fields)

    for run in sorted({row["run"] for row in density_rows}):
        rows = [row for row in density_rows if row["run"] == run]
        by_bin: dict[int, dict[str, object]] = {}
        for row in rows:
            by_bin.setdefault(int(row["bin"]), {"bin": int(row["bin"]), "lane_a_probability": 0.0, "lane_b_probability": 0.0})
            by_bin[int(row["bin"])][f"lane_{row['lane']}_probability"] = row["probability"]
        line_rows = [by_bin[key] for key in sorted(by_bin)]
        line_svg(
            out_dir / f"fig_tdc_code_density_{run}.svg",
            line_rows,
            "bin",
            [("lane_a_probability", "#1d4e89"), ("lane_b_probability", "#a23e48")],
            f"TDC code-density probabilities: {run}",
        )
    return metrics


def write_index(out_dir: Path, trng: list[dict[str, object]], ro_beats: list[dict[str, object]], ro_pull: list[dict[str, object]], tdc: list[dict[str, object]]) -> None:
    lines = [
        "# Fast Mode Offline Figures Index",
        "",
        "Generated from existing CSV analysis files only. No hardware, Vivado, COM, JTAG, or hw_server access is used.",
        "",
        "## Key Outputs",
        "",
        "- `table_trng_formal_fast_metrics.csv/md`: monobit, runs, adjacent, bit/byte min-entropy table.",
        "- `table_trng_repeat_by_placement.csv/md`: formal/repeat placement aggregate table.",
        "- `table_ro_freq_closest_beats.csv/md`: closest all-on data/data beat pairs.",
        "- `table_ro_freq_pulling_summary.csv/md`: all-on vs single-on pulling summary.",
        "- `table_tdc_diff_phase_metrics.csv/md`: TDC diff_std, phase_r, entropy, used-bin metrics.",
        "- `figure_data_tdc_code_density.csv`: code-density rows for TDC figures.",
        "",
        "## Quick Reading",
        "",
    ]
    if trng:
        worst = trng[0]
        best = sorted(trng, key=lambda row: float(row["bit_min_entropy"]), reverse=True)[0]
        lines.append(f"- TRNG bit min-entropy spans `{float(worst['bit_min_entropy']):.6g}` ({worst['placement']}) to `{float(best['bit_min_entropy']):.6g}` ({best['placement']}).")
    if ro_beats:
        for family in sorted({row["family"] for row in ro_beats}):
            first = next(row for row in ro_beats if row["family"] == family)
            lines.append(f"- RO_FREQ closest `{family}` all-on data/data pair is `{first['pair']}` with delta `{float(first['abs_delta_f_mhz']):.6g} MHz`.")
    if ro_pull:
        for row in ro_pull:
            lines.append(f"- RO_FREQ `{row['family']}` sample pulling is `{float(row['sample_shift_ppm']):.6g} ppm`.")
    if tdc:
        for row in tdc:
            lines.append(f"- TDC `{row['run']}` has diff_std `{float(row['diff_std_ps']):.6g} ps` and phase_r `{float(row['phase_pearson_r']):.6g}`.")
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--trng-formal", type=Path, default=DEFAULT_TRNG_FORMAL)
    parser.add_argument("--trng-repeats", type=Path, default=DEFAULT_TRNG_REPEATS)
    parser.add_argument("--ro-freq-dir", type=Path, default=DEFAULT_RO_FREQ)
    parser.add_argument("--tdc-compare", type=Path, default=DEFAULT_TDC_COMPARE)
    parser.add_argument("--tdc-root", type=Path, default=DEFAULT_TDC_ROOT)
    parser.add_argument("--top-n-beats", type=int, default=4)
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    trng, _ = make_trng_tables(args.trng_formal, args.trng_repeats, out_dir)
    ro_beats, ro_pull = make_ro_freq_tables(args.ro_freq_dir, out_dir, args.top_n_beats)
    tdc = make_tdc_tables(args.tdc_compare, args.tdc_root, out_dir)
    write_index(out_dir, trng, ro_beats, ro_pull, tdc)
    print(f"Wrote fast-mode offline outputs to {out_dir}")


if __name__ == "__main__":
    main()
