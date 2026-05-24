# Sampler-Data TDC Summary

- completed metric rows: 6
- interpretation scope: raw-bin and relative comparisons only; no calibrated picosecond claims.
- caution: code-density calibration has not been applied, so `diff_std_ps` is a nominal index-derived value.

| run | family | sampler | data_ro | packets | phase_r | bin_r | diff_std_ps | A Hbin | B Hbin | XADC C |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `tdc_sampler_data_random1_baseline_sample_x36y35_ro0_2mib` | random1 | baseline | 0 | 262144 | 0.00149179 | 0.00103952 | 1978.888 | 2.79191 | 5.54099 | 46.6->46.9 |
| `tdc_sampler_data_random1_baseline_sample_x36y35_ro4_2mib` | random1 | baseline | 4 | 262143 | 0.000164971 | -5.53494e-05 | 1977.164 | 2.7263 | 5.4405 | 46.9->47.0 |
| `tdc_sampler_data_random1_local_sample_x45y39_ro0_2mib` | random1 | local | 0 | 262143 | -0.000490509 | -0.00110407 | 1978.996 | 2.77432 | 5.42345 | 47.1->46.9 |
| `tdc_sampler_data_random1_local_sample_x45y39_ro4_2mib` | random1 | local | 4 | 262144 | -0.00247228 | -0.00237726 | 1980.745 | 2.7381 | 5.60358 | 47.0->47.1 |
| `tdc_sampler_data_random3_sample_x36y35_ro0_2mib` | random3 | goodref | 0 | 262143 | 0.00224361 | 0.0025089 | 1971.942 | 2.63263 | 5.53408 | 47.1->47.2 |
| `tdc_sampler_data_random3_sample_x36y35_ro3_2mib` | random3 | goodref | 3 | 262143 | -0.00140776 | -0.00113083 | 1978.297 | 2.70502 | 5.70526 | 47.0->47.4 |

## Mechanism Reading

If baseline and local sampler variants have similar near-zero TDC correlation while TRNG entropy differs strongly, the result should be treated as a negative control against simple pairwise RO locking. It supports the stronger sampler/register/routing-path hypothesis: the sampler side is part of the entropy source, not just a passive observer.

If later rows show a clear baseline/local split in raw-bin entropy, phase correlation, or phase-difference spread, then TDC can be used as a direct physical mechanism proxy. Otherwise, keep TDC in the main paper as a boundary-setting instrument and put detailed bin tables in supplementary material.
