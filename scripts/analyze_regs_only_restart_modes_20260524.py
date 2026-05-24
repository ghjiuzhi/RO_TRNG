#!/usr/bin/env python3
"""Classify restart failure modes for the random1 regs-only warmup sweep."""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESTART_SUMMARY = ROOT / "data/experiments/restart_summary_20260524/restart_result_summary_20260524.csv"
ARTIFACT_ROOT = ROOT / "data/experiments/paper_artifacts_20260524"
OUT_DIR = ROOT / "data/experiments/sampler_regs_only_20260524"
OUT_CSV = OUT_DIR / "random1_sampler_regs_only_restart_mode_summary_20260524.csv"
OUT_MD = OUT_DIR / "random1_sampler_regs_only_restart_mode_summary_20260524.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: str) -> int | None:
    number = as_float(value)
    return None if number is None else int(number)


def column_dir(warmup: str, repeat: str) -> Path:
    return ARTIFACT_ROOT / f"restart_column_bias_random1_sampler_regs_only_formal_bits_warmup{warmup}_{repeat}"


def top_positions(warmup: str, repeat: str, limit: int = 8) -> list[dict[str, str]]:
    path = column_dir(warmup, repeat) / "top_biased_positions.csv"
    if not path.exists():
        return []
    return read_csv(path)[:limit]


def classify(row: dict[str, object]) -> str:
    status = str(row["status_summary"])
    if status == "passed":
        return "passband"
    p1_mean = float(row["overall_p1_mean"])
    x_max = int(row["x_max_max"])
    if abs(p1_mean - 0.5) >= 0.04:
        return "global_bias"
    if x_max >= 700:
        return "fixed_column_hotspot"
    return "moderate_column_or_mixed_bias"


def main() -> None:
    rows = [
        row
        for row in read_csv(RESTART_SUMMARY)
        if row.get("placement") == "random1_sampler_regs_only"
    ]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["warmup_bytes"]].append(row)

    out_rows: list[dict[str, object]] = []
    for warmup, group in sorted(grouped.items(), key=lambda item: int(item[0])):
        statuses = [row["ea_status"] for row in group]
        repeats = sorted({row["repeat_tag"] for row in group})
        x_values = [as_int(row.get("x_max", "")) for row in group]
        x_values = [value for value in x_values if value is not None]
        p1_values = [as_float(row.get("overall_p1", "")) for row in group]
        p1_values = [value for value in p1_values if value is not None]
        min_h_values = [as_float(row.get("min_h", "")) for row in group]
        min_h_values = [value for value in min_h_values if value is not None]
        worst_positions = []
        top_key_counter: Counter[str] = Counter()
        top_detail: list[str] = []
        for repeat in repeats:
            top = top_positions(warmup, repeat, limit=8)
            if top:
                first = top[0]
                worst_positions.append(f"{repeat}:{first['byte_index']}.{first['bit_index']} x={first['x']} p1={first['p1']}")
                for pos in top[:4]:
                    key = f"{pos['byte_index']}.{pos['bit_index']}"
                    top_key_counter[key] += 1
                    top_detail.append(f"{repeat}:{key}:{pos['x']}:{pos['p1']}")
        status_summary = (
            "passed"
            if statuses and all(status == "passed" for status in statuses)
            else ("mixed" if any(status == "passed" for status in statuses) else "failed")
        )
        p1_mean = statistics.mean(p1_values) if p1_values else float("nan")
        row: dict[str, object] = {
            "warmup_bytes": warmup,
            "status_summary": status_summary,
            "rows": len(group),
            "repeats": ",".join(repeats),
            "passed_rows": sum(1 for status in statuses if status == "passed"),
            "failed_rows": sum(1 for status in statuses if status == "failed"),
            "x_max_min": min(x_values) if x_values else "",
            "x_max_max": max(x_values) if x_values else "",
            "overall_p1_min": min(p1_values) if p1_values else "",
            "overall_p1_max": max(p1_values) if p1_values else "",
            "overall_p1_mean": p1_mean if p1_values else "",
            "min_h_min": min(min_h_values) if min_h_values else "",
            "min_h_max": max(min_h_values) if min_h_values else "",
            "dominant_top_positions": ";".join(f"{key}x{count}" for key, count in top_key_counter.most_common(6)),
            "worst_positions_by_repeat": "; ".join(worst_positions),
            "top_position_detail": ";".join(top_detail[:24]),
        }
        row["failure_mode"] = classify(row)
        out_rows.append(row)

    fields = [
        "warmup_bytes",
        "status_summary",
        "failure_mode",
        "rows",
        "repeats",
        "passed_rows",
        "failed_rows",
        "x_max_min",
        "x_max_max",
        "overall_p1_min",
        "overall_p1_max",
        "overall_p1_mean",
        "min_h_min",
        "min_h_max",
        "dominant_top_positions",
        "worst_positions_by_repeat",
        "top_position_detail",
    ]
    write_csv(OUT_CSV, out_rows, fields)

    lines = [
        "# random1 regs-only Restart Failure-Mode Analysis 20260524",
        "",
        "This is an offline synthesis of the SP800-90B restart warmup sweep and per-column bias diagnostics.",
        "It separates fixed-column hotspots from global p1 shifts and passband behavior.",
        "",
        "## Key Result",
        "",
        "The restart pass/fail boundary is not mirrored by pairwise reset-enable TDC warmup-edge entropy.",
        "Instead, the restart data itself shows a windowed output-position effect: warmups 5/6/8/10 form a restart-safe passband, while adjacent warmups fail through either fixed-column hotspots or global p1 shifts.",
        "",
        "| warmup | status | mode | X_max | p1 mean | top positions |",
        "| ---: | --- | --- | ---: | ---: | --- |",
    ]
    for row in out_rows:
        x_text = f"{row['x_max_min']}-{row['x_max_max']}"
        p1_text = f"{float(row['overall_p1_mean']):.6f}" if row["overall_p1_mean"] != "" else ""
        lines.append(
            f"| {row['warmup_bytes']} | {row['status_summary']} | {row['failure_mode']} | {x_text} | {p1_text} | {row['dominant_top_positions']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Warmup0 fails mainly as fixed-column hotspot behavior: overall p1 is near 0.5, but X_max is extreme.",
            "- Warmup4 and warmup11/12/16 fail mainly through global p1 shifts or mixed global/column effects.",
            "- Warmup5/6/8/10 pass with X_max below cutoff, showing that the safe startup region is a passband rather than a monotonic delay effect.",
            "- Existing pairwise TDC does not show a 4->5 or 10->11 entropy jump, so the passband is probably not a simple two-RO phase-diffusion threshold visible in raw TDC bins.",
            "- The stronger mechanism is sampler-path/output-position dependent: sampling-register placement can repair steady-state stream quality, while restart robustness depends on which early sampled positions are emitted after reset.",
            "",
            "## Next Hardware Target",
            "",
            "The next meaningful hardware design should instrument the true TRNG sampling path rather than another isolated two-RO TDC pair. Two good options:",
            "",
            "1. A restart-position diagnostic top that emits early sampled bytes plus row/position markers for warmup 4/5/10/11.",
            "2. A sampler-register diagnostic top that exposes selected sampled_data lanes or per-stage XOR groups around the 64 sampling registers.",
            "",
            "Both are better aligned with the current evidence than broad repeat captures.",
            "",
            f"- CSV: `{OUT_CSV.relative_to(ROOT)}`",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
