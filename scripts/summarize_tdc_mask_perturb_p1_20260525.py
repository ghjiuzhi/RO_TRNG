#!/usr/bin/env python3
"""Summarize TDC mask-perturb P1 against the P0 pair-only baselines."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_P0 = ROOT / "data/experiments/tdc_mask_perturb_20260525/tdc_mask_perturb_p0_mode_compare_20260525.csv"
DEFAULT_P1 = ROOT / "data/experiments/tdc_mask_perturb_p1_20260525/tdc_mask_perturb_p1_20260525.summary.csv"
DEFAULT_QUEUE = ROOT / "data/experiments/tdc_mask_perturb_p1_20260525/tdc_mask_perturb_queue_summary_20260525.csv"
DEFAULT_XADC = ROOT / "data/hardware/20260511_fpga1_board1/metadata/xadc_readings.csv"
DEFAULT_OUT_DIR = ROOT / "data/experiments/tdc_mask_perturb_p1_20260525"


FIELDS = [
    "label",
    "family",
    "mode",
    "baseline_label",
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
    "capture_sha256",
    "bitstream_sha256",
    "xadc_after_temperature_c",
    "xadc_after_vccint_v",
    "interpretation",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fp:
        return list(csv.DictReader(fp))


def f(value: Any) -> float:
    if value == "":
        return 0.0
    return float(value)


def infer_family(label: str) -> str:
    if label.startswith("tdc_mask_random3"):
        return "random3"
    if "local_sample" in label:
        return "random1_local_sample"
    return "random1"


def infer_mode(label: str) -> str:
    if "neighbors_on" in label:
        return "neighbors_on"
    if "all_data_on" in label:
        return "all_data_on"
    if "pair_plus_sample" in label:
        return "pair_plus_sample"
    if "pair_only" in label:
        return "pair_only"
    return "unknown"


def read_p1_warmup0(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(path):
        if str(row["warmup_start"]) != "0":
            continue
        label = row["label"]
        rows.append(
            {
                "label": label,
                "family": infer_family(label),
                "mode": infer_mode(label),
                "packets": int(row["packets"]),
                "seq_gaps": int(row["seq_gaps"]),
                "entropy_diff": f(row["entropy_diff"]),
                "early_entropy_diff": f(row["early_entropy_diff"]),
                "transition_entropy_diff": f(row["transition_entropy_diff"]),
                "same_diff_transition_ratio": f(row["same_diff_transition_ratio"]),
                "longest_same_diff_bin_run": int(row["longest_same_diff_bin_run"]),
                "autocorr_diff_lag": f(row["autocorr_diff_lag"]),
                "first_later_tvd_diff": f(row["first_later_tvd_diff"]),
            }
        )
    return rows


def baseline_map(p0_path: Path, p1_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    p0_rows = read_csv(p0_path)
    out: dict[str, dict[str, Any]] = {}
    for row in p0_rows:
        if row.get("mode") == "pair_only":
            out[row["family"]] = row
    for row in p1_rows:
        if row["mode"] == "pair_only":
            out[row["family"]] = row
    return out


def xadc_by_run(queue_path: Path, xadc_path: Path) -> dict[str, dict[str, str]]:
    queue_rows = [row for row in read_csv(queue_path) if row.get("status") == "completed"]
    if not queue_rows:
        return {}
    xadc_rows = [row for row in read_csv(xadc_path) if row.get("timestamp", "") >= "2026-05-25 21:00:00"]
    matched: dict[str, dict[str, str]] = {}
    for q, x in zip(queue_rows, xadc_rows[-len(queue_rows):]):
        matched[q["run"]] = x
    return matched


def queue_by_run(queue_path: Path) -> dict[str, dict[str, str]]:
    return {row["run"]: row for row in read_csv(queue_path)}


def interpret(row: dict[str, Any]) -> str:
    mode = row["mode"]
    dh = row["delta_entropy_diff_vs_pair_only"]
    dth = row["delta_transition_entropy_diff_vs_pair_only"]
    autocorr = abs(row["autocorr_diff_lag"])
    longest = row["longest_same_diff_bin_run"]
    no_lock = autocorr < 0.01 and longest <= 4
    if mode == "all_data_on" and dh < -0.5 and dth < -1.0 and no_lock:
        return "replicated strong all-data switching effect without hard-lock signature"
    if mode in {"neighbors_on", "pair_plus_sample"} and dh > -0.15 and dth > -0.25 and no_lock:
        return "does not reproduce all-data collapse; points away from this mode as sole cause"
    if mode == "pair_only" and no_lock:
        return "local-sample pair-only baseline remains non-locking"
    return "requires cautious interpretation"


def enrich(rows: list[dict[str, Any]], baselines: dict[str, dict[str, Any]], queue: dict[str, dict[str, str]], xadc: dict[str, dict[str, str]]) -> None:
    for row in rows:
        family = "random1" if row["family"] == "random1_local_sample" else row["family"]
        base = baselines.get(family)
        row["baseline_label"] = base.get("label", "") if base else ""
        if base:
            row["delta_entropy_diff_vs_pair_only"] = row["entropy_diff"] - f(base["entropy_diff"])
            row["delta_transition_entropy_diff_vs_pair_only"] = row["transition_entropy_diff"] - f(base["transition_entropy_diff"])
            row["delta_same_ratio_vs_pair_only"] = row["same_diff_transition_ratio"] - f(base["same_diff_transition_ratio"])
        else:
            row["delta_entropy_diff_vs_pair_only"] = ""
            row["delta_transition_entropy_diff_vs_pair_only"] = ""
            row["delta_same_ratio_vs_pair_only"] = ""
        q = queue.get(row["label"], {})
        x = xadc.get(row["label"], {})
        row["capture_sha256"] = q.get("capture_sha256", "")
        row["bitstream_sha256"] = q.get("bitstream_sha256", "")
        row["xadc_after_temperature_c"] = x.get("TEMPERATURE", "")
        row["xadc_after_vccint_v"] = x.get("VCCINT", "")
        row["interpretation"] = interpret(row)


def fmt(value: Any, digits: int = 6) -> str:
    if value == "":
        return ""
    if isinstance(value, float):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# TDC Mask-Perturb P1 Summary 20260525",
        "",
        "## Mechanism Answer",
        "",
        "P1 directly tests whether the strong `random3 all_data_on` effect from P0 is reproducible, and whether it can be explained by a local neighbor subset or by enabling the sample RO alone.",
        "",
        "The answer is now more specific: the all-data-on collapse is reproducible, while `neighbors_on` and `pair_plus_sample` stay much closer to pair-only. This narrows the mechanism from generic local perturbation to a full data-RO switching/load condition. The effect still does not look like hard locking because autocorrelation remains near zero and the longest same-bin run is only 4.",
        "",
        "## Mode Comparison Against P0 Pair-Only Baseline",
        "",
        "| label | family | mode | H(diff) | dH vs pair | transition H(diff) | dTH vs pair | same ratio | longest run | autocorr | XADC C | interpretation |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["label"],
                    row["family"],
                    row["mode"],
                    fmt(row["entropy_diff"]),
                    fmt(row["delta_entropy_diff_vs_pair_only"]),
                    fmt(row["transition_entropy_diff"]),
                    fmt(row["delta_transition_entropy_diff_vs_pair_only"]),
                    fmt(row["same_diff_transition_ratio"]),
                    str(row["longest_same_diff_bin_run"]),
                    fmt(row["autocorr_diff_lag"]),
                    row.get("xadc_after_temperature_c", ""),
                    row["interpretation"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Paper Use",
            "",
            "- Stronger claim now allowed: the `random3 all_data_on` TDC entropy/transition-entropy collapse replicated in a second 8MiB capture.",
            "- Mechanism narrowed: a neighbor subset and sample-RO-only activation do not reproduce the collapse, so the observed effect is tied to full data-RO simultaneous switching/load rather than a single nearby RO or sample RO alone.",
            "- Boundary remains careful: this is raw-bin relative TDC evidence. It supports local switching/load perturbation and excludes hard locking; it is not absolute ps-level jitter metrology.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p0", type=Path, default=DEFAULT_P0)
    parser.add_argument("--p1", type=Path, default=DEFAULT_P1)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--xadc", type=Path, default=DEFAULT_XADC)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    rows = read_p1_warmup0(args.p1)
    enrich(rows, baseline_map(args.p0, rows), queue_by_run(args.queue), xadc_by_run(args.queue, args.xadc))
    out_csv = args.out_dir / "tdc_mask_perturb_p1_mode_compare_20260525.csv"
    out_md = args.out_dir / "tdc_mask_perturb_p1_mode_compare_20260525.md"
    write_csv(out_csv, rows)
    write_md(out_md, rows)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
