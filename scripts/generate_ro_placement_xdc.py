#!/usr/bin/env python3
"""Generate LOC/BEL constraints for entropy_source RO placement sweeps."""

from __future__ import annotations

import argparse
import random
from pathlib import Path


BEL_PAIRS = [("A6LUT", "B6LUT"), ("C6LUT", "D6LUT")]


def cell_filter(ro_index: int, stage: str) -> str:
    return f"[get_cells -hierarchical -filter {{NAME =~ *u_entropy_source/RO_NUM_LOOP[{ro_index}].{stage}/u_LUT6}}]"


def emit_ro(ro_index: int, x: int, y: int, pair_index: int) -> list[str]:
    first_bel, second_bel = BEL_PAIRS[pair_index % len(BEL_PAIRS)]
    lines = [f"# RO{ro_index} at SLICE_X{x}Y{y}"]
    first_stage = "RO_AND.u_LUT6_and2_1"  # RO_STAGES=2 in the current top-level.
    second_stage = "RO_STAGE_LOOP[0].u_LUT6_not1"
    lines.append(f"set_property LOC SLICE_X{x}Y{y} {cell_filter(ro_index, first_stage)}")
    lines.append(f"set_property BEL {first_bel} {cell_filter(ro_index, first_stage)}")
    lines.append(f"set_property LOC SLICE_X{x}Y{y} {cell_filter(ro_index, second_stage)}")
    lines.append(f"set_property BEL {second_bel} {cell_filter(ro_index, second_stage)}")
    return lines


def coordinates(pattern: str, x0: int, y0: int, ro_num: int, pitch: int, seed: int) -> list[tuple[int, int, int]]:
    coords: list[tuple[int, int, int]] = []
    if pattern == "compact":
        for i in range(ro_num):
            coords.append((x0 + (i % 4), y0 + (i // 4), 0))
    elif pattern == "row":
        for i in range(ro_num):
            coords.append((x0 + i * pitch, y0, 0))
    elif pattern in ("checker", "sparse"):
        for i in range(ro_num):
            coords.append((x0 + (i % 4) * pitch, y0 + (i // 4) * pitch, i))
    elif pattern in ("column", "same_column"):
        for i in range(ro_num):
            coords.append((x0, y0 + i * pitch, 0))
    elif pattern == "cross_region":
        for i in range(ro_num):
            band = i % 2
            lane = i // 2
            coords.append((x0 + lane * pitch, y0 + band * 30, i))
    elif pattern == "far":
        far_points = [
            (x0, y0),
            (x0 + 12, y0),
            (x0, y0 + 30),
            (x0 + 12, y0 + 30),
            (x0 + 24, y0),
            (x0 + 24, y0 + 30),
            (x0 + 36, y0),
            (x0 + 36, y0 + 30),
        ]
        for i in range(ro_num):
            x, y = far_points[i % len(far_points)]
            coords.append((x, y, i))
    elif pattern == "random":
        rng = random.Random(seed)
        used: set[tuple[int, int]] = set()
        while len(coords) < ro_num:
            x = x0 + rng.randrange(0, max(1, pitch * 4))
            y = y0 + rng.randrange(0, max(1, pitch * 4))
            if (x, y) in used:
                continue
            used.add((x, y))
            coords.append((x, y, len(coords)))
    else:
        raise ValueError(f"Unknown pattern: {pattern}")
    return coords


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pattern",
        choices=["compact", "row", "column", "same_column", "checker", "sparse", "cross_region", "far", "random"],
        default="compact",
    )
    parser.add_argument("--x0", type=int, default=44)
    parser.add_argument("--y0", type=int, default=43)
    parser.add_argument("--ro-num", type=int, default=8)
    parser.add_argument("--pitch", type=int, default=2)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    lines = [
        "################################################################",
        "# Auto-generated RO placement constraints",
        f"# pattern={args.pattern}, x0={args.x0}, y0={args.y0}, ro_num={args.ro_num}, pitch={args.pitch}, seed={args.seed}",
        "# Assumes entropy_source.RO_STAGES == 2 and RO_TRNG_top instance name u_entropy_source.",
        "################################################################",
        "",
    ]
    for ro_index, (x, y, pair_index) in enumerate(coordinates(args.pattern, args.x0, args.y0, args.ro_num, args.pitch, args.seed)):
        lines.extend(emit_ro(ro_index, x, y, pair_index))
        lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
