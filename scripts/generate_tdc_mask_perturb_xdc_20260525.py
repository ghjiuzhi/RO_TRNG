#!/usr/bin/env python3
"""Generate full-matrix placement XDCs for TDC mask perturbation experiments."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "experiments" / "xdc_tdc_mask_perturb"

MATRIX_SOURCES = {
    "random1": ROOT / "data" / "experiments" / "xdc_matrix" / "ro_random_seed1_x36y35.xdc",
    "random3": ROOT / "data" / "experiments" / "xdc_matrix" / "ro_random_seed3_x36y35.xdc",
}

SAMPLE_SOURCES = {
    "baseline": None,
    "local_x45y39": ROOT / "data" / "experiments" / "xdc_sampler_island" / "random1_sample_ro_local_x45y39.xdc",
}


def convert_matrix_xdc(text: str) -> str:
    text = text.replace("u_entropy_source/RO_NUM_LOOP", "u_ro_matrix/RO_NUM_LOOP")
    text = text.replace("u_entropy_source.RO_STAGES", "tdc_ro_mask_matrix.RO_STAGES")
    text = text.replace("RO_TRNG_top instance name u_entropy_source", "RO_TDC_pair_mask_perturb_top instance name u_ro_matrix")
    return text


def extract_sample_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        if "RO_SAMPLE_" in line:
            lines.append(line.replace("u_entropy_source/RO_SAMPLE_", "u_ro_matrix/RO_SAMPLE_"))
    return lines


def baseline_sample_lines() -> list[str]:
    # Keep the baseline sample RO placed near the original random1 origin.
    return [
        "# Baseline sample RO placement for TDC perturbation control",
        "set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]",
        "set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]",
        "set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]",
        "set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]",
        "set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]",
        "set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]",
        "set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]",
        "set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]",
        "set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]",
        "set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]",
        "set_property LOC SLICE_X38Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]",
        "set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]",
    ]


def write_one(out_dir: Path, family: str, sample: str) -> Path:
    matrix_path = MATRIX_SOURCES[family]
    sample_path = SAMPLE_SOURCES[sample]
    matrix_text = matrix_path.read_text(encoding="utf-8")
    body = convert_matrix_xdc(matrix_text)

    if sample_path is None:
        sample_lines = baseline_sample_lines()
    else:
        sample_lines = extract_sample_lines(sample_path.read_text(encoding="utf-8"))
        if not sample_lines:
            raise RuntimeError(f"No sample RO lines found in {sample_path}")

    out_path = out_dir / f"tdc_mask_perturb_{family}_{sample}.xdc"
    header = [
        "################################################################",
        "# Auto-generated TDC mask perturbation placement constraints",
        f"# family={family}",
        f"# matrix_xdc={matrix_path.relative_to(ROOT)}",
        f"# sample_source={sample if sample_path is None else sample_path.relative_to(ROOT)}",
        "# expected top=RO_TDC_pair_mask_perturb_top; RO matrix instance u_ro_matrix",
        "################################################################",
        "",
    ]
    allow_loop_lines = [
        "",
        "# Acknowledge intentional RO combinational loops for bitstream generation.",
        "set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[*].RO_AND.u_LUT6_and2_1/in0[0]}]",
        "set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[*].RO_NAND.u_LUT6_nand2_1/in0[0]}]",
        "set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_AND.u_LUT6_and2_1/in0[0]}]",
        "set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/in0[0]}]",
    ]
    out_path.write_text(
        "\n".join(header)
        + body
        + "\n\n"
        + "\n".join(sample_lines)
        + "\n"
        + "\n".join(allow_loop_lines)
        + "\n",
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for family in ["random1", "random3"]:
        paths.append(write_one(args.out_dir, family, "baseline"))
    paths.append(write_one(args.out_dir, "random1", "local_x45y39"))

    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
