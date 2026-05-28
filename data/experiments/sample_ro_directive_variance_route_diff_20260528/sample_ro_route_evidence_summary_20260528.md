# Sample-RO Routed Evidence 20260528

This artifact summarizes routed DCP evidence for the sampler-side counterfactuals.
It supports bounded physical attribution: sample-RO and local sampler-side routing changed, while this does not isolate LUT delay from every control/FIFO/UART movement.

## Per-Build Summary

| label | sample_ro_cells | sampled_data_regs | data_ro_cells | sample_ro_locs | sampled_reg_loc_count | data_ro_loc_count | sample_ro_nets | sampled_data_nets | data_ro_nets | sample_ro_pips | sampled_data_pips | data_ro_pips | sample_ro_delay_arcs | sampled_data_delay_arcs | data_ro_delay_arcs | neighborhood_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compact_w4_explore1 | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9241 | 282 | 16472 | 276 | 64 | 384 | 241 |
| forward_w4_explore1 | 9 | 64 | 16 | SLICE_X46Y32 SLICE_X46Y33 SLICE_X46Y34 SLICE_X46Y35 SLICE_X46Y36 SLICE_X46Y37 SLICE_X47Y33 SLICE_X49Y45 | 64 | 8 | 36 | 64 | 64 | 9239 | 282 | 16430 | 276 | 64 | 384 | 233 |

## Pair `compact_w4_explore1` vs `forward_w4_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 34 |
| sample_ro | 9 | 2 | 3 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 18 |
| sampled_data_net | 0 | 0 | 0 | 64 | 9 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1285.755 | 3316.000 | 384 | 0.000 | 1162.648 | 2664.000 | -123.107 |
| sample_ro_net | 276 | 0.000 | 602.851 | 3316.000 | 276 | 0.000 | 575.717 | 2465.000 | -27.134 |
| sampled_data_net | 64 | 252.000 | 651.234 | 932.000 | 64 | 252.000 | 651.250 | 932.000 | 0.016 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/sample_ro_directive_variance_route_diff_20260528/compact_w4_explore1_vs_forward_w4_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/sample_ro_directive_variance_route_diff_20260528/compact_w4_explore1_vs_forward_w4_explore1_net_diff_20260528.csv`
