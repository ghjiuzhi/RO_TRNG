#!/usr/bin/env python3
"""Analyze fixed-column bias in a packed SP800-90B restart matrix.

The input is a row-major packed-byte restart dataset:
  restart_count rows, bytes_per_restart bytes per row.

For each original byte position and bit position, this script counts how
many of the restart rows contain a one. It also reports the column index
that the bit would occupy after row-preserving MSB-first or LSB-first
byte-to-bit expansion.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
from datetime import datetime
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def color_for_deviation(p1: float) -> str:
    # White near 0.5, red when biased to 1, blue when biased to 0.
    deviation = max(-0.5, min(0.5, p1 - 0.5))
    strength = min(1.0, abs(deviation) / 0.2)
    base = int(255 * (1.0 - 0.75 * strength))
    if deviation >= 0:
        return f"rgb(255,{base},{base})"
    return f"rgb({base},{base},255)"


def write_svg_heatmap(
    path: Path,
    cells: list[dict[str, object]],
    bytes_per_restart: int,
    title: str,
) -> None:
    cell_w = 7
    cell_h = 20
    left = 84
    top = 58
    bit_label_w = 28
    width = left + bytes_per_restart * cell_w + 24
    height = top + 8 * cell_h + 70

    cell_by_pos = {
        (int(row["byte_index"]), int(row["bit_index"])): row
        for row in cells
    }

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="16" y="24" font-family="Arial, sans-serif" font-size="16" font-weight="700">{html.escape(title)}</text>',
        '<text x="16" y="43" font-family="Arial, sans-serif" font-size="12" fill="#444">color encodes p(1): blue &lt; 0.5, white near 0.5, red &gt; 0.5</text>',
    ]

    for bit in range(7, -1, -1):
        y = top + (7 - bit) * cell_h
        parts.append(
            f'<text x="{left - bit_label_w}" y="{y + 14}" font-family="Arial, sans-serif" '
            f'font-size="11" text-anchor="end">bit{bit}</text>'
        )
        for byte_idx in range(bytes_per_restart):
            row = cell_by_pos[(byte_idx, bit)]
            x = left + byte_idx * cell_w
            p1 = float(row["p1"])
            fill = color_for_deviation(p1)
            tooltip = (
                f"byte {byte_idx}, bit {bit}: ones={row['ones']}, "
                f"zeros={row['zeros']}, p1={p1:.4f}, x={row['x']}"
            )
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
                f'fill="{fill}" stroke="#eee" stroke-width="0.4"><title>{html.escape(tooltip)}</title></rect>'
            )

    for byte_idx in range(0, bytes_per_restart, 10):
        x = left + byte_idx * cell_w
        parts.append(
            f'<text x="{x}" y="{top + 8 * cell_h + 16}" font-family="Arial, sans-serif" '
            f'font-size="9" text-anchor="middle">{byte_idx}</text>'
        )
        parts.append(
            f'<line x1="{x}" y1="{top - 4}" x2="{x}" y2="{top + 8 * cell_h}" '
            f'stroke="#bbb" stroke-width="0.5"/>'
        )

    parts.append(
        f'<text x="{left + bytes_per_restart * cell_w / 2}" y="{top + 8 * cell_h + 38}" '
        f'font-family="Arial, sans-serif" font-size="12" text-anchor="middle">original byte index within restart row</text>'
    )
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--restart-count", required=True, type=int)
    parser.add_argument("--bytes-per-restart", required=True, type=int)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--label", default="")
    parser.add_argument("--x-cutoff", type=int, default=0)
    args = parser.parse_args()

    input_path = args.input.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    expected_size = args.restart_count * args.bytes_per_restart
    actual_size = input_path.stat().st_size
    if actual_size != expected_size:
        raise SystemExit(
            f"input size mismatch: expected {expected_size} bytes "
            f"({args.restart_count} x {args.bytes_per_restart}), got {actual_size}"
        )

    counts = [[0 for _bit in range(8)] for _byte in range(args.bytes_per_restart)]
    row_ones: list[int] = []
    with input_path.open("rb") as f:
        for _row_idx in range(args.restart_count):
            row = f.read(args.bytes_per_restart)
            if len(row) != args.bytes_per_restart:
                raise SystemExit("short row")
            ones_in_row = 0
            for byte_idx, value in enumerate(row):
                ones_in_row += value.bit_count()
                for bit_idx in range(8):
                    counts[byte_idx][bit_idx] += (value >> bit_idx) & 1
            row_ones.append(ones_in_row)

    raw_rows: list[dict[str, object]] = []
    expanded_rows: list[dict[str, object]] = []
    worst = None
    for byte_idx in range(args.bytes_per_restart):
        for bit_idx in range(8):
            ones = counts[byte_idx][bit_idx]
            zeros = args.restart_count - ones
            x = max(ones, zeros)
            p1 = ones / args.restart_count
            row = {
                "byte_index": byte_idx,
                "bit_index": bit_idx,
                "ones": ones,
                "zeros": zeros,
                "p1": f"{p1:.9f}",
                "abs_bias": f"{abs(p1 - 0.5):.9f}",
                "x": x,
                "msb_expanded_column": byte_idx * 8 + (7 - bit_idx),
                "lsb_expanded_column": byte_idx * 8 + bit_idx,
                "over_x_cutoff": bool(args.x_cutoff and x > args.x_cutoff),
            }
            raw_rows.append(row)
            expanded_rows.append({
                "bit_order": "msb",
                "expanded_column": row["msb_expanded_column"],
                **row,
            })
            expanded_rows.append({
                "bit_order": "lsb",
                "expanded_column": row["lsb_expanded_column"],
                **row,
            })
            if worst is None or x > int(worst["x"]):
                worst = row

    raw_rows.sort(key=lambda r: (int(r["byte_index"]), int(r["bit_index"])))
    expanded_rows.sort(key=lambda r: (str(r["bit_order"]), int(r["expanded_column"])))
    ranked_rows = sorted(raw_rows, key=lambda r: int(r["x"]), reverse=True)

    raw_fields = [
        "byte_index",
        "bit_index",
        "ones",
        "zeros",
        "p1",
        "abs_bias",
        "x",
        "msb_expanded_column",
        "lsb_expanded_column",
        "over_x_cutoff",
    ]
    expanded_fields = ["bit_order", "expanded_column"] + raw_fields
    write_csv(out_dir / "raw_byte_bit_counts.csv", raw_rows, raw_fields)
    write_csv(out_dir / "expanded_column_counts.csv", expanded_rows, expanded_fields)
    write_csv(out_dir / "top_biased_positions.csv", ranked_rows[:32], raw_fields)
    write_svg_heatmap(
        out_dir / "restart_byte_bit_heatmap.svg",
        raw_rows,
        args.bytes_per_restart,
        args.label or input_path.name,
    )

    total_bits = args.restart_count * args.bytes_per_restart * 8
    total_ones = sum(sum(bit_counts) for bit_counts in counts)
    row_mean = sum(row_ones) / len(row_ones)
    row_var = sum((x - row_mean) ** 2 for x in row_ones) / len(row_ones)
    summary = {
        "analysis": "packed restart byte/bit column bias",
        "label": args.label,
        "input_file": str(input_path),
        "input_sha256": sha256_file(input_path),
        "input_bytes": actual_size,
        "restart_count": args.restart_count,
        "bytes_per_restart": args.bytes_per_restart,
        "expanded_symbols_per_restart": args.bytes_per_restart * 8,
        "total_bits": total_bits,
        "total_ones": total_ones,
        "overall_p1": total_ones / total_bits,
        "row_ones_mean": row_mean,
        "row_ones_std": math.sqrt(row_var),
        "x_cutoff": args.x_cutoff,
        "positions_over_x_cutoff": sum(1 for row in raw_rows if bool(row["over_x_cutoff"])),
        "worst_position": worst,
        "interpretation_hint": (
            "For a packed input byte, MSB expansion maps bit b to column byte*8+(7-b); "
            "LSB expansion maps bit b to column byte*8+b."
        ),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "outputs": {
            "raw_byte_bit_counts_csv": str(out_dir / "raw_byte_bit_counts.csv"),
            "expanded_column_counts_csv": str(out_dir / "expanded_column_counts.csv"),
            "top_biased_positions_csv": str(out_dir / "top_biased_positions.csv"),
            "heatmap_svg": str(out_dir / "restart_byte_bit_heatmap.svg"),
        },
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        f"# Restart Column Bias: {args.label or input_path.name}",
        "",
        f"- input: `{input_path}`",
        f"- SHA256: `{summary['input_sha256']}`",
        f"- matrix: `{args.restart_count} x {args.bytes_per_restart}` packed bytes",
        f"- expanded columns: `{args.bytes_per_restart * 8}` bit positions per restart",
        f"- overall p1: `{summary['overall_p1']:.9f}`",
        f"- worst raw position: byte `{worst['byte_index']}`, bit `{worst['bit_index']}`, "
        f"ones `{worst['ones']}`, zeros `{worst['zeros']}`, x `{worst['x']}`",
        f"- MSB expanded column: `{worst['msb_expanded_column']}`",
        f"- LSB expanded column: `{worst['lsb_expanded_column']}`",
        "",
        "The CSV files preserve the raw byte/bit mapping so the same physical bit position can be compared across MSB-first and LSB-first SP800-90B input conversions.",
    ]
    (out_dir / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {out_dir / 'summary.json'}")
    print(f"Worst: byte={worst['byte_index']} bit={worst['bit_index']} x={worst['x']} p1={worst['p1']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
