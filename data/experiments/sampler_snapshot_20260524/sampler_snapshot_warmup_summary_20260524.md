# Sampler Snapshot Warmup Summary 20260524

This table compares the direct sampler-register snapshot diagnostic against the regs-only SP800-90B restart passband. The current data are cap64 single-run smoke captures, so they are evidence for observability and direction, not final statistics.

| warmup | restart reference | frames | rand p1 | rand abs bias | rand min-H | stage_xor H | worst sampled bit | worst bit p1 | worst stage p1 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 4 | restart_fail_global_low | 64 | 0.406250000 | 0.093750000 | 0.752072 | 5.613205 | b48 line6/ro0 | 0.609375000 | 0.406250000 |
| 5 | restart_pass | 64 | 0.531250000 | 0.031250000 | 0.912537 | 5.718750 | b6 line0/ro6 | 0.609375000 | 0.421875000 |
| 10 | restart_pass | 64 | 0.375000000 | 0.125000000 | 0.678072 | 5.843750 | b16 line2/ro0 | 0.953125000 | 0.625000000 |
| 11 | restart_fail_global_high | 64 | 0.500000000 | 0.000000000 | 1.000000 | 5.718750 | b6 line0/ro6 | 0.750000000 | 0.609375000 |

## Interpretation

- warmup4 shows a low rand-bit bias in the snapshot (`p1=0.40625`), matching the direction of the restart warmup4 global-low failure.
- warmup5 moves near balance (`p1=0.53125`), consistent with entering the restart passband.
- warmup10/11 do not cleanly reproduce the restart pass/fail boundary in a single cap64 snapshot: warmup10 has a low rand p1 and an extreme sampled-bit hotspot, while warmup11 has balanced rand p1 but still shows a strong sampled-bit hotspot.
- Therefore cap64 proves that the diagnostic can observe sampler-path structure, but it is too small to establish the passband mechanism. The correct next step is a BRAM-backed snapshot with 1024 or more frames, not another isolated pairwise TDC repeat.
