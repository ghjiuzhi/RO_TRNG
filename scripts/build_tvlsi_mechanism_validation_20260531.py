#!/usr/bin/env python3
"""Build TVLSI mechanism-validation tables from warmup, PVT, and route evidence."""

from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiments" / "tvlsi_mechanism_validation_20260531"
TVLSI_MODEL = ROOT / "data" / "experiments" / "tvlsi_sampler_aperture_model_20260530"
WARMUP_DIR = ROOT / "data" / "experiments" / "second_heldout_warmup_aperture_sweep_20260530"
SECOND_ROUTE = ROOT / "data" / "experiments" / "second_heldout_sampler_route_diff_20260530" / "second_heldout_per_bitstream_route_audit_20260530.csv"
SECOND_FULL_MAP = ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_second_heldout_sampler_20260530" / "summary" / "second_heldout_reduced_xor_full_map.csv"
PVT_VALIDATION_CANDIDATES = [
    ROOT / "data" / "experiments" / "xadc_summary" / "pvt_xadc_manifest_validation_20260531.csv",
    ROOT / "data" / "experiments" / "xadc_summary" / "pvt_xadc_manifest_validation_20260530.csv",
]
XADC_COMPARE = ROOT / "data" / "experiments" / "xadc_summary" / "board2_bitstream_xadc_compare_20260531.csv"
PREDICTION_METRICS = TVLSI_MODEL / "prediction_metrics_summary.csv"
TOOLFLOW_DIR = ROOT / "data" / "experiments" / "toolflow_sensitivity_matrix_20260531"
TOOLFLOW_MATRIX = TOOLFLOW_DIR / "toolflow_sensitivity_matrix.csv"
TOOLFLOW_CAPTURE = TOOLFLOW_DIR / "toolflow_capture_metrics.csv"
TOOLFLOW_SUMMARY = TOOLFLOW_DIR / "toolflow_sensitivity_summary.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fnum(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def fmt(value: float, digits: int = 9) -> str:
    if math.isnan(value):
        return ""
    return f"{value:.{digits}f}"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def aperture_sweep_model_fit() -> list[dict[str, Any]]:
    rows = [row for row in read_csv(WARMUP_DIR / "second_heldout_warmup_aperture_sweep.csv") if row.get("status") == "ok"]
    by_key: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        by_key.setdefault((row.get("context", ""), row.get("kind", ""), row.get("index", "")), []).append(row)

    transitions = {
        (row.get("context", ""), row.get("kind", ""), row.get("index", "")): row
        for row in read_csv(WARMUP_DIR / "warmup_transition_points.csv")
    }

    out: list[dict[str, Any]] = []
    for key, items in sorted(by_key.items()):
        context, kind, index = key
        by_warmup: dict[int, list[float]] = {}
        for item in items:
            warmup = int(float(item.get("warmup", "0")))
            p1 = fnum(item.get("p1"))
            if not math.isnan(p1):
                by_warmup.setdefault(warmup, []).append(p1)
        if not by_warmup:
            continue
        means = {
            warmup: mean(values)
            for warmup, values in by_warmup.items()
            if values
        }
        ordered = sorted(means)
        adjacent = []
        for left, right in zip(ordered, ordered[1:]):
            adjacent.append((abs(means[right] - means[left]), means[right] - means[left], left, right))
        largest = max(adjacent, default=(math.nan, math.nan, "", ""))
        biases = [means[warmup] - 0.5 for warmup in ordered]
        sign_changes = sum(1 for a, b in zip(biases, biases[1:]) if sign(a) and sign(b) and sign(a) != sign(b))
        abs_biases = {warmup: abs(means[warmup] - 0.5) for warmup in ordered}
        transition = transitions.get(key, {})
        out.append({
            "context": context,
            "kind": kind,
            "index": index,
            "observed_warmups": ",".join(str(warmup) for warmup in ordered),
            "valid_warmup_count": len(ordered),
            "run_count": sum(len(values) for values in by_warmup.values()),
            "p1_min": fmt(min(means.values())),
            "p1_max": fmt(max(means.values())),
            "p1_range": fmt(max(means.values()) - min(means.values())),
            "abs_bias_min": fmt(min(abs_biases.values())),
            "abs_bias_max": fmt(max(abs_biases.values())),
            "largest_adjacent_delta_from_warmup": largest[2],
            "largest_adjacent_delta_to_warmup": largest[3],
            "largest_adjacent_delta_p1": fmt(largest[1]),
            "bias_sign_changes": sign_changes,
            "transition_bracket": transition.get("transition_bracket", ""),
            "mechanism_read": mechanism_read(kind, index, sign_changes, transition.get("transition_bracket", ""), max(abs_biases.values()) - min(abs_biases.values())),
            "source_file": rel(WARMUP_DIR / "second_heldout_warmup_aperture_sweep.csv"),
        })
    return out


def mechanism_read(kind: str, index: str, sign_changes: int, bracket: str, abs_bias_span: float) -> str:
    if kind == "all640" and bracket and "->" in bracket:
        return "aggregate aperture transition observed"
    if sign_changes > 0:
        return "contributor sign reversals across warmup"
    if abs_bias_span > 0.1:
        return "large warmup-dependent bias magnitude shift"
    return "limited warmup variation in current observations"


def route_delay_bias_shift_model() -> list[dict[str, Any]]:
    route_rows = read_csv(SECOND_ROUTE)
    observed = {
        (row.get("kind", ""), row.get("index", "")): row
        for row in read_csv(SECOND_FULL_MAP)
    }
    all_row = observed.get(("all640", "all"), {})
    all_p1 = fnum(all_row.get("p1"))
    out: list[dict[str, Any]] = []
    for route in route_rows:
        kind = route.get("kind") or route.get("mode", "")
        index = route.get("index", "")
        if kind == "all640":
            obs = observed.get(("all640", "all"), {})
        else:
            obs = observed.get((kind, index), {})
        p1 = fnum(obs.get("p1"))
        sample_delay = fnum(route.get("sample_ro_slow_max_mean_ps"))
        data_delay = fnum(route.get("data_ro_slow_max_mean_ps"))
        sampled_delay = fnum(route.get("sampled_data_slow_max_mean_ps"))
        out.append({
            "label": route.get("label", ""),
            "kind": kind,
            "index": index,
            "observed_p1": fmt(p1),
            "observed_abs_bias": fmt(abs(p1 - 0.5)) if not math.isnan(p1) else "",
            "delta_p1_vs_all640": fmt(p1 - all_p1) if not math.isnan(p1) and not math.isnan(all_p1) else "",
            "sample_ro_route_changed_vs_all640": route.get("sample_ro_route_changed_vs_all640", ""),
            "sampled_data_route_changed_vs_all640": route.get("sampled_data_route_changed_vs_all640", ""),
            "data_ro_route_changed_vs_all640": route.get("data_ro_route_changed_vs_all640", ""),
            "sample_ro_slow_max_mean_ps": route.get("sample_ro_slow_max_mean_ps", ""),
            "sampled_data_slow_max_mean_ps": route.get("sampled_data_slow_max_mean_ps", ""),
            "data_ro_slow_max_mean_ps": route.get("data_ro_slow_max_mean_ps", ""),
            "sample_minus_data_delay_mean_ps": fmt(sample_delay - data_delay) if not math.isnan(sample_delay) and not math.isnan(data_delay) else "",
            "sampled_minus_data_delay_mean_ps": fmt(sampled_delay - data_delay) if not math.isnan(sampled_delay) and not math.isnan(data_delay) else "",
            "neighborhood_rows": route.get("neighborhood_rows", ""),
            "model_boundary": "route/audit proxy, not calibrated aperture delay",
            "route_source": rel(SECOND_ROUTE),
            "observed_source": rel(SECOND_FULL_MAP) if obs else "",
        })
    return out


def toolflow_sensitivity_boundary() -> list[dict[str, Any]]:
    rows = read_csv(TOOLFLOW_MATRIX)
    out: list[dict[str, Any]] = []
    for row in rows:
        movement = row.get("movement_class", "")
        delta_abs = fnum(row.get("delta_abs_bias_explore1_minus_original"))
        if movement == "no_route_shift":
            interpretation = "stable extracted route; directive perturbation preserves observed bias"
        elif movement == "sampler_route_shift":
            interpretation = "sampler-route movement; larger bias shift remains implementation-context sensitivity"
        elif movement == "broad_route_shift":
            interpretation = "broad route movement; use as boundary case, not isolated sampler proof"
        else:
            interpretation = "route-pair status is incomplete"
        out.append({
            "context_label": row.get("context_label", ""),
            "anchor": row.get("anchor", ""),
            "original_p1": row.get("original_p1", ""),
            "explore1_p1": row.get("explore1_p1", ""),
            "delta_p1_explore1_minus_original": row.get("delta_p1_explore1_minus_original", ""),
            "delta_abs_bias_explore1_minus_original": fmt(delta_abs),
            "movement_class": movement,
            "sample_ro_route_changed": row.get("sample_ro_route_changed", ""),
            "sampled_data_route_changed": row.get("sampled_data_route_changed", ""),
            "data_ro_route_changed": row.get("data_ro_route_changed", ""),
            "interpretation": interpretation,
            "source_file": rel(TOOLFLOW_MATRIX),
        })
    return out


def classify_xadc_compare_row(row: dict[str, str]) -> str:
    temp = fnum(row.get("TEMPERATURE"))
    vccint = fnum(row.get("VCCINT"))
    vccaux = fnum(row.get("VCCAUX"))
    vccbram = fnum(row.get("VCCBRAM"))
    if any(math.isnan(x) for x in (temp, vccint, vccaux, vccbram)):
        return "invalid_non_numeric"
    if abs(temp + 273.1) < 0.01 or abs(temp + 273.15) < 0.01:
        return "invalid_sentinel_temperature"
    if not (0.8 <= vccint <= 1.2 and 1.5 <= vccaux <= 2.0 and 0.8 <= vccbram <= 1.2):
        return "invalid_voltage_range"
    return "valid"


def mechanism_validation_summary(
    aperture_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    toolflow_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    warmup_rows = [row for row in read_csv(WARMUP_DIR / "second_heldout_warmup_aperture_sweep.csv") if row.get("status") == "ok"]
    warmup_points = sorted({row.get("warmup", "") for row in warmup_rows if row.get("kind") in ("all640", "data_ro") and row.get("index") in ("all", "0", "4")}, key=lambda x: int(float(x)))
    pvt_validation = first_existing(PVT_VALIDATION_CANDIDATES)
    pvt_rows = read_csv(pvt_validation)
    pvt_counts = Counter(row.get("pvt_row_validity", "") for row in pvt_rows)
    xadc_compare_rows = read_csv(XADC_COMPARE)
    xadc_compare_status = Counter(classify_xadc_compare_row(row) for row in xadc_compare_rows)
    pred_rows = read_csv(PREDICTION_METRICS)
    best_sign = max((fnum(row.get("sign_accuracy")) for row in pred_rows), default=math.nan)
    best_class = max((fnum(row.get("class_accuracy")) for row in pred_rows), default=math.nan)
    rank_values = [fnum(row.get("rank_correlation_spearman")) for row in pred_rows if not math.isnan(fnum(row.get("rank_correlation_spearman")))]
    max_rank = max(rank_values) if rank_values else math.nan
    toolflow_capture_rows = read_csv(TOOLFLOW_CAPTURE)
    toolflow_valid = sum(row.get("status") == "ok" for row in toolflow_capture_rows)
    toolflow_pairs = sum(row.get("movement_class", "") != "missing_route" for row in toolflow_rows)
    stable_deltas = [
        abs(fnum(row.get("delta_abs_bias_explore1_minus_original")))
        for row in toolflow_rows
        if row.get("movement_class") == "no_route_shift" and not math.isnan(fnum(row.get("delta_abs_bias_explore1_minus_original")))
    ]
    moving_deltas = [
        abs(fnum(row.get("delta_abs_bias_explore1_minus_original")))
        for row in toolflow_rows
        if row.get("movement_class") != "no_route_shift" and not math.isnan(fnum(row.get("delta_abs_bias_explore1_minus_original")))
    ]
    return [
        {
            "evidence_item": "warmup_aperture_sweep",
            "status": "established",
            "metric": "anchor warmup points",
            "value": len(warmup_points),
            "interpretation": "10-point anchor sweep completed for all640, data_ro0, and data_ro4",
            "source_file": rel(WARMUP_DIR / "second_heldout_warmup_aperture_sweep.csv"),
        },
        {
            "evidence_item": "aggregate_transition",
            "status": "established",
            "metric": "all640 transition bracket",
            "value": next((row.get("transition_bracket", "") for row in aperture_rows if row.get("kind") == "all640"), ""),
            "interpretation": "aggregate p1 shifts from biased at w8 to near-balanced at w9/w10",
            "source_file": rel(WARMUP_DIR / "warmup_transition_points.csv"),
        },
        {
            "evidence_item": "contributor_warmup_sensitivity",
            "status": "established",
            "metric": "data_ro4 sign changes",
            "value": next((row.get("bias_sign_changes", "") for row in aperture_rows if row.get("kind") == "data_ro" and row.get("index") == "4"), ""),
            "interpretation": "data_ro4 reverses signed bias across warmup, supporting startup/aperture sensitivity",
            "source_file": rel(WARMUP_DIR / "warmup_transition_points.csv"),
        },
        {
            "evidence_item": "pvt_manifest",
            "status": "invalid_for_physical_covariate",
            "metric": "PVT row validity",
            "value": ";".join(f"{k}={v}" for k, v in sorted(pvt_counts.items())),
            "interpretation": "PVT rows are parseable but physically invalid and must remain a limitation",
            "source_file": rel(pvt_validation),
        },
        {
            "evidence_item": "board2_bitstream_xadc_compare",
            "status": "invalid_for_physical_covariate",
            "metric": "XADC compare validity",
            "value": ";".join(f"{k}={v}" for k, v in sorted(xadc_compare_status.items())),
            "interpretation": "Board2 remains at sentinel XADC values even after programming a historical Board1 TRNG bitstream",
            "source_file": rel(XADC_COMPARE),
        },
        {
            "evidence_item": "frozen_prediction",
            "status": "mixed",
            "metric": "best sign/class/rank",
            "value": f"sign={fmt(best_sign)}, class={fmt(best_class)}, rank={fmt(max_rank)}",
            "interpretation": "sign/class transfer has signal, but rank correlation remains weak",
            "source_file": rel(PREDICTION_METRICS),
        },
        {
            "evidence_item": "route_delay_bias_proxy",
            "status": "proxy_only",
            "metric": "route rows",
            "value": len(route_rows),
            "interpretation": "route/PIP/net-delay features are available but not calibrated to aperture delay",
            "source_file": rel(SECOND_ROUTE),
        },
        {
            "evidence_item": "toolflow_directive_sensitivity",
            "status": "established_boundary",
            "metric": "valid captures / route pairs / stable-route max shift / route-moving max shift",
            "value": f"{toolflow_valid}/12; pairs={toolflow_pairs}/6; stable_max={fmt(max(stable_deltas, default=math.nan), 6)}; moving_max={fmt(max(moving_deltas, default=math.nan), 6)}",
            "interpretation": "minimal original-vs-Explore matrix preserves bias when extracted routes are stable and bounds larger shifts to route-moving cases",
            "source_file": rel(TOOLFLOW_MATRIX),
        },
    ]


def model_boundary_cases() -> list[dict[str, Any]]:
    return [
        {
            "boundary_case": "Board2 XADC sentinel readout",
            "evidence": rel(XADC_COMPARE),
            "impact": "PVT cannot be used as a covariate or guard for current Board2 captures",
            "handling": "report as limitation; do not discard otherwise valid UART captures",
        },
        {
            "boundary_case": "Weak rank correlation in frozen prediction",
            "evidence": rel(PREDICTION_METRICS),
            "impact": "current route/aperture proxy is not a calibrated contributor-rank predictor",
            "handling": "use sign/class and residuals as limited validation; retain rank failure explicitly",
        },
        {
            "boundary_case": "Anchor-only warmup sweep",
            "evidence": rel(WARMUP_DIR / "second_heldout_warmup_aperture_sweep.csv"),
            "impact": "mechanism transition evidence is strong for selected anchors but not full-map-wide",
            "handling": "claim anchor mechanism evidence only; run full-map sweep only if needed later",
        },
        {
            "boundary_case": "Route/audit proxy not calibrated timing aperture",
            "evidence": rel(SECOND_ROUTE),
            "impact": "route net-delay differences support implementation sensitivity but not physical delay calibration",
            "handling": "call it route/aperture proxy; leave jitter/metastability calibration for future targeted sweeps",
        },
        {
            "boundary_case": "Minimal directive matrix is not a full seed sweep",
            "evidence": rel(TOOLFLOW_MATRIX),
            "impact": "the current matrix answers a targeted reviewer concern but does not characterize all Vivado seeds/directives",
            "handling": "claim stable-route robustness and route-moving boundary only; do not claim complete toolflow invariance",
        },
    ]


def write_report(summary_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# TVLSI Mechanism Validation 20260531",
        "",
        "Generated from existing warmup/aperture captures, Board2 XADC diagnostics, route audit, and frozen-prediction outputs.",
        "",
        "## Summary",
        "",
    ]
    for row in summary_rows:
        lines.append(f"- {row['evidence_item']}: {row['status']} ({row['metric']} = {row['value']}). {row['interpretation']}")
    lines.extend([
        "",
        "## Interpretation Boundary",
        "",
        "The warmup sweep strengthens the startup/aperture mechanism evidence, especially the all640 transition between w8 and w9 and the data_ro4 sign reversals. The toolflow/directive matrix shows that stable-route original-vs-Explore pairs preserve bias within the current measurement scale, while route-moving pairs are treated as implementation-boundary cases. Board2 PVT remains unusable because the same sentinel values appear even after programming a historical Board1 TRNG bitstream.",
        "",
    ])
    (OUT / "tvlsi_mechanism_validation_20260531.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    aperture = aperture_sweep_model_fit()
    route = route_delay_bias_shift_model()
    toolflow = toolflow_sensitivity_boundary()
    summary = mechanism_validation_summary(aperture, route, toolflow)
    boundaries = model_boundary_cases()
    write_csv(OUT / "aperture_sweep_model_fit.csv", aperture, [
        "context", "kind", "index", "observed_warmups", "valid_warmup_count",
        "run_count", "p1_min", "p1_max", "p1_range", "abs_bias_min",
        "abs_bias_max", "largest_adjacent_delta_from_warmup",
        "largest_adjacent_delta_to_warmup", "largest_adjacent_delta_p1",
        "bias_sign_changes", "transition_bracket", "mechanism_read", "source_file",
    ])
    write_csv(OUT / "route_delay_bias_shift_model.csv", route, [
        "label", "kind", "index", "observed_p1", "observed_abs_bias",
        "delta_p1_vs_all640", "sample_ro_route_changed_vs_all640",
        "sampled_data_route_changed_vs_all640", "data_ro_route_changed_vs_all640",
        "sample_ro_slow_max_mean_ps", "sampled_data_slow_max_mean_ps",
        "data_ro_slow_max_mean_ps", "sample_minus_data_delay_mean_ps",
        "sampled_minus_data_delay_mean_ps", "neighborhood_rows",
        "model_boundary", "route_source", "observed_source",
    ])
    write_csv(OUT / "toolflow_sensitivity_mechanism_boundary.csv", toolflow, [
        "context_label", "anchor", "original_p1", "explore1_p1",
        "delta_p1_explore1_minus_original",
        "delta_abs_bias_explore1_minus_original", "movement_class",
        "sample_ro_route_changed", "sampled_data_route_changed",
        "data_ro_route_changed", "interpretation", "source_file",
    ])
    write_csv(OUT / "mechanism_validation_summary.csv", summary, [
        "evidence_item", "status", "metric", "value", "interpretation", "source_file",
    ])
    write_csv(OUT / "model_boundary_cases.csv", boundaries, [
        "boundary_case", "evidence", "impact", "handling",
    ])
    write_report(summary)
    print(f"Wrote mechanism validation outputs to {OUT}")


if __name__ == "__main__":
    main()
