# Board-Connected Runbook - 2026-05-15

This runbook is the next hardware session order. It assumes the board is connected, UART is on `COM3`, and JTAG is visible to Vivado.

## 0. Offline Readiness Check

Run this before touching the board:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_next_hardware_readiness.ps1
```

Expected:

- `Failed checks: 0`
- `doc/next_hardware_readiness_20260515.md` updated

## 1. XADC Smoke

Purpose: prove Vivado hardware access can read on-chip temperature/voltage before long captures.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
  -OutCsv data\hardware\20260511_fpga1_board1\metadata\xadc_smoke_20260515.csv `
  -HwServerUrl localhost:3122
```

If this fails, fix JTAG/hw_server first.

## 2. random1 Warmup Contrast

Purpose: test whether `random1` has the same restart warmup sensitivity as `random3`.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_restart_warmup_repeat_queue.ps1 `
  -Placement random1 `
  -RepeatTag contrast01 `
  -WarmupsCsv 8,11,12 `
  -Port COM3 `
  -Baud 115200 `
  -InitialEntropyMsb 0.385385 `
  -InitialEntropyLsb 0.383737 `
  -ColumnXCutoff 821 `
  -RecordXadc `
  -BoardId z7020_b01
```

## 3. random3 Repeat03

Purpose: add a third observation for the warmup boundary.

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

## 4. Placement Restart Queue

Purpose: compare restart warmup behavior across `same_column`, `sparse`, `compact`, and `checker`.

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

## 5. Placement 20 MiB Repeat Queue

Purpose: strengthen continuous-stream placement statistics.

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

## 6. Refresh Tables

Run after each major queue, and definitely at the end:

```powershell
python scripts\summarize_xadc_metadata.py --tag 20260515
python scripts\summarize_restart_results.py --tag 20260515
python scripts\summarize_trng_repeats.py
python scripts\analyze_fast_mode_results.py
```

Primary outputs:

- `data/experiments/xadc_summary/xadc_capture_summary_20260515.md`
- `data/experiments/restart_summary_20260515/restart_result_summary_20260515.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`

## Priority Rule

If time is limited, do steps 1, 2, 3, and 4 first. Placement 20 MiB repeats are important for statistics, but restart warmup and placement contrast are more directly tied to the paper's core mechanism claim.
