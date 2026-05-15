#!/usr/bin/env python3
"""Plot the restart warmup transition from the compact CSV table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def status_value(status: str) -> int:
    return 1 if status.lower() == "passed" else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.csv"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/experiments/paper_artifacts_20260515"),
    )
    args = parser.parse_args()

    if args.input.exists():
        rows = [row for row in read_rows(args.input) if row.get("msb_status") or row.get("lsb_status")]
    else:
        rows = []
    mechanism_table = args.out_dir / "table_restart_mechanism_link.csv"
    if mechanism_table.exists():
        rows = []
        for row in read_rows(mechanism_table):
            if row.get("placement") != "random3":
                continue
            if not row.get("bit_order", "").startswith("packed_warmup"):
                continue
            if not row.get("warmup_bytes"):
                continue
            rows.append(
                {
                    "warmup_bytes": row["warmup_bytes"],
                    "packed_sha256": row.get("restart_capture_sha256", ""),
                    "overall_p1": row.get("restart_overall_p1", ""),
                    "positions_over_x_cutoff": row.get("restart_positions_over_x_cutoff", ""),
                    "worst_byte": row.get("restart_worst_byte", ""),
                    "worst_bit": row.get("restart_worst_bit", ""),
                    "worst_x": row.get("restart_worst_x", ""),
                    "worst_p1": row.get("restart_worst_p1", ""),
                    "msb_status": row.get("ea_restart_status_msb", ""),
                    "msb_x_cutoff": row.get("restart_x_cutoff_msb", ""),
                    "msb_x_max": row.get("restart_x_max_msb", ""),
                    "msb_min_entropy": row.get("restart_min_entropy_msb", ""),
                    "lsb_status": row.get("ea_restart_status_lsb", ""),
                    "lsb_x_cutoff": row.get("restart_x_cutoff_lsb", ""),
                    "lsb_x_max": row.get("restart_x_max_lsb", ""),
                    "lsb_min_entropy": row.get("restart_min_entropy_lsb", ""),
                    "repeat_id": row.get("repeat_id", "") or ("repeat02" if "repeat02" in row.get("bit_order", "") else "run01"),
                    "bit_order": row.get("bit_order", ""),
                }
            )
    rows.sort(key=lambda row: int(row["warmup_bytes"]))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    transition_csv = args.out_dir / "table_restart_warmup_transition_with_repeats.csv"
    fieldnames = [
        "warmup_bytes",
        "repeat_id",
        "bit_order",
        "packed_sha256",
        "overall_p1",
        "positions_over_x_cutoff",
        "worst_byte",
        "worst_bit",
        "worst_x",
        "worst_p1",
        "msb_status",
        "msb_x_cutoff",
        "msb_x_max",
        "msb_min_entropy",
        "lsb_status",
        "lsb_x_cutoff",
        "lsb_x_max",
        "lsb_min_entropy",
    ]
    with transition_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})

    import matplotlib.pyplot as plt

    x = [int(row["warmup_bytes"]) + (0.08 if row.get("repeat_id") == "repeat02" else -0.08) for row in rows]
    tick_x = sorted({int(row["warmup_bytes"]) for row in rows})
    worst_x = [int(row["worst_x"]) for row in rows]
    positions = [int(row["positions_over_x_cutoff"]) for row in rows]
    msb_pass = [status_value(row["msb_status"]) for row in rows]
    lsb_pass = [status_value(row["lsb_status"]) for row in rows]

    fig, axes = plt.subplots(3, 1, figsize=(7.2, 7.4), sharex=True)
    axes[0].plot(x, worst_x, marker="o", color="#1f5a7a", linewidth=2)
    axes[0].axhline(605, color="#b33f3f", linestyle="--", linewidth=1.2, label="MSB cutoff 605")
    axes[0].axhline(632, color="#c9852b", linestyle=":", linewidth=1.2, label="LSB cutoff 632")
    axes[0].set_ylabel("Worst column X")
    axes[0].legend(frameon=False, loc="best")
    axes[0].grid(True, axis="y", alpha=0.25)

    axes[1].bar(x, positions, color="#6c7a40", width=0.75)
    axes[1].set_ylabel("Columns over cutoff")
    axes[1].grid(True, axis="y", alpha=0.25)

    axes[2].plot(x, msb_pass, marker="s", color="#2f7d4f", linewidth=2, label="MSB")
    axes[2].plot(x, lsb_pass, marker="^", color="#7b4b8a", linewidth=2, label="LSB")
    axes[2].set_yticks([0, 1], labels=["fail", "pass"])
    axes[2].set_xlabel("Warmup bytes")
    axes[2].set_ylabel("ea_restart")
    axes[2].set_xticks(tick_x)
    axes[2].legend(frameon=False, loc="best")
    axes[2].grid(True, axis="y", alpha=0.25)

    fig.suptitle("Restart Warmup Transition on random3")
    fig.tight_layout()

    png_path = args.out_dir / "fig_restart_warmup_transition.png"
    svg_path = args.out_dir / "fig_restart_warmup_transition.svg"
    fig.savefig(png_path, dpi=180)
    fig.savefig(svg_path)
    plt.close(fig)

    print(f"Wrote {png_path}")
    print(f"Wrote {svg_path}")
    print(f"Wrote {transition_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
