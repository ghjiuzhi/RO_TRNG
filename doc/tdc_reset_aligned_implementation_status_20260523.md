# TDC Reset-Aligned Implementation Status 20260523

## Goal

Implement the reset-aligned / warmup-aligned TDC line needed to test whether
restart fixed-column bias is caused by startup phase memory or slow phase
diffusion.

This line is designed to support three outcomes:

- positive startup evidence: warmup0 TDC bins are concentrated while warmup12
  bins diffuse
- positive diffusion evidence: bad placement shows longer bin residence or lower
  transition entropy than good placement
- negative-control evidence: TDC startup/diffusion does not separate placements,
  moving the mechanism claim toward sampling registers/routing/output sampling
  path

## Implemented Artifacts

- `rtl/tdc/RO_TDC_reset_aligned_top.v`
- `scripts/build_tdc_reset_aligned_bitstreams.ps1`
- `data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_smoke_20260523.csv`
- `data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_matrix_20260523.csv`

## UART Format

Each capture begins with a 16-byte debug header:

```text
54 44 43 52 01 pair_l pair_h family_l family_h warmup_l warmup_h capture_l capture_h samplediv_l samplediv_h 52
```

`54 44 43 52` is ASCII `TDCR`. After that, the design emits standard 8-byte
TDC packets compatible with the existing parser:

```text
A5 seq_l seq_h coarse_l coarse_h bin_a bin_b flags
```

The existing `analyze_tdc_uart.py` will skip the header and parse the standard
`A5` packets. A startup-specific analysis script should additionally parse and
report the header.

## Build Plan

Build smoke bitstreams first:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_reset_aligned_bitstreams.ps1 -Mode smoke
```

Only if smoke capture works, build the full matrix:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_reset_aligned_bitstreams.ps1 -Mode matrix
```

## Hardware Smoke Plan

Before starting any hardware queue, check for active COM3/JTAG/Vivado jobs:

```powershell
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'powershell|vivado|cmd|hw_server' -and
  ($_.CommandLine -match 'run_fast_hardware_queue|program_and_capture_uart|capture_uart|vivado|read_xadc|program_bitstream|hw_server')
} | Select-Object ProcessId,Name,CommandLine | Format-List
```

Run smoke queue:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_smoke_20260523.csv `
  -Port COM3 `
  -Baud 115200 `
  -StatusMarkdown doc\tdc_reset_aligned_smoke_status_20260523.md `
  -LogDir data\experiments\fast_mode\tdc_reset_aligned_smoke_logs_20260523 `
  -RecordXadc `
  -XadcCsv data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv `
  -ContinueOnError
```

Smoke expected bytes are `528`: 16 header bytes plus 64 TDC packets.

## Matrix Plan

After smoke passes, run the matrix queue:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_matrix_20260523.csv `
  -Port COM3 `
  -Baud 115200 `
  -StatusMarkdown doc\tdc_reset_aligned_matrix_status_20260523.md `
  -LogDir data\experiments\fast_mode\tdc_reset_aligned_matrix_logs_20260523 `
  -RecordXadc `
  -XadcCsv data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv `
  -ContinueOnError
```

Each matrix capture is `524304` bytes: 16 header bytes plus 65536 TDC packets.

## Interpretation Rule

Do not claim calibrated ps-level timing from these raw bins. Until
code-density calibration exists, use:

- raw-bin entropy
- transition entropy
- residence time
- small-lag autocorrelation
- first-window versus later-window contrast

The mechanism claim should stay conditional:

> Reset-aligned TDC either reveals startup phase-memory/diffusion differences, or
> acts as a negative control that pushes the dominant explanation toward
> sampler-register/routing/aperture effects rather than pairwise hard locking.

