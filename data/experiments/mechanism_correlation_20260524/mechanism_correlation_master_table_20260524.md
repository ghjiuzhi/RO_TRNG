# Mechanism Correlation Master Table 20260524

This offline table combines placement-level TRNG, restart, RO_FREQ, pair-TDC, reset-enable TDC, sampler-ablation, and XADC summaries.

## Key Finding Added Today

- Reset-enable TDC now has repeatable positive evidence, not only a negative-control role.
- RO0: sampler-local has higher startup differential-bin entropy than baseline across two repeats.
- RO4: the contrast is stronger and repeats cleanly; sampler-local improves mean early H(diff) by about 0.142 bit over baseline.
- Residence and autocorrelation remain small, so this still argues against simple hard locking.
- Stronger causal ablation: regs-only keeps the sample RO at baseline but moves only sampling registers; 20MiB p1=0.499810 and bit min-entropy=0.999451.
- New restart contrast: the same regs-only variant has a non-monotonic restart warmup passband. Warmup 5/6/8/10 passed, while 0/4/11/12/16 failed.

## Selected Rows

| placement | cont. min-H | restart status | reset TDC runs | reset TDC early H(diff) | sampler regs-only min-H | claim | XADC ok/missing |
| --- | ---: | --- | ---: | ---: | ---: | --- | --- |
| checker | 0.999685735936 | failed;passed |  |  |  |  | 3/11 |
| compact | 0.999969731371 | failed;passed |  |  |  |  | 3/11 |
| random1 | 0.596441734915 | passed |  |  | 0.9994511186059211 | regs-only sampler-register placement nearly fixes random1 continuous output | 19/31 |
| random3 | 0.999754962731 | failed;passed |  |  |  |  | 8/79 |
| same_column | 0.999766707199 | failed;passed |  |  |  |  | 3/11 |
| sparse | 0.897989443942 | failed;passed |  |  |  |  | 3/11 |
| random1_baseline |  |  | 2 | 6.548746895 |  | sampler-local minus baseline: delta H(diff)=0.04434, delta early H(diff)=0.07719 |  |
| random1_baseline_ro4 |  |  | 2 | 6.48959856 |  | sampler-local minus baseline: delta H(diff)=0.09543, delta early H(diff)=0.14153 |  |
| random1_sampler_local |  |  | 2 | 6.62593627 |  | sampler-local minus baseline: delta H(diff)=0.04434, delta early H(diff)=0.07719 |  |
| random1_sampler_local_ro4 |  |  | 2 | 6.631133355 |  | sampler-local minus baseline: delta H(diff)=0.09543, delta early H(diff)=0.14153 |  |
| random3_goodref |  |  | 2 | 6.60828515 |  | startup diffusion measured; no hard-lock residence |  |
| random1_sampler_regs_only_x45y31 | 0.9994511186059211 | w0_run01_lsb=failed;w0_run01_msb=failed;w0_run02_lsb=failed;w0_run02_msb=failed;w4_repeat02_lsb=failed;w4_repeat02_msb=failed;w4_sweep01_lsb=failed;w4_sweep01_msb=failed;w5_edge01_lsb=passed;w5_edge01_msb=passed;w5_repeat02_lsb=passed;w5_repeat02_msb=passed;w6_passband01_lsb=passed;w6_passband01_msb=passed;w6_repeat02_lsb=passed;w6_repeat02_msb=passed;w8_repeat02_lsb=passed;w8_repeat02_msb=passed;w8_sweep01_lsb=passed;w8_sweep01_msb=passed;w10_passband01_lsb=passed;w10_passband01_msb=passed;w10_repeat02_lsb=passed;w10_repeat02_msb=passed;w11_edge01_lsb=failed;w11_edge01_msb=failed;w11_repeat02_lsb=failed;w11_repeat02_msb=failed;w12_run01_lsb=failed;w12_run01_msb=failed;w12_run02_lsb=failed;w12_run02_msb=failed;w16_sweep01_lsb=failed;w16_sweep01_msb=failed |  |  | 0.9994511186059211 | regs-only fixes continuous bias and exposes non-monotonic restart warmup passband | 34/0 |

## Inputs

- `E:\Project\MLDSA\RO_TRNG\data\experiments\mechanism_hypothesis_20260523\mechanism_hypothesis_evidence_by_placement.csv`
- `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_reset_enable_stability_20260524\tdc_reset_enable_repeat_stability.csv`
- `E:\Project\MLDSA\RO_TRNG\data\experiments\xadc_summary\xadc_capture_summary_20260523.csv`
- `E:\Project\MLDSA\RO_TRNG\data\experiments\sampler_regs_only_20260524\random1_sampler_ablation_extended_summary_20260524.csv`

## Claim Boundary

- Raw TDC bins are relative indicators; no ps-level calibrated jitter claim is made here.
- Reset-enable TDC supports startup diffusion differences; regs-only sampler-register ablation is the stronger causal evidence for sampler-path entropy-source boundary.
