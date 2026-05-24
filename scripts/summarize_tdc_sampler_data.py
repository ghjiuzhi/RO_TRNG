#!/usr/bin/env python3
"""Summarize sampler-data TDC captures for the mechanism study.

This script is offline-only. It reads existing TDC metric CSV files and capture
metadata; it never accesses COM, JTAG, Vivado, or hardware.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METRICS_ROOT = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "tdc_sampler_data"
DEFAULT_METRICS_PATTERN = "analysis_*/*.tdc_metrics.csv"
DEFAULT_METADATA_DIR = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "metadata"
DEFAULT_QUEUE = ROOT / "data" / "experiments" / "fast_mode" / "hardware_queue_tdc_sampler_data_20260523.csv"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "tdc_sampler_data_20260523"
DEFAULT_CSV = DEFAULT_OUT_DIR / "tdc_sampler_data_summary.csv"
DEFAULT_MD = DEFAULT_OUT_DIR / "tdc_sampler_data_summary.md"

FIELDS = [
    "run",
    "placement_family",
    "sampler_variant",
    "data_ro",
    "priority",
    "notes",
    "packets",
    "seq_gaps",
    "lane_a_shannon_bin",
    "lane_a_min_entropy_bin",
    "lane_b_shannon_bin",
    "lane_b_min_entropy_bin",
    "diff_std_ps",
    "bin_pearson_r",
    "phase_pearson_r",
    "coarse_lsb_std",
    "flag_nonzero_ratio",
    "xadc_before_temp_c",
    "xadc_after_temp_c",
    "xadc_before_vccint",
    "xadc_after_vccint",
    "sha256",
    "bytes_captured",
    "source",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def infer_run_fields(run: str) -> dict[str, str]:
    family = "random3" if "random3" in run else "random1" if "random1" in run else ""
    if "_baseline_" in run:
        variant = "baseline"
    elif "_local_" in run:
        variant = "local"
    elif "random3" in run:
        variant = "goodref"
    else:
        variant = ""
    match = re.search(r"_ro(\d+)(?:_|$)", run)
    return {
        "placement_family": family,
        "sampler_variant": variant,
        "data_ro": match.group(1) if match else "",
    }


def load_queue(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv_rows(path)
    return {row.get("run", ""): row for row in rows if row.get("run")}


def metadata_for_run(metadata_dir: Path, run: str) -> dict[str, Any]:
    return read_json(metadata_dir / f"{run}.json")


def pick_xadc(meta: dict[str, Any], phase: str, key: str) -> str:
    block = meta.get(phase)
    if isinstance(block, dict):
        return str(block.get(key, ""))
    return ""


def summarize(metrics_root: Path, metrics_pattern: str, metadata_dir: Path, queue_csv: Path) -> list[dict[str, str]]:
    queue = load_queue(queue_csv)
    rows: list[dict[str, str]] = []
    for path in sorted(metrics_root.glob(metrics_pattern)):
        metric_rows = read_csv_rows(path)
        if not metric_rows:
            continue
        metric = metric_rows[0]
        run = metric.get("run") or path.name.replace(".tdc_metrics.csv", "")
        meta = metadata_for_run(metadata_dir, run)
        q = queue.get(run, {})
        inferred = infer_run_fields(run)
        row = {field: "" for field in FIELDS}
        row.update(inferred)
        row.update(
            {
                "run": run,
                "priority": q.get("priority", ""),
                "notes": q.get("notes", ""),
                "packets": metric.get("packets", ""),
                "seq_gaps": metric.get("seq_gaps", ""),
                "lane_a_shannon_bin": metric.get("lane_a_shannon_bin", ""),
                "lane_a_min_entropy_bin": metric.get("lane_a_min_entropy_bin", ""),
                "lane_b_shannon_bin": metric.get("lane_b_shannon_bin", ""),
                "lane_b_min_entropy_bin": metric.get("lane_b_min_entropy_bin", ""),
                "diff_std_ps": metric.get("diff_std_ps", ""),
                "bin_pearson_r": metric.get("bin_pearson_r", ""),
                "phase_pearson_r": metric.get("phase_pearson_r", ""),
                "coarse_lsb_std": metric.get("coarse_lsb_std", ""),
                "flag_nonzero_ratio": metric.get("flag_nonzero_ratio", ""),
                "xadc_before_temp_c": pick_xadc(meta, "xadc_before", "temperature_c"),
                "xadc_after_temp_c": pick_xadc(meta, "xadc_after", "temperature_c"),
                "xadc_before_vccint": pick_xadc(meta, "xadc_before", "vccint_v"),
                "xadc_after_vccint": pick_xadc(meta, "xadc_after", "vccint_v"),
                "sha256": str(meta.get("sha256", "")),
                "bytes_captured": str(meta.get("bytes_captured", "")),
                "source": metric.get("source", ""),
            }
        )
        rows.append(row)
    return rows


def fnum(text: str) -> float | None:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def fmt(text: str, digits: int = 6) -> str:
    value = fnum(text)
    if value is None:
        return text or "NA"
    return f"{value:.{digits}g}"


def write_outputs(rows: list[dict[str, str]], csv_path: Path, md_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    lines: list[str] = []
    lines.append("# Sampler-Data TDC Summary")
    lines.append("")
    lines.append(f"- completed metric rows: {len(rows)}")
    lines.append("- interpretation scope: raw-bin and relative comparisons only; no calibrated picosecond claims.")
    lines.append("- caution: code-density calibration has not been applied, so `diff_std_ps` is a nominal index-derived value.")
    lines.append("")
    if rows:
        lines.append("| run | family | sampler | data_ro | packets | phase_r | bin_r | diff_std_ps | A Hbin | B Hbin | XADC C |")
        lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
        for row in rows:
            temp = row["xadc_before_temp_c"]
            if row["xadc_after_temp_c"]:
                temp = f"{temp}->{row['xadc_after_temp_c']}"
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{row['run']}`",
                        row["placement_family"],
                        row["sampler_variant"],
                        row["data_ro"],
                        row["packets"],
                        fmt(row["phase_pearson_r"]),
                        fmt(row["bin_pearson_r"]),
                        fmt(row["diff_std_ps"], 7),
                        fmt(row["lane_a_shannon_bin"]),
                        fmt(row["lane_b_shannon_bin"]),
                        temp or "NA",
                    ]
                )
                + " |"
            )
    lines.append("")
    lines.append("## Mechanism Reading")
    lines.append("")
    lines.append(
        "If baseline and local sampler variants have similar near-zero TDC correlation while TRNG entropy differs strongly, "
        "the result should be treated as a negative control against simple pairwise RO locking. "
        "It supports the stronger sampler/register/routing-path hypothesis: the sampler side is part of the entropy source, not just a passive observer."
    )
    lines.append("")
    lines.append(
        "If later rows show a clear baseline/local split in raw-bin entropy, phase correlation, or phase-difference spread, "
        "then TDC can be used as a direct physical mechanism proxy. Otherwise, keep TDC in the main paper as a boundary-setting instrument and put detailed bin tables in supplementary material."
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-root", type=Path, default=DEFAULT_METRICS_ROOT)
    parser.add_argument("--metrics-pattern", default=DEFAULT_METRICS_PATTERN)
    parser.add_argument("--metadata-dir", type=Path, default=DEFAULT_METADATA_DIR)
    parser.add_argument("--queue-csv", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    rows = summarize(args.metrics_root, args.metrics_pattern, args.metadata_dir, args.queue_csv)
    write_outputs(rows, args.csv, args.md)
    print(f"Wrote {args.csv}")
    print(f"Wrote {args.md}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
