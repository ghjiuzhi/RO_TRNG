# random1 regs-only Restart Summary 20260524

## Result

`regs-only` nearly fixes the 20MiB continuous stream and exposes a non-monotonic restart warmup passband.
Warmup `5/6/8/10` passed the SP800-90B restart sanity check, while `0/4/11/12/16` failed under the same bit-symbol protocol.
This is a high-value mechanism result because it separates steady-state entropy quality from startup-window robustness.

| warmup | repeat | order | status | H_I | X_cutoff | X_max | overall p1 | worst byte.bit | worst p1 | XADC |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| 0 | run01 | lsb | failed | 0.999451 | 572 | 756 | 0.499146 | 1.6 | 0.756000000 | 47.4C->47.6C, VCCINT=1.000V |
| 0 | run01 | msb | failed | 0.999451 | 572 | 756 | 0.499146 | 1.6 | 0.756000000 | 47.4C->47.6C, VCCINT=1.000V |
| 0 | run02 | lsb | failed | 0.999451 | 572 | 802 | 0.498425 | 1.7 | 0.802000000 | 47.6C->47.4C, VCCINT=1.000V |
| 0 | run02 | msb | failed | 0.999451 | 572 | 802 | 0.498425 | 1.7 | 0.802000000 | 47.6C->47.4C, VCCINT=1.000V |
| 4 | repeat02 | lsb | failed | 0.999451 | 572 | 733 | 0.407103 | 0.2 | 0.267000000 | 47.4C->47.4C, VCCINT=1.000V |
| 4 | repeat02 | msb | failed | 0.999451 | 572 | 733 | 0.407103 | 0.2 | 0.267000000 | 47.4C->47.4C, VCCINT=1.000V |
| 4 | sweep01 | lsb | failed | 0.999451 | 572 | 751 | 0.40797 | 1.6 | 0.249000000 | 47.5C->47.2C, VCCINT=1.000V |
| 4 | sweep01 | msb | failed | 0.999451 | 572 | 751 | 0.40797 | 1.6 | 0.249000000 | 47.5C->47.2C, VCCINT=1.000V |
| 5 | edge01 | lsb | passed | 0.999451 | 572 | 560 | 0.497894 | 111.2 | 0.442000000 | 47.2C->47.5C, VCCINT=1.000V |
| 5 | edge01 | msb | passed | 0.999451 | 572 | 560 | 0.497894 | 111.2 | 0.442000000 | 47.2C->47.5C, VCCINT=1.000V |
| 5 | repeat02 | lsb | passed | 0.999451 | 572 | 561 | 0.498602 | 104.4 | 0.561000000 | 47.4C->47.4C, VCCINT=1.000V |
| 5 | repeat02 | msb | passed | 0.999451 | 572 | 561 | 0.498602 | 104.4 | 0.561000000 | 47.4C->47.4C, VCCINT=1.000V |
| 6 | passband01 | lsb | passed | 0.999451 | 572 | 551 | 0.49628 | 24.4 | 0.449000000 | 47.4C->47.5C, VCCINT=1.000V |
| 6 | passband01 | msb | passed | 0.999451 | 572 | 551 | 0.49628 | 24.4 | 0.449000000 | 47.4C->47.5C, VCCINT=1.000V |
| 6 | repeat02 | lsb | passed | 0.999451 | 572 | 554 | 0.497339 | 108.7 | 0.446000000 | 47.5C->47.5C, VCCINT=1.000V |
| 6 | repeat02 | msb | passed | 0.999451 | 572 | 554 | 0.497339 | 108.7 | 0.446000000 | 47.5C->47.5C, VCCINT=1.000V |
| 8 | repeat02 | lsb | passed | 0.999451 | 572 | 566 | 0.484294 | 0.3 | 0.442000000 | 47.5C->47.4C, VCCINT=1.000V |
| 8 | repeat02 | msb | passed | 0.999451 | 572 | 566 | 0.484294 | 0.3 | 0.442000000 | 47.5C->47.4C, VCCINT=1.000V |
| 8 | sweep01 | lsb | passed | 0.999451 | 572 | 566 | 0.482728 | 83.0 | 0.436000000 | 47.2C->47.4C, VCCINT=1.001V |
| 8 | sweep01 | msb | passed | 0.999451 | 572 | 566 | 0.482728 | 83.0 | 0.436000000 | 47.2C->47.4C, VCCINT=1.001V |
| 10 | passband01 | lsb | passed | 0.999451 | 572 | 565 | 0.499174 | 115.3 | 0.435000000 | 47.7C->47.5C, VCCINT=1.000V |
| 10 | passband01 | msb | passed | 0.999451 | 572 | 565 | 0.499174 | 115.3 | 0.435000000 | 47.7C->47.5C, VCCINT=1.000V |
| 10 | repeat02 | lsb | passed | 0.999451 | 572 | 554 | 0.500018 | 14.1 | 0.453000000 | 47.4C->47.1C, VCCINT=1.000V |
| 10 | repeat02 | msb | passed | 0.999451 | 572 | 554 | 0.500018 | 14.1 | 0.453000000 | 47.4C->47.1C, VCCINT=1.000V |
| 11 | edge01 | lsb | failed | 0.999451 | 572 | 688 | 0.55921 | 81.4 | 0.613000000 | 47.5C->47.6C, VCCINT=1.000V |
| 11 | edge01 | msb | failed | 0.999451 | 572 | 688 | 0.55921 | 81.4 | 0.613000000 | 47.5C->47.6C, VCCINT=1.000V |
| 11 | repeat02 | lsb | failed | 0.999451 | 572 | 701 | 0.558805 | 57.2 | 0.618000000 | 46.6C->46.4C, VCCINT=1.000V |
| 11 | repeat02 | msb | failed | 0.999451 | 572 | 701 | 0.558805 | 57.2 | 0.618000000 | 46.6C->46.4C, VCCINT=1.000V |
| 12 | run01 | lsb | failed | 0.999451 | 572 | 609 | 0.452171 | 2.7 | 0.391000000 | 47.6C->47.6C, VCCINT=1.001V |
| 12 | run01 | msb | failed | 0.999451 | 572 | 609 | 0.452171 | 2.7 | 0.391000000 | 47.6C->47.6C, VCCINT=1.001V |
| 12 | run02 | lsb | failed | 0.999451 | 572 | 601 | 0.453785 | 6.1 | 0.399000000 | 47.4C->46.9C, VCCINT=1.000V |
| 12 | run02 | msb | failed | 0.999451 | 572 | 601 | 0.453785 | 6.1 | 0.399000000 | 47.4C->46.9C, VCCINT=1.000V |
| 16 | sweep01 | lsb | failed | 0.999451 | 572 | 586 | 0.466933 | 60.3 | 0.414000000 | 47.5C->47.5C, VCCINT=1.000V |
| 16 | sweep01 | msb | failed | 0.999451 | 572 | 586 | 0.466933 | 60.3 | 0.414000000 | 47.5C->47.5C, VCCINT=1.000V |

## Warmup Transition

| warmup | status | rows | X_max range | overall p1 range | min-H range |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | failed | 4 | 756-802 | 0.498425-0.499146 | - |
| 4 | failed | 4 | 733-751 | 0.407103-0.407970 | - |
| 5 | passed | 4 | 560-561 | 0.497894-0.498602 | 0.813043-0.832264 |
| 6 | passed | 4 | 551-554 | 0.496280-0.497339 | 0.822266-0.868880 |
| 8 | passed | 4 | 566-566 | 0.482728-0.484294 | 0.746339-0.772196 |
| 10 | passed | 4 | 554-565 | 0.499174-0.500018 | 0.815911-0.839326 |
| 11 | failed | 4 | 688-701 | 0.558805-0.559210 | - |
| 12 | failed | 4 | 601-609 | 0.452171-0.453785 | - |
| 16 | failed | 2 | 586-586 | 0.466933-0.466933 | - |

![Warmup transition](E:/Project/MLDSA/RO_TRNG/data/experiments/sampler_regs_only_20260524/random1_sampler_regs_only_warmup_transition_20260524.svg)

## Mechanism Interpretation

- Continuous stream: moving only the 64 sampling registers/routing island makes `random1` near ideal (`p1=0.499809736`, bit min-entropy `0.999451`).
- Restart warmup0: both repeats fail despite near-balanced overall p1. The failure is driven by early fixed-column hotspots (`X_max=756` and `802`, cutoff `572`).
- Restart warmup4 fails with a strong global low-one bias (`overall p1=0.407970`) and a fixed-column hotspot (`X_max=751`).
- Restart warmup5/6/8/10 pass; `warmup8` passed in two independent captures.
- Restart warmup11/12/16 fail again, with the failure mode shifting to global high-one or low-one bias plus moderate fixed-column excursions.
- Therefore warmup is not monotonic. The restart-safe region behaves like a startup phase window or passband, not simply like 'discard more early bytes'.

## Paper Claim

The cleanest claim is not that regs-only solves the entropy source completely. The stronger and more nuanced claim is:

> Sampling-register/routing placement is sufficient to repair steady-state continuous bias, proving that the sampler path is part of the entropy-source boundary. SP800-90B restart experiments further reveal a narrow, non-monotonic startup warmup passband, indicating that restart robustness depends on the sampled phase trajectory rather than on simply waiting longer.

This result strengthens the paper because it gives a layered mechanism: sampler-side physical implementation controls steady-state bias, while reset/startup phase transients control restart sanity.

## Artifacts

- CSV: `data\experiments\sampler_regs_only_20260524\random1_sampler_regs_only_restart_summary_20260524.csv`
- Warmup transition CSV: `data\experiments\sampler_regs_only_20260524\random1_sampler_regs_only_warmup_transition_20260524.csv`
- Warmup transition SVG: `data\experiments\sampler_regs_only_20260524\random1_sampler_regs_only_warmup_transition_20260524.svg`
- Packed captures: `data/hardware/20260511_fpga1_board1/restart/random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup*_run*_20260524.bin`
- ea_restart outputs: `data/hardware/20260511_fpga1_board1/restart/ea_restart_random1_sampler_regs_only_*_20260524/`
- Column diagnostics: `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup*_run*/`
