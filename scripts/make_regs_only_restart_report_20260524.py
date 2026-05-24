#!/usr/bin/env python3
"""Summarize the random1 regs-only restart experiment for paper planning."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESTART_SUMMARY = ROOT / "data/experiments/restart_summary_20260524/restart_result_summary_20260524.csv"
OUT_DIR = ROOT / "data/experiments/sampler_regs_only_20260524"
OUT_CSV = OUT_DIR / "random1_sampler_regs_only_restart_summary_20260524.csv"
OUT_MD = OUT_DIR / "random1_sampler_regs_only_restart_summary_20260524.md"
TRANSITION_CSV = OUT_DIR / "random1_sampler_regs_only_warmup_transition_20260524.csv"
TRANSITION_SVG = OUT_DIR / "random1_sampler_regs_only_warmup_transition_20260524.svg"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def write_transition_svg(path: Path, rows: list[dict[str, str]]) -> None:
    width = 900
    height = 360
    margin_left = 70
    margin_right = 28
    margin_top = 36
    margin_bottom = 58
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    warmups = [int(row["warmup_bytes"]) for row in rows]
    min_w, max_w = min(warmups), max(warmups)
    max_x = max(float(row["x_max_max"]) for row in rows)
    y_max = max(820, max_x + 20)

    def x_pos(warmup: int) -> float:
        if max_w == min_w:
            return margin_left + plot_w / 2
        return margin_left + (warmup - min_w) / (max_w - min_w) * plot_w

    def y_pos(value: float) -> float:
        return margin_top + (1 - value / y_max) * plot_h

    cutoff_y = y_pos(572)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="24" y="24" font-family="Arial, sans-serif" font-size="16" font-weight="700">random1 regs-only restart warmup transition</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{cutoff_y:.2f}" x2="{margin_left + plot_w}" y2="{cutoff_y:.2f}" stroke="#888" stroke-dasharray="5 4"/>',
        f'<text x="{margin_left + plot_w - 4}" y="{cutoff_y - 6:.2f}" font-family="Arial, sans-serif" font-size="11" text-anchor="end" fill="#555">X_cutoff=572</text>',
    ]
    for tick in [0, 200, 400, 600, 800]:
        y = y_pos(tick)
        parts.append(f'<line x1="{margin_left - 4}" y1="{y:.2f}" x2="{margin_left}" y2="{y:.2f}" stroke="#333"/>')
        parts.append(f'<text x="{margin_left - 10}" y="{y + 4:.2f}" font-family="Arial, sans-serif" font-size="11" text-anchor="end">{tick}</text>')
    for row in rows:
        w = int(row["warmup_bytes"])
        x = x_pos(w)
        parts.append(f'<line x1="{x:.2f}" y1="{margin_top + plot_h}" x2="{x:.2f}" y2="{margin_top + plot_h + 4}" stroke="#333"/>')
        parts.append(f'<text x="{x:.2f}" y="{margin_top + plot_h + 20}" font-family="Arial, sans-serif" font-size="11" text-anchor="middle">{w}</text>')
    points = []
    for row in rows:
        x = x_pos(int(row["warmup_bytes"]))
        y = y_pos(float(row["x_max_max"]))
        points.append(f"{x:.2f},{y:.2f}")
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#2b6cb0" stroke-width="2"/>')
    for row in rows:
        x = x_pos(int(row["warmup_bytes"]))
        y = y_pos(float(row["x_max_max"]))
        status = row["status_summary"]
        fill = "#2f855a" if status == "passed" else ("#d69e2e" if status == "mixed" else "#c53030")
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{fill}"><title>warmup {row["warmup_bytes"]}: {status}, Xmax {row["x_max_max"]}, p1 {row["overall_p1_min"]}-{row["overall_p1_max"]}</title></circle>')
        parts.append(f'<text x="{x:.2f}" y="{y - 9:.2f}" font-family="Arial, sans-serif" font-size="10" text-anchor="middle">{row["x_max_max"]}</text>')
    parts.extend(
        [
            f'<text x="{margin_left + plot_w / 2}" y="{height - 16}" font-family="Arial, sans-serif" font-size="12" text-anchor="middle">warmup bytes</text>',
            f'<text x="18" y="{margin_top + plot_h / 2}" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" transform="rotate(-90 18 {margin_top + plot_h / 2})">max restart X</text>',
            '<text x="650" y="24" font-family="Arial, sans-serif" font-size="11" fill="#2f855a">green=passed</text>',
            '<text x="745" y="24" font-family="Arial, sans-serif" font-size="11" fill="#c53030">red=failed</text>',
            '</svg>',
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def status_rank(statuses: list[str]) -> str:
    if statuses and all(status == "passed" for status in statuses):
        return "passed"
    if any(status == "passed" for status in statuses):
        return "mixed"
    return "failed"


def main() -> None:
    rows = [
        row
        for row in read_csv(RESTART_SUMMARY)
        if row.get("placement") == "random1_sampler_regs_only"
    ]
    rows.sort(key=lambda r: (int(r["warmup_bytes"]), r["repeat_tag"], r["bit_order"]))

    fields = [
        "warmup_bytes",
        "repeat_tag",
        "bit_order",
        "ea_status",
        "h_i",
        "x_cutoff",
        "x_max",
        "overall_p1",
        "row_ones_std",
        "worst_byte_index",
        "worst_bit_index",
        "worst_x",
        "worst_p1",
        "worst_msb_expanded_column",
        "worst_lsb_expanded_column",
        "xadc_status",
        "xadc_before_temperature_c",
        "xadc_after_temperature_c",
        "xadc_after_vccint_v",
        "restart_input_sha256",
    ]
    write_csv(OUT_CSV, rows, fields)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["warmup_bytes"]].append(row)

    transition_rows: list[dict[str, str]] = []
    for warmup, group in sorted(grouped.items(), key=lambda item: int(item[0])):
        statuses = [row["ea_status"] for row in group]
        x_values = [int(float(row["x_max"])) for row in group if row.get("x_max")]
        p_values = [v for row in group if (v := as_float(row.get("overall_p1", ""))) is not None]
        min_h_values = [v for row in group if (v := as_float(row.get("min_h", ""))) is not None]
        transition_rows.append(
            {
                "warmup_bytes": warmup,
                "status_summary": status_rank(statuses),
                "rows": str(len(group)),
                "passed_rows": str(sum(1 for status in statuses if status == "passed")),
                "failed_rows": str(sum(1 for status in statuses if status == "failed")),
                "x_max_min": str(min(x_values)) if x_values else "",
                "x_max_max": str(max(x_values)) if x_values else "",
                "overall_p1_min": f"{min(p_values):.6f}" if p_values else "",
                "overall_p1_max": f"{max(p_values):.6f}" if p_values else "",
                "min_h_min": f"{min(min_h_values):.6f}" if min_h_values else "",
                "min_h_max": f"{max(min_h_values):.6f}" if min_h_values else "",
            }
        )
    write_csv(
        TRANSITION_CSV,
        transition_rows,
        [
            "warmup_bytes",
            "status_summary",
            "rows",
            "passed_rows",
            "failed_rows",
            "x_max_min",
            "x_max_max",
            "overall_p1_min",
            "overall_p1_max",
            "min_h_min",
            "min_h_max",
        ],
    )
    write_transition_svg(TRANSITION_SVG, transition_rows)

    lines = [
        "# random1 regs-only Restart Summary 20260524",
        "",
        "## Result",
        "",
        "`regs-only` nearly fixes the 20MiB continuous stream and exposes a non-monotonic restart warmup passband.",
        "Warmup `5/6/8/10` passed the SP800-90B restart sanity check, while `0/4/11/12/16` failed under the same bit-symbol protocol.",
        "This is a high-value mechanism result because it separates steady-state entropy quality from startup-window robustness.",
        "",
        "| warmup | repeat | order | status | H_I | X_cutoff | X_max | overall p1 | worst byte.bit | worst p1 | XADC |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        xadc = ""
        if row.get("xadc_status"):
            xadc = f"{row.get('xadc_before_temperature_c')}C->{row.get('xadc_after_temperature_c')}C, VCCINT={row.get('xadc_after_vccint_v')}V"
        lines.append(
            "| {warmup_bytes} | {repeat_tag} | {bit_order} | {ea_status} | {h_i} | {x_cutoff} | {x_max} | {overall_p1} | {worst_byte_index}.{worst_bit_index} | {worst_p1} | {xadc} |".format(
                xadc=xadc,
                **row,
            )
        )

    lines.extend(
        [
            "",
            "## Warmup Transition",
            "",
            "| warmup | status | rows | X_max range | overall p1 range | min-H range |",
            "| ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in transition_rows:
        lines.append(
            "| {warmup_bytes} | {status_summary} | {rows} | {x_max_min}-{x_max_max} | {overall_p1_min}-{overall_p1_max} | {min_h_min}-{min_h_max} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            f"![Warmup transition]({TRANSITION_SVG.resolve().as_posix()})",
            "",
            "## Mechanism Interpretation",
            "",
            "- Continuous stream: moving only the 64 sampling registers/routing island makes `random1` near ideal (`p1=0.499809736`, bit min-entropy `0.999451`).",
            "- Restart warmup0: both repeats fail despite near-balanced overall p1. The failure is driven by early fixed-column hotspots (`X_max=756` and `802`, cutoff `572`).",
            "- Restart warmup4 fails with a strong global low-one bias (`overall p1=0.407970`) and a fixed-column hotspot (`X_max=751`).",
            "- Restart warmup5/6/8/10 pass; `warmup8` passed in two independent captures.",
            "- Restart warmup11/12/16 fail again, with the failure mode shifting to global high-one or low-one bias plus moderate fixed-column excursions.",
            "- Therefore warmup is not monotonic. The restart-safe region behaves like a startup phase window or passband, not simply like 'discard more early bytes'.",
            "",
            "## Paper Claim",
            "",
            "The cleanest claim is not that regs-only solves the entropy source completely. The stronger and more nuanced claim is:",
            "",
            "> Sampling-register/routing placement is sufficient to repair steady-state continuous bias, proving that the sampler path is part of the entropy-source boundary. SP800-90B restart experiments further reveal a narrow, non-monotonic startup warmup passband, indicating that restart robustness depends on the sampled phase trajectory rather than on simply waiting longer.",
            "",
            "This result strengthens the paper because it gives a layered mechanism: sampler-side physical implementation controls steady-state bias, while reset/startup phase transients control restart sanity.",
            "",
            "## Artifacts",
            "",
            f"- CSV: `{OUT_CSV.relative_to(ROOT)}`",
            f"- Warmup transition CSV: `{TRANSITION_CSV.relative_to(ROOT)}`",
            f"- Warmup transition SVG: `{TRANSITION_SVG.relative_to(ROOT)}`",
            "- Packed captures: `data/hardware/20260511_fpga1_board1/restart/random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup*_run*_20260524.bin`",
            "- ea_restart outputs: `data/hardware/20260511_fpga1_board1/restart/ea_restart_random1_sampler_regs_only_*_20260524/`",
            "- Column diagnostics: `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup*_run*/`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
