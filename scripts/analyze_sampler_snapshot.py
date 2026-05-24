#!/usr/bin/env python3
"""Decode sampler-register snapshot diagnostic captures."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def entropy(values: list[int]) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    total = len(values)
    counts = Counter(values)
    probs = [count / total for count in counts.values()]
    return -sum(p * math.log2(p) for p in probs), -math.log2(max(probs))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def decode(path: Path) -> tuple[dict[str, int], list[dict[str, int]]]:
    data = path.read_bytes()
    if len(data) < 16 or data[:4] != b"SNAP":
        raise ValueError(f"{path} does not start with SNAP header")
    header = {
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
    frame_bytes = 16
    expected = 16 + header["capture_snapshots"] * frame_bytes
    if len(data) != expected:
        raise ValueError(f"size mismatch: expected {expected}, got {len(data)}")
    rows: list[dict[str, int]] = []
    offset = 16
    for _ in range(header["capture_snapshots"]):
        frame = data[offset : offset + frame_bytes]
        offset += frame_bytes
        if frame[0] != 0x5A or frame[15] != 0xA5:
            raise ValueError(f"bad frame marker at offset {offset - frame_bytes}")
        seq = frame[1] | (frame[2] << 8)
        snapshot = int.from_bytes(frame[5:13], "little")
        rows.append(
            {
                "seq": seq,
                "rand_bit": frame[3] & 1,
                "stage_xor": frame[4],
                "snapshot64": snapshot,
            }
        )
    return header, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    input_path = args.input.resolve()
    out_dir = args.out_dir.resolve()
    label = args.label or input_path.stem
    header, frames = decode(input_path)

    frame_rows = []
    rand_bits = []
    stage_xors = []
    bit_ones = [0] * 64
    stage_xor_ones = [0] * 8
    for row in frames:
        snapshot = row["snapshot64"]
        rand_bits.append(row["rand_bit"])
        stage_xors.append(row["stage_xor"])
        out = {
            "label": label,
            "seq": row["seq"],
            "rand_bit": row["rand_bit"],
            "stage_xor_hex": f"{row['stage_xor']:02X}",
            "snapshot64_hex": f"{snapshot:016X}",
        }
        for bit in range(64):
            value = (snapshot >> bit) & 1
            bit_ones[bit] += value
            out[f"b{bit:02d}"] = value
        for bit in range(8):
            value = (row["stage_xor"] >> bit) & 1
            stage_xor_ones[bit] += value
            out[f"sx{bit}"] = value
        frame_rows.append(out)

    n = len(frames)
    bit_rows = []
    for bit, ones in enumerate(bit_ones):
        p1 = ones / n if n else math.nan
        bit_rows.append(
            {
                "label": label,
                "bit_index": bit,
                "line": bit // 8,
                "data_ro": bit % 8,
                "ones": ones,
                "zeros": n - ones,
                "p1": f"{p1:.9f}",
                "abs_bias": f"{abs(p1 - 0.5):.9f}",
            }
        )
    bit_rows.sort(key=lambda r: float(r["abs_bias"]), reverse=True)

    stage_rows = []
    for bit, ones in enumerate(stage_xor_ones):
        p1 = ones / n if n else math.nan
        stage_rows.append(
            {
                "label": label,
                "stage": bit,
                "ones": ones,
                "zeros": n - ones,
                "p1": f"{p1:.9f}",
                "abs_bias": f"{abs(p1 - 0.5):.9f}",
            }
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    frame_fields = ["label", "seq", "rand_bit", "stage_xor_hex", "snapshot64_hex"] + [f"b{i:02d}" for i in range(64)] + [f"sx{i}" for i in range(8)]
    write_csv(out_dir / f"{label}.frames.csv", frame_rows, frame_fields)
    write_csv(out_dir / f"{label}.bit_bias.csv", bit_rows, ["label", "bit_index", "line", "data_ro", "ones", "zeros", "p1", "abs_bias"])
    write_csv(out_dir / f"{label}.stage_xor_bias.csv", stage_rows, ["label", "stage", "ones", "zeros", "p1", "abs_bias"])

    h_rand, hmin_rand = entropy(rand_bits)
    h_stage, hmin_stage = entropy(stage_xors)
    summary = {
        "label": label,
        "input": str(input_path),
        "sha256": sha256_file(input_path),
        **header,
        "frames": n,
        "rand_p1": sum(rand_bits) / n if n else math.nan,
        "rand_entropy": h_rand,
        "rand_min_entropy": hmin_rand,
        "stage_xor_entropy": h_stage,
        "stage_xor_min_entropy": hmin_stage,
        "worst_sampled_bit": bit_rows[0] if bit_rows else {},
        "worst_stage_xor": max(stage_rows, key=lambda r: float(r["abs_bias"])) if stage_rows else {},
    }
    (out_dir / f"{label}.summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        f"# Sampler Snapshot: {label}",
        "",
        f"- input: `{input_path}`",
        f"- SHA256: `{summary['sha256']}`",
        f"- header: variant `{header['variant_id']}`, warmup `{header['warmup_snapshots']}`, frames `{n}`, sample bytes `{header['sample_bytes']}`",
        f"- rand p1: `{summary['rand_p1']:.9f}`",
        f"- rand entropy/min-H: `{summary['rand_entropy']:.6f}` / `{summary['rand_min_entropy']:.6f}`",
        f"- stage_xor entropy/min-H: `{summary['stage_xor_entropy']:.6f}` / `{summary['stage_xor_min_entropy']:.6f}`",
        f"- worst sampled bit: `{summary['worst_sampled_bit']}`",
        f"- worst stage xor: `{summary['worst_stage_xor']}`",
        "",
        "## Outputs",
        "",
        f"- frames: `{label}.frames.csv`",
        f"- bit bias: `{label}.bit_bias.csv`",
        f"- stage XOR bias: `{label}.stage_xor_bias.csv`",
    ]
    (out_dir / f"{label}.summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {out_dir / (label + '.summary.md')}")


if __name__ == "__main__":
    main()
