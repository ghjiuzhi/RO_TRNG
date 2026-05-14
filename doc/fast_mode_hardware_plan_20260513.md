# Fast Mode Hardware Plan

Date: 2026-05-13

Goal: finish the board-connected experiments before the evening of 2026-05-14,
while leaving offline analysis, plotting, and writing to parallel agents.

## Current stage

Already complete:

- TRNG placement matrix: 10 layouts have formal captures and repeat captures.
- RO_FREQ fixed probe: random1/random3 smoke and run01 2MiB are complete.
- TDC baseline: near/far smoke or baseline data exists and is analyzable.
- Serial/JTAG path: COM3 and Vivado programming are known working after the
  board UART jumper was restored.

Not complete yet:

- RO_FREQ repeatability: random1/random3 need run02 and run03.
- RO_FREQ 5MiB pair: random1 has a 5MiB run; random3 still needs the paired
  5MiB run.
- TDC repeat baseline: near/far need at least one repeat after the serial fix.
- Original fpga1 implementation baseline: needs a formal 10MiB capture plus a
  5MiB repeat, so the paper has a direct original-project baseline.
- Pair-specific TDC for random1/random3 is desirable, but it depends on a new
  bitstream. It is a stretch target for this fast window, not a blocker for
  finishing the currently available board experiments.

## Fast-mode rule

Only one process may touch COM3, JTAG, hw_server, or Vivado hardware manager at
a time. All hardware captures run through:

`scripts\run_fast_hardware_queue.ps1`

The queue is:

`data\experiments\fast_mode\hardware_queue_20260513.csv`

The live status file is:

`doc\fast_mode_hardware_status_20260513.md`

The runner is resumable. If interrupted, rerun the same command; completed
captures are detected from output size plus metadata and skipped.

## Command

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -Port COM3 `
  -Baud 115200 `
  -HwServerUrl localhost:3122 `
  -ContinueOnError
```

## Priority queue

P0:

- `random1_ro_freq_fixed_run02_2mib`
- `random3_ro_freq_fixed_run02_2mib`
- `random1_ro_freq_fixed_run03_2mib`
- `random3_ro_freq_fixed_run03_2mib`
- `random3_ro_freq_fixed_run01_5mib`

P1:

- `tdc_near_run03_2mib`
- `tdc_far_run02_2mib`
- `original_fpga1_run01_10mib`
- `original_fpga1_repeat02_5mib`

## Parallel agent split

- Main session: hardware queue owner and final decision maker.
- Analysis agent: merge TRNG metrics with RO_FREQ features, prepare paper
  tables and mechanism comparison.
- TDC agent: prepare the pair-specific TDC design plan and implementation
  checklist; no hardware access.
- Writing agent: keep the paper result narrative updated from completed CSVs.
- Test/statistics agent: prepare offline randomness test commands and result
  templates.

## What counts as done by tomorrow evening

Minimum done:

- Every enabled row in the queue has a `.bin`, `.sha256.txt`, and metadata JSON.
- RO_FREQ groups have CSV analyses under `data\experiments\ro_freq_analysis`.
- TDC runs have analysis folders with metrics, bins, packets, and summaries.
- TRNG summary has been refreshed.
- `doc\fast_mode_hardware_status_20260513.md` says `phase: done`.

High-paper stretch:

- Pair-specific TDC bitstreams are built and added to a second queue.
- Pair-specific TDC captures are collected for random1 closest pair, random1
  data0/data1 pair, and random3 closest pair.
- Offline figures and the Chinese paper draft are updated with the new runs.
