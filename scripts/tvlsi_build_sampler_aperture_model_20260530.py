#!/usr/bin/env python3
"""Build offline TVLSI sampler-aperture interpretation tables.

This script only reads existing CSV summaries and writes derived offline-model
artifacts. It does not touch hardware, Vivado, or the TIM manuscript tree.
"""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiments" / "tvlsi_sampler_aperture_model_20260530"


INPUTS = {
    "board1_reduced_detail": ROOT / "data" / "experiments" / "restart_reduced_xor_vector_anisotropy_20260528" / "reduced_xor_vector_anisotropy_detail_20260528.csv",
    "board1_reduced_group": ROOT / "data" / "experiments" / "restart_reduced_xor_vector_anisotropy_20260528" / "reduced_xor_vector_anisotropy_group_20260528.csv",
    "board1_repeat_compare": ROOT / "data" / "experiments" / "restart_reduced_xor_w10_direction_repeat02_full_20260528" / "summary" / "w10_direction_repeat02_full_compare_r01.csv",
    "board1_warmup_neighbors": ROOT / "data" / "experiments" / "restart_reduced_xor_ro3_warmup_neighbors_20260528" / "reduced_xor_ro3_warmup_neighbors_20260528.csv",
    "board1_route_summary": ROOT / "data" / "experiments" / "sample_ro_route_diff_20260528" / "sample_ro_route_evidence_summary_20260528.csv",
    "heldout_route_summary": ROOT / "data" / "experiments" / "heldout_sampler_route_diff_20260530" / "sample_ro_route_evidence_summary_20260528.csv",
    "heldout_route_cell_diff": ROOT / "data" / "experiments" / "heldout_sampler_route_diff_20260530" / "orig_w10_sampler_island_vs_heldout_w10_sample_x36y35_cell_diff_20260528.csv",
    "heldout_route_net_diff": ROOT / "data" / "experiments" / "heldout_sampler_route_diff_20260530" / "orig_w10_sampler_island_vs_heldout_w10_sample_x36y35_net_diff_20260528.csv",
    "board1_balanced_repeats": ROOT / "data" / "experiments" / "sample_ro_balanced_repeats_20260528" / "sample_ro_balanced_repeats_aggregate_20260528.csv",
    "board2_restart_summary": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_counterfactual" / "summary" / "board2_restart_counterfactual_summary_20260529.csv",
    "board2_counterfactual_repeats_aggregate": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_counterfactual" / "summary" / "board2_sampler_counterfactual_repeats_aggregate_20260530.csv",
    "board2_heldout_reduced": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_heldout_sampler_20260530" / "summary" / "board2_heldout_sampler_w10_reduced_xor_subset.csv",
    "board2_heldout_full_map": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_heldout_sampler_20260530" / "summary" / "board2_heldout_sampler_w10_reduced_xor_full_map.csv",
    "board2_crossboard_full_map": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_crossboard" / "summary" / "board2_reduced_xor_w5_w10_w11_full_map_mechanism.csv",
    "board2_keypoints_vs_board1": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_crossboard" / "summary" / "board2_reduced_xor_keypoints_vs_board1_r02.csv",
    "board2_counterfactual_w4_w5": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_fifo_counterfactual_crossboard" / "summary" / "board2_counterfactual_w4_w5_summary.csv",
    "route_lock_feasibility": ROOT / "data" / "experiments" / "route_lock_20260528" / "route_lock_feasibility_20260528" / "route_lock_feasibility_20260528.csv",
    "second_heldout_full_map": ROOT / "data" / "hardware" / "20260529_fpga1_board2" / "restart_reduced_xor_second_heldout_sampler_20260530" / "summary" / "second_heldout_reduced_xor_full_map.csv",
    "second_heldout_route_audit": ROOT / "data" / "experiments" / "second_heldout_sampler_route_diff_20260530" / "second_heldout_per_bitstream_route_audit_20260530.csv",
}


OPTIONAL_INPUT_DESCRIPTIONS = {
    "board2_heldout_full_map": "held-out full-map reduced-XOR summary",
    "board2_heldout_reduced": "held-out reduced-XOR subset fallback",
    "board2_crossboard_full_map": "Board2 crossboard reduced-XOR repeat/full-map summary",
    "board2_keypoints_vs_board1": "Board2 keypoints compared with Board1 repeat02",
    "board2_counterfactual_repeats_aggregate": "Board2 restart counterfactual balanced repeat aggregate",
    "board2_counterfactual_w4_w5": "Board2 repeat/counterfactual w4-w5 summary",
    "heldout_route_summary": "held-out route audit summary",
    "heldout_route_cell_diff": "held-out route cell diff",
    "heldout_route_net_diff": "held-out route net diff",
    "route_lock_feasibility": "implementation route-lock feasibility metrics",
    "second_heldout_full_map": "second held-out full-map reduced-XOR summary for frozen prediction",
    "second_heldout_route_audit": "second held-out route audit for frozen prediction route/aperture features",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fnum(value: object, default: float = math.nan) -> float:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def signed_bias(p1: float) -> float:
    return p1 - 0.5


def beta_factor(p1: float) -> float:
    return 1.0 - 2.0 * p1


def min_entropy_from_p1(p1: float) -> float:
    q = max(p1, 1.0 - p1)
    if q <= 0:
        return math.nan
    return -math.log(q, 2)


def xor_p1_independent(p_values: list[float]) -> float:
    prod = 1.0
    for p in p_values:
        prod *= beta_factor(p)
    return (1.0 - prod) / 2.0


def fmt(value: float) -> str:
    if math.isnan(value):
        return ""
    return f"{value:.9f}"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def first_existing(names: list[str]) -> tuple[str, Path] | tuple[str, None]:
    for name in names:
        path = INPUTS[name]
        if path.exists():
            return name, path
    return "", None


def source_status_rows() -> list[dict[str, object]]:
    rows = []
    for name, description in OPTIONAL_INPUT_DESCRIPTIONS.items():
        path = INPUTS[name]
        if name == "second_heldout_full_map":
            resolved = optional_second_heldout_full_map_path()
            rows.append({
                "input_name": name,
                "description": description,
                "status": "present" if resolved else "missing",
                "path": rel(resolved) if resolved else rel(path),
            })
            continue
        if name == "second_heldout_route_audit":
            resolved = optional_second_heldout_route_audit_path()
            rows.append({
                "input_name": name,
                "description": description,
                "status": "present" if resolved else "missing",
                "path": rel(resolved) if resolved else rel(path),
            })
            continue
        rows.append({
            "input_name": name,
            "description": description,
            "status": "present" if path.exists() else "missing",
            "path": rel(path),
        })

    per_bitstream = optional_per_bitstream_route_audit_paths()
    rows.append({
        "input_name": "heldout_per_bitstream_route_audit",
        "description": "held-out per-bitstream route audit",
        "status": "present" if per_bitstream else "missing",
        "path": ";".join(rel(path) for path in per_bitstream),
    })

    impl_metrics = optional_implementation_metric_paths()
    rows.append({
        "input_name": "implementation_metrics_generic",
        "description": "resource/timing/power implementation metrics",
        "status": "present" if impl_metrics else "missing",
        "path": ";".join(rel(path) for path in impl_metrics[:8]),
    })
    return rows


def optional_per_bitstream_route_audit_paths() -> list[Path]:
    paths = sorted(
        set(
            (ROOT / "data" / "experiments").glob("**/*per*bitstream*route*audit*.csv")
        )
        | set(
            (ROOT / "data" / "experiments").glob("**/*route*audit*per*bitstream*.csv")
        )
    )
    return prefer_source_over_output_copy(paths)


def optional_implementation_metric_paths() -> list[Path]:
    paths = sorted(
        path for path in (ROOT / "data").glob("**/*.csv")
        if re.search(r"(implementation|impl|resource|utilization|timing|power).*metric", path.name, re.I)
    )
    return prefer_source_over_output_copy(paths)


def optional_second_heldout_full_map_path() -> Path | None:
    if INPUTS["second_heldout_full_map"].exists():
        return INPUTS["second_heldout_full_map"]
    candidates = sorted(
        path for path in (ROOT / "data").glob("**/*.csv")
        if OUT not in path.parents
        and "second" in path.name.lower()
        and "heldout" in path.name.lower()
        and "full" in path.name.lower()
        and "map" in path.name.lower()
    )
    return candidates[0] if candidates else None


def optional_second_heldout_route_audit_path() -> Path | None:
    if INPUTS["second_heldout_route_audit"].exists():
        return INPUTS["second_heldout_route_audit"]
    candidates = sorted(
        path for path in (ROOT / "data").glob("**/*.csv")
        if OUT not in path.parents
        and "second" in path.name.lower()
        and "heldout" in path.name.lower()
        and "route" in path.name.lower()
        and ("audit" in path.name.lower() or "diff" in path.name.lower())
    )
    return candidates[0] if candidates else None


def prefer_source_over_output_copy(paths: list[Path]) -> list[Path]:
    """Avoid reading generated TVLSI output copies when a source copy exists."""
    if not paths:
        return []
    by_name: dict[str, list[Path]] = {}
    for path in paths:
        by_name.setdefault(path.name, []).append(path)
    selected = []
    for name in sorted(by_name):
        candidates = sorted(by_name[name])
        non_output = [path for path in candidates if OUT not in path.parents]
        selected.append(non_output[0] if non_output else candidates[0])
    return selected


def contributor_dataset() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for row in read_csv(INPUTS["board1_reduced_detail"]):
        p1 = fnum(row.get("p1"))
        rows.append({
            "board": "z7020_b01",
            "context": "board1_w10_direction_map",
            "implementation": row.get("source", ""),
            "warmup": row.get("warmup", ""),
            "kind": row.get("group", ""),
            "index": row.get("index", ""),
            "p1": fmt(p1),
            "signed_bias": fmt(signed_bias(p1)),
            "abs_bias": row.get("abs_bias", ""),
            "beta_factor": fmt(beta_factor(p1)),
            "min_entropy": row.get("min_entropy", ""),
            "worst_x": row.get("worst_x", ""),
            "worst_p1": row.get("worst_p1", ""),
            "source_file": rel(INPUTS["board1_reduced_detail"]),
        })

    heldout_name, heldout_path = first_existing(["board2_heldout_full_map", "board2_heldout_reduced"])
    for row in read_csv(heldout_path) if heldout_path else []:
        p1 = fnum(row.get("p1"))
        rows.append({
            "board": row.get("board", "z7020_b02"),
            "context": row.get("context", "heldout_sampler"),
            "implementation": "board2_heldout_sampler_w10",
            "warmup": row.get("warmup", ""),
            "kind": row.get("kind", ""),
            "index": row.get("index", ""),
            "p1": fmt(p1),
            "signed_bias": fmt(signed_bias(p1)),
            "abs_bias": row.get("abs_bias", ""),
            "beta_factor": fmt(beta_factor(p1)),
            "min_entropy": row.get("min_entropy", ""),
            "worst_x": row.get("worst_x", ""),
            "worst_p1": row.get("worst_p1", ""),
            "source_file": rel(heldout_path),
        })

    second_heldout_path = optional_second_heldout_full_map_path()
    for row in read_csv(second_heldout_path) if second_heldout_path else []:
        p1 = fnum(row.get("p1"))
        rows.append({
            "board": row.get("board", "z7020_b02"),
            "context": row.get("context", "second_heldout_sampler"),
            "implementation": row.get("implementation", "board2_second_heldout_sampler"),
            "warmup": row.get("warmup", ""),
            "kind": row.get("kind", ""),
            "index": row.get("index", ""),
            "p1": fmt(p1),
            "signed_bias": fmt(signed_bias(p1)),
            "abs_bias": row.get("abs_bias", fmt(abs(p1 - 0.5))),
            "beta_factor": fmt(beta_factor(p1)),
            "min_entropy": row.get("min_entropy", fmt(min_entropy_from_p1(p1))),
            "worst_x": row.get("worst_x", ""),
            "worst_p1": row.get("worst_p1", ""),
            "source_file": rel(second_heldout_path),
        })

    for row in read_csv(INPUTS["board2_crossboard_full_map"]):
        p1 = fnum(row.get("p1"))
        rows.append({
            "board": row.get("board", "z7020_b02"),
            "context": "board2_crossboard_full_map",
            "implementation": row.get("profile_label", "board2_crossboard"),
            "warmup": row.get("warmup", ""),
            "kind": row.get("kind", ""),
            "index": row.get("index", ""),
            "p1": fmt(p1),
            "signed_bias": fmt(signed_bias(p1)),
            "abs_bias": row.get("abs_bias", ""),
            "beta_factor": fmt(beta_factor(p1)),
            "min_entropy": row.get("min_entropy", ""),
            "worst_x": row.get("worst_x", ""),
            "worst_p1": row.get("worst_p1", ""),
            "source_file": rel(INPUTS["board2_crossboard_full_map"]),
        })

    return rows


def xor_cancellation_model(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = {}
    for row in rows:
        if row["kind"] == "data_ro":
            key = (str(row["board"]), str(row["context"]), str(row["warmup"]))
            groups.setdefault(key, []).append(row)

    for key, contributors in sorted(groups.items()):
        p_values = [fnum(row["p1"]) for row in contributors]
        data_indices = ",".join(str(row["index"]) for row in contributors)
        pred = xor_p1_independent(p_values)
        measured_candidates = [
            row for row in rows
            if (str(row["board"]), str(row["context"]), str(row["warmup"])) == key
            and str(row["kind"]).startswith("all")
        ]
        measured = fnum(measured_candidates[0]["p1"]) if measured_candidates else math.nan
        out.append({
            "board": key[0],
            "context": key[1],
            "warmup": key[2],
            "contributor_count": len(contributors),
            "contributor_indices": data_indices,
            "independent_xor_p1_pred": fmt(pred),
            "measured_all_p1": fmt(measured),
            "residual_measured_minus_pred": fmt(measured - pred) if not math.isnan(measured) else "",
            "pred_abs_bias": fmt(abs(pred - 0.5)),
            "measured_abs_bias": fmt(abs(measured - 0.5)) if not math.isnan(measured) else "",
            "interpretation": "independence approximation; residual indicates correlation/startup structure/unmodeled aperture effects",
        })

    return out


def repeat_stability_summary() -> list[dict[str, object]]:
    rows = read_csv(INPUTS["board1_repeat_compare"])
    out = []
    for mode in sorted(set(row["mode"] for row in rows)):
        sub = [row for row in rows if row["mode"] == mode]
        same = sum(1 for row in sub if row.get("same_bias_sign", "").lower() == "true")
        abs_deltas = [fnum(row["abs_delta_p1"]) for row in sub]
        p1_1 = [fnum(row["p1_run01"]) for row in sub]
        p1_2 = [fnum(row["p1_run02"]) for row in sub]
        corr = pearson(p1_1, p1_2)
        out.append({
            "board": "z7020_b01",
            "context": "w10_direction_repeat02",
            "mode": mode,
            "n": len(sub),
            "same_bias_sign_count": same,
            "same_bias_sign_fraction": fmt(same / len(sub)) if sub else "",
            "mean_abs_delta_p1": fmt(sum(abs_deltas) / len(abs_deltas)) if abs_deltas else "",
            "max_abs_delta_p1": fmt(max(abs_deltas)) if abs_deltas else "",
            "pearson_p1_run01_run02": fmt(corr),
            "source_file": rel(INPUTS["board1_repeat_compare"]),
        })

    for row in read_csv(INPUTS["board2_keypoints_vs_board1"]):
        kind = row.get("kind", "")
        out.append({
            "board": "z7020_b02",
            "context": "keypoints_vs_board1_repeat02",
            "mode": kind,
            "n": 1,
            "same_bias_sign_count": int((fnum(row.get("board1_r02_p1")) - 0.5) * (fnum(row.get("board2_p1")) - 0.5) > 0) if row.get("board1_r02_p1") else "",
            "same_bias_sign_fraction": "",
            "mean_abs_delta_p1": row.get("delta_p1", ""),
            "max_abs_delta_p1": row.get("delta_p1", ""),
            "pearson_p1_run01_run02": "",
            "source_file": rel(INPUTS["board2_keypoints_vs_board1"]),
        })

    return out


def pearson(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or len(a) < 2:
        return math.nan
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    if da == 0 or db == 0:
        return math.nan
    return num / (da * db)


def warmup_neighbor_summary() -> list[dict[str, object]]:
    out = []
    for row in read_csv(INPUTS["board1_warmup_neighbors"]):
        p1 = fnum(row.get("p1"))
        out.append({
            "board": "z7020_b01",
            "context": "ro3_warmup_neighbors",
            "mode": row.get("mode", ""),
            "data_ro": row.get("data_ro", ""),
            "warmup": row.get("warmup", ""),
            "p1": fmt(p1),
            "signed_bias": fmt(signed_bias(p1)),
            "abs_bias": row.get("abs_bias", ""),
            "min_entropy": row.get("min_entropy", ""),
            "worst_x": row.get("worst_x", ""),
            "worst_p1": row.get("worst_p1", ""),
            "source_file": rel(INPUTS["board1_warmup_neighbors"]),
        })
    return out


def route_feature_summary() -> list[dict[str, object]]:
    out = []
    for row in read_csv(INPUTS["board1_route_summary"]):
        sample_pips = fnum(row.get("sample_ro_pips"))
        data_pips = fnum(row.get("data_ro_pips"))
        sampled_pips = fnum(row.get("sampled_data_pips"))
        out.append({
            "board": "z7020_b01",
            "label": row.get("label", ""),
            "sample_ro_cells": row.get("sample_ro_cells", ""),
            "sampled_data_regs": row.get("sampled_data_regs", ""),
            "data_ro_cells": row.get("data_ro_cells", ""),
            "sampled_reg_loc_count": row.get("sampled_reg_loc_count", ""),
            "data_ro_loc_count": row.get("data_ro_loc_count", ""),
            "sample_ro_pips": row.get("sample_ro_pips", ""),
            "sampled_data_pips": row.get("sampled_data_pips", ""),
            "data_ro_pips": row.get("data_ro_pips", ""),
            "total_pips_audited": int(sample_pips + data_pips + sampled_pips) if not math.isnan(sample_pips + data_pips + sampled_pips) else "",
            "sample_ro_delay_arcs": row.get("sample_ro_delay_arcs", ""),
            "sampled_data_delay_arcs": row.get("sampled_data_delay_arcs", ""),
            "data_ro_delay_arcs": row.get("data_ro_delay_arcs", ""),
            "neighborhood_rows": row.get("neighborhood_rows", ""),
            "source_file": rel(INPUTS["board1_route_summary"]),
        })
    return out


def heldout_route_audit_summary() -> list[dict[str, object]]:
    out = []
    for row in read_csv(INPUTS["heldout_route_summary"]):
        sample_pips = fnum(row.get("sample_ro_pips"))
        data_pips = fnum(row.get("data_ro_pips"))
        sampled_pips = fnum(row.get("sampled_data_pips"))
        out.append({
            "board": "z7020_b02_capture_context",
            "route_pair": "orig_w10_sampler_island_vs_heldout_w10_sample_x36y35",
            "label": row.get("label", ""),
            "sample_ro_locs": row.get("sample_ro_locs", ""),
            "sample_ro_cells": row.get("sample_ro_cells", ""),
            "sampled_data_regs": row.get("sampled_data_regs", ""),
            "data_ro_cells": row.get("data_ro_cells", ""),
            "sample_ro_pips": row.get("sample_ro_pips", ""),
            "sampled_data_pips": row.get("sampled_data_pips", ""),
            "data_ro_pips": row.get("data_ro_pips", ""),
            "total_pips_audited": int(sample_pips + data_pips + sampled_pips) if not math.isnan(sample_pips + data_pips + sampled_pips) else "",
            "sample_ro_delay_arcs": row.get("sample_ro_delay_arcs", ""),
            "sampled_data_delay_arcs": row.get("sampled_data_delay_arcs", ""),
            "data_ro_delay_arcs": row.get("data_ro_delay_arcs", ""),
            "neighborhood_rows": row.get("neighborhood_rows", ""),
            "source_file": rel(INPUTS["heldout_route_summary"]),
        })
    return out


def heldout_route_pair_diff_summary() -> list[dict[str, object]]:
    cell_rows = read_csv(INPUTS["heldout_route_cell_diff"])
    net_rows = read_csv(INPUTS["heldout_route_net_diff"])
    groups = sorted({row.get("group", "") for row in cell_rows} | {row.get("group", "") for row in net_rows})
    out = []
    for group in groups:
        cells = [row for row in cell_rows if row.get("group", "") == group]
        nets = [row for row in net_rows if row.get("group", "") == group]
        out.append({
            "route_pair": "orig_w10_sampler_island_vs_heldout_w10_sample_x36y35",
            "group": group,
            "common_cells": len(cells),
            "loc_changed": sum(row.get("loc_changed", "") == "True" for row in cells),
            "bel_changed": sum(row.get("bel_changed", "") == "True" for row in cells),
            "common_nets": len(nets),
            "route_changed": sum(row.get("route_changed", "") == "True" for row in nets),
            "source_cell_diff": rel(INPUTS["heldout_route_cell_diff"]),
            "source_net_diff": rel(INPUTS["heldout_route_net_diff"]),
        })
    return out


def sampler_counterfactual_board_summary() -> list[dict[str, object]]:
    out = []
    for row in read_csv(INPUTS["board1_balanced_repeats"]):
        p1 = fnum(row.get("p1_mean"))
        out.append({
            "board": "z7020_b01",
            "context": "balanced_repeats",
            "case": row.get("case", ""),
            "warmup": row.get("warmup", ""),
            "n": row.get("n", ""),
            "p1": fmt(p1),
            "abs_bias": fmt(abs(p1 - 0.5)),
            "p1_std": row.get("p1_std", ""),
            "min_entropy": row.get("min_entropy_min", ""),
            "worst_x": row.get("worst_x_max", ""),
            "runs": row.get("runs", ""),
            "source_file": rel(INPUTS["board1_balanced_repeats"]),
        })

    board2_repeat_rows = read_csv(INPUTS["board2_counterfactual_repeats_aggregate"])
    for row in board2_repeat_rows:
        p1 = fnum(row.get("p1_mean"))
        out.append({
            "board": "z7020_b02",
            "context": "restart_counterfactual_repeats_20260530",
            "case": row.get("variant", ""),
            "warmup": row.get("warmup", ""),
            "n": row.get("n", ""),
            "p1": fmt(p1),
            "abs_bias": row.get("abs_bias_mean", fmt(abs(p1 - 0.5))),
            "p1_std": row.get("p1_std", ""),
            "min_entropy": row.get("min_entropy_min", fmt(min_entropy_from_p1(p1))),
            "worst_x": row.get("worst_x_max", ""),
            "runs": row.get("runs", ""),
            "source_file": rel(INPUTS["board2_counterfactual_repeats_aggregate"]),
        })

    legacy_board2_rows = [] if board2_repeat_rows else read_csv(INPUTS["board2_restart_summary"])
    for row in legacy_board2_rows:
        p1 = fnum(row.get("overall_p1"))
        out.append({
            "board": "z7020_b02",
            "context": "restart_counterfactual_legacy_single_run",
            "case": row.get("variant", ""),
            "warmup": row.get("warmup", ""),
            "n": "1",
            "p1": fmt(p1),
            "abs_bias": row.get("abs_bias", ""),
            "p1_std": "",
            "min_entropy": fmt(min_entropy_from_p1(p1)),
            "worst_x": row.get("worst_x", ""),
            "runs": row.get("label", ""),
            "source_file": rel(INPUTS["board2_restart_summary"]),
        })

    for row in read_csv(INPUTS["board2_counterfactual_w4_w5"]):
        p1 = fnum(row.get("overall_p1"))
        out.append({
            "board": "z7020_b02",
            "context": "restart_fifo_counterfactual_crossboard_legacy_single_run",
            "case": row.get("condition", ""),
            "warmup": row.get("warmup", ""),
            "n": "1",
            "p1": fmt(p1),
            "abs_bias": row.get("overall_abs_bias", ""),
            "p1_std": "",
            "min_entropy": row.get("overall_min_entropy", fmt(min_entropy_from_p1(p1))),
            "worst_x": row.get("worst_x", ""),
            "runs": row.get("label", ""),
            "source_file": rel(INPUTS["board2_counterfactual_w4_w5"]),
        })
    return out


def prediction_vs_observed(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    b1_by_kind = {
        (str(row.get("kind")), str(row.get("index"))): row
        for row in rows
        if row.get("board") == "z7020_b01" and row.get("context") == "board1_w10_direction_map"
    }
    b2_rows = [
        row for row in rows
        if row.get("board") == "z7020_b02" and row.get("context") == "heldout_sample_x36y35_regs_x45y31"
    ]

    for row in b2_rows:
        kind = str(row.get("kind", ""))
        index = str(row.get("index", ""))
        observed = fnum(row.get("p1"))
        prior = b1_by_kind.get((kind, index))
        predicted = fnum(prior.get("p1")) if prior else math.nan
        out.append({
            "prediction_id": f"board1_w10_prior_to_board2_heldout_{kind}_{index}",
            "train_scope": "Board1 w10 direction map",
            "test_scope": "Board2 held-out sample_x36y35 full map",
            "kind": kind,
            "index": index,
            "predicted_p1": fmt(predicted),
            "observed_p1": fmt(observed),
            "residual_observed_minus_predicted": fmt(observed - predicted) if not math.isnan(predicted) else "",
            "predicted_abs_bias": fmt(abs(predicted - 0.5)) if not math.isnan(predicted) else "",
            "observed_abs_bias": row.get("abs_bias", fmt(abs(observed - 0.5))),
            "predicted_sign": bias_sign(predicted),
            "observed_sign": bias_sign(observed),
            "sign_match": str(bias_sign(predicted) == bias_sign(observed)) if not math.isnan(predicted) else "",
            "model": "Board1 same-kind prior; not calibrated for board/sampler transfer",
            "coverage_note": "full-map held-out available" if INPUTS["board2_heldout_full_map"].exists() else "subset held-out only",
            "prediction_source": rel(INPUTS["board1_reduced_detail"]) if prior else "",
            "observed_source": row.get("source_file", ""),
        })

    for row in xor_cancellation_model(rows):
        observed = fnum(row.get("measured_all_p1"))
        predicted = fnum(row.get("independent_xor_p1_pred"))
        out.append({
            "prediction_id": f"independent_xor_{row.get('board')}_{row.get('context')}_w{row.get('warmup')}",
            "train_scope": "within-context contributor p1 values",
            "test_scope": "measured aggregate in same context",
            "kind": "aggregate_xor",
            "index": "all",
            "predicted_p1": fmt(predicted),
            "observed_p1": fmt(observed),
            "residual_observed_minus_predicted": fmt(observed - predicted) if not math.isnan(observed) and not math.isnan(predicted) else "",
            "predicted_abs_bias": fmt(abs(predicted - 0.5)) if not math.isnan(predicted) else "",
            "observed_abs_bias": fmt(abs(observed - 0.5)) if not math.isnan(observed) else "",
            "predicted_sign": bias_sign(predicted),
            "observed_sign": bias_sign(observed),
            "sign_match": str(bias_sign(predicted) == bias_sign(observed)) if not math.isnan(observed) and not math.isnan(predicted) else "",
            "model": "independent contributor XOR approximation",
            "coverage_note": "same-context explanatory check; residual is not a failed physical calibration",
            "prediction_source": "contributor_dataset.csv",
            "observed_source": "contributor_dataset.csv",
        })
    return out


def bias_sign(value: float) -> str:
    if math.isnan(value):
        return ""
    if value > 0.5:
        return "positive"
    if value < 0.5:
        return "negative"
    return "zero"


def bias_class(value: float, threshold: float = 0.01) -> str:
    if math.isnan(value):
        return ""
    return "near_balanced" if abs(value - 0.5) <= threshold else "biased"


def rank_values(rows: list[dict[str, object]], value_key: str) -> dict[str, int]:
    values = [
        (str(row.get("index", "")), abs(fnum(row.get(value_key)) - 0.5))
        for row in rows
        if str(row.get("index", "")) not in ("", "all")
        and not math.isnan(fnum(row.get(value_key)))
    ]
    values.sort(key=lambda item: (-item[1], item[0]))
    return {index: rank for rank, (index, _) in enumerate(values, start=1)}


def spearman_from_pairs(pairs: list[tuple[float, float]]) -> float:
    valid = [(a, b) for a, b in pairs if not math.isnan(a) and not math.isnan(b)]
    if len(valid) < 2:
        return math.nan
    a_sorted = sorted((value, i) for i, (value, _) in enumerate(valid))
    b_sorted = sorted((value, i) for i, (_, value) in enumerate(valid))
    a_rank = [0.0] * len(valid)
    b_rank = [0.0] * len(valid)
    for rank, (_, i) in enumerate(a_sorted, start=1):
        a_rank[i] = rank
    for rank, (_, i) in enumerate(b_sorted, start=1):
        b_rank[i] = rank
    return pearson(a_rank, b_rank)


def context_rows(rows: list[dict[str, object]], context_match: str) -> list[dict[str, object]]:
    return [row for row in rows if context_match in str(row.get("context", ""))]


def rows_by_kind_index(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    return {
        (str(row.get("kind", "")), str(row.get("index", ""))): row
        for row in rows
        if row.get("kind")
    }


def strongest_contributors(rows: list[dict[str, object]]) -> tuple[str, str]:
    data = [
        row for row in rows
        if str(row.get("kind")) == "data_ro"
        and str(row.get("index", "")) not in ("", "all")
        and not math.isnan(fnum(row.get("p1")))
    ]
    if not data:
        return "", ""
    low = min(data, key=lambda row: fnum(row.get("p1")))
    high = max(data, key=lambda row: fnum(row.get("p1")))
    return str(low.get("index", "")), str(high.get("index", ""))


def heldout_route_feature_for_index(index: str) -> dict[str, object]:
    rows = read_csv(INPUTS["second_heldout_route_audit"]) if INPUTS["second_heldout_route_audit"].exists() else []
    if not rows:
        path = optional_second_heldout_route_audit_path()
        rows = read_csv(path) if path else []
    for row in rows:
        row_index = str(row.get("index", ""))
        label = str(row.get("label", row.get("bitstream", ""))).lower()
        if row_index == index or f"data_ro{index}" in label:
            return row
    return {}


def warmup_proxy_delta(index: str, kind: str) -> float:
    warmup_rows = [
        row for row in read_csv(INPUTS["board1_warmup_neighbors"])
        if str(row.get("data_ro", "")) == index and str(row.get("mode", "")) == kind
    ]
    p10 = next((fnum(row.get("p1")) for row in warmup_rows if str(row.get("warmup", "")) == "10"), math.nan)
    neighbors = [
        fnum(row.get("p1")) for row in warmup_rows
        if str(row.get("warmup", "")) != "10" and not math.isnan(fnum(row.get("p1")))
    ]
    if math.isnan(p10) or not neighbors:
        return math.nan
    return sum(neighbors) / len(neighbors) - p10


def route_aperture_proxy_delta(index: str) -> float:
    feature = heldout_route_feature_for_index(index)
    if not feature:
        return math.nan
    sample_changed = fnum(feature.get("sample_ro_route_changed_vs_all640"), 0.0)
    data_changed = fnum(feature.get("data_ro_route_changed_vs_all640"), 0.0)
    sampled_changed = fnum(feature.get("sampled_data_route_changed_vs_all640"), 0.0)
    route_pressure = sample_changed + 0.25 * sampled_changed - 0.25 * data_changed
    if math.isnan(route_pressure):
        return math.nan
    return max(-0.02, min(0.02, route_pressure / 5000.0))


def clamp_p1(value: float) -> float:
    if math.isnan(value):
        return value
    return max(0.0, min(1.0, value))


def frozen_prediction_vs_observed(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    first_rows = context_rows(rows, "heldout_sample_x36y35_regs_x45y31")
    second_rows = [
        row for row in rows
        if "second" in str(row.get("context", "")).lower()
        and "heldout" in str(row.get("context", "")).lower()
    ]
    second_path = optional_second_heldout_full_map_path()
    if not second_rows:
        return [
            {
                "prediction_id": f"{baseline}_second_heldout_pending",
                "baseline": baseline,
                "train_scope": "Board2 first held-out and existing route/warmup evidence",
                "test_scope": "Board2 second held-out sampler/context",
                "kind": "",
                "index": "",
                "predicted_p1": "",
                "observed_p1": "",
                "residual_observed_minus_predicted": "",
                "predicted_sign": "",
                "observed_sign": "",
                "sign_match": "",
                "predicted_class": "",
                "observed_class": "",
                "class_match": "",
                "predicted_abs_bias_rank": "",
                "observed_abs_bias_rank": "",
                "residual_direction_match": "",
                "coverage_note": "pending second held-out full-map data",
                "prediction_source": rel(INPUTS["board2_heldout_full_map"]) if INPUTS["board2_heldout_full_map"].exists() else "",
                "observed_source": rel(second_path) if second_path else rel(INPUTS["second_heldout_full_map"]),
            }
            for baseline in [
                "aggregate_only",
                "contributor_only_independent_xor",
                "contributor_plus_warmup",
                "contributor_plus_warmup_plus_route_aperture",
            ]
        ]

    first_by_key = rows_by_kind_index(first_rows)
    second_by_key = rows_by_kind_index(second_rows)
    first_all = first_by_key.get(("all640", "all")) or first_by_key.get(("all64", "all"))
    second_all = second_by_key.get(("all640", "all")) or second_by_key.get(("all64", "all"))
    keys = sorted(second_by_key)
    first_ranks = rank_values(first_rows, "p1")
    second_ranks = rank_values(second_rows, "p1")
    low_idx, high_idx = strongest_contributors(first_rows)

    out: list[dict[str, object]] = []
    for baseline in [
        "aggregate_only",
        "contributor_only_independent_xor",
        "contributor_plus_warmup",
        "contributor_plus_warmup_plus_route_aperture",
    ]:
        for kind, index in keys:
            observed_row = second_by_key[(kind, index)]
            observed = fnum(observed_row.get("p1"))
            predicted = math.nan
            source_note = ""
            if baseline == "aggregate_only":
                if kind.startswith("all") and first_all:
                    predicted = fnum(first_all.get("p1"))
                elif first_all:
                    predicted = fnum(first_all.get("p1"))
                source_note = "first held-out aggregate p1 copied as frozen context prior"
            elif baseline == "contributor_only_independent_xor":
                if kind == "data_ro":
                    prior = first_by_key.get((kind, index))
                    predicted = fnum(prior.get("p1")) if prior else math.nan
                elif kind.startswith("all"):
                    predicted = xor_p1_independent([
                        fnum(row.get("p1")) for row in second_rows
                        if row.get("kind") == "data_ro"
                    ])
                source_note = "same-index contributor prior; aggregate uses second-context measured contributors"
            elif baseline == "contributor_plus_warmup":
                prior = first_by_key.get((kind, index))
                if prior:
                    predicted = fnum(prior.get("p1"))
                    delta = warmup_proxy_delta(index, kind)
                    if not math.isnan(delta):
                        predicted += delta
                elif kind.startswith("all") and second_all:
                    predicted = xor_p1_independent([
                        fnum(row.get("p1")) for row in second_rows
                        if row.get("kind") == "data_ro"
                    ])
                source_note = "first held-out contributor prior plus Board1 warmup-neighbor proxy when available"
            elif baseline == "contributor_plus_warmup_plus_route_aperture":
                prior = first_by_key.get((kind, index))
                if prior:
                    predicted = fnum(prior.get("p1"))
                    warm_delta = warmup_proxy_delta(index, kind)
                    route_delta = route_aperture_proxy_delta(index)
                    predicted += 0.0 if math.isnan(warm_delta) else warm_delta
                    predicted += 0.0 if math.isnan(route_delta) else route_delta
                elif kind.startswith("all") and second_all:
                    predicted = xor_p1_independent([
                        fnum(row.get("p1")) for row in second_rows
                        if row.get("kind") == "data_ro"
                    ])
                source_note = "warmup proxy plus route/audit proxy; not calibrated unless second route audit is present"

            predicted = clamp_p1(predicted)
            residual = observed - predicted if not math.isnan(observed) and not math.isnan(predicted) else math.nan
            predicted_rank = first_ranks.get(index, "")
            observed_rank = second_ranks.get(index, "")
            if baseline != "aggregate_only" and kind == "data_ro" and index in (low_idx, high_idx):
                rank_note = f"; first held-out strongest anchor={index}"
            else:
                rank_note = ""
            out.append({
                "prediction_id": f"{baseline}_second_heldout_{kind}_{index}",
                "baseline": baseline,
                "train_scope": "Board2 first held-out plus existing warmup/route proxies",
                "test_scope": "Board2 second held-out sampler/context",
                "kind": kind,
                "index": index,
                "predicted_p1": fmt(predicted),
                "observed_p1": fmt(observed),
                "residual_observed_minus_predicted": fmt(residual),
                "predicted_sign": bias_sign(predicted),
                "observed_sign": bias_sign(observed),
                "sign_match": str(bias_sign(predicted) == bias_sign(observed)) if not math.isnan(predicted) and not math.isnan(observed) else "",
                "predicted_class": bias_class(predicted),
                "observed_class": bias_class(observed),
                "class_match": str(bias_class(predicted) == bias_class(observed)) if not math.isnan(predicted) and not math.isnan(observed) else "",
                "predicted_abs_bias_rank": predicted_rank,
                "observed_abs_bias_rank": observed_rank,
                "residual_direction_match": str(bias_sign(predicted) == bias_sign(observed)) if kind.startswith("all") and not math.isnan(predicted) and not math.isnan(observed) else "",
                "coverage_note": source_note + rank_note,
                "prediction_source": rel(INPUTS["board2_heldout_full_map"]) if INPUTS["board2_heldout_full_map"].exists() else "",
                "observed_source": observed_row.get("source_file", rel(second_path) if second_path else ""),
            })
    return out


def prediction_metrics_summary(frozen_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for baseline in sorted({str(row.get("baseline", "")) for row in frozen_rows if row.get("baseline")}):
        rows = [row for row in frozen_rows if row.get("baseline") == baseline and row.get("observed_p1")]
        contributor_rows = [row for row in rows if row.get("kind") == "data_ro"]
        residuals = [abs(fnum(row.get("residual_observed_minus_predicted"))) for row in rows if not math.isnan(fnum(row.get("residual_observed_minus_predicted")))]
        signed_rows = [row for row in rows if row.get("sign_match") in ("True", "False")]
        class_rows = [row for row in rows if row.get("class_match") in ("True", "False")]
        rank_pairs = [
            (fnum(row.get("predicted_abs_bias_rank")), fnum(row.get("observed_abs_bias_rank")))
            for row in contributor_rows
            if row.get("predicted_abs_bias_rank") and row.get("observed_abs_bias_rank")
        ]
        residual_direction_rows = [row for row in rows if row.get("residual_direction_match") in ("True", "False")]
        out.append({
            "baseline": baseline,
            "rows_evaluated": len(rows),
            "contributor_rows_evaluated": len(contributor_rows),
            "sign_accuracy": fmt(sum(row.get("sign_match") == "True" for row in signed_rows) / len(signed_rows)) if signed_rows else "",
            "rank_correlation_spearman": fmt(spearman_from_pairs(rank_pairs)),
            "class_accuracy": fmt(sum(row.get("class_match") == "True" for row in class_rows) / len(class_rows)) if class_rows else "",
            "mae_p1": fmt(sum(residuals) / len(residuals)) if residuals else "",
            "residual_direction_accuracy": fmt(sum(row.get("residual_direction_match") == "True" for row in residual_direction_rows) / len(residual_direction_rows)) if residual_direction_rows else "",
            "status": "evaluated" if rows else "pending_second_heldout_data",
        })
    if not out:
        out.append({
            "baseline": "all",
            "rows_evaluated": 0,
            "contributor_rows_evaluated": 0,
            "sign_accuracy": "",
            "rank_correlation_spearman": "",
            "class_accuracy": "",
            "mae_p1": "",
            "residual_direction_accuracy": "",
            "status": "pending_second_heldout_data",
        })
    return out


def mechanism_ablation_summary(metrics_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    order = [
        "aggregate_only",
        "contributor_only_independent_xor",
        "contributor_plus_warmup",
        "contributor_plus_warmup_plus_route_aperture",
    ]
    by_baseline = {row.get("baseline"): row for row in metrics_rows}
    out = []
    previous = None
    for baseline in order:
        row = by_baseline.get(baseline)
        if not row:
            continue
        mae = fnum(row.get("mae_p1"))
        prev_mae = fnum(previous.get("mae_p1")) if previous else math.nan
        out.append({
            "baseline": baseline,
            "added_information": {
                "aggregate_only": "first held-out aggregate prior",
                "contributor_only_independent_xor": "per-contributor bias and XOR aggregation",
                "contributor_plus_warmup": "warmup-neighbor proxy",
                "contributor_plus_warmup_plus_route_aperture": "route/audit sampler-aperture proxy",
            }[baseline],
            "rows_evaluated": row.get("rows_evaluated", ""),
            "sign_accuracy": row.get("sign_accuracy", ""),
            "class_accuracy": row.get("class_accuracy", ""),
            "mae_p1": row.get("mae_p1", ""),
            "mae_improvement_vs_previous": fmt(prev_mae - mae) if not math.isnan(prev_mae) and not math.isnan(mae) else "",
            "rank_correlation_spearman": row.get("rank_correlation_spearman", ""),
            "status": row.get("status", ""),
        })
        previous = row
    if not out:
        out.append({
            "baseline": "all",
            "added_information": "pending second held-out observation",
            "rows_evaluated": 0,
            "sign_accuracy": "",
            "class_accuracy": "",
            "mae_p1": "",
            "mae_improvement_vs_previous": "",
            "rank_correlation_spearman": "",
            "status": "pending_second_heldout_data",
        })
    return out


def route_result_correlation(counterfactual: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    result_by_key: dict[tuple[str, str, str], dict[str, object]] = {}
    for row in counterfactual:
        if row.get("board") == "z7020_b01":
            result_by_key[("z7020_b01", normalize_case(str(row.get("case"))), str(row.get("warmup")))] = row
        elif row.get("board") == "z7020_b02" and str(row.get("context", "")).startswith("restart_counterfactual"):
            result_by_key[("z7020_b02", normalize_case(str(row.get("case"))), str(row.get("warmup")))] = row

    route_rows = route_feature_summary()
    for route in route_rows:
        label = str(route.get("label", ""))
        warmup = warmup_from_label(label)
        key = ("z7020_b01", normalize_case(label), warmup)
        result = result_by_key.get(key)
        observed = fnum(result.get("p1")) if result else math.nan
        total_pips = fnum(route.get("total_pips_audited"))
        sample_pips = fnum(route.get("sample_ro_pips"))
        data_pips = fnum(route.get("data_ro_pips"))
        out.append({
            "row_id": f"board1_{label}",
            "board": "z7020_b01",
            "route_label": label,
            "result_case": result.get("case", "") if result else "",
            "warmup": warmup,
            "observed_p1": fmt(observed),
            "observed_abs_bias": result.get("abs_bias", "") if result else "",
            "sample_ro_pips": route.get("sample_ro_pips", ""),
            "sampled_data_pips": route.get("sampled_data_pips", ""),
            "data_ro_pips": route.get("data_ro_pips", ""),
            "total_pips_audited": route.get("total_pips_audited", ""),
            "sample_to_data_pip_ratio": fmt(sample_pips / data_pips) if data_pips and not math.isnan(sample_pips) and not math.isnan(data_pips) else "",
            "neighborhood_rows": route.get("neighborhood_rows", ""),
            "correlation_scope": "route/result join by label and warmup where available",
            "limitation": "" if result else "no matching observed result row; route-only audit",
            "route_source": route.get("source_file", ""),
            "result_source": result.get("source_file", "") if result else "",
        })

    heldout_result_rows = read_csv(INPUTS["board2_heldout_full_map"])
    heldout_all = next((row for row in heldout_result_rows if row.get("kind") == "all640"), {})
    for route in heldout_route_audit_summary():
        label = str(route.get("label", ""))
        if label.startswith("heldout"):
            observed = fnum(heldout_all.get("p1"))
            observed_abs = heldout_all.get("abs_bias", "")
            result_case = "heldout reduced-XOR all640"
            result_source = rel(INPUTS["board2_heldout_full_map"]) if heldout_all else ""
        elif label.startswith("orig"):
            observed = fnum(heldout_all.get("original_w10_p1"))
            observed_abs = fmt(abs(observed - 0.5)) if not math.isnan(observed) else ""
            result_case = "original w10 all640 comparator"
            result_source = rel(INPUTS["board2_heldout_full_map"]) if heldout_all else ""
        else:
            observed = math.nan
            observed_abs = ""
            result_case = ""
            result_source = ""
        total_pips = fnum(route.get("total_pips_audited"))
        sample_pips = fnum(route.get("sample_ro_pips"))
        data_pips = fnum(route.get("data_ro_pips"))
        out.append({
            "row_id": f"heldout_{label}",
            "board": "z7020_b02_capture_context",
            "route_label": label,
            "result_case": result_case,
            "warmup": "10" if "w10" in label else "",
            "observed_p1": fmt(observed),
            "observed_abs_bias": observed_abs,
            "sample_ro_pips": route.get("sample_ro_pips", ""),
            "sampled_data_pips": route.get("sampled_data_pips", ""),
            "data_ro_pips": route.get("data_ro_pips", ""),
            "total_pips_audited": route.get("total_pips_audited", ""),
            "sample_to_data_pip_ratio": fmt(sample_pips / data_pips) if data_pips and not math.isnan(sample_pips) and not math.isnan(data_pips) else "",
            "neighborhood_rows": route.get("neighborhood_rows", ""),
            "correlation_scope": "held-out all640 route audit with companion per-subset audit available",
            "limitation": "all640 context-level row; see per-bitstream rows for reduced-XOR subset route features",
            "route_source": route.get("source_file", ""),
            "result_source": result_source,
        })

    for row in read_csv(INPUTS["route_lock_feasibility"]):
        out.append({
            "row_id": "route_lock_" + row.get("run", ""),
            "board": "z7020_b01",
            "route_label": row.get("label_hint", ""),
            "result_case": "",
            "warmup": warmup_from_label(row.get("run", "")),
            "observed_p1": "",
            "observed_abs_bias": "",
            "sample_ro_pips": "",
            "sampled_data_pips": "",
            "data_ro_pips": "",
            "total_pips_audited": row.get("selected_nets", ""),
            "sample_to_data_pip_ratio": "",
            "neighborhood_rows": "",
            "correlation_scope": "implementation feasibility metric only",
            "limitation": f"hardware_gate={row.get('hardware_gate', '')}; gate_reason={row.get('gate_reason', '')}; applied_ratio={row.get('applied_ratio', '')}",
            "route_source": rel(INPUTS["route_lock_feasibility"]),
            "result_source": "",
        })

    for path in optional_per_bitstream_route_audit_paths():
        for idx, row in enumerate(read_csv(path), start=1):
            label = row.get("bitstream", row.get("label", row.get("run", path.stem)))
            out.append({
                "row_id": f"per_bitstream_route_audit_{path.stem}_{idx}",
                "board": row.get("board", ""),
                "route_label": label,
                "result_case": row.get("case", row.get("variant", "")),
                "warmup": row.get("warmup", warmup_from_label(label)),
                "observed_p1": row.get("p1", row.get("overall_p1", "")),
                "observed_abs_bias": row.get("abs_bias", row.get("overall_abs_bias", "")),
                "sample_ro_pips": row.get("sample_ro_pips", ""),
                "sampled_data_pips": row.get("sampled_data_pips", ""),
                "data_ro_pips": row.get("data_ro_pips", ""),
                "total_pips_audited": row.get("total_pips_audited", row.get("selected_nets", "")),
                "sample_to_data_pip_ratio": row.get("sample_to_data_pip_ratio", ""),
                "neighborhood_rows": row.get("neighborhood_rows", ""),
                "correlation_scope": "per-bitstream route audit as provided",
                "limitation": row.get("limitation", "schema-normalized optional input"),
                "route_source": rel(path),
                "result_source": rel(path),
            })

    for path in optional_implementation_metric_paths():
        for idx, row in enumerate(read_csv(path), start=1):
            label = row.get("implementation", row.get("label", row.get("run", path.stem)))
            out.append({
                "row_id": f"implementation_metrics_{path.stem}_{idx}",
                "board": row.get("board", ""),
                "route_label": label,
                "result_case": row.get("case", row.get("variant", "")),
                "warmup": row.get("warmup", warmup_from_label(label)),
                "observed_p1": row.get("p1", row.get("overall_p1", "")),
                "observed_abs_bias": row.get("abs_bias", row.get("overall_abs_bias", "")),
                "sample_ro_pips": row.get("sample_ro_pips", ""),
                "sampled_data_pips": row.get("sampled_data_pips", ""),
                "data_ro_pips": row.get("data_ro_pips", ""),
                "total_pips_audited": row.get("total_pips_audited", row.get("selected_nets", "")),
                "sample_to_data_pip_ratio": row.get("sample_to_data_pip_ratio", ""),
                "neighborhood_rows": row.get("neighborhood_rows", ""),
                "correlation_scope": "implementation metrics as provided",
                "limitation": row.get("limitation", "resource/timing/power schema not standardized by this script"),
                "route_source": rel(path),
                "result_source": rel(path),
            })
    return out


def normalize_case(text: str) -> str:
    low = text.lower()
    if "reverse" in low:
        return "reverse repair"
    if "forward" in low:
        return "forward fail"
    if "compact" in low or "baseline" in low:
        return "compact baseline"
    return low


def warmup_from_label(label: str) -> str:
    match = re.search(r"(?:^|_)w(?:armup)?(\d+)(?:_|$)", label)
    return match.group(1) if match else ""


def find_row(rows: list[dict[str, object]], **matches: object) -> dict[str, object] | None:
    for row in rows:
        if all(row.get(key) == value for key, value in matches.items()):
            return row
    return None


def write_report(paths: dict[str, Path], counts: dict[str, int], highlights: dict[str, str], missing_rows: list[dict[str, object]]) -> None:
    report = OUT / "tvlsi_sampler_aperture_model_20260530.md"
    missing_text = "\n".join(f"- {row['input_name']}: {row['description']}" for row in missing_rows)
    if not missing_text:
        missing_text = "- None of the tracked optional inputs are missing."
    text = f"""# TVLSI Sampler-Aperture Offline Model

Generated from existing CSV summaries and routed-DCP audit CSVs. No hardware capture was run by this script; the held-out sampler route audit was extracted from existing routed DCPs.

## Model

For contributor bitstream `X_i(b,r,w)`, define:

- `p_i = Pr[X_i=1]`
- signed bias `s_i = p_i - 0.5`
- XOR factor `beta_i = 1 - 2p_i`

For an XOR over contributor set `S`, the independence approximation is:

```text
Pr[Y_S=1] = (1 - product_i(1 - 2p_i)) / 2
```

The approximation is intentionally limited. Residuals should be interpreted as correlation, fixed-position restart structure, or unmodeled sampler-aperture effects, not as a calibrated physical proof.

## Generated Tables

| Table | Rows | Path |
|---|---:|---|
| Contributor dataset | {counts['contributors']} | `{paths['contributors'].relative_to(ROOT)}` |
| XOR cancellation model | {counts['xor']} | `{paths['xor'].relative_to(ROOT)}` |
| Repeat stability summary | {counts['repeat']} | `{paths['repeat'].relative_to(ROOT)}` |
| Warmup neighbor summary | {counts['warmup']} | `{paths['warmup'].relative_to(ROOT)}` |
| Route feature summary | {counts['route']} | `{paths['route'].relative_to(ROOT)}` |
| Held-out sampler route audit | {counts['heldout_route']} | `{paths['heldout_route'].relative_to(ROOT)}` |
| Held-out sampler route pair diff | {counts['heldout_pair']} | `{paths['heldout_pair'].relative_to(ROOT)}` |
| Sampler counterfactual board summary | {counts['counterfactual']} | `{paths['counterfactual'].relative_to(ROOT)}` |
| Prediction versus observed | {counts['prediction']} | `{paths['prediction'].relative_to(ROOT)}` |
| Frozen prediction versus observed | {counts['frozen_prediction']} | `{paths['frozen_prediction'].relative_to(ROOT)}` |
| Prediction metrics summary | {counts['prediction_metrics']} | `{paths['prediction_metrics'].relative_to(ROOT)}` |
| Mechanism ablation summary | {counts['mechanism_ablation']} | `{paths['mechanism_ablation'].relative_to(ROOT)}` |
| Route/result correlation | {counts['route_correlation']} | `{paths['route_correlation'].relative_to(ROOT)}` |
| Input source status | {counts['source_status']} | `{paths['source_status'].relative_to(ROOT)}` |

## First Offline Highlights

- {highlights['board1_xor']}
- {highlights['board2_xor']}
- {highlights['repeat']}
- {highlights['prediction']}
- {highlights['frozen_prediction']}
- {highlights['heldout_route']}
- {highlights['route_correlation']}
- {highlights['counterfactual']}

## Interpretation

The useful TVLSI-level story is not simply that one run is biased. The stronger story is that the contributor distribution, warmup setting, board instance, and sampler route context jointly determine the effective sampling aperture. XOR aggregation can hide biased contributors through cancellation, so aggregate pass/fail metrics alone are not enough for implementation guidance.

## Current Limits

- The XOR model assumes independent contributors and therefore cannot explain correlation or deterministic startup-position structure by itself.
- Route/PIP/net-delay linkage is extracted for the original sampler-island, first held-out sample-x36y35, and second held-out sample_ro_local contexts when those routed-DCP audits are present.
- Route/result correlation remains mixed evidence: per-bitstream route rows are available, but the route/aperture proxy is not yet a calibrated causal model.
- Frozen second-held-out prediction is evaluated when the second full map is present; weak baselines and residuals are retained as model-boundary evidence.
- This report is an interpretation scaffold. TVLSI-strength mechanism claims still need targeted phase/PVT/coupling experiments.

## Missing Optional Inputs

{missing_text}
"""
    report.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    contributors = contributor_dataset()
    xor_rows = xor_cancellation_model(contributors)
    repeats = repeat_stability_summary()
    warmup = warmup_neighbor_summary()
    route = route_feature_summary()
    heldout_route = heldout_route_audit_summary()
    heldout_pair = heldout_route_pair_diff_summary()
    counterfactual = sampler_counterfactual_board_summary()
    prediction = prediction_vs_observed(contributors)
    frozen_prediction = frozen_prediction_vs_observed(contributors)
    prediction_metrics = prediction_metrics_summary(frozen_prediction)
    mechanism_ablation = mechanism_ablation_summary(prediction_metrics)
    route_correlation = route_result_correlation(counterfactual)
    source_status = source_status_rows()
    missing_rows = [row for row in source_status if row.get("status") == "missing"]

    paths = {
        "contributors": OUT / "contributor_dataset.csv",
        "xor": OUT / "xor_cancellation_model.csv",
        "repeat": OUT / "repeat_stability_summary.csv",
        "warmup": OUT / "warmup_neighbor_summary.csv",
        "route": OUT / "route_feature_summary.csv",
        "heldout_route": OUT / "heldout_sampler_route_audit_summary.csv",
        "heldout_pair": OUT / "heldout_sampler_route_pair_diff_summary.csv",
        "counterfactual": OUT / "sampler_counterfactual_board_summary.csv",
        "prediction": OUT / "prediction_vs_observed.csv",
        "frozen_prediction": OUT / "frozen_prediction_vs_observed.csv",
        "prediction_metrics": OUT / "prediction_metrics_summary.csv",
        "mechanism_ablation": OUT / "mechanism_ablation_summary.csv",
        "route_correlation": OUT / "route_result_correlation.csv",
        "source_status": OUT / "input_source_status.csv",
    }

    common_fields = [
        "board", "context", "implementation", "warmup", "kind", "index", "p1",
        "signed_bias", "abs_bias", "beta_factor", "min_entropy", "worst_x",
        "worst_p1", "source_file",
    ]
    write_csv(paths["contributors"], contributors, common_fields)
    write_csv(paths["xor"], xor_rows, [
        "board", "context", "warmup", "contributor_count", "contributor_indices",
        "independent_xor_p1_pred", "measured_all_p1", "residual_measured_minus_pred",
        "pred_abs_bias", "measured_abs_bias", "interpretation",
    ])
    write_csv(paths["repeat"], repeats, [
        "board", "context", "mode", "n", "same_bias_sign_count",
        "same_bias_sign_fraction", "mean_abs_delta_p1", "max_abs_delta_p1",
        "pearson_p1_run01_run02", "source_file",
    ])
    write_csv(paths["warmup"], warmup, [
        "board", "context", "mode", "data_ro", "warmup", "p1", "signed_bias",
        "abs_bias", "min_entropy", "worst_x", "worst_p1", "source_file",
    ])
    write_csv(paths["route"], route, [
        "board", "label", "sample_ro_cells", "sampled_data_regs", "data_ro_cells",
        "sampled_reg_loc_count", "data_ro_loc_count", "sample_ro_pips",
        "sampled_data_pips", "data_ro_pips", "total_pips_audited",
        "sample_ro_delay_arcs", "sampled_data_delay_arcs", "data_ro_delay_arcs",
        "neighborhood_rows", "source_file",
    ])
    write_csv(paths["heldout_route"], heldout_route, [
        "board", "route_pair", "label", "sample_ro_locs", "sample_ro_cells",
        "sampled_data_regs", "data_ro_cells", "sample_ro_pips",
        "sampled_data_pips", "data_ro_pips", "total_pips_audited",
        "sample_ro_delay_arcs", "sampled_data_delay_arcs", "data_ro_delay_arcs",
        "neighborhood_rows", "source_file",
    ])
    write_csv(paths["heldout_pair"], heldout_pair, [
        "route_pair", "group", "common_cells", "loc_changed", "bel_changed",
        "common_nets", "route_changed", "source_cell_diff", "source_net_diff",
    ])
    write_csv(paths["counterfactual"], counterfactual, [
        "board", "context", "case", "warmup", "n", "p1", "abs_bias", "p1_std",
        "min_entropy", "worst_x", "runs", "source_file",
    ])
    write_csv(paths["prediction"], prediction, [
        "prediction_id", "train_scope", "test_scope", "kind", "index",
        "predicted_p1", "observed_p1", "residual_observed_minus_predicted",
        "predicted_abs_bias", "observed_abs_bias", "predicted_sign",
        "observed_sign", "sign_match", "model", "coverage_note",
        "prediction_source", "observed_source",
    ])
    write_csv(paths["frozen_prediction"], frozen_prediction, [
        "prediction_id", "baseline", "train_scope", "test_scope", "kind", "index",
        "predicted_p1", "observed_p1", "residual_observed_minus_predicted",
        "predicted_sign", "observed_sign", "sign_match", "predicted_class",
        "observed_class", "class_match", "predicted_abs_bias_rank",
        "observed_abs_bias_rank", "residual_direction_match", "coverage_note",
        "prediction_source", "observed_source",
    ])
    write_csv(paths["prediction_metrics"], prediction_metrics, [
        "baseline", "rows_evaluated", "contributor_rows_evaluated",
        "sign_accuracy", "rank_correlation_spearman", "class_accuracy",
        "mae_p1", "residual_direction_accuracy", "status",
    ])
    write_csv(paths["mechanism_ablation"], mechanism_ablation, [
        "baseline", "added_information", "rows_evaluated", "sign_accuracy",
        "class_accuracy", "mae_p1", "mae_improvement_vs_previous",
        "rank_correlation_spearman", "status",
    ])
    write_csv(paths["route_correlation"], route_correlation, [
        "row_id", "board", "route_label", "result_case", "warmup",
        "observed_p1", "observed_abs_bias", "sample_ro_pips",
        "sampled_data_pips", "data_ro_pips", "total_pips_audited",
        "sample_to_data_pip_ratio", "neighborhood_rows", "correlation_scope",
        "limitation", "route_source", "result_source",
    ])
    write_csv(paths["source_status"], source_status, [
        "input_name", "description", "status", "path",
    ])

    b1_xor = find_row(xor_rows, board="z7020_b01")
    b2_xor = find_row(xor_rows, board="z7020_b02", context="heldout_sample_x36y35_regs_x45y31")
    data_repeat = find_row(repeats, mode="data_ro")
    board1_forward_w4 = find_row(counterfactual, board="z7020_b01", case="forward fail", warmup="4")
    board2_forward_w4 = next((row for row in counterfactual if row["board"] == "z7020_b02" and row.get("context") == "restart_counterfactual_repeats_20260530" and str(row["case"]).startswith("forward") and row["warmup"] == "4"), None)
    sample_ro_pair = find_row(heldout_pair, group="sample_ro")
    data_ro_pair = find_row(heldout_pair, group="data_ro")
    sample_ro_net_pair = find_row(heldout_pair, group="sample_ro_net")
    heldout_predictions = [row for row in prediction if str(row.get("prediction_id", "")).startswith("board1_w10_prior")]
    matched_predictions = sum(1 for row in heldout_predictions if row.get("sign_match") == "True")
    frozen_evaluated = [row for row in prediction_metrics if row.get("status") == "evaluated"]
    frozen_pending = not frozen_evaluated
    matched_route_results = sum(1 for row in route_correlation if row.get("observed_p1"))

    highlights = {
        "board1_xor": f"Board1 full 8-data-RO independence approximation predicts p1={b1_xor['independent_xor_p1_pred']} versus measured all64 p1={b1_xor['measured_all_p1']}, leaving residual {b1_xor['residual_measured_minus_pred']}." if b1_xor else "Board1 XOR prediction was skipped because the contributor input is missing.",
        "board2_xor": f"Board2 held-out sampler uses {b2_xor['contributor_count']} data-RO contributors and predicts p1={b2_xor['independent_xor_p1_pred']} versus measured aggregate p1={b2_xor['measured_all_p1']}." if b2_xor else "Board2 held-out XOR prediction was skipped because held-out contributor input is missing.",
        "repeat": f"Board1 data_ro repeat has same bias sign {data_repeat['same_bias_sign_count']}/{data_repeat['n']} with Pearson r={data_repeat['pearson_p1_run01_run02']}." if data_repeat else "Repeat stability summary was skipped because repeat input is missing.",
        "prediction": f"Held-out prediction table contains {len(heldout_predictions)} Board1-prior-to-Board2 rows with {matched_predictions} sign matches; this is a falsification-oriented prior, not a calibrated transfer model.",
        "frozen_prediction": f"Second held-out frozen prediction is pending because the second held-out full-map input is not present; schema-stable pending rows were generated." if frozen_pending else f"Second held-out frozen prediction evaluated {sum(int(row.get('rows_evaluated', 0)) for row in frozen_evaluated)} rows across {len(frozen_evaluated)} baselines; see prediction metrics for accuracy and residuals.",
        "heldout_route": f"Held-out route audit keeps data-RO cells fixed ({data_ro_pair['loc_changed']}/{data_ro_pair['common_cells']} LOC changes) while moving sample-RO cells ({sample_ro_pair['loc_changed']}/{sample_ro_pair['common_cells']} LOC changes) and changing {sample_ro_net_pair['route_changed']}/{sample_ro_net_pair['common_nets']} sample-RO nets." if sample_ro_pair and data_ro_pair and sample_ro_net_pair else "Held-out route audit is partial or missing; route pair-diff highlight was skipped.",
        "route_correlation": f"Route/result correlation table has {len(route_correlation)} rows, with observed p1 joined for {matched_route_results}; unmatched rows are retained as route-only or implementation-gate evidence.",
        "counterfactual": f"Forward sampler counterfactual remains biased in both balanced summaries: Board1 w4 mean p1={board1_forward_w4['p1']} over n={board1_forward_w4['n']}; Board2 w4 mean p1={board2_forward_w4['p1']} over n={board2_forward_w4['n']}." if board1_forward_w4 and board2_forward_w4 else "Counterfactual highlight was skipped because one side of the board comparison is missing.",
    }

    write_report(paths, {
        "contributors": len(contributors),
        "xor": len(xor_rows),
        "repeat": len(repeats),
        "warmup": len(warmup),
        "route": len(route),
        "heldout_route": len(heldout_route),
        "heldout_pair": len(heldout_pair),
        "counterfactual": len(counterfactual),
        "prediction": len(prediction),
        "frozen_prediction": len(frozen_prediction),
        "prediction_metrics": len(prediction_metrics),
        "mechanism_ablation": len(mechanism_ablation),
        "route_correlation": len(route_correlation),
        "source_status": len(source_status),
    }, highlights, missing_rows)

    print(f"Wrote TVLSI offline model outputs to {OUT}")
    if missing_rows:
        print("Missing optional inputs: " + ", ".join(str(row["input_name"]) for row in missing_rows))


if __name__ == "__main__":
    main()
