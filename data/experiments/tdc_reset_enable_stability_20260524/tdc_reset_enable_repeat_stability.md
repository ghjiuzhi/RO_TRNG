# TDC Reset-Enable Repeat Stability

This table merges reset-enable TDC startup-diffusion summaries across repeats.
It uses raw TDC bins only; no ps-level calibration is claimed.

## Per-Run Metrics

| placement | repeat | edge | post packets | H(diff) | early H(diff) | warmup H(diff) | transition H(diff) | same ratio | longest run | autocorr |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline | repeat01 | 9595 | 252548 | 6.67227 | 6.54038 | 6.54209 | 13.2961 | 0.011344 | 4 | -0.001179 |
| random1_baseline | repeat02 | 5701 | 256442 | 6.67673 | 6.55711 | 6.55446 | 13.3062 | 0.011597 | 4 | -0.001494 |
| random1_baseline_ro4 | repeat01 | 9293 | 252850 | 6.60639 | 6.47378 | 6.47196 | 13.1670 | 0.012541 | 3 | 0.000597 |
| random1_baseline_ro4 | repeat02 | 9234 | 252909 | 6.60514 | 6.50542 | 6.50871 | 13.1651 | 0.012305 | 4 | -0.000544 |
| random1_sampler_local | repeat01 | 9644 | 252499 | 6.71817 | 6.60532 | 6.60266 | 13.3895 | 0.010959 | 3 | -0.000525 |
| random1_sampler_local | repeat02 | 9141 | 253002 | 6.71952 | 6.64656 | 6.64163 | 13.3913 | 0.010696 | 3 | -0.000126 |
| random1_sampler_local_ro4 | repeat01 | 9388 | 252756 | 6.70052 | 6.63186 | 6.63209 | 13.3568 | 0.011046 | 3 | 0.002082 |
| random1_sampler_local_ro4 | repeat02 | 9498 | 252645 | 6.70189 | 6.63041 | 6.63395 | 13.3589 | 0.010952 | 4 | 0.001350 |
| random3_goodref | repeat01 | 9582 | 252561 | 6.69450 | 6.58148 | 6.58243 | 13.3466 | 0.010995 | 3 | 0.000273 |
| random3_goodref | repeat02 | 7743 | 254400 | 6.69607 | 6.63509 | 6.64063 | 13.3488 | 0.010853 | 3 | 0.001043 |
| random3_goodref_ro3 | repeat01 | 9869 | 252274 | 6.67248 | 6.54411 | 6.54869 | 13.2987 | 0.011384 | 4 | 0.000386 |
| random3_goodref_ro3 | repeat02 | 9944 | 252199 | 6.67484 | 6.55376 | 6.54804 | 13.3026 | 0.011277 | 3 | -0.002068 |

## Repeat Means

| placement | repeats | mean H(diff) | mean early H(diff) | mean warmup H(diff) | mean transition H(diff) | mean same ratio | max longest run |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline | 2 | 6.67450 | 6.54875 | 6.54827 | 13.3012 | 0.011471 | 4 |
| random1_baseline_ro4 | 2 | 6.60577 | 6.48960 | 6.49033 | 13.1661 | 0.012423 | 4 |
| random1_sampler_local | 2 | 6.71884 | 6.62594 | 6.62214 | 13.3904 | 0.010827 | 3 |
| random1_sampler_local_ro4 | 2 | 6.70120 | 6.63113 | 6.63302 | 13.3578 | 0.010999 | 4 |
| random3_goodref | 2 | 6.69528 | 6.60829 | 6.61153 | 13.3477 | 0.010924 | 3 |
| random3_goodref_ro3 | 2 | 6.67366 | 6.54893 | 6.54837 | 13.3007 | 0.011331 | 4 |

## Interpretation

- In the two completed RO0 repeats, `random1_baseline` is consistently lower than `random1_sampler_local` in differential-bin entropy.
- The RO4 contrast is stronger and repeats cleanly: `random1_baseline_ro4` remains about 0.095 bit lower than `random1_sampler_local_ro4` in mean H(diff), and about 0.142 bit lower in mean early H(diff).
- `random3_goodref_ro3` is lower than `random3_goodref_ro0`, which shows that startup diffusion also depends on the specific data-RO/sampler geometry, not only the placement family label.
- Autocorrelation remains close to zero and longest residence runs are short, so the result still does not support a strong hard-locking explanation.
- This upgrades reset-enable TDC from a purely negative-control result to repeatable weak-positive evidence that sampler/data geometry changes startup phase-diffusion behavior.
- The strongest paper wording is causal by combination: sampler-side relocation repairs TRNG output, while reset-enable TDC shows matching startup-diffusion changes without hard locking.
