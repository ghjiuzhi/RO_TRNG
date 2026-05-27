# Fixed-LUT TDC Pair Dynamics Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv`

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro0_2mib | 16 | 262144 | 0.000640955512 | 0.0210209763 | 1419.93511 | 50.9552324 | 0 |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro4_2mib | 16 | 262143 | 0.00151656395 | 0.0204740687 | 1428.80619 | 44.0117361 | 0 |
| tdc_sampler_data_random1_local_sample_x45y39_ro0_2mib | 16 | 262143 | -0.00143358855 | 0.0222326552 | 1425.79178 | 28.2624655 | 0 |
| tdc_sampler_data_random1_local_sample_x45y39_ro4_2mib | 16 | 262144 | -0.00240669346 | 0.02056795 | 1430.3628 | 46.4826557 | 0 |
| tdc_sampler_data_random3_sample_x36y35_ro0_2mib | 16 | 262143 | 0.00314801023 | 0.0272195217 | 1440.27198 | 34.7780534 | 0 |
| tdc_sampler_data_random3_sample_x36y35_ro3_2mib | 16 | 262143 | -0.000725409625 | 0.0229971378 | 1434.21446 | 38.4004041 | 0 |

## Interpretation

- Maximum fixed-LUT small-lag `|r|`: `0.0272195217`.
- Strong-lock windows at threshold `|r| >= 0.5`: `0`.
- This is a calibration sensitivity check. It uses one external LUT pair for all pair-specific captures, so the absolute ps spread is more comparable than per-run self-calibration, but it is still not a full per-run metrology calibration.
- If the strong-lock count remains zero, the pair-specific TDC evidence continues to support the negative-control claim against simple pairwise RO hard locking.
