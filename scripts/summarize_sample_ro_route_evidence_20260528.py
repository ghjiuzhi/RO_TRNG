#!/usr/bin/env python3
"""Summarize sample-RO routed evidence extracted from Vivado DCPs."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/experiments/sample_ro_route_diff_20260528"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path or not path.exists() or not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def label_paths(out_dir: Path) -> dict[str, dict[str, Path]]:
    labels: dict[str, dict[str, Path]] = defaultdict(dict)
    for path in out_dir.glob("*_cells.csv"):
        if path.name.endswith("_neighborhood_cells.csv"):
            continue
        labels[path.name[: -len("_cells.csv")]]["cells"] = path
    for path in out_dir.glob("*_nets.csv"):
        labels[path.name[: -len("_nets.csv")]]["nets"] = path
    for path in out_dir.glob("*_pips.csv"):
        labels[path.name[: -len("_pips.csv")]]["pips"] = path
    for path in out_dir.glob("*_net_delays.csv"):
        labels[path.name[: -len("_net_delays.csv")]]["net_delays"] = path
    for path in out_dir.glob("*_neighborhood_cells.csv"):
        labels[path.name[: -len("_neighborhood_cells.csv")]]["neighborhood"] = path
    return dict(labels)


def group_counts(rows: list[dict[str, str]], key: str) -> Counter[str]:
    return Counter(row.get(key, "") for row in rows)


def summarize_label(label: str, paths: dict[str, Path]) -> dict[str, object]:
    cells = read_csv(paths.get("cells", Path()))
    nets = read_csv(paths.get("nets", Path()))
    pips = read_csv(paths.get("pips", Path()))
    net_delays = read_csv(paths.get("net_delays", Path()))
    neighborhood = read_csv(paths.get("neighborhood", Path()))

    cell_groups = group_counts(cells, "group")
    net_groups = group_counts(nets, "group")
    pip_groups = group_counts(pips, "group")
    delay_groups = group_counts(net_delays, "group")
    sample_locs = sorted({row.get("loc", "") for row in cells if row.get("group") == "sample_ro"})
    sampled_reg_locs = sorted(
        {row.get("loc", "") for row in cells if row.get("group") == "sampled_data_regs"}
    )
    data_locs = sorted({row.get("loc", "") for row in cells if row.get("group") == "data_ro"})

    return {
        "label": label,
        "sample_ro_cells": cell_groups["sample_ro"],
        "sampled_data_regs": cell_groups["sampled_data_regs"],
        "data_ro_cells": cell_groups["data_ro"],
        "sample_ro_locs": " ".join(sample_locs),
        "sampled_reg_loc_count": len(sampled_reg_locs),
        "data_ro_loc_count": len(data_locs),
        "sample_ro_nets": net_groups["sample_ro_net"],
        "sampled_data_nets": net_groups["sampled_data_net"],
        "data_ro_nets": net_groups["data_ro_net"],
        "sample_ro_pips": pip_groups["sample_ro_net"],
        "sampled_data_pips": pip_groups["sampled_data_net"],
        "data_ro_pips": pip_groups["data_ro_net"],
        "sample_ro_delay_arcs": delay_groups["sample_ro_net"],
        "sampled_data_delay_arcs": delay_groups["sampled_data_net"],
        "data_ro_delay_arcs": delay_groups["data_ro_net"],
        "neighborhood_rows": len(neighborhood),
    }


def compare_cells(label_a: str, paths_a: dict[str, Path], label_b: str, paths_b: dict[str, Path]) -> list[dict[str, object]]:
    a = {row["name"]: row for row in read_csv(paths_a.get("cells", Path()))}
    b = {row["name"]: row for row in read_csv(paths_b.get("cells", Path()))}
    rows = []
    for name in sorted(set(a) & set(b)):
        ra = a[name]
        rb = b[name]
        rows.append(
            {
                "label_a": label_a,
                "label_b": label_b,
                "group": ra.get("group", rb.get("group", "")),
                "name": name,
                "loc_a": ra.get("loc", ""),
                "loc_b": rb.get("loc", ""),
                "bel_a": ra.get("bel", ""),
                "bel_b": rb.get("bel", ""),
                "loc_changed": str(ra.get("loc", "") != rb.get("loc", "")),
                "bel_changed": str(ra.get("bel", "") != rb.get("bel", "")),
            }
        )
    return rows


def compare_nets(label_a: str, paths_a: dict[str, Path], label_b: str, paths_b: dict[str, Path]) -> list[dict[str, object]]:
    a = {row["net"]: row for row in read_csv(paths_a.get("nets", Path()))}
    b = {row["net"]: row for row in read_csv(paths_b.get("nets", Path()))}
    rows = []
    for name in sorted(set(a) & set(b)):
        ra = a[name]
        rb = b[name]
        rows.append(
            {
                "label_a": label_a,
                "label_b": label_b,
                "group": ra.get("group", rb.get("group", "")),
                "net": name,
                "pips_a": ra.get("pips_count", ""),
                "pips_b": rb.get("pips_count", ""),
                "nodes_a": ra.get("nodes_count", ""),
                "nodes_b": rb.get("nodes_count", ""),
                "route_changed": str(ra.get("route", "") != rb.get("route", "")),
                "drivers_a": ra.get("driver_cells", ""),
                "drivers_b": rb.get("driver_cells", ""),
                "loads_a": ra.get("load_cells", ""),
                "loads_b": rb.get("load_cells", ""),
            }
        )
    return rows


def delay_stats(rows: list[dict[str, str]]) -> dict[str, tuple[int, float, float, float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        group = row.get("group", "")
        value = row.get("slow_max", "")
        try:
            grouped[group].append(float(value))
        except ValueError:
            continue
    out = {}
    for group, values in grouped.items():
        if not values:
            continue
        out[group] = (len(values), min(values), sum(values) / len(values), max(values))
    return out


def compare_delay_groups(label_a: str, paths_a: dict[str, Path], label_b: str, paths_b: dict[str, Path]) -> list[dict[str, object]]:
    a = delay_stats(read_csv(paths_a.get("net_delays", Path())))
    b = delay_stats(read_csv(paths_b.get("net_delays", Path())))
    rows = []
    for group in sorted(set(a) | set(b)):
        ca, mina, meana, maxa = a.get(group, (0, 0.0, 0.0, 0.0))
        cb, minb, meanb, maxb = b.get(group, (0, 0.0, 0.0, 0.0))
        rows.append(
            {
                "group": group,
                "arcs_a": ca,
                "slow_max_min_a": f"{mina:.3f}",
                "slow_max_mean_a": f"{meana:.3f}",
                "slow_max_max_a": f"{maxa:.3f}",
                "arcs_b": cb,
                "slow_max_min_b": f"{minb:.3f}",
                "slow_max_mean_b": f"{meanb:.3f}",
                "slow_max_max_b": f"{maxb:.3f}",
                "mean_delta_b_minus_a": f"{(meanb - meana):.3f}",
            }
        )
    return rows


def pair_summary(cell_rows: list[dict[str, object]], net_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups = sorted({str(row["group"]) for row in cell_rows} | {str(row["group"]) for row in net_rows})
    out = []
    for group in groups:
        c = [row for row in cell_rows if row["group"] == group]
        n = [row for row in net_rows if row["group"] == group]
        out.append(
            {
                "group": group,
                "common_cells": len(c),
                "loc_changed": sum(row["loc_changed"] == "True" for row in c),
                "bel_changed": sum(row["bel_changed"] == "True" for row in c),
                "common_nets": len(n),
                "route_changed": sum(row["route_changed"] == "True" for row in n),
            }
        )
    return out


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--pairs",
        nargs="*",
        default=[
            "compact_w5_baseline:forward_w5_formal_sample",
            "formal_w4_baseline:reverse_w4_compact_sample",
        ],
        help="Pairs to compare as label_a:label_b.",
    )
    args = parser.parse_args()

    paths_by_label = label_paths(args.out_dir)
    if not paths_by_label:
        raise SystemExit(f"No extracted CSV files found in {args.out_dir}")

    summary_fields = [
        "label",
        "sample_ro_cells",
        "sampled_data_regs",
        "data_ro_cells",
        "sample_ro_locs",
        "sampled_reg_loc_count",
        "data_ro_loc_count",
        "sample_ro_nets",
        "sampled_data_nets",
        "data_ro_nets",
        "sample_ro_pips",
        "sampled_data_pips",
        "data_ro_pips",
        "sample_ro_delay_arcs",
        "sampled_data_delay_arcs",
        "data_ro_delay_arcs",
        "neighborhood_rows",
    ]
    summaries = [summarize_label(label, paths_by_label[label]) for label in sorted(paths_by_label)]
    write_csv(args.out_dir / "sample_ro_route_evidence_summary_20260528.csv", summaries, summary_fields)

    md_lines = [
        "# Sample-RO Routed Evidence 20260528",
        "",
        "This artifact summarizes routed DCP evidence for the sampler-side counterfactuals.",
        "It supports bounded physical attribution: sample-RO and local sampler-side routing changed, while this does not isolate LUT delay from every control/FIFO/UART movement.",
        "",
        "## Per-Build Summary",
        "",
        markdown_table(summaries, summary_fields),
        "",
    ]

    for pair in args.pairs:
        label_a, label_b = pair.split(":", 1)
        if label_a not in paths_by_label or label_b not in paths_by_label:
            md_lines.extend(["", f"## Missing Pair `{pair}`", "", "One or both labels were not extracted."])
            continue
        cell_rows = compare_cells(label_a, paths_by_label[label_a], label_b, paths_by_label[label_b])
        net_rows = compare_nets(label_a, paths_by_label[label_a], label_b, paths_by_label[label_b])
        cell_path = args.out_dir / f"{label_a}_vs_{label_b}_cell_diff_20260528.csv"
        net_path = args.out_dir / f"{label_a}_vs_{label_b}_net_diff_20260528.csv"
        write_csv(
            cell_path,
            cell_rows,
            [
                "label_a",
                "label_b",
                "group",
                "name",
                "loc_a",
                "loc_b",
                "bel_a",
                "bel_b",
                "loc_changed",
                "bel_changed",
            ],
        )
        write_csv(
            net_path,
            net_rows,
            [
                "label_a",
                "label_b",
                "group",
                "net",
                "pips_a",
                "pips_b",
                "nodes_a",
                "nodes_b",
                "route_changed",
                "drivers_a",
                "drivers_b",
                "loads_a",
                "loads_b",
            ],
        )
        ps = pair_summary(cell_rows, net_rows)
        delay_rows = compare_delay_groups(label_a, paths_by_label[label_a], label_b, paths_by_label[label_b])
        md_lines.extend(
            [
                f"## Pair `{label_a}` vs `{label_b}`",
                "",
                markdown_table(ps, ["group", "common_cells", "loc_changed", "bel_changed", "common_nets", "route_changed"]),
                "",
                "### Net Delay Summary",
                "",
                markdown_table(
                    delay_rows,
                    [
                        "group",
                        "arcs_a",
                        "slow_max_min_a",
                        "slow_max_mean_a",
                        "slow_max_max_a",
                        "arcs_b",
                        "slow_max_min_b",
                        "slow_max_mean_b",
                        "slow_max_max_b",
                        "mean_delta_b_minus_a",
                    ],
                ),
                "",
                f"- cell diff CSV: `{cell_path.as_posix()}`",
                f"- net diff CSV: `{net_path.as_posix()}`",
                "",
            ]
        )

    md_path = args.out_dir / "sample_ro_route_evidence_summary_20260528.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote {args.out_dir / 'sample_ro_route_evidence_summary_20260528.csv'}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
