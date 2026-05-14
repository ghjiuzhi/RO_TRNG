# TDC Calibration and Metrics

- run: `tdc_near_smoke_direct01`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc\tdc_near_smoke_direct01.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 127 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1354.19 |
| lane_b_std_phase_ps | 1369.86 |
| diff_std_ps | 1881.2 |
| bin_pearson_r | 0.0612823 |
| phase_pearson_r | 0.0462028 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 232 | -1 | 105.835 | 191 |
| B | 229 | -1 | 105.835 | 191 |
