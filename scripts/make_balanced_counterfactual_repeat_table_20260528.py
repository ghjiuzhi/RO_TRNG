#!/usr/bin/env python3
"""Build a balanced sample-RO counterfactual repeat table."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/experiments/sample_ro_balanced_repeats_20260528"


RUNS = [
    (
        "compact baseline",
        "4",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260524/restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.summary.csv",
    ),
    (
        "compact baseline",
        "4",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260528/restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528.summary.csv",
    ),
    (
        "compact baseline",
        "4",
        "run03",
        ROOT
        / "data/experiments/restart_fifo_diag_20260528/restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528.summary.csv",
    ),
    (
        "compact baseline",
        "5",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260524/restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.summary.csv",
    ),
    (
        "compact baseline",
        "5",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260528/restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528.summary.csv",
    ),
    (
        "compact baseline",
        "11",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260524/restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.summary.csv",
    ),
    (
        "compact baseline",
        "11",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260528/restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528.summary.csv",
    ),
    (
        "forward fail",
        "4",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260524/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.summary.csv",
    ),
    (
        "forward fail",
        "4",
        "repeat03-oldbit",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.summary.csv",
    ),
    (
        "forward fail",
        "4",
        "run03",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528.summary.csv",
    ),
    (
        "forward fail",
        "5",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.summary.csv",
    ),
    (
        "forward fail",
        "5",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525.summary.csv",
    ),
    (
        "forward fail",
        "5",
        "run03",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528.summary.csv",
    ),
    (
        "forward fail",
        "11",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.summary.csv",
    ),
    (
        "forward fail",
        "11",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528.summary.csv",
    ),
    (
        "reverse repair",
        "4",
        "run01",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run01_20260525_summary.csv",
    ),
    (
        "reverse repair",
        "4",
        "run02",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run02_20260525_summary.csv",
    ),
    (
        "reverse repair",
        "4",
        "run03",
        ROOT
        / "data/experiments/restart_fifo_diag_20260525/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run03_20260528_summary.csv",
    ),
]


FIELDS = [
    "case",
    "warmup",
    "run_id",
    "overall_p1",
    "abs_bias",
    "overall_min_entropy",
    "row_ones_std",
    "worst_byte_index",
    "worst_bit_index",
    "worst_x",
    "worst_p1",
    "source_file",
]


AGG_FIELDS = [
    "case",
    "warmup",
    "n",
    "p1_mean",
    "p1_std",
    "min_entropy_min",
    "worst_x_max",
    "runs",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"empty CSV: {path}")
    return rows[0]


def min_entropy(p1: float) -> float:
    return -math.log2(max(p1, 1.0 - p1))


def maybe_float(text: str, default: float = float("nan")) -> float:
    try:
        return float(text)
    except (TypeError, ValueError):
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    missing = []
    for case, warmup, run_id, path in RUNS:
        if not path.exists():
            missing.append(path)
            continue
        raw = read_one(path)
        p1 = maybe_float(raw.get("overall_p1"))
        h = raw.get("overall_min_entropy", "")
        if not h and not math.isnan(p1):
            h = f"{min_entropy(p1):.9f}"
        rows.append(
            {
                "case": case,
                "warmup": warmup,
                "run_id": run_id,
                "overall_p1": raw.get("overall_p1", ""),
                "abs_bias": f"{abs(p1 - 0.5):.9f}" if not math.isnan(p1) else "",
                "overall_min_entropy": h,
                "row_ones_std": raw.get("row_ones_std", ""),
                "worst_byte_index": raw.get("worst_byte_index", ""),
                "worst_bit_index": raw.get("worst_bit_index", ""),
                "worst_x": raw.get("worst_x", ""),
                "worst_p1": raw.get("worst_p1", ""),
                "source_file": path.as_posix(),
            }
        )

    csv_path = OUT / "sample_ro_balanced_repeats_20260528.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["case"], row["warmup"]), []).append(row)

    agg_rows = []
    for (case, warmup), items in sorted(grouped.items()):
        p1s = [maybe_float(item["overall_p1"]) for item in items]
        p1s = [p for p in p1s if not math.isnan(p)]
        hs = [maybe_float(item["overall_min_entropy"]) for item in items]
        hs = [h for h in hs if not math.isnan(h)]
        xs = [maybe_float(item["worst_x"]) for item in items]
        xs = [x for x in xs if not math.isnan(x)]
        mean = sum(p1s) / len(p1s) if p1s else float("nan")
        std = math.sqrt(sum((p - mean) ** 2 for p in p1s) / (len(p1s) - 1)) if len(p1s) > 1 else 0.0
        agg_rows.append(
            {
                "case": case,
                "warmup": warmup,
                "n": len(items),
                "p1_mean": f"{mean:.9f}" if p1s else "",
                "p1_std": f"{std:.9f}" if p1s else "",
                "min_entropy_min": f"{min(hs):.9f}" if hs else "",
                "worst_x_max": f"{max(xs):.0f}" if xs else "",
                "runs": ", ".join(item["run_id"] for item in items),
            }
        )

    agg_path = OUT / "sample_ro_balanced_repeats_aggregate_20260528.csv"
    with agg_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AGG_FIELDS)
        writer.writeheader()
        writer.writerows(agg_rows)

    md = [
        "# Sample-RO Balanced Repeats 20260528",
        "",
        f"- run-level CSV: `{csv_path.as_posix()}`",
        f"- aggregate CSV: `{agg_path.as_posix()}`",
        "",
        "## Aggregate",
        "",
        "| case | warmup | n | p1 mean | p1 std | min entropy min | worst x max | runs |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in agg_rows:
        md.append(
            "| {case} | {warmup} | {n} | {p1_mean} | {p1_std} | {min_entropy_min} | {worst_x_max} | {runs} |".format(
                **row
            )
        )
    md.extend(["", "## Missing Inputs", ""])
    if missing:
        md.extend(f"- `{path.as_posix()}`" for path in missing)
    else:
        md.append("- none")

    md_path = OUT / "sample_ro_balanced_repeats_20260528.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {agg_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
