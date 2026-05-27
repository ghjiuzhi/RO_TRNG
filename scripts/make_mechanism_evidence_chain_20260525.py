#!/usr/bin/env python3
"""Build a paper-facing mechanism evidence chain table for 2026-05-25.

Offline only: this script reads existing analysis artifacts and does not touch
hardware, Vivado, UART, JTAG, or capture flows.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TDC = (
    ROOT
    / "data/experiments/tdc_reset_aligned_clean32k_all_20260525/"
    / "tdc_reset_aligned_clean32k_all_20260525.summary.csv"
)
DEFAULT_SAMPLE_RO_DIR = ROOT / "data/experiments/restart_fifo_diag_20260525"
DEFAULT_REDUCED_XOR_MAP = (
    ROOT
    / "data/experiments/restart_reduced_xor_w10_direction_map_20260526/"
    / "summary/w10_direction_map_combined.csv"
)
DEFAULT_REDUCED_XOR_REPEAT = (
    ROOT
    / "data/experiments/restart_reduced_xor_w10_direction_repeat02_minimal_20260526/"
    / "summary/w10_direction_repeat_compare_wide.csv"
)
DEFAULT_OUT_DIR = ROOT / "data/experiments/mechanism_evidence_chain_20260525"

COLUMNS = [
    "evidence_id",
    "layer",
    "experiment",
    "comparison",
    "evidence_strength",
    "claim_supported",
    "key_metric_1",
    "key_metric_2",
    "key_metric_3",
    "xadc_status",
    "xadc_after_temperature_c",
    "xadc_after_vccint_v",
    "source_file",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def parse_xadc_log(path: Path) -> dict[str, str]:
    out = {
        "xadc_status": "missing",
        "xadc_after_temperature_c": "",
        "xadc_after_vccint_v": "",
    }
    if not path.exists():
        return out
    # Tee-Object logs from Windows PowerShell may be UTF-16LE-like text with
    # interleaved NUL bytes. Removing NULs keeps the numeric CSV line parseable.
    text = path.read_bytes().replace(b"\x00", b"").decode("utf-8", errors="ignore")
    lines = text.splitlines()
    for line in lines:
        if re.match(r"^\d{4}-\d{2}-\d{2} ", line):
            parts = [part.strip() for part in line.split(",")]
            if len(parts) >= 5:
                out.update(
                    {
                        "xadc_status": "after_only_ok",
                        "xadc_after_temperature_c": parts[1],
                        "xadc_after_vccint_v": parts[2],
                    }
                )
    return out


def tdc_xadc_log(label: str) -> Path:
    run = {
        "random1_baseline_warmup0": "tdc_reset_random1_baseline_ro0_clean32k_warmup0_preopen_20260525",
        "random1_baseline_warmup12": "tdc_reset_random1_baseline_ro0_clean32k_warmup12_preopen_20260525",
        "random3_goodref_warmup0": "tdc_reset_random3_goodref_ro0_clean32k_warmup0_preopen_20260525",
        "random3_goodref_warmup12": "tdc_reset_random3_goodref_ro0_clean32k_warmup12_preopen_20260525",
        "random1_sampler_local_warmup0": "tdc_reset_random1_sampler_local_ro0_clean32k_warmup0_preopen_20260525",
        "random1_sampler_local_warmup12": "tdc_reset_random1_sampler_local_ro0_clean32k_warmup12_preopen_20260525",
    }[label]
    root = (
        ROOT / "data/experiments/tdc_reset_aligned_clean32k_20260525/logs"
        if "warmup0" in label and label == "random1_baseline_warmup0"
        else ROOT / "data/experiments/tdc_reset_aligned_clean32k_remaining_20260525/logs"
    )
    return root / f"{run}.xadc_after.log"


def build_tdc_rows(tdc_csv: Path) -> list[dict[str, str]]:
    rows = [row for row in read_csv(tdc_csv) if row.get("warmup_start") == "0"]
    out: list[dict[str, str]] = []
    for row in rows:
        label = row["label"]
        xadc = parse_xadc_log(tdc_xadc_log(label))
        same = to_float(row.get("same_diff_transition_ratio"))
        autocorr = to_float(row.get("autocorr_diff_lag"))
        transition = to_float(row.get("transition_entropy_diff"))
        strength = "negative/control evidence"
        claim = "Rules out simple pairwise RO hard locking as the dominant explanation"
        if label == "random1_sampler_local_warmup12":
            strength = "weak positive evidence"
            claim = (
                "Sampler-local warmup12 has the highest clean reset-aligned "
                "differential/transition entropy in this six-point matrix"
            )
        out.append(
            {
                "evidence_id": f"tdc_clean32k_{label}",
                "layer": "reset-aligned TDC",
                "experiment": label,
                "comparison": "random1 baseline / random3 good reference / random1 sampler-local, warmup0 vs warmup12",
                "evidence_strength": strength,
                "claim_supported": claim,
                "key_metric_1": f"Hdiff={fmt(to_float(row.get('entropy_diff')))} early={fmt(to_float(row.get('early_entropy_diff')))}",
                "key_metric_2": f"transition_Hdiff={fmt(transition)} same_ratio={fmt(same)}",
                "key_metric_3": f"longest_run={row.get('longest_same_diff_bin_run')} autocorr={fmt(autocorr)}",
                **xadc,
                "source_file": rel(tdc_csv),
                "notes": (
                    "TDCR header present; raw-bin relative comparison only, "
                    "not calibrated ps-level jitter."
                ),
            }
        )
    return out


def one_row_from_summary(path: Path) -> dict[str, str] | None:
    rows = read_csv(path)
    return rows[0] if rows else None


def build_sample_ro_rows(sample_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    fail_paths = sorted(sample_dir.glob("restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup*_20260525*.summary.csv"))
    for path in fail_paths:
        row = one_row_from_summary(path)
        if not row:
            continue
        warmup = row.get("warmup_bytes", "")
        rows.append(
            {
                "evidence_id": f"sample_ro_forward_fail_w{warmup}_{path.stem}",
                "layer": "sample RO counterfactual",
                "experiment": row.get("label", path.stem),
                "comparison": "compact diagnostic top + formal-routed sample RO",
                "evidence_strength": "strong causal evidence",
                "claim_supported": "Moving only the sample RO physical implementation can pull an otherwise near-ideal restart passband into a biased failing regime",
                "key_metric_1": f"overall_p1={row.get('overall_p1')} abs_bias={row.get('overall_abs_bias')}",
                "key_metric_2": f"worst_byte={row.get('worst_byte_index')} bit={row.get('worst_bit_index')} x={row.get('worst_x')}",
                "key_metric_3": f"worst_p1={row.get('worst_p1')} row_std={row.get('row_ones_std')}",
                "xadc_status": "see metadata/log",
                "source_file": rel(path),
                "notes": "Forward counterfactual: compact topology becomes biased when sample RO is locked to formal routed locations.",
            }
        )

    repair_paths = sorted(sample_dir.glob("restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run*_20260525_summary.csv"))
    for path in repair_paths:
        row = one_row_from_summary(path)
        if not row:
            continue
        rows.append(
            {
                "evidence_id": f"sample_ro_reverse_repair_{path.stem}",
                "layer": "sample RO counterfactual",
                "experiment": row.get("label", path.stem),
                "comparison": "formal auto top + compact-routed sample RO",
                "evidence_strength": "strong causal evidence",
                "claim_supported": "Moving the sample RO back to the compact-routed implementation repairs the formal warmup4 restart failure",
                "key_metric_1": f"overall_p1={row.get('overall_p1')} minH={row.get('overall_min_entropy')}",
                "key_metric_2": f"worst_byte={row.get('worst_byte_index')} bit={row.get('worst_bit_index')} x={row.get('worst_x')}",
                "key_metric_3": f"worst_p1={row.get('worst_p1')} row_std={row.get('row_ones_std')}",
                "xadc_status": "see metadata/log",
                "source_file": rel(path),
                "notes": "Reverse counterfactual closes the causal loop; sample RO neighborhood is part of the entropy-source boundary.",
            }
        )
    return rows


def row_by_label(rows: list[dict[str, str]], mode: str, data_ro: str) -> dict[str, str] | None:
    for row in rows:
        if row.get("mode") == mode and row.get("data_ro") == data_ro:
            return row
    return None


def repeat_metric(rows: list[dict[str, str]], mode: str, data_ro: str) -> str:
    row = row_by_label(rows, mode, data_ro)
    if not row:
        return ""
    return f"{row.get('p1_run01')}->{row.get('p1_run02')} delta={row.get('delta_p1')}"


def build_reduced_xor_rows(map_csv: Path, repeat_csv: Path) -> list[dict[str, str]]:
    direction = read_csv(map_csv)
    repeat = read_csv(repeat_csv)
    if not direction:
        return []

    all64 = row_by_label(direction, "all64", "all")
    data0 = row_by_label(direction, "data_ro", "0")
    data2 = row_by_label(direction, "data_ro", "2")
    data3 = row_by_label(direction, "data_ro", "3")
    except0 = row_by_label(direction, "except_data_ro", "0")
    except2 = row_by_label(direction, "except_data_ro", "2")
    except6 = row_by_label(direction, "except_data_ro", "6")

    rows: list[dict[str, str]] = []
    if all64 and data0 and data2 and data3:
        rows.append(
            {
                "evidence_id": "reduced_xor_w10_direction_map_data_ro_bias",
                "layer": "reduced-XOR hardware counterfactual",
                "experiment": "sampler_island_local warmup10, data_ro[0..7] direction map",
                "comparison": "same top all64 vs same-data-RO direction functions",
                "evidence_strength": "strong mechanism evidence",
                "claim_supported": "Same-data-RO directions are real biased hardware functions, not only offline snapshot artifacts",
                "key_metric_1": f"all64_p1={all64.get('p1')} abs_bias={all64.get('abs_bias')}",
                "key_metric_2": f"data_ro0_p1={data0.get('p1')} data_ro2_p1={data2.get('p1')} data_ro3_p1={data3.get('p1')}",
                "key_metric_3": f"repeat data_ro0 {repeat_metric(repeat, 'data_ro', '0')}; data_ro2 {repeat_metric(repeat, 'data_ro', '2')}; data_ro3 {repeat_metric(repeat, 'data_ro', '3')}",
                "xadc_status": "see reduced-XOR metadata/logs",
                "source_file": rel(map_csv),
                "notes": "All captures used restart auto-stream with valid A55A03E8007D01D0 header and 1000x125-byte payload.",
            }
        )

    if all64 and except0 and except2 and except6:
        rows.append(
            {
                "evidence_id": "reduced_xor_w10_complement_cancellation",
                "layer": "reduced-XOR hardware counterfactual",
                "experiment": "sampler_island_local warmup10, except_data_ro complement map",
                "comparison": "all64 vs all64 XOR data_ro[j]",
                "evidence_strength": "strong mechanism evidence",
                "claim_supported": "Final all64 quality is governed by sampler-vector XOR cancellation rather than one bad data_ro group",
                "key_metric_1": f"except_ro0_p1={except0.get('p1')} abs_bias={except0.get('abs_bias')}",
                "key_metric_2": f"except_ro2_p1={except2.get('p1')} abs_bias={except2.get('abs_bias')}; except_ro6_p1={except6.get('p1')} abs_bias={except6.get('abs_bias')}",
                "key_metric_3": f"repeat except_ro0 {repeat_metric(repeat, 'except_data_ro', '0')}; except_ro2 {repeat_metric(repeat, 'except_data_ro', '2')}; except_ro6 {repeat_metric(repeat, 'except_data_ro', '6')}",
                "xadc_status": "see reduced-XOR metadata/logs",
                "source_file": rel(repeat_csv),
                "notes": "Near-ideal complements coexist with strongly biased same-data-RO functions, supporting a sampler-side XOR-combination boundary.",
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, str]], csv_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Mechanism Evidence Chain 20260525/20260527\n\n")
        f.write(f"- CSV: `{rel(csv_path)}`\n")
        f.write(f"- Rows: `{len(rows)}`\n\n")
        f.write("## Main Claim\n\n")
        f.write(
            "The sampler-side physical implementation is part of the RO-TRNG "
            "entropy-source boundary. Clean reset-aligned TDC now constrains the "
            "mechanism by ruling out simple pairwise hard locking. Sample-RO "
            "counterfactual placement provides causal evidence, and reduced-XOR "
            "counterfactuals show that final output quality depends on sampler-vector "
            "XOR cancellation among biased same-data-RO directions.\n\n"
        )
        f.write("## Evidence Table\n\n")
        keep = [
            "evidence_id",
            "layer",
            "evidence_strength",
            "claim_supported",
            "key_metric_1",
            "key_metric_2",
            "key_metric_3",
            "xadc_status",
            "source_file",
        ]
        f.write("| " + " | ".join(keep) + " |\n")
        f.write("| " + " | ".join(["---"] * len(keep)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(row.get(col, "").replace("|", "/") for col in keep) + " |\n")
        f.write("\n## Interpretation\n\n")
        f.write(
            "- Strong evidence: the bidirectional sample-RO counterfactual loop flips "
            "restart outcomes while changing only sampler-side physical realization.\n"
        )
        f.write(
            "- Constraint evidence: all clean32k TDC files have a valid `TDCR` header, "
            "32768 packets, same-bin residence around 1%, longest run 3, and near-zero "
            "lag-1 autocorrelation; this argues against a simple hard-locking story.\n"
        )
        f.write(
            "- Weak positive TDC evidence: sampler-local warmup12 has the highest "
            "H(diff) and transition H(diff) in this six-point clean matrix, consistent "
            "with but not sufficient to prove improved startup phase diffusion.\n"
        )
        f.write(
            "- Reduced-XOR mechanism evidence: same-data-RO directions can be severely "
            "biased on hardware, while selected complements are near ideal and repeat "
            "stably; this supports a sampler-vector XOR cancellation boundary.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tdc-csv", type=Path, default=DEFAULT_TDC)
    parser.add_argument("--sample-ro-dir", type=Path, default=DEFAULT_SAMPLE_RO_DIR)
    parser.add_argument("--reduced-xor-map", type=Path, default=DEFAULT_REDUCED_XOR_MAP)
    parser.add_argument("--reduced-xor-repeat", type=Path, default=DEFAULT_REDUCED_XOR_REPEAT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    rows = (
        build_sample_ro_rows(args.sample_ro_dir)
        + build_reduced_xor_rows(args.reduced_xor_map, args.reduced_xor_repeat)
        + build_tdc_rows(args.tdc_csv)
    )
    out_csv = args.out_dir / "mechanism_evidence_chain_20260525.csv"
    out_md = args.out_dir / "mechanism_evidence_chain_20260525.md"
    write_csv(out_csv, rows)
    write_markdown(out_md, rows, out_csv)
    print(f"Wrote {out_csv}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
