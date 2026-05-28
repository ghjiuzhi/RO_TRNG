# Formal Restart Output Profile

- rows: `4`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 0.576638000 | 0.794262182 | 8.852511282 | 1.7 | 769 | 0.769000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 0.503005000 | 0.991355354 | 16.058672890 | 50.7 | 557 | 0.557000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 11 | 0.544560000 | 0.876837080 | 8.132428911 | 0.5 | 730 | 0.730000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 11 | 0.501558000 | 0.995511552 | 14.921214294 | 89.3 | 560 | 0.560000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 0 | 16000 | 0.585500000 | 0.772258924 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 1 | 16000 | 0.574000000 | 0.800877358 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 2 | 16000 | 0.568750000 | 0.814133455 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 3 | 16000 | 0.554437500 | 0.850903256 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 4 | 16000 | 0.577812500 | 0.791326680 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 5 | 16000 | 0.588562500 | 0.764732470 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 6 | 16000 | 0.581250000 | 0.782769284 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 7 | 16000 | 0.570312500 | 0.810175441 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 0 | 16000 | 0.567625000 | 0.816989963 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 1 | 16000 | 0.590125000 | 0.760907517 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 2 | 16000 | 0.586812500 | 0.769028492 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 3 | 16000 | 0.578750000 | 0.788987807 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 4 | 16000 | 0.574000000 | 0.800877358 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 5 | 16000 | 0.559937500 | 0.836662292 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 6 | 16000 | 0.572000000 | 0.805912948 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 7 | 16000 | 0.592437500 | 0.755265132 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 0 | 16000 | 0.576125000 | 0.795546232 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 1 | 16000 | 0.566062500 | 0.820966742 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 2 | 16000 | 0.567125000 | 0.818261340 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 3 | 16000 | 0.592062500 | 0.756178616 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 4 | 16000 | 0.589625000 | 0.762130399 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 5 | 16000 | 0.579375000 | 0.787430661 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 6 | 16000 | 0.572250000 | 0.805282537 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 7 | 16000 | 0.561687500 | 0.832160398 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 0 | 16000 | 0.594562500 | 0.750099622 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 1 | 16000 | 0.581937500 | 0.781063879 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 2 | 16000 | 0.573187500 | 0.802920947 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 3 | 16000 | 0.560250000 | 0.835857351 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 4 | 16000 | 0.560125000 | 0.836179274 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 5 | 16000 | 0.587937500 | 0.766265296 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 6 | 16000 | 0.587750000 | 0.766725461 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 7 | 16000 | 0.575687500 | 0.796642208 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 0 | 16000 | 0.563812500 | 0.826712631 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 1 | 16000 | 0.583500000 | 0.777195439 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 2 | 16000 | 0.592687500 | 0.754656464 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 3 | 16000 | 0.583125000 | 0.778122919 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 4 | 16000 | 0.583125000 | 0.778122919 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 5 | 16000 | 0.563687500 | 0.827032519 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 6 | 16000 | 0.558562500 | 0.840209376 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 7 | 16000 | 0.585500000 | 0.772258924 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 0 | 15000 | 0.585066667 | 0.773327070 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 1 | 15000 | 0.569466667 | 0.812316698 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 2 | 15000 | 0.557666667 | 0.842525055 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 3 | 15000 | 0.577533333 | 0.792023878 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 4 | 15000 | 0.588133333 | 0.765784835 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 5 | 15000 | 0.581933333 | 0.781074208 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 6 | 15000 | 0.582000000 | 0.780908942 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 7 | 15000 | 0.568066667 | 0.815867845 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 0 | 15000 | 0.586200000 | 0.770535127 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 1 | 15000 | 0.590600000 | 0.759746738 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 2 | 15000 | 0.582200000 | 0.780413255 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 3 | 15000 | 0.569600000 | 0.811978949 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 4 | 15000 | 0.560066667 | 0.836329529 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 5 | 15000 | 0.580200000 | 0.785377799 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 6 | 15000 | 0.587333333 | 0.767748576 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 7 | 15000 | 0.590666667 | 0.759583897 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 0 | 15000 | 0.553866667 | 0.852389379 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 1 | 15000 | 0.568600000 | 0.814513996 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 2 | 15000 | 0.591200000 | 0.758281825 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 3 | 15000 | 0.577533333 | 0.792023878 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 4 | 15000 | 0.583133333 | 0.778102302 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 5 | 15000 | 0.574333333 | 0.800039799 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 6 | 15000 | 0.562133333 | 0.831015729 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 7 | 15000 | 0.575466667 | 0.797195731 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 0 | 16000 | 0.540250000 | 0.888300928 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 1 | 16000 | 0.561187500 | 0.833445220 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 2 | 16000 | 0.542125000 | 0.883302557 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 3 | 16000 | 0.530062500 | 0.915765616 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 4 | 16000 | 0.549250000 | 0.864465130 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 5 | 16000 | 0.557750000 | 0.842309486 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 6 | 16000 | 0.534500000 | 0.903738147 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 0 | 7 | 16000 | 0.544125000 | 0.877989980 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 0 | 16000 | 0.547312500 | 0.869563288 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 1 | 16000 | 0.538187500 | 0.893819212 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 2 | 16000 | 0.549437500 | 0.863972715 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 3 | 16000 | 0.549937500 | 0.862660428 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 4 | 16000 | 0.536375000 | 0.898686099 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 5 | 16000 | 0.543250000 | 0.880311825 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 6 | 16000 | 0.557250000 | 0.843603383 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 1 | 7 | 16000 | 0.539875000 | 0.889302683 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 0 | 16000 | 0.550937500 | 0.860039430 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 1 | 16000 | 0.554000000 | 0.852042119 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 2 | 16000 | 0.536937500 | 0.897173928 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 3 | 16000 | 0.548875000 | 0.865450466 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 4 | 16000 | 0.549875000 | 0.862824399 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 5 | 16000 | 0.537937500 | 0.894489531 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 6 | 16000 | 0.537750000 | 0.894992475 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 2 | 7 | 16000 | 0.550000000 | 0.862496476 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 0 | 16000 | 0.531375000 | 0.912197741 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 1 | 16000 | 0.547125000 | 0.870057616 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 2 | 16000 | 0.556437500 | 0.845708444 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 3 | 16000 | 0.535687500 | 0.900536463 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 4 | 16000 | 0.548937500 | 0.865286196 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 5 | 16000 | 0.549687500 | 0.863316422 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 6 | 16000 | 0.542437500 | 0.882471176 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 3 | 7 | 16000 | 0.530937500 | 0.913386053 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 0 | 16000 | 0.540250000 | 0.888300928 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 1 | 16000 | 0.533625000 | 0.906101837 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 2 | 16000 | 0.542062500 | 0.883468890 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 3 | 16000 | 0.550312500 | 0.861676996 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 4 | 16000 | 0.539562500 | 0.890138012 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 5 | 16000 | 0.539375000 | 0.890639441 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 6 | 16000 | 0.553437500 | 0.853507693 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 4 | 7 | 16000 | 0.541812500 | 0.884134417 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 0 | 15000 | 0.546866667 | 0.870738967 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 1 | 15000 | 0.545800000 | 0.873555700 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 2 | 15000 | 0.545066667 | 0.875495399 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 3 | 15000 | 0.543533333 | 0.879559581 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 4 | 15000 | 0.553933333 | 0.852215739 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 5 | 15000 | 0.545466667 | 0.874437058 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 6 | 15000 | 0.548466667 | 0.866524152 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 5 | 7 | 15000 | 0.546533333 | 0.871618606 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 0 | 15000 | 0.543000000 | 0.880975897 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 1 | 15000 | 0.540133333 | 0.888612511 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 2 | 15000 | 0.543400000 | 0.879913529 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 3 | 15000 | 0.539533333 | 0.890216000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 4 | 15000 | 0.535333333 | 0.901490608 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 5 | 15000 | 0.545200000 | 0.875142533 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 6 | 15000 | 0.551600000 | 0.858305638 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 6 | 7 | 15000 | 0.541333333 | 0.885410868 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 0 | 15000 | 0.552333333 | 0.856388898 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 1 | 15000 | 0.538666667 | 0.892535303 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 2 | 15000 | 0.542266667 | 0.882925605 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 3 | 15000 | 0.552733333 | 0.855344476 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 4 | 15000 | 0.548933333 | 0.865297147 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 5 | 15000 | 0.538600000 | 0.892713865 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 6 | 15000 | 0.546733333 | 0.871090758 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_data_ro3_1000x125_strict_20260528_ro3_warmup_neighbors.payload | 7 | 7 | 15000 | 0.546933333 | 0.870563104 |
