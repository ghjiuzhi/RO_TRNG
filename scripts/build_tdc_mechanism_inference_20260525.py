#!/usr/bin/env python3
"""Build paper-facing TDC mechanism inference artifacts for 2026-05-25.

This is an offline analysis script. It reads existing CSV/Markdown artifacts
and writes compact tables that connect TDC observations to RO frequency,
restart, and TRNG evidence. It must not touch Vivado, JTAG, UART, or hardware.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

TDC_MASK = (
    ROOT
    / "data/experiments/tdc_mask_perturb_20260525/"
    / "tdc_mask_perturb_p0_with_xadc_20260525.csv"
)
TDC_MASK_P1 = (
    ROOT
    / "data/experiments/tdc_mask_perturb_p1_20260525/"
    / "tdc_mask_perturb_p1_mode_compare_20260525.csv"
)
TDC_RESET = (
    ROOT
    / "data/experiments/tdc_reset_aligned_clean32k_all_20260525/"
    / "tdc_reset_aligned_clean32k_all_20260525.summary.csv"
)
MECH_MASTER = (
    ROOT
    / "data/experiments/mechanism_correlation_20260524/"
    / "mechanism_correlation_master_by_placement.csv"
)
OUT_DIR = ROOT / "data/experiments/tdc_mechanism_inference_20260525"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(value: str | float | None, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(out):
        return default
    return out


def fmt(value: Any) -> str:
    number = f(value)
    if number is None:
        return ""
    return f"{number:.6g}"


def by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows}


def hard_lock_rejected(row: dict[str, str]) -> bool:
    autocorr = abs(f(row.get("autocorr_diff_lag"), 0.0) or 0.0)
    longest = f(row.get("longest_same_diff_bin_run"), 0.0) or 0.0
    same = f(row.get("same_diff_transition_ratio"), 1.0) or 1.0
    return autocorr < 0.01 and longest <= 4 and same < 0.02


def family_of(row: dict[str, str]) -> str:
    return row.get("family", "") or row.get("placement", "")


def build_mask_rows(mask_rows: list[dict[str, str]], master: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    pair_only_by_family = {
        row["family"]: row
        for row in mask_rows
        if row.get("mode") == "pair_only"
    }
    for row in mask_rows:
        family = family_of(row)
        mode = row.get("mode", "")
        base = pair_only_by_family.get(family)
        m = master.get("random1" if family == "random1_local_sample" else family, {})

        delta_h = f(row.get("delta_entropy_diff_vs_pair_only"))
        delta_th = f(row.get("delta_transition_entropy_diff_vs_pair_only"))
        if base and mode == "pair_only":
            delta_h = 0.0
            delta_th = 0.0

        local_switching = ""
        if mode == "all_data_on" and delta_h is not None and delta_th is not None:
            if delta_h <= -0.3 or delta_th <= -0.6:
                local_switching = "strong TDC distribution reshaping"
            elif abs(delta_h) >= 0.04 or abs(delta_th) >= 0.08:
                local_switching = "weak/moderate TDC distribution reshaping"
            else:
                local_switching = "little TDC response"
        elif mode == "pair_plus_sample":
            if delta_h is None:
                local_switching = "sampler-on comparison without pair-only baseline"
            elif abs(delta_h) >= 0.04 or abs(delta_th or 0.0) >= 0.08:
                local_switching = "sample-RO activity changes TDC weakly"
            else:
                local_switching = "sample-RO activity has little TDC effect"
        else:
            local_switching = "low-activity pair baseline"

        claim = "rules out hard locking"
        if mode == "all_data_on" and local_switching.startswith("strong"):
            claim = "local switching reshapes phase-bin diffusion without hard locking"
        elif mode == "pair_plus_sample" and "weak" in local_switching:
            claim = "sample RO switching perturbs phase-bin diffusion weakly"
        elif family == "random1_local_sample":
            claim = "sampler-local TDC remains non-locking after sampler relocation"

        out.append(
            {
                "experiment_layer": "tdc_mask_perturb",
                "family": family,
                "mode": mode,
                "run": row.get("run", ""),
                "packets": row.get("packets", ""),
                "tdc_entropy_diff": fmt(row.get("entropy_diff")),
                "tdc_transition_entropy_diff": fmt(row.get("transition_entropy_diff")),
                "tdc_delta_entropy_vs_pair_only": fmt(delta_h),
                "tdc_delta_transition_entropy_vs_pair_only": fmt(delta_th),
                "tdc_same_ratio": fmt(row.get("same_diff_transition_ratio")),
                "tdc_longest_run": row.get("longest_same_diff_bin_run", ""),
                "tdc_autocorr": fmt(row.get("autocorr_diff_lag")),
                "hard_lock_signature": "no" if hard_lock_rejected(row) else "possible",
                "local_switching_signature": local_switching,
                "continuous_p1": m.get("continuous_p1", ""),
                "continuous_bit_min_entropy": m.get("continuous_bit_min_entropy", ""),
                "restart_transition": m.get("restart_warmup_transition", ""),
                "restart_pass_count": m.get("restart_pass_count", ""),
                "restart_fail_count": m.get("restart_fail_count", ""),
                "rofreq_sample_shift_ppm": m.get("rofreq_ro_sample_shift_ppm", ""),
                "rofreq_data_max_abs_shift_ppm": m.get("rofreq_ro_data_max_abs_shift_ppm", ""),
                "xadc_after_temperature_c": row.get("xadc_after_temperature_c", ""),
                "xadc_after_vccint_v": row.get("xadc_after_vccint_v", ""),
                "paper_claim": claim,
            }
        )
    return out


def build_mask_p1_rows(p1_rows: list[dict[str, str]], master: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in p1_rows:
        family = family_of(row)
        mode = row.get("mode", "")
        m = master.get("random1" if family == "random1_local_sample" else family, {})
        delta_h = f(row.get("delta_entropy_diff_vs_pair_only"))
        delta_th = f(row.get("delta_transition_entropy_diff_vs_pair_only"))

        claim = "P1 control remains non-locking"
        if mode == "all_data_on" and delta_h is not None and delta_th is not None and delta_h <= -0.5 and delta_th <= -1.0:
            claim = "replicated all-data switching/load reshapes TDC diffusion without hard locking"
        elif mode in {"neighbors_on", "pair_plus_sample"}:
            claim = "neighbor subset or sample-RO-only activation does not reproduce all-data collapse"
        elif family == "random1_local_sample":
            claim = "sampler-local pair-only baseline remains non-locking"

        out.append(
            {
                "experiment_layer": "tdc_mask_perturb_p1",
                "family": family,
                "mode": mode,
                "run": row.get("label", ""),
                "packets": row.get("packets", ""),
                "tdc_entropy_diff": fmt(row.get("entropy_diff")),
                "tdc_transition_entropy_diff": fmt(row.get("transition_entropy_diff")),
                "tdc_delta_entropy_vs_pair_only": fmt(delta_h),
                "tdc_delta_transition_entropy_vs_pair_only": fmt(delta_th),
                "tdc_same_ratio": fmt(row.get("same_diff_transition_ratio")),
                "tdc_longest_run": row.get("longest_same_diff_bin_run", ""),
                "tdc_autocorr": fmt(row.get("autocorr_diff_lag")),
                "hard_lock_signature": "no" if hard_lock_rejected(row) else "possible",
                "local_switching_signature": row.get("interpretation", ""),
                "continuous_p1": m.get("continuous_p1", ""),
                "continuous_bit_min_entropy": m.get("continuous_bit_min_entropy", ""),
                "restart_transition": m.get("restart_warmup_transition", ""),
                "restart_pass_count": m.get("restart_pass_count", ""),
                "restart_fail_count": m.get("restart_fail_count", ""),
                "rofreq_sample_shift_ppm": m.get("rofreq_ro_sample_shift_ppm", ""),
                "rofreq_data_max_abs_shift_ppm": m.get("rofreq_ro_data_max_abs_shift_ppm", ""),
                "xadc_after_temperature_c": row.get("xadc_after_temperature_c", ""),
                "xadc_after_vccint_v": row.get("xadc_after_vccint_v", ""),
                "paper_claim": claim,
            }
        )
    return out


def build_reset_rows(reset_rows: list[dict[str, str]], master: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    selected = [row for row in reset_rows if row.get("warmup_start") == "0"]
    for row in selected:
        label = row.get("label", "")
        family = "random1" if label.startswith("random1_baseline") else "random3" if label.startswith("random3") else "random1_sampler_local"
        m = master.get("random1" if family == "random1_sampler_local" else family, {})
        claim = "startup phase diffusion measured without hard-lock signature"
        if label == "random1_sampler_local_warmup12":
            claim = "sampler-local warmup12 gives the strongest clean reset-aligned diffusion in the six-point matrix"
        out.append(
            {
                "experiment_layer": "reset_aligned_tdc",
                "family": family,
                "mode": label.replace(f"{family}_", ""),
                "run": label,
                "packets": row.get("packets", ""),
                "tdc_entropy_diff": fmt(row.get("entropy_diff")),
                "tdc_transition_entropy_diff": fmt(row.get("transition_entropy_diff")),
                "tdc_delta_entropy_vs_pair_only": "",
                "tdc_delta_transition_entropy_vs_pair_only": "",
                "tdc_same_ratio": fmt(row.get("same_diff_transition_ratio")),
                "tdc_longest_run": row.get("longest_same_diff_bin_run", ""),
                "tdc_autocorr": fmt(row.get("autocorr_diff_lag")),
                "hard_lock_signature": "no" if hard_lock_rejected(row) else "possible",
                "local_switching_signature": "reset/warmup startup diffusion probe",
                "continuous_p1": m.get("continuous_p1", ""),
                "continuous_bit_min_entropy": m.get("continuous_bit_min_entropy", ""),
                "restart_transition": m.get("restart_warmup_transition", ""),
                "restart_pass_count": m.get("restart_pass_count", ""),
                "restart_fail_count": m.get("restart_fail_count", ""),
                "rofreq_sample_shift_ppm": m.get("rofreq_ro_sample_shift_ppm", ""),
                "rofreq_data_max_abs_shift_ppm": m.get("rofreq_ro_data_max_abs_shift_ppm", ""),
                "xadc_after_temperature_c": "",
                "xadc_after_vccint_v": "",
                "paper_claim": claim,
            }
        )
    return out


def build_hypothesis_rows(all_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    no_lock = [r for r in all_rows if r.get("hard_lock_signature") == "no"]
    strong_switch = [
        r
        for r in all_rows
        if str(r.get("local_switching_signature", "")).startswith("strong")
        or str(r.get("paper_claim", "")).startswith("replicated all-data")
    ]
    sampler_positive = [
        r
        for r in all_rows
        if "sampler" in str(r.get("paper_claim", "")).lower()
        or "sample RO" in str(r.get("local_switching_signature", ""))
    ]

    rows.append(
        {
            "hypothesis": "H1: simple RO-RO hard locking is not dominant",
            "status": "supported as exclusion/control evidence",
            "evidence": f"{len(no_lock)}/{len(all_rows)} rows show no hard-lock signature by autocorr/residence/same-ratio thresholds",
            "paper_use": "Write TDC as a falsification layer, not as proof of locking.",
            "next_test": "Only repeat if a future mode produces autocorr/residence anomalies.",
        }
    )
    rows.append(
        {
            "hypothesis": "H2: local switching/load activity can reshape phase-bin diffusion",
            "status": "supported for at least one placement/mode",
            "evidence": "; ".join(
                f"{r['family']} {r['mode']} ΔH={r['tdc_delta_entropy_vs_pair_only']} ΔTH={r['tdc_delta_transition_entropy_vs_pair_only']}"
                for r in strong_switch
            )
            or "No strong mask-perturb response found.",
            "paper_use": "Use as positive TDC evidence that RO-group activity changes delay/phase statistics without hard locking.",
            "next_test": "P1 already replicated all-data-on and checked neighbor/sample-only controls; next best test is RO_FREQ all-on/single-on or cross-board replication.",
        }
    )
    rows.append(
        {
            "hypothesis": "H3: restart startup bias is related to short-time phase diffusion, but not fully explained by pair TDC",
            "status": "partially supported / bounded",
            "evidence": "Reset-aligned TDC has no hard-lock signature; sampler-local warmup12 is best among clean32k rows, while restart still shows warmup passbands and packing-dependent fixed-position bias.",
            "paper_use": "Argue that startup transient exists, but the dominant boundary includes sampler path and bit-position sampling, not only RO pair phase.",
            "next_test": "Run sample-only and sample+regs-local restart passband warmups 4/5/10/11 already built.",
        }
    )
    rows.append(
        {
            "hypothesis": "H4: sampler-side physical implementation is part of the entropy-source boundary",
            "status": "strongly supported by counterfactuals; TDC is a supporting constraint",
            "evidence": f"{len(sampler_positive)} TDC rows are consistent with non-locking sampler-side perturbation; sample-RO forward/reverse restart counterfactuals provide the stronger causal evidence.",
            "paper_use": "Main paper claim: sampling circuit is not a passive readout; it belongs inside the physical entropy-source boundary.",
            "next_test": "Prioritize sampler-only vs regs-only restart/continuous ablation over more same-pair TDC repeats.",
        }
    )
    return rows


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, str]],
    csv_path: Path,
    hypothesis_csv: Path,
) -> None:
    lines: list[str] = []
    lines.append("# TDC 机制推断汇总 2026-05-25")
    lines.append("")
    lines.append("## 结论先行")
    lines.append("")
    lines.append(
        "本表把 TDC mask-perturb、reset-aligned TDC、RO_FREQ、TRNG/restart 结果放在同一条证据链里。"
        "当前最稳的写法不是“坏 placement 来自 RO-RO 锁定”，而是：TDC 多次排除了 hard-lock signature；"
        "同时 mask-perturb 显示局部 RO 开关活动能改变 TDC phase/bin 扩散；再结合 sample-RO 双向反事实，"
        "更合理的机制是 sampler-side physical implementation 参与熵源边界。"
    )
    lines.append("")
    lines.append("## 假设状态")
    lines.append("")
    lines.append("| Hypothesis | Status | Evidence | Paper use | Next test |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in hypothesis_rows:
        lines.append(
            "| {hypothesis} | {status} | {evidence} | {paper_use} | {next_test} |".format(
                **{k: str(v).replace("|", "/") for k, v in row.items()}
            )
        )
    lines.append("")
    lines.append("## 关键 TDC 行")
    lines.append("")
    lines.append(
        "| Layer | Family | Mode | H(diff) | ΔH vs pair | TH(diff) | ΔTH vs pair | "
        "Hard lock? | Switching signature | Paper claim |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |")
    for row in rows:
        if row["experiment_layer"].startswith("tdc_mask_perturb") or row["mode"].endswith("warmup12"):
            lines.append(
                "| {experiment_layer} | {family} | {mode} | {tdc_entropy_diff} | "
                "{tdc_delta_entropy_vs_pair_only} | {tdc_transition_entropy_diff} | "
                "{tdc_delta_transition_entropy_vs_pair_only} | {hard_lock_signature} | "
                "{local_switching_signature} | {paper_claim} |".format(
                    **{k: str(v).replace("|", "/") for k, v in row.items()}
                )
            )
    lines.append("")
    lines.append("## 论文表达边界")
    lines.append("")
    lines.append("- 可以写：TDC evidence rules out simple pairwise RO hard locking as the dominant cause.")
    lines.append("- 可以写：Local switching activity can reshape raw TDC phase/bin diffusion without producing hard-lock signatures.")
    lines.append("- 可以写：The decisive causal evidence for sampler-side boundary comes from sample-RO forward/reverse counterfactuals; TDC constrains the mechanism rather than serving as the sole proof.")
    lines.append("- 不能强写：raw TDC bin 已经给出了绝对 ps 级 jitter 结论；除非后续 code-density calibration 完整接入该实验。")
    lines.append("")
    lines.append("## 输出文件")
    lines.append("")
    lines.append(f"- CSV: `{csv_path.relative_to(ROOT).as_posix()}`")
    lines.append(f"- Hypothesis CSV: `{hypothesis_csv.relative_to(ROOT).as_posix()}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    mask_rows = read_csv(TDC_MASK)
    mask_p1_rows = read_csv(TDC_MASK_P1)
    reset_rows = read_csv(TDC_RESET)
    master = by_key(read_csv(MECH_MASTER), "placement")

    rows = build_mask_rows(mask_rows, master)
    rows.extend(build_mask_p1_rows(mask_p1_rows, master))
    rows.extend(build_reset_rows(reset_rows, master))
    hypothesis_rows = build_hypothesis_rows(rows)

    fieldnames = [
        "experiment_layer",
        "family",
        "mode",
        "run",
        "packets",
        "tdc_entropy_diff",
        "tdc_transition_entropy_diff",
        "tdc_delta_entropy_vs_pair_only",
        "tdc_delta_transition_entropy_vs_pair_only",
        "tdc_same_ratio",
        "tdc_longest_run",
        "tdc_autocorr",
        "hard_lock_signature",
        "local_switching_signature",
        "continuous_p1",
        "continuous_bit_min_entropy",
        "restart_transition",
        "restart_pass_count",
        "restart_fail_count",
        "rofreq_sample_shift_ppm",
        "rofreq_data_max_abs_shift_ppm",
        "xadc_after_temperature_c",
        "xadc_after_vccint_v",
        "paper_claim",
    ]
    hyp_fields = ["hypothesis", "status", "evidence", "paper_use", "next_test"]
    csv_path = OUT_DIR / "tdc_mechanism_inference_20260525.csv"
    hyp_csv_path = OUT_DIR / "tdc_mechanism_hypothesis_status_20260525.csv"
    md_path = OUT_DIR / "tdc_mechanism_inference_20260525.md"

    write_csv(csv_path, rows, fieldnames)
    write_csv(hyp_csv_path, hypothesis_rows, hyp_fields)
    write_markdown(md_path, rows, hypothesis_rows, csv_path, hyp_csv_path)

    print(f"Wrote {csv_path}")
    print(f"Wrote {hyp_csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
