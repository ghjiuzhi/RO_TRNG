# Formal Restart Output Profile

- rows: `3`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro0_1000x125_strict_20260526.payload | 5 | 0.488326000 | 0.966703168 | 15.794927160 | 97.2 | 563 | 0.437000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_except_data_ro0_1000x125_strict_20260526.payload | 10 | 0.501020000 | 0.997059900 | 15.997737340 | 12.5 | 571 | 0.571000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 11 | 0.540569000 | 0.887449315 | 18.178592877 | 104.6 | 594 | 0.594000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 0 | 16000 | 0.533062500 | 0.907623400 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 1 | 16000 | 0.536000000 | 0.899695094 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 2 | 16000 | 0.538375000 | 0.893316676 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 3 | 16000 | 0.545687500 | 0.873853098 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 4 | 16000 | 0.541687500 | 0.884467295 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 5 | 16000 | 0.536562500 | 0.898181866 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 6 | 16000 | 0.543187500 | 0.880477815 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 0 | 7 | 16000 | 0.536687500 | 0.897845808 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 0 | 16000 | 0.544750000 | 0.876333804 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 1 | 16000 | 0.535812500 | 0.900199857 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 2 | 16000 | 0.535062500 | 0.902220674 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 3 | 16000 | 0.544750000 | 0.876333804 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 4 | 16000 | 0.539375000 | 0.890639441 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 5 | 16000 | 0.542375000 | 0.882637414 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 6 | 16000 | 0.542562500 | 0.882138758 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 1 | 7 | 16000 | 0.545000000 | 0.875671865 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 0 | 16000 | 0.537937500 | 0.894489531 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 1 | 16000 | 0.537937500 | 0.894489531 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 2 | 16000 | 0.543562500 | 0.879482166 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 3 | 16000 | 0.538562500 | 0.892814316 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 4 | 16000 | 0.542062500 | 0.883468890 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 5 | 16000 | 0.534062500 | 0.904919508 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 6 | 16000 | 0.550125000 | 0.862168628 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 2 | 7 | 16000 | 0.544500000 | 0.876996046 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 0 | 16000 | 0.541062500 | 0.886132841 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 1 | 16000 | 0.541000000 | 0.886299501 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 2 | 16000 | 0.546437500 | 0.871871601 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 3 | 16000 | 0.543250000 | 0.880311825 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 4 | 16000 | 0.542562500 | 0.882138758 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 5 | 16000 | 0.540312500 | 0.888134036 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 6 | 16000 | 0.542062500 | 0.883468890 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 3 | 7 | 16000 | 0.534000000 | 0.905088353 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 0 | 16000 | 0.545687500 | 0.873853098 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 1 | 16000 | 0.540750000 | 0.886966335 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 2 | 16000 | 0.537562500 | 0.895495595 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 3 | 16000 | 0.538500000 | 0.892981750 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 4 | 16000 | 0.539937500 | 0.889135676 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 5 | 16000 | 0.540125000 | 0.888634769 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 6 | 16000 | 0.537312500 | 0.896166694 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 4 | 7 | 16000 | 0.536125000 | 0.899358684 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 0 | 15000 | 0.537133333 | 0.896647840 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 1 | 15000 | 0.534933333 | 0.902568990 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 2 | 15000 | 0.545133333 | 0.875318955 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 3 | 15000 | 0.543666667 | 0.879205719 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 4 | 15000 | 0.533600000 | 0.906169428 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 5 | 15000 | 0.545066667 | 0.875495399 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 6 | 15000 | 0.542266667 | 0.882925605 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 5 | 7 | 15000 | 0.540733333 | 0.887010801 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 0 | 15000 | 0.547400000 | 0.869332660 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 1 | 15000 | 0.546000000 | 0.873027144 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 2 | 15000 | 0.529400000 | 0.917569900 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 3 | 15000 | 0.539400000 | 0.890572573 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 4 | 15000 | 0.547133333 | 0.870035642 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 5 | 15000 | 0.549666667 | 0.863371102 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 6 | 15000 | 0.536600000 | 0.898081040 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 6 | 7 | 15000 | 0.541933333 | 0.883812707 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 0 | 15000 | 0.542400000 | 0.882570916 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 1 | 15000 | 0.542400000 | 0.882570916 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 2 | 15000 | 0.538733333 | 0.892356762 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 3 | 15000 | 0.540133333 | 0.888612511 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 4 | 15000 | 0.536933333 | 0.897185123 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 5 | 15000 | 0.537933333 | 0.894500706 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 6 | 15000 | 0.537333333 | 0.896110757 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro0_1000x125_strict_20260526.payload | 7 | 7 | 15000 | 0.544533333 | 0.876907729 |
