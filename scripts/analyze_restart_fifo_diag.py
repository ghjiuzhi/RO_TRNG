#!/usr/bin/env python3
"""Decode restart FIFO diagnostic captures."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def decode(path: Path) -> tuple[dict[str, int], list[dict[str, int]]]:
    data = path.read_bytes()
    if len(data) < 16 or data[:4] != b"FDIA":
        raise ValueError(f"{path} does not start with FDIA header")
    header = {
        "version": data[4],
        "restart_count": data[5] | (data[6] << 8),
        "row_bytes": data[7] | (data[8] << 8),
        "warmup_bytes": data[9] | (data[10] << 8),
        "pre_warmup_bytes": data[11] | (data[12] << 8),
        "frames": data[13] | (data[14] << 8),
        "marker": data[15],
    }
    expected = 16 + header["frames"] * 16
    if len(data) != expected:
        raise ValueError(f"size mismatch: expected {expected}, got {len(data)}")
    frames = []
    for idx in range(header["frames"]):
        off = 16 + idx * 16
        frame = data[off : off + 16]
        if frame[0] != 0x5A or frame[15] != 0xA5:
            raise ValueError(f"bad frame marker at frame {idx}, offset {off}")
        # The RTL sends read_frame[7:0] first.  The diagnostic frame is packed
        # as {a5, flags, fifo_dout, event_index, phase, row_index, 56'd0, 5a},
        # so the meaningful fields appear near the end of the byte stream.
        row_index = frame[8] | (frame[9] << 8)
        phase = frame[10]
        event_index = frame[11] | (frame[12] << 8)
        fifo_byte = frame[13]
        flags = frame[14]
        frames.append(
            {
                "seq": idx,
                "row_index": row_index,
                "phase": phase,
                "phase_name": "warmup" if phase == 1 else ("send" if phase == 2 else f"unknown_{phase}"),
                "event_index": event_index,
                "fifo_byte": fifo_byte,
                "fifo_empty": (flags >> 1) & 1,
                "fifo_full": (flags >> 2) & 1,
                "ro_en": flags & 1,
            }
        )
    return header, frames


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    label = args.label or args.input.stem
    header, frames = decode(args.input)
    out_dir = args.out_dir
    rows = [{"label": label, **row} for row in frames]
    write_csv(
        out_dir / f"{label}.frames.csv",
        rows,
        ["label", "seq", "row_index", "phase", "phase_name", "event_index", "fifo_byte", "fifo_empty", "fifo_full", "ro_en"],
    )

    send_rows = [row for row in frames if row["phase"] == 2]
    warm_rows = [row for row in frames if row["phase"] == 1]
    md = [
        f"# Restart FIFO Diagnostic: {label}",
        "",
        f"- input: `{args.input}`",
        f"- header: `{header}`",
        f"- frames: `{len(frames)}`",
        f"- warmup frames: `{len(warm_rows)}`",
        f"- send frames: `{len(send_rows)}`",
        "",
    ]
    for phase_name, subset in [("warmup", warm_rows), ("send", send_rows)]:
        if not subset:
            continue
        md.append(f"## {phase_name}")
        md.append("")
        md.append(f"- rows observed: `{len(set(row['row_index'] for row in subset))}`")
        md.append(f"- event index range: `{min(row['event_index'] for row in subset)}` to `{max(row['event_index'] for row in subset)}`")
        md.append(f"- fifo_byte p1: `{sum(row['fifo_byte'].bit_count() for row in subset) / (len(subset) * 8):.9f}`")
        md.append("")
    (out_dir / f"{label}.summary.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_dir / (label + '.summary.md')}")


if __name__ == "__main__":
    main()
