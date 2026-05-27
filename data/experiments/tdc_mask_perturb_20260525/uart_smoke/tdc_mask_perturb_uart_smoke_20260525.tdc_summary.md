# TDC Calibration and Metrics

- run: `tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525`
- source: `data\hardware\20260511_fpga1_board1\tdc_mask_perturb\tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525.bin`
- clock_period_ps: 10000
- bins: 128

| metric | value |
| --- | ---: |
| packets | 131071 |
| seq_gaps | 1 |
| lane_a_std_phase_ps | 2885.62 |
| lane_b_std_phase_ps | 2885.29 |
| diff_std_ps | 4082.09 |
| bin_pearson_r | -0.000634544 |
| phase_pearson_r | -0.000707329 |
| lane_a_peak_abs_inl_lsb | 63 |
| lane_b_peak_abs_inl_lsb | 63 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 67 | -1 | 5.33599 | 63 |
| B | 67 | -1 | 6.46197 | 63 |
