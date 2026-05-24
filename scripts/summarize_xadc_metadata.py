#!/usr/bin/env python3
"""Summarize XADC before/after readings stored in capture metadata."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


RAILS = ("vccint_v", "vccaux_v", "vccbram_v", "vpvn_v")


def as_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rel_or_abs(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def extract_xadc(prefix: str, meta: dict[str, Any]) -> dict[str, Any]:
    block = meta.get(f"xadc_{prefix}")
    if isinstance(block, list):
        dict_items = [item for item in block if isinstance(item, dict)]
        block = dict_items[-1] if dict_items else {}
    if not isinstance(block, dict):
        block = {}
    return {
        f"xadc_{prefix}_status": as_str(block.get("status")),
        f"xadc_{prefix}_timestamp": as_str(block.get("timestamp")),
        f"xadc_{prefix}_temperature_c": as_str(block.get("temperature_c")),
        f"xadc_{prefix}_vccint_v": as_str(block.get("vccint_v")),
        f"xadc_{prefix}_vccaux_v": as_str(block.get("vccaux_v")),
        f"xadc_{prefix}_vccbram_v": as_str(block.get("vccbram_v")),
        f"xadc_{prefix}_vpvn_v": as_str(block.get("vpvn_v")),
        f"xadc_{prefix}_error": as_str(block.get("error")),
    }


def delta(after: Any, before: Any) -> str:
    a = as_float(after)
    b = as_float(before)
    if a is None or b is None:
        return ""
    return f"{a - b:.6g}"


def classify_xadc(row: dict[str, str]) -> str:
    before = row["xadc_before_status"]
    after = row["xadc_after_status"]
    if before == "ok" and after == "ok":
        return "ok"
    if before or after:
        return "partial_or_failed"
    return "missing"


def row_from_metadata(repo_root: Path, meta_path: Path) -> dict[str, str]:
    meta = read_json(meta_path)
    output_file = as_str(meta.get("output_file"))
    output_path = rel_or_abs(repo_root, output_file) if output_file else None
    file_bytes = output_path.stat().st_size if output_path and output_path.exists() else ""

    row: dict[str, str] = {
        "metadata_file": str(meta_path),
        "capture_id": as_str(meta.get("capture_id") or meta_path.stem),
        "board_id": as_str(meta.get("board_id")),
        "kind": as_str(meta.get("kind")),
        "output_file": output_file,
        "file_bytes": str(file_bytes),
        "bytes_requested": as_str(meta.get("bytes_requested")),
        "bytes_captured": as_str(meta.get("bytes_captured")),
        "start_time": as_str(meta.get("start_time")),
        "end_time": as_str(meta.get("end_time")),
        "duration_seconds": as_str(meta.get("duration_seconds")),
        "uart_port": as_str(meta.get("uart_port")),
        "baud": as_str(meta.get("baud")),
        "bitstream": as_str(meta.get("bitstream")),
        "sha256": as_str(meta.get("sha256")).upper(),
        "legacy_fpga_temperature_c": as_str(meta.get("fpga_temperature_c")),
        "legacy_voltage_condition": as_str(meta.get("voltage_condition")),
        "xadc_csv": as_str(meta.get("xadc_csv")),
    }
    row.update(extract_xadc("before", meta))
    row.update(extract_xadc("after", meta))

    row["xadc_status"] = classify_xadc(row)
    row["temperature_delta_c"] = delta(
        row["xadc_after_temperature_c"], row["xadc_before_temperature_c"]
    )
    for rail in RAILS:
        row[f"{rail}_delta"] = delta(row[f"xadc_after_{rail}"], row[f"xadc_before_{rail}"])
    return row


def collect_rows(repo_root: Path, metadata_roots: list[Path]) -> list[dict[str, str]]:
    paths: list[Path] = []
    for root in metadata_roots:
        resolved = rel_or_abs(repo_root, str(root))
        if resolved.is_file() and resolved.suffix.lower() == ".json":
            paths.append(resolved)
        elif resolved.exists():
            paths.extend(sorted(resolved.rglob("*.json")))
    rows = []
    for path in sorted(set(paths)):
        try:
            rows.append(row_from_metadata(repo_root, path))
        except Exception as exc:  # keep one bad metadata file from hiding the rest
            rows.append(
                {
                    "metadata_file": str(path),
                    "capture_id": path.stem,
                    "xadc_status": "metadata_parse_failed",
                    "xadc_before_error": str(exc),
                }
            )
    return rows


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


def fmt_stat(values: list[float]) -> str:
    if not values:
        return ""
    return f"min={min(values):.4g}, mean={mean(values):.4g}, max={max(values):.4g}"


def write_markdown(path: Path, rows: list[dict[str, str]], csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.get("xadc_status", "")] = counts.get(row.get("xadc_status", ""), 0) + 1

    ok_rows = [row for row in rows if row.get("xadc_status") == "ok"]
    temp_before = [
        value
        for row in ok_rows
        if (value := as_float(row.get("xadc_before_temperature_c"))) is not None
    ]
    temp_after = [
        value
        for row in ok_rows
        if (value := as_float(row.get("xadc_after_temperature_c"))) is not None
    ]
    temp_delta = [
        value
        for row in ok_rows
        if (value := as_float(row.get("temperature_delta_c"))) is not None
    ]

    columns = [
        "capture_id",
        "board_id",
        "kind",
        "xadc_status",
        "xadc_before_temperature_c",
        "xadc_after_temperature_c",
        "temperature_delta_c",
        "xadc_after_vccint_v",
        "xadc_after_vccaux_v",
        "xadc_after_vccbram_v",
    ]

    with path.open("w", encoding="utf-8") as f:
        f.write("# XADC Capture Summary\n\n")
        f.write(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- CSV: `{csv_path}`\n")
        f.write(f"- Metadata files scanned: {len(rows)}\n")
        f.write(f"- Status counts: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}\n")
        f.write(f"- Before die temperature C: {fmt_stat(temp_before)}\n")
        f.write(f"- After die temperature C: {fmt_stat(temp_after)}\n")
        f.write(f"- Temperature delta C: {fmt_stat(temp_delta)}\n\n")
        f.write("## Recent Rows\n\n")
        f.write("| " + " | ".join(columns) + " |\n")
        f.write("| " + " | ".join(["---"] * len(columns)) + " |\n")
        for row in rows[-40:]:
            f.write("| " + " | ".join(row.get(col, "") for col in columns) + " |\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--metadata-root",
        type=Path,
        action="append",
        default=[Path("data/hardware")],
        help="Directory or metadata JSON to scan. Can be repeated.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/experiments/xadc_summary"),
        help="Output directory for CSV and Markdown summary.",
    )
    parser.add_argument("--tag", default=datetime.now().strftime("%Y%m%d"))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    out_dir = rel_or_abs(repo_root, str(args.out_dir))
    rows = collect_rows(repo_root, args.metadata_root)
    csv_path = out_dir / f"xadc_capture_summary_{args.tag}.csv"
    md_path = out_dir / f"xadc_capture_summary_{args.tag}.md"
    write_csv(csv_path, rows)
    write_markdown(md_path, rows, csv_path)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
