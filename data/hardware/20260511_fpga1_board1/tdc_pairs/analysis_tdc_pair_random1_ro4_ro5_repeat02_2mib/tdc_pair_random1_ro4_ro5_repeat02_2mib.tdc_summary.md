# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro4_ro5_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro4_ro5_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262144 |
| seq_gaps | 10 |
| lane_a_std_phase_ps | 1442.9 |
| lane_b_std_phase_ps | 1442.49 |
| diff_std_ps | 2043.25 |
| bin_pearson_r | -0.00299421 |
| phase_pearson_r | -0.00290955 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 194.957 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 195 | -1 | 10.3975 | 191 |
| B | 196 | -1 | 17.0078 | 194.957 |
