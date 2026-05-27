# Fixed-LUT TDC Pair Dynamics Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_b_lut.csv`

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro0_2mib | 16 | 262144 | 0.00103860348 | 0.0214575733 | 1355.15068 | 51.6562176 | 0 |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro4_2mib | 16 | 262143 | 0.00115404542 | 0.0214705938 | 1350.6561 | 45.7769455 | 0 |
| tdc_sampler_data_random1_local_sample_x45y39_ro0_2mib | 16 | 262143 | -0.00109738023 | 0.0219952664 | 1368.06844 | 27.1364153 | 0 |
| tdc_sampler_data_random1_local_sample_x45y39_ro4_2mib | 16 | 262144 | -0.00247114239 | 0.0204124541 | 1352.60785 | 44.7068911 | 0 |
| tdc_sampler_data_random3_sample_x36y35_ro0_2mib | 16 | 262143 | 0.00289033312 | 0.0272990321 | 1361.60588 | 34.2238105 | 0 |
| tdc_sampler_data_random3_sample_x36y35_ro3_2mib | 16 | 262143 | -0.001037825 | 0.0230930575 | 1357.88855 | 35.9906566 | 0 |

## Interpretation

- Maximum fixed-LUT small-lag `|r|`: `0.0272990321`.
- Strong-lock windows at threshold `|r| >= 0.5`: `0`.
- This is a calibration sensitivity check. It uses one external LUT pair for all pair-specific captures, so the absolute ps spread is more comparable than per-run self-calibration, but it is still not a full per-run metrology calibration.
- If the strong-lock count remains zero, the pair-specific TDC evidence continues to support the negative-control claim against simple pairwise RO hard locking.
