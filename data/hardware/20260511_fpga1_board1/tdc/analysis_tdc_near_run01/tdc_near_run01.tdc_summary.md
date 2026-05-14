# TDC Calibration and Metrics

- run: `tdc_near_run01`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc\tdc_near_run01.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 2049 |
| seq_gaps | 2048 |
| lane_a_std_phase_ps | 0 |
| lane_b_std_phase_ps | 1354.44 |
| diff_std_ps | 1354.44 |
| bin_pearson_r | 0 |
| phase_pearson_r | 0 |
| lane_a_peak_abs_inl_lsb | 157 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 255 | -1 | 255 | 157 |
| B | 197 | -1 | 101.2 | 191 |
