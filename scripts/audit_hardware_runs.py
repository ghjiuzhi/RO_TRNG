#!/usr/bin/env python3
"""Audit captured FPGA hardware runs and build a paper-facing status table."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def read_csv_first(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return rows[0] if rows else {}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def resolve_path(root: Path, value: str) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    cwd_candidate = Path.cwd() / path
    if cwd_candidate.exists():
        return cwd_candidate
    root_candidate = root / path
    if root_candidate.exists():
        return root_candidate
    return cwd_candidate


def infer_analysis_dir(root: Path, kind: str, run: str) -> Path:
    if kind == "tdc":
        return root / "tdc" / f"analysis_{run}"
    if kind == "trng":
        return root / "trng" / f"analysis_{run}"
    return root / f"analysis_{run}"


def load_metrics(root: Path, kind: str, run: str) -> dict[str, str]:
    analysis = infer_analysis_dir(root, kind, run)
    if kind == "tdc":
        return read_csv_first(analysis / f"{run}.tdc_metrics.csv")
    if kind == "trng":
        return read_csv_first(analysis / "trng_summary.csv")
    return {}


def audit_one(root: Path, meta_path: Path) -> dict[str, str]:
    meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
    run = str(meta.get("capture_id") or meta_path.stem)
    kind = str(meta.get("kind") or "")
    out_path = resolve_path(root, str(meta.get("output_file") or ""))
    bit_path = resolve_path(root, str(meta.get("bitstream_resolved") or meta.get("bitstream") or ""))
    metrics = load_metrics(root, kind, run)

    exists = bool(out_path and out_path.exists())
    file_bytes = out_path.stat().st_size if exists and out_path else 0
    requested = as_int(meta.get("bytes_requested"))
    captured = as_int(meta.get("bytes_captured"), file_bytes)
    duration = as_float(meta.get("duration_seconds"))
    throughput = as_float(meta.get("throughput_bytes_per_second"))
    if throughput == 0.0 and duration > 0.0 and captured:
        throughput = captured / duration
    reasons: list[str] = []
    role = "formal"
    if "smoke" in run.lower():
        role = "smoke"
    elif requested and requested < 1024 * 1024:
        role = "sanity"

    if not exists:
        reasons.append("missing_output_file")
    if exists and file_bytes == 0:
        reasons.append("zero_bytes")
    if requested and file_bytes and file_bytes < requested:
        reasons.append("incomplete_file")
    if requested and captured and captured < requested:
        reasons.append("incomplete_metadata")

    data_sha = str(meta.get("sha256") or "").upper()
    if exists and data_sha and data_sha != sha256_file(out_path):
        reasons.append("sha256_mismatch")

    bit_sha = str(meta.get("bitstream_sha256") or "").upper()
    if bit_path and bit_path.exists():
        actual_bit_sha = sha256_file(bit_path)
        if bit_sha and bit_sha != actual_bit_sha:
            reasons.append("bitstream_sha256_mismatch")
        bit_sha = bit_sha or actual_bit_sha
    elif meta.get("bitstream"):
        reasons.append("missing_bitstream")

    if kind == "tdc":
        packets = as_int(metrics.get("packets"))
        expected_packets = file_bytes // 8
        if expected_packets and packets < int(expected_packets * 0.9):
            reasons.append("tdc_packet_loss_or_bad_framing")
        seq_gaps = as_int(metrics.get("seq_gaps"))
        if packets and (seq_gaps / packets) > 0.001:
            reasons.append("tdc_seq_gap_ratio_gt_0.1pct")
        if not metrics:
            reasons.append("missing_tdc_analysis")
    elif kind == "trng":
        if not metrics:
            reasons.append("missing_trng_analysis")

    valid = "no" if reasons else "yes"
    row = {
        "run": run,
        "kind": kind,
        "valid_for_paper": valid,
        "exclude_reason": ";".join(reasons),
        "bytes_requested": str(requested),
        "bytes_captured": str(captured),
        "file_bytes": str(file_bytes),
        "sample_role": role,
        "duration_seconds": f"{duration:.3f}" if duration else "",
        "throughput_bytes_per_second": f"{throughput:.3f}" if throughput else "",
        "throughput_kib_per_second": f"{throughput / 1024.0:.3f}" if throughput else "",
        "sha256": data_sha,
        "bitstream": str(meta.get("bitstream", "")),
        "bitstream_sha256": bit_sha,
        "start_time": str(meta.get("start_time", "")),
        "end_time": str(meta.get("end_time", "")),
        "uart_port": str(meta.get("uart_port", "")),
        "baud": str(meta.get("baud", "")),
        "room_temperature_c": str(meta.get("room_temperature_c", "")),
        "fpga_temperature_c": str(meta.get("fpga_temperature_c", "")),
        "voltage_condition": str(meta.get("voltage_condition", "")),
    }

    for key in [
        "p1",
        "bit_min_entropy",
        "monobit_p",
        "runs_p",
        "shannon_entropy_byte",
        "min_entropy_byte",
        "packets",
        "seq_gaps",
        "seq_wraps",
        "lane_a_std_phase_ps",
        "lane_b_std_phase_ps",
        "diff_std_ps",
        "phase_pearson_r",
        "lane_a_shannon_bin",
        "lane_b_shannon_bin",
    ]:
        row[key] = metrics.get(key, "")
    return row


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    headers = [
        "run",
        "kind",
        "valid_for_paper",
        "exclude_reason",
        "file_bytes",
        "sample_role",
        "throughput_kib_per_second",
        "p1",
        "bit_min_entropy",
        "packets",
        "seq_gaps",
        "diff_std_ps",
        "phase_pearson_r",
    ]
    with path.open("w", encoding="utf-8") as f:
        f.write("# Hardware Run Audit\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in rows:
            cells = [str(row.get(key, "")).replace("|", "\\|") for key in headers]
            f.write("| " + " | ".join(cells) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="Hardware collection root containing metadata/")
    parser.add_argument("--out-csv", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    meta_dir = root / "metadata"
    metas = sorted(meta_dir.glob("*.json"))
    if not metas:
        raise SystemExit(f"No metadata JSON files found in {meta_dir}")

    rows = [audit_one(root, path) for path in metas]
    out_csv = args.out_csv or (root / "hardware_run_audit.csv")
    out_md = args.out_md or (root / "hardware_run_audit.md")
    write_csv(out_csv, rows)
    write_markdown(out_md, rows)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
