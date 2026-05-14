# TDC Calibration and Metrics

- run: `tdc_far_run01`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc\tdc_far_run01.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262132 |
| seq_gaps | 43 |
| lane_a_std_phase_ps | 1350.52 |
| lane_b_std_phase_ps | 1361.22 |
| diff_std_ps | 1915.29 |
| bin_pearson_r | 0.00292773 |
| phase_pearson_r | 0.00230247 |
| lane_a_peak_abs_inl_lsb | 190.988 |
| lane_b_peak_abs_inl_lsb | 190.986 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 183 | -1 | 102.269 | 190.988 |
| B | 183 | -1 | 96.6373 | 190.986 |
