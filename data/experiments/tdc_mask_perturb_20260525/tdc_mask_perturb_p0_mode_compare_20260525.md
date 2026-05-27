# TDC Mask-Perturb P0 Summary 20260525

## Mode Comparison

| label | family | mode | packets | seq gaps | H(diff) | transition H(diff) | same ratio | longest run | autocorr | dH vs pair | dTransH vs pair |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_mask_random1_ro0_ro1_pair_only | random1 | pair_only | 1048575 | 1 | 6.686386 | 13.362153 | 0.010857 | 3 | 0.000874 | 0 | 0 |
| tdc_mask_random1_ro0_ro1_all_data_on | random1 | all_data_on | 1048575 | 1 | 6.747066 | 13.482718 | 0.010303 | 4 | -0.000932 | 0.06068 | 0.120565 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | random1 | pair_plus_sample | 1048575 | 1 | 6.646222 | 13.282559 | 0.010963 | 4 | -0.000067 | -0.040164 | -0.079593 |
| tdc_mask_random3_ro0_ro6_pair_only | random3 | pair_only | 1048575 | 1 | 6.697029 | 13.383203 | 0.010748 | 4 | 0.000729 | 0 | 0 |
| tdc_mask_random3_ro0_ro6_all_data_on | random3 | all_data_on | 1048575 | 1 | 5.982632 | 11.96249 | 0.016026 | 4 | -0.001284 | -0.714397 | -1.420713 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | random1_local_sample | pair_plus_sample | 1048575 | 1 | 6.668195 | 13.325698 | 0.01106 | 4 | -0.000176 |  |  |

## Interpretation

- All six 8 MiB captures completed and decode to 1,048,575 TDC packets each. The one sequence gap per run is consistent with pre-open capture alignment at stream boundaries.
- Random1 RO0/RO1 changes only mildly across pair-only, all-data-on, and pair-plus-sample modes. This suggests that for this bad-reference pair, local switching perturbation does not create a simple locking signature.
- Random3 RO0/RO6 shows a strong all-data-on effect: H(diff) and transition H(diff) drop substantially relative to pair-only, while lag autocorrelation remains near zero and longest residence is only four packets.
- This supports a mechanism distinction: enabling neighboring RO activity can reshape phase/bin distributions without producing pairwise hard locking.
- The result should be linked with RO_FREQ pulling and restart behavior, but should not be written as absolute ps-level metrology because the TDC LUT is still placement/top dependent.
