# TDC Code-Density Calibration Summary: tdc_code_density_cal_a7_b11_formal_8mib_20260525

- input: `data\hardware\20260511_fpga1_board1\tdc\tdc_code_density_cal_a7_b11_formal_8mib_20260525.bin`
- capture bytes: `8388608`
- decoded packets: `1048575`
- seq gaps: `0`
- capture SHA256: `FF7A25B3CBE5289A8A480A8D117C81A9C462713EB6DB7CD86183B2540A553B32`
- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv`

## Lane Summary

| lane | used bins | dead bins | H(bin) | min-H(bin) | max DNL | min DNL | peak abs INL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 64 | 1 | 3.001707 | 1.422009 | 23.257492 | -1.000000 | 23.257492 |
| B | 64 | 1 | 2.460396 | 1.261893 | 26.104766 | -1.000000 | 26.104766 |

## Claim Boundary

This is a dedicated code-density calibration smoke, not yet the full publication calibration set. Use it to check feasibility, dead-code structure, and first-order bin-width LUT generation.
