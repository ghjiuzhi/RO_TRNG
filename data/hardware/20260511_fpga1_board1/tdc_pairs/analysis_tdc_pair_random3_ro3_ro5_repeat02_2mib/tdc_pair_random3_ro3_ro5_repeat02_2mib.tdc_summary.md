# TDC Calibration and Metrics

- run: `tdc_pair_random3_ro3_ro5_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random3_ro3_ro5_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262144 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1442.75 |
| lane_b_std_phase_ps | 1442.61 |
| diff_std_ps | 2037.49 |
| bin_pearson_r | 0.00272241 |
| phase_pearson_r | 0.00271368 |
| lane_a_peak_abs_inl_lsb | 193.949 |
| lane_b_peak_abs_inl_lsb | 195 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 195 | -1 | 13.8389 | 193.949 |
| B | 199 | -1 | 14.1191 | 195 |
