# TDC Calibration and Metrics

- run: `tdc_pair_random3_ro3_ro7_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random3_ro3_ro7_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1442.82 |
| lane_b_std_phase_ps | 1442.75 |
| diff_std_ps | 2040.71 |
| bin_pearson_r | -0.000270505 |
| phase_pearson_r | -0.000303672 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 194 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 194 | -1 | 10.6407 | 191 |
| B | 197 | -1 | 14.2149 | 194 |
