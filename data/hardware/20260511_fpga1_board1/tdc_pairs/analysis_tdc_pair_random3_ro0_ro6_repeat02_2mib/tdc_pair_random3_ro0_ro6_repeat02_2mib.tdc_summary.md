# TDC Calibration and Metrics

- run: `tdc_pair_random3_ro0_ro6_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random3_ro0_ro6_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1442.93 |
| lane_b_std_phase_ps | 1442.72 |
| diff_std_ps | 2043.04 |
| bin_pearson_r | -0.00240622 |
| phase_pearson_r | -0.00252742 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 193 | -1 | 10.0645 | 191 |
| B | 192 | -1 | 14.5967 | 191 |
