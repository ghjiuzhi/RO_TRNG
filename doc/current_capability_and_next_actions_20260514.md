# Current Capability and Next Actions

Date: 2026-05-14

## What is finished

The fast-mode hardware queue has completed all currently available
board-connected experiments:

- RO_FREQ repeat runs:
  - `random1_ro_freq_fixed_run02_2mib`
  - `random3_ro_freq_fixed_run02_2mib`
  - `random1_ro_freq_fixed_run03_2mib`
  - `random3_ro_freq_fixed_run03_2mib`
  - `random3_ro_freq_fixed_run01_5mib`
- TDC baseline repeat:
  - `tdc_near_run03_2mib`
  - `tdc_far_run02_2mib`
- Original fpga1 baseline:
  - `original_fpga1_run01_10mib`
  - `original_fpga1_repeat02_5mib`

The fast-mode status file says `phase: done`:

`doc/fast_mode_hardware_status_20260513.md`

## What the current evidence supports

The current data supports a strong placement-sensitivity result:

- `random1` is a repeatable bad case: p1 near 0.337 and bit min-entropy near
  0.594.
- `random3` is a repeatable good case: p1 near 0.5 and bit min-entropy near
  0.9999.
- `same_column` shows a useful warning case: monobit looks good, but runs and
  adjacent-equality structure are abnormal.
- The original `fpga1` implementation is a strong baseline on this board:
  formal p1 0.500036, bit min-entropy 0.999896; repeat p1 0.500217, bit
  min-entropy 0.999374.

The current mechanism data supports a mechanism-evidence narrative:

- `random1` combines severe TRNG bias with a close all-on pair
  `data4/data5`, delta about 0.466 MHz, and a large positive sample-RO pulling
  shift around 3467 ppm in run01.
- `random3` remains high entropy despite close pairs, so close pair frequency
  alone cannot be claimed as the cause.
- The more defensible hypothesis is a combined placement interaction: close
  frequencies, sample/data relation, and local coupling jointly alter the
  sampling process.

## What is still not enough for top-tier claims

The current TDC near/far baseline is useful, but it is not yet measuring the
actual `random1` and `random3` RO pairs. Therefore, it cannot prove the
coupling/locking mechanism.

For a high-level paper, the next highest-value work is:

1. Build pair-specific TDC bitstreams for selected random1/random3 RO pairs.
2. Capture pair-specific TDC data with the same fast queue pattern.
3. Merge TRNG, RO_FREQ, and pair-specific TDC metrics into one results table.
4. Run NIST SP 800-90B style entropy-source analysis or, at minimum, document
   exactly which required 90B tests remain outside the current local scripts.
5. Expand matched mechanism measurements beyond only random1/random3 if time
   allows, because two cases are not statistical correlation.

## What agents are doing now

- Pair-specific TDC engineering: generate XDC/RTL/TCL preparation for the next
  hardware queue.
- Fast-mode results aggregation: create a single results summary from the new
  queue outputs.
- High-level paper plan: completed in
  `doc/paper_high_level_upgrade_plan_20260514.md`.

## Immediate next command once pair-specific TDC bitstreams exist

Create a second queue CSV with pair-specific TDC bitstreams and reuse:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_pairs_20260514.csv `
  -Port COM3 `
  -Baud 115200 `
  -HwServerUrl localhost:3122 `
  -ContinueOnError
```
