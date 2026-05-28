#!/usr/bin/env python3
"""Summarize reduced-XOR data_ro3 warmup-neighbor counterfactuals."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEW_SUMMARY = ROOT / "data/experiments/restart_reduced_xor_w5_w11_data_ro3_except3_20260528/profile/restart_reduced_xor_strict_20260526_summary.csv"
W10_MAP = ROOT / "data/experiments/restart_reduced_xor_w10_direction_map_20260526/summary/w10_direction_map_combined.csv"
OUT_DIR = ROOT / "data/experiments/restart_reduced_xor_ro3_warmup_neighbors_20260528"


def infer_mode(label: str) -> str:
    if "_except_data_ro3_" in label:
        return "except_data_ro"
    if "_data_ro3_" in label:
        return "data_ro"
    raise ValueError(f"Cannot infer mode from {label}")


def load_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    with W10_MAP.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["data_ro"] == "3" and row["mode"] in {"data_ro", "except_data_ro"}:
                rows.append(
                    {
                        "mode": row["mode"],
                        "data_ro": "3",
                        "warmup": row["warmup"],
                        "p1": row["p1"],
                        "abs_bias": row["abs_bias"],
                        "min_entropy": row["min_entropy"],
                        "row_ones_std": row["row_ones_std"],
                        "worst_byte_bit": row["worst_byte_bit"],
                        "worst_x": row["worst_x"],
                        "worst_p1": row["worst_p1"],
                        "source": "w10_direction_map_20260526",
                    }
                )

    with NEW_SUMMARY.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            mode = infer_mode(row["label"])
            rows.append(
                {
                    "mode": mode,
                    "data_ro": "3",
                    "warmup": row["warmup_bytes"],
                    "p1": row["overall_p1"],
                    "abs_bias": row["overall_abs_bias"],
                    "min_entropy": row["overall_min_entropy"],
                    "row_ones_std": row["row_ones_std"],
                    "worst_byte_bit": f"{row['worst_byte_index']}.{row['worst_bit_index']}",
                    "worst_x": row["worst_x"],
                    "worst_p1": row["worst_p1"],
                    "source": "w5_w11_ro3_warmup_neighbors_20260528",
                }
            )

    return sorted(rows, key=lambda r: (int(r["warmup"]), r["mode"]))


def fmt_float(text: str, digits: int = 9) -> str:
    return f"{float(text):.{digits}f}".rstrip("0").rstrip(".")


def write_md(rows: list[dict[str, str]], path: Path) -> None:
    data_rows = [r for r in rows if r["mode"] == "data_ro"]
    except_rows = [r for r in rows if r["mode"] == "except_data_ro"]
    by_key = {(r["mode"], int(r["warmup"])): r for r in rows}

    lines: list[str] = []
    lines.append("# Reduced-XOR data_ro3 Warmup-Neighbor Summary")
    lines.append("")
    lines.append("## Mechanism Question")
    lines.append("")
    lines.append(
        "This experiment tests whether the strongest high-biased warmup-10 direction, "
        "`data_ro3`, is a warmup-10-only artifact or a stable same-data-RO direction "
        "whose complement/cancellation behavior changes with the restart warmup window."
    )
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| warmup | data_ro3 p1 | data_ro3 min-H | except_ro3 p1 | except_ro3 min-H | interpretation |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | --- |")
    for warmup in sorted({int(r["warmup"]) for r in rows}):
        d = by_key[("data_ro", warmup)]
        e = by_key[("except_data_ro", warmup)]
        if warmup == 10:
            interp = "high-biased direction peaks; complement remains moderately high-biased"
        else:
            interp = "high-biased direction persists; complement is near balanced"
        lines.append(
            "| {warmup} | {dp1} | {dh} | {ep1} | {eh} | {interp} |".format(
                warmup=warmup,
                dp1=fmt_float(d["p1"]),
                dh=fmt_float(d["min_entropy"]),
                ep1=fmt_float(e["p1"]),
                eh=fmt_float(e["min_entropy"]),
                interp=interp,
            )
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "`data_ro3` is high-biased at all three warmups, but the bias is strongest at "
        "warmup 10. Its complement is near balanced at warmup 5 and warmup 11, while "
        "warmup 10 leaves a moderate high bias. This supports a sampler-vector "
        "cancellation model rather than a single bad direction model: individual "
        "directions can be stable biased hardware functions, but the final all64 "
        "quality depends on how the remaining directions cancel or reinforce them "
        "under a specific startup/warmup condition."
    )
    lines.append("")
    lines.append("## Execution Note")
    lines.append("")
    lines.append(
        "The first hardware queue attempted `RecordXadc` before capture and produced "
        "zero-byte captures because the additional Vivado/XADC step missed the "
        "auto-stream UART window for this 60 s start-delay bitstream. A no-XADC "
        "sanity capture of the existing warmup-10 all64 bitstream succeeded, and the "
        "four target captures were then rerun without pre-capture XADC. XADC readings "
        "taken immediately before the failed queue were around 43.7-43.9 C with "
        "nominal rails, so they are contextual only, not per-capture measurements."
    )
    lines.append("")
    lines.append("## Source Files")
    lines.append("")
    lines.append("- `data/experiments/restart_reduced_xor_w10_direction_map_20260526/summary/w10_direction_map_combined.csv`")
    lines.append("- `data/experiments/restart_reduced_xor_w5_w11_data_ro3_except3_20260528/profile/restart_reduced_xor_strict_20260526_summary.csv`")
    lines.append("- `data/experiments/fast_mode/hardware_queue_restart_reduced_xor_w5_w11_data_ro3_except3_20260528.csv`")
    lines.append("")
    lines.append("## Detailed Rows")
    lines.append("")
    lines.append("| mode | warmup | p1 | abs bias | min-H | row ones std | worst byte.bit | worst x | worst p1 | source |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for row in rows:
        lines.append(
            "| {mode} | {warmup} | {p1} | {bias} | {h} | {std} | {wbb} | {wx} | {wp1} | {src} |".format(
                mode=row["mode"],
                warmup=row["warmup"],
                p1=fmt_float(row["p1"]),
                bias=fmt_float(row["abs_bias"]),
                h=fmt_float(row["min_entropy"]),
                std=fmt_float(row["row_ones_std"]),
                wbb=row["worst_byte_bit"],
                wx=row["worst_x"],
                wp1=fmt_float(row["worst_p1"]),
                src=row["source"],
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    csv_path = OUT_DIR / "reduced_xor_ro3_warmup_neighbors_20260528.csv"
    md_path = OUT_DIR / "reduced_xor_ro3_warmup_neighbors_20260528.md"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_md(rows, md_path)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
