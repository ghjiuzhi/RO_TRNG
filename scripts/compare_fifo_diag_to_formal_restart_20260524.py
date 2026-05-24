#!/usr/bin/env python3
"""Compare restart FIFO diagnostic matrices with formal restart profiles."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def warmup_from_label(text: str) -> str:
    match = re.search(r"warmup(\d+)", text)
    return match.group(1) if match else ""


def f(value: str) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def classify(delta: float | None) -> str:
    if delta is None:
        return "missing"
    if abs(delta) <= 0.02:
        return "same_direction_close"
    if delta > 0:
        return "fifo_less_biased_than_formal"
    return "fifo_more_biased_than_formal"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fifo-summary",
        type=Path,
        default=Path("data/experiments/restart_fifo_diag_20260524/restart_fifo_diag_matrix_summary_20260524.csv"),
    )
    parser.add_argument(
        "--formal-summary",
        type=Path,
        default=Path("data/experiments/sampler_snapshot_20260524/regs_only_formal_restart_profile_w4_w5_w10_w11_20260524_summary.csv"),
    )
    parser.add_argument("--out-csv", type=Path, default=Path("data/experiments/restart_fifo_diag_20260524/fifo_diag_vs_formal_restart_20260524.csv"))
    parser.add_argument("--out-md", type=Path, default=Path("data/experiments/restart_fifo_diag_20260524/fifo_diag_vs_formal_restart_20260524.md"))
    args = parser.parse_args()

    fifo_rows = read_csv(args.fifo_summary)
    formal_rows = read_csv(args.formal_summary)

    formal_by_warmup: dict[str, dict[str, str]] = {}
    for row in formal_rows:
        warmup = row.get("warmup", "") or warmup_from_label(row.get("label", ""))
        if warmup:
            formal_by_warmup[warmup] = row

    rows: list[dict[str, object]] = []
    for fifo in fifo_rows:
        warmup = fifo.get("warmup", "") or warmup_from_label(fifo.get("label", ""))
        formal = formal_by_warmup.get(warmup, {})
        fifo_p1 = f(fifo.get("overall_p1", ""))
        formal_p1 = f(formal.get("overall_p1", ""))
        fifo_bias = abs(fifo_p1 - 0.5) if fifo_p1 is not None else None
        formal_bias = abs(formal_p1 - 0.5) if formal_p1 is not None else None
        delta = None
        if fifo_bias is not None and formal_bias is not None:
            delta = formal_bias - fifo_bias
        rows.append(
            {
                "warmup": warmup,
                "fifo_label": fifo.get("label", ""),
                "fifo_overall_p1": fifo.get("overall_p1", ""),
                "fifo_abs_bias": f"{fifo_bias:.9f}" if fifo_bias is not None else "",
                "fifo_row_ones_mean": fifo.get("row_ones_mean", ""),
                "fifo_row_ones_std": fifo.get("row_ones_std", ""),
                "fifo_worst_x": fifo.get("worst_x", ""),
                "fifo_worst_p1": fifo.get("worst_p1", ""),
                "formal_label": formal.get("label", ""),
                "formal_overall_p1": formal.get("overall_p1", ""),
                "formal_abs_bias": f"{formal_bias:.9f}" if formal_bias is not None else "",
                "formal_row_ones_std": formal.get("row_ones_std", ""),
                "formal_worst_x": formal.get("worst_x", ""),
                "bias_delta_formal_minus_fifo": f"{delta:.9f}" if delta is not None else "",
                "interpretation": classify(delta),
            }
        )

    fields = [
        "warmup",
        "fifo_label",
        "fifo_overall_p1",
        "fifo_abs_bias",
        "fifo_row_ones_mean",
        "fifo_row_ones_std",
        "fifo_worst_x",
        "fifo_worst_p1",
        "formal_label",
        "formal_overall_p1",
        "formal_abs_bias",
        "formal_row_ones_std",
        "formal_worst_x",
        "bias_delta_formal_minus_fifo",
        "interpretation",
    ]
    write_csv(args.out_csv, rows, fields)

    lines = [
        "# FIFO Diagnostic vs Formal Restart",
        "",
        "This table compares the short `1000 x 32` FIFO send-phase diagnostic with the existing formal restart profile.",
        "",
        "| warmup | fifo p1 | formal p1 | fifo bias | formal bias | formal-fifo bias delta | interpretation |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['warmup']} | {row['fifo_overall_p1']} | {row['formal_overall_p1']} | "
            f"{row['fifo_abs_bias']} | {row['formal_abs_bias']} | {row['bias_delta_formal_minus_fifo']} | {row['interpretation']} |"
        )
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
