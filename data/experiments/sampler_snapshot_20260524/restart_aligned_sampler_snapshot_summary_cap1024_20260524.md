# Restart-Aligned Sampler Snapshot Summary cap1024 20260524

This diagnostic captures the real sampler-register state at the same restart-aligned output position across 1024 mini-restarts. It is designed to match the statistical object of the SP800-90B restart test more closely than continuous post-start snapshots.

| warmup | restart reference | seq ok | rand p1 | rand abs bias | rand min-H | stage_xor H | fixed sampled bits | heavy sampled bits | worst sampled bit | worst bit p1 | worst stage p1 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 4 | restart_fail_global_low | True | 0.340820312 | 0.159179688 | 0.601256 | 1.978579 | 19 | 60 | b1 line0/ro1 | 0.000000000 | 0.000000000 |
| 5 | restart_pass | True | 0.514648438 | 0.014648438 | 0.958341 | 5.585576 | 38 | 52 | b2 line0/ro2 | 1.000000000 | 0.018554688 |
| 10 | restart_pass | True | 0.448242188 | 0.051757812 | 0.857893 | 4.753995 | 22 | 56 | b1 line0/ro1 | 1.000000000 | 0.000000000 |
| 11 | restart_fail_global_high | True | 0.504882812 | 0.004882812 | 0.985980 | 5.472599 | 27 | 53 | b1 line0/ro1 | 1.000000000 | 0.977539062 |

## Interpretation

- warmup4: rand p1=0.340820, sampled fixed bits=19, heavy sampled bits=60, restart reference=restart_fail_global_low.
- warmup5: rand p1=0.514648, sampled fixed bits=38, heavy sampled bits=52, restart reference=restart_pass.
- warmup10: rand p1=0.448242, sampled fixed bits=22, heavy sampled bits=56, restart reference=restart_pass.
- warmup11: rand p1=0.504883, sampled fixed bits=27, heavy sampled bits=53, restart reference=restart_fail_global_high.

The key comparison is against continuous cap1024 snapshots. Continuous post-start snapshots showed only weak sampled-bit bias, while restart-aligned snapshots expose startup-position determinism. This supports the mechanism that restart failures are tied to fixed early sampler/output positions rather than steady-state continuous randomness alone.
