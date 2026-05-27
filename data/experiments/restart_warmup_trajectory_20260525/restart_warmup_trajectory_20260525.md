# Restart Warmup Trajectory 20260525

This is an offline analysis over packed-byte restart summaries. It asks whether warmup reduces fixed-position startup hotspots or merely changes the expanded SP800-90B column number.

## Warmup Summary

| family | warmup | runs | mean p1 | mean worst_x | max worst_x | mean worst byte | early-byte runs | class counts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| random1_reverse_repair_sample_ro_compact | 4 | 1 | 0.499754 | 552 | 552 | 109 | 0/1 | weak:1 |
| random1_sampler_regs_only | 0 | 2 | 0.498785 | 779 | 802 | 1 | 2/2 | severe:2 |
| random1_sampler_regs_only | 4 | 2 | 0.407536 | 742 | 751 | 0.5 | 2/2 | severe:2 |
| random1_sampler_regs_only | 5 | 2 | 0.498248 | 559.5 | 561 | 107.5 | 0/2 | weak:2 |
| random1_sampler_regs_only | 6 | 2 | 0.49681 | 552.5 | 554 | 66 | 0/2 | weak:2 |
| random1_sampler_regs_only | 8 | 2 | 0.483511 | 561 | 564 | 41.5 | 1/2 | early_position_weak:1;weak:1 |
| random1_sampler_regs_only | 10 | 2 | 0.499596 | 556 | 565 | 64.5 | 0/2 | weak:2 |
| random1_sampler_regs_only | 11 | 2 | 0.559007 | 615.5 | 618 | 69 | 0/2 | strong:2 |
| random1_sampler_regs_only | 12 | 2 | 0.452978 | 605 | 609 | 4 | 2/2 | strong:2 |
| random1_sampler_regs_only | 16 | 1 | 0.466933 | 586 | 586 | 60 | 0/1 | moderate:1 |
| random3_formal | 0 | 2 | 0.49786 | 682.5 | 685 | 1 | 2/2 | severe:2 |
| random3_formal | 8 | 1 | 0.374385 | 721 | 721 | 2 | 1/1 | severe:1 |
| random3_formal | 10 | 3 | 0.415083 | 638 | 650 | 2.67 | 3/3 | severe:1;strong:2 |
| random3_formal | 11 | 3 | 0.46868 | 588.667 | 595 | 23 | 2/3 | moderate:3 |
| random3_formal | 12 | 3 | 0.499444 | 553.667 | 562 | 80.33 | 0/3 | weak:3 |
| random3_formal | 16 | 1 | 0.499126 | 547 | 547 | 43 | 0/1 | weak:1 |

## Per-Run Hotspots

| family | warmup | label | worst byte.bit | worst_x | worst_p1 | MSB col | LSB col | class |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| random1_reverse_repair_sample_ro_compact | 4 | restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run02_20260525 | 109.4 | 552 | 0.448 | 875 | 876 | weak |
| random1_sampler_regs_only | 0 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup0_header_delay60s_run01_20260524 | 1.6 | 756 | 0.756 | 9 | 14 | severe |
| random1_sampler_regs_only | 0 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup0_header_delay60s_run02_20260524 | 1.7 | 802 | 0.802 | 8 | 15 | severe |
| random1_sampler_regs_only | 4 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup4_header_delay60s_repeat02_20260524 | 0.2 | 733 | 0.267 | 5 | 2 | severe |
| random1_sampler_regs_only | 4 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup4_header_delay60s_sweep01_20260524 | 1.6 | 751 | 0.249 | 9 | 14 | severe |
| random1_sampler_regs_only | 5 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup5_header_delay60s_edge01_20260524 | 111.2 | 558 | 0.442 | 893 | 890 | weak |
| random1_sampler_regs_only | 5 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup5_header_delay60s_repeat02_20260524 | 104.4 | 561 | 0.561 | 835 | 836 | weak |
| random1_sampler_regs_only | 6 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup6_header_delay60s_passband01_20260524 | 24.4 | 551 | 0.449 | 195 | 196 | weak |
| random1_sampler_regs_only | 6 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup6_header_delay60s_repeat02_20260524 | 108.7 | 554 | 0.446 | 864 | 871 | weak |
| random1_sampler_regs_only | 8 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_repeat02_20260524 | 0.3 | 558 | 0.442 | 4 | 3 | early_position_weak |
| random1_sampler_regs_only | 8 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_sweep01_20260524 | 83.0 | 564 | 0.436 | 671 | 664 | weak |
| random1_sampler_regs_only | 10 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_passband01_20260524 | 115.3 | 565 | 0.435 | 924 | 923 | weak |
| random1_sampler_regs_only | 10 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_repeat02_20260524 | 14.1 | 547 | 0.453 | 118 | 113 | weak |
| random1_sampler_regs_only | 11 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_edge01_20260524 | 81.4 | 613 | 0.613 | 651 | 652 | strong |
| random1_sampler_regs_only | 11 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_repeat02_20260524 | 57.2 | 618 | 0.618 | 461 | 458 | strong |
| random1_sampler_regs_only | 12 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_run01_20260524 | 2.7 | 609 | 0.391 | 16 | 23 | strong |
| random1_sampler_regs_only | 12 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_run02_20260524 | 6.1 | 601 | 0.399 | 54 | 49 | strong |
| random1_sampler_regs_only | 16 | random1_sampler_regs_only_restart_auto_formal_bits_1000x125_warmup16_header_delay60s_sweep01_20260524 | 60.3 | 586 | 0.414 | 484 | 483 | moderate |
| random3_formal | 0 | random3_restart_auto_formal_bits_1000x125_header_delay60s_20260515 | 0.0 | 685 | 0.315 | 7 | 0 | severe |
| random3_formal | 0 | random3_restart_auto_formal_bits_1000x125_header_delay60s_repeat02_20260515 | 2.7 | 680 | 0.68 | 16 | 23 | severe |
| random3_formal | 8 | random3_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_20260515 | 2.2 | 721 | 0.279 | 21 | 18 | severe |
| random3_formal | 10 | random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_20260515 | 1.4 | 650 | 0.35 | 11 | 12 | severe |
| random3_formal | 10 | random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_repeat02_20260515 | 6.0 | 633 | 0.367 | 55 | 48 | strong |
| random3_formal | 10 | random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_repeat03_20260522_20260515 | 1.6 | 631 | 0.369 | 9 | 14 | strong |
| random3_formal | 11 | random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_20260515 | 1.3 | 583 | 0.417 | 12 | 11 | moderate |
| random3_formal | 11 | random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_repeat02_20260515 | 68.3 | 588 | 0.412 | 548 | 547 | moderate |
| random3_formal | 11 | random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_repeat03_20260522_20260515 | 0.5 | 595 | 0.405 | 2 | 5 | moderate |
| random3_formal | 12 | random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_20260515 | 88.3 | 562 | 0.562 | 708 | 707 | weak |
| random3_formal | 12 | random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_repeat02_20260515 | 118.1 | 549 | 0.451 | 950 | 945 | weak |
| random3_formal | 12 | random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_repeat03_20260522_20260515 | 35.0 | 550 | 0.45 | 287 | 280 | weak |
| random3_formal | 16 | random3_restart_auto_formal_bits_1000x125_warmup16_header_delay60s_20260515 | 43.7 | 547 | 0.547 | 344 | 351 | weak |

## Interpretation

- Early-byte severe hotspots support a startup-transient interpretation: restart exposes fixed output positions near the beginning of the stream.
- If warmup reduces `worst_x` and moves hotspots away from early bytes, it supports the claim that warmup lets the sampler/data phase relation diffuse before SP800-90B columns are formed.
- If later warmups remain biased but the hotspot moves, the safer wording is multiple biased fixed positions in a startup/passband structure, not a single immutable bad column.
- These are packed-position statements, not FPGA physical column statements; the packing counterfactual shows expanded column numbers depend on bit order.
