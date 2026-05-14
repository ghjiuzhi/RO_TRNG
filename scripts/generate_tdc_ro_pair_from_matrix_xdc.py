#!/usr/bin/env python3
"""Extract a selected entropy_source RO pair into TDC u_ro_a/u_ro_b XDC."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


SOURCE_STAGE_TO_TARGET = {
    "RO_AND.u_LUT6_and2_1": "RO_AND.u_LUT6_and2_1",
    "RO_NAND.u_LUT6_nand2_1": "RO_NAND.u_LUT6_nand2_1",
    "RO_STAGE_LOOP[0].u_LUT6_not1": "RO_STAGE_LOOP[0].u_LUT6_not1",
}

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


def parse_pair(text: str) -> tuple[int, int]:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("pair must be formatted as i,j")
    try:
        a, b = (int(parts[0]), int(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("pair indexes must be integers") from exc
    if a == b:
        raise argparse.ArgumentTypeError("pair indexes must be different")
    if a < 0 or b < 0:
        raise argparse.ArgumentTypeError("pair indexes must be non-negative")
    return a, b


def infer_family(path: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    name = path.stem.lower()
    if "seed1" in name or "random1" in name:
        return "random1"
    if "seed3" in name or "random3" in name:
        return "random3"
    return "unknown"


def read_matrix_xdc(path: Path) -> dict[int, RoPlacement]:
    placements: dict[int, RoPlacement] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = XDC_RE.match(line)
        if not match:
            continue
        ro_index = int(match.group("ro"))
        stage = match.group("stage")
        if stage not in SOURCE_STAGE_TO_TARGET:
            continue
        placement = placements.setdefault(ro_index, RoPlacement())
        stage_placement = placement.stages.setdefault(stage, StagePlacement())
        prop = match.group("prop")
        if prop == "LOC":
            stage_placement.loc = match.group("value")
        elif prop == "BEL":
            stage_placement.bel = match.group("value")
        else:
            raise ValueError(f"Unexpected property at line {line_no}: {prop}")
    return placements


def validate_ro(ro_index: int, ro: RoPlacement, require_bel: bool) -> None:
    required = ("RO_AND.u_LUT6_and2_1", "RO_STAGE_LOOP[0].u_LUT6_not1")
    missing: list[str] = []
    for stage in required:
        stage_placement = ro.stages.get(stage)
        if stage_placement is None or stage_placement.loc is None:
            missing.append(f"{stage} LOC")
        if require_bel and (stage_placement is None or stage_placement.bel is None):
            missing.append(f"{stage} BEL")
    if missing:
        raise ValueError(f"RO{ro_index} is missing required placement fields: {', '.join(missing)}")


def target_filter(instance: str, target_stage: str) -> str:
    return f"[get_cells -hierarchical -filter {{NAME =~ *{instance}/{target_stage}/u_LUT6}}]"


def emit_stage(instance: str, target_stage: str, placement: StagePlacement, copy_bel: bool) -> list[str]:
    lines = [f"set_property LOC {placement.loc} {target_filter(instance, target_stage)}"]
    if copy_bel and placement.bel is not None:
        lines.append(f"set_property BEL {placement.bel} {target_filter(instance, target_stage)}")
    return lines


def emit_ro(instance: str, source_index: int, ro: RoPlacement, copy_bel: bool) -> list[str]:
    first = ro.stages["RO_AND.u_LUT6_and2_1"]
    second = ro.stages["RO_STAGE_LOOP[0].u_LUT6_not1"]
    lines = [
        f"# {instance} <= source RO{source_index}",
        f"#   stage0: loc={first.loc}, bel={first.bel if first.bel else 'not copied'}",
        f"#   stage1: loc={second.loc}, bel={second.bel if second.bel else 'not copied'}",
    ]
    lines.extend(emit_stage(instance, "RO_AND.u_LUT6_and2_1", first, copy_bel))
    lines.extend(emit_stage(instance, "RO_STAGE_LOOP[0].u_LUT6_not1", second, copy_bel))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate pair-specific TDC u_ro_a/u_ro_b constraints from a matrix RO XDC."
    )
    parser.add_argument("--matrix-xdc", type=Path, required=True, help="Input random1/random3 matrix XDC")
    parser.add_argument("--pair", type=parse_pair, required=True, help="RO pair as i,j; i maps to u_ro_a")
    parser.add_argument("--out", type=Path, required=True, help="Output TDC pair placement XDC")
    parser.add_argument("--family", help="Optional family label for comments, e.g. random1")
    parser.add_argument("--pair-id", help="Optional pair/run label for comments")
    parser.add_argument("--no-copy-bel", action="store_true", help="Copy LOC only and omit BEL constraints")
    args = parser.parse_args()

    if not args.matrix_xdc.exists():
        raise FileNotFoundError(args.matrix_xdc)

    ro_a_index, ro_b_index = args.pair
    copy_bel = not args.no_copy_bel
    placements = read_matrix_xdc(args.matrix_xdc)
    for ro_index in (ro_a_index, ro_b_index):
        if ro_index not in placements:
            raise ValueError(f"RO{ro_index} was not found in {args.matrix_xdc}")
        validate_ro(ro_index, placements[ro_index], require_bel=copy_bel)

    family = infer_family(args.matrix_xdc, args.family)
    pair_id = args.pair_id or f"{family}_ro{ro_a_index}_ro{ro_b_index}"
    ro_a = placements[ro_a_index]
    ro_b = placements[ro_b_index]

    lines = [
        "################################################################",
        "# Auto-generated pair-specific TDC RO placement constraints",
        f"# source_matrix_xdc={args.matrix_xdc.as_posix()}",
        f"# family={family}",
        f"# pair_id={pair_id}",
        f"# pair=({ro_a_index},{ro_b_index}); u_ro_a=RO{ro_a_index}; u_ro_b=RO{ro_b_index}",
        "# ro_stages=2; expected top=RO_TDC_pair_sysclk_top",
        f"# copy_bel={'yes' if copy_bel else 'no'}",
        "################################################################",
        "",
    ]
    lines.extend(emit_ro("u_ro_a", ro_a_index, ro_a, copy_bel))
    lines.append("")
    lines.extend(emit_ro("u_ro_b", ro_b_index, ro_b, copy_bel))
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
