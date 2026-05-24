# TDC Reset-Enable Warmup-Edge Interpretation 20260524

This report re-analyzes existing reset-enable TDC captures with warmup-window starts at packets 4, 5, 10, 11, and 12 after the RO-enable edge. It is an offline analysis only; no new hardware capture was used. Raw TDC bins are relative and uncalibrated.

## Key Result

The restart experiment shows a sharp non-monotonic passband for the regs-only TRNG path: warmup 5/6/8/10 passed SP800-90B restart sanity, while 4/11/12/16 failed. The reset-enable TDC windows do not show an analogous sharp jump between 4->5 or 10->11. Across the existing sample-data TDC captures, warmup-window H(diff) changes by only a few millibits across starts 4..12.

This makes TDC a useful negative/constraint result: the restart passband is unlikely to be explained by a simple pairwise sampler-RO/data-RO raw-bin diffusion transition visible in the current TDC topology. Combined with the regs-only continuous-stream ablation, the stronger mechanism points toward sampling-register/routing/aperture effects and fixed output-position startup behavior.

## Edge Delta Summary

| placement group | runs | H4 | H5 | delta 5-4 | H10 | H11 | delta 11-10 | H12 | range 4..12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline_ro0 | 2 | 6.549796 | 6.550741 | 0.000945 | 6.549697 | 6.547856 | -0.001841 | 6.548272 | 0.002885 |
| random1_baseline_ro4 | 2 | 6.492451 | 6.493617 | 0.001166 | 6.491887 | 6.491331 | -0.000556 | 6.490333 | 0.003284 |
| random1_sampler_local_ro0 | 2 | 6.624101 | 6.623839 | -0.000262 | 6.624316 | 6.624000 | -0.000316 | 6.622144 | 0.002171 |
| random1_sampler_local_ro4 | 2 | 6.632391 | 6.632395 | 0.000004 | 6.633455 | 6.633926 | 0.000471 | 6.633018 | 0.001534 |
| random3_goodref_ro0 | 2 | 6.607943 | 6.609450 | 0.001507 | 6.610611 | 6.611782 | 0.001171 | 6.611533 | 0.003839 |
| random3_goodref_ro3 | 2 | 6.549418 | 6.548458 | -0.000959 | 6.548411 | 6.547394 | -0.001016 | 6.548365 | 0.002024 |

## Paper Interpretation

- Positive TDC evidence remains at the placement/geometry level: sampler-local improves early H(diff), especially for RO4.
- Warmup-edge TDC does not reproduce the restart pass/fail boundary. That weakens a pure sampler/data RO phase-diffusion explanation for the passband.
- The best current claim is layered: TDC rules out strong locking and shows geometry-dependent startup diffusion, while regs-only TRNG/restart proves the sampling register/routing path controls steady-state quality and startup robustness in a way not fully captured by pairwise TDC.
- Next hardware should not be another broad reset-enable repeat. The most valuable next design is a TDC or diagnostic top that explicitly instantiates the TRNG sampling register island, or a restart-position probe that emits early bit columns with state markers.
