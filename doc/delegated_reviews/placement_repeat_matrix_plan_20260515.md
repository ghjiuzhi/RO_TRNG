# Placement Repeat Matrix Plan - 2026-05-15

Scope: offline planning only. Do not start hardware, Vivado programming, COM3, JTAG, or hw_server from this review.

Inputs read:

- `data\experiments\fast_mode\*.csv`
- `doc\fast_mode_master_status_20260514.md`
- `doc\paper_high_level_upgrade_plan_20260514.md`
- `scripts\run_fast_hardware_queue.ps1`
- `scripts\capture_uart.ps1`

Only output file written by this review:

- `doc\delegated_reviews\placement_repeat_matrix_plan_20260515.md`

## Existing Evidence Baseline

The current fast-mode matrix already contains valid 10 MiB formal captures and 5 MiB repeats for the main placement families. `random1` and `random3` additionally have completed 20 MiB repeats from the short queue.

| placement | current formal | current repeat | key current observation |
| --- | ---: | ---: | --- |
| `random1` | 10 MiB | 5 MiB + 20 MiB | stable bad case; 20 MiB repeat already reinforces bias |
| `random3` | 10 MiB | 5 MiB + 20 MiB | stable good case; 20 MiB repeat already reinforces near-ideal balance |
| `compact` | 10 MiB | 5 MiB | high bit entropy; needs larger repeat for error bars |
| `checker` | 10 MiB | 5 MiB | high bit entropy; needs larger repeat for error bars |
| `sparse` | 10 MiB | 5 MiB | lower entropy family; important non-random bad-ish case |
| `far` | 10 MiB | 5 MiB | mild bias, runs failure; useful mechanism/control contrast |
| `same_column` | 10 MiB | 5 MiB | p1 near ideal but runs/adjacent anomaly; important single-metric counterexample |
| `random2` | 10 MiB | 5 MiB | random-family middle/low case; useful bridge between random1/random3 |
| `row` | 10 MiB | 5 MiB | lower entropy structured placement; useful for full matrix |
| `cross_region` | 10 MiB | 5 MiB | high-quality structured placement; useful as a second good structured control |

## Timing Model

Use conservative queue planning numbers derived from existing metadata:

- 10 MiB TRNG capture: plan 25 minutes capture time.
- 20 MiB TRNG capture: plan 50 minutes capture time.
- Per row programming/switch/analysis overhead: reserve 5 minutes.
- Practical queue estimate: 10 MiB row = 30 minutes; 20 MiB row = 55 minutes.

Measured examples supporting this range:

- `random1_repeat03`, 20 MiB: 2839 s, about 47.3 minutes.
- `checker_run01`, 10 MiB: 1210 s, about 20.2 minutes.
- `same_column_run01`, 10 MiB: 1786 s, about 29.8 minutes.

## Recommended Matrix

Main recommendation: build a full larger repeat matrix with one 20 MiB repeat for every non-original placement, while not re-running `random1` and `random3` unless the goal is balanced repeat count rather than new evidence.

| priority | placement | size | proposed run | reason | est. row time |
| --- | --- | ---: | --- | --- | ---: |
| P0 | `same_column` | 20 MiB | `same_column_repeat03_20mib` | p1 looks good but runs/adjacent anomaly is central to the paper's multi-metric argument | 55 min |
| P0 | `sparse` | 20 MiB | `sparse_repeat03_20mib` | structured low-entropy placement; validates that non-random layouts can also be poor | 55 min |
| P0 | `far` | 20 MiB | `far_repeat03_20mib` | mild bias with runs failure; useful distance/control contrast | 55 min |
| P0 | `compact` | 20 MiB | `compact_repeat03_20mib` | strong structured good/control case; needed for error-bar comparison | 55 min |
| P0 | `checker` | 20 MiB | `checker_repeat03_20mib` | strong structured good/control case; needed for error-bar comparison | 55 min |
| P1 | `random2` | 20 MiB | `random2_repeat03_20mib` | fills random-family middle case between random1 and random3 | 55 min |
| P1 | `row` | 20 MiB | `row_repeat03_20mib` | lower-entropy structured placement; improves full-matrix completeness | 55 min |
| P1 | `cross_region` | 20 MiB | `cross_region_repeat03_20mib` | high-quality structured control; completes 10-placement repeat matrix | 55 min |
| P2 | `random1` | 10 MiB | `random1_repeat04_10mib` | optional balanced extra replicate; 20 MiB repeat already exists | 30 min |
| P2 | `random3` | 10 MiB | `random3_repeat04_10mib` | optional balanced extra replicate; 20 MiB repeat already exists | 30 min |

Estimated totals:

- P0 only: 5 rows, about 4.6 hours.
- P0 + P1: 8 rows, about 7.3 hours.
- P0 + P1 + P2: 10 rows, about 8.3 hours.

If only one overnight run is available, use P0 + P1. If human supervision is limited, run P0 first and stop; it gives the largest paper value per board-hour.

## Naming Rules

Use explicit size suffixes for all new larger repeats to avoid ambiguity with existing `repeat02_5mib` and `repeat03` names:

- Run id: `<placement>_repeat03_20mib` for placements that do not yet have a 20 MiB repeat.
- Optional extra run id: `random1_repeat04_10mib`, `random3_repeat04_10mib`.
- Output: `data\hardware\20260511_fpga1_board1\trng\<run>.bin`
- Metadata: `data\hardware\20260511_fpga1_board1\metadata\<run>.json`
- SHA256: produced by `capture_uart.ps1` / queue flow as `<out_file>.sha256.txt`

Do not reuse `random1_repeat03` or `random3_repeat03`; those already exist as 20 MiB captures without the size suffix.

## Queue CSV Recommendation

Suggested CSV path, if/when hardware collection is authorized later:

- `data\experiments\fast_mode\hardware_queue_placement_repeat_20260515.csv`

Recommended queue content:

```csv
enabled,priority,run,kind,bitstream,bytes,out_file,metadata_dir
1,P0,same_column_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\same_column_pitch3_x44y35\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\same_column_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P0,sparse_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\sparse_pitch6_x36y35\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\sparse_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P0,far_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\far_x20y25\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\far_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P0,compact_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_sweep\ro_compact_x44y43\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\compact_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P0,checker_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_sweep\ro_checker_pitch3_x44y43\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\checker_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P1,random2_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\random_seed2_x36y35\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\random2_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P1,row_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\row_pitch3_x38y43\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\row_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
1,P1,cross_region_repeat03_20mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\cross_region_x36y25\seed_1\RO_TRNG_top.bit,20MiB,data\hardware\20260511_fpga1_board1\trng\cross_region_repeat03_20mib.bin,data\hardware\20260511_fpga1_board1\metadata
0,P2,random1_repeat04_10mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit,10MiB,data\hardware\20260511_fpga1_board1\trng\random1_repeat04_10mib.bin,data\hardware\20260511_fpga1_board1\metadata
0,P2,random3_repeat04_10mib,trng,data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit,10MiB,data\hardware\20260511_fpga1_board1\trng\random3_repeat04_10mib.bin,data\hardware\20260511_fpga1_board1\metadata
```

Notes:

- P2 rows are intentionally disabled (`enabled=0`) because random1/random3 already have 20 MiB repeats.
- `run_fast_hardware_queue.ps1` will skip rows only when output and metadata exist with the requested byte count, so these names avoid accidental collision with completed data.
- Keep `kind=trng` so the queue flow invokes analysis after capture.

## Execution Order Rationale

1. `same_column`, `sparse`, and `far` first: these are the most useful for defending that p1 alone is insufficient and that structured placements can produce repeatable non-ideal behavior.
2. `compact` and `checker` next: they provide high-quality structured controls and error bars for the good-placement side.
3. `random2`, `row`, `cross_region` next: these complete the full 10-placement larger-repeat matrix.
4. `random1` and `random3` optional: already have 20 MiB repeats, so extra 10 MiB repeats are mostly for balanced replicate counts or reviewer-facing robustness.

## Recommended Claim Boundary After Collection

After P0 + P1 completes, the paper can say the 10-placement matrix has a larger-repeat reproducibility check, with 20 MiB repeats for every non-original placement family except the already completed random1/random3 pair, which already have 20 MiB repeats under existing names.

It should still avoid claiming cross-board, cross-PVT, or cross-Vivado-seed generality. The result remains single-board, nominal-condition, fixed-flow evidence.
