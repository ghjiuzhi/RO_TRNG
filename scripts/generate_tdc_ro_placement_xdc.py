#!/usr/bin/env python3
"""Generate placement constraints for the two RO probes in RO_TDC_sysclk_top."""

from __future__ import annotations

import argparse
from pathlib import Path


BELS = ["A6LUT", "B6LUT", "C6LUT", "D6LUT"]


def ro_cells(instance: str, stages: int) -> list[str]:
    cells = [f"{instance}/RO_NAND.u_LUT6_nand2_1/u_LUT6"]
    cells.extend(f"{instance}/RO_STAGE_LOOP[{i}].u_LUT6_not1/u_LUT6" for i in range(stages - 1))
    return cells


def emit_cell(cell: str, x: int, y: int, bel: str) -> list[str]:
    filt = f"[get_cells -hierarchical -filter {{NAME =~ *{cell}}}]"
    return [
        f"set_property LOC SLICE_X{x}Y{y} {filt}",
        f"set_property BEL {bel} {filt}",
    ]


def emit_ro(instance: str, stages: int, x0: int, y0: int, stride: int) -> list[str]:
    lines = [f"# {instance}: stages={stages}, origin=SLICE_X{x0}Y{y0}"]
    for i, cell in enumerate(ro_cells(instance, stages)):
        slice_index = i // len(BELS)
        bel = BELS[i % len(BELS)]
        lines.extend(emit_cell(cell, x0 + slice_index * stride, y0, bel))
    return lines


def origins(pattern: str, x0: int, y0: int, distance: int) -> tuple[tuple[int, int], tuple[int, int]]:
    if pattern == "near":
        return (x0, y0), (x0 + 3, y0)
    if pattern == "same_column":
        return (x0, y0), (x0, y0 + distance)
    if pattern == "far":
        return (x0, y0), (x0 + distance, y0 + distance)
    if pattern == "vertical_far":
        return (x0, y0), (x0, y0 + distance)
    raise ValueError(f"Unknown pattern: {pattern}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", choices=["near", "same_column", "far", "vertical_far"], default="near")
    parser.add_argument("--x0", type=int, default=36)
    parser.add_argument("--y0", type=int, default=35)
    parser.add_argument("--distance", type=int, default=30)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    (ax, ay), (bx, by) = origins(args.pattern, args.x0, args.y0, args.distance)
    lines = [
        "################################################################",
        "# Auto-generated TDC RO placement constraints",
        f"# pattern={args.pattern}, x0={args.x0}, y0={args.y0}, distance={args.distance}, stride={args.stride}",
        "################################################################",
        "",
    ]
    lines.extend(emit_ro("u_ro_a", 9, ax, ay, args.stride))
    lines.append("")
    lines.extend(emit_ro("u_ro_b", 7, bx, by, args.stride))
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
