#!/usr/bin/env python3
"""Summarize partial route-lock feasibility probes.

The output is intentionally conservative: a run is only hardware-ready when it
has a bitstream, a clean route-status report, and enough route locks applied.
Current route-lock probes are expected to fail this gate; that is useful because
it prevents accidental board programming from fragile route replay attempts.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROBE_ROOT = ROOT / "data/vivado_runs/route_lock_probe_20260528"
DEFAULT_LOCK_ROOT = ROOT / "data/experiments/route_lock_20260528"
DEFAULT_OUT = ROOT / "data/experiments/route_lock_20260528/route_lock_feasibility_20260528"


def parse_kv_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def count_text(path: Path, pattern: str) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(pattern, text))


def to_int(value: str | None, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except ValueError:
        return default


def source_summaries(lock_root: Path) -> dict[str, dict[str, str]]:
    summaries: dict[str, dict[str, str]] = {}
    for path in lock_root.glob("*.tcl.summary.txt"):
        data = parse_kv_file(path)
        label = data.get("label") or path.name.replace(".tcl.summary.txt", "")
        data["summary_file"] = str(path)
        summaries[label] = data
    return summaries


def route_status_clean(path: Path) -> str:
    if not path.exists():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    bad_patterns = [
        "unrouted",
        "partially routed",
        "routing errors",
        "nets with routing errors",
    ]
    return "no" if any(p in text for p in bad_patterns) else "yes"


def summarize_builds(probe_root: Path, lock_root: Path, min_applied_ratio: float) -> list[dict[str, object]]:
    src = source_summaries(lock_root)
    rows: list[dict[str, object]] = []
    for run_dir in sorted([p for p in probe_root.iterdir() if p.is_dir()]):
        name = run_dir.name
        bitstreams = list(run_dir.glob("*.bit"))
        route_status = run_dir / "reports/route_status.rpt"
        routed_dcp = run_dir / "checkpoints/RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
        post_physopt_dcp = run_dir / "checkpoints/RO_TRNG_restart_fifo_compact_diag_top_post_physopt.dcp"
        physopt_dcp = run_dir / "checkpoints/RO_TRNG_restart_fifo_compact_diag_top_physopt.dcp"

        # Infer the exported route-lock source from the run name.
        label_hint = ""
        if "data_sampled" in name:
            label_hint = "compact_w4_data_sampled"
        elif "sampled_regs_data" in name:
            label_hint = "compact_w4_sampled_regs_and_data"
        elif "sampled_data" in name:
            label_hint = "compact_w4_sampled_data"
        elif "sampled_bel_routes" in name:
            label_hint = "compact_w4_sampled_data"

        selected = to_int(src.get(label_hint, {}).get("selected_nets"))
        source_summary = src.get(label_hint, {}).get("summary_file", "")

        all_text_files = list(run_dir.rglob("*"))
        text_paths = [p for p in all_text_files if p.is_file() and p.suffix.lower() in {".jou", ".log", ".txt", ".rpt"}]
        route_applied = sum(count_text(p, r"ROUTE_LOCK_APPLIED") for p in text_paths)
        route_failed = sum(count_text(p, r"ROUTE_LOCK_FAILED") for p in text_paths)
        route_skipped = sum(count_text(p, r"ROUTE_LOCK_SKIP") for p in text_paths)
        cell_failed = sum(count_text(p, r"CELL_LOCK_FAILED") for p in text_paths)

        applied_ratio = (route_applied / selected) if selected else 0.0
        clean = route_status_clean(route_status)
        has_bitstream = bool(bitstreams)
        has_routed_dcp = routed_dcp.exists()
        reached_post_physopt = post_physopt_dcp.exists() or physopt_dcp.exists()

        ready = (
            has_bitstream
            and clean == "yes"
            and selected > 0
            and applied_ratio >= min_applied_ratio
            and route_failed == 0
            and route_skipped == 0
            and cell_failed == 0
        )
        if not has_bitstream:
            reason = "no_bitstream"
        elif clean != "yes":
            reason = "route_status_not_clean"
        elif selected == 0:
            reason = "unknown_selected_net_count"
        elif applied_ratio < min_applied_ratio:
            reason = "insufficient_route_lock_coverage"
        elif route_failed or route_skipped or cell_failed:
            reason = "route_or_cell_lock_failures"
        else:
            reason = "ready"

        rows.append(
            {
                "run": name,
                "label_hint": label_hint,
                "selected_nets": selected,
                "route_lock_applied": route_applied,
                "route_lock_failed": route_failed,
                "route_lock_skipped": route_skipped,
                "cell_lock_failed": cell_failed,
                "applied_ratio": f"{applied_ratio:.6f}",
                "has_physopt_or_postphysopt_checkpoint": str(reached_post_physopt),
                "has_routed_checkpoint": str(has_routed_dcp),
                "has_bitstream": str(has_bitstream),
                "route_status_clean": clean,
                "hardware_gate": "READY_FOR_HARDWARE" if ready else "DO_NOT_PROGRAM",
                "gate_reason": reason,
                "source_summary": source_summary,
            }
        )
    return rows


def summarize_dryruns(lock_root: Path, min_applied_ratio: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    src = source_summaries(lock_root)
    for path in sorted(lock_root.glob("dryrun_*/*_probe_summary.txt")):
        data = parse_kv_file(path)
        label = data.get("label", path.stem)
        apply_tcl = data.get("apply_tcl", "")
        source_status = data.get("source_status", "missing")

        selected = 0
        source_summary = ""
        for summary in src.values():
            if summary.get("out_file", "").replace("\\", "/") == apply_tcl.replace("\\", "/"):
                selected = to_int(summary.get("selected_nets"))
                source_summary = summary.get("summary_file", "")
                break

        route_applied = to_int(data.get("route_lock_applied"))
        route_failed = to_int(data.get("route_lock_failed"))
        cell_failed = to_int(data.get("cell_lock_failed"))
        applied_ratio = (route_applied / selected) if selected else 0.0
        ready = (
            source_status == "ok"
            and selected > 0
            and applied_ratio >= min_applied_ratio
            and route_failed == 0
            and cell_failed == 0
        )
        if source_status != "ok":
            reason = "probe_source_failed"
        elif selected == 0:
            reason = "unknown_selected_net_count"
        elif applied_ratio < min_applied_ratio:
            reason = "insufficient_route_lock_coverage"
        elif route_failed or cell_failed:
            reason = "route_or_cell_lock_failures"
        else:
            reason = "ready_for_build_attempt"

        rows.append(
            {
                "run": label,
                "label_hint": "dryrun",
                "selected_nets": selected,
                "route_lock_applied": route_applied,
                "route_lock_failed": route_failed,
                "route_lock_skipped": 0,
                "cell_lock_failed": cell_failed,
                "applied_ratio": f"{applied_ratio:.6f}",
                "has_physopt_or_postphysopt_checkpoint": "True",
                "has_routed_checkpoint": "False",
                "has_bitstream": "False",
                "route_status_clean": "not_routed",
                "hardware_gate": "READY_FOR_BUILD_ATTEMPT" if ready else "DO_NOT_PROGRAM",
                "gate_reason": reason,
                "source_summary": source_summary,
                "probe_summary": str(path),
                "source_status": source_status,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], min_applied_ratio: float) -> None:
    fields = [
        "run",
        "selected_nets",
        "route_lock_applied",
        "route_lock_failed",
        "route_lock_skipped",
        "applied_ratio",
        "has_bitstream",
        "hardware_gate",
        "gate_reason",
    ]
    with path.open("w", encoding="utf-8") as f:
        f.write("# Route-Lock Feasibility Gate 20260528\n\n")
        f.write(
            "This is an offline gate for partial route-lock attempts. A build should not be programmed "
            "unless the gate says READY_FOR_HARDWARE. The current threshold is "
            f"applied_ratio >= {min_applied_ratio:.2f}, zero route/cell failures, clean route status, and a bitstream.\n\n"
        )
        f.write("| " + " | ".join(fields) + " |\n")
        f.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-root", type=Path, default=DEFAULT_PROBE_ROOT)
    parser.add_argument("--lock-root", type=Path, default=DEFAULT_LOCK_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--min-applied-ratio", type=float, default=0.875)
    args = parser.parse_args()

    rows = summarize_builds(args.probe_root, args.lock_root, args.min_applied_ratio)
    rows.extend(summarize_dryruns(args.lock_root, args.min_applied_ratio))
    if not rows:
        raise SystemExit(f"No route-lock probe build directories found in {args.probe_root}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "route_lock_feasibility_20260528.csv"
    md_path = args.out_dir / "route_lock_feasibility_20260528.md"
    write_csv(csv_path, rows)
    write_markdown(md_path, rows, args.min_applied_ratio)
    print(csv_path)
    print(md_path)
    for row in rows:
        print(f"{row['hardware_gate']} {row['run']} reason={row['gate_reason']} applied={row['route_lock_applied']}/{row['selected_nets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
