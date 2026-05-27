#!/usr/bin/env python3
"""Summarize TDC mask-perturb P0 mode comparisons."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = ROOT / "data" / "experiments" / "tdc_mask_perturb_20260525" / "tdc_mask_perturb_p0_20260525.summary.csv"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_mask_perturb_20260525"


FIELDS = [
    "label",
    "family",
    "mode",
    "packets",
    "seq_gaps",
    "entropy_diff",
    "early_entropy_diff",
    "transition_entropy_diff",
    "same_diff_transition_ratio",
    "longest_same_diff_bin_run",
    "autocorr_diff_lag",
    "first_later_tvd_diff",
    "delta_entropy_diff_vs_pair_only",
    "delta_transition_entropy_diff_vs_pair_only",
    "delta_same_ratio_vs_pair_only",
]


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def infer_family(label: str) -> str:
    if label.startswith("tdc_mask_random3"):
        return "random3"
    if "local_sample" in label:
        return "random1_local_sample"
    return "random1"


def infer_mode(label: str) -> str:
    if "all_data_on" in label:
        return "all_data_on"
    if "pair_plus_sample" in label:
        return "pair_plus_sample"
    if "pair_only" in label:
        return "pair_only"
    return "unknown"


def read_warmup0(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.DictReader(fp):
            if str(row["warmup_start"]) != "0":
                continue
            label = row["label"]
            out = {
                "label": label,
                "family": infer_family(label),
                "mode": infer_mode(label),
                "packets": int(row["packets"]),
                "seq_gaps": int(row["seq_gaps"]),
                "entropy_diff": f(row, "entropy_diff"),
                "early_entropy_diff": f(row, "early_entropy_diff"),
                "transition_entropy_diff": f(row, "transition_entropy_diff"),
                "same_diff_transition_ratio": f(row, "same_diff_transition_ratio"),
                "longest_same_diff_bin_run": int(row["longest_same_diff_bin_run"]),
                "autocorr_diff_lag": f(row, "autocorr_diff_lag"),
                "first_later_tvd_diff": f(row, "first_later_tvd_diff"),
                "delta_entropy_diff_vs_pair_only": "",
                "delta_transition_entropy_diff_vs_pair_only": "",
                "delta_same_ratio_vs_pair_only": "",
            }
            rows.append(out)
    return rows


def add_deltas(rows: list[dict[str, Any]]) -> None:
    baselines = {
        row["family"]: row
        for row in rows
        if row["mode"] == "pair_only" and row["family"] in {"random1", "random3"}
    }
    for row in rows:
        family = row["family"]
        base = baselines.get(family)
        if base is None:
            continue
        row["delta_entropy_diff_vs_pair_only"] = row["entropy_diff"] - base["entropy_diff"]
        row["delta_transition_entropy_diff_vs_pair_only"] = (
            row["transition_entropy_diff"] - base["transition_entropy_diff"]
        )
        row["delta_same_ratio_vs_pair_only"] = (
            row["same_diff_transition_ratio"] - base["same_diff_transition_ratio"]
        )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: Any, digits: int = 6) -> str:
    if value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# TDC Mask-Perturb P0 Summary 20260525",
        "",
        "## Mode Comparison",
        "",
        "| label | family | mode | packets | seq gaps | H(diff) | transition H(diff) | same ratio | longest run | autocorr | dH vs pair | dTransH vs pair |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["label"],
                    row["family"],
                    row["mode"],
                    str(row["packets"]),
                    str(row["seq_gaps"]),
                    fmt(row["entropy_diff"]),
                    fmt(row["transition_entropy_diff"]),
                    fmt(row["same_diff_transition_ratio"]),
                    str(row["longest_same_diff_bin_run"]),
                    fmt(row["autocorr_diff_lag"]),
                    fmt(row["delta_entropy_diff_vs_pair_only"]),
                    fmt(row["delta_transition_entropy_diff_vs_pair_only"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- All six 8 MiB captures completed and decode to 1,048,575 TDC packets each. The one sequence gap per run is consistent with pre-open capture alignment at stream boundaries.",
            "- Random1 RO0/RO1 changes only mildly across pair-only, all-data-on, and pair-plus-sample modes. This suggests that for this bad-reference pair, local switching perturbation does not create a simple locking signature.",
            "- Random3 RO0/RO6 shows a strong all-data-on effect: H(diff) and transition H(diff) drop substantially relative to pair-only, while lag autocorrelation remains near zero and longest residence is only four packets.",
            "- This supports a mechanism distinction: enabling neighboring RO activity can reshape phase/bin distributions without producing pairwise hard locking.",
            "- The result should be linked with RO_FREQ pulling and restart behavior, but should not be written as absolute ps-level metrology because the TDC LUT is still placement/top dependent.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    rows = read_warmup0(args.summary)
    add_deltas(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "tdc_mask_perturb_p0_mode_compare_20260525.csv", rows)
    write_md(args.out_dir / "tdc_mask_perturb_p0_mode_compare_20260525.md", rows)
    print(f"Wrote {args.out_dir}")


if __name__ == "__main__":
    main()
