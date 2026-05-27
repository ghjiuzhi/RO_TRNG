#!/usr/bin/env python3
"""Join TDC mask-perturb mode metrics with capture hashes and XADC readings."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODE = ROOT / "data" / "experiments" / "tdc_mask_perturb_20260525" / "tdc_mask_perturb_p0_mode_compare_20260525.csv"
DEFAULT_QUEUE = ROOT / "data" / "experiments" / "tdc_mask_perturb_20260525" / "tdc_mask_perturb_queue_summary_20260525.csv"
DEFAULT_XADC = ROOT / "data" / "hardware" / "20260511_fpga1_board1" / "metadata" / "xadc_readings.csv"
DEFAULT_OUT = ROOT / "data" / "experiments" / "tdc_mask_perturb_20260525" / "tdc_mask_perturb_p0_with_xadc_20260525.csv"


FIELDS = [
    "run",
    "family",
    "mode",
    "packets",
    "seq_gaps",
    "entropy_diff",
    "transition_entropy_diff",
    "same_diff_transition_ratio",
    "longest_same_diff_bin_run",
    "autocorr_diff_lag",
    "delta_entropy_diff_vs_pair_only",
    "delta_transition_entropy_diff_vs_pair_only",
    "capture_sha256",
    "bitstream_sha256",
    "xadc_after_timestamp",
    "xadc_after_temperature_c",
    "xadc_after_vccint_v",
    "xadc_after_vccaux_v",
    "xadc_after_vccbram_v",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fp:
        return list(csv.DictReader(fp))


def parse_time(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=Path, default=DEFAULT_MODE)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--xadc", type=Path, default=DEFAULT_XADC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    modes = read_csv(args.mode)
    queues = {row["run"]: row for row in read_csv(args.queue)}
    xadc_rows = read_csv(args.xadc)
    tdc_xadc = [row for row in xadc_rows if row.get("timestamp", "") >= "2026-05-25 19:00:00"]

    # Queue rows and XADC rows are both produced sequentially. Match by order.
    xadc_by_run: dict[str, dict[str, str]] = {}
    queue_order = [row["run"] for row in read_csv(args.queue) if row.get("status") == "completed"]
    for run, xadc in zip(queue_order, tdc_xadc[-len(queue_order):]):
        xadc_by_run[run] = xadc

    out_rows: list[dict[str, Any]] = []
    for row in modes:
        run = row["label"]
        q = queues.get(run, {})
        x = xadc_by_run.get(run, {})
        out_rows.append(
            {
                "run": run,
                "family": row["family"],
                "mode": row["mode"],
                "packets": row["packets"],
                "seq_gaps": row["seq_gaps"],
                "entropy_diff": row["entropy_diff"],
                "transition_entropy_diff": row["transition_entropy_diff"],
                "same_diff_transition_ratio": row["same_diff_transition_ratio"],
                "longest_same_diff_bin_run": row["longest_same_diff_bin_run"],
                "autocorr_diff_lag": row["autocorr_diff_lag"],
                "delta_entropy_diff_vs_pair_only": row["delta_entropy_diff_vs_pair_only"],
                "delta_transition_entropy_diff_vs_pair_only": row["delta_transition_entropy_diff_vs_pair_only"],
                "capture_sha256": q.get("capture_sha256", ""),
                "bitstream_sha256": q.get("bitstream_sha256", ""),
                "xadc_after_timestamp": x.get("timestamp", ""),
                "xadc_after_temperature_c": x.get("TEMPERATURE", ""),
                "xadc_after_vccint_v": x.get("VCCINT", ""),
                "xadc_after_vccaux_v": x.get("VCCAUX", ""),
                "xadc_after_vccbram_v": x.get("VCCBRAM", ""),
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
