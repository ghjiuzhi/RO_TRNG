# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro2_ro4_run01_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro2_ro4_run01_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262138 |
| seq_gaps | 122 |
| lane_a_std_phase_ps | 1442.6 |
| lane_b_std_phase_ps | 1442.41 |
| diff_std_ps | 2042.29 |
| bin_pearson_r | -0.00118267 |
| phase_pearson_r | -0.00223673 |
| lane_a_peak_abs_inl_lsb | 193.694 |
| lane_b_peak_abs_inl_lsb | 190.992 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 194 | -1 | 13.5501 | 193.694 |
| B | 189 | -1 | 15.9301 | 190.992 |
