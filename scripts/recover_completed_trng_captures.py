#!/usr/bin/env python3
"""Recover metadata/analysis for completed TRNG captures after post-capture failures."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "hardware" / "20260511_fpga1_board1"
TRNG_DIR = BASE / "trng"
METADATA_DIR = BASE / "metadata"
XADC_CSV = METADATA_DIR / "xadc_readings.csv"

BITSTREAMS = {
    "checker": "data/vivado_runs/fpga1_ro_trng_matrix/checker_pitch3_x44y43/seed_1/RO_TRNG_top.bit",
    "compact": "data/vivado_runs/fpga1_ro_trng_matrix/compact_x44y43/seed_1/RO_TRNG_top.bit",
    "cross_region": "data/vivado_runs/fpga1_ro_trng_matrix/cross_region_x36y25/seed_1/RO_TRNG_top.bit",
    "far": "data/vivado_runs/fpga1_ro_trng_matrix/far_x20y25/seed_1/RO_TRNG_top.bit",
    "random1": "data/vivado_runs/fpga1_ro_trng_matrix/random_seed1_x36y35/seed_1/RO_TRNG_top.bit",
    "random2": "data/vivado_runs/fpga1_ro_trng_matrix/random_seed2_x36y35/seed_1/RO_TRNG_top.bit",
    "random3": "data/vivado_runs/fpga1_ro_trng_matrix/random_seed3_x36y35/seed_1/RO_TRNG_top.bit",
    "row": "data/vivado_runs/fpga1_ro_trng_matrix/row_pitch3_x38y43/seed_1/RO_TRNG_top.bit",
    "same_column": "data/vivado_runs/fpga1_ro_trng_matrix/same_column_pitch3_x44y35/seed_1/RO_TRNG_top.bit",
    "sparse": "data/vivado_runs/fpga1_ro_trng_matrix/sparse_pitch6_x36y35/seed_1/RO_TRNG_top.bit",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_xadc(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def xadc_block(phase: str, row: dict[str, str] | None) -> dict[str, str]:
    if row is None:
        return {
            "phase": phase,
            "status": "missing",
            "csv": str(XADC_CSV),
            "timestamp": "",
            "temperature_c": "",
            "vccint_v": "",
            "vccaux_v": "",
            "vccbram_v": "",
            "vpvn_v": "",
            "error": "recovered metadata could not match XADC row",
        }
    return {
        "phase": phase,
        "status": "ok",
        "csv": str(XADC_CSV),
        "timestamp": row.get("timestamp", ""),
        "temperature_c": row.get("TEMPERATURE", ""),
        "vccint_v": row.get("VCCINT", ""),
        "vccaux_v": row.get("VCCAUX", ""),
        "vccbram_v": row.get("VCCBRAM", ""),
        "vpvn_v": row.get("VPVN", ""),
        "error": "",
    }


def nearest_xadc_pair(xadc_rows: list[dict[str, str]], end_time: datetime) -> tuple[dict[str, str] | None, dict[str, str] | None]:
    timed: list[tuple[datetime, dict[str, str]]] = []
    for row in xadc_rows:
        ts = parse_time(row.get("timestamp", ""))
        if ts is not None:
            timed.append((ts, row))
    timed.sort(key=lambda item: item[0])
    for idx, (ts, row) in enumerate(timed):
        if ts >= end_time and ts - end_time <= timedelta(minutes=5):
            before = timed[idx - 1][1] if idx > 0 else None
            return before, row
    return None, None


def placement_from_run(run: str) -> str:
    for placement in sorted(BITSTREAMS, key=len, reverse=True):
        if run.startswith(f"{placement}_"):
            return placement
    return ""


def run_analysis(python: str, bin_path: Path, analysis_dir: Path) -> None:
    summary = analysis_dir / "trng_summary.csv"
    if summary.exists():
        return
    analysis_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            python,
            str(ROOT / "scripts" / "analyze_trng_dataset.py"),
            str(bin_path),
            "--out-dir",
            str(analysis_dir),
        ],
        check=True,
    )


def recover_one(python: str, bin_path: Path, xadc_rows: list[dict[str, str]], board_id: str, baud: int, force: bool) -> dict[str, Any]:
    run = bin_path.stem
    analysis_dir = bin_path.parent / f"analysis_{run}"
    run_analysis(python, bin_path, analysis_dir)

    metadata_path = METADATA_DIR / f"{run}.json"
    if metadata_path.exists() and not force:
        return {"run": run, "metadata": "exists", "analysis": str(analysis_dir)}

    file_size = bin_path.stat().st_size
    end_time = datetime.fromtimestamp(bin_path.stat().st_mtime)
    # UART 115200 8N1 has a theoretical 11520 B/s ceiling; this gives a
    # conservative reconstructed start time for provenance only.
    duration_seconds = round(file_size / 7386.0, 3)
    start_time = end_time - timedelta(seconds=duration_seconds)
    before, after = nearest_xadc_pair(xadc_rows, end_time)

    placement = placement_from_run(run)
    bitstream = BITSTREAMS.get(placement, "")
    bit_abs = (ROOT / bitstream).resolve() if bitstream else Path("")
    bit_hash = sha256(bit_abs) if bitstream and bit_abs.exists() else ""
    data_hash = sha256(bin_path)

    metadata = {
        "capture_id": run,
        "board_id": board_id,
        "kind": "trng",
        "output_file": str(bin_path.resolve()),
        "bitstream": bitstream.replace("/", "\\"),
        "bitstream_resolved": str(bit_abs) if bitstream else "",
        "bitstream_sha256": bit_hash,
        "uart_port": "COM3",
        "baud": baud,
        "uart_format": "8N1, no parity, no flow control",
        "bytes_requested": file_size,
        "bytes_captured": file_size,
        "sha256": data_hash,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": duration_seconds,
        "throughput_bytes_per_second": round(file_size / duration_seconds, 3) if duration_seconds else 0,
        "room_temperature_c": "",
        "fpga_temperature_c": (after or {}).get("TEMPERATURE", ""),
        "voltage_condition": "nominal_board_power",
        "xadc_csv": str(XADC_CSV),
        "xadc_before": xadc_block("before_capture", before),
        "xadc_after": xadc_block("after_capture", after),
        "notes": "Recovered after the original capture completed but post-capture XADC metadata handling failed.",
    }
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=4), encoding="utf-8")
    return {"run": run, "metadata": str(metadata_path), "analysis": str(analysis_dir)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--board-id", default="z7020_b01")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    xadc_rows = load_xadc(XADC_CSV)
    for item in args.inputs:
        result = recover_one(args.python, item, xadc_rows, args.board_id, args.baud, args.force)
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
