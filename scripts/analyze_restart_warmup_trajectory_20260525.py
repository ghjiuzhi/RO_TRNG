#!/usr/bin/env python3
"""Summarize restart hotspot movement across warmup settings.

The input is the packed-byte counterfactual summary. This script groups runs by
design family and warmup count, then reports whether the worst raw byte/bit
hotspot stays in the early startup window or moves/degrades after warmup.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = (
    ROOT
    / "data"
    / "experiments"
    / "restart_packing_counterfactual_20260525"
    / "restart_packing_counterfactual_summary.csv"
)
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "restart_warmup_trajectory_20260525"


def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return float("nan")


def parse_int(value: str) -> int:
    return int(float(value))


def infer_family(label: str) -> str:
    if label.startswith("random3_restart_auto"):
        return "random3_formal"
    if label.startswith("random1_sampler_regs_only"):
        return "random1_sampler_regs_only"
    if label.startswith("restart_auto_random1_regs_only_sample_ro_compact_locked"):
        return "random1_reverse_repair_sample_ro_compact"
    return "other"


def infer_warmup(label: str) -> int:
    m = re.search(r"warmup(\d+)", label)
    if m:
        return int(m.group(1))
    return 0


def classify_hotspot(worst_x: int, worst_byte: int) -> str:
    if worst_x >= 650:
        return "severe"
    if worst_x >= 600:
        return "strong"
    if worst_x >= 570:
        return "moderate"
    if worst_byte < 8:
        return "early_position_weak"
    return "weak"


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = row["label"]
            worst_byte = parse_int(row["worst_byte"])
            worst_bit = parse_int(row["worst_bit_lsb_index"])
            worst_x = parse_int(row["worst_x"])
            rows.append(
                {
                    "label": label,
                    "family": infer_family(label),
                    "warmup": infer_warmup(label),
                    "overall_p1": parse_float(row["overall_p1"]),
                    "worst_byte": worst_byte,
                    "worst_bit_lsb_index": worst_bit,
                    "worst_x": worst_x,
                    "worst_p1": parse_float(row["worst_p1"]),
                    "msb_column": parse_int(row["msb_column"]),
                    "lsb_column": parse_int(row["lsb_column"]),
                    "byte_reverse_msb_column": parse_int(row["byte_reverse_msb_column"]),
                    "row_ones_std": parse_float(row["row_ones_std"]),
                    "hotspot_class": classify_hotspot(worst_x, worst_byte),
                    "early_byte": int(worst_byte < 8),
                }
            )
    return rows


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["family"], row["warmup"])].append(row)

    out: list[dict[str, Any]] = []
    for (family, warmup), items in sorted(groups.items()):
        worst_xs = [r["worst_x"] for r in items]
        worst_bytes = [r["worst_byte"] for r in items]
        p1s = [r["overall_p1"] for r in items]
        early_count = sum(r["early_byte"] for r in items)
        classes = defaultdict(int)
        for r in items:
            classes[r["hotspot_class"]] += 1
        out.append(
            {
                "family": family,
                "warmup": warmup,
                "runs": len(items),
                "mean_overall_p1": mean(p1s),
                "mean_worst_x": mean(worst_xs),
                "max_worst_x": max(worst_xs),
                "mean_worst_byte": mean(worst_bytes),
                "std_worst_byte": pstdev(worst_bytes) if len(worst_bytes) > 1 else 0.0,
                "early_byte_runs": early_count,
                "early_byte_fraction": early_count / len(items),
                "hotspot_classes": ";".join(f"{k}:{classes[k]}" for k in sorted(classes)),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: Any, digits: int = 6) -> str:
    if isinstance(value, float):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def write_markdown(out_dir: Path, rows: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> None:
    lines = [
        "# Restart Warmup Trajectory 20260525",
        "",
        "This is an offline analysis over packed-byte restart summaries. It asks whether warmup reduces fixed-position startup hotspots or merely changes the expanded SP800-90B column number.",
        "",
        "## Warmup Summary",
        "",
        "| family | warmup | runs | mean p1 | mean worst_x | max worst_x | mean worst byte | early-byte runs | class counts |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["family"],
                    str(row["warmup"]),
                    str(row["runs"]),
                    fmt(row["mean_overall_p1"]),
                    fmt(row["mean_worst_x"], 3),
                    str(row["max_worst_x"]),
                    fmt(row["mean_worst_byte"], 2),
                    f"{row['early_byte_runs']}/{row['runs']}",
                    row["hotspot_classes"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Per-Run Hotspots",
            "",
            "| family | warmup | label | worst byte.bit | worst_x | worst_p1 | MSB col | LSB col | class |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=lambda r: (r["family"], r["warmup"], r["label"])):
        lines.append(
            "| "
            + " | ".join(
                [
                    row["family"],
                    str(row["warmup"]),
                    row["label"],
                    f"{row['worst_byte']}.{row['worst_bit_lsb_index']}",
                    str(row["worst_x"]),
                    fmt(row["worst_p1"]),
                    str(row["msb_column"]),
                    str(row["lsb_column"]),
                    row["hotspot_class"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Early-byte severe hotspots support a startup-transient interpretation: restart exposes fixed output positions near the beginning of the stream.",
            "- If warmup reduces `worst_x` and moves hotspots away from early bytes, it supports the claim that warmup lets the sampler/data phase relation diffuse before SP800-90B columns are formed.",
            "- If later warmups remain biased but the hotspot moves, the safer wording is multiple biased fixed positions in a startup/passband structure, not a single immutable bad column.",
            "- These are packed-position statements, not FPGA physical column statements; the packing counterfactual shows expanded column numbers depend on bit order.",
            "",
        ]
    )
    (out_dir / "restart_warmup_trajectory_20260525.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    rows = load_rows(args.input)
    summaries = summarize(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "restart_warmup_trajectory_runs_20260525.csv", rows)
    write_csv(args.out_dir / "restart_warmup_trajectory_summary_20260525.csv", summaries)
    write_markdown(args.out_dir, rows, summaries)
    print(f"Wrote {args.out_dir}")
    print(f"runs={len(rows)} groups={len(summaries)}")


if __name__ == "__main__":
    main()
