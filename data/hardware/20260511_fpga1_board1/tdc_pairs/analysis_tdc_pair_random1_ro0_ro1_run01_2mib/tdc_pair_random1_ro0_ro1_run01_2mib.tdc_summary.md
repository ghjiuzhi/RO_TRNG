# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro0_ro1_run01_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro0_ro1_run01_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262142 |
| seq_gaps | 67 |
| lane_a_std_phase_ps | 1442.69 |
| lane_b_std_phase_ps | 1442.82 |
| diff_std_ps | 2042.9 |
| bin_pearson_r | -0.00255348 |
| phase_pearson_r | -0.00249082 |
| lane_a_peak_abs_inl_lsb | 190.999 |
| lane_b_peak_abs_inl_lsb | 194.926 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 193 | -1 | 18.175 | 190.999 |
| B | 198 | -1 | 11.4337 | 194.926 |
