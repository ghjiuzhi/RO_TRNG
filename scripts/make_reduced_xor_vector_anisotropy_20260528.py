#!/usr/bin/env python3
"""Build a paper-facing reduced-XOR row/column anisotropy summary."""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
W10_DIRECTIONS = ROOT / "data/experiments/restart_reduced_xor_w10_direction_map_20260526/summary/w10_direction_map_combined.csv"
LINE_SUMMARY = ROOT / "data/experiments/restart_reduced_xor_w10_line_map_20260528/profile/restart_reduced_xor_strict_20260526_summary.csv"
LINE6_REPEAT = ROOT / "data/experiments/restart_reduced_xor_w10_line6_repeat02_20260528/profile/restart_reduced_xor_strict_20260526_summary.csv"
OUT_DIR = ROOT / "data/experiments/restart_reduced_xor_vector_anisotropy_20260528"


def infer_line(label: str) -> str:
    marker = "_line"
    tail = label.split(marker, 1)[1]
    return tail.split("_", 1)[0]


def fnum(text: str) -> float:
    return float(text)


def fmt(x: float, digits: int = 9) -> str:
    return f"{x:.{digits}f}".rstrip("0").rstrip(".")


def load_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with W10_DIRECTIONS.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["mode"] not in {"all64", "data_ro", "except_data_ro"}:
                continue
            rows.append(
                {
                    "group": row["mode"],
                    "index": row["data_ro"],
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

    with LINE_SUMMARY.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "group": "line",
                    "index": infer_line(row["label"]),
                    "warmup": row["warmup_bytes"],
                    "p1": row["overall_p1"],
                    "abs_bias": row["overall_abs_bias"],
                    "min_entropy": row["overall_min_entropy"],
                    "row_ones_std": row["row_ones_std"],
                    "worst_byte_bit": f"{row['worst_byte_index']}.{row['worst_bit_index']}",
                    "worst_x": row["worst_x"],
                    "worst_p1": row["worst_p1"],
                    "source": "w10_line_map_20260528",
                }
            )
    order = {"all64": 0, "data_ro": 1, "line": 2, "except_data_ro": 3}
    return sorted(rows, key=lambda r: (order[r["group"]], 99 if r["index"] == "all" else int(r["index"])))


def summarize_group(rows: list[dict[str, str]], group: str) -> dict[str, str]:
    subset = [r for r in rows if r["group"] == group]
    p1s = [fnum(r["p1"]) for r in subset]
    biases = [fnum(r["abs_bias"]) for r in subset]
    minhs = [fnum(r["min_entropy"]) for r in subset]
    worsts = [int(float(r["worst_x"])) for r in subset]
    worst_row = max(subset, key=lambda r: fnum(r["abs_bias"]))
    return {
        "group": group,
        "count": str(len(subset)),
        "p1_min": fmt(min(p1s)),
        "p1_max": fmt(max(p1s)),
        "mean_abs_bias": fmt(mean(biases)),
        "max_abs_bias": fmt(max(biases)),
        "min_min_entropy": fmt(min(minhs)),
        "max_worst_x": str(max(worsts)),
        "max_bias_member": f"{worst_row['group']}{worst_row['index']}",
        "max_bias_member_p1": fmt(fnum(worst_row["p1"])),
    }


def load_line6_repeat() -> dict[str, str]:
    with LINE6_REPEAT.open(newline="", encoding="utf-8-sig") as f:
        return next(csv.DictReader(f))


def write_md(rows: list[dict[str, str]], group_rows: list[dict[str, str]], path: Path) -> None:
    line6_r1 = next(r for r in rows if r["group"] == "line" and r["index"] == "6")
    line6_r2 = load_line6_repeat()
    lines: list[str] = []
    lines.append("# Reduced-XOR Warmup10 Vector Anisotropy")
    lines.append("")
    lines.append("## Mechanism Question")
    lines.append("")
    lines.append(
        "This experiment asks whether the sampled 8 x 8 vector is biased primarily "
        "along same-data-RO directions, along sampler-phase line directions, or both. "
        "It uses the same warmup-10 reduced-XOR top as the full direction map."
    )
    lines.append("")
    lines.append("## Group Summary")
    lines.append("")
    lines.append("| group | rows | p1 range | mean abs bias | max abs bias | min min-H | max worst x | max-bias member |")
    lines.append("| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |")
    for row in group_rows:
        lines.append(
            "| {group} | {count} | {pmin}-{pmax} | {meanb} | {maxb} | {minh} | {wx} | {member} ({p1}) |".format(
                group=row["group"],
                count=row["count"],
                pmin=row["p1_min"],
                pmax=row["p1_max"],
                meanb=row["mean_abs_bias"],
                maxb=row["max_abs_bias"],
                minh=row["min_min_entropy"],
                wx=row["max_worst_x"],
                member=row["max_bias_member"],
                p1=row["max_bias_member_p1"],
            )
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The warmup-10 row/column control is strongly anisotropic. Same-data-RO "
        "directions span p1=0.191877 to 0.671833, with maximum absolute bias "
        "0.308123. Sampler-phase line directions stay close to balance, spanning "
        "p1=0.486473 to 0.501004, with maximum absolute bias 0.013527. Therefore "
        "the dominant marginal reduced-XOR structure in this warmup-10 run is not "
        "a generic per-sampler-phase line failure. It is concentrated in "
        "same-data-RO directions and then reshaped by XOR complements."
    )
    lines.append("")
    lines.append(
        "Line6 has the largest line-direction deviation and a large worst fixed-position "
        "count, so it was repeated as a targeted mechanism check. The repeat stayed "
        "close in overall p1 and hit the same worst byte.bit position. Thus line6 "
        "looks like a stable fixed-position startup outlier with weak global bias, "
        "not a row-direction analogue of the strong data-RO direction bias."
    )
    lines.append("")
    lines.append("## Line6 Repeat Check")
    lines.append("")
    lines.append("| run | p1 | abs bias | min-H | worst byte.bit | worst x | worst p1 |")
    lines.append("| --- | ---: | ---: | ---: | --- | ---: | ---: |")
    lines.append(
        "| run01 | {p1} | {bias} | {h} | {wbb} | {wx} | {wp1} |".format(
            p1=fmt(fnum(line6_r1["p1"])),
            bias=fmt(fnum(line6_r1["abs_bias"])),
            h=fmt(fnum(line6_r1["min_entropy"])),
            wbb=line6_r1["worst_byte_bit"],
            wx=line6_r1["worst_x"],
            wp1=fmt(fnum(line6_r1["worst_p1"])),
        )
    )
    lines.append(
        "| repeat02 | {p1} | {bias} | {h} | {wbb} | {wx} | {wp1} |".format(
            p1=fmt(fnum(line6_r2["overall_p1"])),
            bias=fmt(fnum(line6_r2["overall_abs_bias"])),
            h=fmt(fnum(line6_r2["overall_min_entropy"])),
            wbb=f"{line6_r2['worst_byte_index']}.{line6_r2['worst_bit_index']}",
            wx=line6_r2["worst_x"],
            wp1=fmt(fnum(line6_r2["worst_p1"])),
        )
    )
    lines.append("")
    lines.append("## Detailed Rows")
    lines.append("")
    lines.append("| group | index | p1 | abs bias | min-H | row ones std | worst byte.bit | worst x | worst p1 | source |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |")
    for row in rows:
        lines.append(
            "| {group} | {index} | {p1} | {bias} | {h} | {std} | {wbb} | {wx} | {wp1} | {src} |".format(
                group=row["group"],
                index=row["index"],
                p1=fmt(fnum(row["p1"])),
                bias=fmt(fnum(row["abs_bias"])),
                h=fmt(fnum(row["min_entropy"])),
                std=fmt(fnum(row["row_ones_std"])),
                wbb=row["worst_byte_bit"],
                wx=row["worst_x"],
                wp1=fmt(fnum(row["worst_p1"])),
                src=row["source"],
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    group_rows = [summarize_group(rows, group) for group in ["data_ro", "line", "except_data_ro"]]

    detail_csv = OUT_DIR / "reduced_xor_vector_anisotropy_detail_20260528.csv"
    group_csv = OUT_DIR / "reduced_xor_vector_anisotropy_group_20260528.csv"
    md_path = OUT_DIR / "reduced_xor_vector_anisotropy_20260528.md"

    with detail_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with group_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(group_rows[0].keys()))
        writer.writeheader()
        writer.writerows(group_rows)
    write_md(rows, group_rows, md_path)
    print(f"Wrote {detail_csv}")
    print(f"Wrote {group_csv}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
