# TDC Code-Density Calibration Comparison 20260525

## Summary Table

| label | lane | bytes | packets | seq gaps | temp C | used/dead bins | H(bin) | min-H(bin) | max DNL | peak abs INL |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_code_density_cal_a11_b7_formal_8mib_20260525 | A | 8388608 | 1048575 | 0 | 47.2 | 63/2 | 2.39701 | 1.24577 | 26.4094 | 26.4094 |
| tdc_code_density_cal_a11_b7_formal_8mib_20260525 | B | 8388608 | 1048575 | 0 | 47.2 | 64/1 | 3.11855 | 1.46653 | 22.5204 | 22.5204 |
| tdc_code_density_cal_a7_b11_formal_8mib_20260525 | A | 8388608 | 1048575 | 0 | 46.9 | 64/1 | 3.00171 | 1.42201 | 23.2575 | 23.2575 |
| tdc_code_density_cal_a7_b11_formal_8mib_20260525 | B | 8388608 | 1048575 | 0 | 46.9 | 64/1 | 2.4604 | 1.26189 | 26.1048 | 26.1048 |
| tdc_code_density_cal_a7_b11_smoke_2mib_20260525 | A | 2097152 | 262143 | 0 |  | 64/1 | 2.99439 | 1.41489 | 23.3776 | 23.3776 |
| tdc_code_density_cal_a7_b11_smoke_2mib_20260525 | B | 2097152 | 262143 | 0 |  | 64/1 | 2.45099 | 1.26164 | 26.1096 | 26.1096 |

## Interpretation

- The 8 MiB formal calibration captures decode cleanly with zero sequence gaps.
- The lane-swap run reverses the high-entropy lane tendency: `a7/b11` has the higher-entropy A lane, while `a11/b7` has the higher-entropy B lane. This is consistent with calibration nonlinearity being tied to the driven lane/RO implementation rather than a PC-side parser artifact.
- Every run still has dead codes and large DNL/INL, so raw TDC bins must remain relative indicators unless the generated LUTs are explicitly applied.
- XADC after-capture readings place the formal calibration runs near 47 C with nominal VCCINT around 1.000 V.
