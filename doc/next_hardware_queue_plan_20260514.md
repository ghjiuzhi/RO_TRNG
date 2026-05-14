# Next Hardware Queue Plan 2026-05-14

Scope: planning only. Do not start Vivado programming, UART capture, COM3, JTAG, or board power cycling from this document.

## Operating constraints

- Hardware access must remain single-queue and serialized. Any item that programs a bitstream or captures UART data grabs COM3 and JTAG and must not run in parallel with another hardware job.
- Current measured UART throughput is about 11.45 KiB/s at 115200 baud. Use these planning estimates: 2 MiB is about 3.1 min capture, 5 MiB about 7.6 min, 10 MiB about 15.2 min, and 20 MiB about 30.5 min, before Vivado programming and post-analysis overhead.
- `scripts/run_fast_hardware_queue.ps1` can run CSV-driven single-shot captures and then refresh fast-mode analyses. It does not implement a SP800-90B restart protocol by itself.
- SP800-90B restart evidence requires independent restart rows, not ordinary sequential `.bin` captures. Treat restart capture as a separate protocol until a dedicated wrapper exists.

## Short queue: tonight / tomorrow

Goal: add the most valuable same-board evidence without expanding the story sideways. Prioritize `random1` as the stable bad case and `random3` as the stable good case.

Recommended order:

| Priority | Project | Purpose | Bitstream | Capture size | Estimated hardware time | COM3/JTAG | Analysis scripts |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| S0 | `random1_trng_repeat03_20mib` | Long repeat for the biased `random1` case; tests whether the low entropy/bias result remains stable at larger sample size. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` | 20 MiB | about 31 min capture, plan 35-40 min with programming/analysis | Yes, COM3 during capture; JTAG during programming | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\analyze_fast_mode_results.py`; then `scripts\prepare_90b_inputs.py` for 90B input |
| S0 | `random3_trng_repeat03_20mib` | Long repeat for the high-entropy `random3` case; paired control against `random1`. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` | 20 MiB | about 31 min capture, plan 35-40 min with programming/analysis | Yes, COM3 during capture; JTAG during programming | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\analyze_fast_mode_results.py`; then `scripts\prepare_90b_inputs.py` for 90B input |
| S1 | `random1_ro_freq_fixed_run04_5mib` | Longer RO-frequency repeat for `random1`; checks whether sample pulling remains larger than `random3`. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random1_seed1_x36y35\RO_FREQ_trng_probe_top.bit` | 5 MiB | about 8 min capture, plan 10-12 min | Yes, COM3 during capture; JTAG during programming | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| S1 | `random3_ro_freq_fixed_run04_5mib` | Paired RO-frequency repeat for `random3`; keeps the mechanism comparison balanced. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random3_seed3_x36y35\RO_FREQ_trng_probe_top.bit` | 5 MiB | about 8 min capture, plan 10-12 min | Yes, COM3 during capture; JTAG during programming | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| S2 | `random1_restart_pilot_100x1k` | Pilot restart dataset to validate row protocol, file naming, and 90B conversion before committing to 1000 restarts. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` | 100 restarts x 1 KiB raw each, total 100 KiB payload | Payload is short, but repeated programming/restart dominates; plan 1-2 h if each restart is 30-60 s | Yes, repeatedly grabs JTAG and COM3; highest conflict risk | Requires new restart wrapper; then `scripts\prepare_90b_inputs.py`; later `ea_restart` from `sim\SP800-90B_EntropyAssessment\cpp` |
| S2 | `random3_restart_pilot_100x1k` | Same restart-pilot protocol for the good case; only run after `random1` pilot path is confirmed. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` | 100 restarts x 1 KiB raw each, total 100 KiB payload | Plan 1-2 h if each restart is 30-60 s | Yes, repeatedly grabs JTAG and COM3; highest conflict risk | Requires new restart wrapper; then `scripts\prepare_90b_inputs.py`; later `ea_restart` from `sim\SP800-90B_EntropyAssessment\cpp` |

Short-queue recommendation: run the two 20 MiB TRNG repeats first. They are the cleanest tonight/tomorrow payoff and use existing queue mechanics. Add the two 5 MiB RO_FREQ repeats only if the board window is still clear. Treat restart as a pilot, because the current queue runner cannot make SP800-90B restart rows without extra wrapper logic.

Expected short-queue wall time:

| Subset | Items | Rough time |
| --- | --- | --- |
| Minimal | two 20 MiB TRNG repeats | about 1.2-1.4 h |
| Useful add-on | plus two 5 MiB RO_FREQ repeats | about 1.6-1.9 h |
| With restart pilots | plus two 100-restart pilots | about 3.6-5.9 h, dominated by repeated JTAG/restart overhead |

## Restart protocol notes

- Formal SP800-90B restart should target 1000 restarts x 1000 symbols per placement. For a raw bitstream represented as one byte per bit-symbol, the final 90B input is row-major symbols; the hardware capture may still be packed bytes if `scripts\prepare_90b_inputs.py` records the conversion.
- The pilot above intentionally uses 100 restarts x 1 KiB raw payload to debug control flow, metadata, and row conversion. It should not be used as headline 90B restart evidence.
- The dedicated restart wrapper should record per-row metadata: bitstream SHA-256, restart index, requested bytes, captured bytes, UART SHA-256, start/end time, board id, room/FPGA temperature, voltage condition, and whether the restart was full power-cycle, PS reset, PL reprogram, or another method.
- Do not merge restart rows into ordinary sequential repeat files. Keep them under a separate directory such as `data\hardware\20260511_fpga1_board1\restart\`.

## Top-journal queue: multi-board / PVT / voltage-temperature

Goal: support claims beyond one board at nominal voltage and room temperature. This is not a quick data-grab queue; it is a validation campaign.

### Multi-board replication

Run on at least two additional boards with the same protocol and explicit board IDs.

| Priority | Project | Purpose | Bitstream | Capture size | Estimated hardware time per board | COM3/JTAG | Analysis scripts |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| T0 | `boardN_random1_trng_formal_10mib` | Check whether the `random1` bad-case behavior reproduces across boards. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` or board-matched rebuilt bitstream if the device/project differs | 10 MiB | about 15 min capture, plan 18-22 min | Yes | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\prepare_90b_inputs.py`, 90B `ea_non_iid` |
| T0 | `boardN_random3_trng_formal_10mib` | Check whether the `random3` good-case behavior reproduces across boards. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` or board-matched rebuilt bitstream | 10 MiB | about 15 min capture, plan 18-22 min | Yes | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\prepare_90b_inputs.py`, 90B `ea_non_iid` |
| T1 | `boardN_random1_ro_freq_5mib` | Mechanism replication for `random1` sample pulling / frequency proximity. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random1_seed1_x36y35\RO_FREQ_trng_probe_top.bit` or board-matched rebuilt bitstream | 5 MiB | about 8 min capture, plan 10-12 min | Yes | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| T1 | `boardN_random3_ro_freq_5mib` | Mechanism replication for `random3`. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random3_seed3_x36y35\RO_FREQ_trng_probe_top.bit` or board-matched rebuilt bitstream | 5 MiB | about 8 min capture, plan 10-12 min | Yes | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| T2 | `boardN_random1_restart_formal_1000x1000` | Formal restart evidence for the bad case. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` or board-matched rebuilt bitstream | 1000 restarts x at least 1000 bit-symbols | 8-17 h if each restart takes 30-60 s, plus capture/metadata overhead | Yes, repeatedly; schedule as exclusive board time | Dedicated restart wrapper, `scripts\prepare_90b_inputs.py`, 90B `ea_restart` |
| T2 | `boardN_random3_restart_formal_1000x1000` | Formal restart evidence for the good case. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` or board-matched rebuilt bitstream | 1000 restarts x at least 1000 bit-symbols | 8-17 h if each restart takes 30-60 s, plus capture/metadata overhead | Yes, repeatedly; schedule as exclusive board time | Dedicated restart wrapper, `scripts\prepare_90b_inputs.py`, 90B `ea_restart` |

### PVT / voltage-temperature sweep

Use `random1` and `random3` only at first. Expanding to all placements before these two are stable will dilute the evidence.

| Priority | Project | Purpose | Bitstream | Capture size | Estimated hardware time per condition | COM3/JTAG | Analysis scripts |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| P0 | `pvt_<cond>_random1_trng_10mib` | Bias/entropy stability of `random1` under one PVT condition. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` | 10 MiB | about 15 min capture, plan 20-25 min including stabilization notes | Yes | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\prepare_90b_inputs.py`, 90B `ea_non_iid` |
| P0 | `pvt_<cond>_random3_trng_10mib` | Entropy stability of `random3` under the paired PVT condition. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` | 10 MiB | about 15 min capture, plan 20-25 min including stabilization notes | Yes | `scripts\analyze_trng_dataset.py`, `scripts\summarize_trng_repeats.py`, `scripts\prepare_90b_inputs.py`, 90B `ea_non_iid` |
| P1 | `pvt_<cond>_random1_ro_freq_2mib` | Frequency/pulling mechanism under PVT for `random1`. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random1_seed1_x36y35\RO_FREQ_trng_probe_top.bit` | 2 MiB | about 3 min capture, plan 5-7 min | Yes | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| P1 | `pvt_<cond>_random3_ro_freq_2mib` | Frequency/pulling mechanism under PVT for `random3`. | `data\vivado_runs\fpga1_ro_freq_probe_fixed\random3_seed3_x36y35\RO_FREQ_trng_probe_top.bit` | 2 MiB | about 3 min capture, plan 5-7 min | Yes | `scripts\analyze_ro_frequency_matrix.py`, `scripts\analyze_fast_mode_results.py` |
| P2 | `pvt_<cond>_random1_restart_1000x1000` | Formal restart check at a selected worst/best PVT corner. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` | 1000 restarts x at least 1000 bit-symbols | 8-17 h per condition if restart is JTAG/reprogram based | Yes, exclusive | Dedicated restart wrapper, `scripts\prepare_90b_inputs.py`, 90B `ea_restart` |
| P2 | `pvt_<cond>_random3_restart_1000x1000` | Formal restart check at a selected worst/best PVT corner. | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` | 1000 restarts x at least 1000 bit-symbols | 8-17 h per condition if restart is JTAG/reprogram based | Yes, exclusive | Dedicated restart wrapper, `scripts\prepare_90b_inputs.py`, 90B `ea_restart` |

Suggested PVT condition ladder:

| Stage | Conditions | Rationale | Rough hardware time |
| --- | --- | --- | --- |
| PVT-A | Room temperature, nominal voltage, one repeat after board warm-up | Separates warm-up drift from placement effect. | about 1 h for two TRNG + two RO_FREQ items |
| PVT-B | Low voltage / nominal temperature and high voltage / nominal temperature | Voltage sensitivity without thermal chamber complexity. | about 2 h for two voltage points, excluding setup/stabilization |
| PVT-C | Cold / nominal voltage and hot / nominal voltage | Temperature sensitivity at stable supply. | about 2 h for two temperature points, excluding chamber stabilization |
| PVT-D | Worst two corners from PVT-B/C with formal restart | Converts the most informative corners into SP800-90B restart evidence. | 16-34 h per placement pair if using JTAG/reprogram restart |

## Queue-file implementation notes

- For single-shot short-queue TRNG/RO_FREQ items, create a new CSV such as `data\experiments\fast_mode\hardware_queue_short_20260514.csv` with the same columns as `hardware_queue_20260513.csv`.
- Use `kind=trng` for `RO_TRNG_top.bit` captures and `kind=raw` for `RO_FREQ_trng_probe_top.bit` captures.
- Keep output directories separate by campaign: short repeats under `data\hardware\20260511_fpga1_board1\trng\` and `ro_freq\`; restart under `data\hardware\20260511_fpga1_board1\restart\`; PVT under a condition-specific path such as `data\hardware\20260511_fpga1_board1_pvt\<condition>\`.
- Do not append restart rows to the existing fast-mode CSV until a restart-capable wrapper exists. The existing queue script will only do one program/capture per row and then analyze it as a sequential capture.

## Go / no-go summary

- Go first: `random1_trng_repeat03_20mib` and `random3_trng_repeat03_20mib`.
- Go second if the board is still free: paired 5 MiB RO_FREQ repeats.
- Pilot only: 100-row restart for `random1` and `random3`, after a wrapper is reviewed.
- Defer to a scheduled exclusive campaign: multi-board, full PVT, and formal 1000x1000 restart datasets.
