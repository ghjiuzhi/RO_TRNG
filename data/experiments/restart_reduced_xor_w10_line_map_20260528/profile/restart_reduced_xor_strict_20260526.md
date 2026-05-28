# Formal Restart Output Profile

- rows: `8`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line0_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.499648000 | 0.998984700 | 14.526737280 | 0.1 | 652 | 0.348000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line1_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.499561000 | 0.998733870 | 15.144315072 | 2.0 | 658 | 0.658000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line2_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.500273000 | 0.999212503 | 16.223762541 | 1.3 | 583 | 0.417000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line3_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.500945000 | 0.997275880 | 15.685278926 | 1.6 | 665 | 0.665000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line4_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.501004000 | 0.997105973 | 14.119135384 | 0.3 | 618 | 0.618000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line5_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.500182000 | 0.999474955 | 14.666317738 | 0.0 | 560 | 0.560000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.486473000 | 0.961487963 | 15.810922522 | 0.3 | 701 | 0.299000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line7_1000x125_strict_20260528_line_w10_map.payload | 10 | 0.500176000 | 0.999492261 | 13.930865874 | 0.4 | 585 | 0.585000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line_w10_map.payload | 0 | 4 | 16000 | 0.479375000 | 0.941683504 |
