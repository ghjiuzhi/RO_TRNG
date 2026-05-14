#!/usr/bin/env python3
"""Convert RO frequency probe UART frames into mechanism-validation CSVs."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


FRAME_LEN = 14
MAGIC = (0x52, 0x46)
MODE_NAMES = {0: "all_on", 1: "single_on"}
DEFAULT_FAMILY_NAMES = {0: "unknown", 1: "random1", 3: "random3"}
MEASUREMENT_FIELDS = [
    "source_file",
    "family_id",
    "family",
    "mode_id",
    "mode",
    "target_index",
    "target_name",
    "active_data_mask",
    "sample_active",
    "window_cycles",
    "window_ns",
    "count",
    "freq_mhz",
    "seq",
]
SUMMARY_FIELDS = [
    "family",
    "family_id",
    "mode",
    "mode_id",
    "target_index",
    "target_name",
    "window_cycles",
    "window_ns",
    "samples",
    "freq_mean_mhz",
    "freq_std_mhz",
    "freq_std_ppm",
    "freq_min_mhz",
    "freq_max_mhz",
]
PAIRWISE_FIELDS = [
    "family",
    "mode",
    "a_index",
    "a_name",
    "b_index",
    "b_name",
    "relation",
    "freq_a_mhz",
    "freq_b_mhz",
    "abs_delta_f_mhz",
    "beat_period_ns",
]
PULLING_FIELDS = [
    "family",
    "target_index",
    "target_name",
    "all_on_freq_mhz",
    "single_on_freq_mhz",
    "shift_mhz",
    "shift_ppm_vs_single",
]


def checksum(frame: bytes) -> int:
    value = 0
    for byte in frame[:-1]:
        value ^= byte
    return value & 0xFF


def parse_frames(path: Path, family_names: dict[int, str], sys_clk_mhz: float) -> tuple[list[dict[str, object]], int]:
    data = path.read_bytes()
    rows: list[dict[str, object]] = []
    dropped = 0
    i = 0
    while i <= len(data) - FRAME_LEN:
        if data[i] != MAGIC[0] or data[i + 1] != MAGIC[1]:
            dropped += 1
            i += 1
            continue
        frame = data[i : i + FRAME_LEN]
        if checksum(frame) != frame[-1]:
            dropped += 1
            i += 1
            continue

        family_id = frame[3]
        mode = frame[4]
        target = frame[5] & 0x0F
        window_cycles = frame[8] | (frame[9] << 8)
        count = frame[10]
        seq = frame[11] | (frame[12] << 8)
        window_ns = window_cycles * 1000.0 / sys_clk_mhz
        freq_mhz = count / window_ns * 1000.0 if window_ns else 0.0
        rows.append(
            {
                "source_file": str(path),
                "family_id": family_id,
                "family": family_names.get(family_id, f"family{family_id}"),
                "mode_id": mode,
                "mode": MODE_NAMES.get(mode, f"mode{mode}"),
                "target_index": target,
                "target_name": "sample" if target == 8 else f"data{target}",
                "active_data_mask": f"0x{frame[6]:02x}",
                "sample_active": frame[7] & 1,
                "window_cycles": window_cycles,
                "window_ns": window_ns,
                "count": count,
                "freq_mhz": freq_mhz,
                "seq": seq,
            }
        )
        i += FRAME_LEN
    dropped += max(0, len(data) - i)
    return rows, dropped


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], list[float]] = defaultdict(list)
    meta: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = (row["family"], row["family_id"], row["mode"], row["mode_id"], row["target_index"], row["target_name"])
        groups[key].append(float(row["freq_mhz"]))
        meta[key] = {
            "family": row["family"],
            "family_id": row["family_id"],
            "mode": row["mode"],
            "mode_id": row["mode_id"],
            "target_index": row["target_index"],
            "target_name": row["target_name"],
            "window_cycles": row["window_cycles"],
            "window_ns": row["window_ns"],
        }

    out: list[dict[str, object]] = []
    for key in sorted(groups):
        values = groups[key]
        mean = statistics.fmean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        out.append(
            {
                **meta[key],
                "samples": len(values),
                "freq_mean_mhz": mean,
                "freq_std_mhz": std,
                "freq_std_ppm": std / mean * 1e6 if mean else 0.0,
                "freq_min_mhz": min(values),
                "freq_max_mhz": max(values),
            }
        )
    return out


def mean_lookup(summary_rows: list[dict[str, object]], mode: str) -> dict[tuple[str, int], float]:
    result: dict[tuple[str, int], float] = {}
    for row in summary_rows:
        if row["mode"] == mode:
            result[(str(row["family"]), int(row["target_index"]))] = float(row["freq_mean_mhz"])
    return result


def pairwise(summary_rows: list[dict[str, object]], mode: str) -> list[dict[str, object]]:
    means = mean_lookup(summary_rows, mode)
    families = sorted({family for family, _ in means})
    out: list[dict[str, object]] = []
    for family in families:
        for a in range(9):
            for b in range(a + 1, 9):
                if (family, a) not in means or (family, b) not in means:
                    continue
                fa = means[(family, a)]
                fb = means[(family, b)]
                delta = abs(fa - fb)
                relation = "data_sample" if 8 in (a, b) else "data_data"
                out.append(
                    {
                        "family": family,
                        "mode": mode,
                        "a_index": a,
                        "a_name": "sample" if a == 8 else f"data{a}",
                        "b_index": b,
                        "b_name": "sample" if b == 8 else f"data{b}",
                        "relation": relation,
                        "freq_a_mhz": fa,
                        "freq_b_mhz": fb,
                        "abs_delta_f_mhz": delta,
                        "beat_period_ns": 1000.0 / delta if delta else math.inf,
                    }
                )
    return sorted(out, key=lambda row: (row["family"], row["relation"], row["abs_delta_f_mhz"]))


def pulling(summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    all_on = mean_lookup(summary_rows, "all_on")
    single_on = mean_lookup(summary_rows, "single_on")
    out: list[dict[str, object]] = []
    for key in sorted(all_on):
        if key not in single_on:
            continue
        family, target = key
        all_freq = all_on[key]
        single_freq = single_on[key]
        shift = all_freq - single_freq
        out.append(
            {
                "family": family,
                "target_index": target,
                "target_name": "sample" if target == 8 else f"data{target}",
                "all_on_freq_mhz": all_freq,
                "single_on_freq_mhz": single_freq,
                "shift_mhz": shift,
                "shift_ppm_vs_single": shift / single_freq * 1e6 if single_freq else 0.0,
            }
        )
    return out


def parse_family_map(text: str | None) -> dict[int, str]:
    result = dict(DEFAULT_FAMILY_NAMES)
    if not text:
        return result
    for item in text.split(","):
        if not item.strip():
            continue
        key, value = item.split("=", 1)
        result[int(key.strip())] = value.strip()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path, help="Raw UART frame files from RO_FREQ_trng_probe_top")
    parser.add_argument("--sys-clk-mhz", type=float, default=200.0, help="Measurement FSM clock frequency")
    parser.add_argument("--family-map", default=None, help="Comma list such as 1=random1,3=random3")
    parser.add_argument("--out-dir", type=Path, default=Path("data/experiments/ro_freq_analysis"))
    parser.add_argument("--prefix", default="ro_freq")
    args = parser.parse_args()

    family_names = parse_family_map(args.family_map)
    measurements: list[dict[str, object]] = []
    dropped_total = 0
    for path in args.inputs:
        rows, dropped = parse_frames(path, family_names, args.sys_clk_mhz)
        measurements.extend(rows)
        dropped_total += dropped

    if not measurements:
        raise SystemExit("No valid RO frequency frames found.")

    summary_rows = summarize(measurements)
    pair_rows = pairwise(summary_rows, "all_on")
    pulling_rows = pulling(summary_rows)

    write_csv(args.out_dir / f"{args.prefix}_measurements.csv", measurements, MEASUREMENT_FIELDS)
    write_csv(args.out_dir / f"{args.prefix}_summary.csv", summary_rows, SUMMARY_FIELDS)
    write_csv(args.out_dir / f"{args.prefix}_pairwise_all_on.csv", pair_rows, PAIRWISE_FIELDS)
    write_csv(args.out_dir / f"{args.prefix}_pulling.csv", pulling_rows, PULLING_FIELDS)

    print(f"valid_frames={len(measurements)} dropped_or_unframed_bytes={dropped_total}")
    print(f"wrote {args.out_dir / f'{args.prefix}_measurements.csv'}")
    print(f"wrote {args.out_dir / f'{args.prefix}_summary.csv'}")
    print(f"wrote {args.out_dir / f'{args.prefix}_pairwise_all_on.csv'}")
    print(f"wrote {args.out_dir / f'{args.prefix}_pulling.csv'}")


if __name__ == "__main__":
    main()
