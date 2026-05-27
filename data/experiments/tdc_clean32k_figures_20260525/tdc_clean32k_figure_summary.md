# Clean Reset-Aligned TDC Figure Summary 20260525

## Generated Artifacts

- `fig_tdc_clean32k_entropy.png`
- `fig_tdc_clean32k_entropy.svg`
- `fig_tdc_clean32k_hard_lock_indicators.png`
- `fig_tdc_clean32k_hard_lock_indicators.svg`
- `fig_tdc_clean32k_window_entropy.png`
- `fig_tdc_clean32k_window_entropy.svg`
- `tdc_clean32k_main_metrics.csv`
- `tdc_clean32k_warmup_deltas.csv`
- `tdc_clean32k_window_stats.csv`

## Main Metrics

| label                          |   tdcr_header_found |   tdcr_pair_id |   tdcr_warmup_packets |   tdcr_capture_packets |   post_enable_packets |   entropy_diff |   early_entropy_diff |   transition_entropy_diff |   same_diff_transition_ratio |   longest_same_diff_bin_run |   autocorr_diff_lag |   first_later_tvd_diff |
|:-------------------------------|--------------------:|---------------:|----------------------:|-----------------------:|----------------------:|---------------:|---------------------:|--------------------------:|-----------------------------:|----------------------------:|--------------------:|-----------------------:|
| random1_baseline_warmup0       |                   1 |           1501 |                     0 |                  32768 |                 32768 |        6.75886 |              6.53655 |                   13.1434 |                   0.00994903 |                           3 |        -0.0082803   |              0.0682199 |
| random1_baseline_warmup12      |                   1 |           1502 |                    12 |                  32768 |                 32768 |        6.66619 |              6.44347 |                   12.9741 |                   0.0116581  |                           3 |         3.71515e-06 |              0.0660575 |
| random3_goodref_warmup0        |                   1 |           1503 |                     0 |                  32768 |                 32768 |        6.61583 |              6.43642 |                   12.8973 |                   0.0131535  |                           3 |        -0.00921983  |              0.0677665 |
| random3_goodref_warmup12       |                   1 |           1504 |                    12 |                  32768 |                 32768 |        6.60778 |              6.46444 |                   12.8768 |                   0.0129398  |                           3 |        -0.00613231  |              0.0748465 |
| random1_sampler_local_warmup0  |                   1 |           1505 |                     0 |                  32768 |                 32768 |        6.65464 |              6.43888 |                   12.9439 |                   0.0130314  |                           3 |        -0.000825613 |              0.0567104 |
| random1_sampler_local_warmup12 |                   1 |           1506 |                    12 |                  32768 |                 32768 |        6.73356 |              6.50239 |                   13.0993 |                   0.010651   |                           3 |         0.00185527  |              0.0721261 |

## Warmup12 - Warmup0 Deltas

| placement             |   delta_entropy_diff_w12_minus_w0 |   delta_early_entropy_diff_w12_minus_w0 |   delta_transition_entropy_diff_w12_minus_w0 |   delta_same_ratio_w12_minus_w0 |
|:----------------------|----------------------------------:|----------------------------------------:|---------------------------------------------:|--------------------------------:|
| random1_baseline      |                       -0.0926714  |                              -0.0930802 |                                   -0.169239  |                      0.00170904 |
| random1_sampler_local |                        0.0789216  |                               0.0635086 |                                    0.155408  |                     -0.00238044 |
| random3_goodref       |                       -0.00805282 |                               0.028014  |                                   -0.0204793 |                     -0.00021363 |

## Window Stability

| label                          |   entropy_diff_mean |   entropy_diff_std |   transition_entropy_diff_mean |   same_diff_transition_ratio_mean |   autocorr_diff_lag_mean |   diff_std_bin_mean |
|:-------------------------------|--------------------:|-------------------:|-------------------------------:|----------------------------------:|-------------------------:|--------------------:|
| random1_baseline_warmup0       |             6.74005 |          0.0130116 |                        11.6078 |                        0.00995116 |             -0.00838888  |             35.6668 |
| random1_baseline_warmup12      |             6.64761 |          0.0111587 |                        11.5368 |                        0.0116606  |             -0.000215307 |             35.4929 |
| random3_goodref_warmup0        |             6.59667 |          0.0158121 |                        11.5127 |                        0.0131563  |             -0.00927264  |             34.2299 |
| random3_goodref_warmup12       |             6.5891  |          0.0154177 |                        11.4979 |                        0.0129426  |             -0.00625929  |             34.4189 |
| random1_sampler_local_warmup0  |             6.63592 |          0.0119874 |                        11.517  |                        0.0130342  |             -0.000869212 |             35.1773 |
| random1_sampler_local_warmup12 |             6.71267 |          0.0150222 |                        11.5927 |                        0.0106532  |              0.0018041   |             35.186  |

## Paper Interpretation

- All six clean captures have `TDCR` headers and 32768 post-enable packets, so they are defensible reset/header-aligned TDC data.
- Same-differential-bin transition ratios stay near 1%, longest same-bin runs are 3, and lag-1 autocorrelation is near zero; this supports a negative-control claim against simple pairwise hard locking.
- `random1_sampler_local_warmup12` has the strongest clean TDC entropy numbers in this matrix, but the effect is modest. Treat it as weak positive mechanism evidence, not as the primary causal proof.
- No code-density calibration has been applied; use raw-bin relative comparisons only, not absolute ps-level jitter claims.
