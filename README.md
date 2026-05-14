# RO_TRNG Placement/TDC Paper Analysis Package

This repository is a curated analysis package for the FPGA RO-TRNG placement-sensitivity paper work.

It intentionally includes documents, RTL, scripts, constraints, metadata, and compact analysis outputs, but excludes large or generated hardware artifacts such as Vivado `.runs/.cache`, bitstreams, raw UART `.bin` captures, and generated packet-level TDC CSV dumps.

## Start Here

- `doc/fast_mode_master_status_20260514.md` - current project status and what has/has not been proven.
- `doc/paper_results_after_tdc_pairs_utf8_20260514.md` - clean Chinese result summary after pair-specific TDC.
- `doc/paper_draft_cn_v2_20260514.md` - Chinese paper draft v2.
- `doc/next_hardware_queue_plan_20260514.md` - short and top-journal hardware queue plan.
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md` - concise claim/evidence/caveat table.
- `data/experiments/paper_artifacts_20260514/README.md` - generated paper tables and figures.

## Key Current Findings

- Placement strongly affects raw RO-TRNG quality on the measured Zynq-7020 board.
- `random1` is a repeatable bad case: 10MiB formal `p1 = 0.337315512`, bit min-entropy `0.593605945`.
- `random3` is a repeatable good case: 10MiB formal `p1 = 0.499968565`, bit min-entropy `0.999909299`.
- `same_column` shows why bit balance alone is insufficient: p1 is near 0.5, but runs/adjacent structure is abnormal.
- Six pair-specific TDC captures show no conservative strong-lock windows under the current measurement condition.
- SP800-90B input preparation exists, but the estimator has not yet been run because the local C++ toolchain is blocked.

## Repository Layout

- `doc/` - Chinese planning, status, result, paper-draft, and limitation documents.
- `rtl/` - original and added Verilog RTL, including TDC and RO frequency probe tops.
- `scripts/` - capture, Vivado, analysis, plotting, and SP800-90B input-prep scripts.
- `fpga1/xc7z020clg400/lab_xdc/` - board/lab XDC constraints.
- `data/experiments/` - placement XDCs, queue CSVs, generated tables/figures, and compact dynamics summaries.
- `data/hardware/20260511_fpga1_board1/` - compact CSV/MD/JSON analysis outputs and metadata only.
- `data/sp800_90b/inputs_smoke_20260514/manifest.*` - manifest for smoke-size 90B inputs; binary inputs are excluded.

## Excluded On Purpose

- Raw capture files: `*.bin`
- Bitstreams and checkpoints: `*.bit`, `*.dcp`
- Vivado generated directories: `.Xil`, `.runs`, `.cache`, `.gen`, `.hw`, `.ip_user_files`, `.sim`
- Large TDC packet dumps: `*.tdc_packets.csv`
- Third-party SP800-90B source tree and large PDFs

The raw files remain on the local experiment machine. Their SHA256 hashes and metadata are preserved in JSON/CSV summaries where available.

## Reproducibility Notes

Most analysis scripts are offline-only and should not touch COM, JTAG, Vivado, or hardware unless their names clearly indicate capture/programming.

Useful offline commands:

```powershell
python scripts/analyze_fast_mode_results.py
python scripts/analyze_tdc_pair_dynamics.py
python scripts/make_paper_artifacts_20260514.py
python scripts/prepare_90b_inputs.py --help
```

Hardware scripts such as `scripts/run_fast_hardware_queue.ps1`, `scripts/program_and_capture_uart.ps1`, and `scripts/capture_uart.ps1` require the FPGA board, COM3/UART, and Vivado setup.

