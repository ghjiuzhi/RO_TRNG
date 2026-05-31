#!/usr/bin/env python3
"""Summarize TVLSI toolflow/directive sensitivity captures and route diffs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DIR = (
    ROOT
    / "data"
    / "hardware"
    / "20260529_fpga1_board2"
    / "restart_toolflow_sensitivity_20260531"
)
DEFAULT_ROUTE_DIR = ROOT / "data" / "experiments" / "toolflow_sensitivity_matrix_20260531" / "route_extract"
DEFAULT_OUT_DIR = ROOT / "data" / "experiments" / "toolflow_sensitivity_matrix_20260531"

BOARD = "z7020_b02"
RESTART_COUNT = 1000
ROW_BYTES = 125
HEADER_BYTES = 8
SYNC_HEADER = bytes.fromhex("A55A")
DATE_TAG = "20260531"

CONTEXTS = [
    ("heldout_sample_x36y35_regs_x45y31", "heldout_x36y35"),
    ("second_heldout_sample_ro_local", "sample_ro_local"),
]
ANCHORS = [("all640", "all640", "all"), ("data_ro0", "data_ro", "0"), ("data_ro4", "data_ro", "4")]
IMPLEMENTATIONS = [
    ("original", "", "", "", ""),
    ("explore1", "explore1", "Explore", "Explore", "Explore"),
]

RAW_RE = re.compile(
    r"^restart_toolflow_random1_(?P<context>.+?)"
    r"_warmup(?P<warmup>\d+)_"
    r"(?P<anchor>all640|data_ro\d+)_"
    r"(?P<implementation>original|explore1)_"
    r"(?P<run_id>[^_]+)_"
    r"(?P<restart_count>\d+)x(?P<row_bytes>\d+)_strict_"
    r"(?P<date_tag>\d{8})\.bin$"
)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def entropy_binary(p1: float) -> float:
    q = max(p1, 1.0 - p1)
    return -math.log2(q) if q > 0.0 else 0.0


def fmt(value: Any, digits: int = 9) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(x):
        return ""
    return f"{x:.{digits}f}"


def to_float(value: Any) -> float | None:
    try:
        if value in ("", None):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def anchor_parts(anchor: str) -> tuple[str, str]:
    if anchor == "all640":
        return "all640", "all"
    m = re.fullmatch(r"(data_ro)(\d+)", anchor)
    if not m:
        raise ValueError(f"Cannot parse anchor: {anchor}")
    return m.group(1), m.group(2)


def expected_rows() -> list[dict[str, str]]:
    rows = []
    for context, context_label in CONTEXTS:
        for anchor, kind, index in ANCHORS:
            for implementation, directive_tag, place, phys_opt, route in IMPLEMENTATIONS:
                rows.append(
                    {
                        "board": BOARD,
                        "context": context,
                        "context_label": context_label,
                        "warmup": "10",
                        "run_id": "run01",
                        "anchor": anchor,
                        "kind": kind,
                        "index": index,
                        "implementation": implementation,
                        "directive_tag": directive_tag,
                        "place_directive": place,
                        "phys_opt_directive": phys_opt,
                        "route_directive": route,
                        "route_label": f"{context_label}_{anchor}_{implementation}",
                    }
                )
    return rows


def summarize_payload(path: Path, restart_count: int, row_bytes: int) -> dict[str, Any]:
    data = path.read_bytes()
    expected_bytes = HEADER_BYTES + restart_count * row_bytes
    header_ok = len(data) >= HEADER_BYTES and data[:2] == SYNC_HEADER
    if len(data) != expected_bytes:
        return {
            "status": "invalid_size",
            "status_detail": f"expected {expected_bytes} bytes, got {len(data)}",
            "raw_bytes": len(data),
            "payload_bytes": max(len(data) - HEADER_BYTES, 0),
            "header_ok": header_ok,
        }
    if not header_ok:
        return {
            "status": "invalid_header",
            "status_detail": "sync header A55A not found at byte 0",
            "raw_bytes": len(data),
            "payload_bytes": len(data) - HEADER_BYTES,
            "header_ok": False,
        }

    payload = data[HEADER_BYTES:]
    total_bits = len(payload) * 8
    ones = sum(byte.bit_count() for byte in payload)
    p1 = ones / total_bits

    worst_abs_bias = -1.0
    worst_x = -1
    worst_p1 = math.nan
    for byte_idx in range(row_bytes):
        for bit_idx in range(8):
            bit_ones = 0
            for row_idx in range(restart_count):
                value = payload[row_idx * row_bytes + byte_idx]
                bit_ones += (value >> bit_idx) & 1
            bit_p1 = bit_ones / restart_count
            bit_abs_bias = abs(bit_p1 - 0.5)
            if bit_abs_bias > worst_abs_bias:
                worst_abs_bias = bit_abs_bias
                worst_x = byte_idx * 8 + bit_idx
                worst_p1 = bit_p1

    row_ones = []
    for row_idx in range(restart_count):
        start = row_idx * row_bytes
        row = payload[start : start + row_bytes]
        row_ones.append(sum(byte.bit_count() for byte in row))

    return {
        "status": "ok",
        "status_detail": "",
        "p1": p1,
        "signed_bias": p1 - 0.5,
        "abs_bias": abs(p1 - 0.5),
        "min_entropy": entropy_binary(p1),
        "worst_x": worst_x,
        "worst_p1": worst_p1,
        "worst_abs_bias": worst_abs_bias,
        "row_ones_mean": mean(row_ones),
        "row_ones_std": pstdev(row_ones) if len(row_ones) > 1 else 0.0,
        "raw_bytes": len(data),
        "payload_bytes": len(payload),
        "header_ok": header_ok,
    }


def discover_captures(raw_dir: Path, metadata_dir: Path) -> dict[tuple[str, str, str], dict[str, Any]]:
    rows: dict[tuple[str, str, str], dict[str, Any]] = {}
    if not raw_dir.exists():
        return rows
    for path in sorted(raw_dir.glob("*.bin")):
        match = RAW_RE.match(path.name)
        if not match:
            continue
        fields = match.groupdict()
        context = fields["context"]
        anchor = fields["anchor"]
        implementation = fields["implementation"]
        kind, index = anchor_parts(anchor)
        restart_count = int(fields["restart_count"])
        row_bytes = int(fields["row_bytes"])
        meta_path = metadata_dir / f"{path.stem}.json"
        meta = read_json(meta_path)
        stats = summarize_payload(path, restart_count, row_bytes)
        context_label = str(meta.get("context_label", dict(CONTEXTS).get(context, context)))
        directive_tag = str(meta.get("directive_tag", ""))
        row = {
            "board": str(meta.get("board_id", BOARD)),
            "context": str(meta.get("context", context)),
            "context_label": context_label,
            "warmup": fields["warmup"],
            "run_id": fields["run_id"],
            "anchor": anchor,
            "kind": str(meta.get("kind", kind)),
            "index": str(meta.get("index", index)),
            "implementation": str(meta.get("implementation", implementation)),
            "directive_tag": directive_tag,
            "place_directive": str(meta.get("place_directive", "")),
            "phys_opt_directive": str(meta.get("phys_opt_directive", "")),
            "route_directive": str(meta.get("route_directive", "")),
            "route_label": str(meta.get("route_label", f"{context_label}_{anchor}_{implementation}")),
            "status": stats["status"],
            "status_detail": stats["status_detail"],
            "p1": fmt(stats.get("p1")),
            "signed_bias": fmt(stats.get("signed_bias")),
            "abs_bias": fmt(stats.get("abs_bias")),
            "min_entropy": fmt(stats.get("min_entropy")),
            "worst_x": stats.get("worst_x", ""),
            "worst_p1": fmt(stats.get("worst_p1")),
            "worst_abs_bias": fmt(stats.get("worst_abs_bias")),
            "row_ones_mean": fmt(stats.get("row_ones_mean"), 6),
            "row_ones_std": fmt(stats.get("row_ones_std"), 6),
            "raw_bytes": stats.get("raw_bytes", ""),
            "payload_bytes": stats.get("payload_bytes", ""),
            "header_ok": stats.get("header_ok", ""),
            "restart_count": restart_count,
            "row_bytes": row_bytes,
            "file": rel(path),
            "metadata_file": rel(meta_path) if meta_path.exists() else "",
            "output_sha256": str(meta.get("output_sha256") or sha256_file(path)),
            "bitstream": str(meta.get("bitstream", "")),
            "bitstream_sha256": str(meta.get("bitstream_sha256", "")),
            "capture_start_time": str(meta.get("start_time", "")),
            "date_tag": fields["date_tag"],
        }
        rows[(context, anchor, implementation)] = row
    return rows


def build_capture_rows(run_dir: Path) -> list[dict[str, Any]]:
    observed = discover_captures(run_dir / "raw", run_dir / "metadata")
    rows = []
    for expected in expected_rows():
        key = (expected["context"], expected["anchor"], expected["implementation"])
        if key in observed:
            rows.append(observed[key])
            continue
        rows.append(
            {
                **expected,
                "status": "missing",
                "status_detail": "expected raw capture not found",
                "p1": "",
                "signed_bias": "",
                "abs_bias": "",
                "min_entropy": "",
                "worst_x": "",
                "worst_p1": "",
                "worst_abs_bias": "",
                "row_ones_mean": "",
                "row_ones_std": "",
                "raw_bytes": "",
                "payload_bytes": "",
                "header_ok": "",
                "restart_count": RESTART_COUNT,
                "row_bytes": ROW_BYTES,
                "file": rel(
                    run_dir
                    / "raw"
                    / (
                        f"restart_toolflow_random1_{expected['context']}_warmup10_"
                        f"{expected['anchor']}_{expected['implementation']}_run01_"
                        f"1000x125_strict_{DATE_TAG}.bin"
                    )
                ),
                "metadata_file": "",
                "output_sha256": "",
                "bitstream": "",
                "bitstream_sha256": "",
                "capture_start_time": "",
                "date_tag": DATE_TAG,
            }
        )
    return rows


def route_summary_by_label(route_dir: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(route_dir / "sample_ro_route_evidence_summary_20260528.csv")
    return {row.get("label", ""): row for row in rows}


def pair_summary(route_dir: Path, label_a: str, label_b: str) -> dict[str, Any]:
    stem = f"{label_a}_vs_{label_b}"
    cell_rows = read_csv(route_dir / f"{stem}_cell_diff_20260528.csv")
    net_rows = read_csv(route_dir / f"{stem}_net_diff_20260528.csv")
    delay_rows = []
    md_path = route_dir / "sample_ro_route_evidence_summary_20260528.md"
    if md_path.exists():
        delay_rows = parse_delay_rows_from_md(md_path, label_a, label_b)

    def count_cell(group: str, field: str) -> int:
        return sum(row.get("group") == group and row.get(field) == "True" for row in cell_rows)

    def count_net(group: str) -> int:
        return sum(row.get("group") == group and row.get("route_changed") == "True" for row in net_rows)

    def delay_delta(group: str) -> str:
        for row in delay_rows:
            if row.get("group") == group:
                return row.get("mean_delta_b_minus_a", "")
        return ""

    return {
        "label_a": label_a,
        "label_b": label_b,
        "route_pair_present": bool(cell_rows or net_rows),
        "sample_ro_loc_changed": count_cell("sample_ro", "loc_changed"),
        "sample_ro_bel_changed": count_cell("sample_ro", "bel_changed"),
        "sample_ro_route_changed": count_net("sample_ro_net"),
        "sampled_data_loc_changed": count_cell("sampled_data_regs", "loc_changed"),
        "sampled_data_bel_changed": count_cell("sampled_data_regs", "bel_changed"),
        "sampled_data_route_changed": count_net("sampled_data_net"),
        "data_ro_loc_changed": count_cell("data_ro", "loc_changed"),
        "data_ro_bel_changed": count_cell("data_ro", "bel_changed"),
        "data_ro_route_changed": count_net("data_ro_net"),
        "sample_ro_delay_mean_delta_ps": delay_delta("sample_ro_net"),
        "sampled_data_delay_mean_delta_ps": delay_delta("sampled_data_net"),
        "data_ro_delay_mean_delta_ps": delay_delta("data_ro_net"),
    }


def parse_delay_rows_from_md(path: Path, label_a: str, label_b: str) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    header = f"## Pair `{label_a}` vs `{label_b}`"
    start = text.find(header)
    if start < 0:
        return []
    next_start = text.find("\n## Pair `", start + len(header))
    section = text[start : next_start if next_start >= 0 else len(text)]
    marker = "### Net Delay Summary"
    marker_pos = section.find(marker)
    if marker_pos < 0:
        return []
    table = section[marker_pos:].splitlines()
    rows = []
    fields: list[str] = []
    for line in table:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not fields:
            fields = cells
            continue
        if set(cells) == {"---"}:
            continue
        if len(cells) == len(fields):
            rows.append(dict(zip(fields, cells)))
    return rows


def movement_class(pair: dict[str, Any]) -> str:
    if not pair.get("route_pair_present"):
        return "missing_route"
    sample_changed = int(pair.get("sample_ro_route_changed") or 0) > 0
    data_changed = int(pair.get("data_ro_route_changed") or 0) > 0
    sampled_changed = int(pair.get("sampled_data_route_changed") or 0) > 0
    if sample_changed and (data_changed or sampled_changed):
        return "broad_route_shift"
    if sample_changed:
        return "sampler_route_shift"
    if data_changed or sampled_changed:
        return "data_route_shift"
    return "no_route_shift"


def build_matrix_rows(capture_rows: list[dict[str, Any]], route_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    captures = {
        (row["context"], row["anchor"], row["implementation"]): row
        for row in capture_rows
    }
    route_by_label = route_summary_by_label(route_dir)
    rows = []
    route_rows = []
    for context, context_label in CONTEXTS:
        for anchor, _kind, _index in ANCHORS:
            orig = captures[(context, anchor, "original")]
            explore = captures[(context, anchor, "explore1")]
            label_a = f"{context_label}_{anchor}_original"
            label_b = f"{context_label}_{anchor}_explore1"
            pair = pair_summary(route_dir, label_a, label_b)
            pair["context"] = context
            pair["context_label"] = context_label
            pair["anchor"] = anchor
            pair["movement_class"] = movement_class(pair)
            route_rows.append(pair)

            orig_p1 = to_float(orig.get("p1"))
            exp_p1 = to_float(explore.get("p1"))
            orig_abs = to_float(orig.get("abs_bias"))
            exp_abs = to_float(explore.get("abs_bias"))
            delta_p1 = None if orig_p1 is None or exp_p1 is None else exp_p1 - orig_p1
            delta_abs = None if orig_abs is None or exp_abs is None else exp_abs - orig_abs
            rows.append(
                {
                    "context": context,
                    "context_label": context_label,
                    "anchor": anchor,
                    "original_status": orig.get("status", ""),
                    "explore1_status": explore.get("status", ""),
                    "original_p1": orig.get("p1", ""),
                    "explore1_p1": explore.get("p1", ""),
                    "delta_p1_explore1_minus_original": fmt(delta_p1),
                    "original_abs_bias": orig.get("abs_bias", ""),
                    "explore1_abs_bias": explore.get("abs_bias", ""),
                    "delta_abs_bias_explore1_minus_original": fmt(delta_abs),
                    "original_min_entropy": orig.get("min_entropy", ""),
                    "explore1_min_entropy": explore.get("min_entropy", ""),
                    "original_worst_x": orig.get("worst_x", ""),
                    "explore1_worst_x": explore.get("worst_x", ""),
                    "original_bitstream_sha256": orig.get("bitstream_sha256", ""),
                    "explore1_bitstream_sha256": explore.get("bitstream_sha256", ""),
                    "original_route_rows_present": label_a in route_by_label,
                    "explore1_route_rows_present": label_b in route_by_label,
                    "route_pair_present": pair["route_pair_present"],
                    "movement_class": pair["movement_class"],
                    "sample_ro_route_changed": pair["sample_ro_route_changed"],
                    "sampled_data_route_changed": pair["sampled_data_route_changed"],
                    "data_ro_route_changed": pair["data_ro_route_changed"],
                    "sample_ro_delay_mean_delta_ps": pair["sample_ro_delay_mean_delta_ps"],
                    "sampled_data_delay_mean_delta_ps": pair["sampled_data_delay_mean_delta_ps"],
                    "data_ro_delay_mean_delta_ps": pair["data_ro_delay_mean_delta_ps"],
                }
            )
    return rows, route_rows


def build_missing_manifest(capture_rows: list[dict[str, Any]], matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in capture_rows:
        if row.get("status") != "ok":
            rows.append(
                {
                    "item_type": "capture",
                    "context": row.get("context", ""),
                    "anchor": row.get("anchor", ""),
                    "implementation": row.get("implementation", ""),
                    "status": row.get("status", ""),
                    "detail": row.get("status_detail", ""),
                    "path": row.get("file", ""),
                }
            )
    for row in matrix_rows:
        if not row.get("route_pair_present"):
            rows.append(
                {
                    "item_type": "route_pair",
                    "context": row.get("context", ""),
                    "anchor": row.get("anchor", ""),
                    "implementation": "original_vs_explore1",
                    "status": "missing",
                    "detail": "route pair diff not found",
                    "path": "",
                }
            )
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return lines


def write_markdown(path: Path, capture_rows: list[dict[str, Any]], matrix_rows: list[dict[str, Any]], missing_rows: list[dict[str, Any]]) -> None:
    ok = sum(row.get("status") == "ok" for row in capture_rows)
    invalid = sum(str(row.get("status", "")).startswith("invalid") for row in capture_rows)
    route_pairs = sum(bool(row.get("route_pair_present")) for row in matrix_rows)
    fields = [
        "context_label",
        "anchor",
        "original_status",
        "explore1_status",
        "original_p1",
        "explore1_p1",
        "delta_abs_bias_explore1_minus_original",
        "movement_class",
        "sample_ro_route_changed",
        "data_ro_route_changed",
    ]
    lines = [
        "# TVLSI Toolflow Sensitivity Matrix 20260531",
        "",
        "This summary joins the original and Explore/Explore/Explore directive builds for the two held-out sampler contexts. PVT rows are logged for traceability but are not used as covariates.",
        "",
        "## Coverage",
        "",
        f"- Valid captures: {ok}/12.",
        f"- Missing captures: {sum(row.get('status') == 'missing' for row in capture_rows)}/12.",
        f"- Invalid captures: {invalid}/12.",
        f"- Route pair diffs: {route_pairs}/6 original-vs-explore1 pairs.",
        "",
        "## Matrix",
        "",
        *md_table(matrix_rows, fields),
        "",
        "## Interpretation Boundary",
        "",
        "A stable bias under changed directives supports sampler-aperture robustness, while large bias movement with broad route changes bounds the mechanism claim to a placed/routed physical context. Missing route or capture rows are reported explicitly and are not interpolated.",
        "",
    ]
    if missing_rows:
        lines.extend(
            [
                "## Missing Or Invalid Items",
                "",
                *md_table(missing_rows, ["item_type", "context", "anchor", "implementation", "status", "detail"]),
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--route-dir", type=Path, default=DEFAULT_ROUTE_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    capture_rows = build_capture_rows(args.run_dir)
    matrix_rows, route_rows = build_matrix_rows(capture_rows, args.route_dir)
    missing_rows = build_missing_manifest(capture_rows, matrix_rows)

    capture_fields = [
        "board",
        "context",
        "context_label",
        "warmup",
        "run_id",
        "anchor",
        "kind",
        "index",
        "implementation",
        "directive_tag",
        "place_directive",
        "phys_opt_directive",
        "route_directive",
        "route_label",
        "status",
        "status_detail",
        "p1",
        "signed_bias",
        "abs_bias",
        "min_entropy",
        "worst_x",
        "worst_p1",
        "worst_abs_bias",
        "row_ones_mean",
        "row_ones_std",
        "raw_bytes",
        "payload_bytes",
        "header_ok",
        "restart_count",
        "row_bytes",
        "file",
        "metadata_file",
        "output_sha256",
        "bitstream",
        "bitstream_sha256",
        "capture_start_time",
        "date_tag",
    ]
    matrix_fields = sorted({key for row in matrix_rows for key in row})
    route_fields = sorted({key for row in route_rows for key in row})
    missing_fields = ["item_type", "context", "anchor", "implementation", "status", "detail", "path"]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "toolflow_capture_metrics.csv", capture_rows, capture_fields)
    write_csv(args.out_dir / "toolflow_sensitivity_matrix.csv", matrix_rows, matrix_fields)
    write_csv(args.out_dir / "route_overlap_vs_bias_shift.csv", matrix_rows, matrix_fields)
    write_csv(args.out_dir / "toolflow_route_pair_diff_summary.csv", route_rows, route_fields)
    write_csv(args.out_dir / "missing_manifest.csv", missing_rows, missing_fields)
    write_markdown(args.out_dir / "toolflow_sensitivity_summary.md", capture_rows, matrix_rows, missing_rows)

    print(f"Wrote {args.out_dir / 'toolflow_sensitivity_matrix.csv'}")
    print(f"Wrote {args.out_dir / 'toolflow_route_pair_diff_summary.csv'}")
    print(f"Wrote {args.out_dir / 'toolflow_sensitivity_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
