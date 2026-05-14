#!/usr/bin/env python3
"""Expand a row-major restart byte dataset into one-byte bit symbols.

The input is assumed to be row-major bytes:
  row r contains symbols_per_restart captured UART bytes.

The output is row-major one-byte bit symbols:
  row r contains symbols_per_restart * 8 bytes, each 0x00 or 0x01.

This is a format conversion helper only. It does not turn an ordinary
sequential capture into a restart dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def expand_byte(byte: int, order: str) -> list[int]:
    if order == "msb":
        return [(byte >> bit) & 1 for bit in range(7, -1, -1)]
    if order == "lsb":
        return [(byte >> bit) & 1 for bit in range(8)]
    raise ValueError(f"unknown bit order: {order}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--restart-count", type=int, required=True)
    parser.add_argument("--symbols-per-restart", type=int, required=True)
    parser.add_argument("--bit-order", choices=("msb", "lsb"), default="msb")
    parser.add_argument("--metadata", type=Path, default=None)
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_path = args.output.resolve()
    metadata_path = args.metadata.resolve() if args.metadata else output_path.with_suffix(output_path.suffix + ".metadata.json")

    expected_input = args.restart_count * args.symbols_per_restart
    input_size = input_path.stat().st_size
    if input_size != expected_input:
        raise SystemExit(
            f"input size mismatch: expected {expected_input} bytes "
            f"({args.restart_count} x {args.symbols_per_restart}), got {input_size}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    if tmp_path.exists():
        tmp_path.unlink()

    start = datetime.now()
    with input_path.open("rb") as src, tmp_path.open("wb") as dst:
        for _row in range(args.restart_count):
            row = src.read(args.symbols_per_restart)
            if len(row) != args.symbols_per_restart:
                raise SystemExit("short row while reading input")
            expanded = bytearray()
            for value in row:
                expanded.extend(expand_byte(value, args.bit_order))
            dst.write(expanded)
    tmp_path.replace(output_path)
    end = datetime.now()

    output_size = output_path.stat().st_size
    expected_output = expected_input * 8
    if output_size != expected_output:
        raise SystemExit(f"output size mismatch: expected {expected_output}, got {output_size}")

    metadata = {
        "dataset_type": "SP800-90B restart bit-symbol dataset",
        "conversion": "row-preserving byte-to-bit expansion",
        "input_file": str(input_path),
        "input_sha256": sha256_file(input_path),
        "input_bytes": input_size,
        "output_file": str(output_path),
        "output_sha256": sha256_file(output_path),
        "output_bytes": output_size,
        "restart_count": args.restart_count,
        "input_symbols_per_restart": args.symbols_per_restart,
        "output_symbols_per_restart": args.symbols_per_restart * 8,
        "bits_per_symbol": 1,
        "bit_order": args.bit_order,
        "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": round((end - start).total_seconds(), 3),
        "notes": (
            "This preserves restart row boundaries. It is only valid if the input "
            "was collected as an actual restart dataset."
        ),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    output_path.with_suffix(output_path.suffix + ".sha256.txt").write_text(
        f"{metadata['output_sha256']}  {output_path}\n", encoding="ascii"
    )

    print(f"Wrote {output_path}")
    print(f"Wrote {metadata_path}")
    print(f"SHA256 {metadata['output_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
