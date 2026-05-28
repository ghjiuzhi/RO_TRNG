# Formal Restart Output Profile

- rows: `1`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line6_repeat02.payload | 10 | 0.487182000 | 0.963481193 | 15.410349639 | 0.3 | 714 | 0.286000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line6_repeat02.payload | 0 | 3 | 16000 | 0.469562500 | 0.914745323 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line6_repeat02.payload | 0 | 4 | 16000 | 0.478750000 | 0.939952616 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_line6_1000x125_strict_20260528_line6_repeat02.payload | 4 | 7 | 16000 | 0.479687500 | 0.942549728 |
