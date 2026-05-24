#!/usr/bin/env python3
"""Summarize restart byte-aligned sampler snapshots by output byte position.

This is an offline post-processing script. It reads SNAP captures decoded by
``analyze_sampler_snapshot.py`` and aggregates metrics by ``seq % 8`` so each
row corresponds to one output byte position.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path
from typing import Any

from analyze_sampler_snapshot import decode, entropy, sha256_file


SNAP_HEADER_BYTES = 16
SNAP_FRAME_BYTES = 16
SNAP_START = 0x5A
SNAP_END = 0xA5

WARMUP_BITS_TO_FORMAL_BYTES = {
    32: 4,
    40: 5,
    80: 10,
    88: 11,
}

RESTART_REF_STATUS = {
    4: "fail",
    5: "pass",
    10: "pass",
    11: "fail",
}

FIELDS = [
    "label",
    "input",
    "sha256",
    "decode_status",
    "decode_error",
    "formal_warmup_bytes",
    "snapshot_warmup_bits",
    "restart_ref_status",
    "byte_pos",
    "samples",
    "rand_p1",
    "rand_abs_bias",
    "rand_entropy",
    "rand_min_entropy",
    "stage_xor_entropy",
    "stage_xor_min_entropy",
    "sampled_fixed_bits",
    "sampled_heavy_bits",
    "worst_sampled_bit",
    "worst_sampled_p1",
    "worst_sampled_abs_bias",
    "bad_marker_rows",
    "invalid_frames",
]


def parse_header(data: bytes) -> dict[str, int]:
    if len(data) < SNAP_HEADER_BYTES or data[:4] != b"SNAP":
        raise ValueError("missing SNAP header")
    return {
        "version": data[4],
        "variant_id": data[5] | (data[6] << 8),
        "warmup_snapshots": data[7] | (data[8] << 8),
        "capture_snapshots": data[9] | (data[10] << 8),
        "sample_bytes": data[11],
        "ro_num": data[12],
        "sample_stages": data[13],
        "marker0": data[14],
        "marker1": data[15],
    }


def decode_frame(frame: bytes) -> dict[str, int]:
    seq = frame[1] | (frame[2] << 8)
    return {
        "seq": seq,
        "rand_bit": frame[3] & 1,
        "stage_xor": frame[4],
        "snapshot64": int.from_bytes(frame[5:13], "little"),
    }


def scan_snap_frames(path: Path) -> tuple[dict[str, int], list[dict[str, int]], int, int]:
    """Best-effort SNAP frame scan used after strict decode fails."""
    data = path.read_bytes()
    frames: list[dict[str, int]] = []
    bad_marker_rows = 0
    invalid_frames = 0

    try:
        header = parse_header(data)
    except ValueError:
        header = {}
        invalid_frames = 1
        for offset in range(0, max(0, len(data) - SNAP_FRAME_BYTES + 1)):
            frame = data[offset : offset + SNAP_FRAME_BYTES]
            if frame[0] == SNAP_START and frame[15] == SNAP_END:
                frames.append(decode_frame(frame))
        return header, frames, bad_marker_rows, invalid_frames

    declared = header.get("capture_snapshots", 0)
    body = data[SNAP_HEADER_BYTES:]
    complete_frames = len(body) // SNAP_FRAME_BYTES
    trailing_bytes = len(body) % SNAP_FRAME_BYTES
    scan_count = min(complete_frames, declared) if declared else complete_frames

    invalid_frames += max(0, declared - complete_frames)
    invalid_frames += max(0, complete_frames - declared) if declared else 0
    invalid_frames += 1 if trailing_bytes else 0

    for idx in range(scan_count):
        offset = SNAP_HEADER_BYTES + idx * SNAP_FRAME_BYTES
        frame = data[offset : offset + SNAP_FRAME_BYTES]
        if frame[0] != SNAP_START or frame[15] != SNAP_END:
            bad_marker_rows += 1
            invalid_frames += 1
            continue
        frames.append(decode_frame(frame))

    return header, frames, bad_marker_rows, invalid_frames


def read_capture(path: Path) -> tuple[dict[str, int], list[dict[str, int]], str, str, int, int]:
    try:
        header, frames = decode(path)
        return header, frames, "decoded", "", 0, 0
    except Exception as exc:  # noqa: BLE001 - decode failures must not stop batch summaries.
        header, frames, bad_marker_rows, invalid_frames = scan_snap_frames(path)
        status = "scanned_after_decode_error" if frames else "decode_failed"
        return header, frames, status, str(exc), bad_marker_rows, invalid_frames


def infer_warmup_bits(label: str, header: dict[str, int], override: int | None) -> int | None:
    if override is not None:
        return override
    if "warmup_snapshots" in header:
        return header["warmup_snapshots"]
    match = re.search(r"warmup(\d+)", label, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def infer_formal_warmup_bytes(label: str, snapshot_warmup_bits: int | None, override: int | None) -> int | None:
    if override is not None:
        return override
    if snapshot_warmup_bits in WARMUP_BITS_TO_FORMAL_BYTES:
        return WARMUP_BITS_TO_FORMAL_BYTES[snapshot_warmup_bits]
    match = re.search(r"warmup(\d+)", label, re.IGNORECASE)
    if match:
        return WARMUP_BITS_TO_FORMAL_BYTES.get(int(match.group(1)))
    return None


def fnum(value: float | int | None, digits: int = 9) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return f"{value:.{digits}f}" if isinstance(value, float) else str(value)


def summarize_group(frames: list[dict[str, int]], heavy_threshold: float) -> dict[str, Any]:
    n = len(frames)
    if not n:
        return {
            "samples": 0,
            "rand_p1": "",
            "rand_abs_bias": "",
            "rand_entropy": "",
            "rand_min_entropy": "",
            "stage_xor_entropy": "",
            "stage_xor_min_entropy": "",
            "sampled_fixed_bits": "",
            "sampled_heavy_bits": "",
            "worst_sampled_bit": "",
            "worst_sampled_p1": "",
            "worst_sampled_abs_bias": "",
        }

    rand_bits = [row["rand_bit"] for row in frames]
    stage_xors = [row["stage_xor"] for row in frames]
    rand_h, rand_hmin = entropy(rand_bits)
    stage_h, stage_hmin = entropy(stage_xors)
    rand_p1 = sum(rand_bits) / n

    bit_stats: list[tuple[int, float, float]] = []
    for bit in range(64):
        ones = sum((row["snapshot64"] >> bit) & 1 for row in frames)
        p1 = ones / n
        bit_stats.append((bit, p1, abs(p1 - 0.5)))

    fixed_bits = sum(1 for _, p1, _ in bit_stats if p1 == 0.0 or p1 == 1.0)
    heavy_bits = sum(1 for _, _, bias in bit_stats if bias >= heavy_threshold)
    worst_bit, worst_p1, worst_bias = max(bit_stats, key=lambda item: item[2])

    return {
        "samples": n,
        "rand_p1": fnum(rand_p1),
        "rand_abs_bias": fnum(abs(rand_p1 - 0.5)),
        "rand_entropy": fnum(rand_h),
        "rand_min_entropy": fnum(rand_hmin),
        "stage_xor_entropy": fnum(stage_h),
        "stage_xor_min_entropy": fnum(stage_hmin),
        "sampled_fixed_bits": fixed_bits,
        "sampled_heavy_bits": heavy_bits,
        "worst_sampled_bit": worst_bit,
        "worst_sampled_p1": fnum(worst_p1),
        "worst_sampled_abs_bias": fnum(worst_bias),
    }


def summarize_file(
    path: Path,
    label: str,
    formal_warmup_override: int | None,
    snapshot_warmup_override: int | None,
    heavy_threshold: float,
) -> list[dict[str, Any]]:
    input_path = path.resolve()
    header, frames, decode_status, decode_error, bad_marker_rows, invalid_frames = read_capture(input_path)
    snapshot_warmup_bits = infer_warmup_bits(label, header, snapshot_warmup_override)
    formal_warmup_bytes = infer_formal_warmup_bytes(label, snapshot_warmup_bits, formal_warmup_override)
    restart_ref_status = RESTART_REF_STATUS.get(formal_warmup_bytes, "")

    groups = {byte_pos: [] for byte_pos in range(8)}
    for frame in frames:
        groups[frame["seq"] % 8].append(frame)

    rows: list[dict[str, Any]] = []
    digest = sha256_file(input_path) if input_path.exists() else ""
    for byte_pos in range(8):
        row: dict[str, Any] = {
            "label": label,
            "input": str(input_path),
            "sha256": digest,
            "decode_status": decode_status,
            "decode_error": decode_error,
            "formal_warmup_bytes": formal_warmup_bytes if formal_warmup_bytes is not None else "",
            "snapshot_warmup_bits": snapshot_warmup_bits if snapshot_warmup_bits is not None else "",
            "restart_ref_status": restart_ref_status,
            "byte_pos": byte_pos,
            "bad_marker_rows": bad_marker_rows,
            "invalid_frames": invalid_frames,
        }
        row.update(summarize_group(groups[byte_pos], heavy_threshold))
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_cell(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|") if text else ""


def write_md(path: Path, rows: list[dict[str, Any]], out_csv: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    labels = sorted({str(row["label"]) for row in rows})
    invalid_rows = [row for row in rows if row["decode_status"] != "decoded"]
    lines = [
        "# Restart Byte Snapshot Position Summary",
        "",
        f"- CSV: `{out_csv}`",
        f"- labels: {len(labels)}",
        f"- rows: {len(rows)}",
        f"- decode warnings: {len({row['label'] for row in invalid_rows})}",
        "",
        "| label | formal warmup bytes | snapshot warmup bits | ref | byte_pos | samples | rand p1 | rand abs bias | rand H | rand min-H | stage_xor H | stage_xor min-H | fixed bits | heavy bits | worst bit | worst p1 | invalid |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                md_cell(row[field])
                for field in [
                    "label",
                    "formal_warmup_bytes",
                    "snapshot_warmup_bits",
                    "restart_ref_status",
                    "byte_pos",
                    "samples",
                    "rand_p1",
                    "rand_abs_bias",
                    "rand_entropy",
                    "rand_min_entropy",
                    "stage_xor_entropy",
                    "stage_xor_min_entropy",
                    "sampled_fixed_bits",
                    "sampled_heavy_bits",
                    "worst_sampled_bit",
                    "worst_sampled_p1",
                    "invalid_frames",
                ]
            )
            + " |"
        )

    if invalid_rows:
        lines.extend(["", "## Decode Warnings", ""])
        for row in invalid_rows[::8]:
            lines.append(
                f"- `{row['label']}`: {row['decode_status']}; bad_marker_rows={row['bad_marker_rows']}; "
                f"invalid_frames={row['invalid_frames']}; error={row['decode_error']}"
            )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def collect_inputs(args: argparse.Namespace) -> list[Path]:
    inputs = list(args.input or []) + list(args.inputs or [])
    if not inputs:
        raise SystemExit("at least one SNAP bin input is required")
    return inputs


def labels_for_inputs(inputs: list[Path], labels: list[str]) -> list[str]:
    if not labels:
        return [path.stem for path in inputs]
    if len(labels) == 1 and len(inputs) == 1:
        return labels
    if len(labels) == len(inputs):
        return labels
    raise SystemExit("--label may be used once for a single input or once per input")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize SNAP restart byte snapshots by seq %% 8 byte position."
    )
    parser.add_argument("inputs", nargs="*", type=Path, help="SNAP .bin files")
    parser.add_argument("--input", action="append", type=Path, help="SNAP .bin file; may be repeated")
    parser.add_argument("--label", action="append", default=[], help="Label override; repeat to match inputs")
    parser.add_argument("--formal-warmup-bytes", type=int, help="Override formal restart warmup bytes")
    parser.add_argument("--snapshot-warmup-bits", type=int, help="Override snapshot warmup bits")
    parser.add_argument("--heavy-threshold", type=float, default=0.25, help="Sampled-bit abs-bias threshold")
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    inputs = collect_inputs(args)
    labels = labels_for_inputs(inputs, args.label)

    rows: list[dict[str, Any]] = []
    for input_path, label in zip(inputs, labels):
        rows.extend(
            summarize_file(
                input_path,
                label,
                args.formal_warmup_bytes,
                args.snapshot_warmup_bits,
                args.heavy_threshold,
            )
        )

    write_csv(args.out_csv, rows)
    write_md(args.out_md, rows, args.out_csv)
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
