#!/usr/bin/env python3
"""Extract payload bytes from restart auto-stream captures.

The restart auto-stream tops emit an 8-byte header before the row-major
payload:

  A5 5A restart_count[15:8] restart_count[7:0]
        row_bytes[15:8] row_bytes[7:0] version state

This helper keeps formal restart analysis honest by rejecting captures where
the header consumed part of the requested payload byte budget.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


HEADER_LEN = 8
MAGIC = bytes([0xA5, 0x5A])


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def parse_header(data: bytes) -> dict[str, object] | None:
    if len(data) < HEADER_LEN or data[:2] != MAGIC:
        return None
    restart_count = (data[2] << 8) | data[3]
    row_bytes = (data[4] << 8) | data[5]
    return {
        "header_hex": data[:HEADER_LEN].hex().upper(),
        "restart_count": restart_count,
        "row_bytes": row_bytes,
        "version": data[6],
        "state": data[7],
    }


def write_metadata(path: Path, metadata: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--restart-count", type=int, required=True)
    parser.add_argument("--row-bytes", type=int, required=True)
    parser.add_argument("--metadata", type=Path, default=None)
    parser.add_argument(
        "--diagnostic-trim-complete-rows",
        action="store_true",
        help=(
            "For incomplete captures, write only complete post-header rows and "
            "mark the output as diagnostic-only. Do not feed this to SP800-90B."
        ),
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_path = args.output.resolve()
    metadata_path = (
        args.metadata.resolve()
        if args.metadata
        else output_path.with_suffix(output_path.suffix + ".metadata.json")
    )
    payload_expected = args.restart_count * args.row_bytes
    data = input_path.read_bytes()
    header = parse_header(data)
    mode = ""
    status = "ok"
    diagnostic_only = False
    rows_written = args.restart_count
    payload = b""
    error = ""

    try:
        if header is not None:
            if header["restart_count"] != args.restart_count or header["row_bytes"] != args.row_bytes:
                raise ValueError(
                    "header shape mismatch: "
                    f"header={header['restart_count']}x{header['row_bytes']} "
                    f"expected={args.restart_count}x{args.row_bytes}"
                )
            available = len(data) - HEADER_LEN
            if available == payload_expected:
                payload = data[HEADER_LEN:]
                mode = "stripped_header_strict"
            elif args.diagnostic_trim_complete_rows and available > 0:
                rows_written = available // args.row_bytes
                if rows_written <= 0:
                    raise ValueError("not enough post-header bytes for one complete row")
                payload = data[HEADER_LEN : HEADER_LEN + rows_written * args.row_bytes]
                mode = "stripped_header_diagnostic_complete_rows"
                diagnostic_only = True
                status = "diagnostic_only"
            else:
                raise ValueError(
                    f"incomplete payload after header: expected {payload_expected}, "
                    f"available {available}; capture should request {payload_expected + HEADER_LEN} bytes"
                )
        else:
            if len(data) != payload_expected:
                raise ValueError(
                    f"payload-only size mismatch: expected {payload_expected}, got {len(data)}"
                )
            payload = data
            mode = "payload_only_strict"
    except Exception as exc:
        status = "failed"
        error = str(exc)

    metadata: dict[str, object] = {
        "input_file": str(input_path),
        "input_sha256": sha256_file(input_path),
        "input_bytes": len(data),
        "output_file": str(output_path),
        "restart_count_expected": args.restart_count,
        "row_bytes_expected": args.row_bytes,
        "payload_bytes_expected": payload_expected,
        "header": header,
        "mode": mode,
        "status": status,
        "diagnostic_only": diagnostic_only,
        "rows_written": rows_written if payload else 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error": error,
    }

    if status != "failed":
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
        tmp_path.write_bytes(payload)
        tmp_path.replace(output_path)
        metadata.update(
            {
                "output_sha256": sha256_file(output_path),
                "output_bytes": output_path.stat().st_size,
            }
        )
        output_path.with_suffix(output_path.suffix + ".sha256.txt").write_text(
            f"{metadata['output_sha256']}  {output_path}\n", encoding="ascii"
        )

    write_metadata(metadata_path, metadata)
    print(json.dumps(metadata, indent=2))
    if status == "failed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
