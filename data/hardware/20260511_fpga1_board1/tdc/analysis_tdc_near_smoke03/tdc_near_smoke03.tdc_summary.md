# TDC Calibration and Metrics

- run: `tdc_near_smoke03`
- source: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\tdc\tdc_near_smoke03.bin`
- clock_period_ps: 5000
- bins: 256

| metric | value |
| --- | ---: |
| packets | 127 |
| seq_gaps | 0 |
| lane_a_std_phase_ps | 1376.79 |
| lane_b_std_phase_ps | 1368.45 |
| diff_std_ps | 1979.24 |
| bin_pearson_r | -0.0232999 |
| phase_pearson_r | -0.0395868 |
| lane_a_peak_abs_inl_lsb | 191 |
| lane_b_peak_abs_inl_lsb | 191 |

## Code-Density Extremes

| lane | dead_bins | min_dnl_lsb | max_dnl_lsb | peak_abs_inl_lsb |
| --- | ---: | ---: | ---: | ---: |
| A | 230 | -1 | 99.7874 | 191 |
| B | 228 | -1 | 97.7717 | 191 |
