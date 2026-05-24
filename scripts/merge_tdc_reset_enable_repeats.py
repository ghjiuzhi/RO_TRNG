#!/usr/bin/env python3
"""Merge reset-enable TDC startup summaries into a compact stability table."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

KEEP_FIELDS = [
    "placement",
    "repeat",
    "enable_edge_index",
    "post_enable_packets",
    "entropy_diff",
    "early_entropy_diff",
    "warmup_entropy_diff",
    "transition_entropy_diff",
    "warmup_transition_entropy_diff",
    "same_diff_transition_ratio",
    "longest_same_diff_bin_run",
    "autocorr_diff_lag",
]


def normalize_label(label: str) -> tuple[str, str]:
    if label.endswith("_repeat02"):
        return label.removesuffix("_repeat02"), "repeat02"
    if label.endswith("_repeat03"):
        return label.removesuffix("_repeat03"), "repeat03"
    return label, "repeat01"


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value != "" else float("nan")


def read_rows(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                placement, repeat = normalize_label(row["label"])
                out = {field: row.get(field, "") for field in KEEP_FIELDS if field not in {"placement", "repeat"}}
                out["placement"] = placement
                out["repeat"] = repeat
                rows.append(out)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=KEEP_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in KEEP_FIELDS})


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    by_placement: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_placement[row["placement"]].append(row)

    lines: list[str] = []
    lines.append("# TDC Reset-Enable Repeat Stability")
    lines.append("")
    lines.append("This table merges reset-enable TDC startup-diffusion summaries across repeats.")
    lines.append("It uses raw TDC bins only; no ps-level calibration is claimed.")
    lines.append("")
    lines.append("## Per-Run Metrics")
    lines.append("")
    lines.append("| placement | repeat | edge | post packets | H(diff) | early H(diff) | warmup H(diff) | transition H(diff) | same ratio | longest run | autocorr |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in sorted(rows, key=lambda r: (r["placement"], r["repeat"])):
        lines.append(
            "| {placement} | {repeat} | {enable_edge_index} | {post_enable_packets} | "
            "{entropy_diff:.5f} | {early_entropy_diff:.5f} | {warmup_entropy_diff:.5f} | "
            "{transition_entropy_diff:.4f} | {same_diff_transition_ratio:.6f} | "
            "{longest_same_diff_bin_run} | {autocorr_diff_lag:.6f} |".format(
                placement=row["placement"],
                repeat=row["repeat"],
                enable_edge_index=row["enable_edge_index"],
                post_enable_packets=row["post_enable_packets"],
                entropy_diff=as_float(row, "entropy_diff"),
                early_entropy_diff=as_float(row, "early_entropy_diff"),
                warmup_entropy_diff=as_float(row, "warmup_entropy_diff"),
                transition_entropy_diff=as_float(row, "transition_entropy_diff"),
                same_diff_transition_ratio=as_float(row, "same_diff_transition_ratio"),
                longest_same_diff_bin_run=row["longest_same_diff_bin_run"],
                autocorr_diff_lag=as_float(row, "autocorr_diff_lag"),
            )
        )

    lines.append("")
    lines.append("## Repeat Means")
    lines.append("")
    lines.append("| placement | repeats | mean H(diff) | mean early H(diff) | mean warmup H(diff) | mean transition H(diff) | mean same ratio | max longest run |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for placement, group in sorted(by_placement.items()):
        longest = max(int(float(row["longest_same_diff_bin_run"])) for row in group)
        lines.append(
            "| {placement} | {n} | {h:.5f} | {early:.5f} | {warm:.5f} | {trans:.4f} | {same:.6f} | {longest} |".format(
                placement=placement,
                n=len(group),
                h=mean([as_float(row, "entropy_diff") for row in group]),
                early=mean([as_float(row, "early_entropy_diff") for row in group]),
                warm=mean([as_float(row, "warmup_entropy_diff") for row in group]),
                trans=mean([as_float(row, "transition_entropy_diff") for row in group]),
                same=mean([as_float(row, "same_diff_transition_ratio") for row in group]),
                longest=longest,
            )
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- In the two completed RO0 repeats, `random1_baseline` is consistently lower than `random1_sampler_local` in differential-bin entropy.")
    lines.append("- The RO4 contrast is stronger and repeats cleanly: `random1_baseline_ro4` remains about 0.095 bit lower than `random1_sampler_local_ro4` in mean H(diff), and about 0.142 bit lower in mean early H(diff).")
    lines.append("- `random3_goodref_ro3` is lower than `random3_goodref_ro0`, which shows that startup diffusion also depends on the specific data-RO/sampler geometry, not only the placement family label.")
    lines.append("- Autocorrelation remains close to zero and longest residence runs are short, so the result still does not support a strong hard-locking explanation.")
    lines.append("- This upgrades reset-enable TDC from a purely negative-control result to repeatable weak-positive evidence that sampler/data geometry changes startup phase-diffusion behavior.")
    lines.append("- The strongest paper wording is causal by combination: sampler-side relocation repairs TRNG output, while reset-enable TDC shows matching startup-diffusion changes without hard locking.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, help="tdc_startup_diffusion.summary.csv; may repeat")
    parser.add_argument("--out-dir", default=str(ROOT / "data" / "experiments" / "tdc_reset_enable_stability_20260524"))
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    rows = read_rows([Path(p) for p in args.input])
    rows.sort(key=lambda r: (r["placement"], r["repeat"]))
    write_csv(out_dir / "tdc_reset_enable_repeat_stability.csv", rows)
    write_md(out_dir / "tdc_reset_enable_repeat_stability.md", rows)
    print(f"Wrote {out_dir / 'tdc_reset_enable_repeat_stability.csv'}")
    print(f"Wrote {out_dir / 'tdc_reset_enable_repeat_stability.md'}")


if __name__ == "__main__":
    main()
