# TDC 机制推断汇总 2026-05-25

## 结论先行

本表把 TDC mask-perturb、reset-aligned TDC、RO_FREQ、TRNG/restart 结果放在同一条证据链里。当前最稳的写法不是“坏 placement 来自 RO-RO 锁定”，而是：TDC 多次排除了 hard-lock signature；同时 mask-perturb 显示局部 RO 开关活动能改变 TDC phase/bin 扩散；再结合 sample-RO 双向反事实，更合理的机制是 sampler-side physical implementation 参与熵源边界。

## 假设状态

| Hypothesis | Status | Evidence | Paper use | Next test |
| --- | --- | --- | --- | --- |
| H1: simple RO-RO hard locking is not dominant | supported as exclusion/control evidence | 16/16 rows show no hard-lock signature by autocorr/residence/same-ratio thresholds | Write TDC as a falsification layer, not as proof of locking. | Only repeat if a future mode produces autocorr/residence anomalies. |
| H2: local switching/load activity can reshape phase-bin diffusion | supported for at least one placement/mode | random3 all_data_on ΔH=-0.714397 ΔTH=-1.42071; random3 all_data_on ΔH=-0.714957 ΔTH=-1.42189 | Use as positive TDC evidence that RO-group activity changes delay/phase statistics without hard locking. | P1 already replicated all-data-on and checked neighbor/sample-only controls; next best test is RO_FREQ all-on/single-on or cross-board replication. |
| H3: restart startup bias is related to short-time phase diffusion, but not fully explained by pair TDC | partially supported / bounded | Reset-aligned TDC has no hard-lock signature; sampler-local warmup12 is best among clean32k rows, while restart still shows warmup passbands and packing-dependent fixed-position bias. | Argue that startup transient exists, but the dominant boundary includes sampler path and bit-position sampling, not only RO pair phase. | Run sample-only and sample+regs-local restart passband warmups 4/5/10/11 already built. |
| H4: sampler-side physical implementation is part of the entropy-source boundary | strongly supported by counterfactuals; TDC is a supporting constraint | 3 TDC rows are consistent with non-locking sampler-side perturbation; sample-RO forward/reverse restart counterfactuals provide the stronger causal evidence. | Main paper claim: sampling circuit is not a passive readout; it belongs inside the physical entropy-source boundary. | Prioritize sampler-only vs regs-only restart/continuous ablation over more same-pair TDC repeats. |

## 关键 TDC 行

| Layer | Family | Mode | H(diff) | ΔH vs pair | TH(diff) | ΔTH vs pair | Hard lock? | Switching signature | Paper claim |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| tdc_mask_perturb | random1 | pair_only | 6.68639 | 0 | 13.3622 | 0 | no | low-activity pair baseline | rules out hard locking |
| tdc_mask_perturb | random1 | all_data_on | 6.74707 | 0.0606804 | 13.4827 | 0.120565 | no | weak/moderate TDC distribution reshaping | rules out hard locking |
| tdc_mask_perturb | random1 | pair_plus_sample | 6.64622 | -0.0401638 | 13.2826 | -0.079593 | no | sample-RO activity changes TDC weakly | sample RO switching perturbs phase-bin diffusion weakly |
| tdc_mask_perturb | random3 | pair_only | 6.69703 | 0 | 13.3832 | 0 | no | low-activity pair baseline | rules out hard locking |
| tdc_mask_perturb | random3 | all_data_on | 5.98263 | -0.714397 | 11.9625 | -1.42071 | no | strong TDC distribution reshaping | local switching reshapes phase-bin diffusion without hard locking |
| tdc_mask_perturb | random1_local_sample | pair_plus_sample | 6.6682 |  | 13.3257 |  | no | sampler-on comparison without pair-only baseline | sampler-local TDC remains non-locking after sampler relocation |
| tdc_mask_perturb_p1 | random3 | all_data_on | 5.98207 | -0.714957 | 11.9613 | -1.42189 | no | replicated strong all-data switching effect without hard-lock signature | replicated all-data switching/load reshapes TDC diffusion without hard locking |
| tdc_mask_perturb_p1 | random3 | neighbors_on | 6.64861 | -0.0484188 | 13.287 | -0.0961571 | no | does not reproduce all-data collapse; points away from this mode as sole cause | neighbor subset or sample-RO-only activation does not reproduce all-data collapse |
| tdc_mask_perturb_p1 | random3 | pair_plus_sample | 6.62633 | -0.0706962 | 13.2427 | -0.140483 | no | does not reproduce all-data collapse; points away from this mode as sole cause | neighbor subset or sample-RO-only activation does not reproduce all-data collapse |
| tdc_mask_perturb_p1 | random1_local_sample | pair_only | 6.69899 | 0.0126074 | 13.3871 | 0.0249852 | no | local-sample pair-only baseline remains non-locking | sampler-local pair-only baseline remains non-locking |
| reset_aligned_tdc | random1 | baseline_warmup12 | 6.66619 |  | 12.9741 |  | no | reset/warmup startup diffusion probe | startup phase diffusion measured without hard-lock signature |
| reset_aligned_tdc | random3 | goodref_warmup12 | 6.60778 |  | 12.8768 |  | no | reset/warmup startup diffusion probe | startup phase diffusion measured without hard-lock signature |
| reset_aligned_tdc | random1_sampler_local | warmup12 | 6.73356 |  | 13.0993 |  | no | reset/warmup startup diffusion probe | sampler-local warmup12 gives the strongest clean reset-aligned diffusion in the six-point matrix |

## 论文表达边界

- 可以写：TDC evidence rules out simple pairwise RO hard locking as the dominant cause.
- 可以写：Local switching activity can reshape raw TDC phase/bin diffusion without producing hard-lock signatures.
- 可以写：The decisive causal evidence for sampler-side boundary comes from sample-RO forward/reverse counterfactuals; TDC constrains the mechanism rather than serving as the sole proof.
- 不能强写：raw TDC bin 已经给出了绝对 ps 级 jitter 结论；除非后续 code-density calibration 完整接入该实验。

## 输出文件

- CSV: `data/experiments/tdc_mechanism_inference_20260525/tdc_mechanism_inference_20260525.csv`
- Hypothesis CSV: `data/experiments/tdc_mechanism_inference_20260525/tdc_mechanism_hypothesis_status_20260525.csv`
