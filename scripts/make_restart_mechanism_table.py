#!/usr/bin/env python3
"""Build a compact table linking restart bias to available mechanism metrics."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


RESTART_AUDIT_FIELDS = [
    "restart_method",
    "warmup_bytes",
    "warmup_unit",
    "restart_rows",
    "restart_row_packed_bytes",
    "restart_output_bit_symbols_per_row",
    "restart_input_file",
    "restart_capture_sha256",
    "restart_bps1_sha256",
    "restart_bps1_sha256_msb",
    "restart_bps1_sha256_lsb",
    "ea_restart_status_msb",
    "ea_restart_status_lsb",
    "restart_hi_msb",
    "restart_hi_lsb",
    "restart_hi_source_msb",
    "restart_hi_source_lsb",
    "restart_x_cutoff_msb",
    "restart_x_cutoff_lsb",
    "restart_x_max_msb",
    "restart_x_max_lsb",
    "restart_hr_msb",
    "restart_hr_lsb",
    "restart_hc_msb",
    "restart_hc_lsb",
    "restart_min_entropy_msb",
    "restart_min_entropy_lsb",
    "repeat_id",
    "run_id",
]


def to_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def read_csv_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return {row[key]: row for row in csv.DictReader(f) if row.get(key)}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def first_value(*values: object) -> str:
    for value in values:
        cell = to_cell(value)
        if cell:
            return cell
    return ""


def capture_metadata_path(input_file: str) -> Path | None:
    if not input_file:
        return None
    input_path = Path(input_file)
    candidates = [
        input_path.with_suffix(".metadata.json"),
        Path(str(input_path) + ".metadata.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def bps1_metadata_path(input_file: str, bit_order: str) -> Path | None:
    if not input_file:
        return None
    input_path = Path(input_file)
    stem_path = input_path.with_suffix("")
    candidates = [
        Path(f"{stem_path}_bps1_{bit_order}.metadata.json"),
        Path(f"{stem_path}_bps1_{bit_order}.bin.metadata.json"),
        Path(f"{input_path}_bps1_{bit_order}.metadata.json"),
        Path(f"{input_path}_bps1_{bit_order}.bin.metadata.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def read_manifest(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def bitstream_manifest_path(capture_meta: dict[str, object]) -> Path | None:
    bitstream = source_value(capture_meta, "bitstream_resolved", "bitstream")
    if not bitstream:
        return None
    path = Path(bitstream)
    candidates = [
        path.parent / "manifest.txt",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def parse_ea_restart_stdout(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    out: dict[str, str] = {}
    if "Validation Test Passed" in text:
        out["ea_restart_status"] = "passed"
    elif "Restart Sanity Check Failed" in text:
        out["ea_restart_status"] = "failed"

    patterns = {
        "restart_hi": r"H_I:\s*([0-9.]+)",
        "restart_x_cutoff": r"X_cutoff:\s*([0-9]+)",
        "restart_x_max": r"X_max:\s*([0-9]+)",
        "restart_hr": r"H_r:\s*([0-9.]+)",
        "restart_hc": r"H_c:\s*([0-9.]+)",
        "restart_min_entropy": r"min\(H_r,\s*H_c,\s*H_I\):\s*([0-9.]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            out[key] = match.group(1)
    return out


def find_ea_restart_result(input_file: str) -> dict[str, str]:
    if not input_file:
        return {}
    input_path = Path(input_file).resolve()
    restart_dir = input_path.parent
    if not restart_dir.is_dir():
        return {}

    for meta_path in restart_dir.glob("ea_restart*/*.ea_restart.metadata.json"):
        meta = read_json(meta_path)
        meta_input = source_value(meta, "input_file")
        if not meta_input:
            continue
        try:
            same_input = Path(meta_input).resolve() == input_path
        except OSError:
            same_input = str(meta_input).lower() == str(input_path).lower()
        if not same_input:
            continue

        result = parse_ea_restart_stdout(Path(source_value(meta, "stdout")))
        result["restart_hi"] = first_value(result.get("restart_hi"), source_value(meta, "initial_entropy"))
        result["restart_hi_source"] = "ea_restart_stdout"
        return result
    return {}


def source_value(source: dict[str, object], *keys: str) -> str:
    for key in keys:
        if key in source:
            cell = to_cell(source.get(key))
            if cell:
                return cell
    return ""


def nested_bit_order_value(source: dict[str, object], bit_order: str, *keys: str) -> str:
    for key in keys:
        cell = source_value(source, f"{key}_{bit_order}", key)
        if cell:
            return cell

    for container_key in ("ea_restart", "restart", "audit"):
        container = source.get(container_key)
        if not isinstance(container, dict):
            continue
        by_order = container.get(bit_order)
        if isinstance(by_order, dict):
            cell = source_value(by_order, *keys)
            if cell:
                return cell
        for key in keys:
            value = container.get(f"{key}_{bit_order}")
            if value is not None:
                cell = to_cell(value)
                if cell:
                    return cell
    return ""


def infer_repeat_id(run_id: str) -> str:
    match = re.search(r"(?:^|_)(repeat[0-9]+)(?:_|$)", run_id)
    return match.group(1) if match else ""


def add_restart_audit_fields(
    row: dict[str, str],
    summary: dict[str, object],
    capture_meta: dict[str, object],
    build_manifest: dict[str, str],
    bps1_meta: dict[str, dict[str, object]],
    bit_order: str,
) -> None:
    for field in RESTART_AUDIT_FIELDS:
        row.setdefault(field, "")

    current_order = bit_order.lower()
    current_bps1 = bps1_meta.get(current_order, {}) if current_order in {"msb", "lsb"} else {}
    capture_id = first_value(
        source_value(capture_meta, "run_id", "capture_id", "label"),
        source_value(summary, "run_id", "capture_id", "label"),
    )

    row["restart_method"] = first_value(
        source_value(summary, "restart_method"),
        source_value(capture_meta, "restart_method"),
    )
    row["warmup_bytes"] = first_value(
        source_value(build_manifest, "warmup_bytes"),
        source_value(summary, "warmup_bytes"),
        source_value(capture_meta, "warmup_bytes"),
        source_value(capture_meta, "warmup_symbols_discarded"),
    )
    row["warmup_unit"] = first_value(
        "packed_byte" if source_value(build_manifest, "warmup_bytes") else "",
        source_value(summary, "warmup_unit"),
        source_value(capture_meta, "warmup_unit"),
        "symbols" if row["warmup_bytes"] else "",
    )
    row["restart_rows"] = first_value(
        source_value(summary, "restart_rows", "restart_count"),
        source_value(current_bps1, "restart_rows", "restart_count"),
        source_value(capture_meta, "restart_rows", "restart_count"),
    )
    row["restart_row_packed_bytes"] = first_value(
        source_value(build_manifest, "row_bytes"),
        source_value(summary, "restart_row_packed_bytes", "bytes_per_restart"),
        source_value(current_bps1, "restart_row_packed_bytes", "input_symbols_per_restart"),
        source_value(capture_meta, "restart_row_packed_bytes", "symbols_per_restart"),
    )
    row["restart_output_bit_symbols_per_row"] = first_value(
        source_value(summary, "restart_output_bit_symbols_per_row", "expanded_symbols_per_restart"),
        source_value(current_bps1, "restart_output_bit_symbols_per_row", "output_symbols_per_restart"),
    )
    row["restart_input_file"] = first_value(
        source_value(summary, "restart_input_file", "input_file"),
        source_value(current_bps1, "restart_input_file", "input_file"),
        source_value(capture_meta, "restart_input_file", "output_file"),
    )
    row["restart_capture_sha256"] = first_value(
        source_value(summary, "restart_capture_sha256", "input_sha256"),
        source_value(current_bps1, "restart_capture_sha256", "input_sha256"),
        source_value(capture_meta, "restart_capture_sha256", "output_sha256", "dataset_sha256"),
    )
    row["restart_bps1_sha256"] = first_value(
        source_value(summary, "restart_bps1_sha256"),
        source_value(current_bps1, "restart_bps1_sha256", "output_sha256"),
        source_value(bps1_meta.get("msb", {}), "restart_bps1_sha256", "output_sha256"),
        source_value(bps1_meta.get("lsb", {}), "restart_bps1_sha256", "output_sha256"),
    )
    row["restart_bps1_sha256_msb"] = first_value(
        nested_bit_order_value(summary, "msb", "restart_bps1_sha256"),
        source_value(bps1_meta.get("msb", {}), "restart_bps1_sha256", "output_sha256"),
    )
    row["restart_bps1_sha256_lsb"] = first_value(
        nested_bit_order_value(summary, "lsb", "restart_bps1_sha256"),
        source_value(bps1_meta.get("lsb", {}), "restart_bps1_sha256", "output_sha256"),
    )

    for order in ("msb", "lsb"):
        sources = [bps1_meta.get(order, {}), summary, capture_meta]
        row[f"ea_restart_status_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "ea_restart_status", "status") for source in sources)
        )
        row[f"restart_hi_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_hi", "hi", "h_i") for source in sources)
        )
        row[f"restart_hi_source_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_hi_source", "hi_source") for source in sources)
        )
        row[f"restart_x_cutoff_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_x_cutoff", "x_cutoff") for source in sources)
        )
        row[f"restart_x_max_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_x_max", "x_max") for source in sources),
            source_value(summary.get("worst_position", {}) if isinstance(summary.get("worst_position"), dict) else {}, "x"),
        )
        row[f"restart_hr_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_hr", "h_r") for source in sources)
        )
        row[f"restart_hc_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_hc", "h_c") for source in sources)
        )
        row[f"restart_min_entropy_{order}"] = first_value(
            *(nested_bit_order_value(source, order, "restart_min_entropy", "min_entropy") for source in sources)
        )

    row["run_id"] = first_value(
        source_value(summary, "run_id"),
        source_value(capture_meta, "run_id"),
        capture_id,
    )
    row["repeat_id"] = first_value(
        source_value(summary, "repeat_id"),
        source_value(capture_meta, "repeat_id"),
        infer_repeat_id(row["run_id"]),
    )


def flatten_restart_summary(path: Path, placement: str, bit_order: str) -> dict[str, str]:
    data = read_json(path)
    worst = data.get("worst_position", {}) or {}
    if not isinstance(worst, dict):
        worst = {}
    input_file = to_cell(data.get("input_file"))
    capture_meta = read_json(capture_metadata_path(input_file) or Path())
    build_manifest = read_manifest(bitstream_manifest_path(capture_meta) or Path())
    bps1_meta = {
        order: read_json(bps1_metadata_path(input_file, order) or Path())
        for order in ("msb", "lsb")
    }
    for order in ("msb", "lsb"):
        ea_result = find_ea_restart_result(source_value(bps1_meta.get(order, {}), "output_file"))
        bps1_meta[order].update(ea_result)

    row = {
        "placement": placement,
        "bit_order": bit_order,
        "restart_input_sha256": str(data.get("input_sha256", "")),
        "restart_overall_p1": f"{float(data.get('overall_p1', 0.0)):.9f}",
        "restart_x_cutoff": str(data.get("x_cutoff", "")),
        "restart_positions_over_x_cutoff": str(data.get("positions_over_x_cutoff", "")),
        "restart_worst_byte": str(worst.get("byte_index", "")),
        "restart_worst_bit": str(worst.get("bit_index", "")),
        "restart_worst_ones": str(worst.get("ones", "")),
        "restart_worst_zeros": str(worst.get("zeros", "")),
        "restart_worst_x": str(worst.get("x", "")),
        "restart_worst_p1": str(worst.get("p1", "")),
        "restart_worst_msb_column": str(worst.get("msb_expanded_column", "")),
        "restart_worst_lsb_column": str(worst.get("lsb_expanded_column", "")),
        "restart_summary": str(path),
    }
    add_restart_audit_fields(row, data, capture_meta, build_manifest, bps1_meta, bit_order)
    return row


def placement_from_tdc_run(run: str) -> str:
    match = re.search(r"tdc_pair_(random[0-9]+|compact|sparse|far|checker|same_column|row|cross_region)", run)
    return match.group(1) if match else ""


def summarize_tdc_by_placement(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        placement = row.get("placement") or placement_from_tdc_run(row.get("run", ""))
        if placement:
            grouped.setdefault(placement, []).append(row)

    out: dict[str, dict[str, str]] = {}
    numeric_fields = [
        "phase_r_mean",
        "phase_r_max_abs",
        "best_lag_abs_r_max",
        "diff_std_ps_mean",
        "diff_mean_ps_slope_per_window",
        "strong_lock_windows",
    ]
    for placement, placement_rows in grouped.items():
        result: dict[str, str] = {"tdc_pair_count": str(len(placement_rows))}
        for field in numeric_fields:
            vals = []
            for row in placement_rows:
                try:
                    vals.append(float(row.get(field, "")))
                except ValueError:
                    pass
            if vals:
                result[f"tdc_{field}_mean"] = f"{sum(vals) / len(vals):.9g}"
                result[f"tdc_{field}_max"] = f"{max(vals):.9g}"
        out[placement] = result
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out-dir", type=Path, default=Path("data/experiments/paper_artifacts_20260515"))
    parser.add_argument(
        "--restart-summary",
        action="append",
        default=[],
        help="placement,bit_order,path_to_restart_column_summary_json",
    )
    args = parser.parse_args()

    root = args.repo_root.resolve()
    out_dir = (root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    restart_items = list(args.restart_summary)
    if not restart_items:
        auto_root = out_dir
        if auto_root.exists():
            for summary_path in sorted(auto_root.glob("restart_column_bias_*/summary.json")):
                label = summary_path.parent.name
                placement = ""
                if label.startswith("restart_column_bias_"):
                    remainder = label[len("restart_column_bias_") :]
                    placement = remainder.split("_formal_bits", 1)[0]
                if not placement:
                    continue
                restart_items.append(f"{placement},packed_warmup0,{summary_path.relative_to(root)}")

    trng = read_csv_by_key(
        root / "data/experiments/fast_mode/offline_figures_20260513/table_trng_repeat_by_placement.csv",
        "placement",
    )
    ro_freq = read_csv_by_key(
        root / "data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv",
        "placement",
    )
    tdc = summarize_tdc_by_placement(
        read_rows(root / "data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.csv")
    )

    rows: list[dict[str, str]] = []
    for item in restart_items:
        parts = item.split(",", 2)
        if len(parts) != 3:
            raise SystemExit(f"bad --restart-summary item: {item}")
        placement, bit_order, summary_path = parts
        row = flatten_restart_summary((root / summary_path).resolve(), placement, bit_order)
        row.update({f"trng_{k}": v for k, v in trng.get(placement, {}).items() if k != "placement"})
        row.update({f"rofreq_{k}": v for k, v in ro_freq.get(placement, {}).items() if k != "placement"})
        row.update(tdc.get(placement, {}))
        rows.append(row)

    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    csv_path = out_dir / "table_restart_mechanism_link.csv"
    md_path = out_dir / "table_restart_mechanism_link.md"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# Restart Mechanism Link Table", ""]
    for row in rows:
        md_lines.extend(
            [
                f"## {row.get('placement')} {row.get('bit_order')}",
                "",
                f"- restart worst raw position: byte `{row.get('restart_worst_byte')}`, bit `{row.get('restart_worst_bit')}`, x `{row.get('restart_worst_x')}`, p1 `{row.get('restart_worst_p1')}`",
                f"- expanded columns: MSB `{row.get('restart_worst_msb_column')}`, LSB `{row.get('restart_worst_lsb_column')}`",
                f"- TRNG bit min-entropy mean: `{row.get('trng_bit_min_entropy_mean', '')}`",
                f"- RO closest data-data delta MHz: `{row.get('rofreq_ro_min_data_data_delta_mhz', '')}`",
                f"- TDC pair count: `{row.get('tdc_pair_count', '')}`",
                "",
            ]
        )
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
