# random1 Sampler-Side Ablation Extended Summary 20260524

## Main New Result

`regs-only` keeps the sample RO at the baseline/unconstrained site and moves only the 64 sampling registers to a local island.
The 20MiB programmed confirmation is near ideal:

- p1: `0.4998097360134125`
- bit min-entropy: `0.9994511186059211`
- adjacent equal ratio: `0.5017850369321408`
- byte min-entropy: `7.961801166556656`
- XADC: `47.4 C -> 47.4 C`, `VCCINT=1.000 V`

This is a strong mechanism result: the sampling-register/routing side alone can nearly remove the random1 continuous-stream bias.

## Comparison

| experiment | bytes | p1 | bit min-entropy | adjacent equal | interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| random1_baseline_5mib | 5242880 | 0.33766937255859375 | 0.5943765221217542 | 0.5566827191515618 | strong continuous bias with strong positive sample-RO pulling |
| random1_sample_ro_local_x45y39_20mib_programmed | 20971520 | 0.4847988963127136 | 0.9567924108244498 | 0.501911249768205 | programmed capture; moving only sample RO greatly reduces random1 bias but leaves small residual bias |
| random1_sampler_island_local_x45y39_regs_x45y31_20mib_programmed | 20971520 | 0.5000507473945618 | 0.9998535814012921 | 0.49998243749131227 | programmed 20MiB confirmation; sample RO plus local sampling registers stably fixes random1 continuous output |
| random3_good_reference_5mib | 5242880 | 0.4999711275100708 | 0.9999166940091502 | 0.4998478293382604 | good-placement reference |
| random1_sampler_regs_only_x45y31_20mib_programmed | 20971520 | 0.4998097360134125 | 0.9994511186059211 | 0.5017850369321408 | programmed 20MiB confirmation; sample RO left baseline while only sampling registers are locally constrained; nearly fixes random1 continuous output |

## Window Stability

- 1MiB windows p1 range: `0.499405980110` to `0.500097632408`
- 1MiB windows bit min-entropy range: `0.998287038234` to `0.999890279241`
- 1MiB windows adjacent-equal range: `0.501292467117` to `0.502276062965`
- 5MiB windows p1 range: `0.499736380577` to `0.499865269661`
- 5MiB windows bit min-entropy range: `0.999239555582` to `0.999611302783`
- 5MiB windows adjacent-equal range: `0.501687097549` to `0.501874005839`

## Paper Interpretation

The prior sampler-island result already showed that moving sample RO plus sampling registers fixes random1. The new regs-only result is more discriminating: even with the sample RO left at baseline, constraining the sampling registers/routing island nearly fixes the source.

Therefore the sampler path is not merely readout logic. The sampling registers and their local routing participate in the physical entropy-source boundary and can dominate the observed placement sensitivity.

## Restart Contrast

The same `regs-only` variant was tested with SP800-90B restart auto-stream captures after the 20MiB continuous result.
Each packed restart capture has `1000 x 125` bytes and is expanded row-preservingly to `1000 x 1000` bit symbols before `ea_restart`.

| warmup | repeats | ea_restart | X_cutoff | X_max range | overall p1 range | interpretation |
| ---: | ---: | --- | ---: | ---: | ---: | --- |
| 0 | 2 | failed | 572 | 756-802 | 0.498425-0.499146 | continuous-like global balance, but strong fixed early-column hotspot |
| 12 | 2 | failed | 572 | 601-609 | 0.452171-0.453785 | warmup reduces the worst fixed-column hotspot but introduces/reveals a repeatable global low-one bias |

This is now a useful negative/partial result rather than a disappointment. It separates two physical effects:

- sampling-register/routing placement can repair steady-state continuous-stream bias;
- restart/startup fixed-position robustness is controlled by an additional transient mechanism.

Paper wording should avoid saying that `regs-only` fully fixes the entropy source. The stronger claim is that sampler-side placement is causal for steady-state bias, while SP800-90B restart exposes a stricter startup condition that continuous non-IID estimates do not cover.

Detailed restart artifacts:

- `data/experiments/sampler_regs_only_20260524/random1_sampler_regs_only_restart_summary_20260524.md`
- `data/experiments/restart_summary_20260524/restart_result_summary_20260524.csv`
- `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup*_run*/`
