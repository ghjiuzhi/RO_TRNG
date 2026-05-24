#!/usr/bin/env python3
"""Refresh sampler-ablation summary with the regs-only 2026-05-24 result."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv"
OUT_DIR = ROOT / "data/experiments/sampler_regs_only_20260524"
OUT_CSV = OUT_DIR / "random1_sampler_ablation_extended_summary_20260524.csv"
OUT_MD = OUT_DIR / "random1_sampler_ablation_extended_summary_20260524.md"

REGS_SUMMARY = (
    ROOT
    / "data/hardware/20260511_fpga1_board1/trng/analysis_random1_sampler_regs_only_x45y31_20mib_20260524/trng_summary.csv"
)
REGS_META = ROOT / "data/hardware/20260511_fpga1_board1/metadata/random1_sampler_regs_only_x45y31_20mib_20260524.json"
REGS_SOURCE = ROOT / "data/hardware/20260511_fpga1_board1/trng/random1_sampler_regs_only_x45y31_20mib_20260524.bin"
WINDOW_1M = OUT_DIR / "random1_sampler_regs_only_x45y31_20mib_1mib_windows.csv"
WINDOW_5M = OUT_DIR / "random1_sampler_regs_only_x45y31_20mib_5mib_windows.csv"


FIELDS = [
    "experiment",
    "bitstream_or_source",
    "bytes",
    "p1",
    "bit_min_entropy",
    "runs_p",
    "adjacent_equal_ratio",
    "byte_min_entropy",
    "sample_all_on_freq_mhz",
    "sample_single_on_freq_mhz",
    "sample_shift_mhz",
    "sample_shift_ppm_vs_single",
    "xadc_before_c",
    "xadc_after_c",
    "interpretation",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def metric_range(path: Path, field: str) -> tuple[float, float]:
    values = [float(row[field]) for row in read_csv(path)]
    return min(values), max(values)


def main() -> None:
    rows = read_csv(BASE)
    regs = read_csv(REGS_SUMMARY)[0]
    rows.append(
        {
            "experiment": "random1_sampler_regs_only_x45y31_20mib_programmed",
            "bitstream_or_source": str(REGS_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "bytes": regs["bytes"],
            "p1": regs["p1"],
            "bit_min_entropy": regs["bit_min_entropy"],
            "runs_p": regs["runs_p"],
            "adjacent_equal_ratio": regs["adjacent_equal_ratio"],
            "byte_min_entropy": regs["min_entropy_byte"],
            "sample_all_on_freq_mhz": "",
            "sample_single_on_freq_mhz": "",
            "sample_shift_mhz": "",
            "sample_shift_ppm_vs_single": "",
            "xadc_before_c": "47.4",
            "xadc_after_c": "47.4",
            "interpretation": "programmed 20MiB confirmation; sample RO left baseline while only sampling registers are locally constrained; nearly fixes random1 continuous output",
        }
    )
    write_csv(OUT_CSV, rows)

    p1_1m = metric_range(WINDOW_1M, "p1")
    mh_1m = metric_range(WINDOW_1M, "bit_min_entropy")
    ae_1m = metric_range(WINDOW_1M, "adjacent_equal_ratio")
    p1_5m = metric_range(WINDOW_5M, "p1")
    mh_5m = metric_range(WINDOW_5M, "bit_min_entropy")
    ae_5m = metric_range(WINDOW_5M, "adjacent_equal_ratio")

    lines = [
        "# random1 Sampler-Side Ablation Extended Summary 20260524",
        "",
        "## Main New Result",
        "",
        "`regs-only` keeps the sample RO at the baseline/unconstrained site and moves only the 64 sampling registers to a local island.",
        "The 20MiB programmed confirmation is near ideal:",
        "",
        f"- p1: `{regs['p1']}`",
        f"- bit min-entropy: `{regs['bit_min_entropy']}`",
        f"- adjacent equal ratio: `{regs['adjacent_equal_ratio']}`",
        f"- byte min-entropy: `{regs['min_entropy_byte']}`",
        "- XADC: `47.4 C -> 47.4 C`, `VCCINT=1.000 V`",
        "",
        "This is a strong mechanism result: the sampling-register/routing side alone can nearly remove the random1 continuous-stream bias.",
        "",
        "## Comparison",
        "",
        "| experiment | bytes | p1 | bit min-entropy | adjacent equal | interpretation |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {experiment} | {bytes} | {p1} | {bit_min_entropy} | {adjacent_equal_ratio} | {interpretation} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Window Stability",
            "",
            f"- 1MiB windows p1 range: `{p1_1m[0]:.12f}` to `{p1_1m[1]:.12f}`",
            f"- 1MiB windows bit min-entropy range: `{mh_1m[0]:.12f}` to `{mh_1m[1]:.12f}`",
            f"- 1MiB windows adjacent-equal range: `{ae_1m[0]:.12f}` to `{ae_1m[1]:.12f}`",
            f"- 5MiB windows p1 range: `{p1_5m[0]:.12f}` to `{p1_5m[1]:.12f}`",
            f"- 5MiB windows bit min-entropy range: `{mh_5m[0]:.12f}` to `{mh_5m[1]:.12f}`",
            f"- 5MiB windows adjacent-equal range: `{ae_5m[0]:.12f}` to `{ae_5m[1]:.12f}`",
            "",
            "## Paper Interpretation",
            "",
            "The prior sampler-island result already showed that moving sample RO plus sampling registers fixes random1. The new regs-only result is more discriminating: even with the sample RO left at baseline, constraining the sampling registers/routing island nearly fixes the source.",
            "",
            "Therefore the sampler path is not merely readout logic. The sampling registers and their local routing participate in the physical entropy-source boundary and can dominate the observed placement sensitivity.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
