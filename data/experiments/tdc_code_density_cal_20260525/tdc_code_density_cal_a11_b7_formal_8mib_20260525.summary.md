# TDC Code-Density Calibration Summary: tdc_code_density_cal_a11_b7_formal_8mib_20260525

- input: `data\hardware\20260511_fpga1_board1\tdc\tdc_code_density_cal_a11_b7_formal_8mib_20260525.bin`
- capture bytes: `8388608`
- decoded packets: `1048575`
- seq gaps: `0`
- capture SHA256: `1F4B6EA436524ABC500B5DCAB979D149E601EF383B2784C982870F645C26F415`
- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_b_lut.csv`

## Lane Summary

| lane | used bins | dead bins | H(bin) | min-H(bin) | max DNL | min DNL | peak abs INL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 63 | 2 | 2.397010 | 1.245767 | 26.409441 | -1.000000 | 26.409441 |
| B | 64 | 1 | 3.118547 | 1.466528 | 22.520382 | -1.000000 | 22.520382 |

## Claim Boundary

This is a dedicated code-density calibration smoke, not yet the full publication calibration set. Use it to check feasibility, dead-code structure, and first-order bin-width LUT generation.
