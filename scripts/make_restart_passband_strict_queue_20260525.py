#!/usr/bin/env python3
"""Create strict pre-open restart queue rows that include the 8-byte header."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = [
    "enabled",
    "priority",
    "run",
    "kind",
    "bitstream",
    "bytes",
    "out_file",
    "metadata_dir",
    "analyze_group",
    "idle_timeout_sec",
    "notes",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/experiments/fast_mode/hardware_queue_restart_sampler_island_passband_preopen_20260525.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/experiments/fast_mode/hardware_queue_restart_sampler_island_passband_strict_20260525.csv"),
    )
    parser.add_argument("--payload-bytes", type=int, default=125000)
    parser.add_argument("--header-bytes", type=int, default=8)
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    with args.input.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            run = row["run"].replace("_preopen_20260525", "_strict_20260525")
            out_file = row["out_file"].replace("_preopen_20260525.bin", "_strict_20260525.bin")
            new_row = {field: row.get(field, "") for field in FIELDS}
            new_row.update(
                {
                    "run": run,
                    "bytes": str(args.payload_bytes + args.header_bytes),
                    "out_file": out_file,
                    "analyze_group": "restart_sampler_island_passband_strict_20260525",
                    "notes": (
                        "strict pre-open capture; byte count includes 8-byte "
                        "restart header plus full 1000x125 payload"
                    ),
                }
            )
            rows.append(new_row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
