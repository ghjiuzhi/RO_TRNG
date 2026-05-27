# Fixed-LUT TDC Pair Dynamics Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv`

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_pair_random1_ro0_ro1_repeat02_2mib | 16 | 262143 | 0.000136162624 | 0.0243258451 | 658.924422 | 12.6275306 | 0 |
| tdc_pair_random1_ro0_ro1_run01_2mib | 16 | 262141 | -0.00226527746 | 0.0202845562 | 660.891754 | 22.8227747 | 0 |
| tdc_pair_random1_ro2_ro4_repeat02_2mib | 16 | 262143 | 0.00021728173 | 0.0311090298 | 479.542271 | 11.5603092 | 0 |
| tdc_pair_random1_ro2_ro4_run01_2mib | 16 | 262130 | -0.00185994773 | 0.0313742149 | 480.19043 | 13.156704 | 0 |
| tdc_pair_random1_ro4_ro5_repeat02_2mib | 16 | 262144 | -0.00333573391 | 0.0293993614 | 491.889432 | 14.1609623 | 0 |
| tdc_pair_random1_ro4_ro5_run01_2mib | 16 | 262143 | -0.00189804075 | 0.0260278669 | 491.349322 | 10.3176345 | 0 |
| tdc_pair_random3_ro0_ro6_repeat02_2mib | 16 | 262143 | -0.00592916298 | 0.0213851261 | 575.234433 | 14.2439007 | 0 |
| tdc_pair_random3_ro0_ro6_run01_2mib | 16 | 262142 | -0.00275612088 | 0.0241074164 | 575.317286 | 18.2090412 | 0 |
| tdc_pair_random3_ro3_ro5_repeat02_2mib | 16 | 262144 | 0.00281679826 | 0.027469613 | 444.274112 | 12.1554773 | 0 |
| tdc_pair_random3_ro3_ro5_run01_2mib | 16 | 262143 | -0.00015844973 | 0.0278676184 | 444.939024 | 12.539284 | 0 |
| tdc_pair_random3_ro3_ro7_repeat02_2mib | 16 | 262143 | -0.000115302383 | 0.0246514958 | 496.700137 | 15.4542205 | 0 |
| tdc_pair_random3_ro3_ro7_run01_2mib | 16 | 262141 | 4.11244319e-06 | 0.0233563143 | 496.61719 | 12.6371765 | 0 |

## Interpretation

- Maximum fixed-LUT small-lag `|r|`: `0.0313742149`.
- Strong-lock windows at threshold `|r| >= 0.5`: `0`.
- This is a calibration sensitivity check. It uses one external LUT pair for all pair-specific captures, so the absolute ps spread is more comparable than per-run self-calibration, but it is still not a full per-run metrology calibration.
- If the strong-lock count remains zero, the pair-specific TDC evidence continues to support the negative-control claim against simple pairwise RO hard locking.
