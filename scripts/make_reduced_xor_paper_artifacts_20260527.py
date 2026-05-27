#!/usr/bin/env python3
"""Build paper-facing reduced-XOR counterfactual artifacts.

Offline only: this script reads existing reduced-XOR summary CSVs and writes
small CSV/Markdown/PNG/SVG artifacts for the paper. It does not touch hardware,
Vivado, UART, JTAG, or hw_server.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = (
    ROOT
    / "data/experiments/restart_reduced_xor_w10_direction_map_20260526/"
    / "summary/w10_direction_map_combined.csv"
)
DEFAULT_REPEAT = (
    ROOT
    / "data/experiments/restart_reduced_xor_w10_direction_repeat02_minimal_20260526/"
    / "summary/w10_direction_repeat_compare_wide.csv"
)
DEFAULT_OUT = ROOT / "data/experiments/reduced_xor_paper_artifacts_20260527"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(row.get(key, "")) for key in fields})


def f(row: dict[str, str], key: str, default: float = math.nan) -> float:
    value = row.get(key, "")
    if value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def fmt(value: object) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.9g}"
    return str(value)


def markdown_table(
    path: Path,
    title: str,
    rows: list[dict[str, object]],
    fields: list[str],
    note: str = "",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        if note:
            out.write(note.rstrip() + "\n\n")
        out.write("| " + " | ".join(fields) + " |\n")
        out.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
        for row in rows:
            out.write("| " + " | ".join(fmt(row.get(field, "")).replace("|", "\\|") for field in fields) + " |\n")


def mode_label(row: dict[str, str]) -> str:
    mode = row["mode"]
    idx = row["data_ro"]
    if mode == "all64":
        return "all64"
    if mode == "data_ro":
        return f"data_ro{idx}"
    if mode == "except_data_ro":
        return f"except_ro{idx}"
    return f"{mode}{idx}"


def build_direction_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        p1 = f(row, "p1")
        out.append(
            {
                "mode": row["mode"],
                "data_ro": row["data_ro"],
                "label": mode_label(row),
                "p1": p1,
                "bias_signed": p1 - 0.5,
                "abs_bias": f(row, "abs_bias"),
                "min_entropy": f(row, "min_entropy"),
                "worst_x": f(row, "worst_x"),
                "worst_p1": f(row, "worst_p1"),
            }
        )
    return out


def build_repeat_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "mode": row["mode"],
                "data_ro": row["data_ro"],
                "label": mode_label(row),
                "p1_run01": f(row, "p1_run01"),
                "p1_run02": f(row, "p1_run02"),
                "delta_p1": f(row, "delta_p1"),
                "abs_bias_run01": f(row, "abs_bias_run01"),
                "abs_bias_run02": f(row, "abs_bias_run02"),
                "minH_run01": f(row, "minH_run01"),
                "minH_run02": f(row, "minH_run02"),
            }
        )
    return out


def plot_direction_map(rows: list[dict[str, object]], out: Path) -> None:
    all64 = [r for r in rows if r["mode"] == "all64"]
    data = sorted([r for r in rows if r["mode"] == "data_ro"], key=lambda r: int(str(r["data_ro"])))
    excepts = sorted([r for r in rows if r["mode"] == "except_data_ro"], key=lambda r: int(str(r["data_ro"])))

    labels = [str(r["data_ro"]) for r in data]
    x = range(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(9.6, 4.8), dpi=180)
    ax.axhline(0, color="#555555", linewidth=1)
    ax.bar([i - width / 2 for i in x], [float(r["bias_signed"]) for r in data], width, label="data_ro[j]", color="#3B6EA8")
    ax.bar([i + width / 2 for i in x], [float(r["bias_signed"]) for r in excepts], width, label="all64 XOR data_ro[j]", color="#D07A2D")
    if all64:
        ax.axhline(float(all64[0]["bias_signed"]), color="#222222", linestyle="--", linewidth=1.2, label="all64")
    ax.set_xticks(list(x), labels)
    ax.set_xlabel("data_ro index j")
    ax.set_ylabel("signed bias p1 - 0.5")
    ax.set_title("Reduced-XOR direction map at sampler_island_local warmup10")
    ax.legend(frameon=False, ncol=3, fontsize=8)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(out / "reduced_xor_w10_direction_bias.png")
    fig.savefig(out / "reduced_xor_w10_direction_bias.svg")
    plt.close(fig)


def plot_repeat(rows: list[dict[str, object]], out: Path) -> None:
    labels = [str(r["label"]) for r in rows]
    x = range(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=180)
    ax.axhline(0.5, color="#555555", linewidth=1)
    ax.bar([i - width / 2 for i in x], [float(r["p1_run01"]) for r in rows], width, label="run01", color="#4C78A8")
    ax.bar([i + width / 2 for i in x], [float(r["p1_run02"]) for r in rows], width, label="run02", color="#F58518")
    ax.set_xticks(list(x), labels, rotation=28, ha="right")
    ax.set_ylabel("p1")
    ax.set_title("Reduced-XOR minimal repeat at warmup10")
    ax.set_ylim(0.12, 0.74)
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(out / "reduced_xor_w10_repeat_p1.png")
    fig.savefig(out / "reduced_xor_w10_repeat_p1.svg")
    plt.close(fig)


def write_summary(path: Path, direction: list[dict[str, object]], repeat: list[dict[str, object]]) -> None:
    data = [r for r in direction if r["mode"] == "data_ro"]
    excepts = [r for r in direction if r["mode"] == "except_data_ro"]
    all64 = next((r for r in direction if r["mode"] == "all64"), None)
    strongest_low = min(data, key=lambda r: float(r["p1"]))
    strongest_high = max(data, key=lambda r: float(r["p1"]))
    best_except = min(excepts, key=lambda r: float(r["abs_bias"]))
    stable = max(repeat, key=lambda r: abs(float(r["delta_p1"])))

    with path.open("w", encoding="utf-8") as out:
        out.write("# Reduced-XOR Paper Artifacts 2026-05-27\n\n")
        out.write("## Key Result\n\n")
        out.write(
            "The reduced-XOR hardware counterfactual shows that same-data-RO directions "
            "are real biased hardware output functions, while the final all64 output is "
            "an XOR-cancellation result over a structured sampler vector.\n\n"
        )
        if all64:
            out.write(f"- all64 at w10: p1={fmt(all64['p1'])}, abs_bias={fmt(all64['abs_bias'])}, min-H={fmt(all64['min_entropy'])}.\n")
        out.write(
            f"- strongest low-biased direction: {strongest_low['label']} p1={fmt(strongest_low['p1'])}, "
            f"abs_bias={fmt(strongest_low['abs_bias'])}.\n"
        )
        out.write(
            f"- strongest high-biased direction: {strongest_high['label']} p1={fmt(strongest_high['p1'])}, "
            f"abs_bias={fmt(strongest_high['abs_bias'])}.\n"
        )
        out.write(
            f"- best cancelling complement: {best_except['label']} p1={fmt(best_except['p1'])}, "
            f"abs_bias={fmt(best_except['abs_bias'])}.\n"
        )
        out.write(
            f"- largest repeat delta among diagnostic modes: {stable['label']} delta_p1={fmt(stable['delta_p1'])}.\n\n"
        )
        out.write("## Files\n\n")
        out.write("- `reduced_xor_w10_direction_paper.csv`\n")
        out.write("- `reduced_xor_w10_direction_paper.md`\n")
        out.write("- `reduced_xor_w10_direction_bias.png` / `.svg`\n")
        out.write("- `reduced_xor_w10_repeat_paper.csv`\n")
        out.write("- `reduced_xor_w10_repeat_paper.md`\n")
        out.write("- `reduced_xor_w10_repeat_p1.png` / `.svg`\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--direction-map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--repeat", type=Path, default=DEFAULT_REPEAT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    direction = build_direction_rows(read_csv(args.direction_map))
    repeat = build_repeat_rows(read_csv(args.repeat))

    direction_fields = ["mode", "data_ro", "label", "p1", "bias_signed", "abs_bias", "min_entropy", "worst_x", "worst_p1"]
    repeat_fields = ["mode", "data_ro", "label", "p1_run01", "p1_run02", "delta_p1", "abs_bias_run01", "abs_bias_run02", "minH_run01", "minH_run02"]

    write_csv(out / "reduced_xor_w10_direction_paper.csv", direction, direction_fields)
    write_csv(out / "reduced_xor_w10_repeat_paper.csv", repeat, repeat_fields)
    markdown_table(
        out / "reduced_xor_w10_direction_paper.md",
        "Reduced-XOR Warmup10 Direction Map",
        direction,
        direction_fields,
        "p1 is the one probability over the 1000 x 1000 bit-symbol restart matrix.",
    )
    markdown_table(
        out / "reduced_xor_w10_repeat_paper.md",
        "Reduced-XOR Warmup10 Minimal Repeat",
        repeat,
        repeat_fields,
        "Repeat02 covers the most diagnostic all64/data_ro/except_data_ro modes.",
    )
    plot_direction_map(direction, out)
    plot_repeat(repeat, out)
    write_summary(out / "reduced_xor_paper_summary.md", direction, repeat)
    print(f"Wrote reduced-XOR paper artifacts to {out}")


if __name__ == "__main__":
    main()
