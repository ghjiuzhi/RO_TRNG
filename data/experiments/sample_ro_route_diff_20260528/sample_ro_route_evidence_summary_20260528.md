# Sample-RO Routed Evidence 20260528

This artifact summarizes routed DCP evidence for the sampler-side counterfactuals.
It supports bounded physical attribution: sample-RO and local sampler-side routing changed, while this does not isolate LUT delay from every control/FIFO/UART movement.

## Per-Build Summary

| label | sample_ro_cells | sampled_data_regs | data_ro_cells | sample_ro_locs | sampled_reg_loc_count | data_ro_loc_count | sample_ro_nets | sampled_data_nets | data_ro_nets | sample_ro_pips | sampled_data_pips | data_ro_pips | sample_ro_delay_arcs | sampled_data_delay_arcs | data_ro_delay_arcs | neighborhood_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compact_w11_baseline | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9251 | 282 | 16456 | 276 | 64 | 384 | 241 |
| compact_w4_baseline | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9241 | 282 | 16469 | 276 | 64 | 384 | 241 |
| compact_w5_baseline | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9270 | 282 | 16496 | 276 | 64 | 384 | 241 |
| formal_w4_baseline | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9212 | 282 | 16382 | 276 | 64 | 384 | 233 |
| forward_w11_formal_sample | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9261 | 282 | 16464 | 276 | 64 | 384 | 234 |
| forward_w4_formal_sample | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9240 | 282 | 16438 | 276 | 64 | 384 | 233 |
| forward_w5_formal_sample | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9261 | 282 | 16478 | 276 | 64 | 384 | 233 |
| reverse_w4_compact_sample | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 17 | 7 | 36 | 64 | 64 | 8694 | 259 | 16104 | 276 | 64 | 384 | 551 |

## Pair `compact_w5_baseline` vs `forward_w5_formal_sample`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 32 |
| sample_ro | 9 | 2 | 3 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 18 |
| sampled_data_net | 0 | 0 | 0 | 64 | 10 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1239.721 | 3083.000 | 384 | 0.000 | 1195.086 | 2748.000 | -44.635 |
| sample_ro_net | 276 | 0.000 | 594.054 | 3083.000 | 276 | 0.000 | 581.475 | 2748.000 | -12.580 |
| sampled_data_net | 64 | 252.000 | 651.250 | 932.000 | 64 | 252.000 | 651.109 | 932.000 | -0.141 |

- cell diff CSV: `data/experiments/sample_ro_route_diff_20260528/compact_w5_baseline_vs_forward_w5_formal_sample_cell_diff_20260528.csv`
- net diff CSV: `data/experiments/sample_ro_route_diff_20260528/compact_w5_baseline_vs_forward_w5_formal_sample_net_diff_20260528.csv`

## Pair `formal_w4_baseline` vs `reverse_w4_compact_sample`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 16 | 12 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 64 |
| sample_ro | 9 | 2 | 3 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 36 |
| sampled_data_net | 0 | 0 | 0 | 64 | 64 |
| sampled_data_regs | 64 | 64 | 63 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1162.549 | 2664.000 | 384 | 0.000 | 703.510 | 1507.000 | -459.039 |
| sample_ro_net | 276 | 0.000 | 575.819 | 2445.000 | 276 | 0.000 | 568.783 | 1507.000 | -7.036 |
| sampled_data_net | 64 | 252.000 | 651.234 | 932.000 | 64 | 116.000 | 480.297 | 802.000 | -170.938 |

- cell diff CSV: `data/experiments/sample_ro_route_diff_20260528/formal_w4_baseline_vs_reverse_w4_compact_sample_cell_diff_20260528.csv`
- net diff CSV: `data/experiments/sample_ro_route_diff_20260528/formal_w4_baseline_vs_reverse_w4_compact_sample_net_diff_20260528.csv`
