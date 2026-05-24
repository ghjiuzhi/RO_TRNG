# TDC Sampler-Mechanism Experiment Plan 20260523

- workspace: `E:\Project\MLDSA\RO_TRNG`
- board: `z7020_b01`
- current priority: hypothesis-driven TDC, not blind pair repetition

## Core Hypothesis

The current evidence says that placement-dependent RO-TRNG degradation is more likely dominated by the sampler side than by persistent data-data RO locking.

The strongest causal observation is:

- baseline `random1`: `p1=0.337669`, bit min-entropy `0.594377`
- same data placement, sample RO moved to `SLICE_X45Y39`: programmed 20MiB `p1=0.484799`, bit min-entropy `0.956792`
- same data placement, sample RO plus sampling registers local: programmed 5MiB `p1=0.500027`, bit min-entropy `0.999923`

This means the sampler path should be treated as part of the entropy source. TDC should now test sampler-data phase behavior, not just data-data pair locking.

## TDC Guess A: Sampler-Data Phase Pulling

Claim:

Bad placements are created when the sample RO is pulled into a sampler-data phase relationship that over-samples a biased region of the data-RO ensemble.

Predictions:

- `random1` baseline should show larger sampler-data phase drift structure than `random3` or sampler-island-fixed `random1`.
- The nearest data-to-sampler RO pairs should have stronger low-lag correlation or lower phase diffusion in bad placements.
- Moving the sample RO from `X36Y35` to `X45Y39` should reduce sampler-data TDC structure and match the improved TRNG output.

Next hardware:

1. Build TDC where RO A is the sample RO and RO B is a selected `random1` data RO.
2. Repeat for the same data RO with sample RO moved to `X45Y39`.
3. Run the same pair style on `random3` as a good reference.

Decision rule:

- If sampler-data TDC structure tracks TRNG bias while data-data pair TDC remains weak, this becomes the main mechanism figure.
- If sampler-data TDC is also weak, the mechanism shifts toward sampling-register routing/metastability aperture rather than RO phase pulling alone.

### 2026-05-23 P0 Result

The first causal sampler-data TDC pair has completed for `random1` RO0:

| run | TRNG context | packets | phase_r | bin_r | diff_std_ps nominal | A Hbin | B Hbin | XADC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `tdc_sampler_data_random1_baseline_sample_x36y35_ro0_2mib` | bad baseline sampler, baseline TRNG `p1=0.337669` | 262144 | 0.001492 | 0.001040 | 1978.888 | 2.79191 | 5.54099 | 46.6 -> 46.9 C |
| `tdc_sampler_data_random1_local_sample_x45y39_ro0_2mib` | same data RO, sampler moved to local-fix placement, TRNG `p1=0.484799` sample-only / `0.500051` sampler-island | 262143 | -0.000491 | -0.001104 | 1978.996 | 2.77432 | 5.42345 | 47.1 -> 46.9 C |

Interpretation:

- This P0 pair does **not** support a simple hard-locking explanation. The bad baseline and improved local-sampler cases have nearly zero sampler-data Pearson correlation and nearly identical nominal phase-difference spread.
- The result is valuable as a negative control: the TRNG entropy shift is large, but the simple raw TDC phase-correlation metric is not.
- The mechanism should therefore be written more carefully as a sampler/register/routing-path effect, with TDC constraining what the mechanism is not. TDC is still useful, but the central causal evidence remains the sampler-island ablation.
- No calibrated picosecond claim should be made from these raw TDC bins until code-density calibration is added.

P1 remains worth running, but only as a mechanism-stability check:

1. `random1` RO4 baseline/local tests whether the negative-control result is RO0-specific.
2. `random3` references show whether a good placement has the same weak sampler-data correlation.
3. If all P1 runs remain weak, stop repeating sampler-data TDC and move to restart startup/warmup tests or routing/register ablations.

### 2026-05-23 P1 Closure

The full six-run sampler-data TDC queue completed:

| run group | completed runs | phase_r range | nominal diff_std_ps range | result |
| --- | ---: | ---: | ---: | --- |
| `random1` baseline/local, RO0/RO4 | 4 | `-0.002472` to `0.001492` | `1977.164` to `1980.745` | weak correlation in all causal variants |
| `random3` good reference, RO0/RO3 | 2 | `-0.001408` to `0.002244` | `1971.942` to `1978.297` | same weak-correlation pattern |

Decision:

- Stop adding same-style sampler-data TDC repeats. The result is stable enough for a negative-control conclusion.
- Do not claim that TDC explains the sampler-island repair through direct pairwise locking or strong measured phase correlation.
- Use TDC to bound the mechanism: the large TRNG entropy repair occurs without a matching raw sampler-data TDC correlation split.
- Next discriminating hardware should target `sample RO only` versus `sampling registers/routing only`, plus restart/warmup behavior.

## TDC Guess B: Phase Diffusion, Not Locking

Claim:

The important feature may be how fast relative phase diffuses through the sampling aperture, not whether two ROs hard-lock.

Predictions:

- Bad continuous streams should show lower phase-diffusion rate or structured TDC-bin recurrence, even without high Pearson correlation.
- Good streams should have flatter transition behavior across TDC bins/windows.

Metrics:

- windowed TDC-bin entropy
- small-lag autocorrelation
- phase-bin transition entropy
- residence time in the most common bins
- run length of repeated/similar TDC bins

Decision rule:

- If diffusion metrics separate `random1` baseline from sampler-island-fixed `random1`, use this as the TDC explanation.
- If only TRNG bit statistics separate them, TDC is a supporting negative-control instrument rather than the central evidence.

## TDC Guess C: Startup Phase Memory

Claim:

Restart failures come from deterministic startup phase memory. Warmup removes this memory, but the warmup threshold is placement-dependent.

Predictions:

- TDC immediately after enable/reset should have low bin entropy or repeated early columns.
- TDC after warmup should have higher bin entropy and lower fixed-column bias.
- This should align with SP800-90B restart observations: warmup0 fails, warmup12 passes for several placements.

Next hardware:

1. Capture short TDC bursts with `warmup0`.
2. Capture matched bursts with `warmup12`.
3. Compare first-window bin entropy and most-common-bin concentration.

Decision rule:

- If early TDC is deterministic and warmup TDC is diffuse, restart transient becomes a strong paper section.
- If TDC does not change but restart bits do, the transient is likely in the sampled data path or output packing, not the measured RO pair.

## TDC Guess D: Calibration Boundary

Claim:

Raw TDC bins are enough for relative/categorical mechanism evidence, but not enough for calibrated time claims.

Policy:

- Use raw-bin entropy, correlation, transition structure, and windowed comparisons in the main mechanism analysis.
- Do not claim calibrated picoseconds unless a code-density calibration is added.
- If calibration is added, run a free-running asynchronous source through the same TDC path and estimate per-bin widths before converting bins to time.

## Next Concrete Queue

After the current sampler-island 20MiB confirmation finishes, the next hardware queue should be:

1. `random1` baseline sampler-data TDC: sample `X36Y35` versus nearest/representative data ROs.
2. `random1` sampler-local sampler-data TDC: sample `X45Y39` versus the same data ROs.
3. `random3` sampler-data TDC reference.
4. Optional: startup/warmup TDC bursts if the above separates the cases.

The expected high-level result is not necessarily "locking exists." The better expected result is:

> TDC either detects sampler-data phase-structure differences that track entropy, or it serves as a negative control showing that the decisive placement sensitivity is in the sampler/register/routing path rather than persistent pairwise RO locking.

## Prepared Artifacts

Generated sampler-data TDC XDCs:

- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_baseline_sample_x36y35_ro4.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_local_sample_x45y39_ro4.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random3_sample_x36y35_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random3_sample_x36y35_ro3.xdc`

Supporting code:

- `scripts/generate_tdc_sampler_data_xdc.py`
- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl` now accepts optional synth generics as arg 4.
- `scripts/build_tdc_sampler_data_bitstreams.ps1`
- `data/experiments/fast_mode/hardware_queue_tdc_sampler_data_20260523.csv`

Build pattern:

```powershell
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" -mode batch `
  -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
  -tclargs data\experiments\xdc_tdc_sampler_data\<xdc>.xdc `
           data\vivado_runs\fpga1_tdc_sampler_data\<run_name> `
           RO_TDC_pair_sysclk_top `
           "{RO_A_STAGES=9 RO_B_STAGES=2 PAIR_ID=<id> FAMILY_ID=<id>}"
```

Do not run these builds concurrently with UART/JTAG capture on a weak PC. They do not use COM3, but Vivado implementation can consume enough CPU and memory to make a long serial capture less stable.
