#!/usr/bin/env python3
"""Analyze sampler snapshot bit correlation and XOR ablation structure."""

from __future__ import annotations

import argparse
import csv
import itertools
import math
from pathlib import Path


BIT_FIELDS = [f"b{i:02d}" for i in range(64)]
STAGE_FIELDS = [f"sx{i}" for i in range(8)]


def read_frames(path: Path) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            row: dict[str, int] = {
                "rand_bit": int(raw["rand_bit"]),
            }
            for field in BIT_FIELDS + STAGE_FIELDS:
                row[field] = int(raw[field])
            rows.append(row)
    if not rows:
        raise ValueError(f"empty frames CSV: {path}")
    return rows


def entropy_binary(p1: float) -> float:
    if p1 <= 0.0 or p1 >= 1.0:
        return 0.0
    return -(p1 * math.log2(p1) + (1.0 - p1) * math.log2(1.0 - p1))


def binary_mi(x: list[int], y: list[int]) -> float:
    n = len(x)
    if n == 0 or n != len(y):
        return math.nan
    counts = [[0, 0], [0, 0]]
    cx = [0, 0]
    cy = [0, 0]
    for a, b in zip(x, y):
        counts[a][b] += 1
        cx[a] += 1
        cy[b] += 1
    mi = 0.0
    for a in (0, 1):
        for b in (0, 1):
            c = counts[a][b]
            if c == 0:
                continue
            pxy = c / n
            px = cx[a] / n
            py = cy[b] / n
            mi += pxy * math.log2(pxy / (px * py))
    return mi


def pearson_binary(x: list[int], y: list[int]) -> float:
    n = len(x)
    if n == 0 or n != len(y):
        return math.nan
    mx = sum(x) / n
    my = sum(y) / n
    vx = sum((v - mx) ** 2 for v in x)
    vy = sum((v - my) ** 2 for v in y)
    if vx == 0.0 or vy == 0.0:
        return 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(vx * vy)


def p1(values: list[int]) -> float:
    return sum(values) / len(values) if values else math.nan


def xor_of_fields(rows: list[dict[str, int]], fields: list[str]) -> list[int]:
    out = []
    for row in rows:
        value = 0
        for field in fields:
            value ^= row[field]
        out.append(value)
    return out


def bit_label(bit: int) -> str:
    return f"b{bit:02d}_line{bit // 8}_ro{bit % 8}"


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def summarize_run(label: str, rows: list[dict[str, int]]) -> dict[str, object]:
    rand = [row["rand_bit"] for row in rows]
    bit_p1s = []
    for i, field in enumerate(BIT_FIELDS):
        vals = [row[field] for row in rows]
        bit_p1s.append(p1(vals))
    stage_vals = [[row[field] for row in rows] for field in STAGE_FIELDS]
    stage_p1s = [p1(vals) for vals in stage_vals]
    return {
        "label": label,
        "frames": len(rows),
        "rand_p1": f"{p1(rand):.9f}",
        "rand_entropy": f"{entropy_binary(p1(rand)):.9f}",
        "sampled_bit_mean_p1": f"{sum(bit_p1s) / len(bit_p1s):.9f}",
        "sampled_bit_mean_abs_bias": f"{sum(abs(v - 0.5) for v in bit_p1s) / len(bit_p1s):.9f}",
        "sampled_bits_p1_gt_0p55": sum(1 for v in bit_p1s if v > 0.55),
        "sampled_bits_p1_lt_0p45": sum(1 for v in bit_p1s if v < 0.45),
        "stage_xor_mean_p1": f"{sum(stage_p1s) / len(stage_p1s):.9f}",
        "stage_xor_gt_0p5": sum(1 for v in stage_p1s if v > 0.5),
        "stage_xor_lt_0p5": sum(1 for v in stage_p1s if v < 0.5),
    }


def analyze_one(label: str, rows: list[dict[str, int]], out_dir: Path) -> dict[str, Path]:
    bit_vectors = {field: [row[field] for row in rows] for field in BIT_FIELDS}
    rand = [row["rand_bit"] for row in rows]

    pair_rows: list[dict[str, object]] = []
    aggregate: dict[str, dict[str, list[float]]] = {
        "all": {"abs_r": [], "mi": []},
        "same_line": {"abs_r": [], "mi": []},
        "same_data_ro": {"abs_r": [], "mi": []},
        "diff_line_diff_ro": {"abs_r": [], "mi": []},
    }
    for i, j in itertools.combinations(range(64), 2):
        xi = bit_vectors[f"b{i:02d}"]
        yj = bit_vectors[f"b{j:02d}"]
        r = pearson_binary(xi, yj)
        mi = binary_mi(xi, yj)
        keys = ["all"]
        if i // 8 == j // 8:
            keys.append("same_line")
        if i % 8 == j % 8:
            keys.append("same_data_ro")
        if i // 8 != j // 8 and i % 8 != j % 8:
            keys.append("diff_line_diff_ro")
        for key in keys:
            aggregate[key]["abs_r"].append(abs(r))
            aggregate[key]["mi"].append(mi)
        pair_rows.append(
            {
                "label": label,
                "bit_i": i,
                "bit_j": j,
                "line_i": i // 8,
                "line_j": j // 8,
                "data_ro_i": i % 8,
                "data_ro_j": j % 8,
                "pearson_r": f"{r:.9f}",
                "abs_pearson_r": f"{abs(r):.9f}",
                "mi_bits": f"{mi:.9f}",
            }
        )
    pair_rows.sort(key=lambda r: (float(r["mi_bits"]), float(r["abs_pearson_r"])), reverse=True)

    def quantile(values: list[float], p: float) -> float:
        if not values:
            return math.nan
        values = sorted(values)
        idx = (len(values) - 1) * p
        lo = math.floor(idx)
        hi = math.ceil(idx)
        if lo == hi:
            return values[lo]
        return values[lo] * (hi - idx) + values[hi] * (idx - lo)

    aggregate_rows = []
    for category, vals in aggregate.items():
        abs_r = vals["abs_r"]
        mi_vals = vals["mi"]
        aggregate_rows.append(
            {
                "label": label,
                "category": category,
                "pair_count": len(abs_r),
                "mean_abs_r": f"{sum(abs_r) / len(abs_r):.9f}",
                "median_abs_r": f"{quantile(abs_r, 0.50):.9f}",
                "p95_abs_r": f"{quantile(abs_r, 0.95):.9f}",
                "p99_abs_r": f"{quantile(abs_r, 0.99):.9f}",
                "mean_mi_bits": f"{sum(mi_vals) / len(mi_vals):.9f}",
                "median_mi_bits": f"{quantile(mi_vals, 0.50):.9f}",
                "p95_mi_bits": f"{quantile(mi_vals, 0.95):.9f}",
                "p99_mi_bits": f"{quantile(mi_vals, 0.99):.9f}",
            }
        )

    rand_corr_rows = []
    for i in range(64):
        vals = bit_vectors[f"b{i:02d}"]
        r = pearson_binary(vals, rand)
        mi = binary_mi(vals, rand)
        rand_corr_rows.append(
            {
                "label": label,
                "bit": i,
                "bit_label": bit_label(i),
                "line": i // 8,
                "data_ro": i % 8,
                "p1": f"{p1(vals):.9f}",
                "pearson_to_rand": f"{r:.9f}",
                "abs_pearson_to_rand": f"{abs(r):.9f}",
                "mi_to_rand_bits": f"{mi:.9f}",
            }
        )
    rand_corr_rows.sort(key=lambda r: (float(r["mi_to_rand_bits"]), float(r["abs_pearson_to_rand"])), reverse=True)

    fields_all = BIT_FIELDS
    xor_rows = []

    def add_group(group_type: str, group: str, fields: list[str]) -> None:
        group_xor = xor_of_fields(rows, fields)
        complement = [a ^ b for a, b in zip(rand, group_xor)]
        xor_rows.append(
            {
                "label": label,
                "group_type": group_type,
                "group": group,
                "num_bits": len(fields),
                "group_xor_p1": f"{p1(group_xor):.9f}",
                "group_xor_entropy": f"{entropy_binary(p1(group_xor)):.9f}",
                "complement_xor_p1": f"{p1(complement):.9f}",
                "complement_xor_entropy": f"{entropy_binary(p1(complement)):.9f}",
                "corr_group_to_rand": f"{pearson_binary(group_xor, rand):.9f}",
                "mi_group_to_rand_bits": f"{binary_mi(group_xor, rand):.9f}",
            }
        )

    add_group("all_bits", "all_64", fields_all)
    for line in range(8):
        add_group("line", f"line{line}", [f"b{line * 8 + ro:02d}" for ro in range(8)])
    for ro in range(8):
        add_group("data_ro", f"ro{ro}", [f"b{line * 8 + ro:02d}" for line in range(8)])
    for stage in range(8):
        add_group("stage_xor", f"sx{stage}", [f"sx{stage}"])
    xor_rows.sort(key=lambda r: (r["group_type"], r["group"]))

    paths = {
        "summary": out_dir / f"{label}.correlation_xor_summary.csv",
        "pairs": out_dir / f"{label}.pairwise_top.csv",
        "rand": out_dir / f"{label}.bit_to_rand_top.csv",
        "xor": out_dir / f"{label}.xor_ablation.csv",
        "aggregate": out_dir / f"{label}.pairwise_aggregate.csv",
    }
    write_csv(paths["summary"], [summarize_run(label, rows)], list(summarize_run(label, rows).keys()))
    write_csv(
        paths["pairs"],
        pair_rows[:200],
        ["label", "bit_i", "bit_j", "line_i", "line_j", "data_ro_i", "data_ro_j", "pearson_r", "abs_pearson_r", "mi_bits"],
    )
    write_csv(
        paths["rand"],
        rand_corr_rows,
        ["label", "bit", "bit_label", "line", "data_ro", "p1", "pearson_to_rand", "abs_pearson_to_rand", "mi_to_rand_bits"],
    )
    write_csv(
        paths["xor"],
        xor_rows,
        [
            "label",
            "group_type",
            "group",
            "num_bits",
            "group_xor_p1",
            "group_xor_entropy",
            "complement_xor_p1",
            "complement_xor_entropy",
            "corr_group_to_rand",
            "mi_group_to_rand_bits",
        ],
    )
    write_csv(
        paths["aggregate"],
        aggregate_rows,
        [
            "label",
            "category",
            "pair_count",
            "mean_abs_r",
            "median_abs_r",
            "p95_abs_r",
            "p99_abs_r",
            "mean_mi_bits",
            "median_mi_bits",
            "p95_mi_bits",
            "p99_mi_bits",
        ],
    )
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="append", required=True, help="label=frames.csv")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    run_rows: dict[str, list[dict[str, int]]] = {}
    for spec in args.run:
        if "=" not in spec:
            raise ValueError("--run must be label=path")
        label, path_text = spec.split("=", 1)
        run_rows[label] = read_frames(Path(path_text))

    all_summaries = []
    generated = []
    for label, rows in run_rows.items():
        paths = analyze_one(label, rows, out_dir)
        generated.extend(paths.values())
        all_summaries.append(summarize_run(label, rows))

    write_csv(
        out_dir / "sampler_snapshot_w5_w10_w11_correlation_xor_summary_20260526.csv",
        all_summaries,
        list(all_summaries[0].keys()),
    )
    labels = list(run_rows)
    aggregate_rows_all = []
    for label in labels:
        aggregate_path = out_dir / f"{label}.pairwise_aggregate.csv"
        with aggregate_path.open("r", newline="", encoding="utf-8") as f:
            aggregate_rows_all.extend(list(csv.DictReader(f)))
    write_csv(
        out_dir / "sampler_snapshot_w5_w10_w11_pairwise_aggregate_20260526.csv",
        aggregate_rows_all,
        [
            "label",
            "category",
            "pair_count",
            "mean_abs_r",
            "median_abs_r",
            "p95_abs_r",
            "p99_abs_r",
            "mean_mi_bits",
            "median_mi_bits",
            "p95_mi_bits",
            "p99_mi_bits",
        ],
    )

    if len(labels) >= 2:
        # Compare pairwise MI/correlation deltas against the first label as baseline.
        pair_tables = {}
        for label in labels:
            path = out_dir / f"{label}.pairwise_top.csv"
            with path.open("r", newline="", encoding="utf-8") as f:
                pair_tables[label] = {
                    (int(r["bit_i"]), int(r["bit_j"])): r for r in csv.DictReader(f)
                }
        # Recompute all pairs for robust deltas, not only top-200 overlap.
        full_metrics: dict[str, dict[tuple[int, int], tuple[float, float]]] = {}
        for label, rows in run_rows.items():
            bit_vectors = {field: [row[field] for row in rows] for field in BIT_FIELDS}
            full_metrics[label] = {}
            for i, j in itertools.combinations(range(64), 2):
                xi = bit_vectors[f"b{i:02d}"]
                yj = bit_vectors[f"b{j:02d}"]
                full_metrics[label][(i, j)] = (pearson_binary(xi, yj), binary_mi(xi, yj))
        base = labels[0]
        delta_rows = []
        for label in labels[1:]:
            for (i, j), (r, mi) in full_metrics[label].items():
                br, bmi = full_metrics[base][(i, j)]
                delta_rows.append(
                    {
                        "compare": f"{label}_minus_{base}",
                        "bit_i": i,
                        "bit_j": j,
                        "line_i": i // 8,
                        "line_j": j // 8,
                        "data_ro_i": i % 8,
                        "data_ro_j": j % 8,
                        "delta_abs_pearson": f"{abs(r) - abs(br):.9f}",
                        "delta_mi_bits": f"{mi - bmi:.9f}",
                        "label_abs_pearson": f"{abs(r):.9f}",
                        "base_abs_pearson": f"{abs(br):.9f}",
                        "label_mi_bits": f"{mi:.9f}",
                        "base_mi_bits": f"{bmi:.9f}",
                    }
                )
        delta_rows.sort(key=lambda r: abs(float(r["delta_mi_bits"])), reverse=True)
        write_csv(
            out_dir / "sampler_snapshot_pairwise_delta_top_20260526.csv",
            delta_rows[:300],
            [
                "compare",
                "bit_i",
                "bit_j",
                "line_i",
                "line_j",
                "data_ro_i",
                "data_ro_j",
                "delta_abs_pearson",
                "delta_mi_bits",
                "label_abs_pearson",
                "base_abs_pearson",
                "label_mi_bits",
                "base_mi_bits",
            ],
        )

    md_lines = [
        "# Sampler Snapshot Correlation/XOR Analysis 2026-05-26",
        "",
        "## Summary",
        "",
        "| label | frames | rand p1 | sampled mean p1 | sampled mean abs bias | bits p1 > 0.55 | stage mean p1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in all_summaries:
        md_lines.append(
            f"| {row['label']} | {row['frames']} | {row['rand_p1']} | {row['sampled_bit_mean_p1']} | "
            f"{row['sampled_bit_mean_abs_bias']} | {row['sampled_bits_p1_gt_0p55']} | {row['stage_xor_mean_p1']} |"
        )
    md_lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- per-run summary: `sampler_snapshot_w5_w10_w11_correlation_xor_summary_20260526.csv`",
            "- per-run top pairwise MI/correlation: `<label>.pairwise_top.csv`",
            "- per-run bit-to-rand MI/correlation: `<label>.bit_to_rand_top.csv`",
            "- per-run line/data_ro/stage XOR ablation: `<label>.xor_ablation.csv`",
            "- per-run pairwise aggregate categories: `<label>.pairwise_aggregate.csv`",
            "- combined pairwise aggregate categories: `sampler_snapshot_w5_w10_w11_pairwise_aggregate_20260526.csv`",
            "- cross-run pairwise deltas: `sampler_snapshot_pairwise_delta_top_20260526.csv`",
        ]
    )
    md_path = out_dir / "sampler_snapshot_w5_w10_w11_correlation_xor_analysis_20260526.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {md_path}")
    for path in generated:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
