# TDC pair validation plan for random1/random3

Date: 2026-05-13

Scope: engineering preparation only. Do not program hardware, do not run
Vivado, do not access COM/JTAG/hw_server. This note turns the existing TDC and
RO_FREQ material into the next minimal TDC validation step for the key
random1/random3 RO pairs.

## 1. Existing material read

Relevant RTL and scripts:

- `rtl/tdc/RO_TDC_sysclk_top.v`: current TDC top. It instantiates two probe ROs,
  `u_ro_a` with 9 stages and `u_ro_b` with 7 stages, then samples each through a
  `tdc_lane` at `clk_200m`.
- `rtl/tdc/tdc_lane.v`: CARRY4 chain, sampler, bubble correction, encoder.
- `rtl/tdc/tdc_uart_packetizer.v`: emits 8-byte frames:
  `0xA5, seq[15:0], coarse[15:0], bin_a, bin_b, flags`.
- `scripts/analyze_tdc_uart.py`: decodes frames, computes per-lane
  code-density calibration, DNL/INL, phase mean/std, `diff_std_ps`, and
  `bin/phase_pearson_r`.
- `scripts/generate_tdc_ro_placement_xdc.py`: places only `u_ro_a/u_ro_b`;
  current generator knows `near`, `far`, `same_column`, and `vertical_far`.
- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`: build-only TDC flow with an
  optional extra placement XDC.
- `rtl/debug/RO_FREQ_trng_probe_top.v` and
  `rtl/debug/ro_freq_entropy_probe.v`: TRNG-like 8 data RO plus 1 sample RO
  frequency probe, using `u_entropy_source` hierarchy compatible with the
  random placement XDC.
- `scripts/vivado/run_fpga1_ro_freq_probe_inmem.tcl`: build-only RO_FREQ flow.

Existing build/result folders:

- `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_near_x36y35`
- `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_far_x24y25`
- `data/vivado_runs/fpga1_ro_freq_probe_fixed/random1_seed1_x36y35`
- `data/vivado_runs/fpga1_ro_freq_probe_fixed/random3_seed3_x36y35`

Existing random placement coordinates:

| family | RO0 | RO1 | RO2 | RO3 | RO4 | RO5 | RO6 | RO7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random1 | X44Y39 | X52Y42 | X67Y63 | X66Y59 | X49Y41 | X67Y36 | X60Y62 | X36Y63 |
| random3 | X51Y43 | X59Y65 | X40Y35 | X66Y51 | X50Y47 | X66Y65 | X61Y44 | X50Y44 |

## 2. Why the current near/far TDC baseline is not enough

The existing TDC runs are useful as a platform smoke test, but they do not prove
or disprove coupling in random1/random3.

First, they measure different oscillators. `RO_TDC_sysclk_top` measures two
standalone probe ROs: 9-stage `u_ro_a` and 7-stage `u_ro_b`. The TRNG and
RO_FREQ probes use eight 2-stage data ROs plus one 9-stage sample RO inside
`u_entropy_source`. Therefore, the present near/far data is not measuring the
actual random1/random3 data RO pair behavior.

Second, the placement does not correspond to the random1/random3 matrix. The
near case places probe ROs around `SLICE_X36Y35` and `SLICE_X39Y35`; the far
case uses `SLICE_X24Y25` and `SLICE_X54Y55`. Those are generic baseline sites,
not the key coordinates from `ro_random_seed1_x36y35.xdc` or
`ro_random_seed3_x36y35.xdc`.

Third, the current near/far metrics are nearly indistinguishable:

| run | packets | seq gaps | lane A std phase | lane B std phase | diff std | phase Pearson r |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `tdc_near_run02` | 262143 | 0 | 1350.48 ps | 1379.85 ps | 1927.59 ps | 0.00328 |
| `tdc_far_run01` | 262132 | 43 | 1350.52 ps | 1361.22 ps | 1915.29 ps | 0.00230 |

This says the current probe pair did not show a strong near/far difference. It
does not say that random1's biased TRNG behavior is unrelated to coupling,
frequency beating, or sample/data phase relation.

Fourth, the current TDC analysis captures zero-lag pair phase statistics, but
the random1 failure may involve low beat frequency, slow pulling, sample-edge
aliasing, or multi-RO interaction. Those mechanisms need pair-specific TDC data
combined with RO_FREQ and TRNG metrics.

## 3. Minimal next design change

Use the current TDC chain, sampler, encoder, UART packetizer, and in-memory
Vivado script. Make the smallest RTL/XDC extension that lets the TDC probe use
random1/random3-like 2-stage data RO pairs.

Recommended new RTL draft:

- Add `rtl/tdc/RO_TDC_pair_sysclk_top.v`.
- Keep the ports identical to `RO_TDC_sysclk_top`: `sys_clk`, `por_n_i`,
  `UART_TX_o`.
- Reuse `clk_wiz_0`, `proc_sys_reset_0`, two `tdc_lane` instances,
  `tdc_uart_packetizer`, and `uart_tx`.
- Replace fixed `RO_STAGES(9)` and `RO_STAGES(7)` with generics:
  `RO_A_STAGES=2`, `RO_B_STAGES=2`, `PAIR_ID`, `FAMILY_ID`.
- Preserve instance names `u_ro_a` and `u_ro_b`, so a placement generator can
  constrain them without disturbing the existing top.

Recommended new XDC generator draft:

- Add `scripts/generate_tdc_ro_pair_from_matrix_xdc.py`.
- Inputs:
  `--matrix-xdc data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc`,
  `--pair 4,5`, `--out data/experiments/xdc_tdc_pairs/...xdc`.
- Parse the matrix XDC for the selected `u_entropy_source/RO_NUM_LOOP[i]`
  LOC/BEL values.
- Emit equivalent LOC/BEL constraints for `u_ro_a` and `u_ro_b`.
- Record comments with `family`, `pair`, source XDC, source RO coordinates, RO
  stage count, and whether BEL is copied exactly.

Recommended TCL draft:

- Copy `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl` to a pair-specific
  build script only if needed, or extend it with optional top/generic args.
- It must remain build-only: no hardware manager, no programming, no capture.
- Add a manifest similar to the RO_FREQ flow:
  `top`, `part`, `family_id`, `pair_id`, `ro_a_index`, `ro_b_index`,
  `ro_a_site`, `ro_b_site`, `placement_xdc`, `vivado_version`, and a clear
  `note=build-only flow`.

Do not try to solve all TRNG/sample behavior in the first pair build. The first
goal is to get a controlled pair-specific phase dataset.

## 4. Priority pairs

RO_FREQ analysis already gives a useful shortlist. For data/data TDC, measure
low beat-frequency pairs first, then spatial controls.

| priority | family | pair | reason |
| ---: | --- | --- | --- |
| 1 | random1 | `(4,5)` | smallest observed all-on data/data delta: about `0.466 MHz`; tests low beat relation in the bad family. |
| 2 | random1 | `(0,1)` | second low delta: about `0.979 MHz`; also moderate spatial proximity. |
| 3 | random1 | `(2,4)` | about `1.980 MHz`; checks whether data4 participates in multiple close-frequency relations. |
| 4 | random1 | `(2,5)` | about `2.446 MHz`; pairs with data5, near the strongest `(4,5)` candidate. |
| 5 | random1 | `(2,3)` or `(2,6)` | spatial cluster around the high-Y region; useful even if frequency delta is not the lowest. |
| 6 | random3 | `(3,7)` | smallest observed random3 delta: about `0.673 MHz`; good-family low-beat control. |
| 7 | random3 | `(3,5)` | about `2.327 MHz`; good-family medium-low beat control. |
| 8 | random3 | `(5,7)` | exactly about `3.000 MHz` in current summary; checks another good-family relation. |
| 9 | random3 | `(0,6)` | about `3.078 MHz`; high-frequency pair in good family. |
| 10 | random3 | `(0,7)` or `(4,7)` | spatially close good-family controls; helps separate "near" from "bad". |

Keep at least one random1 and one random3 far/spatial control even if the first
round is short. The comparison must not become "bad family low-beat" versus
"good family arbitrary pair."

## 5. Fields to capture

Keep the existing 8-byte TDC UART frame for the minimal pair experiment:

| field | use |
| --- | --- |
| `seq` | packet continuity, gap/wrap detection. |
| `coarse_lsb` | slow drift/check for packet timing regularity. |
| `bin_a`, `bin_b` | raw TDC phase code for each RO edge stream. |
| `flags` | valid, bubble, empty/full status; reject or stratify suspect samples. |

Add metadata outside the UART packet, in a manifest:

- placement family: `random1` or `random3`
- pair: `(i,j)`
- `ro_a_index`, `ro_b_index`
- `ro_a_site`, `ro_b_site`, copied BELs
- `RO_A_STAGES`, `RO_B_STAGES`
- TDC top version and git commit if available
- TDC carry-chain placement policy; if unconstrained, say so explicitly
- bitstream path and SHA256 in the later hardware phase
- capture file path, size, SHA256, board id, temperature/voltage notes in the
  later hardware phase

For later analysis, extend `scripts/analyze_tdc_uart.py` or post-process its
packet CSV to add:

- lag correlation of `phase_a`, `phase_b`, and `phase_a - phase_b`
- low-frequency drift or Allan-like statistics on the phase difference
- circular phase difference histogram
- per-flag filtered metrics, especially excluding bubble/empty/full frames

## 6. Code-density calibration

Use code-density calibration per lane and per run, as the existing analyzer
already does. The raw `bin_a/bin_b` codes are not uniform-time bins because
carry-chain tap delays vary and many codes can be dead.

Procedure:

1. Decode raw frames and keep only frames with valid sequence continuity unless
   explicitly studying gaps.
2. Build a histogram for each lane across `bins=256` or the inferred bin count.
3. For each code `k`, estimate width:
   `width_ps[k] = count[k] / total_count * clock_period_ps`.
4. For the 200 MHz sampling clock, use `clock_period_ps = 5000`.
5. Compute:
   `DNL[k] = count[k] / ideal_count - 1`,
   `INL[k] = cumulative(DNL)`,
   and `phase_center_ps[k] = cumulative_width_ps + 0.5 * width_ps[k]`.
6. Map each raw code to `phase_center_ps` before computing
   `lane_*_std_phase_ps`, `diff_std_ps`, and `phase_pearson_r`.
7. Report dead bins, max/min DNL, and peak absolute INL with every pair metric.

Calibration caveat: code-density assumes the sampled phase sweeps through the
TDC range sufficiently. If a pair shows very low used-bin count or extreme INL,
that is both a measurement-quality warning and possibly a mechanism signal. Do
not compare raw bin std across builds without the code-density phase mapping.

## 7. How to connect TDC with RO_FREQ and TRNG metrics

The intended evidence chain is:

`placement -> RO frequency / beat / pulling -> TDC phase relation -> TRNG bias/min-entropy`

For every TDC pair row, join these columns from the RO_FREQ summary:

- family
- all-on `freq_a_mhz`, `freq_b_mhz`
- `abs_delta_f_mhz`
- `beat_period_ns = 1000 / abs_delta_f_mhz`
- single-on versus all-on pulling shift for each RO
- whether either RO belongs to a low-beat cluster

Then join TRNG outcome at family/run level:

- `p1`
- bit min-entropy
- monobit p-value
- runs p-value
- adjacent equal ratio if available

Interpretation rules:

- If random1 low-beat pairs such as `(4,5)` and `(0,1)` show higher
  `phase_pearson_r`, lower `diff_std_ps`, stronger lag correlation, or slower
  phase-difference diffusion than random3 low-beat controls, that supports a
  coupling/pulling/phase-locking mechanism.
- If random1 and random3 pair TDC metrics are similar, but random1 has stronger
  sample-RO pulling or data/sample beat evidence, prioritize the next TDC step:
  data RO versus sample RO.
- If neither data/data nor data/sample TDC differs materially, treat the
  random1 failure as likely involving XOR composition, routing delay, or a
  higher-order multi-RO interaction rather than simple pair coupling.

## 8. Recommended execution order for the next worker

1. Create the pair-specific top and XDC generator as draft files.
2. Generate XDCs for:
   `random1 (4,5)`, `random1 (0,1)`, `random1 (2,4)`,
   `random3 (3,7)`, `random3 (3,5)`, `random3 (0,6)`.
3. Review generated XDC text only; confirm cells target `u_ro_a/u_ro_b` and
   not `u_entropy_source`.
4. In a separate build-authorized session, run the build-only Vivado flow for
   those XDCs and save manifests. Do not program hardware in the build step.
5. In a separate hardware-authorized session, capture UART binary files and run
   `scripts/analyze_tdc_uart.py`.
6. Merge TDC metrics with:
   `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/*`
   and TRNG summary rows for random1/random3.

## 9. Minimal acceptance criteria

A pair-specific TDC run is usable only if:

- packet count is at least the same order as the current baseline
  (`~262k` packets for the reference runs), or the shorter capture is clearly
  marked as smoke data;
- sequence gaps are reported;
- flags are summarized and nonzero flag ratio is not hidden;
- each lane reports used/dead bins, DNL/INL, and phase std;
- the manifest identifies the family, pair, coordinates, and XDC source;
- the final table includes both random1 and random3 controls.

The result should be worded cautiously: pair TDC can support or weaken the
coupling hypothesis, but only data/sample TDC plus RO_FREQ/TRNG correlation can
make a stronger mechanism claim.
