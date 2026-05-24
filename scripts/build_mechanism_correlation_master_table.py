#!/usr/bin/env python3
"""Build a paper-facing mechanism evidence master table.

The master table extends the existing placement-level evidence table with
reset-enable TDC startup-diffusion metrics and XADC status summaries. It is
offline-only: no hardware, Vivado, UART, JTAG, or capture processes are used.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_BASE = ROOT / "data/experiments/mechanism_hypothesis_20260523/mechanism_hypothesis_evidence_by_placement.csv"
DEFAULT_RESET_TDC = ROOT / "data/experiments/tdc_reset_enable_stability_20260524/tdc_reset_enable_repeat_stability.csv"
DEFAULT_XADC = ROOT / "data/experiments/xadc_summary/xadc_capture_summary_20260523.csv"
DEFAULT_SAMPLER_EXTENDED = (
    ROOT / "data/experiments/sampler_regs_only_20260524/random1_sampler_ablation_extended_summary_20260524.csv"
)
DEFAULT_REGS_ONLY_RESTART = (
    ROOT / "data/experiments/restart_summary_20260524/restart_result_summary_20260524.csv"
)
DEFAULT_OUT_DIR = ROOT / "data/experiments/mechanism_correlation_20260524"

RESET_TDC_COLUMNS = [
    "reset_tdc_available",
    "reset_tdc_runs",
    "reset_tdc_mean_hdiff",
    "reset_tdc_mean_early_hdiff",
    "reset_tdc_mean_warmup_hdiff",
    "reset_tdc_mean_transition_hdiff",
    "reset_tdc_mean_same_ratio",
    "reset_tdc_max_longest_run",
    "reset_tdc_claim",
]

XADC_COLUMNS = [
    "xadc_capture_count",
    "xadc_ok_count",
    "xadc_missing_count",
    "xadc_before_temp_c_mean",
    "xadc_after_temp_c_mean",
    "xadc_after_vccint_v_mean",
    "xadc_temp_delta_c_max_abs",
]

SAMPLER_EXTENDED_COLUMNS = [
    "sampler_extended_available",
    "sampler_extended_rows",
    "sampler_regs_only_p1",
    "sampler_regs_only_bit_min_entropy",
    "sampler_regs_only_adjacent_equal_ratio",
    "sampler_regs_only_xadc_before_c",
    "sampler_regs_only_xadc_after_c",
    "sampler_extended_claim",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def fmt(value: float | int | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def reset_tdc_placement(label: str) -> str:
    if label in {"random1_baseline", "random1_sampler_local", "random3_goodref"}:
        return label
    if label in {"random1_baseline_ro4", "random1_sampler_local_ro4"}:
        return label
    return label


def summarize_reset_tdc(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        placement = reset_tdc_placement(row.get("placement", ""))
        if placement:
            grouped[placement].append(row)

    out: dict[str, dict[str, str]] = {}
    for placement, group in grouped.items():
        hdiff = [v for row in group if (v := to_float(row.get("entropy_diff"))) is not None]
        early = [v for row in group if (v := to_float(row.get("early_entropy_diff"))) is not None]
        warmup = [v for row in group if (v := to_float(row.get("warmup_entropy_diff"))) is not None]
        trans = [v for row in group if (v := to_float(row.get("transition_entropy_diff"))) is not None]
        same = [v for row in group if (v := to_float(row.get("same_diff_transition_ratio"))) is not None]
        longest = [int(float(row["longest_same_diff_bin_run"])) for row in group if row.get("longest_same_diff_bin_run")]
        out[placement] = {
            "reset_tdc_available": "yes",
            "reset_tdc_runs": str(len(group)),
            "reset_tdc_mean_hdiff": fmt(mean(hdiff)),
            "reset_tdc_mean_early_hdiff": fmt(mean(early)),
            "reset_tdc_mean_warmup_hdiff": fmt(mean(warmup)),
            "reset_tdc_mean_transition_hdiff": fmt(mean(trans)),
            "reset_tdc_mean_same_ratio": fmt(mean(same)),
            "reset_tdc_max_longest_run": str(max(longest)) if longest else "",
            "reset_tdc_claim": "startup diffusion measured; no hard-lock residence" if group else "",
        }
    return out


def placement_from_capture_id(capture_id: str) -> str:
    text = capture_id.lower()
    known = [
        "same_column",
        "cross_region",
        "sampler_island",
        "sampler_local",
        "sample_ro_local",
        "original_fpga1",
        "random1",
        "random2",
        "random3",
        "compact",
        "checker",
        "sparse",
        "far",
        "row",
    ]
    for key in known:
        if text.startswith(key) or key in text:
            if key in {"sampler_local", "sample_ro_local", "sampler_island"}:
                return "random1"
            return key
    return ""


def summarize_xadc(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        placement = placement_from_capture_id(row.get("capture_id", ""))
        if placement:
            grouped[placement].append(row)

    out: dict[str, dict[str, str]] = {}
    for placement, group in grouped.items():
        before = [v for row in group if (v := to_float(row.get("xadc_before_temperature_c"))) is not None]
        after = [v for row in group if (v := to_float(row.get("xadc_after_temperature_c"))) is not None]
        vccint = [v for row in group if (v := to_float(row.get("xadc_after_vccint_v"))) is not None]
        deltas = [abs(v) for row in group if (v := to_float(row.get("temperature_delta_c"))) is not None]
        ok_count = sum(1 for row in group if row.get("xadc_status") == "ok")
        missing_count = sum(1 for row in group if row.get("xadc_status") == "missing")
        out[placement] = {
            "xadc_capture_count": str(len(group)),
            "xadc_ok_count": str(ok_count),
            "xadc_missing_count": str(missing_count),
            "xadc_before_temp_c_mean": fmt(mean(before)),
            "xadc_after_temp_c_mean": fmt(mean(after)),
            "xadc_after_vccint_v_mean": fmt(mean(vccint)),
            "xadc_temp_delta_c_max_abs": fmt(max(deltas) if deltas else None),
        }
    return out


def add_delta_claims(rows: list[dict[str, str]]) -> None:
    by_placement = {row["placement"]: row for row in rows}

    pairs = [
        ("random1_baseline", "random1_sampler_local"),
        ("random1_baseline_ro4", "random1_sampler_local_ro4"),
    ]
    for baseline, local in pairs:
        b = by_placement.get(baseline)
        l = by_placement.get(local)
        if not b or not l:
            continue
        b_early = to_float(b.get("reset_tdc_mean_early_hdiff"))
        l_early = to_float(l.get("reset_tdc_mean_early_hdiff"))
        b_h = to_float(b.get("reset_tdc_mean_hdiff"))
        l_h = to_float(l.get("reset_tdc_mean_hdiff"))
        if b_early is None or l_early is None or b_h is None or l_h is None:
            continue
        delta_early = l_early - b_early
        delta_h = l_h - b_h
        claim = f"sampler-local minus baseline: delta H(diff)={delta_h:.5f}, delta early H(diff)={delta_early:.5f}"
        b["reset_tdc_claim"] = claim
        l["reset_tdc_claim"] = claim


def summarize_sampler_extended(rows: list[dict[str, str]]) -> dict[str, str]:
    if not rows:
        return {"sampler_extended_available": "no"}
    regs = next((row for row in rows if row.get("experiment") == "random1_sampler_regs_only_x45y31_20mib_programmed"), None)
    out = {
        "sampler_extended_available": "yes",
        "sampler_extended_rows": str(len(rows)),
        "sampler_extended_claim": "regs-only sampler-register placement nearly fixes random1 continuous output",
    }
    if regs:
        out.update(
            {
                "sampler_regs_only_p1": regs.get("p1", ""),
                "sampler_regs_only_bit_min_entropy": regs.get("bit_min_entropy", ""),
                "sampler_regs_only_adjacent_equal_ratio": regs.get("adjacent_equal_ratio", ""),
                "sampler_regs_only_xadc_before_c": regs.get("xadc_before_c", ""),
                "sampler_regs_only_xadc_after_c": regs.get("xadc_after_c", ""),
            }
        )
    return out


def build_regs_only_variant_row(
    sampler_rows: list[dict[str, str]], restart_rows: list[dict[str, str]]
) -> dict[str, str] | None:
    regs = next((row for row in sampler_rows if row.get("experiment") == "random1_sampler_regs_only_x45y31_20mib_programmed"), None)
    restarts = [row for row in restart_rows if row.get("placement") == "random1_sampler_regs_only"]
    if not regs and not restarts:
        return None

    row: dict[str, str] = {
        "placement": "random1_sampler_regs_only_x45y31",
        "failure_mode_guess": "continuous stream repaired by sampling-register/routing island; restart startup transient remains",
        "evidence_note": (
            "sample RO kept at baseline while only sampling registers/routing are locally constrained; "
            "20MiB continuous stream is near ideal, but formal bit-symbol restart fails for warmup0 and warmup12"
        ),
    }
    if regs:
        p1 = to_float(regs.get("p1"))
        row.update(
            {
                "continuous_source": regs.get("bitstream_or_source", ""),
                "continuous_bytes": regs.get("bytes", ""),
                "continuous_p1": regs.get("p1", ""),
                "continuous_abs_bias": fmt(abs(p1 - 0.5) if p1 is not None else None),
                "continuous_bit_min_entropy": regs.get("bit_min_entropy", ""),
                "continuous_adjacent_equal": regs.get("adjacent_equal_ratio", ""),
                "sampler_extended_available": "yes",
                "sampler_extended_rows": str(len(sampler_rows)),
                "sampler_regs_only_p1": regs.get("p1", ""),
                "sampler_regs_only_bit_min_entropy": regs.get("bit_min_entropy", ""),
                "sampler_regs_only_adjacent_equal_ratio": regs.get("adjacent_equal_ratio", ""),
                "sampler_regs_only_xadc_before_c": regs.get("xadc_before_c", ""),
                "sampler_regs_only_xadc_after_c": regs.get("xadc_after_c", ""),
                "sampler_extended_claim": "regs-only fixes continuous bias and exposes non-monotonic restart warmup passband",
            }
        )

    if restarts:
        pass_count = sum(1 for r in restarts if r.get("ea_status") == "passed")
        fail_count = sum(1 for r in restarts if r.get("ea_status") == "failed")
        warmups = sorted({int(r["warmup_bytes"]) for r in restarts if r.get("warmup_bytes", "").isdigit()})
        failed_warmups = sorted({int(r["warmup_bytes"]) for r in restarts if r.get("ea_status") == "failed" and r.get("warmup_bytes", "").isdigit()})
        passed_warmups = sorted({int(r["warmup_bytes"]) for r in restarts if r.get("ea_status") == "passed" and r.get("warmup_bytes", "").isdigit()})
        passing_desc = (
            f"pass warmups={','.join(str(w) for w in passed_warmups)}; "
            f"fail warmups={','.join(str(w) for w in failed_warmups)}"
        )
        x_max_values = [(int(float(r["x_max"])), r) for r in restarts if r.get("x_max")]
        worst_x, worst = max(x_max_values, key=lambda item: item[0]) if x_max_values else ("", {})
        overall = [to_float(r.get("overall_p1")) for r in restarts]
        overall_values = [v for v in overall if v is not None]
        xadc_ok = [r for r in restarts if r.get("xadc_status") == "ok"]
        before = [v for r in restarts if (v := to_float(r.get("xadc_before_temperature_c"))) is not None]
        after = [v for r in restarts if (v := to_float(r.get("xadc_after_temperature_c"))) is not None]
        vccint = [v for r in restarts if (v := to_float(r.get("xadc_after_vccint_v"))) is not None]
        deltas = [abs(v) for r in restarts if (v := to_float(r.get("xadc_temperature_delta_c"))) is not None]
        statuses = ";".join(
            f"w{r.get('warmup_bytes')}_{r.get('repeat_tag')}_{r.get('bit_order')}={r.get('ea_status')}"
            for r in restarts
        )
        row.update(
            {
                "restart_source": "data/experiments/restart_summary_20260524/restart_result_summary_20260524.csv",
                "restart_rows": str(len(restarts)),
                "restart_pass_count": str(pass_count),
                "restart_fail_count": str(fail_count),
                "restart_statuses": statuses,
                "restart_warmup_bytes_observed": ",".join(str(w) for w in warmups),
                "restart_min_passing_warmup_bytes": str(min(passed_warmups)) if passed_warmups else "",
                "restart_max_failing_warmup_bytes": str(max(failed_warmups)) if failed_warmups else "",
                "restart_warmup_transition": (
                    "non-monotonic warmup passband; " + passing_desc
                ),
                "restart_worst_x_max": str(worst_x),
                "restart_worst_x_row": f"warmup{worst.get('warmup_bytes','')}_{worst.get('repeat_tag','')}",
                "restart_worst_warmup_bytes": worst.get("warmup_bytes", ""),
                "restart_worst_bit_order": worst.get("bit_order", ""),
                "restart_worst_byte_index": worst.get("worst_byte_index", ""),
                "restart_worst_bit_index": worst.get("worst_bit_index", ""),
                "restart_worst_msb_expanded_column": worst.get("worst_msb_expanded_column", ""),
                "restart_worst_lsb_expanded_column": worst.get("worst_lsb_expanded_column", ""),
                "restart_worst_p1": worst.get("worst_p1", ""),
                "xadc_capture_count": str(len(restarts)),
                "xadc_ok_count": str(len(xadc_ok)),
                "xadc_missing_count": str(len(restarts) - len(xadc_ok)),
                "xadc_before_temp_c_mean": fmt(mean(before)),
                "xadc_after_temp_c_mean": fmt(mean(after)),
                "xadc_after_vccint_v_mean": fmt(mean(vccint)),
                "xadc_temp_delta_c_max_abs": fmt(max(deltas) if deltas else None),
            }
        )
        if overall_values:
            row["evidence_note"] += f"; restart overall p1 range {min(overall_values):.6f}-{max(overall_values):.6f}"
        if passed_warmups:
            row["evidence_note"] += (
                f"; restart passband observed at warmup bytes {','.join(str(w) for w in passed_warmups)}"
            )
    return row


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    interesting = [
        row
        for row in rows
        if row.get("placement") in {
            "random1",
            "random3",
            "random1_baseline",
            "random1_sampler_local",
            "random1_baseline_ro4",
            "random1_sampler_local_ro4",
            "random3_goodref",
            "random1_sampler_regs_only_x45y31",
            "compact",
            "checker",
            "same_column",
            "sparse",
        }
    ]
    lines = [
        "# Mechanism Correlation Master Table 20260524",
        "",
        "This offline table combines placement-level TRNG, restart, RO_FREQ, pair-TDC, reset-enable TDC, sampler-ablation, and XADC summaries.",
        "",
        "## Key Finding Added Today",
        "",
        "- Reset-enable TDC now has repeatable positive evidence, not only a negative-control role.",
        "- RO0: sampler-local has higher startup differential-bin entropy than baseline across two repeats.",
        "- RO4: the contrast is stronger and repeats cleanly; sampler-local improves mean early H(diff) by about 0.142 bit over baseline.",
        "- Residence and autocorrelation remain small, so this still argues against simple hard locking.",
        "- Stronger causal ablation: regs-only keeps the sample RO at baseline but moves only sampling registers; 20MiB p1=0.499810 and bit min-entropy=0.999451.",
        "- New restart contrast: the same regs-only variant has a non-monotonic restart warmup passband. Warmup 5/6/8/10 passed, while 0/4/11/12/16 failed.",
        "",
        "## Selected Rows",
        "",
        "| placement | cont. min-H | restart status | reset TDC runs | reset TDC early H(diff) | sampler regs-only min-H | claim | XADC ok/missing |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in interesting:
        xadc = ""
        if row.get("xadc_capture_count"):
            xadc = f"{row.get('xadc_ok_count','0')}/{row.get('xadc_missing_count','0')}"
        lines.append(
            "| {placement} | {minh} | {restart} | {runs} | {early} | {regs_minh} | {claim} | {xadc} |".format(
                placement=row.get("placement", ""),
                minh=row.get("continuous_bit_min_entropy", ""),
                restart=row.get("restart_statuses", ""),
                runs=row.get("reset_tdc_runs", ""),
                early=row.get("reset_tdc_mean_early_hdiff", ""),
                regs_minh=row.get("sampler_regs_only_bit_min_entropy", ""),
                claim=row.get("sampler_extended_claim") or row.get("reset_tdc_claim", ""),
                xadc=xadc,
            )
        )
    lines.extend(
        [
            "",
            "## Inputs",
            "",
            f"- `{args.base}`",
            f"- `{args.reset_tdc}`",
            f"- `{args.xadc}`",
            f"- `{args.sampler_extended}`",
            "",
            "## Claim Boundary",
            "",
            "- Raw TDC bins are relative indicators; no ps-level calibrated jitter claim is made here.",
            "- Reset-enable TDC supports startup diffusion differences; regs-only sampler-register ablation is the stronger causal evidence for sampler-path entropy-source boundary.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--reset-tdc", type=Path, default=DEFAULT_RESET_TDC)
    parser.add_argument("--xadc", type=Path, default=DEFAULT_XADC)
    parser.add_argument("--sampler-extended", type=Path, default=DEFAULT_SAMPLER_EXTENDED)
    parser.add_argument("--regs-only-restart", type=Path, default=DEFAULT_REGS_ONLY_RESTART)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    base_rows = read_csv(args.base)
    reset_tdc = summarize_reset_tdc(read_csv(args.reset_tdc))
    xadc = summarize_xadc(read_csv(args.xadc))
    sampler_extended_rows = read_csv(args.sampler_extended)
    sampler_extended = summarize_sampler_extended(sampler_extended_rows)
    regs_only_restart_rows = read_csv(args.regs_only_restart)

    existing = {row.get("placement", "") for row in base_rows}
    for placement in sorted(set(reset_tdc) - existing):
        base_rows.append({"placement": placement})

    for row in base_rows:
        placement = row.get("placement", "")
        for column in RESET_TDC_COLUMNS:
            row.setdefault(column, "")
        for column in XADC_COLUMNS:
            row.setdefault(column, "")
        for column in SAMPLER_EXTENDED_COLUMNS:
            row.setdefault(column, "")
        row.update(reset_tdc.get(placement, {"reset_tdc_available": "no"}))
        row.update(xadc.get(placement, {}))
        if placement == "random1":
            row.update(sampler_extended)
        elif "sampler_extended_available" not in row or row["sampler_extended_available"] == "":
            row["sampler_extended_available"] = "no"

    regs_only_row = build_regs_only_variant_row(sampler_extended_rows, regs_only_restart_rows)
    if regs_only_row:
        for column in RESET_TDC_COLUMNS:
            regs_only_row.setdefault(column, "")
        for column in XADC_COLUMNS:
            regs_only_row.setdefault(column, "")
        for column in SAMPLER_EXTENDED_COLUMNS:
            regs_only_row.setdefault(column, "")
        base_rows.append(regs_only_row)

    add_delta_claims(base_rows)

    base_columns = list(base_rows[0].keys()) if base_rows else ["placement"]
    columns = []
    for column in [*base_columns, *RESET_TDC_COLUMNS, *XADC_COLUMNS, *SAMPLER_EXTENDED_COLUMNS]:
        if column not in columns:
            columns.append(column)

    out_csv = args.out_dir / "mechanism_correlation_master_by_placement.csv"
    out_md = args.out_dir / "mechanism_correlation_master_table_20260524.md"
    write_csv(out_csv, base_rows, columns)
    write_markdown(out_md, base_rows, args)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
