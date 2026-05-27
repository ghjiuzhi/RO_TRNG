# Sampler Snapshot Correlation/XOR Analysis 2026-05-26

## Summary

| label | frames | rand p1 | sampled mean p1 | sampled mean abs bias | bits p1 > 0.55 | stage mean p1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| w5 | 1024 | 0.509765625 | 0.523620605 | 0.026367188 | 9 | 0.498046875 |
| w10 | 1024 | 0.466796875 | 0.523178101 | 0.026046753 | 12 | 0.510131836 |
| w11 | 1024 | 0.500976562 | 0.524139404 | 0.027099609 | 13 | 0.499755859 |

## Outputs

- per-run summary: `sampler_snapshot_w5_w10_w11_correlation_xor_summary_20260526.csv`
- per-run top pairwise MI/correlation: `<label>.pairwise_top.csv`
- per-run bit-to-rand MI/correlation: `<label>.bit_to_rand_top.csv`
- per-run line/data_ro/stage XOR ablation: `<label>.xor_ablation.csv`
- per-run pairwise aggregate categories: `<label>.pairwise_aggregate.csv`
- combined pairwise aggregate categories: `sampler_snapshot_w5_w10_w11_pairwise_aggregate_20260526.csv`
- cross-run pairwise deltas: `sampler_snapshot_pairwise_delta_top_20260526.csv`
