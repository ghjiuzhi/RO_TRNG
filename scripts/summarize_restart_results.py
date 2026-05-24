#!/usr/bin/env python3
"""Build a paper-facing summary table for SP800-90B restart experiments."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


HI_RE = re.compile(r"H_I:\s*([0-9.]+)")
XCUTOFF_RE = re.compile(r"X_cutoff:\s*([0-9]+)")
XMAX_RE = re.compile(r"X_max:\s*([0-9]+)")
MIN_RE = re.compile(r"min\(H_r,\s*H_c,\s*H_I\):\s*([0-9.]+)")
HR_RE = re.compile(r"H_r:\s*([0-9.]+)")
HC_RE = re.compile(r"H_c:\s*([0-9.]+)")


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def as_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def rel_or_abs(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_ea_stdout(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    status = "passed" if "Validation Test Passed" in text else ""
    if "Restart Sanity Check Failed" in text:
        status = "failed"
    if not status:
        status = "error"

    def one(regex: re.Pattern[str]) -> str:
        match = regex.search(text)
        return match.group(1) if match else ""

    return {
        "ea_status": status,
        "h_i": one(HI_RE),
        "h_r": one(HR_RE),
        "h_c": one(HC_RE),
        "x_cutoff": one(XCUTOFF_RE),
        "x_max": one(XMAX_RE),
        "min_h": one(MIN_RE),
        "ea_stdout": str(path),
    }


def infer_fields_from_ea_path(path: Path) -> dict[str, str]:
    text = path.as_posix()
    name = path.name
    run = name.removesuffix(".ea_restart.stdout.txt")
    bit_order = "msb" if "_msb" in run else ("lsb" if "_lsb" in run else "")
    placement = ""
    warmup = ""
    repeat = ""
    match = re.search(r"ea_restart_([^/\\]+)_warmup(\d+)(?:_([^/\\]+?))?_(msb|lsb)_\d{8}", text)
    if match:
        placement = match.group(1)
        warmup = match.group(2)
        repeat = match.group(3) or "run01"
        bit_order = match.group(4)
    else:
        match = re.search(r"([^/\\]+)_warmup(\d+)(?:_([^/\\]+?))?_(msb|lsb)_\d{8}", run)
        if match:
            placement = match.group(1)
            warmup = match.group(2)
            repeat = match.group(3) or "run01"
            bit_order = match.group(4)
        elif "random3_header_delay60s" in text:
            placement = "random3"
            warmup = "0"
            repeat = "formal01"
        elif "random1_header_delay60s" in text:
            placement = "random1"
            warmup = "0"
            repeat = "formal01"
    return {
        "placement": placement,
        "warmup_bytes": warmup,
        "repeat_tag": repeat,
        "bit_order": bit_order,
        "ea_run": run,
    }


def find_column_summary(
    artifact_root: Path, placement: str, warmup: str, repeat: str
) -> Path | None:
    candidates = []
    if placement and warmup:
        if repeat:
            candidates.append(
                artifact_root / f"restart_column_bias_{placement}_formal_bits_warmup{warmup}_{repeat}" / "summary.json"
            )
        candidates.append(
            artifact_root / f"restart_column_bias_{placement}_formal_bits_warmup{warmup}" / "summary.json"
        )
    if placement and warmup == "0":
        candidates.append(artifact_root / f"restart_column_bias_{placement}_formal_bits" / "summary.json")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def metadata_for_column_summary(summary: dict[str, Any]) -> Path | None:
    input_file = Path(as_str(summary.get("input_file")))
    if not input_file:
        return None
    candidates = [
        input_file.with_suffix(input_file.suffix + ".metadata.json"),
        input_file.with_suffix(".metadata.json"),
        input_file.parent / f"{input_file.stem}.metadata.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def xadc_fields(meta: dict[str, Any]) -> dict[str, str]:
    before = normalize_xadc_block(meta.get("xadc_before"))
    after = normalize_xadc_block(meta.get("xadc_after"))
    temp_delta = ""
    before_temp = as_float(before.get("temperature_c"))
    after_temp = as_float(after.get("temperature_c"))
    if before_temp is not None and after_temp is not None:
        temp_delta = f"{after_temp - before_temp:.6g}"
    return {
        "board_id": as_str(meta.get("board_id")),
        "xadc_status": "ok"
        if before.get("status") == "ok" and after.get("status") == "ok"
        else ("missing" if not before and not after else "partial_or_failed"),
        "xadc_before_temperature_c": as_str(before.get("temperature_c")),
        "xadc_after_temperature_c": as_str(after.get("temperature_c")),
        "xadc_temperature_delta_c": temp_delta,
        "xadc_after_vccint_v": as_str(after.get("vccint_v")),
        "xadc_after_vccaux_v": as_str(after.get("vccaux_v")),
        "xadc_after_vccbram_v": as_str(after.get("vccbram_v")),
        "capture_start_time": as_str(meta.get("start_time")),
        "capture_end_time": as_str(meta.get("end_time")),
        "capture_output_sha256": as_str(meta.get("output_sha256") or meta.get("sha256")).upper(),
        "capture_metadata": as_str(meta.get("_metadata_file")),
    }


def normalize_xadc_block(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        for item in reversed(value):
            if isinstance(item, dict) and (
                "temperature_c" in item or "status" in item or "vccint_v" in item
            ):
                return item
    return {}


def build_row(repo_root: Path, artifact_root: Path, ea_stdout: Path) -> dict[str, str]:
    row = infer_fields_from_ea_path(ea_stdout)
    row.update(parse_ea_stdout(ea_stdout))

    column_path = find_column_summary(
        artifact_root, row["placement"], row["warmup_bytes"], row["repeat_tag"]
    )
    if column_path:
        col = read_json(column_path)
        worst = col.get("worst_position") if isinstance(col.get("worst_position"), dict) else {}
        row.update(
            {
                "column_summary": str(column_path),
                "overall_p1": as_str(col.get("overall_p1")),
                "row_ones_mean": as_str(col.get("row_ones_mean")),
                "row_ones_std": as_str(col.get("row_ones_std")),
                "positions_over_x_cutoff": as_str(col.get("positions_over_x_cutoff")),
                "worst_byte_index": as_str(worst.get("byte_index")),
                "worst_bit_index": as_str(worst.get("bit_index")),
                "worst_ones": as_str(worst.get("ones")),
                "worst_zeros": as_str(worst.get("zeros")),
                "worst_p1": as_str(worst.get("p1")),
                "worst_x": as_str(worst.get("x")),
                "worst_msb_expanded_column": as_str(worst.get("msb_expanded_column")),
                "worst_lsb_expanded_column": as_str(worst.get("lsb_expanded_column")),
                "restart_input_file": as_str(col.get("input_file")),
                "restart_input_sha256": as_str(col.get("input_sha256")).upper(),
            }
        )
        meta_path = metadata_for_column_summary(col)
        if meta_path:
            meta = read_json(meta_path)
            meta["_metadata_file"] = str(meta_path)
            row.update(xadc_fields(meta))
    else:
        row["column_summary"] = ""

    row["paper_use"] = "candidate"
    if row.get("ea_status") == "error":
        row["paper_use"] = "debug_only"
    return row


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns: list[str] = []
    seen: set[str] = set()
    preferred = [
        "placement",
        "warmup_bytes",
        "repeat_tag",
        "bit_order",
        "ea_status",
        "h_i",
        "x_cutoff",
        "x_max",
        "h_r",
        "h_c",
        "min_h",
        "overall_p1",
        "positions_over_x_cutoff",
        "worst_byte_index",
        "worst_bit_index",
        "worst_x",
        "worst_msb_expanded_column",
        "worst_lsb_expanded_column",
        "board_id",
        "xadc_status",
        "xadc_before_temperature_c",
        "xadc_after_temperature_c",
        "xadc_temperature_delta_c",
    ]
    for key in preferred:
        seen.add(key)
        columns.append(key)
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]], csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "placement",
        "warmup_bytes",
        "repeat_tag",
        "bit_order",
        "ea_status",
        "h_i",
        "x_cutoff",
        "x_max",
        "min_h",
        "worst_byte_index",
        "worst_bit_index",
        "worst_x",
        "xadc_status",
    ]
    with path.open("w", encoding="utf-8") as f:
        f.write("# Restart Result Summary\n\n")
        f.write(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- CSV: `{csv_path}`\n")
        f.write(f"- Rows: {len(rows)}\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(row.get(col, "") for col in headers) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--restart-root",
        type=Path,
        default=Path("data/hardware/20260511_fpga1_board1/restart"),
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=Path("data/experiments/paper_artifacts_20260515"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/experiments/restart_summary_20260515"),
    )
    parser.add_argument("--tag", default="20260515")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    restart_root = rel_or_abs(repo_root, str(args.restart_root))
    artifact_root = rel_or_abs(repo_root, str(args.artifact_root))
    out_dir = rel_or_abs(repo_root, str(args.out_dir))
    ea_paths = sorted(restart_root.rglob("*.ea_restart.stdout.txt"))
    rows = [build_row(repo_root, artifact_root, path) for path in ea_paths]
    rows.sort(key=lambda r: (r.get("placement", ""), int(r.get("warmup_bytes") or -1), r.get("repeat_tag", ""), r.get("bit_order", "")))

    csv_path = out_dir / f"restart_result_summary_{args.tag}.csv"
    md_path = out_dir / f"restart_result_summary_{args.tag}.md"
    write_csv(csv_path, rows)
    write_md(md_path, rows, csv_path)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
