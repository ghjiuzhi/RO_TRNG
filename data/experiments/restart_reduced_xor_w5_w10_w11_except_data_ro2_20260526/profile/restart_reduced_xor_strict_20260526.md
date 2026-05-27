# Formal Restart Output Profile

- rows: `3`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 0.599459000 | 0.738267011 | 19.267026730 | 6.4 | 654 | 0.654000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_except_data_ro2_1000x125_strict_20260526.payload | 10 | 0.499674000 | 0.999059669 | 16.104028192 | 121.7 | 557 | 0.557000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 11 | 0.669279000 | 0.579320347 | 17.756665199 | 65.3 | 718 | 0.718000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 0 | 16000 | 0.601875000 | 0.732464202 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 1 | 16000 | 0.598062500 | 0.741631835 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 2 | 16000 | 0.598062500 | 0.741631835 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 3 | 16000 | 0.598125000 | 0.741481075 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 4 | 16000 | 0.600437500 | 0.735914012 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 5 | 16000 | 0.603250000 | 0.729172084 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 6 | 16000 | 0.603500000 | 0.728574324 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 0 | 7 | 16000 | 0.600812500 | 0.735013266 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 0 | 16000 | 0.603687500 | 0.728126166 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 1 | 16000 | 0.598312500 | 0.741028891 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 2 | 16000 | 0.603812500 | 0.727827471 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 3 | 16000 | 0.602437500 | 0.731116518 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 4 | 16000 | 0.595375000 | 0.748129451 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 5 | 16000 | 0.592375000 | 0.755417339 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 6 | 16000 | 0.601812500 | 0.732614022 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 1 | 7 | 16000 | 0.596687500 | 0.744952541 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 0 | 16000 | 0.592750000 | 0.754504337 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 1 | 16000 | 0.602812500 | 0.730218762 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 2 | 16000 | 0.602687500 | 0.730517952 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 3 | 16000 | 0.604812500 | 0.725440138 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 4 | 16000 | 0.596375000 | 0.745708314 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 5 | 16000 | 0.602437500 | 0.731116518 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 6 | 16000 | 0.605750000 | 0.723205595 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 2 | 7 | 16000 | 0.595000000 | 0.749038426 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 0 | 16000 | 0.604000000 | 0.727379545 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 1 | 16000 | 0.599750000 | 0.737566842 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 2 | 16000 | 0.595250000 | 0.748432379 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 3 | 16000 | 0.595750000 | 0.747221048 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 4 | 16000 | 0.602625000 | 0.730667570 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 5 | 16000 | 0.595562500 | 0.747675178 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 6 | 16000 | 0.599125000 | 0.739071060 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 3 | 7 | 16000 | 0.601062500 | 0.734413081 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 0 | 16000 | 0.596375000 | 0.745708314 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 1 | 16000 | 0.597750000 | 0.742385870 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 2 | 16000 | 0.603750000 | 0.727976811 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 3 | 16000 | 0.595625000 | 0.747523786 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 4 | 16000 | 0.600250000 | 0.736364596 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 5 | 16000 | 0.600000000 | 0.736965594 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 6 | 16000 | 0.596062500 | 0.746464483 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 4 | 7 | 16000 | 0.602875000 | 0.730069190 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 0 | 15000 | 0.601400000 | 0.733603227 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 1 | 15000 | 0.604666667 | 0.725788045 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 2 | 15000 | 0.601200000 | 0.734083086 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 3 | 15000 | 0.601266667 | 0.733923115 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 4 | 15000 | 0.597000000 | 0.744197163 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 5 | 15000 | 0.594400000 | 0.750493979 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 6 | 15000 | 0.598133333 | 0.741460975 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 5 | 7 | 15000 | 0.606200000 | 0.722134243 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 0 | 15000 | 0.596733333 | 0.744841727 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 1 | 15000 | 0.598133333 | 0.741460975 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 2 | 15000 | 0.599200000 | 0.738890471 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 3 | 15000 | 0.598800000 | 0.739853873 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 4 | 15000 | 0.601333333 | 0.733763162 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 5 | 15000 | 0.597600000 | 0.742747947 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 6 | 15000 | 0.591266667 | 0.758119149 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 6 | 7 | 15000 | 0.594466667 | 0.750332178 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 0 | 15000 | 0.599800000 | 0.737446573 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 1 | 15000 | 0.603200000 | 0.729291666 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 2 | 15000 | 0.597000000 | 0.744197163 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 3 | 15000 | 0.605933333 | 0.722769022 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 4 | 15000 | 0.598200000 | 0.741300184 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 5 | 15000 | 0.600266667 | 0.736324539 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 6 | 15000 | 0.597200000 | 0.743713929 |
| restart_reduced_xor_random1_sampler_island_local_warmup5_except_data_ro2_1000x125_strict_20260526.payload | 7 | 7 | 15000 | 0.594333333 | 0.750655798 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 0 | 16000 | 0.666875000 | 0.584511729 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 1 | 16000 | 0.669125000 | 0.579652347 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 2 | 16000 | 0.663187500 | 0.592511280 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 3 | 16000 | 0.674562500 | 0.567975976 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 4 | 16000 | 0.672187500 | 0.573064380 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 5 | 16000 | 0.663812500 | 0.591152298 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 6 | 16000 | 0.668312500 | 0.581405237 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 0 | 7 | 16000 | 0.671750000 | 0.574003679 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 0 | 16000 | 0.664812500 | 0.588980587 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 1 | 16000 | 0.673187500 | 0.570919706 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 2 | 16000 | 0.669875000 | 0.578036184 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 3 | 16000 | 0.665750000 | 0.586947571 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 4 | 16000 | 0.672062500 | 0.573332689 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 5 | 16000 | 0.673875000 | 0.569447090 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 6 | 16000 | 0.663750000 | 0.591288139 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 1 | 7 | 16000 | 0.669375000 | 0.579113425 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 0 | 16000 | 0.665437500 | 0.587624925 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 1 | 16000 | 0.663375000 | 0.592103451 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 2 | 16000 | 0.668687500 | 0.580595946 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 3 | 16000 | 0.673437500 | 0.570384036 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 4 | 16000 | 0.666187500 | 0.585999811 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 5 | 16000 | 0.669750000 | 0.578305419 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 6 | 16000 | 0.679875000 | 0.556658574 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 2 | 7 | 16000 | 0.665812500 | 0.586812139 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 0 | 16000 | 0.670562500 | 0.576556290 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 1 | 16000 | 0.670250000 | 0.577228781 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 2 | 16000 | 0.676062500 | 0.564771469 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 3 | 16000 | 0.668187500 | 0.581675101 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 4 | 16000 | 0.667625000 | 0.582890116 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 5 | 16000 | 0.672562500 | 0.572259754 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 6 | 16000 | 0.669937500 | 0.577901585 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 3 | 7 | 16000 | 0.667687500 | 0.582755064 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 0 | 16000 | 0.667375000 | 0.583430451 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 1 | 16000 | 0.665062500 | 0.588438169 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 2 | 16000 | 0.663625000 | 0.591559859 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 3 | 16000 | 0.665687500 | 0.587083017 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 4 | 16000 | 0.670437500 | 0.576825248 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 5 | 16000 | 0.666687500 | 0.584917417 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 6 | 16000 | 0.668000000 | 0.582079992 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 4 | 7 | 16000 | 0.669000000 | 0.579921884 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 0 | 15000 | 0.670333333 | 0.577049419 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 1 | 15000 | 0.665200000 | 0.588139926 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 2 | 15000 | 0.674133333 | 0.568894132 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 3 | 15000 | 0.671266667 | 0.575042091 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 4 | 15000 | 0.669600000 | 0.578628567 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 5 | 15000 | 0.664200000 | 0.590310372 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 6 | 15000 | 0.666800000 | 0.584673991 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 5 | 7 | 15000 | 0.674666667 | 0.567753211 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 0 | 15000 | 0.669200000 | 0.579490650 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 1 | 15000 | 0.669533333 | 0.578772212 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 2 | 15000 | 0.673800000 | 0.569607666 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 3 | 15000 | 0.670866667 | 0.575902033 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 4 | 15000 | 0.669666667 | 0.578484937 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 5 | 15000 | 0.662466667 | 0.594080231 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 6 | 15000 | 0.672333333 | 0.572751417 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 6 | 7 | 15000 | 0.671733333 | 0.574039474 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 0 | 15000 | 0.670666667 | 0.576332196 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 1 | 15000 | 0.678733333 | 0.559083228 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 2 | 15000 | 0.669800000 | 0.578197719 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 3 | 15000 | 0.671666667 | 0.574182662 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 4 | 15000 | 0.671466667 | 0.574612313 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 5 | 15000 | 0.669066667 | 0.579778125 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 6 | 15000 | 0.668066667 | 0.581936018 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_except_data_ro2_1000x125_strict_20260526.payload | 7 | 7 | 15000 | 0.665933333 | 0.586550339 |
