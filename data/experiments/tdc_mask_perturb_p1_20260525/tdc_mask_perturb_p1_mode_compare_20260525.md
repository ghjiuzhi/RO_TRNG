# TDC Mask-Perturb P1 Summary 20260525

## Mechanism Answer

P1 directly tests whether the strong `random3 all_data_on` effect from P0 is reproducible, and whether it can be explained by a local neighbor subset or by enabling the sample RO alone.

The answer is now more specific: the all-data-on collapse is reproducible, while `neighbors_on` and `pair_plus_sample` stay much closer to pair-only. This narrows the mechanism from generic local perturbation to a full data-RO switching/load condition. The effect still does not look like hard locking because autocorrelation remains near zero and the longest same-bin run is only 4.

## Mode Comparison Against P0 Pair-Only Baseline

| label | family | mode | H(diff) | dH vs pair | transition H(diff) | dTH vs pair | same ratio | longest run | autocorr | XADC C | interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | random3 | all_data_on | 5.982072 | -0.714957 | 11.961317 | -1.421886 | 0.015947 | 4 | 0.000826 | 46.3 | replicated strong all-data switching effect without hard-lock signature |
| tdc_mask_random3_ro0_ro6_neighbors_on | random3 | neighbors_on | 6.64861 | -0.048419 | 13.287046 | -0.096157 | 0.011174 | 4 | -0.000818 | 46.5 | does not reproduce all-data collapse; points away from this mode as sole cause |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | random3 | pair_plus_sample | 6.626333 | -0.070696 | 13.24272 | -0.140483 | 0.011338 | 4 | 0.000281 | 46.0 | does not reproduce all-data collapse; points away from this mode as sole cause |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | random1_local_sample | pair_only | 6.698993 | 0.012607 | 13.387138 | 0.024985 | 0.01067 | 4 | -0.001635 | 46.3 | local-sample pair-only baseline remains non-locking |

## Paper Use

- Stronger claim now allowed: the `random3 all_data_on` TDC entropy/transition-entropy collapse replicated in a second 8MiB capture.
- Mechanism narrowed: a neighbor subset and sample-RO-only activation do not reproduce the collapse, so the observed effect is tied to full data-RO simultaneous switching/load rather than a single nearby RO or sample RO alone.
- Boundary remains careful: this is raw-bin relative TDC evidence. It supports local switching/load perturbation and excludes hard locking; it is not absolute ps-level jitter metrology.
