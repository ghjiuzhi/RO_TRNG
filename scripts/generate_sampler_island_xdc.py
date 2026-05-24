#!/usr/bin/env python3
"""Generate TRNG placement XDC variants that control the sampler island.

The input matrix XDC fixes the eight data ROs. This generator copies those
constraints and optionally adds constraints for the sample RO and the sampling
registers. It is intended for the random1 sampler-coupling ablation.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def cell_filter(pattern: str) -> str:
    return f"[get_cells -hierarchical -filter {{NAME =~ {pattern}}}]"


def sample_ro_constraints(x: int, y: int) -> list[str]:
    cells = ["RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6"]
    cells.extend(f"RO_SAMPLE_LOOP[{i}].u_LUT6_not1/u_LUT6" for i in range(8))
    bels = ["A6LUT", "B6LUT", "C6LUT", "D6LUT"]

    lines: list[str] = [
        "",
        f"# Sample RO constrained near data ROs, origin=SLICE_X{x}Y{y}",
    ]
    for index, cell in enumerate(cells):
        slice_x = x + index // 4
        bel = bels[index % 4]
        filt = cell_filter(f"*u_entropy_source/{cell}")
        lines.append(f"set_property LOC SLICE_X{slice_x}Y{y} {filt}")
        lines.append(f"set_property BEL {bel} {filt}")
    return lines


def sampler_reg_constraints(x: int, y: int) -> list[str]:
    lines: list[str] = [
        "",
        f"# Sampling registers constrained as an 8x8 local island, origin=SLICE_X{x}Y{y}",
    ]
    for line in range(8):
        for bit in range(8):
            reg_index = line * 8 + bit
            filt = cell_filter(
                f"*u_entropy_source/SAMPLE_DATA_LINE_LOOP[{line}]."
                f"SAMPLE_DATA_BIT_LOOP[{bit}].sampled_data_reg*"
            )
            lines.append(f"# sampled_data[{reg_index}] line={line} bit={bit}")
            lines.append(f"set_property LOC SLICE_X{x + bit}Y{y + line} {filt}")
    return lines


def build_xdc(
    matrix_xdc: Path,
    out: Path,
    sample_x: int,
    sample_y: int,
    include_sampler_regs: bool,
    regs_x: int,
    regs_y: int,
    label: str,
) -> None:
    source = matrix_xdc.read_text(encoding="utf-8").splitlines()
    lines = [
        "################################################################",
        "# Auto-generated sampler-island TRNG placement constraints",
        f"# label={label}",
        f"# matrix_xdc={matrix_xdc.as_posix()}",
        "# Data RO constraints are copied verbatim from the matrix XDC.",
        "################################################################",
        "",
    ]
    lines.extend(source)
    lines.extend(sample_ro_constraints(sample_x, sample_y))
    if include_sampler_regs:
        lines.extend(sampler_reg_constraints(regs_x, regs_y))
    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate sample-RO / sampler-island ablation XDCs."
    )
    parser.add_argument("--matrix-xdc", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--sample-x", type=int, default=45)
    parser.add_argument("--sample-y", type=int, default=39)
    parser.add_argument(
        "--keep-baseline-sample-ro",
        action="store_true",
        help="Do not add sample-RO LOC/BEL constraints; only copy matrix XDC and optional sampler regs.",
    )
    parser.add_argument("--include-sampler-regs", action="store_true")
    parser.add_argument("--regs-x", type=int, default=45)
    parser.add_argument("--regs-y", type=int, default=31)
    args = parser.parse_args()

    if not args.matrix_xdc.exists():
        raise FileNotFoundError(args.matrix_xdc)

    source = args.matrix_xdc.read_text(encoding="utf-8").splitlines()
    lines = [
        "################################################################",
        "# Auto-generated sampler-island TRNG placement constraints",
        f"# label={args.label}",
        f"# matrix_xdc={args.matrix_xdc.as_posix()}",
        "# Data RO constraints are copied verbatim from the matrix XDC.",
        "################################################################",
        "",
    ]
    lines.extend(source)
    if args.keep_baseline_sample_ro:
        lines.extend(
            [
                "",
                "# Sample RO intentionally left unconstrained/baseline for regs-only ablation.",
            ]
        )
    else:
        lines.extend(sample_ro_constraints(args.sample_x, args.sample_y))
    if args.include_sampler_regs:
        lines.extend(sampler_reg_constraints(args.regs_x, args.regs_y))
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
