# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro2_ro4_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro2_ro4_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1442.6 |
| lane_b_std_phase_ps | 1442.41 |
| diff_std_ps | 2039.02 |
| bin_pearson_r | 0.000949512 |
| phase_pearson_r | 0.000965486 |
| lane_a_peak_abs_inl_lsb | 193.672 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 197 | -1 | 13.6827 | 193.672 |
| B | 195 | -1 | 15.8926 | 191 |
