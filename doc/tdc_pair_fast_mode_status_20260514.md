# Pair-Specific TDC Fast-Mode Status

Date: 2026-05-14

## Summary

Pair-specific TDC has moved from a plan to working bitstreams and partial
hardware data.

Completed engineering preparation:

- `rtl/tdc/RO_TDC_pair_sysclk_top.v`
- `scripts/generate_tdc_ro_pair_from_matrix_xdc.py`
- top override in `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`
- pair XDC files in `data/experiments/xdc_tdc_pairs`
- six pair-specific bitstreams in `data/vivado_runs/fpga1_tdc_pairs`

The first pair build initially failed at bitgen because 2-stage RO loops use
`RO_AND`, while the old timing XDC only allowed `RO_NAND` loop nets. This was
fixed by adding `RO_AND` loop allowances to:

`fpga1/xc7z020clg400/lab_xdc/tdc_sysclk_timing.xdc`

After that, all six pair-specific bitstreams built successfully.

## Hardware capture status

Final status: all six planned pair-specific TDC captures are complete.

Completed pair-specific captures:

| pair | role | status | packets | seq gaps | diff_std_ps | phase_r |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| random1 RO4/RO5 | random1 closest RO_FREQ pair | complete | 262143 | 124 | 2041.510 | -0.001195 |
| random1 RO0/RO1 | random1 second close pair | complete | 262142 | 67 | 2042.904 | -0.002491 |
| random1 RO2/RO4 | random1 additional close pair | complete | 262138 | 122 | 2042.290 | -0.002237 |
| random3 RO3/RO7 | random3 closest RO_FREQ pair | complete | 262142 | 120 | 2040.448 | -0.0000368 |
| random3 RO3/RO5 | random3 additional close pair | complete | 262143 | 4 | 2040.263 | -0.0000203 |
| random3 RO0/RO6 | random3 additional close pair | complete | 262143 | 8 | 2041.957 | -0.001465 |

Earlier retry stalls were resolved by restarting `hw_server` on port 3122 and
capturing the two remaining random3 pairs individually.

## Interpretation

The four completed pair-specific TDC captures show similar zero-lag phase
correlation and similar calibrated phase-difference spread:

- random1 completed pairs: `diff_std_ps` about 2041.5 to 2042.9 ps;
  `phase_pearson_r` about -0.0012 to -0.0025.
- random3 completed pair: `diff_std_ps` about 2040.4 ps;
  `phase_pearson_r` about -0.00004.

This does **not** show an obvious zero-lag phase-locking signature in the
completed pair captures. That is useful evidence: the random1 failure is less
likely to be explained by a simple static zero-lag phase correlation alone.

The more defensible mechanism statement is now:

> The severe random1 entropy degradation coincides with close RO frequency pairs
> and abnormal sample-RO pulling in RO_FREQ measurements, while pair-specific
> TDC does not yet reveal strong zero-lag phase locking. This points toward a
> combined or dynamic interaction mechanism rather than a single close-pair
> explanation.

## Next actions

1. Join the completed pair TDC metrics with the RO_FREQ beat/pulling table and
   the TRNG placement table.
2. Keep the paper wording conservative: pair-specific TDC currently constrains
   the mechanism hypothesis but does not prove causality.
3. Use the completed dynamic analysis to state that no strong TDC-level
   pair-locking was detected in these 2 MiB captures.

## Useful files

- Queue: `data/experiments/fast_mode/hardware_queue_tdc_pairs_20260514.csv`
- Remaining retry queue:
  `data/experiments/fast_mode/hardware_queue_tdc_pairs_remaining_20260514.csv`
- Status:
  `doc/fast_mode_tdc_pair_status_20260514.md`
- Remaining status:
  `doc/fast_mode_tdc_pair_remaining_status_20260514.md`
- Completed capture directory:
  `data/hardware/20260511_fpga1_board1/tdc_pairs`

## Heartbeat Check 2026-05-14 09:13 CST

- No `run_fast_hardware_queue.ps1`, `program_and_capture_uart.ps1`,
  `capture_uart.ps1`, or Vivado process is active.
- `hw_server.exe` is still running on `localhost:3122`.
- Main fast-mode hardware queue remains complete.
- Pair-specific TDC remains 4/6 complete.
- Remaining retries still have no metadata/bin output:
  - `tdc_pair_random3_ro3_ro5_run01_2mib`
  - `tdc_pair_random3_ro0_ro6_run01_2mib`
- The latest retry log again stops during Vivado startup/programming, after
  `Sourcing tcl script ... Vivado_init.tcl`; the earlier original log showed
  very slow `enable_beta_device` and `connect_hw_server`.

Do not launch another retry blindly. Restart or refresh the Vivado/hw_server
environment first, then retry only the remaining queue.

## Heartbeat Check 2026-05-14 09:44 CST

- No new TDC pair metadata or bin files appeared since the previous check.
- Completed pair-specific TDC remains 4/6.
- The only persistent hardware-related process seen is `hw_server.exe`; no
  active Vivado/program/capture queue is making progress.
- Remaining retry log still stops at Vivado startup after sourcing
  `Vivado_init.tcl`.

No automatic retry was started. The next useful action is still to restart or
refresh Vivado/hw_server, then run only
`data/experiments/fast_mode/hardware_queue_tdc_pairs_remaining_20260514.csv`.

## Heartbeat Check 2026-05-14 10:14 CST

- Status remains unchanged.
- Only `hw_server.exe` is visible as a persistent hardware-related process.
- No new complete metadata/bin files for the two remaining random3 TDC pairs
  were detected.
- The remaining retry log is still stopped at Vivado startup after sourcing
  `Vivado_init.tcl`.

No retry was launched, because the last two attempts point to a Vivado/hw_server
startup stall rather than a data-capture failure.

## Heartbeat Check 2026-05-14 10:45 CST

- Status remains unchanged.
- No active hardware queue, capture script, or Vivado process is making
  progress; only `hw_server.exe` remains visible.
- Pair-specific TDC is still 4/6 complete.
- The retry log for `random3_ro3_ro5` still stops immediately after
  `Vivado_init.tcl`.

No automatic retry was launched. The remaining two pair captures should wait
until the Vivado/hw_server path has been refreshed.

## Heartbeat Check 2026-05-14 11:15 CST

- Status remains unchanged.
- Pair-specific TDC is still 4/6 complete.
- No active queue/program/capture/Vivado process is running; only
  `hw_server.exe` remains visible.
- No new metadata or 2MiB bin files appeared for the two remaining random3
  pairs.
- Remaining retry log still stops after `Vivado_init.tcl`.

No automatic retry was launched.

## Completion Update 2026-05-14 11:50 CST

- `tdc_pair_random3_ro3_ro5_run01_2mib` completed after restarting
  `hw_server`.
- `tdc_pair_random3_ro0_ro6_run01_2mib` completed immediately afterward.
- Pair-specific TDC is now 6/6 complete.
- Dynamic analysis was refreshed:
  - runs: 6
  - windows: 96
  - strong-lock windows: 0
  - maximum absolute zero-lag window phase correlation: about 0.017
  - maximum absolute small-lag window phase correlation: about 0.032

The hardware fast-mode objective for the currently planned experiment set is
complete.

## SP800-90B Preparation Update 2026-05-14

- Generated a smoke-size SP800-90B input set under
  `data/sp800_90b/inputs_smoke_20260514`.
- Inputs cover 11 complete formal TRNG datasets.
- Each dataset was converted into:
  - `bit-symbols-msb`: one byte per bit, `bits_per_symbol=1`
  - `byte-symbols`: raw byte symbols, `bits_per_symbol=8`
- `manifest.csv` and `manifest.json` record source SHA-256, output SHA-256,
  offsets, read length, and symbol format.
- No SP800-90B estimator was run yet; local compiler/binary availability still
  needs to be checked before claiming 90B results.
