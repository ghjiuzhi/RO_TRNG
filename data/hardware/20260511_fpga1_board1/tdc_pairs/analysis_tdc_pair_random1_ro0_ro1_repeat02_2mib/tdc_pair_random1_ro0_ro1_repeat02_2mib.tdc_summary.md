# TDC Calibration and Metrics

- run: `tdc_pair_random1_ro0_ro1_repeat02_2mib`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc_pairs\tdc_pair_random1_ro0_ro1_repeat02_2mib.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1442.69 |
| lane_b_std_phase_ps | 1442.83 |
| diff_std_ps | 2038.1 |
| bin_pearson_r | 0.00221762 |
| phase_pearson_r | 0.00222641 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 194.868 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 194 | -1 | 18.1593 | 191 |
| B | 199 | -1 | 11.3633 | 194.868 |
