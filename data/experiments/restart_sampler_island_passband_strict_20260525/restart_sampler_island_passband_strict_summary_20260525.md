# Restart Sampler-Island Passband Strict Summary

Only strict captures with an 8-byte restart header plus a complete 1000x125 payload should be used as formal restart evidence.

| variant | warmup | order | restart | X_max/cutoff | overall p1 | worst byte.bit | worst p1 | min restart H |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: | ---: |
| sample_ro_local_only | 4 | lsb | passed | 553/632 | 0.499286000 | 29.7 | 0.447000000 | 0.828444 |
| sample_ro_local_only | 4 | msb | passed | 553/605 | 0.499286000 | 29.7 | 0.447000000 | 0.839080 |
| sample_ro_local_only | 5 | lsb | failed | 713/632 | 0.410871000 | 1.2 | 0.287000000 |  |
| sample_ro_local_only | 5 | msb | failed | 713/605 | 0.410871000 | 1.2 | 0.287000000 |  |
| sample_ro_local_only | 10 | lsb | passed | 550/632 | 0.500648000 | 34.1 | 0.450000000 | 0.828444 |
| sample_ro_local_only | 10 | msb | passed | 550/605 | 0.500648000 | 34.1 | 0.450000000 | 0.826984 |
| sample_ro_local_only | 11 | lsb | failed | 666/632 | 0.422998000 | 0.0 | 0.334000000 |  |
| sample_ro_local_only | 11 | msb | failed | 666/605 | 0.422998000 | 0.0 | 0.334000000 |  |
| sample_ro_plus_regs_local | 4 | lsb | passed | 551/632 | 0.499770000 | 14.3 | 0.450000000 | 0.828444 |
| sample_ro_plus_regs_local | 4 | msb | passed | 551/605 | 0.499770000 | 14.3 | 0.450000000 | 0.813217 |
| sample_ro_plus_regs_local | 5 | lsb | passed | 549/632 | 0.500804000 | 66.6 | 0.549000000 | 0.817899 |
| sample_ro_plus_regs_local | 5 | msb | passed | 549/605 | 0.500804000 | 66.6 | 0.549000000 | 0.862733 |
| sample_ro_plus_regs_local | 10 | lsb | passed | 610/632 | 0.451448000 | 4.2 | 0.397000000 | 0.686477 |
| sample_ro_plus_regs_local | 10 | msb | failed | 610/605 | 0.451448000 | 4.2 | 0.397000000 |  |
| sample_ro_plus_regs_local | 11 | lsb | passed | 594/632 | 0.470665000 | 2.1 | 0.406000000 | 0.763764 |
| sample_ro_plus_regs_local | 11 | msb | passed | 594/605 | 0.470665000 | 2.1 | 0.406000000 | 0.753564 |

Interpretation guide:

- `sample_ro_local_only` isolates the sample RO placement change while leaving sampling registers/routing in the baseline implementation.
- `sample_ro_plus_regs_local` is the sampler-island variant and tests the combined sampler-side physical boundary.
- A non-monotonic passband is evidence that warmup is selecting a startup phase window, not simply improving randomness by waiting longer.
