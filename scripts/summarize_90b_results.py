#!/usr/bin/env python3
"""Summarize local SP800-90B EntropyAssessment smoke logs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


H_RE = re.compile(r"H_original:\s*([0-9.]+)")


def parse_name(path: Path) -> tuple[str, str, str]:
    name = path.name
    suffix = "_non_iid_1m.log"
    stem = name[: -len(suffix)] if name.endswith(suffix) else path.stem
    if stem.endswith("_bps1_msb"):
        return stem[: -len("_bps1_msb")], "bit-symbols-msb", "1"
    if stem.endswith("_bps1_lsb"):
        return stem[: -len("_bps1_lsb")], "bit-symbols-lsb", "1"
    if stem.endswith("_bps8"):
        return stem[: -len("_bps8")], "byte-symbols", "8"
    return stem, "unknown", ""


def summarize(log_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for log in sorted(log_dir.glob("*_non_iid_*.log")):
        raw = log.read_bytes()
        if raw.startswith(b"\xff\xfe") or raw.count(b"\x00") > len(raw) // 8:
            text = raw.decode("utf-16", errors="replace")
        else:
            text = raw.decode("utf-8", errors="replace")
        match = H_RE.search(text)
        dataset, mode, bits_per_symbol = parse_name(log)
        rows.append(
            {
                "dataset": dataset,
                "mode": mode,
                "bits_per_symbol": bits_per_symbol,
                "limit_symbols": "1000000" if "_1m" in log.stem else "",
                "h_original_bits_per_symbol": match.group(1) if match else "",
                "log": str(log),
                "status": "ok" if match else "missing_h_original",
            }
        )
    rows.sort(key=lambda r: (r["mode"], r["dataset"]))
    return rows


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "dataset",
        "mode",
        "bits_per_symbol",
        "limit_symbols",
        "h_original_bits_per_symbol",
        "status",
        "log",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SP800-90B Smoke Summary",
        "",
        "- estimator: NIST SP800-90B EntropyAssessment `ea_non_iid`",
        "- sample window: first 1,000,000 symbols per prepared input",
        "- interpretation: smoke screening only; not a full validation campaign",
        "",
        "| dataset | mode | bits/symbol | H_original | status |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        h = row["h_original_bits_per_symbol"] or "NA"
        lines.append(
            f"| {row['dataset']} | {row['mode']} | {row['bits_per_symbol']} | {h} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "Notes:",
            "",
            "- `H_original` is reported in bits per output symbol by the EntropyAssessment tool.",
            "- The bit-symbol mode expands each captured byte into eight binary symbols before running the non-IID estimator.",
            "- These smoke results are suitable for layout comparison and triage, not for claiming SP800-90B compliance.",
        ]
    )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=Path("data/sp800_90b/results_smoke_20260514"),
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/sp800_90b/results_smoke_20260514/summary.csv"),
    )
    parser.add_argument(
        "--md",
        type=Path,
        default=Path("data/sp800_90b/results_smoke_20260514/summary.md"),
    )
    args = parser.parse_args()

    rows = summarize(args.log_dir)
    write_csv(rows, args.csv)
    write_md(rows, args.md)
    print(f"Wrote {args.csv}")
    print(f"Wrote {args.md}")


if __name__ == "__main__":
    main()
