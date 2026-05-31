# Sample-RO Routed Evidence 20260528

This artifact summarizes routed DCP evidence for the sampler-side counterfactuals.
It supports bounded physical attribution: sample-RO and local sampler-side routing changed, while this does not isolate LUT delay from every control/FIFO/UART movement.

## Per-Build Summary

| label | sample_ro_cells | sampled_data_regs | data_ro_cells | sample_ro_locs | sampled_reg_loc_count | data_ro_loc_count | sample_ro_nets | sampled_data_nets | data_ro_nets | sample_ro_pips | sampled_data_pips | data_ro_pips | sample_ro_delay_arcs | sampled_data_delay_arcs | data_ro_delay_arcs | neighborhood_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| heldout_x36y35_all640_explore1 | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9295 | 283 | 16320 | 276 | 64 | 384 | 99 |
| heldout_x36y35_all640_original | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9285 | 283 | 16345 | 276 | 64 | 384 | 99 |
| heldout_x36y35_data_ro0_explore1 | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9290 | 35 | 16309 | 276 | 8 | 384 | 81 |
| heldout_x36y35_data_ro0_original | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9290 | 35 | 16309 | 276 | 8 | 384 | 81 |
| heldout_x36y35_data_ro4_explore1 | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9279 | 38 | 16317 | 276 | 8 | 384 | 81 |
| heldout_x36y35_data_ro4_original | 9 | 64 | 16 | SLICE_X36Y35 SLICE_X37Y35 SLICE_X38Y35 | 64 | 8 | 36 | 64 | 64 | 9279 | 38 | 16317 | 276 | 8 | 384 | 81 |
| sample_ro_local_all640_explore1 | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 16 | 8 | 36 | 64 | 64 | 8591 | 243 | 15970 | 276 | 64 | 384 | 100 |
| sample_ro_local_all640_original | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 16 | 8 | 36 | 64 | 64 | 8591 | 243 | 15970 | 276 | 64 | 384 | 100 |
| sample_ro_local_data_ro0_explore1 | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 26 | 8 | 36 | 64 | 64 | 8876 | 32 | 16215 | 276 | 8 | 384 | 218 |
| sample_ro_local_data_ro0_original | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 26 | 8 | 36 | 64 | 64 | 8876 | 32 | 16215 | 276 | 8 | 384 | 218 |
| sample_ro_local_data_ro4_explore1 | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 20 | 8 | 36 | 64 | 64 | 8796 | 32 | 16138 | 276 | 8 | 384 | 149 |
| sample_ro_local_data_ro4_original | 9 | 64 | 16 | SLICE_X45Y39 SLICE_X46Y39 SLICE_X47Y39 | 20 | 8 | 36 | 64 | 64 | 8805 | 32 | 16138 | 276 | 8 | 384 | 149 |

## Pair `heldout_x36y35_all640_original` vs `heldout_x36y35_all640_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 11 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 9 |
| sampled_data_net | 0 | 0 | 0 | 64 | 8 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1242.177 | 2794.000 | 384 | 0.000 | 1205.146 | 2778.000 | -37.031 |
| sample_ro_net | 276 | 0.000 | 813.721 | 2794.000 | 276 | 0.000 | 799.674 | 2778.000 | -14.047 |
| sampled_data_net | 64 | 255.000 | 649.781 | 915.000 | 64 | 255.000 | 649.797 | 915.000 | 0.016 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_all640_original_vs_heldout_x36y35_all640_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_all640_original_vs_heldout_x36y35_all640_explore1_net_diff_20260528.csv`

## Pair `heldout_x36y35_data_ro0_original` vs `heldout_x36y35_data_ro0_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 0 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 0 |
| sampled_data_net | 0 | 0 | 0 | 64 | 0 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1253.922 | 3072.000 | 384 | 0.000 | 1253.922 | 3072.000 | 0.000 |
| sample_ro_net | 276 | 0.000 | 807.486 | 3072.000 | 276 | 0.000 | 807.486 | 3072.000 | 0.000 |
| sampled_data_net | 8 | 255.000 | 610.125 | 919.000 | 8 | 255.000 | 610.125 | 919.000 | 0.000 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_data_ro0_original_vs_heldout_x36y35_data_ro0_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_data_ro0_original_vs_heldout_x36y35_data_ro0_explore1_net_diff_20260528.csv`

## Pair `heldout_x36y35_data_ro4_original` vs `heldout_x36y35_data_ro4_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 0 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 0 |
| sampled_data_net | 0 | 0 | 0 | 64 | 0 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1153.245 | 2595.000 | 384 | 0.000 | 1153.245 | 2595.000 | 0.000 |
| sample_ro_net | 276 | 0.000 | 777.587 | 2442.000 | 276 | 0.000 | 777.587 | 2442.000 | 0.000 |
| sampled_data_net | 8 | 383.000 | 729.625 | 1043.000 | 8 | 383.000 | 729.625 | 1043.000 | 0.000 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_data_ro4_original_vs_heldout_x36y35_data_ro4_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/heldout_x36y35_data_ro4_original_vs_heldout_x36y35_data_ro4_explore1_net_diff_20260528.csv`

## Pair `sample_ro_local_all640_original` vs `sample_ro_local_all640_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 0 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 0 |
| sampled_data_net | 0 | 0 | 0 | 64 | 0 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1096.500 | 2833.000 | 384 | 0.000 | 1096.500 | 2833.000 | 0.000 |
| sample_ro_net | 276 | 0.000 | 681.351 | 2833.000 | 276 | 0.000 | 681.351 | 2833.000 | 0.000 |
| sampled_data_net | 64 | 112.000 | 462.391 | 819.000 | 64 | 112.000 | 462.391 | 819.000 | 0.000 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_all640_original_vs_sample_ro_local_all640_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_all640_original_vs_sample_ro_local_all640_explore1_net_diff_20260528.csv`

## Pair `sample_ro_local_data_ro0_original` vs `sample_ro_local_data_ro0_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 0 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 0 |
| sampled_data_net | 0 | 0 | 0 | 64 | 0 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1113.359 | 2940.000 | 384 | 0.000 | 1113.359 | 2940.000 | 0.000 |
| sample_ro_net | 276 | 0.000 | 682.261 | 2940.000 | 276 | 0.000 | 682.261 | 2940.000 | 0.000 |
| sampled_data_net | 8 | 213.000 | 493.375 | 793.000 | 8 | 213.000 | 493.375 | 793.000 | 0.000 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_data_ro0_original_vs_sample_ro_local_data_ro0_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_data_ro0_original_vs_sample_ro_local_data_ro0_explore1_net_diff_20260528.csv`

## Pair `sample_ro_local_data_ro4_original` vs `sample_ro_local_data_ro4_explore1`

| group | common_cells | loc_changed | bel_changed | common_nets | route_changed |
| --- | --- | --- | --- | --- | --- |
| data_ro | 16 | 0 | 0 | 0 | 0 |
| data_ro_net | 0 | 0 | 0 | 64 | 0 |
| sample_ro | 9 | 0 | 0 | 0 | 0 |
| sample_ro_net | 0 | 0 | 0 | 36 | 9 |
| sampled_data_net | 0 | 0 | 0 | 64 | 0 |
| sampled_data_regs | 64 | 0 | 0 | 0 | 0 |

### Net Delay Summary

| group | arcs_a | slow_max_min_a | slow_max_mean_a | slow_max_max_a | arcs_b | slow_max_min_b | slow_max_mean_b | slow_max_max_b | mean_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data_ro_net | 384 | 0.000 | 1079.070 | 2407.000 | 384 | 0.000 | 1079.070 | 2407.000 | 0.000 |
| sample_ro_net | 276 | 0.000 | 763.920 | 2407.000 | 276 | 0.000 | 749.431 | 2407.000 | -14.489 |
| sampled_data_net | 8 | 240.000 | 443.125 | 669.000 | 8 | 240.000 | 443.125 | 669.000 | 0.000 |

- cell diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_data_ro4_original_vs_sample_ro_local_data_ro4_explore1_cell_diff_20260528.csv`
- net diff CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/sample_ro_local_data_ro4_original_vs_sample_ro_local_data_ro4_explore1_net_diff_20260528.csv`
