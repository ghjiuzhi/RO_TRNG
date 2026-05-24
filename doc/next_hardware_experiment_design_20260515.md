# Next Hardware Experiment Design - 2026-05-15

## Scope

Hardware is currently unavailable, so this document only prepares the next board-connected runs. Do not start COM3, JTAG, Vivado programming, or capture jobs until the board is connected and explicitly available.

Goal: complete the minimum submission gaps first, then the high-impact extensions:

1. P0 minimum submission: `random1` restart warmup contrast and automatic XADC temperature/voltage recording.
2. P1 high-impact: `random3` warmup repeat03, placement 20 MiB repeat matrix, and TDC code-density calibration planning.
3. P2 stronger paper: multi-board replication and additional placement restart contrasts.

Board-connected command sequence:

- `doc/board_connected_runbook_20260515.md`

Before the next board session, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_next_hardware_readiness.ps1
```

Current readiness result on 2026-05-15: `Failed checks: 0`.

## Automatic XADC Recording

Yes, XADC can be recorded automatically. The repo already had `scripts/read_xadc.ps1` and `scripts/vivado/read_xadc.tcl`; the capture scripts now support automated before/after snapshots.

Supported scripts now include:

- `scripts/capture_uart.ps1 -RecordXadc`
- `scripts/program_and_capture_uart.ps1 -RecordXadc`
- `scripts/run_fast_hardware_queue.ps1 -RecordXadc`
- `scripts/capture_90b_restart_dataset.ps1 -RecordXadc`
- `scripts/run_restart_warmup_repeat_queue.ps1 -RecordXadc`

Metadata now records:

- `board_id`
- `xadc_csv`
- `xadc_before`
- `xadc_after`
- FPGA die temperature from XADC
- XADC rails: `VCCINT`, `VCCAUX`, `VCCBRAM`, `VPVN` when available

Important boundary: XADC gives on-chip die temperature and board/FPGA supply telemetry. It does not measure external room temperature directly. If no external thermometer is used, paper wording should say "on-chip XADC temperature/voltage was logged before and after each capture," not "ambient temperature was controlled."

After capture, summarize all metadata XADC readings with:

```powershell
python scripts\summarize_xadc_metadata.py --tag 20260515
```

Outputs:

- `data/experiments/xadc_summary/xadc_capture_summary_20260515.csv`
- `data/experiments/xadc_summary/xadc_capture_summary_20260515.md`

The summary keeps legacy metadata rows even when they do not contain XADC fields, so missing temperature/voltage coverage is visible instead of silently dropped.

## Board ID Convention

Use stable physical board IDs:

- current board: `z7020_b01`
- second board: `z7020_b02`
- third board: `z7020_b03`

Do not use COM port or date as board identity. New metadata will carry `board_id`.

## P0: Minimum Submission Runs

### 1. random1 warmup contrast

Purpose: test whether `random1` also has warmup-sensitive fixed-position bias, or whether `ea_restart` pass/fail is mostly hidden by low `H_I` and a wider cutoff.

Bitstreams already built:

| warmup | bitstream |
| ---: | --- |
| 8 | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup8_header_delay60s/RO_TRNG_restart_auto_top.bit` |
| 11 | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup11_header_delay60s/RO_TRNG_restart_auto_top.bit` |
| 12 | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup12_header_delay60s/RO_TRNG_restart_auto_top.bit` |

Command when hardware is available:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_restart_warmup_repeat_queue.ps1 `
  -Placement random1 `
  -RepeatTag contrast01 `
  -WarmupsCsv 8,11,12 `
  -Port COM3 `
  -Baud 115200 `
  -InitialEntropyMsb 0.389520 `
  -InitialEntropyLsb 0.383737 `
  -ColumnXCutoff 821 `
  -RecordXadc `
  -BoardId z7020_b01
```

Expected output family:

- `data/hardware/20260511_fpga1_board1/restart/random1_restart_auto_formal_bits_1000x125_warmup*_header_delay60s_contrast01_20260515.bin`
- MSB/LSB expanded bps1 files
- `ea_restart_random1_warmup*_contrast01_*`
- XADC rows in metadata xadc CSV

### 2. random3 warmup repeat03

Purpose: strengthen the boundary from two observations to three observations.

Command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_restart_warmup_repeat_queue.ps1 `
  -Placement random3 `
  -RepeatTag repeat03 `
  -WarmupsCsv 10,11,12 `
  -Port COM3 `
  -Baud 115200 `
  -InitialEntropyMsb 0.902345 `
  -InitialEntropyLsb 0.828444 `
  -ColumnXCutoff 605 `
  -RecordXadc `
  -BoardId z7020_b01
```

## P1: Placement 20 MiB Repeat Matrix

Queue file prepared:

- `data/experiments/fast_mode/hardware_queue_placement_repeat_20260515.csv`

Enabled rows with existing bitstreams:

- `same_column_repeat03_20mib`
- `sparse_repeat03_20mib`
- `far_repeat03_20mib`
- `compact_repeat03_20mib`
- `checker_repeat03_20mib`
- `random2_repeat03_20mib`
- `row_repeat03_20mib`
- `cross_region_repeat03_20mib`

Disabled optional rows:

- optional `random1_repeat04_10mib`
- optional `random3_repeat04_10mib`

Command when hardware is available:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_placement_repeat_20260515.csv `
  -Port COM3 `
  -Baud 115200 `
  -HwServerUrl localhost:3122 `
  -RecordXadc `
  -BoardId z7020_b01 `
  -StatusMarkdown doc\fast_mode_placement_repeat_status_20260515.md `
  -LogDir data\experiments\fast_mode\placement_repeat_logs_20260515 `
  -ContinueOnError
```

Estimated time: about 7.3 hours for the enabled 20 MiB placement rows.

## P1/P2: More Placement Restart Contrasts

Recommended extra restart placements after random1/random3 are stable:

| placement | no-warmup | warmup12 | purpose |
| --- | --- | --- | --- |
| `same_column` | yes | yes | p1-good but structure-bad placement |
| `sparse` | yes | yes | structured low-entropy placement |
| `compact` | yes | yes | structured good control |
| `checker` | yes | yes | structured good control |

These require building restart auto-stream bitstreams from each placement XDC using `scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl` with `restart_count=1000`, `row_bytes=125`, `debug_header=1`, `start_delay_cycles=12000000000`, and selected `warmup_bytes`.

Build helper prepared:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_restart_placement_contrasts_20260515.ps1
```

Build status on 2026-05-15: completed, 8/8 restart placement bitstreams ready. Status table:

- `doc/restart_placement_bitstream_status_20260515.md`
- `data/experiments/fast_mode/restart_placement_bitstream_status_20260515.csv`

Capture/analysis queue prepared:

- `data/experiments/fast_mode/restart_placement_queue_20260515.csv`
- `scripts/run_restart_placement_queue.ps1`

When hardware is available, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_restart_placement_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\restart_placement_queue_20260515.csv `
  -Port COM3 `
  -Baud 115200 `
  -HwServerUrl localhost:3122 `
  -RecordXadc `
  -BoardId z7020_b01 `
  -ContinueOnError
```

This queue captures `1000 x 125` packed bytes for each row, expands to `1000 x 1000` bit-symbol restart inputs, runs MSB/LSB `ea_restart`, performs packed byte/bit column-bias analysis, and records XADC before/after each capture. Initial entropy values are taken from the 2026-05-14 non-IID continuous-stream smoke runs for the corresponding placement and bit order.

After any restart queue run, refresh the paper-facing restart table:

```powershell
python scripts\summarize_restart_results.py --tag 20260515
```

Outputs:

- `data/experiments/restart_summary_20260515/restart_result_summary_20260515.csv`
- `data/experiments/restart_summary_20260515/restart_result_summary_20260515.md`

Target bitstreams:

- `same_column`: warmup0, warmup12
- `sparse`: warmup0, warmup12
- `compact`: warmup0, warmup12
- `checker`: warmup0, warmup12

## TDC Code-Density Calibration

Current TDC data supports "code-density-normalized TDC observations," not a fully independent calibrated TDC.

For a stronger paper, build a dedicated calibration top/mode:

- reuse same TDC lane and UART packet format;
- drive lane inputs from independent asynchronous calibration ROs or a phase-walk source;
- capture 8-16 MiB per lane/mode;
- repeat at least once;
- derive `width_ps[k] = count[k] / total * 5000 ps` and phase-center lookup.

Until that is built, paper wording should not claim full calibrated ps-level TDC. Use "relative/code-density-normalized TDC metrics."

## Multi-Board Plan

If you can borrow more boards, start with same-bitstream validation:

Per extra board P0:

1. continuous TRNG 10 MiB: `random1`, `random3`, original baseline if compatible;
2. RO_FREQ fixed probe: `random1`, `random3`;
3. restart warmup boundary: `random3` warmup10/11/12;
4. XADC before/after for every run;
5. metadata `board_id=z7020_b02` or `z7020_b03`.

Do not pool different boards blindly. Report `(board_id, placement, bitstream_sha256, run_id)` as factors.

## First Action When Board Is Available

1. Confirm no hardware process is already running.
2. Run a standalone XADC smoke:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
  -OutCsv data\hardware\20260511_fpga1_board1\metadata\xadc_smoke_20260515.csv `
  -HwServerUrl localhost:3122
```

3. Run `random1` warmup contrast with `-RecordXadc`.
4. Run `random3` repeat03 with `-RecordXadc`.
5. Run placement restart queue with `-RecordXadc`.
6. Run placement repeat queue with `-RecordXadc`.
7. Refresh XADC and restart summaries:

```powershell
python scripts\summarize_xadc_metadata.py --tag 20260515
python scripts\summarize_restart_results.py --tag 20260515
```
