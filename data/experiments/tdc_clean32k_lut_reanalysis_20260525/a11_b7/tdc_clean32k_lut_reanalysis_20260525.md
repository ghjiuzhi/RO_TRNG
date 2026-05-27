# Clean32k TDC LUT Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a11_b7_formal_8mib_20260525.lane_b_lut.csv`

## Summary

| label | packets | seq gaps | diff std ps | early diff std ps | autocorr | A/B Pearson r | raw same ratio | raw longest run |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline_warmup0 | 32768 | 0 | 1369.47189 | 1398.09982 | -0.00392754518 | -0.0089395034 | 0.0165105136 | 3 |
| random1_baseline_warmup12 | 32768 | 0 | 1359.47929 | 1313.92821 | -0.00295439584 | -0.00983149438 | 0.017670217 | 3 |
| random3_goodref_warmup0 | 32768 | 0 | 1348.38751 | 1336.55046 | -0.00789508765 | -0.00346917573 | 0.0205694754 | 3 |
| random3_goodref_warmup12 | 32768 | 0 | 1348.86492 | 1336.34137 | -0.00124950606 | -0.00442152501 | 0.0190740684 | 3 |
| random1_sampler_local_warmup0 | 32768 | 0 | 1353.43184 | 1330.43214 | -0.00220025947 | -0.00464022847 | 0.0198065126 | 3 |
| random1_sampler_local_warmup12 | 32768 | 0 | 1360.30119 | 1356.29557 | 0.00249933715 | -0.00353253614 | 0.0169377728 | 3 |

## Interpretation

- This table applies one fixed code-density LUT pair to the existing clean32k captures; it is a sensitivity check, not a full metrological calibration of every placement-specific TDC build.
- The calibrated phase-difference autocorrelation remains close to zero and the raw same-differential-bin residence indicators remain short, so the earlier conclusion against simple pairwise hard locking is not overturned by the first LUT-based reanalysis.
- The absolute `diff std ps` values should be written cautiously because the LUTs were generated on a dedicated calibration top, not interleaved immediately before and after every clean32k run.
