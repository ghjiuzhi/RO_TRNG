#!/usr/bin/env python3
"""Generate paper-facing figures/tables for clean reset-aligned TDC.

Offline only. Reads the clean32k reset-aligned TDC CSV files and writes figure
PNGs/SVGs plus compact CSV/Markdown summaries. No hardware/Vivado/UART access.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN_DIR = ROOT / "data/experiments/tdc_reset_aligned_clean32k_all_20260525"
DEFAULT_OUT_DIR = ROOT / "data/experiments/tdc_clean32k_figures_20260525"


LABEL_ORDER = [
    "random1_baseline_warmup0",
    "random1_baseline_warmup12",
    "random3_goodref_warmup0",
    "random3_goodref_warmup12",
    "random1_sampler_local_warmup0",
    "random1_sampler_local_warmup12",
]

DISPLAY_LABELS = {
    "random1_baseline_warmup0": "R1 base w0",
    "random1_baseline_warmup12": "R1 base w12",
    "random3_goodref_warmup0": "R3 good w0",
    "random3_goodref_warmup12": "R3 good w12",
    "random1_sampler_local_warmup0": "R1 sampler w0",
    "random1_sampler_local_warmup12": "R1 sampler w12",
}

COLORS = {
    "random1_baseline": "#4C78A8",
    "random3_goodref": "#59A14F",
    "random1_sampler_local": "#F28E2B",
}


def parse_label(label: str) -> tuple[str, int]:
    if label.endswith("_warmup0"):
        return label[: -len("_warmup0")], 0
    if label.endswith("_warmup12"):
        return label[: -len("_warmup12")], 12
    return label, -1


def load_inputs(in_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary = pd.read_csv(in_dir / "tdc_reset_aligned_clean32k_all_20260525.summary.csv")
    windows = pd.read_csv(in_dir / "tdc_reset_aligned_clean32k_all_20260525.windows.csv")
    main = summary[summary["warmup_start"].eq(0)].copy()
    main["placement"], main["warmup"] = zip(*main["label"].map(parse_label))
    windows["placement"], windows["warmup"] = zip(*windows["label"].map(parse_label))
    main["label_order"] = main["label"].map({label: i for i, label in enumerate(LABEL_ORDER)})
    main = main.sort_values("label_order")
    return main, windows


def save_fig(fig: plt.Figure, out_dir: Path, stem: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"{stem}.png", dpi=220, bbox_inches="tight")
    fig.savefig(out_dir / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def plot_entropy_bars(main: pd.DataFrame, out_dir: Path) -> None:
    labels = [DISPLAY_LABELS[v] for v in main["label"]]
    x = range(len(main))
    fig, ax = plt.subplots(figsize=(9.5, 4.3))
    width = 0.36
    ax.bar([i - width / 2 for i in x], main["entropy_diff"], width=width, label="H(diff)")
    ax.bar(
        [i + width / 2 for i in x],
        main["early_entropy_diff"],
        width=width,
        label="early H(diff)",
    )
    ax.set_ylabel("raw-bin entropy (bits)")
    ax.set_title("Clean reset-aligned TDC differential-bin entropy")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(6.30, max(main["entropy_diff"].max(), main["early_entropy_diff"].max()) + 0.08)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncols=2)
    save_fig(fig, out_dir, "fig_tdc_clean32k_entropy")


def plot_lock_metrics(main: pd.DataFrame, out_dir: Path) -> None:
    labels = [DISPLAY_LABELS[v] for v in main["label"]]
    x = range(len(main))
    fig, axes = plt.subplots(2, 1, figsize=(9.5, 6.4), sharex=True)
    axes[0].bar(list(x), main["same_diff_transition_ratio"] * 100.0, color="#4C78A8")
    axes[0].set_ylabel("same diff transitions (%)")
    axes[0].set_title("Clean TDC hard-lock indicators remain small")
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].bar(list(x), main["autocorr_diff_lag"], color="#F28E2B")
    axes[1].axhline(0.0, color="black", linewidth=0.8)
    axes[1].set_ylabel("lag-1 autocorr")
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels(labels, rotation=25, ha="right")
    axes[1].grid(axis="y", alpha=0.25)
    save_fig(fig, out_dir, "fig_tdc_clean32k_hard_lock_indicators")


def plot_window_entropy(windows: pd.DataFrame, out_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    for label in LABEL_ORDER:
        group = windows[windows["label"].eq(label)].sort_values("window_index")
        if group.empty:
            continue
        placement, _ = parse_label(label)
        style = "-" if label.endswith("warmup12") else "--"
        ax.plot(
            group["window_index"],
            group["entropy_diff"],
            linestyle=style,
            marker="o",
            markersize=3,
            linewidth=1.5,
            color=COLORS.get(placement, "#555555"),
            label=DISPLAY_LABELS[label],
        )
    ax.set_xlabel("4096-packet window index")
    ax.set_ylabel("H(diff) per window (bits)")
    ax.set_title("Windowed clean TDC phase-diffusion stability")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, ncols=2, fontsize=8)
    save_fig(fig, out_dir, "fig_tdc_clean32k_window_entropy")


def build_tables(main: pd.DataFrame, windows: pd.DataFrame, out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metrics_cols = [
        "label",
        "tdcr_header_found",
        "tdcr_pair_id",
        "tdcr_warmup_packets",
        "tdcr_capture_packets",
        "post_enable_packets",
        "entropy_diff",
        "early_entropy_diff",
        "transition_entropy_diff",
        "same_diff_transition_ratio",
        "longest_same_diff_bin_run",
        "autocorr_diff_lag",
        "first_later_tvd_diff",
    ]
    metrics = main[metrics_cols].copy()
    metrics.to_csv(out_dir / "tdc_clean32k_main_metrics.csv", index=False)

    pivot = main.pivot(index="placement", columns="warmup")
    delta_rows = []
    for placement in sorted(main["placement"].unique()):
        rows = main[main["placement"].eq(placement)].set_index("warmup")
        if 0 not in rows.index or 12 not in rows.index:
            continue
        delta_rows.append(
            {
                "placement": placement,
                "delta_entropy_diff_w12_minus_w0": rows.loc[12, "entropy_diff"] - rows.loc[0, "entropy_diff"],
                "delta_early_entropy_diff_w12_minus_w0": rows.loc[12, "early_entropy_diff"] - rows.loc[0, "early_entropy_diff"],
                "delta_transition_entropy_diff_w12_minus_w0": rows.loc[12, "transition_entropy_diff"] - rows.loc[0, "transition_entropy_diff"],
                "delta_same_ratio_w12_minus_w0": rows.loc[12, "same_diff_transition_ratio"] - rows.loc[0, "same_diff_transition_ratio"],
            }
        )
    del pivot
    deltas = pd.DataFrame(delta_rows)
    deltas.to_csv(out_dir / "tdc_clean32k_warmup_deltas.csv", index=False)

    window_stats = (
        windows.groupby("label", as_index=False)
        .agg(
            entropy_diff_mean=("entropy_diff", "mean"),
            entropy_diff_std=("entropy_diff", "std"),
            transition_entropy_diff_mean=("transition_entropy_diff", "mean"),
            same_diff_transition_ratio_mean=("same_diff_transition_ratio", "mean"),
            autocorr_diff_lag_mean=("autocorr_diff_lag", "mean"),
            diff_std_bin_mean=("diff_std_bin", "mean"),
        )
        .sort_values("label", key=lambda s: s.map({label: i for i, label in enumerate(LABEL_ORDER)}))
    )
    window_stats.to_csv(out_dir / "tdc_clean32k_window_stats.csv", index=False)
    return metrics, deltas, window_stats


def write_markdown(out_dir: Path, metrics: pd.DataFrame, deltas: pd.DataFrame, window_stats: pd.DataFrame) -> None:
    path = out_dir / "tdc_clean32k_figure_summary.md"
    with path.open("w", encoding="utf-8") as f:
        f.write("# Clean Reset-Aligned TDC Figure Summary 20260525\n\n")
        f.write("## Generated Artifacts\n\n")
        for name in [
            "fig_tdc_clean32k_entropy.png",
            "fig_tdc_clean32k_entropy.svg",
            "fig_tdc_clean32k_hard_lock_indicators.png",
            "fig_tdc_clean32k_hard_lock_indicators.svg",
            "fig_tdc_clean32k_window_entropy.png",
            "fig_tdc_clean32k_window_entropy.svg",
            "tdc_clean32k_main_metrics.csv",
            "tdc_clean32k_warmup_deltas.csv",
            "tdc_clean32k_window_stats.csv",
        ]:
            f.write(f"- `{name}`\n")

        f.write("\n## Main Metrics\n\n")
        f.write(metrics.to_markdown(index=False, floatfmt=".6g"))
        f.write("\n\n## Warmup12 - Warmup0 Deltas\n\n")
        f.write(deltas.to_markdown(index=False, floatfmt=".6g"))
        f.write("\n\n## Window Stability\n\n")
        f.write(window_stats.to_markdown(index=False, floatfmt=".6g"))

        f.write("\n\n## Paper Interpretation\n\n")
        f.write(
            "- All six clean captures have `TDCR` headers and 32768 post-enable packets, "
            "so they are defensible reset/header-aligned TDC data.\n"
        )
        f.write(
            "- Same-differential-bin transition ratios stay near 1%, longest same-bin "
            "runs are 3, and lag-1 autocorrelation is near zero; this supports a "
            "negative-control claim against simple pairwise hard locking.\n"
        )
        f.write(
            "- `random1_sampler_local_warmup12` has the strongest clean TDC entropy "
            "numbers in this matrix, but the effect is modest. Treat it as weak "
            "positive mechanism evidence, not as the primary causal proof.\n"
        )
        f.write(
            "- No code-density calibration has been applied; use raw-bin relative "
            "comparisons only, not absolute ps-level jitter claims.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in-dir", type=Path, default=DEFAULT_IN_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    main_df, windows_df = load_inputs(args.in_dir)
    metrics, deltas, window_stats = build_tables(main_df, windows_df, out_dir)
    plot_entropy_bars(main_df, out_dir)
    plot_lock_metrics(main_df, out_dir)
    plot_window_entropy(windows_df, out_dir)
    write_markdown(out_dir, metrics, deltas, window_stats)
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
