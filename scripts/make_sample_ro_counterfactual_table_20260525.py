#!/usr/bin/env python3
"""Build a paper-facing sample-RO counterfactual table.

This script is offline-only. It reads the 2026-05-25 mechanism evidence chain
and extracts the bidirectional sample-RO counterfactual evidence into a compact
CSV/Markdown table suitable for manuscript drafting.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT
    / "data/experiments/mechanism_evidence_chain_20260525/"
    / "mechanism_evidence_chain_20260525.csv"
)
DEFAULT_OUT = ROOT / "data/experiments/sample_ro_counterfactual_20260525"


FIELDNAMES = [
    "case_id",
    "direction",
    "top_design",
    "sample_ro_implementation",
    "warmup",
    "overall_p1",
    "abs_bias",
    "overall_min_entropy",
    "worst_position",
    "worst_p1",
    "worst_x",
    "xadc_status",
    "interpretation",
    "source_file",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_key_value(metric: str, key: str) -> str:
    for token in metric.replace(",", " ").split():
        if token.startswith(f"{key}="):
            return token.split("=", 1)[1]
    return ""


def parse_warmup(text: str) -> str:
    parts = text.split("_")
    for part in parts:
        if part.startswith("warmup"):
            return part.replace("warmup", "")
        if part.startswith("w") and part[1:].isdigit():
            return part[1:]
    return ""


def classify(row: dict[str, str]) -> dict[str, str] | None:
    if row.get("layer") != "sample RO counterfactual":
        return None

    evidence_id = row.get("evidence_id", "")
    comparison = row.get("comparison", "")
    metric1 = row.get("key_metric_1", "")
    metric2 = row.get("key_metric_2", "")
    metric3 = row.get("key_metric_3", "")
    claim = row.get("claim_supported", "")

    if "forward_fail" in evidence_id:
        direction = "forward fail"
        top_design = "compact FIFO diagnostic"
        sample_ro = "formal-routed sample RO locked"
        interpretation = (
            "Moving only the sample RO from the compact-routed implementation "
            "to the formal-routed implementation pulls an otherwise near-ideal "
            "restart passband into a biased failing regime."
        )
    elif "reverse_repair" in evidence_id:
        direction = "reverse repair"
        top_design = "formal auto restart"
        sample_ro = "compact-routed sample RO locked"
        interpretation = (
            "Moving the sample RO back to the compact-routed implementation "
            "repairs the formal warmup4 restart failure."
        )
    else:
        direction = "sample RO counterfactual"
        top_design = comparison
        sample_ro = comparison
        interpretation = claim

    overall_p1 = parse_key_value(metric1, "overall_p1")
    abs_bias = parse_key_value(metric1, "abs_bias")
    min_entropy = parse_key_value(metric1, "minH")
    worst_p1 = parse_key_value(metric3, "worst_p1")
    row_std = parse_key_value(metric3, "row_std")
    worst_x = parse_key_value(metric2, "x")
    worst_byte = parse_key_value(metric2, "worst_byte")
    if worst_byte:
        bit = parse_key_value(metric2, "bit")
        worst_position = f"byte{worst_byte}.bit{bit}" if bit else f"byte{worst_byte}"
    else:
        worst_position = ""

    if not min_entropy and overall_p1:
        try:
            p = float(overall_p1)
            pmax = max(p, 1.0 - p)
            # Conservative single-bit min-entropy proxy from overall bias.
            import math

            min_entropy = f"{-math.log2(pmax):.9f}"
        except ValueError:
            min_entropy = ""

    case_id = evidence_id
    for prefix in [
        "sample_ro_forward_fail_",
        "sample_ro_reverse_repair_",
    ]:
        if case_id.startswith(prefix):
            case_id = case_id[len(prefix) :]
    case_id = case_id.replace("_20260525.summary", "").replace("_20260525_summary", "")

    if row_std:
        interpretation += f" Row ones std={row_std}."

    return {
        "case_id": case_id,
        "direction": direction,
        "top_design": top_design,
        "sample_ro_implementation": sample_ro,
        "warmup": parse_warmup(evidence_id),
        "overall_p1": overall_p1,
        "abs_bias": abs_bias,
        "overall_min_entropy": min_entropy,
        "worst_position": worst_position,
        "worst_p1": worst_p1,
        "worst_x": worst_x,
        "xadc_status": row.get("xadc_status", ""),
        "interpretation": interpretation,
        "source_file": row.get("source_file", ""),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, str]]) -> str:
    columns = [
        "direction",
        "top_design",
        "sample_ro_implementation",
        "warmup",
        "overall_p1",
        "overall_min_entropy",
        "worst_position",
        "worst_p1",
        "worst_x",
        "xadc_status",
    ]
    lines = []
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row.get(col, "") for col in columns) + " |")
    return "\n".join(lines)


def write_md(path: Path, rows: list[dict[str, str]], csv_path: Path) -> None:
    forward = [r for r in rows if r["direction"] == "forward fail"]
    reverse = [r for r in rows if r["direction"] == "reverse repair"]
    lines = [
        "# Sample-RO Counterfactual Table 20260525",
        "",
        f"- CSV: `{csv_path.as_posix()}`",
        f"- rows: `{len(rows)}`",
        "",
        "## Main Interpretation",
        "",
        (
            "The bidirectional sample-RO counterfactual is currently the "
            "strongest mechanism evidence. In the forward direction, a compact "
            "diagnostic topology becomes biased when only the sample RO is "
            "locked to the formal routed implementation. In the reverse "
            "direction, the formal warmup4 failure is repaired when only the "
            "sample RO is locked to the compact-routed implementation."
        ),
        "",
        "## Paper-Facing Table",
        "",
        md_table(rows),
        "",
        "## Forward Fail Cases",
        "",
    ]
    for row in forward:
        lines.append(
            f"- warmup{row['warmup']}: overall p1={row['overall_p1']}, "
            f"worst={row['worst_position']} x={row['worst_x']} "
            f"p1={row['worst_p1']}"
        )
    lines.extend(["", "## Reverse Repair Cases", ""])
    for row in reverse:
        lines.append(
            f"- warmup{row['warmup']}: overall p1={row['overall_p1']}, "
            f"min-H={row['overall_min_entropy']}, worst={row['worst_position']} "
            f"x={row['worst_x']} p1={row['worst_p1']}"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            (
                "This table supports sampler-side physical realization as part "
                "of the entropy-source boundary. It does not prove that the "
                "sample RO is the only relevant sampler-side element; sampling "
                "registers, local routing, control placement, and aperture "
                "effects remain part of the mechanism boundary."
            ),
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    rows = [classify(row) for row in read_csv(args.input)]
    out_rows = [row for row in rows if row is not None]
    out_rows.sort(key=lambda r: (r["direction"], int(r["warmup"] or 0), r["case_id"]))

    csv_path = args.out_dir / "sample_ro_counterfactual_table_20260525.csv"
    md_path = args.out_dir / "sample_ro_counterfactual_table_20260525.md"
    write_csv(csv_path, out_rows)
    write_md(md_path, out_rows, csv_path)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()

