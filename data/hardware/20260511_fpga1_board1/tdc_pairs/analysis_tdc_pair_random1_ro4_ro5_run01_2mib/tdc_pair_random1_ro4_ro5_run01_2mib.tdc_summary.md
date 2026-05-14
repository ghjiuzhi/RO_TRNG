# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro4_ro5_run01_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro4_ro5_run01_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 124 |
| lane_a_std_phase_ps | 1442.89 |
| lane_b_std_phase_ps | 1442.51 |
| diff_std_ps | 2041.51 |
| bin_pearson_r | -0.00117702 |
| phase_pearson_r | -0.00119466 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 194.979 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 195 | -1 | 10.8018 | 191 |
| B | 196 | -1 | 16.6309 | 194.979 |
