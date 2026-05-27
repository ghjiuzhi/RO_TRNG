# TDC Calibration and Metrics

- run: `tdc_reset_random1_baseline_ro0_smoke_warmup0_preopen_20260525`
- source: `data\hardware\20260511_fpga1_board1\tdc_reset_aligned\tdc_reset_random1_baseline_ro0_smoke_warmup0_preopen_20260525.bin`
- clock_period_ps: 10000
- bins: 128

| metric | value |
| --- | ---: |
| packets | 64 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 2781.74 |
| lane_b_std_phase_ps | 2905.75 |
| diff_std_ps | 4024.21 |
| bin_pearson_r | -0.0470685 |
| phase_pearson_r | -0.000791057 |
| lane_a_peak_abs_inl_lsb | 63 |
| lane_b_peak_abs_inl_lsb | 63 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 108 | -1 | 51 | 63 |
| B | 95 | -1 | 11 | 63 |
