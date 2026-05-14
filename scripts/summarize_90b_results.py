#!/usr/bin/env python3
"""Summarize local SP800-90B EntropyAssessment smoke logs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


H_RE = re.compile(r"H_original:\s*([0-9.]+)")
LIMIT_RE = re.compile(r"_(\d+)m\.log$")


def parse_name(path: Path) -> tuple[str, str, str, str]:
    name = path.name
    tool = "unknown"
    if "_non_iid_" in name and name.endswith("m.log"):
        stem = name.rsplit("_non_iid_", 1)[0]
        tool = "ea_non_iid"
    elif "_iid_" in name and name.endswith("m.log"):
        stem = name.rsplit("_iid_", 1)[0]
        tool = "ea_iid"
    else:
        stem = path.stem
    if stem.endswith("_bps1_msb"):
        return stem[: -len("_bps1_msb")], "bit-symbols-msb", "1", tool
    if stem.endswith("_bps1_lsb"):
        return stem[: -len("_bps1_lsb")], "bit-symbols-lsb", "1", tool
    if stem.endswith("_bps8"):
        return stem[: -len("_bps8")], "byte-symbols", "8", tool
    return stem, "unknown", "", tool


def summarize(log_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for log in sorted(log_dir.glob("*m.log")):
        raw = log.read_bytes()
        if raw.startswith(b"\xff\xfe") or raw.count(b"\x00") > len(raw) // 8:
            text = raw.decode("utf-16", errors="replace")
        else:
            text = raw.decode("utf-8", errors="replace")
        match = H_RE.search(text)
        dataset, mode, bits_per_symbol, tool = parse_name(log)
        chi_square = ""
        lrs = ""
        if tool == "ea_iid":
            if "Passed chi square tests" in text:
                chi_square = "pass"
            elif "Failed chi square tests" in text:
                chi_square = "fail"
            if "Passed length of longest repeated substring test" in text:
                lrs = "pass"
            elif "Failed length of longest repeated substring test" in text:
                lrs = "fail"
        if not match:
            status = "missing_h_original"
        elif tool == "ea_iid" and (chi_square == "fail" or lrs == "fail"):
            status = "iid_failed"
        else:
            status = "ok"
        limit_match = LIMIT_RE.search(log.name)
        limit_symbols = str(int(limit_match.group(1)) * 1_000_000) if limit_match else ""
        rows.append(
            {
                "dataset": dataset,
                "tool": tool,
                "mode": mode,
                "bits_per_symbol": bits_per_symbol,
                "limit_symbols": limit_symbols,
                "h_original_bits_per_symbol": match.group(1) if match else "",
                "iid_chi_square": chi_square,
                "iid_lrs": lrs,
                "log": str(log),
                "status": status,
            }
        )
    rows.sort(key=lambda r: (r["tool"], r["mode"], r["dataset"]))
    return rows


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "dataset",
        "tool",
        "mode",
        "bits_per_symbol",
        "limit_symbols",
        "h_original_bits_per_symbol",
        "iid_chi_square",
        "iid_lrs",
        "status",
        "log",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    limits = sorted({row["limit_symbols"] for row in rows if row["limit_symbols"]})
    if not limits:
        sample_note = "saved log window per input"
    elif len(limits) == 1:
        sample_note = f"first {int(limits[0]):,} symbols per prepared input"
    else:
        sample_note = "mixed symbol windows: " + ", ".join(f"{int(v):,}" for v in limits)
    lines = [
        "# SP800-90B Smoke Summary",
        "",
        "- estimator: NIST SP800-90B EntropyAssessment `ea_non_iid` plus selected `ea_iid` diagnostics",
        f"- sample window: {sample_note}",
        "- interpretation: smoke screening only; not a full validation campaign",
        "",
        "| dataset | tool | mode | bits/symbol | H_original | IID chi-square | IID LRS | status |",
        "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        h = row["h_original_bits_per_symbol"] or "NA"
        lines.append(
            f"| {row['dataset']} | {row['tool']} | {row['mode']} | {row['bits_per_symbol']} | {h} | "
            f"{row['iid_chi_square'] or 'NA'} | {row['iid_lrs'] or 'NA'} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "Notes:",
            "",
            "- `H_original` is reported in bits per output symbol by the EntropyAssessment tool.",
            "- The bit-symbol mode expands each captured byte into eight binary symbols before running the non-IID estimator.",
            "- IID rows are diagnostic only; the headline entropy claim should use the conservative non-IID rows unless IID is fully justified.",
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
