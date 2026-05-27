# Restart Sampler-Island Passband Strict Summary

Only strict captures with an 8-byte restart header plus a complete 1000x125 payload should be used as formal restart evidence.

| variant | warmup | order | restart | X_max/cutoff | overall p1 | worst byte.bit | worst p1 | min restart H |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: | ---: |
| sample_ro_plus_regs_local | 10 | lsb | passed | 593/632 | 0.457368000 | 18.0 | 0.407000000 | 0.712102 |
| sample_ro_plus_regs_local | 10 | msb | passed | 593/605 | 0.457368000 | 18.0 | 0.407000000 | 0.690213 |

Interpretation guide:

- `sample_ro_local_only` isolates the sample RO placement change while leaving sampling registers/routing in the baseline implementation.
- `sample_ro_plus_regs_local` is the sampler-island variant and tests the combined sampler-side physical boundary.
- A non-monotonic passband is evidence that warmup is selecting a startup phase window, not simply improving randomness by waiting longer.
