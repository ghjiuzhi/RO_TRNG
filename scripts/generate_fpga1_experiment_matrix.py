#!/usr/bin/env python3
"""Generate the first fpga1 RO placement matrix for layout/entropy experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


MATRIX = [
    ("compact_x44y43", "compact", 44, 43, 2, 1),
    ("checker_pitch3_x44y43", "checker", 44, 43, 3, 1),
    ("same_column_pitch3_x44y35", "same_column", 44, 35, 3, 1),
    ("row_pitch3_x38y43", "row", 38, 43, 3, 1),
    ("sparse_pitch6_x36y35", "sparse", 36, 35, 6, 1),
    ("cross_region_x36y25", "cross_region", 36, 25, 4, 1),
    ("far_x20y25", "far", 20, 25, 4, 1),
    ("random_seed1_x36y35", "random", 36, 35, 8, 1),
    ("random_seed2_x36y35", "random", 36, 35, 8, 2),
    ("random_seed3_x36y35", "random", 36, 35, 8, 3),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("data/experiments/xdc_matrix"))
    parser.add_argument("--ro-num", type=int, default=8)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    generator = root / "scripts" / "generate_ro_placement_xdc.py"
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_lines = ["name,pattern,x0,y0,pitch,seed,xdc"]
    for name, pattern, x0, y0, pitch, seed in MATRIX:
        xdc = out_dir / f"ro_{name}.xdc"
        cmd = [
            sys.executable,
            str(generator),
            "--pattern",
            pattern,
            "--x0",
            str(x0),
            "--y0",
            str(y0),
            "--ro-num",
            str(args.ro_num),
            "--pitch",
            str(pitch),
            "--seed",
            str(seed),
            "--out",
            str(xdc),
        ]
        subprocess.run(cmd, check=True)
        manifest_lines.append(f"{name},{pattern},{x0},{y0},{pitch},{seed},{xdc.as_posix()}")

    manifest = out_dir / "matrix_manifest.csv"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"Wrote {manifest}")


if __name__ == "__main__":
    main()
