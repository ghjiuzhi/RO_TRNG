#!/usr/bin/env python3
"""Create a hardware capture queue for restart reduced-XOR counterfactuals."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


TOP = "RO_TRNG_restart_reduced_xor_top.bit"


def split_csv(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", default="sampler_island_local")
    parser.add_argument("--warmups", default="10")
    parser.add_argument("--modes", default="data_ro")
    parser.add_argument("--indexes", default="2")
    parser.add_argument("--tag", default="20260526")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--capture-dir", default=r"data\hardware\20260511_fpga1_board1\restart")
    parser.add_argument("--metadata-dir", default=r"data\hardware\20260511_fpga1_board1\metadata")
    parser.add_argument("--bytes", default="125008")
    parser.add_argument("--idle-timeout-sec", default="180")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for variant in split_csv(args.variants):
        for warmup_text in split_csv(args.warmups):
            warmup = int(warmup_text)
            for mode in split_csv(args.modes):
                for index_text in split_csv(args.indexes):
                    index = int(index_text)
                    run = (
                        f"restart_reduced_xor_random1_{variant}_warmup{warmup}_"
                        f"{mode}{index}_1000x125_strict_{args.tag}"
                    )
                    bitstream = (
                        f"data\\vivado_runs\\restart_reduced_xor_random1_{variant}_"
                        f"formal_bits_1000x125_warmup{warmup}_{mode}{index}_"
                        f"header_delay60s\\{TOP}"
                    )
                    rows.append(
                        {
                            "enabled": "1",
                            "priority": "P0" if warmup == 10 and mode == "data_ro" and index == 2 else "P1",
                            "run": run,
                            "kind": "restart",
                            "bitstream": bitstream,
                            "bytes": args.bytes,
                            "out_file": f"{args.capture_dir}\\{run}.bin",
                            "metadata_dir": args.metadata_dir,
                            "analyze_group": f"restart_reduced_xor_strict_{args.tag}",
                            "idle_timeout_sec": args.idle_timeout_sec,
                            "notes": f"reduced_xor variant={variant} warmup={warmup} mode={mode} index={index}",
                        }
                    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "enabled",
                "priority",
                "run",
                "kind",
                "bitstream",
                "bytes",
                "out_file",
                "metadata_dir",
                "analyze_group",
                "idle_timeout_sec",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.out} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
