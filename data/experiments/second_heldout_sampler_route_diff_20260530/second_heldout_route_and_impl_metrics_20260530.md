# Second Held-Out Sampler Route and Implementation Metrics 20260530

Generated from existing `sample_ro_local` routed DCP extraction CSVs and Vivado reports. No hardware capture was run by this summarizer.

## Coverage

- Route extraction coverage: 17/17 second held-out bitstreams.
- Pairwise route comparisons against second_all640: 16/16 available data_ro/except_data_ro bitstreams.
- Implementation metrics coverage: 17/17 report sets.

## Route Audit Snapshot

| label | kind | index | sample_ro_pips | sampled_data_pips | data_ro_pips | sample_ro_slow_max_mean_ps | sampled_data_slow_max_mean_ps | data_ro_slow_max_mean_ps | neighborhood_rows | sample_ro_route_changed_vs_all640 | data_ro_route_changed_vs_all640 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| second_all640 | all640 | all | 8591 | 243 | 15970 | 681.351 | 462.391 | 1096.500 | 100 | 0 | 0 |
| second_data_ro0 | data_ro | 0 | 8876 | 32 | 16215 | 682.261 | 493.375 | 1113.359 | 218 | 26 | 24 |
| second_data_ro1 | data_ro | 1 | 8752 | 29 | 16161 | 602.993 | 444.125 | 1186.117 | 415 | 26 | 24 |
| second_data_ro2 | data_ro | 2 | 8795 | 31 | 16220 | 626.475 | 416.875 | 1077.542 | 234 | 26 | 26 |
| second_data_ro3 | data_ro | 3 | 8928 | 30 | 16108 | 637.899 | 433.750 | 1092.958 | 252 | 26 | 28 |
| second_data_ro4 | data_ro | 4 | 8805 | 32 | 16138 | 763.920 | 443.125 | 1079.070 | 149 | 26 | 26 |
| second_data_ro5 | data_ro | 5 | 8782 | 36 | 16177 | 588.228 | 580.500 | 1144.958 | 378 | 26 | 28 |
| second_data_ro6 | data_ro | 6 | 8722 | 35 | 16186 | 645.297 | 634.000 | 1061.682 | 165 | 26 | 24 |
| second_data_ro7 | data_ro | 7 | 8811 | 35 | 16225 | 632.754 | 566.625 | 1041.419 | 243 | 26 | 24 |
| second_except_data_ro0 | except_data_ro | 0 | 8760 | 276 | 16282 | 601.259 | 493.403 | 1083.680 | 455 | 26 | 24 |
| second_except_data_ro1 | except_data_ro | 1 | 8760 | 273 | 16240 | 624.137 | 489.931 | 1041.799 | 513 | 26 | 24 |
| second_except_data_ro2 | except_data_ro | 2 | 8663 | 281 | 16220 | 531.856 | 517.306 | 1118.409 | 624 | 26 | 24 |
| second_except_data_ro3 | except_data_ro | 3 | 8719 | 277 | 16214 | 614.590 | 490.472 | 1152.435 | 299 | 26 | 28 |
| second_except_data_ro4 | except_data_ro | 4 | 8728 | 271 | 16317 | 549.691 | 505.181 | 1196.854 | 612 | 26 | 24 |
| second_except_data_ro5 | except_data_ro | 5 | 8712 | 267 | 16221 | 630.464 | 505.111 | 1074.914 | 505 | 26 | 26 |
| second_except_data_ro6 | except_data_ro | 6 | 8763 | 270 | 16274 | 654.252 | 484.472 | 1132.156 | 269 | 26 | 26 |
| second_except_data_ro7 | except_data_ro | 7 | 8750 | 281 | 16245 | 610.471 | 501.667 | 1120.690 | 563 | 26 | 26 |

## Implementation Metrics Snapshot

| label | slice_luts | slice_registers | bram_tiles | wns_ns | whs_ns | total_on_chip_power_w | fully_routed_nets | routing_error_nets | drc_violations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| second_all640 | 349 | 365 | 0.5 | 0.636 | 0.117 | 0.221 | 647 | 0 | 31 |
| second_data_ro0 | 338 | 365 | 0.5 | 0.489 | 0.120 | 0.222 | 582 | 0 | 31 |
| second_data_ro1 | 338 | 365 | 0.5 | 0.441 | 0.116 | 0.221 | 581 | 0 | 31 |
| second_data_ro2 | 338 | 365 | 0.5 | 0.493 | 0.036 | 0.223 | 579 | 0 | 31 |
| second_data_ro3 | 338 | 365 | 0.5 | 0.387 | 0.112 | 0.221 | 581 | 0 | 31 |
| second_data_ro4 | 338 | 365 | 0.5 | 0.532 | 0.130 | 0.222 | 580 | 0 | 31 |
| second_data_ro5 | 339 | 365 | 0.5 | 0.618 | 0.059 | 0.222 | 579 | 0 | 31 |
| second_data_ro6 | 338 | 365 | 0.5 | 0.690 | 0.119 | 0.222 | 580 | 0 | 31 |
| second_data_ro7 | 338 | 365 | 0.5 | 0.749 | 0.111 | 0.222 | 580 | 0 | 31 |
| second_except_data_ro0 | 352 | 366 | 0.5 | 0.636 | 0.061 | 0.223 | 651 | 0 | 31 |
| second_except_data_ro1 | 352 | 366 | 0.5 | 0.645 | 0.105 | 0.223 | 649 | 0 | 31 |
| second_except_data_ro2 | 352 | 366 | 0.5 | 0.645 | 0.118 | 0.222 | 652 | 0 | 31 |
| second_except_data_ro3 | 352 | 366 | 0.5 | 0.478 | 0.105 | 0.222 | 650 | 0 | 31 |
| second_except_data_ro4 | 352 | 366 | 0.5 | 0.544 | 0.081 | 0.222 | 651 | 0 | 31 |
| second_except_data_ro5 | 352 | 366 | 0.5 | 0.615 | 0.120 | 0.223 | 651 | 0 | 31 |
| second_except_data_ro6 | 352 | 366 | 0.5 | 0.445 | 0.052 | 0.222 | 651 | 0 | 31 |
| second_except_data_ro7 | 352 | 366 | 0.5 | 0.580 | 0.121 | 0.222 | 650 | 0 | 31 |
