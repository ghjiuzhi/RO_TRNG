#!/usr/bin/env python3
"""Summarize completed TRNG formal/repeat captures for paper tables."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


BASE_DIR = Path("data/hardware/20260511_fpga1_board1")
METADATA_DIR = BASE_DIR / "metadata"
TRNG_DIR = BASE_DIR / "trng"

RUN_RE = re.compile(r"^(?P<placement>.+)_run(?P<idx>\d+)$")
REPEAT_RE = re.compile(r"^(?P<placement>.+)_repeat(?P<idx>\d+)(?:_(?P<size>5mib|10mib|20mib))?$")

RUN_COLUMNS = [
    "run",
    "placement",
    "sample_role",
    "formal_or_repeat",
    "bytes",
    "p1",
    "abs_bias",
    "bit_min_entropy",
    "monobit_p",
    "runs_p",
    "adjacent_equal_ratio",
    "byte_min_entropy",
    "sha256",
    "valid",
]

METRIC_COLUMNS = [
    "bytes",
    "p1",
    "abs_bias",
    "bit_min_entropy",
    "monobit_p",
    "runs_p",
    "adjacent_equal_ratio",
    "byte_min_entropy",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_summary_rows(trng_dir: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for csv_path in sorted(trng_dir.glob("analysis_*/trng_summary.csv")):
        with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = Path(row.get("name") or row.get("file") or "").stem
                if name:
                    rows[name] = row
    return rows


def classify_capture(capture_id: str) -> tuple[str | None, str | None, str]:
    match = RUN_RE.match(capture_id)
    if match:
        return match.group("placement"), "formal", ""
    match = REPEAT_RE.match(capture_id)
    if match:
        return match.group("placement"), "repeat", ""
    return None, None, "not a formal/repeat capture id"


def to_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else math.nan


def complete_reason(meta: dict[str, Any]) -> str:
    requested = meta.get("bytes_requested")
    captured = meta.get("bytes_captured")
    if requested is None or captured is None:
        return "missing byte count"
    if int(requested) != int(captured):
        return f"partial capture: {captured}/{requested} bytes"
    return ""


def build_rows(metadata_dir: Path, trng_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summaries = load_summary_rows(trng_dir)
    valid_rows: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for meta_path in sorted(metadata_dir.glob("*.json")):
        meta = load_json(meta_path)
        if meta.get("kind") != "trng":
            excluded.append(
                {
                    "run": meta.get("capture_id", meta_path.stem),
                    "placement": "",
                    "sample_role": "",
                    "bytes": meta.get("bytes_captured", ""),
                    "reason": "metadata kind is not trng",
                }
            )
            continue

        capture_id = str(meta.get("capture_id") or meta_path.stem)
        placement, role, reason = classify_capture(capture_id)
        completeness = complete_reason(meta)
        summary = summaries.get(capture_id)
        if summary is None:
            reason = reason or "missing trng_summary.csv row"
        if completeness:
            reason = reason or completeness

        if reason:
            excluded.append(
                {
                    "run": capture_id,
                    "placement": placement or "",
                    "sample_role": role or "",
                    "bytes": meta.get("bytes_captured", ""),
                    "reason": reason,
                }
            )
            continue

        assert placement is not None
        assert role is not None
        p1 = to_float(summary, "p1")
        row = {
            "run": capture_id,
            "placement": placement,
            "sample_role": role,
            "formal_or_repeat": role,
            "bytes": int(float(summary["bytes"])),
            "p1": p1,
            "abs_bias": abs(p1 - 0.5),
            "bit_min_entropy": to_float(summary, "bit_min_entropy"),
            "monobit_p": to_float(summary, "monobit_p"),
            "runs_p": to_float(summary, "runs_p"),
            "adjacent_equal_ratio": to_float(summary, "adjacent_equal_ratio"),
            "byte_min_entropy": to_float(summary, "min_entropy_byte"),
            "sha256": str(meta.get("sha256", "")),
            "valid": True,
        }
        valid_rows.append(row)

    valid_rows.sort(key=lambda r: (str(r["placement"]), str(r["sample_role"]), str(r["run"])))
    return valid_rows, excluded


def mean_std(values: list[float]) -> tuple[float, float]:
    clean = [value for value in values if not math.isnan(value)]
    if not clean:
        return math.nan, math.nan
    mean = sum(clean) / len(clean)
    if len(clean) == 1:
        return mean, math.nan
    var = sum((value - mean) ** 2 for value in clean) / (len(clean) - 1)
    return mean, math.sqrt(var)


def build_placement_rows(run_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[(str(row["placement"]), str(row["sample_role"]), int(row["bytes"]))].append(row)

    out_rows: list[dict[str, Any]] = []
    for (placement, role, target_bytes), rows in sorted(grouped.items()):
        out: dict[str, Any] = {
            "placement": placement,
            "sample_role": role,
            "formal_or_repeat": role,
            "target_bytes": target_bytes,
            "n": len(rows),
        }
        for key in METRIC_COLUMNS:
            mean, std = mean_std([float(row[key]) for row in rows])
            out[f"{key}_mean"] = mean
            out[f"{key}_std"] = std
        out_rows.append(out)
    return out_rows


def format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_value(row.get(key, "")) for key in columns})


def write_markdown_table(f, rows: list[dict[str, Any]], columns: list[str]) -> None:
    f.write("| " + " | ".join(columns) + " |\n")
    f.write("| " + " | ".join(["---"] * len(columns)) + " |\n")
    for row in rows:
        cells = [format_value(row.get(key, "")) for key in columns]
        f.write("| " + " | ".join(cells) + " |\n")


def write_run_markdown(path: Path, rows: list[dict[str, Any]], excluded: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("# TRNG Repeats by Run\n\n")
        f.write("Complete formal/repeat captures only.\n\n")
        write_markdown_table(f, rows, RUN_COLUMNS)
        if excluded:
            f.write("\n## Excluded captures\n\n")
            write_markdown_table(f, excluded, ["run", "placement", "sample_role", "bytes", "reason"])


def write_placement_markdown(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("# TRNG Repeats by Placement\n\n")
        f.write("Aggregates include complete formal/repeat captures recognized by metadata and analysis summaries.\n\n")
        write_markdown_table(f, rows, columns)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-dir", type=Path, default=METADATA_DIR)
    parser.add_argument("--trng-dir", type=Path, default=TRNG_DIR)
    args = parser.parse_args()

    run_rows, excluded = build_rows(args.metadata_dir, args.trng_dir)
    placement_rows = build_placement_rows(run_rows)

    placement_columns = ["placement", "sample_role", "formal_or_repeat", "target_bytes", "n"]
    for key in METRIC_COLUMNS:
        placement_columns.extend([f"{key}_mean", f"{key}_std"])

    run_csv = args.trng_dir / "trng_repeats_by_run.csv"
    run_md = args.trng_dir / "trng_repeats_by_run.md"
    placement_csv = args.trng_dir / "trng_repeats_by_placement.csv"
    placement_md = args.trng_dir / "trng_repeats_by_placement.md"

    write_csv(run_csv, run_rows, RUN_COLUMNS)
    write_run_markdown(run_md, run_rows, excluded)
    write_csv(placement_csv, placement_rows, placement_columns)
    write_placement_markdown(placement_md, placement_rows, placement_columns)

    print(f"Wrote {run_csv}")
    print(f"Wrote {run_md}")
    print(f"Wrote {placement_csv}")
    print(f"Wrote {placement_md}")
    print(f"Included {len(run_rows)} captures; excluded {len(excluded)} captures.")


if __name__ == "__main__":
    main()
