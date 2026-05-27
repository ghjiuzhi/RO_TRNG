# Clean32k TDC LUT Reanalysis 20260525

## Calibration LUTs

- lane A LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_a_lut.csv`
- lane B LUT: `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_code_density_cal_20260525\tdc_code_density_cal_a7_b11_formal_8mib_20260525.lane_b_lut.csv`

## Summary

| label | packets | seq gaps | diff std ps | early diff std ps | autocorr | A/B Pearson r | raw same ratio | raw longest run |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline_warmup0 | 32768 | 0 | 1442.6369 | 1465.84272 | -0.00325471251 | -0.00936172741 | 0.0165105136 | 3 |
| random1_baseline_warmup12 | 32768 | 0 | 1431.91184 | 1389.35202 | -0.00259548461 | -0.00886479341 | 0.017670217 | 3 |
| random3_goodref_warmup0 | 32768 | 0 | 1433.09286 | 1429.95368 | -0.00752850922 | -0.00361723679 | 0.0205694754 | 3 |
| random3_goodref_warmup12 | 32768 | 0 | 1431.70779 | 1419.56559 | 0.000226070335 | -0.0047181387 | 0.0190740684 | 3 |
| random1_sampler_local_warmup0 | 32768 | 0 | 1429.51444 | 1413.12972 | -0.00133642186 | -0.00608745181 | 0.0198065126 | 3 |
| random1_sampler_local_warmup12 | 32768 | 0 | 1436.39295 | 1440.37989 | 0.00123206863 | -0.00364909543 | 0.0169377728 | 3 |

## Interpretation

- This table applies one fixed code-density LUT pair to the existing clean32k captures; it is a sensitivity check, not a full metrological calibration of every placement-specific TDC build.
- The calibrated phase-difference autocorrelation remains close to zero and the raw same-differential-bin residence indicators remain short, so the earlier conclusion against simple pairwise hard locking is not overturned by the first LUT-based reanalysis.
- The absolute `diff std ps` values should be written cautiously because the LUTs were generated on a dedicated calibration top, not interleaved immediately before and after every clean32k run.
