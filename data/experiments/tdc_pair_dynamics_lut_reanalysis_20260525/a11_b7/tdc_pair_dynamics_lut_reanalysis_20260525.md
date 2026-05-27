# Fixed-LUT TDC Pair Dynamics Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_b_lut.csv`

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_pair_random1_ro0_ro1_repeat02_2mib | 16 | 262143 | -0.000801167818 | 0.0236574354 | 620.341147 | 11.4687365 | 0 |
| tdc_pair_random1_ro0_ro1_run01_2mib | 16 | 262141 | -0.00192155613 | 0.0220964105 | 622.023951 | 20.6107335 | 0 |
| tdc_pair_random1_ro2_ro4_repeat02_2mib | 16 | 262143 | 0.00047430128 | 0.0296831846 | 495.73364 | 10.8487021 | 0 |
| tdc_pair_random1_ro2_ro4_run01_2mib | 16 | 262130 | -0.00211796792 | 0.0313610782 | 495.780325 | 14.4230035 | 0 |
| tdc_pair_random1_ro4_ro5_repeat02_2mib | 16 | 262144 | -0.00308101541 | 0.0295551034 | 489.820154 | 14.1780899 | 0 |
| tdc_pair_random1_ro4_ro5_run01_2mib | 16 | 262143 | -0.00234032681 | 0.0260810274 | 489.445869 | 11.1325971 | 0 |
| tdc_pair_random3_ro0_ro6_repeat02_2mib | 16 | 262143 | -0.00474709757 | 0.0224031288 | 589.570859 | 15.5171756 | 0 |
| tdc_pair_random3_ro0_ro6_run01_2mib | 16 | 262142 | -0.00157337392 | 0.0252497088 | 589.814627 | 18.7693108 | 0 |
| tdc_pair_random3_ro3_ro5_repeat02_2mib | 16 | 262144 | 0.00256070145 | 0.0267041267 | 432.192248 | 9.8977798 | 0 |
| tdc_pair_random3_ro3_ro5_run01_2mib | 16 | 262143 | -0.000166441558 | 0.0286362018 | 432.552743 | 14.669347 | 0 |
| tdc_pair_random3_ro3_ro7_repeat02_2mib | 16 | 262143 | 0.000108338976 | 0.0226081026 | 476.273773 | 15.6969958 | 0 |
| tdc_pair_random3_ro3_ro7_run01_2mib | 16 | 262141 | 0.00017665404 | 0.0234010145 | 476.004329 | 11.1526932 | 0 |

## Interpretation

- Maximum fixed-LUT small-lag `|r|`: `0.0313610782`.
- Strong-lock windows at threshold `|r| >= 0.5`: `0`.
- This is a calibration sensitivity check. It uses one external LUT pair for all pair-specific captures, so the absolute ps spread is more comparable than per-run self-calibration, but it is still not a full per-run metrology calibration.
- If the strong-lock count remains zero, the pair-specific TDC evidence continues to support the negative-control claim against simple pairwise RO hard locking.
