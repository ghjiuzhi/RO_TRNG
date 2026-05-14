# TDC Calibration and Metrics

- run: `tdc_pair_random3_ro3_ro5_run01_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random3_ro3_ro5_run01_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 4 |
| lane_a_std_phase_ps | 1442.75 |
| lane_b_std_phase_ps | 1442.59 |
| diff_std_ps | 2040.26 |
| bin_pearson_r | -0.000135991 |
| phase_pearson_r | -2.03433e-05 |
| lane_a_peak_abs_inl_lsb | 193.883 |
| lane_b_peak_abs_inl_lsb | 195 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 195 | -1 | 13.71 | 193.883 |
| B | 199 | -1 | 14.5919 | 195 |
