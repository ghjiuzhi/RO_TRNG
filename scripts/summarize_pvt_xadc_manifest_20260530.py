#!/usr/bin/env python3
"""Validate PVT/XADC manifest rows without touching hardware.

The capture-side schema records whether an XADC read parsed successfully.
This offline checker adds a physical-validity layer so sentinel readings such
as -273.1 C with zero rails are not treated as usable PVT evidence.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = (
    "capture_id",
    "context",
    "moment",
    "xadc_status",
    "xadc_timestamp",
    "temperature_c",
    "vccint_v",
    "vccaux_v",
    "vccbram_v",
    "source_file",
    "error",
)

RANGES = {
    "temperature_c": (-40.0, 125.0),
    "vccint_v": (0.80, 1.20),
    "vccaux_v": (1.50, 2.00),
    "vccbram_v": (0.80, 1.20),
}

SENTINEL_TEMPERATURES = {-273.1, -273.15}


def rel_or_abs(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def as_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def find_manifests(repo_root: Path, explicit: list[Path]) -> list[Path]:
    if explicit:
        paths = [rel_or_abs(repo_root, path) for path in explicit]
    else:
        paths = sorted(repo_root.glob("data/**/summary/*pvt_manifest*.csv"))
    return [path for path in paths if path.exists()]


def validate_row(row: dict[str, str]) -> tuple[str, str]:
    status = row.get("xadc_status", "")
    if status != "ok":
        return "not_ok", f"xadc_status={status or 'blank'}"

    reasons: list[str] = []
    for field, (low, high) in RANGES.items():
        value = as_float(row.get(field))
        if value is None:
            reasons.append(f"{field}=missing_or_non_numeric")
            continue
        if field == "temperature_c" and any(abs(value - x) < 0.01 for x in SENTINEL_TEMPERATURES):
            reasons.append(f"{field}=sentinel_{value:g}")
        elif value < low or value > high:
            reasons.append(f"{field}=out_of_range_{value:g}_not_{low:g}..{high:g}")

    if reasons:
        return "invalid", "; ".join(reasons)
    return "valid", ""


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
    if missing:
        raise ValueError(f"{path} missing required columns: {', '.join(missing)}")
    return rows


def classify_capture(rows: list[dict[str, str]]) -> tuple[str, str]:
    moments = Counter(row.get("moment", "") for row in rows)
    valid_moments = Counter(
        row.get("moment", "") for row in rows if row.get("pvt_row_validity") == "valid"
    )
    if valid_moments.get("before", 0) >= 1 and valid_moments.get("after", 0) >= 1:
        if moments.get("before", 0) == 1 and moments.get("after", 0) == 1:
            return "valid_pair", ""
        return "valid_pair_with_duplicates", f"moments={dict(moments)}"
    if moments.get("before", 0) == 0 or moments.get("after", 0) == 0:
        return "missing_moment", f"moments={dict(moments)}"
    return "invalid_pair", f"moments={dict(moments)}"


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    by_capture: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_capture[row.get("capture_id", "")].append(row)

    capture_status = Counter()
    for capture_rows in by_capture.values():
        status, _ = classify_capture(capture_rows)
        capture_status[status] += 1

    return {
        "row_validity": Counter(row.get("pvt_row_validity", "") for row in rows),
        "capture_status": capture_status,
        "capture_count": len(by_capture),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--manifest",
        type=Path,
        action="append",
        default=[],
        help="PVT manifest CSV to validate. Defaults to data/**/summary/*pvt_manifest*.csv.",
    )
    parser.add_argument("--out-csv", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifests = find_manifests(repo_root, args.manifest)
    if not manifests:
        raise SystemExit("No PVT manifest CSV files found.")

    all_rows: list[dict[str, str]] = []
    for manifest in manifests:
        rows = read_manifest(manifest)
        for row in rows:
            validity, reason = validate_row(row)
            row["manifest_file"] = str(manifest)
            row["pvt_row_validity"] = validity
            row["pvt_invalid_reason"] = reason
            all_rows.append(row)

    by_capture: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in all_rows:
        by_capture[row.get("capture_id", "")].append(row)
    for capture_id, rows in by_capture.items():
        status, reason = classify_capture(rows)
        for row in rows:
            row["pvt_capture_status"] = status
            row["pvt_capture_reason"] = reason

    stats = summarize(all_rows)
    print(f"Manifests scanned: {len(manifests)}")
    print(f"Rows scanned: {len(all_rows)}")
    print(f"Captures scanned: {stats['capture_count']}")
    print(
        "Row validity: "
        + ", ".join(f"{k}={v}" for k, v in sorted(stats["row_validity"].items()))
    )
    print(
        "Capture validity: "
        + ", ".join(f"{k}={v}" for k, v in sorted(stats["capture_status"].items()))
    )

    invalid = [row for row in all_rows if row.get("pvt_row_validity") != "valid"]
    if invalid:
        print("First invalid rows:")
        for row in invalid[:10]:
            print(
                f"- {row.get('capture_id')} {row.get('moment')}: "
                f"{row.get('pvt_invalid_reason')}"
            )

    if args.out_csv:
        out_csv = rel_or_abs(repo_root, args.out_csv)
        write_csv(out_csv, all_rows)
        print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
