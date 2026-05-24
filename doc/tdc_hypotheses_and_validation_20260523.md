# TDC Hypotheses and Validation Plan

- updated: 2026-05-23 00:20
- board: z7020_b01
- active queue: `data\experiments\fast_mode\hardware_queue_tdc_pairs_repeat02_20260523.csv`
- status doc: `doc\fast_mode_tdc_pairs_repeat02_status_20260523.md`

## Current Interpretation

Existing evidence already says something useful: the six TDC pair captures from run01 did not show strong pair locking. The strongest small-lag absolute phase correlation was about `0.032`, and the generated paper artifact reports `strong_lock_windows=0`. This means the already observed TRNG degradation in `random1`, `sparse`, `row`, and `far` should not be explained too casually as simple two-RO phase locking.

The stronger current explanation is that placement affects several mechanisms at once:

1. RO frequency spacing and all-on pulling change the sampling relationship.
2. Startup/restart transient has fixed-position bias, visible as restart worst columns.
3. Pairwise phase locking, if present, is weak or only appears in specific windows/pairs not yet covered.
4. TDC bin code-density itself is nonuniform, so raw TDC bin numbers must be treated as calibrated categorical/phase evidence, not linear time without calibration.

## Hypotheses

### H1: No Strong Pair Locking in Tested random1/random3 Pairs

Prediction:

- repeat02 should again show small `best_lag_abs_r_max`, preferably below about `0.05`.
- `strong_lock_windows` should remain `0` or near `0`.

Why it matters:

- If this holds, then `random1` poor entropy is not because two monitored ROs simply lock together.
- It pushes the paper toward a richer explanation: placement-dependent pulling, sampling bias, and startup phase structure.

Experiments:

- Repeat all six TDC pair captures:
  - `random1_ro4_ro5`
  - `random1_ro0_ro1`
  - `random1_ro2_ro4`
  - `random3_ro3_ro7`
  - `random3_ro3_ro5`
  - `random3_ro0_ro6`

Metrics:

- `best_lag_abs_r_max`
- `phase_r_mean`
- `phase_r_max_abs`
- `strong_lock_windows`
- `diff_std_ps_mean`

### H2: Frequency Beat / Phase Drift Is More Plausible Than Hard Locking

Prediction:

- closest RO_FREQ pairs should show slowly varying TDC phase difference rather than a flat locked phase.
- `diff_mean_ps_slope_per_window` may be nonzero even when correlation is weak.

Why it matters:

- This can explain why continuous TRNG quality changes with placement even without strong locking.
- Slow beat and phase drift can modulate the sampler relationship and create bias/correlation.

Experiments:

- Compare TDC pair dynamics against RO_FREQ nearest-pair tables.
- Prioritize pairs already chosen from RO_FREQ closest pairs.

Metrics:

- RO_FREQ closest data/data delta MHz
- TDC `diff_mean_ps_slope_per_window`
- TDC `diff_std_ps_mean`
- windowed phase-difference trajectory

### H3: Restart Bias Is a Startup-Window Effect, Not Continuous Locking

Prediction:

- `random3` warmup10 fails while warmup11/12 pass, even though continuous TRNG remains good.
- TDC pair repeat should remain no-lock; restart failure then points to deterministic early transient positions, not long-run pair locking.

Why it matters:

- This is one of the best paper mechanisms: continuous non-IID quality and restart sanity are related but not equivalent.

Experiments:

- Use existing restart summary with fixed XADC association.
- Link restart worst byte/bit/expanded column to TRNG and TDC metrics.

Metrics:

- restart `x_max`, `x_cutoff`, `worst_byte_index`, `worst_bit_index`
- TRNG bit min-entropy / abs bias
- TDC pair locking metrics

### H4: Raw TDC Bin Metrics Need Code-Density Calibration

Prediction:

- used bins are far below 256 in existing near/far TDC data, and many bins are dead.
- DNL/INL are large; therefore raw bin index should not be reported as linear picosecond time unless code-density calibrated.

Current evidence:

- Existing near/far runs use only about `63-73` bins out of 256.
- peak abs INL reaches about `191 LSB` in current simple code-density output.

Why it matters:

- This is a methods caveat and a reviewer-proofing point.
- For the paper, TDC is still valuable as a relative phase/bin-distribution probe, but the wording must be calibrated and careful.

Experiments:

- For each TDC capture, keep `.tdc_bins.csv` and use code-density-derived phase centers.
- Later, if time allows, add a dedicated TDC code-density calibration run not tied to a specific RO pair.

## Immediate Hardware Queue

The repeat02 queue is intended to test H1/H2 reproducibility:

| run | purpose |
| --- | --- |
| `tdc_pair_random1_ro4_ro5_repeat02_2mib` | random1 closest RO_FREQ pair repeat |
| `tdc_pair_random1_ro0_ro1_repeat02_2mib` | random1 second close pair repeat |
| `tdc_pair_random1_ro2_ro4_repeat02_2mib` | random1 extra close pair repeat |
| `tdc_pair_random3_ro3_ro7_repeat02_2mib` | random3 closest RO_FREQ pair repeat |
| `tdc_pair_random3_ro3_ro5_repeat02_2mib` | random3 extra close pair repeat |
| `tdc_pair_random3_ro0_ro6_repeat02_2mib` | random3 extra close pair repeat |

## Expected Paper Outcome

If repeat02 agrees with run01, the defensible statement is:

> Across the selected closest-frequency RO pairs in random1 and random3, TDC window analysis did not reveal strong pairwise phase locking. The observed placement-dependent TRNG quality difference is therefore better explained by placement-dependent frequency pulling, sampling relationship, and restart/startup bias rather than by a simple persistent pair-locking mechanism.

If repeat02 shows stronger windows than run01, the paper should instead say:

> Pairwise coupling is intermittent and placement/run dependent. TDC does not show universal locking, but it can reveal transient phase-correlation windows that may contribute to entropy degradation under specific RO pair placements.

## Repeat02 Results

- completed: 2026-05-23 01:02
- captures: 6 / 6 complete, each `2MiB`
- refreshed analysis:
  - `data\experiments\tdc_pair_dynamics\tdc_pair_dynamics_20260514.csv`
  - `data\experiments\paper_artifacts_20260514\table_tdc_pair_dynamics_summary.csv`
  - `doc\tdc_pair_dynamics_interpretation_20260514.md`

Repeat02 supports H1. Across run01 and repeat02, there are now `12` pair-specific TDC captures and `192` windowed records. The analyzer reports `strong_lock_windows=0`. The maximum zero-lag window phase correlation is `0.0265191`, and the maximum small-lag phase correlation remains `0.0317827`.

Representative repeat02 rows:

| run | phase_r_mean | phase_r_max_abs | best_lag_abs_r_max | diff_std_ps_mean | strong_lock_windows |
| --- | ---: | ---: | ---: | ---: | ---: |
| `tdc_pair_random1_ro4_ro5_repeat02_2mib` | -0.00294471 | 0.0265191 | 0.0265191 | 2043.21872 | 0 |
| `tdc_pair_random1_ro0_ro1_repeat02_2mib` | 0.0022153 | 0.0218069 | 0.0233717 | 2038.10867 | 0 |
| `tdc_pair_random1_ro2_ro4_repeat02_2mib` | 0.000935983 | 0.0129595 | 0.0240830 | 2039.03343 | 0 |
| `tdc_pair_random3_ro3_ro7_repeat02_2mib` | -0.000306843 | 0.0122850 | 0.0276015 | 2040.68271 | 0 |
| `tdc_pair_random3_ro3_ro5_repeat02_2mib` | 0.00272779 | 0.0210031 | 0.0270783 | 2037.46575 | 0 |
| `tdc_pair_random3_ro0_ro6_repeat02_2mib` | -0.00251103 | 0.0133606 | 0.0227691 | 2043.01228 | 0 |

Interpretation:

The repeat confirms that the tested closest-frequency RO pairs do not exhibit strong pairwise phase locking under the current board, voltage, temperature, and 2MiB capture length. This helps explain the existing placement/TRNG results in a negative-evidence way: `random1` has poor continuous TRNG entropy, but its monitored TDC pairs are not strongly locked; therefore the degradation is more plausibly tied to placement-dependent frequency pulling, sampling relationship, and/or global startup/phase structure rather than one obvious locked pair.
