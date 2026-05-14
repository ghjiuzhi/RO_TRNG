# TDC Calibration and Metrics

- run: `tdc_near_run02`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc\tdc_near_run02.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 262143 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1350.48 |
| lane_b_std_phase_ps | 1379.85 |
| diff_std_ps | 1927.59 |
| bin_pearson_r | 0.00321445 |
| phase_pearson_r | 0.00327627 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 193 | -1 | 101.94 | 191 |
| B | 193 | -1 | 90.9388 | 191 |
