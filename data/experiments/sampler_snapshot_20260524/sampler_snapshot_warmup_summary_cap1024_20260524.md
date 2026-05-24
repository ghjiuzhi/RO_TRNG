# Sampler Snapshot Warmup Summary cap1024 20260524

Direct sampler-register snapshot diagnostic for `random1_sampler_regs_only_x45y31`. Each row contains 1024 consecutive post-warmup frames captured from the real sampler path and emitted after RO shutdown.

| warmup | restart reference | seq ok | rand p1 | rand abs bias | rand min-H | stage_xor H | worst sampled bit | worst bit p1 | worst bit abs bias | worst stage p1 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 4 | restart_fail_global_low | True | 0.506835938 | 0.006835938 | 0.980409 | 7.805931 | b2 line0/ro2 | 0.563476562 | 0.063476562 | 0.491210938 |
| 5 | restart_pass | True | 0.440429688 | 0.059570312 | 0.837609 | 7.805915 | b10 line1/ro2 | 0.567382812 | 0.067382812 | 0.527343750 |
| 10 | restart_pass | True | 0.455078125 | 0.044921875 | 0.875879 | 7.827542 | b6 line0/ro6 | 0.566406250 | 0.066406250 | 0.521484375 |
| 11 | restart_fail_global_high | True | 0.482421875 | 0.017578125 | 0.950151 | 7.804820 | b15 line1/ro7 | 0.583984375 | 0.083984375 | 0.472656250 |

## Interpretation

- warmup4: rand p1=0.506836, worst sampled bit=b2 abs_bias=0.063477, restart reference=restart_fail_global_low.
- warmup5: rand p1=0.440430, worst sampled bit=b10 abs_bias=0.067383, restart reference=restart_pass.
- warmup10: rand p1=0.455078, worst sampled bit=b6 abs_bias=0.066406, restart reference=restart_pass.
- warmup11: rand p1=0.482422, worst sampled bit=b15 abs_bias=0.083984, restart reference=restart_fail_global_high.

Compared with cap64, cap1024 removes much of the small-sample ambiguity. The direct sampler snapshot should be interpreted as a local mechanism probe, not a replacement for SP800-90B restart testing: it observes early true sampler-register states and stage-XOR structure at the same warmup positions that define the restart passband.
