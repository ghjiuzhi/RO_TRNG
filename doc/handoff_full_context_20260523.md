# RO_TRNG Project Handoff - Full Context 20260523

This file is the canonical handoff for a new conversation/model taking over
the RO_TRNG paper, hardware, TDC, SP800-90B restart, and mechanism-validation
work.

## How to Use This Handoff

At the start of a new conversation, tell the new model:

1. Work in `E:\Project\MLDSA\RO_TRNG`.
2. Read this file first.
3. Then read `doc/new_conversation_bootstrap_prompt_20260523.md`.
4. Then inspect only the specific docs/scripts listed here before acting.

The new model should not assume it has hidden chat memory. This document is the
memory bridge.

## User Goal

The user is preparing a high-level paper on FPGA RO-TRNG placement sensitivity.
The goal is not just to collect random data, but to build a defensible mechanism
story:

> RO-TRNG randomness depends on the physical implementation of the sampler side.
> Placement changes the sample RO, sampling registers, local routing, and
> sampling aperture. The entropy source boundary therefore includes the sampler
> path, not only the ring oscillators that generate data.

The user wants proactive, fast, accurate work. Prefer doing useful offline work
when hardware is unavailable, and carefully sequenced hardware queues when the
board is connected.

## Environment

- Workspace: `E:\Project\MLDSA\RO_TRNG`
- Shell: PowerShell
- Vivado: `C:\Programs\Xilinx2023\Vivado\2023.2`
- Board: 正点原子领航者 V2, Zynq-7020 / `xc7z020clg400`
- UART: `COM3`, `115200`, 8N1, no flow control
- Board label used in data paths: `20260511_fpga1_board1` / `z7020_b01`
- Hardware rule: never run two COM3/JTAG/Vivado programming/capture jobs in
  parallel.
- GitHub push: do not push unless the user explicitly asks.

## Current Process State at Handoff

Last checked on 2026-05-23:

- No COM3/JTAG capture queue is running.
- `hw_server` is resident on `localhost:3122`.
- No new hardware task should be launched without first checking the process
  list.

Process check command:

```powershell
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'powershell|vivado|cmd|hw_server' -and
  ($_.CommandLine -match 'run_fast_hardware_queue|program_and_capture_uart|capture_uart|vivado|read_xadc|program_bitstream|hw_server')
} | Select-Object ProcessId,Name,CommandLine | Format-List
```

## Scientific State

### Main Story

The current best paper story is:

1. Placement strongly changes raw TRNG behavior.
2. Sampler-side placement can repair a bad source while holding the data-RO
   placement fixed.
3. TDC does not show strong pairwise sampler-data or data-data hard locking in
   the measured cases.
4. Therefore the mechanism should not be oversimplified as "near ROs lock and
   become bad."
5. The stronger and more defensible mechanism is:

   > The sampler path is part of the physical entropy source boundary. Placement
   > affects entropy through sample RO placement, sampling registers, local
   > routing, and sampling aperture/metastability behavior. TDC is used to bound
   > and falsify simpler locking explanations, and future reset-aligned TDC can
   > test startup phase memory.

### What TDC Has and Has Not Shown

TDC has shown:

- Existing pairwise TDC correlations are near zero.
- This weakens the strong-locking hypothesis.
- TDC is currently a negative-control / mechanism-bounding instrument.

TDC has not yet shown:

- Calibrated ps-level jitter.
- A positive direct explanation for the sampler-island repair.
- Reset-aligned or warmup-aligned startup transient behavior.

Do not claim absolute timing from raw TDC bins unless code-density calibration is
implemented.

## Most Important Completed Results

### Sampler-Island 20MiB Confirmation

File:

- `data/hardware/20260511_fpga1_board1/trng/random1_sampler_island_local_x45y39_regs_x45y31_program_20mib_20260523.bin`

Results:

- SHA256: `C42E39A9BC46909105678F20EE918D054C82564FA344FA2F8E1A761D0E0D95E4`
- Size: 20 MiB
- `p1 = 0.5000507474`
- bit min-entropy: `0.9998535814`
- runs p-value: `0.6489840131`
- adjacent-equal ratio: `0.4999824375`
- byte min-entropy: `7.9855784492`
- XADC: `46.0 C -> 46.3 C`, VCCINT about `1.000 V`

Interpretation:

This is the strongest causal mechanism evidence in the project. Holding the
`random1` data-RO placement fixed, sampler-side placement repairs the stream
from strongly biased to near ideal.

Reference comparison:

- `random1 baseline`: `p1 ~= 0.337669`, bit min-entropy `~= 0.594377`
- `random1 sample_ro_local_x45y39_20mib`: `p1 ~= 0.484799`, bit min-entropy
  `~= 0.956792`
- `random1_sampler_island_local_x45y39_regs_x45y31_program_20mib`: near ideal

Read:

- `doc/random1_sampler_island_ablation_20260523.md`
- `doc/fast_mode_status_20260523.md`
- `data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv`

### Sampler-Data TDC Six-Run Queue

Summary files:

- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.md`
- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.csv`

Script:

- `scripts/summarize_tdc_sampler_data.py`

Runs:

- `random1` baseline sample `X36Y35` vs data RO0/RO4
- `random1` local sample `X45Y39` vs data RO0/RO4
- `random3` good reference sample `X36Y35` vs data RO0/RO3

Key result:

- All `phase_r` values are near zero: about `-0.00247` to `0.00224`.
- Nominal `diff_std_ps` is similar across cases, but it is raw-bin derived and
  uncalibrated.

Interpretation:

This does not support a simple hard-locking explanation. The TRNG entropy shift
is large, but raw sampler-data TDC phase correlation does not split in the same
way. Use this as negative-control evidence.

Read:

- `doc/tdc_sampler_mechanism_experiment_plan_20260523.md`
- `doc/tdc_sampler_data_capture_status_20260523.md`
- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.md`

### Restart Sampler-Island Diagnostic Attempt

Built four restart bitstreams:

- `sample_ro_local`, warmup0
- `sample_ro_local`, warmup12
- `sampler_island_local`, warmup0
- `sampler_island_local`, warmup12

Files:

- `scripts/build_restart_sampler_island_20260523.ps1`
- `data/experiments/fast_mode/hardware_queue_restart_sampler_island_20260523.csv`
- `doc/restart_sampler_island_experiment_plan_20260523.md`
- `doc/restart_sampler_island_capture_status_20260523.md`

Capture outcome:

| variant | warmup | expected bytes | captured bytes | status |
| --- | ---: | ---: | ---: | --- |
| `sample_ro_local` | 0 | 125000 | 0 | no UART bytes |
| `sample_ro_local` | 12 | 125000 | 0 | no UART bytes |
| `sampler_island_local` | 0 | 125000 | 36529 | partial stream, then timeout |
| `sampler_island_local` | 12 | 125000 | 0 | no UART bytes |

These are diagnostic only. They are not valid SP800-90B restart datasets.

Interpretation:

Restart auto-stream behavior is sensitive to sampler-side constraints. The
next step is a reduced debug-header smoke variant, not another blind formal
1000x125 rerun.

## Older but Still Important Results

### SP800-90B Restart Path

The project has previously achieved a real `1000 x 1000` auto-stream restart
long capture for `random3`:

- File:
  `data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_1000x1000_header_delay60s_20260515.bin`
- Header: `A55A03E803E801D0`
- Size: `1,000,000 bytes`
- SHA256 prefix/suffix: `7789491D...E3D6`

Bit-symbol SP800-90B restart inputs were also generated from `1000 x 125 bytes`
captures expanded to `1000 x 1000` bit symbols:

- MSB input SHA256: `8C927742...6726`
- LSB input SHA256: `25A3C2E9...07A4`

`ea_restart` ran, but `random3` did not pass restart sanity:

- MSB: `H_I=0.902345`, `X_cutoff=605`, `X_max=685`
- LSB: `H_I=0.828444`, `X_cutoff=632`, `X_max=685`

Mechanism finding:

- Failure was not global randomness collapse.
- Fixed columns had strong bias:
  - MSB abnormal column: `7`
  - LSB abnormal column: `0`
- These map to the same raw byte position.

This supports the idea that continuous non-IID entropy can be high while restart
fixed-position behavior remains biased.

Read:

- `doc/restart_auto_stream_plan_20260514.md`
- `doc/sp800_90b_restart_execution_status_20260514.md`
- `data/experiments/restart_summary_20260515/restart_result_summary_20260522.md`
- `data/experiments/paper_artifacts_20260515/`

### Placement / Continuous TRNG Matrix

The project has placement variants such as:

- `compact`
- `checker`
- `sparse`
- `far`
- `same_column`
- `random1`
- `random3`
- original/fpga1 baseline

Many continuous TRNG 10MiB/20MiB repeats and XADC metadata exist under:

- `data/hardware/20260511_fpga1_board1/trng/`
- `data/experiments/xadc_summary/`
- `data/experiments/paper_artifacts_20260514/`
- `data/experiments/mechanism_hypothesis_20260523/`

Before summarizing claims, regenerate or inspect:

```powershell
python scripts\summarize_trng_repeats.py
python scripts\analyze_fast_mode_results.py
python scripts\summarize_xadc_metadata.py --tag 20260523
python scripts\make_mechanism_hypothesis_evidence_table.py
```

## Key Files to Read Before Acting

Start with:

- `doc/fast_mode_status_20260523.md`
- `doc/new_conversation_bootstrap_prompt_20260523.md`
- `doc/mechanism_hypothesis_goal_20260523.md`
- `doc/random1_sampler_island_ablation_20260523.md`
- `doc/tdc_sampler_mechanism_experiment_plan_20260523.md`
- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.md`
- `doc/restart_sampler_island_experiment_plan_20260523.md`
- `doc/restart_sampler_island_capture_status_20260523.md`

Then read task-specific source:

- TDC RTL:
  - `rtl/tdc/RO_TDC_pair_sysclk_top.v`
  - `rtl/tdc/tdc_lane.v`
  - `rtl/tdc/tdc_uart_packetizer.v`
- Restart RTL:
  - `rtl/restart/`
- TDC Vivado flow:
  - `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`
- TDC sampler-data support:
  - `scripts/generate_tdc_sampler_data_xdc.py`
  - `scripts/build_tdc_sampler_data_bitstreams.ps1`
  - `scripts/summarize_tdc_sampler_data.py`
- Capture support:
  - `scripts/program_and_capture_uart.ps1`
  - `scripts/capture_uart.ps1`
  - `scripts/run_fast_hardware_queue.ps1`
  - `scripts/read_xadc.ps1`

## Immediate Best Next Work

### P0: Build reset-aligned / warmup-aligned TDC debug line

Current `RO_TDC_pair_sysclk_top.v` streams continuously and cannot distinguish
startup transient from steady state. Implement a new reset-aligned top that:

- waits after reset/PLL lock
- enables both ROs at a known time
- optionally discards a warmup number of TDC packets
- emits a fixed debug header
- outputs exactly `CAPTURE_PACKETS`
- stops cleanly

Suggested new RTL:

- `rtl/tdc/RO_TDC_reset_aligned_top.v`

Suggested parameters:

- `START_DELAY_CYCLES`
- `RO_ENABLE_DELAY_CYCLES`
- `WARMUP_PACKETS`
- `CAPTURE_PACKETS`
- `DEBUG_HEADER`
- `RO_A_STAGES`
- `RO_B_STAGES`
- `PAIR_ID`
- `FAMILY_ID`

Minimal experimental matrix:

- `random1 baseline`: warmup0 / warmup12-equivalent
- `random3 goodref`: warmup0 / warmup12-equivalent
- `random1 sampler-island`: warmup0 / warmup12-equivalent, but only after a
  tiny debug-header smoke test passes

Analysis metrics:

- early-window bin entropy
- transition entropy
- residence time / longest same-bin run
- small-lag autocorrelation
- first-window vs later-window comparison

Suggested analysis script:

- `scripts/analyze_tdc_startup_diffusion.py`

Suggested output:

- `data/experiments/tdc_startup_diffusion_20260523/tdc_startup_diffusion_summary.csv`
- `data/experiments/tdc_startup_diffusion_20260523/tdc_startup_diffusion_summary.md`

Decision interpretation:

- If warmup0 is concentrated and warmup12 is diffuse, TDC gives positive startup
  transient evidence.
- If TDC does not split but TRNG/restart does, TDC further bounds the mechanism
  toward sampling registers/routing/output sampling path.

### P1: Separate sample RO from sampling registers/routing

The sampler-island repair has two components:

1. sample RO moved/localized
2. sampling registers/routing localized

To strengthen causality, create ablations that hold one part fixed and move the
other. This may require XDC/RTL changes to constrain sampling registers
independently.

### P1: Fix restart sampler-island debug

Do not rerun the 1000x125 sampler-island restart queue blindly. First build a
reduced debug-header smoke variant:

- very small rows/counts
- header emitted immediately
- longer timeout only after header proves startup

Use the partial 36529-byte warmup0 sampler-island run as a clue that the logic
can start under one constraint variant but is not robust enough for formal data.

### P2: Multi-board replication

If the user can borrow multiple boards, repeat the most compact evidence set:

- random1 baseline continuous 10MiB/20MiB
- random1 sampler-island continuous 10MiB/20MiB
- random3 reference continuous 10MiB/20MiB
- one restart warmup boundary case
- one or two TDC negative-control checks

Purpose: show the sampler-side effect is not a one-board artifact.

## Commands and Patterns

### Safe Hardware Queue Pattern

Before starting:

```powershell
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -match 'powershell|vivado|cmd|hw_server' -and
  ($_.CommandLine -match 'run_fast_hardware_queue|program_and_capture_uart|capture_uart|vivado|read_xadc|program_bitstream|hw_server')
} | Select-Object ProcessId,Name,CommandLine | Format-List
```

Do not start if another capture/programming task is active.

### TDC Build Pattern

```powershell
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" -mode batch `
  -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
  -tclargs data\experiments\xdc_tdc_sampler_data\<xdc>.xdc `
           data\vivado_runs\fpga1_tdc_sampler_data\<run_name> `
           RO_TDC_pair_sysclk_top `
           "{RO_A_STAGES=9 RO_B_STAGES=2 PAIR_ID=<id> FAMILY_ID=<id>}"
```

### Capture Pattern

Use existing queue/capture scripts rather than manual serial tools:

- `scripts/program_and_capture_uart.ps1`
- `scripts/capture_uart.ps1`
- `scripts/run_fast_hardware_queue.ps1`

These support `Kind` values including `trng`, `tdc`, and `restart`. XADC
before/after metadata is supported through the programming/capture flow.

## Claim Boundaries

Safe claims:

- Placement strongly affects raw RO-TRNG statistics.
- Sampler-side placement can repair `random1` from biased to near ideal while
  preserving data-RO placement.
- Measured pairwise TDC correlations do not support simple hard-locking as the
  dominant explanation.
- Restart testing reveals fixed-position/column bias that can remain even when
  continuous-stream entropy looks high.
- XADC was recorded before/after many captures and should be used to bound
  simple temperature/voltage explanations.

Unsafe claims unless more work is done:

- Full NIST SP800-90B certification.
- Absolute ps-level jitter or calibrated phase drift.
- Universal effect across all boards/PVT.
- Proof that no coupling exists.
- Proof that sampler-side aperture is the only mechanism.

Use wording like:

> The current TDC measurements rule out a simple persistent pairwise hard-locking
> explanation in the measured configurations, but they do not rule out weaker,
> transient, multi-oscillator, routing, register, or PVT-dependent mechanisms.

## How the New Model Should Behave

- Speak Chinese to the user unless asked otherwise.
- Be proactive, but do not launch blind hardware repeats.
- Keep the user informed at the level of major experimental phases.
- Update docs whenever experiments or analyses finish.
- Close/stop any background/subagent work that has completed.
- If using subagents, give them narrow tasks with clear input files and expected
  outputs, then merge their findings into docs.
- If hardware is unavailable, continue with RTL, analysis scripts, paper tables,
  literature framing, and experiment design.
- If hardware is available, prioritize discriminating experiments that test a
  mechanism, not repeated data volume for its own sake.

