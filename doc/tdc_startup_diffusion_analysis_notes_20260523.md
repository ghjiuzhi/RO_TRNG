# TDC Startup Diffusion Analysis Notes 20260523

This note documents the offline script `scripts/analyze_tdc_startup_diffusion.py`.
It only reads existing TDC UART `.bin` captures or packet CSV files produced by
`scripts/analyze_tdc_uart.py`; it does not touch RTL, Vivado projects, hardware
queues, COM ports, JTAG, or `hw_server`.

## Packet Source

Raw `.bin` input is decoded with the existing TDC UART frame convention:

- byte 0: sync byte `0xA5`
- bytes 1-2: little-endian sequence counter
- bytes 3-4: little-endian coarse LSB field
- byte 5: TDC lane A bin
- byte 6: TDC lane B bin
- byte 7: flags

For `.tdc_packets.csv`, the expected fields are `seq`, `coarse_lsb`, `bin_a`,
`bin_b`, and `flags`.

## Metrics

The script reports one summary row per input and one row per fixed-size window.
The core startup-diffusion observables are:

- packet count and sequence gap/wrap checks
- Shannon and min-entropy for lane A, lane B, and signed wrapped differential
  bin `A-B`
- early-window entropy over the first `--early-packets` packets
- transition entropy over consecutive differential-bin pairs
- residence statistics over consecutive runs of the same differential bin,
  including mean, median, p95, and longest run
- small-lag autocorrelation for A, B, and differential bins at `--lag`
- first-window versus later-window entropy deltas, distribution total variation
  distance, and differential-bin mean shift

## Suggested Invocation

```powershell
python scripts\analyze_tdc_startup_diffusion.py `
  --input data\hardware\20260511_fpga1_board1\tdc\tdc_near_run03_2mib.bin `
  --input data\hardware\20260511_fpga1_board1\tdc\tdc_far_run02_2mib.bin `
  --out-dir data\experiments\tdc_startup_diffusion_20260523 `
  --label near `
  --label far `
  --early-packets 1024 `
  --window-packets 16384 `
  --lag 1
```

Outputs:

- `tdc_startup_diffusion.summary.csv`
- `tdc_startup_diffusion.windows.csv`
- `tdc_startup_diffusion.summary.md`

## Interpretation Guidance

Use these metrics as a screening view of reset/warmup startup diffusion. A
strong startup transient is suggested by lower early differential entropy,
larger first-vs-later total variation distance, elevated same-diff residence,
or high small-lag autocorrelation concentrated in the first window. These are
descriptive indicators, not a standalone proof of physical coupling or
restart-state determinism.
