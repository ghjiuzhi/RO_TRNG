#!/usr/bin/env python3
"""Generate RO frequency probe placement XDC from an existing TRNG matrix XDC."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BELS = ["A6LUT", "B6LUT", "C6LUT", "D6LUT"]
RO_COMMENT_RE = re.compile(r"# RO(?P<index>\d+) at SLICE_X(?P<x>\d+)Y(?P<y>\d+)")


def parse_ro_comments(path: Path) -> list[tuple[int, int, int]]:
    coords: list[tuple[int, int, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = RO_COMMENT_RE.match(line.strip())
        if match:
            coords.append((int(match.group("index")), int(match.group("x")), int(match.group("y"))))
    if len(coords) != 8:
        raise SystemExit(f"Expected 8 RO comments in {path}, found {len(coords)}.")
    return sorted(coords)


def emit_sample_ro(x0: int, y0: int, stride: int) -> list[str]:
    cells = ["RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6"]
    cells.extend(f"RO_SAMPLE_LOOP[{i}].u_LUT6_not1/u_LUT6" for i in range(8))

    lines = [f"# sample RO at SLICE_X{x0}Y{y0}, stages=9"]
    for stage, cell in enumerate(cells):
        x = x0 + (stage // len(BELS)) * stride
        y = y0
        bel = BELS[stage % len(BELS)]
        filt = f"[get_cells -hierarchical -filter {{NAME =~ *u_entropy_source/{cell}}}]"
        lines.append(f"set_property LOC SLICE_X{x}Y{y} {filt}")
        lines.append(f"set_property BEL {bel} {filt}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-xdc", type=Path, required=True)
    parser.add_argument("--sample-x", type=int, default=36)
    parser.add_argument("--sample-y", type=int, default=35)
    parser.add_argument("--sample-stride", type=int, default=1)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    coords = parse_ro_comments(args.matrix_xdc)
    source = args.matrix_xdc.read_text(encoding="utf-8").splitlines()

    lines = [
        "################################################################",
        "# Auto-generated RO frequency probe placement constraints",
        f"# matrix_xdc={args.matrix_xdc.as_posix()}",
        "# Data RO constraints are copied from the matrix XDC. The probe RTL",
        "# intentionally keeps instance name u_entropy_source and generate labels",
        "# compatible with RO_TRNG_top entropy_source placement constraints.",
        "################################################################",
        "",
        "# Data RO coordinates copied from source:",
    ]
    for index, x, y in coords:
        lines.append(f"# RO{index}: SLICE_X{x}Y{y}")
    lines.append("")

    copying = False
    for line in source:
        stripped = line.strip()
        if stripped.startswith("# RO"):
            copying = True
        if copying and stripped:
            lines.append(line)
        elif copying and not stripped:
            lines.append("")

    lines.append("")
    lines.extend(emit_sample_ro(args.sample_x, args.sample_y, args.sample_stride))
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
