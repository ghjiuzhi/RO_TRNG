# TDC Code-Density Calibration Summary: tdc_code_density_cal_a7_b11_smoke_2mib_20260525

- input: `data\hardware\20260511_fpga1_board1\tdc\tdc_code_density_cal_a7_b11_smoke_2mib_20260525.bin`
- capture bytes: `2097152`
- decoded packets: `262143`
- seq gaps: `0`
- capture SHA256: `DE4E52D858D814BEA2B88AA564B51D94A35323A8D6C7D5A38ADDD6C4E736264B`
- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_smoke_2mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_smoke_2mib_20260525.lane_b_lut.csv`

## Lane Summary

| lane | used bins | dead bins | H(bin) | min-H(bin) | max DNL | min DNL | peak abs INL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 64 | 1 | 2.994386 | 1.414885 | 23.377573 | -1.000000 | 23.377573 |
| B | 64 | 1 | 2.450985 | 1.261638 | 26.109555 | -1.000000 | 26.109555 |

## Claim Boundary

This is a dedicated code-density calibration smoke, not yet the full publication calibration set. Use it to check feasibility, dead-code structure, and first-order bin-width LUT generation.
