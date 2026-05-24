#!/usr/bin/env python3
"""Offline position-structure analysis for 20 MiB TRNG placement captures.

This script reads existing raw byte captures only. It does not call Vivado,
hardware servers, UART capture scripts, or any board-facing tooling.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only on minimal Python installs.
    np = None


DEFAULT_INPUT_DIR = Path("data/hardware/20260511_fpga1_board1/trng")
DEFAULT_OUTPUT_DIR = Path("data/experiments/position_structure_20260523")
DEFAULT_GLOB = "*repeat03*.bin"

REPEAT_RE = re.compile(r"^(?P<placement>.+)_repeat(?P<run>\d+)(?:_(?P<size>\d+mib))?$", re.IGNORECASE)
RUN_RE = re.compile(r"^(?P<placement>.+)_run(?P<run>\d+)(?:_(?P<size>\d+mib))?$", re.IGNORECASE)


@dataclass(frozen=True)
class ByteInfo:
    ones: int
    bits: tuple[int, ...]
    first: int
    last: int
    internal_pairs: tuple[int, int, int, int]
    runs: tuple[tuple[int, int], ...]
    leading_bit: int
    leading_len: int
    trailing_bit: int
    trailing_len: int
    all_same: bool


def build_byte_table() -> list[ByteInfo]:
    table: list[ByteInfo] = []
    for value in range(256):
        bits = tuple((value >> shift) & 1 for shift in range(7, -1, -1))
        pairs = [0, 0, 0, 0]
        for left, right in zip(bits, bits[1:]):
            pairs[(left << 1) | right] += 1

        runs: list[tuple[int, int]] = []
        current = bits[0]
        length = 1
        for bit in bits[1:]:
            if bit == current:
                length += 1
            else:
                runs.append((current, length))
                current = bit
                length = 1
        runs.append((current, length))

        table.append(
            ByteInfo(
                ones=sum(bits),
                bits=bits,
                first=bits[0],
                last=bits[-1],
                internal_pairs=tuple(pairs),
                runs=tuple(runs),
                leading_bit=runs[0][0],
                leading_len=runs[0][1],
                trailing_bit=runs[-1][0],
                trailing_len=runs[-1][1],
                all_same=len(runs) == 1,
            )
        )
    return table


BYTE_TABLE = build_byte_table()


def classify_path(path: Path) -> dict[str, str]:
    stem = path.stem
    for regex, role in ((REPEAT_RE, "repeat"), (RUN_RE, "formal")):
        match = regex.match(stem)
        if match:
            return {
                "capture_id": stem,
                "placement": match.group("placement"),
                "run": match.group("run"),
                "sample_role": role,
            }
    return {"capture_id": stem, "placement": stem, "run": "", "sample_role": ""}


def run_bucket(length: int) -> str:
    if length <= 4:
        return f"runs_len{length}"
    if length <= 8:
        return "runs_len5_8"
    if length <= 16:
        return "runs_len9_16"
    if length <= 32:
        return "runs_len17_32"
    return "runs_len_gt32"


def phi_from_pairs(n00: int, n01: int, n10: int, n11: int) -> float:
    row0 = n00 + n01
    row1 = n10 + n11
    col0 = n00 + n10
    col1 = n01 + n11
    denom = math.sqrt(row0 * row1 * col0 * col1)
    if denom == 0.0:
        return math.nan
    return ((n00 * n11) - (n01 * n10)) / denom


def bit_min_entropy(p1: float) -> float:
    return -math.log2(max(p1, 1.0 - p1)) if 0.0 <= p1 <= 1.0 else math.nan


def iter_files(inputs: list[Path], glob_pattern: str) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        if item.is_dir():
            files.extend(sorted(item.glob(glob_pattern)))
        elif item.is_file():
            files.append(item)
    return sorted(dict.fromkeys(files))


def finish_run(
    bit: int | None,
    length: int,
    longest: list[int],
    bucket_counts: dict[str, int],
    total_runs: list[int],
) -> None:
    if bit is None or length <= 0:
        return
    longest[bit] = max(longest[bit], length)
    bucket_counts[run_bucket(length)] += 1
    total_runs[0] += 1


def analyze_file(path: Path, chunk_size: int) -> dict[str, Any]:
    if np is not None:
        return analyze_file_numpy(path)
    return analyze_file_standard(path, chunk_size)


def analyze_file_numpy(path: Path) -> dict[str, Any]:
    data = np.fromfile(path, dtype=np.uint8)
    byte_count = int(data.size)
    bit_count = byte_count * 8
    if byte_count == 0:
        raise ValueError(f"Empty capture: {path}")

    ones_lookup = np.array([item.ones for item in BYTE_TABLE], dtype=np.uint8)
    byte_ones = ones_lookup[data]
    ones = int(byte_ones.sum(dtype=np.uint64))
    p1 = ones / bit_count

    bits = np.unpackbits(data, bitorder="big")
    pos_ones = bits.reshape((-1, 8)).sum(axis=0, dtype=np.uint64)

    pair_codes = (bits[:-1].astype(np.uint8) << 1) | bits[1:].astype(np.uint8)
    pair_counts_np = np.bincount(pair_codes, minlength=4)
    pair_counts = [int(v) for v in pair_counts_np[:4]]

    change_idx = np.flatnonzero(bits[1:] != bits[:-1]) + 1
    starts = np.concatenate((np.array([0], dtype=np.int64), change_idx))
    ends = np.concatenate((change_idx, np.array([bit_count], dtype=np.int64)))
    lengths = ends - starts
    values = bits[starts]

    longest = [0, 0]
    bucket_counts = {
        "runs_len1": 0,
        "runs_len2": 0,
        "runs_len3": 0,
        "runs_len4": 0,
        "runs_len5_8": 0,
        "runs_len9_16": 0,
        "runs_len17_32": 0,
        "runs_len_gt32": 0,
    }
    total_runs = int(lengths.size)
    for bit in (0, 1):
        selected = lengths[values == bit]
        longest[bit] = int(selected.max()) if selected.size else 0
    bucket_counts["runs_len1"] = int(np.count_nonzero(lengths == 1))
    bucket_counts["runs_len2"] = int(np.count_nonzero(lengths == 2))
    bucket_counts["runs_len3"] = int(np.count_nonzero(lengths == 3))
    bucket_counts["runs_len4"] = int(np.count_nonzero(lengths == 4))
    bucket_counts["runs_len5_8"] = int(np.count_nonzero((lengths >= 5) & (lengths <= 8)))
    bucket_counts["runs_len9_16"] = int(np.count_nonzero((lengths >= 9) & (lengths <= 16)))
    bucket_counts["runs_len17_32"] = int(np.count_nonzero((lengths >= 17) & (lengths <= 32)))
    bucket_counts["runs_len_gt32"] = int(np.count_nonzero(lengths > 32))

    row = build_result_row(
        path=path,
        byte_count=byte_count,
        bit_count=bit_count,
        ones=ones,
        p1=p1,
        pair_counts=pair_counts,
        pos_ones=[int(v) for v in pos_ones],
        longest=longest,
        total_runs=total_runs,
        bucket_counts=bucket_counts,
    )

    for mod in (16, 32):
        biases: list[float] = []
        max_slot = ""
        max_abs = -1.0
        for slot in range(mod):
            slot_bytes = byte_ones[slot::mod]
            slot_p1 = int(slot_bytes.sum(dtype=np.uint64)) / (int(slot_bytes.size) * 8)
            bias = slot_p1 - 0.5
            row[f"bytepos_mod{mod}_{slot:02d}_p1"] = slot_p1
            row[f"bytepos_mod{mod}_{slot:02d}_bias"] = bias
            biases.append(bias)
            if abs(bias) > max_abs:
                max_abs = abs(bias)
                max_slot = str(slot)
        row[f"bytepos_mod{mod}_max_abs_bias"] = max_abs
        row[f"bytepos_mod{mod}_max_abs_bias_slot"] = max_slot
        row[f"bytepos_mod{mod}_span_p1"] = max(biases) - min(biases)
    return row


def build_result_row(
    path: Path,
    byte_count: int,
    bit_count: int,
    ones: int,
    p1: float,
    pair_counts: list[int],
    pos_ones: list[int],
    longest: list[int],
    total_runs: int,
    bucket_counts: dict[str, int],
) -> dict[str, Any]:
    adjacent_pairs = bit_count - 1 if bit_count > 1 else 0
    adjacent_equal = (pair_counts[0] + pair_counts[3]) / adjacent_pairs if adjacent_pairs else math.nan
    lag1_phi = phi_from_pairs(*pair_counts)

    row: dict[str, Any] = {
        "file": str(path),
        "name": path.name,
        **classify_path(path),
        "bytes": byte_count,
        "bits": bit_count,
        "ones": ones,
        "p1": p1,
        "abs_bias": abs(p1 - 0.5) if not math.isnan(p1) else math.nan,
        "bit_min_entropy": bit_min_entropy(p1),
        "adjacent_equal": adjacent_equal,
        "lag1_phi": lag1_phi,
        "lag1_n00": pair_counts[0],
        "lag1_n01": pair_counts[1],
        "lag1_n10": pair_counts[2],
        "lag1_n11": pair_counts[3],
        "longest_zero_run": longest[0],
        "longest_one_run": longest[1],
        "runs_total": total_runs,
    }

    for idx, count in enumerate(pos_ones):
        col_p1 = count / byte_count if byte_count else math.nan
        row[f"bitpos{idx}_p1"] = col_p1
        row[f"bitpos{idx}_bias"] = col_p1 - 0.5 if not math.isnan(col_p1) else math.nan

    row.update(bucket_counts)
    row["runs_len1_fraction"] = bucket_counts["runs_len1"] / total_runs if total_runs else math.nan
    return row


def analyze_file_standard(path: Path, chunk_size: int) -> dict[str, Any]:
    byte_count = 0
    bit_count = 0
    ones = 0
    pos_ones = [0] * 8
    mod_ones = {16: [0] * 16, 32: [0] * 32}
    mod_bytes = {16: [0] * 16, 32: [0] * 32}
    pair_counts = [0, 0, 0, 0]  # 00, 01, 10, 11
    longest = [0, 0]
    total_runs = [0]
    bucket_counts = {
        "runs_len1": 0,
        "runs_len2": 0,
        "runs_len3": 0,
        "runs_len4": 0,
        "runs_len5_8": 0,
        "runs_len9_16": 0,
        "runs_len17_32": 0,
        "runs_len_gt32": 0,
    }
    prev_bit: int | None = None
    open_bit: int | None = None
    open_len = 0

    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for byte in chunk:
                info = BYTE_TABLE[byte]
                byte_count += 1
                bit_count += 8
                ones += info.ones

                for idx, bit in enumerate(info.bits):
                    pos_ones[idx] += bit

                byte_index = byte_count - 1
                for mod in (16, 32):
                    slot = byte_index % mod
                    mod_bytes[mod][slot] += 1
                    mod_ones[mod][slot] += info.ones

                for idx, count in enumerate(info.internal_pairs):
                    pair_counts[idx] += count
                if prev_bit is not None:
                    pair_counts[(prev_bit << 1) | info.first] += 1
                prev_bit = info.last

                if open_bit is None:
                    open_bit = info.leading_bit
                    open_len = info.leading_len
                    inner_runs = info.runs[1:]
                elif open_bit == info.leading_bit:
                    open_len += info.leading_len
                    inner_runs = info.runs[1:]
                else:
                    finish_run(open_bit, open_len, longest, bucket_counts, total_runs)
                    open_bit = info.leading_bit
                    open_len = info.leading_len
                    inner_runs = info.runs[1:]

                if info.all_same:
                    continue

                for run_bit, run_len in inner_runs[:-1]:
                    finish_run(run_bit, run_len, longest, bucket_counts, total_runs)
                tail_bit, tail_len = inner_runs[-1]
                finish_run(open_bit, open_len, longest, bucket_counts, total_runs)
                open_bit = tail_bit
                open_len = tail_len

    finish_run(open_bit, open_len, longest, bucket_counts, total_runs)

    p1 = ones / bit_count if bit_count else math.nan
    adjacent_pairs = bit_count - 1 if bit_count > 1 else 0
    adjacent_equal = (pair_counts[0] + pair_counts[3]) / adjacent_pairs if adjacent_pairs else math.nan
    lag1_phi = phi_from_pairs(*pair_counts)

    row: dict[str, Any] = {
        "file": str(path),
        "name": path.name,
        **classify_path(path),
        "bytes": byte_count,
        "bits": bit_count,
        "ones": ones,
        "p1": p1,
        "abs_bias": abs(p1 - 0.5) if not math.isnan(p1) else math.nan,
        "bit_min_entropy": bit_min_entropy(p1),
        "adjacent_equal": adjacent_equal,
        "lag1_phi": lag1_phi,
        "lag1_n00": pair_counts[0],
        "lag1_n01": pair_counts[1],
        "lag1_n10": pair_counts[2],
        "lag1_n11": pair_counts[3],
        "longest_zero_run": longest[0],
        "longest_one_run": longest[1],
        "runs_total": total_runs[0],
    }

    for idx, count in enumerate(pos_ones):
        col_p1 = count / byte_count if byte_count else math.nan
        row[f"bitpos{idx}_p1"] = col_p1
        row[f"bitpos{idx}_bias"] = col_p1 - 0.5 if not math.isnan(col_p1) else math.nan

    for mod in (16, 32):
        biases: list[float] = []
        max_slot = ""
        max_abs = -1.0
        for slot in range(mod):
            denom = mod_bytes[mod][slot] * 8
            slot_p1 = mod_ones[mod][slot] / denom if denom else math.nan
            bias = slot_p1 - 0.5 if not math.isnan(slot_p1) else math.nan
            row[f"bytepos_mod{mod}_{slot:02d}_p1"] = slot_p1
            row[f"bytepos_mod{mod}_{slot:02d}_bias"] = bias
            if not math.isnan(bias):
                biases.append(bias)
                if abs(bias) > max_abs:
                    max_abs = abs(bias)
                    max_slot = str(slot)
        row[f"bytepos_mod{mod}_max_abs_bias"] = max_abs if max_abs >= 0.0 else math.nan
        row[f"bytepos_mod{mod}_max_abs_bias_slot"] = max_slot
        row[f"bytepos_mod{mod}_span_p1"] = (max(biases) - min(biases)) if biases else math.nan

    row.update(bucket_counts)
    row["runs_len1_fraction"] = bucket_counts["runs_len1"] / total_runs[0] if total_runs[0] else math.nan
    return row


def format_value(value: Any) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        return f"{value:.12g}"
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_value(row.get(key, "")) for key in columns})


def mean(values: list[float]) -> float:
    clean = [v for v in values if not math.isnan(v)]
    return sum(clean) / len(clean) if clean else math.nan


def write_readme(path: Path, rows: list[dict[str, Any]]) -> None:
    sorted_abs_bias = sorted(rows, key=lambda r: float(r["abs_bias"]), reverse=True)
    sorted_lag = sorted(rows, key=lambda r: abs(float(r["lag1_phi"])), reverse=True)
    sorted_mod32 = sorted(rows, key=lambda r: float(r["bytepos_mod32_max_abs_bias"]), reverse=True)
    sorted_min_entropy = sorted(rows, key=lambda r: float(r["bit_min_entropy"]))

    def table(columns: list[str], data: list[dict[str, Any]]) -> str:
        lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
        for row in data:
            lines.append("| " + " | ".join(format_value(row.get(col, "")) for col in columns) + " |")
        return "\n".join(lines)

    overview_cols = [
        "capture_id",
        "placement",
        "bytes",
        "p1",
        "bit_min_entropy",
        "adjacent_equal",
        "lag1_phi",
        "bytepos_mod16_max_abs_bias",
        "bytepos_mod32_max_abs_bias",
        "longest_zero_run",
        "longest_one_run",
    ]
    bitpos_cols = ["capture_id"] + [f"bitpos{i}_bias" for i in range(8)]

    with path.open("w", encoding="utf-8") as f:
        f.write("# TRNG Position Structure Analysis 20260523\n\n")
        f.write("Offline analysis of existing 20 MiB placement captures under ")
        f.write("`data/hardware/20260511_fpga1_board1/trng`. No hardware or Vivado flow was started.\n\n")
        f.write("## Outputs\n\n")
        f.write("- `position_structure_summary.csv`: one row per capture with scalar metrics and expanded bit/byte-position fields.\n")
        f.write("- `README.md`: this summary.\n\n")
        f.write("## Metric Notes\n\n")
        f.write("- `p1`: fraction of one bits over the whole bitstream, MSB-first within each byte.\n")
        f.write("- `bit_min_entropy`: `-log2(max(p1, 1-p1))`, the binary most-common-value estimate.\n")
        f.write("- `adjacent_equal`: fraction of adjacent bit pairs that are `00` or `11`.\n")
        f.write("- `lag1_phi`: phi/Pearson correlation from adjacent-bit 2x2 counts.\n")
        f.write("- `bitpos0..7`: byte-internal bit positions, where 0 is the MSB and 7 is the LSB.\n")
        f.write("- `bytepos_mod16/mod32`: one-bit fraction grouped by byte index modulo 16 or 32.\n\n")
        f.write("## Core Findings\n\n")
        f.write(f"- Captures analyzed: {len(rows)}, total bytes: {sum(int(r['bytes']) for r in rows)}.\n")
        f.write(f"- Mean p1: {format_value(mean([float(r['p1']) for r in rows]))}; ")
        f.write(f"largest absolute whole-stream bias: {sorted_abs_bias[0]['capture_id']} ")
        f.write(f"({format_value(sorted_abs_bias[0]['abs_bias'])}).\n")
        f.write(f"- Lowest binary min-entropy: {sorted_min_entropy[0]['capture_id']} ")
        f.write(f"({format_value(sorted_min_entropy[0]['bit_min_entropy'])} bits/bit).\n")
        f.write(f"- Strongest lag-1 magnitude: {sorted_lag[0]['capture_id']} ")
        f.write(f"({format_value(sorted_lag[0]['lag1_phi'])}); adjacent_equal = ")
        f.write(f"{format_value(sorted_lag[0]['adjacent_equal'])}.\n")
        f.write(f"- Largest byte-position mod32 max bias: {sorted_mod32[0]['capture_id']} ")
        f.write(f"({format_value(sorted_mod32[0]['bytepos_mod32_max_abs_bias'])} at slot ")
        f.write(f"{sorted_mod32[0]['bytepos_mod32_max_abs_bias_slot']}).\n\n")
        f.write("## Per-Capture Overview\n\n")
        f.write(table(overview_cols, rows))
        f.write("\n\n## Byte-Internal Bit-Position Bias\n\n")
        f.write(table(bitpos_cols, rows))
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", type=Path, default=[DEFAULT_INPUT_DIR])
    parser.add_argument("--glob", default=DEFAULT_GLOB, help="Glob for directory inputs")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--chunk-size", type=int, default=1024 * 1024)
    args = parser.parse_args()

    files = iter_files(args.inputs, args.glob)
    if not files:
        raise SystemExit(f"No input files found for glob {args.glob!r}.")

    rows = [analyze_file(path, args.chunk_size) for path in files]
    rows.sort(key=lambda r: (str(r["placement"]), str(r["capture_id"])))

    scalar_columns = [
        "file",
        "name",
        "capture_id",
        "placement",
        "run",
        "sample_role",
        "bytes",
        "bits",
        "ones",
        "p1",
        "abs_bias",
        "bit_min_entropy",
        "adjacent_equal",
        "lag1_phi",
        "lag1_n00",
        "lag1_n01",
        "lag1_n10",
        "lag1_n11",
    ]
    bitpos_columns = [item for i in range(8) for item in (f"bitpos{i}_p1", f"bitpos{i}_bias")]
    mod_columns = []
    for mod in (16, 32):
        mod_columns.extend(
            [f"bytepos_mod{mod}_max_abs_bias", f"bytepos_mod{mod}_max_abs_bias_slot", f"bytepos_mod{mod}_span_p1"]
        )
        for slot in range(mod):
            mod_columns.extend([f"bytepos_mod{mod}_{slot:02d}_p1", f"bytepos_mod{mod}_{slot:02d}_bias"])
    run_columns = [
        "longest_zero_run",
        "longest_one_run",
        "runs_total",
        "runs_len1",
        "runs_len2",
        "runs_len3",
        "runs_len4",
        "runs_len5_8",
        "runs_len9_16",
        "runs_len17_32",
        "runs_len_gt32",
        "runs_len1_fraction",
    ]
    columns = scalar_columns + bitpos_columns + mod_columns + run_columns

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "position_structure_summary.csv"
    readme_path = args.out_dir / "README.md"
    write_csv(csv_path, rows, columns)
    write_readme(readme_path, rows)
    print(f"Wrote {csv_path}")
    print(f"Wrote {readme_path}")


if __name__ == "__main__":
    main()
