#!/usr/bin/env python3
"""Generate TDC constraints for sampler-RO versus data-RO experiments.

The TDC top instantiates two generic RO modules as `u_ro_a` and `u_ro_b`.
This generator maps `u_ro_a` to a 9-stage sample RO island and maps `u_ro_b`
to one selected 2-stage data RO copied from a placement matrix XDC.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


XDC_RE = re.compile(
    r"^\s*set_property\s+"
    r"(?P<prop>LOC|BEL)\s+"
    r"(?P<value>\S+)\s+"
    r"\[get_cells\s+-hierarchical\s+-filter\s+\{NAME\s+=~\s+\*"
    r"u_entropy_source/RO_NUM_LOOP\[(?P<ro>\d+)\]\."
    r"(?P<stage>.+?)/u_LUT6\}\]\s*$"
)


@dataclass
class StagePlacement:
    loc: str | None = None
    bel: str | None = None


@dataclass
class RoPlacement:
    stages: dict[str, StagePlacement] = field(default_factory=dict)


def cell_filter(pattern: str) -> str:
    return f"[get_cells -hierarchical -filter {{NAME =~ {pattern}}}]"


def read_matrix_xdc(path: Path) -> dict[int, RoPlacement]:
    placements: dict[int, RoPlacement] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = XDC_RE.match(line)
        if not match:
            continue
        ro_index = int(match.group("ro"))
        placement = placements.setdefault(ro_index, RoPlacement())
        stage = placement.stages.setdefault(match.group("stage"), StagePlacement())
        if match.group("prop") == "LOC":
            stage.loc = match.group("value")
        else:
            stage.bel = match.group("value")
    return placements


def require_stage(ro_index: int, ro: RoPlacement, stage_name: str) -> StagePlacement:
    stage = ro.stages.get(stage_name)
    if stage is None or stage.loc is None:
        raise ValueError(f"RO{ro_index} is missing {stage_name} LOC")
    return stage


def emit_data_ro(instance: str, ro_index: int, ro: RoPlacement, copy_bel: bool) -> list[str]:
    mapping = {
        "RO_AND.u_LUT6_and2_1": "RO_AND.u_LUT6_and2_1",
        "RO_STAGE_LOOP[0].u_LUT6_not1": "RO_STAGE_LOOP[0].u_LUT6_not1",
    }
    lines = [f"# {instance} <= data RO{ro_index}, expected RO_STAGES=2"]
    for source_stage, target_stage in mapping.items():
        stage = require_stage(ro_index, ro, source_stage)
        filt = cell_filter(f"*{instance}/{target_stage}/u_LUT6")
        lines.append(f"set_property LOC {stage.loc} {filt}")
        if copy_bel and stage.bel:
            lines.append(f"set_property BEL {stage.bel} {filt}")
    return lines


def emit_sample_ro(instance: str, x: int, y: int) -> list[str]:
    cells = ["RO_NAND.u_LUT6_nand2_1/u_LUT6"]
    cells.extend(f"RO_STAGE_LOOP[{i}].u_LUT6_not1/u_LUT6" for i in range(8))
    bels = ["A6LUT", "B6LUT", "C6LUT", "D6LUT"]
    lines = [f"# {instance} <= sample RO island at SLICE_X{x}Y{y}, expected RO_STAGES=9"]
    for index, cell in enumerate(cells):
        slice_x = x + index // 4
        bel = bels[index % 4]
        filt = cell_filter(f"*{instance}/{cell}")
        lines.append(f"set_property LOC SLICE_X{slice_x}Y{y} {filt}")
        lines.append(f"set_property BEL {bel} {filt}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix-xdc", type=Path, required=True)
    parser.add_argument("--data-ro", type=int, required=True)
    parser.add_argument("--sample-x", type=int, required=True)
    parser.add_argument("--sample-y", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--family", default="")
    parser.add_argument("--no-copy-bel", action="store_true")
    args = parser.parse_args()

    placements = read_matrix_xdc(args.matrix_xdc)
    if args.data_ro not in placements:
        raise ValueError(f"RO{args.data_ro} was not found in {args.matrix_xdc}")

    copy_bel = not args.no_copy_bel
    lines = [
        "################################################################",
        "# Auto-generated sampler-data TDC placement constraints",
        f"# label={args.label}",
        f"# family={args.family}",
        f"# source_matrix_xdc={args.matrix_xdc.as_posix()}",
        f"# u_ro_a=sample_ro_x{args.sample_x}y{args.sample_y}; u_ro_b=data_ro{args.data_ro}",
        "# expected top=RO_TDC_pair_sysclk_top",
        "# required synth generics: {RO_A_STAGES=9 RO_B_STAGES=2}",
        "################################################################",
        "",
    ]
    lines.extend(emit_sample_ro("u_ro_a", args.sample_x, args.sample_y))
    lines.append("")
    lines.extend(emit_data_ro("u_ro_b", args.data_ro, placements[args.data_ro], copy_bel))
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
