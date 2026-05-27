#!/usr/bin/env python3
"""Summarize strict restart sampler-island passband results."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


H_I_RE = re.compile(r"H_I:\s*([0-9.]+)")
X_CUTOFF_RE = re.compile(r"X_cutoff:\s*([0-9]+)")
X_MAX_RE = re.compile(r"X_max:\s*([0-9]+)")
MIN_H_RE = re.compile(r"min\(H_r, H_c, H_I\):\s*([0-9.]+)")


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
        writer.writerows(rows)


def infer_variant(label: str) -> str:
    if "sampler_island_local" in label:
        return "sample_ro_plus_regs_local"
    if "sample_ro_local" in label:
        return "sample_ro_local_only"
    if "sampler_regs_only" in label or "regs_only" in label:
        return "regs_local_only"
    if "random3" in label:
        return "random3_reference"
    if "random1" in label:
        return "random1_baseline"
    return "unknown"


def infer_warmup(label: str) -> str:
    match = re.search(r"warmup(\d+)", label)
    return match.group(1) if match else ""


def parse_ea_restart(stdout: Path) -> dict[str, str]:
    if not stdout.exists():
        return {
            "status": "missing",
            "h_i": "",
            "x_cutoff": "",
            "x_max": "",
            "min_restart_entropy": "",
            "stdout": str(stdout),
        }
    text = stdout.read_text(encoding="utf-8", errors="replace")
    status = "error"
    if "Validation Test Passed" in text:
        status = "passed"
    elif "Restart Sanity Check Failed" in text:
        status = "failed"
    return {
        "status": status,
        "h_i": match_or_blank(H_I_RE, text),
        "x_cutoff": match_or_blank(X_CUTOFF_RE, text),
        "x_max": match_or_blank(X_MAX_RE, text),
        "min_restart_entropy": match_or_blank(MIN_H_RE, text),
        "stdout": str(stdout),
    }


def match_or_blank(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    return match.group(1) if match else ""


def profile_by_label(profile_csv: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(profile_csv)
    return {row["label"]: row for row in rows}


def read_manifest(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(path)
    return {
        (row["label"], row["bit_order"]): row
        for row in rows
        if row.get("label") and row.get("bit_order")
    }


def find_payload_meta(payload_dir: Path, label: str) -> dict[str, object]:
    path = payload_dir / f"{label}.payload.bin.metadata.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_profile_label(label: str) -> str:
    if label.endswith(".payload"):
        return label[: -len(".payload")]
    return label


def build_rows(args: argparse.Namespace) -> list[dict[str, object]]:
    profile_map = profile_by_label(args.profile_csv)
    manifest = read_manifest(args.manifest_csv)
    rows: list[dict[str, object]] = []
    for profile_label, profile in sorted(profile_map.items()):
        label = normalize_profile_label(profile_label)
        variant = infer_variant(label)
        warmup = infer_warmup(label)
        payload_meta = find_payload_meta(args.payload_dir, label)
        for order in ("msb", "lsb"):
            manifest_row = manifest.get((label, order), {})
            run = manifest_row.get("ea_run") or f"{label}_{order}"
            stdout = args.ea_restart_dir / run / f"{run}.ea_restart.stdout.txt"
            ea = parse_ea_restart(stdout)
            rows.append(
                {
                    "label": label,
                    "variant": variant,
                    "warmup": warmup,
                    "bit_order": order,
                    "ea_restart_status": ea["status"],
                    "h_i": ea["h_i"],
                    "x_cutoff": ea["x_cutoff"],
                    "x_max": ea["x_max"],
                    "min_restart_entropy": ea["min_restart_entropy"],
                    "overall_p1": profile.get("overall_p1", ""),
                    "overall_min_entropy": profile.get("overall_min_entropy", ""),
                    "worst_byte_index": profile.get("worst_byte_index", ""),
                    "worst_bit_index": profile.get("worst_bit_index", ""),
                    "worst_x_profile": profile.get("worst_x", ""),
                    "worst_p1": profile.get("worst_p1", ""),
                    "payload_sha256": payload_meta.get("output_sha256", ""),
                    "capture_sha256": payload_meta.get("input_sha256", ""),
                    "header_hex": (payload_meta.get("header") or {}).get("header_hex", ""),
                    "payload_file": payload_meta.get("output_file", profile.get("input", "")),
                    "ea_stdout": ea["stdout"],
                }
            )
    return rows


def write_md(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Restart Sampler-Island Passband Strict Summary",
        "",
        "Only strict captures with an 8-byte restart header plus a complete 1000x125 payload should be used as formal restart evidence.",
        "",
        "| variant | warmup | order | restart | X_max/cutoff | overall p1 | worst byte.bit | worst p1 | min restart H |",
        "| --- | ---: | --- | --- | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in sorted(rows, key=lambda r: (str(r["variant"]), int(r["warmup"] or 9999), str(r["bit_order"]))):
        x_pair = f"{row['x_max']}/{row['x_cutoff']}" if row["x_max"] or row["x_cutoff"] else ""
        worst = f"{row['worst_byte_index']}.{row['worst_bit_index']}"
        lines.append(
            f"| {row['variant']} | {row['warmup']} | {row['bit_order']} | "
            f"{row['ea_restart_status']} | {x_pair} | {row['overall_p1']} | "
            f"{worst} | {row['worst_p1']} | {row['min_restart_entropy']} |"
        )

    lines.extend(
        [
            "",
            "Interpretation guide:",
            "",
            "- `sample_ro_local_only` isolates the sample RO placement change while leaving sampling registers/routing in the baseline implementation.",
            "- `sample_ro_plus_regs_local` is the sampler-island variant and tests the combined sampler-side physical boundary.",
            "- A non-monotonic passband is evidence that warmup is selecting a startup phase window, not simply improving randomness by waiting longer.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile-csv",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/profile/restart_sampler_island_passband_strict_20260525_summary.csv"),
    )
    parser.add_argument(
        "--payload-dir",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/payloads"),
    )
    parser.add_argument(
        "--ea-restart-dir",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/ea_restart"),
    )
    parser.add_argument(
        "--manifest-csv",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/ea_restart_manifest_20260525.csv"),
    )
    parser.add_argument(
        "--out-csv",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/restart_sampler_island_passband_strict_summary_20260525.csv"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("data/experiments/restart_sampler_island_passband_strict_20260525/restart_sampler_island_passband_strict_summary_20260525.md"),
    )
    args = parser.parse_args()

    rows = build_rows(args)
    fields = [
        "label",
        "variant",
        "warmup",
        "bit_order",
        "ea_restart_status",
        "h_i",
        "x_cutoff",
        "x_max",
        "min_restart_entropy",
        "overall_p1",
        "overall_min_entropy",
        "worst_byte_index",
        "worst_bit_index",
        "worst_x_profile",
        "worst_p1",
        "header_hex",
        "capture_sha256",
        "payload_sha256",
        "payload_file",
        "ea_stdout",
    ]
    write_csv(args.out_csv, rows, fields)
    write_md(args.out_md, rows)
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
