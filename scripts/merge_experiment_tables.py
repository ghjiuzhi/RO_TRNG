#!/usr/bin/env python3
"""Merge TDC, TRNG, RO counter, and placement/Vivado metrics.

Inputs are ordinary CSV files plus optional Vivado run directories.  The merge is
keyed by a run label inferred from common columns, parent directory names, or an
explicit key column.  This keeps paper-table generation reproducible without
adding pandas or other dependencies.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


UTIL_NAMES = {
    "Slice LUTs": "slice_luts",
    "LUT as Logic": "lut_as_logic",
    "LUT as Memory": "lut_as_memory",
    "Slice Registers": "slice_registers",
    "Slice": "slices",
    "Block RAM Tile": "bram_tiles",
    "RAMB18": "ramb18",
    "DSPs": "dsps",
    "Bonded IOB": "bonded_iob",
    "BUFGCTRL": "bufgctrl",
    "MMCME2_ADV": "mmcm",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return [dict(row) for row in csv.DictReader(f)]


def run_key(row: dict[str, str], path: Path, key_column: str | None = None) -> str:
    candidates = [key_column] if key_column else []
    candidates += ["run", "experiment", "placement", "variant", "name"]
    for key in candidates:
        if key and row.get(key):
            value = Path(row[key]).stem if key in {"file", "source"} else row[key]
            return normalize_key(value)
    for key in ["file", "source"]:
        if row.get(key):
            return normalize_key(Path(row[key]).stem)
    return normalize_key(path.stem)


def normalize_key(value: str) -> str:
    value = value.replace("\\", "/").strip()
    if "/" in value:
        value = Path(value).stem
    for suffix in [".tdc_metrics", ".tdc_packets", ".tdc_bins", "_summary"]:
        if value.endswith(suffix):
            value = value[: -len(suffix)]
    return value or "run"


def add_prefixed(
    table: dict[str, dict[str, str]],
    key: str,
    row: dict[str, str],
    prefix: str,
    skip: set[str],
) -> None:
    dest = table.setdefault(key, {"run": key})
    for column, value in row.items():
        if column in skip or value == "":
            continue
        out_key = f"{prefix}_{column}" if prefix else column
        if out_key == "run":
            out_key = f"{prefix}_run"
        dest[out_key] = value


def merge_csv_files(
    table: dict[str, dict[str, str]],
    paths: list[Path],
    prefix: str,
    key_column: str | None,
) -> None:
    for path in paths:
        for row in read_csv_rows(path):
            key = run_key(row, path, key_column)
            add_prefixed(table, key, row, prefix, {"run", "experiment", "placement", "variant"})


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[f"place_{key.strip()}"] = value.strip()
    return result


def parse_timing(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    text = "\n".join(lines)
    for idx, line in enumerate(lines):
        if "WNS(ns)" not in line or "TNS(ns)" not in line or "WHS(ns)" not in line:
            continue
        for candidate in lines[idx + 1 : idx + 5]:
            values = re.findall(r"[-+]?\d+\.\d+|[-+]?\d+", candidate)
            if len(values) >= 6:
                result["place_wns_ns"] = values[0]
                result["place_tns_ns"] = values[1]
                result["place_whs_ns"] = values[4]
                result["place_ths_ns"] = values[5]
                break
        if "place_wns_ns" in result:
            break
    for label in ["no_clock", "unconstrained_internal_endpoints", "loops"]:
        match = re.search(rf"checking {re.escape(label)} \((\d+)\)", text)
        if match:
            result[f"place_check_{label}"] = match.group(1)
    return result


def parse_route_status(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="ignore")
    for label, key in [
        ("# of logical nets", "logical_nets"),
        ("# of fully routed nets", "fully_routed_nets"),
        ("# of nets with routing errors", "routing_error_nets"),
    ]:
        match = re.search(rf"{re.escape(label)}\.*\s*:\s*([0-9,]+)\s*:", text)
        if match:
            result[f"place_{key}"] = match.group(1).replace(",", "")
    return result


def split_table_line(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_utilization(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "|" not in line:
            continue
        parts = split_table_line(line)
        if len(parts) < 2:
            continue
        site_type = re.sub(r"\s+", " ", parts[0])
        key = UTIL_NAMES.get(site_type)
        if key:
            result[f"place_{key}_used"] = parts[1].replace(",", "")
            if len(parts) >= 5:
                result[f"place_{key}_available"] = parts[4].replace(",", "")
            if len(parts) >= 6:
                result[f"place_{key}_util_pct"] = parts[5].replace("<", "").replace("%", "")
    return result


def vivado_run_key(seed_dir: Path) -> str:
    placement = seed_dir.parent.name
    seed_match = re.search(r"seed[_-]?(\d+)", seed_dir.name)
    seed = seed_match.group(1) if seed_match else seed_dir.name
    return normalize_key(f"{placement}_seed{seed}")


def add_vivado_runs(table: dict[str, dict[str, str]], roots: list[Path]) -> None:
    for root in roots:
        seed_dirs = [path for path in root.rglob("manifest.txt") if path.is_file()]
        if root.is_dir() and (root / "manifest.txt").exists():
            seed_dirs.append(root / "manifest.txt")
        for manifest in sorted(set(seed_dirs)):
            run_dir = manifest.parent
            key = vivado_run_key(run_dir)
            row = {"run": key, **parse_manifest(manifest)}
            row.update(parse_timing(run_dir / "timing_summary.rpt"))
            row.update(parse_route_status(run_dir / "route_status.rpt"))
            row.update(parse_utilization(run_dir / "utilization.rpt"))
            table.setdefault(key, {"run": key}).update(row)


def preferred_columns(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    columns: list[str] = []
    preferred = [
        "run",
        "tdc_packets",
        "tdc_diff_std_ps",
        "tdc_phase_pearson_r",
        "tdc_lane_a_peak_abs_inl_lsb",
        "tdc_lane_b_peak_abs_inl_lsb",
        "trng_bytes",
        "trng_p1",
        "trng_bit_min_entropy",
        "trng_monobit_p",
        "trng_runs_p",
        "trng_min_entropy_byte",
        "ro_ro_freq_mhz",
        "ro_jitter_std_ps",
        "place_placement_xdc",
        "place_seed",
        "place_wns_ns",
        "place_tns_ns",
        "place_whs_ns",
        "place_slice_luts_used",
        "place_slice_registers_used",
    ]
    for column in preferred:
        if any(column in row for row in rows):
            columns.append(column)
            seen.add(column)
    for row in rows:
        for column in row:
            if column not in seen:
                columns.append(column)
                seen.add(column)
    return columns


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_markdown(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    visible = columns[:18]
    with path.open("w", encoding="utf-8") as f:
        f.write("# Merged Experiment Table\n\n")
        f.write("| " + " | ".join(visible) + " |\n")
        f.write("| " + " | ".join(["---"] * len(visible)) + " |\n")
        for row in rows:
            cells = [row.get(column, "").replace("|", "\\|") for column in visible]
            f.write("| " + " | ".join(cells) + " |\n")
        if len(columns) > len(visible):
            f.write(f"\nMarkdown shows the first {len(visible)} columns; CSV contains all {len(columns)} columns.\n")


def existing_paths(values: list[Path]) -> list[Path]:
    return [path for path in values if path.exists()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tdc", nargs="*", type=Path, default=[], help="TDC metrics CSV files")
    parser.add_argument("--trng", nargs="*", type=Path, default=[], help="TRNG summary CSV files")
    parser.add_argument("--ro", nargs="*", type=Path, default=[], help="RO counter summary CSV files")
    parser.add_argument("--csv", nargs="*", type=Path, default=[], help="Additional CSV files")
    parser.add_argument("--vivado-runs", nargs="*", type=Path, default=[], help="Vivado run root(s) with manifest/report files")
    parser.add_argument("--key-column", default=None, help="Override key column for CSV inputs")
    parser.add_argument("--out-csv", type=Path, default=Path("data/experiments/merged_experiment_table.csv"))
    parser.add_argument("--out-md", type=Path, default=Path("data/experiments/merged_experiment_table.md"))
    args = parser.parse_args()

    table: dict[str, dict[str, str]] = {}
    merge_csv_files(table, existing_paths(args.tdc), "tdc", args.key_column)
    merge_csv_files(table, existing_paths(args.trng), "trng", args.key_column)
    merge_csv_files(table, existing_paths(args.ro), "ro", args.key_column)
    merge_csv_files(table, existing_paths(args.csv), "extra", args.key_column)
    add_vivado_runs(table, existing_paths(args.vivado_runs))

    if not table:
        raise SystemExit("No input rows found.")

    rows = [table[key] for key in sorted(table)]
    columns = preferred_columns(rows)
    write_csv(args.out_csv, rows, columns)
    write_markdown(args.out_md, rows, columns)
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
