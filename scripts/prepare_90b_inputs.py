#!/usr/bin/env python3
"""Prepare local SP800-90B EntropyAssessment input files.

This script is intentionally offline-only. It does not invoke Vivado, hardware
servers, serial ports, JTAG, or the EntropyAssessment binaries. It only slices
existing capture files and writes one-byte-per-symbol datasets plus a manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_INPUTS = [
    Path("data/hardware/20260511_fpga1_board1/trng/original_fpga1_run01_10mib.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/random1_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/random2_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/random3_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/compact_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/sparse_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/row_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/same_column_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/checker_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/far_run01.bin"),
    Path("data/hardware/20260511_fpga1_board1/trng/cross_region_run02.bin"),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unpack_lsb_first(data: bytes) -> bytes:
    out = bytearray(len(data) * 8)
    index = 0
    for byte in data:
        for bit in range(8):
            out[index] = (byte >> bit) & 1
            index += 1
    return bytes(out)


def unpack_msb_first(data: bytes) -> bytes:
    out = bytearray(len(data) * 8)
    index = 0
    for byte in data:
        for bit in range(7, -1, -1):
            out[index] = (byte >> bit) & 1
            index += 1
    return bytes(out)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for idx in range(2, 10000):
        candidate = path.with_name(f"{stem}_{idx}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find a unique path for {path}")


def prepare_one(
    src: Path,
    out_dir: Path,
    max_bytes: int | None,
    offset: int,
    modes: list[str],
    overwrite: bool,
) -> list[dict[str, str | int]]:
    if not src.is_file():
        raise FileNotFoundError(src)
    if offset < 0:
        raise ValueError("--offset-bytes must be non-negative")

    with src.open("rb") as f:
        if offset:
            f.seek(offset)
        data = f.read(max_bytes if max_bytes is not None else -1)

    if not data:
        raise ValueError(f"No data read from {src}")

    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []
    source_hash = sha256_file(src)
    source_name = src.stem

    for mode in modes:
        if mode == "byte-symbols":
            payload = data
            bits_per_symbol = 8
            suffix = "bps8"
        elif mode == "bit-symbols-msb":
            payload = unpack_msb_first(data)
            bits_per_symbol = 1
            suffix = "bps1_msb"
        elif mode == "bit-symbols-lsb":
            payload = unpack_lsb_first(data)
            bits_per_symbol = 1
            suffix = "bps1_lsb"
        else:
            raise ValueError(f"Unknown mode: {mode}")

        out_path = out_dir / f"{source_name}_{suffix}.bin"
        if not overwrite:
            out_path = unique_path(out_path)
        out_path.write_bytes(payload)
        rows.append(
            {
                "source": str(src),
                "source_sha256": source_hash,
                "source_bytes": src.stat().st_size,
                "offset_bytes": offset,
                "read_bytes": len(data),
                "mode": mode,
                "bits_per_symbol": bits_per_symbol,
                "output": str(out_path),
                "output_bytes": len(payload),
                "output_sha256": sha256_file(out_path),
            }
        )

    return rows


def write_manifest(out_dir: Path, rows: list[dict[str, str | int]]) -> None:
    csv_path = out_dir / "manifest.csv"
    json_path = out_dir / "manifest.json"
    fields = [
        "source",
        "source_sha256",
        "source_bytes",
        "offset_bytes",
        "read_bytes",
        "mode",
        "bits_per_symbol",
        "output",
        "output_bytes",
        "output_sha256",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Prepared for local SP800-90B EntropyAssessment runs; no tests were executed.",
        "rows": rows,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Raw capture .bin files. Defaults to complete 10 MiB TRNG formal runs.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/sp800_90b/inputs_20260514"),
        help="Output directory for 90B input files and manifest.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=1_000_000,
        help="Bytes to read from each source file. Use 0 for the full file.",
    )
    parser.add_argument("--offset-bytes", type=int, default=0, help="Byte offset into each source file.")
    parser.add_argument(
        "--mode",
        choices=["byte-symbols", "bit-symbols-msb", "bit-symbols-lsb"],
        action="append",
        default=None,
        help="Output representation. Repeat to write several representations.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output filenames.")
    args = parser.parse_args()

    max_bytes = None if args.max_bytes == 0 else args.max_bytes
    if max_bytes is not None and max_bytes < 0:
        raise SystemExit("--max-bytes must be non-negative")

    inputs = args.inputs or DEFAULT_INPUTS
    modes = args.mode or ["bit-symbols-msb", "byte-symbols"]
    rows: list[dict[str, str | int]] = []
    for src in inputs:
        rows.extend(prepare_one(src, args.out_dir, max_bytes, args.offset_bytes, modes, args.overwrite))
    write_manifest(args.out_dir, rows)
    print(f"Wrote {len(rows)} prepared files under {args.out_dir}")
    print(f"Wrote {args.out_dir / 'manifest.csv'}")
    print(f"Wrote {args.out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
