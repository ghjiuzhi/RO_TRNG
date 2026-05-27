# Formal Restart Output Profile

- rows: `3`

## Summary

| label | warmup | p1 | min-H | row ones std | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup5_all640_1000x125_strict_20260526.payload | 5 | 0.499323000 | 0.998047912 | 16.052123567 | 27.3 | 560 | 0.440000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 10 | 0.458617000 | 0.885278509 | 16.927737917 | 83.7 | 590 | 0.410000000 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 11 | 0.470488000 | 0.917264715 | 15.721763769 | 2.0 | 584 | 0.416000000 |

## Byte-Phase Aggregate

This groups positions by `byte_index % 8`. A strong pattern here would indicate an output-packing or periodic byte-position effect.

| label | phase | bit | samples | p1 | min-H |
| --- | ---: | ---: | ---: | ---: | ---: |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 0 | 16000 | 0.459812500 | 0.888467839 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 1 | 16000 | 0.459187500 | 0.886799597 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 2 | 16000 | 0.456875000 | 0.880643823 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 3 | 16000 | 0.458812500 | 0.885799578 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 4 | 16000 | 0.461625000 | 0.893316676 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 5 | 16000 | 0.457812500 | 0.883136242 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 6 | 16000 | 0.453687500 | 0.872201662 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 0 | 7 | 16000 | 0.453875000 | 0.872696894 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 0 | 16000 | 0.457687500 | 0.882803671 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 1 | 16000 | 0.462937500 | 0.896838105 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 2 | 16000 | 0.460312500 | 0.889803822 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 3 | 16000 | 0.457375000 | 0.881972577 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 4 | 16000 | 0.461375000 | 0.892646902 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 5 | 16000 | 0.456812500 | 0.880477815 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 6 | 16000 | 0.454875000 | 0.875341010 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 1 | 7 | 16000 | 0.458062500 | 0.883801615 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 0 | 16000 | 0.454875000 | 0.875341010 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 1 | 16000 | 0.463437500 | 0.898181866 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 2 | 16000 | 0.462125000 | 0.894657160 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 3 | 16000 | 0.465937500 | 0.904919508 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 4 | 16000 | 0.461875000 | 0.893986762 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 5 | 16000 | 0.460187500 | 0.889469710 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 6 | 16000 | 0.464625000 | 0.901378323 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 2 | 7 | 16000 | 0.452937500 | 0.870222430 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 0 | 16000 | 0.464250000 | 0.900368150 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 1 | 16000 | 0.454562500 | 0.874514203 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 2 | 16000 | 0.458437500 | 0.884800251 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 3 | 16000 | 0.457500000 | 0.882304957 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 4 | 16000 | 0.455500000 | 0.876996046 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 5 | 16000 | 0.462875000 | 0.896670223 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 6 | 16000 | 0.468250000 | 0.911179967 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 3 | 7 | 16000 | 0.458000000 | 0.883635243 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 0 | 16000 | 0.454562500 | 0.874514203 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 1 | 16000 | 0.456812500 | 0.880477815 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 2 | 16000 | 0.450312500 | 0.863316422 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 3 | 16000 | 0.462875000 | 0.896670223 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 4 | 16000 | 0.455875000 | 0.877989980 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 5 | 16000 | 0.453812500 | 0.872531798 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 6 | 16000 | 0.457312500 | 0.881806416 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 4 | 7 | 16000 | 0.456687500 | 0.880145855 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 0 | 15000 | 0.453333333 | 0.871266686 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 1 | 15000 | 0.453066667 | 0.870563104 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 2 | 15000 | 0.460866667 | 0.891285984 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 3 | 15000 | 0.460800000 | 0.891107598 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 4 | 15000 | 0.461866667 | 0.893964421 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 5 | 15000 | 0.453266667 | 0.871090758 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 6 | 15000 | 0.464533333 | 0.901131326 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 5 | 7 | 15000 | 0.468333333 | 0.911406077 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 0 | 15000 | 0.460266667 | 0.889681306 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 1 | 15000 | 0.452666667 | 0.869508374 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 2 | 15000 | 0.451266667 | 0.865822879 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 3 | 15000 | 0.461400000 | 0.892713865 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 4 | 15000 | 0.461600000 | 0.893249685 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 5 | 15000 | 0.455333333 | 0.876554517 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 6 | 15000 | 0.461400000 | 0.892713865 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 6 | 7 | 15000 | 0.456066667 | 0.878498255 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 0 | 15000 | 0.463333333 | 0.897901812 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 1 | 15000 | 0.461000000 | 0.891642822 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 2 | 15000 | 0.461866667 | 0.893964421 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 3 | 15000 | 0.457933333 | 0.883457801 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 4 | 15000 | 0.457333333 | 0.881861801 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 5 | 15000 | 0.456600000 | 0.879913529 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 6 | 15000 | 0.453733333 | 0.872322703 |
| restart_reduced_xor_random1_sampler_island_local_warmup10_all640_1000x125_strict_20260526.payload | 7 | 7 | 15000 | 0.458866667 | 0.885943982 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 0 | 16000 | 0.476000000 | 0.932361283 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 1 | 16000 | 0.472062500 | 0.921560949 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 2 | 16000 | 0.469687500 | 0.915085340 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 3 | 16000 | 0.464562500 | 0.901209912 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 4 | 16000 | 0.471500000 | 0.920024623 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 5 | 16000 | 0.464187500 | 0.900199857 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 6 | 16000 | 0.473125000 | 0.924467369 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 0 | 7 | 16000 | 0.474125000 | 0.927208182 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 0 | 16000 | 0.471187500 | 0.919171815 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 1 | 16000 | 0.472000000 | 0.921390165 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 2 | 16000 | 0.469437500 | 0.914405385 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 3 | 16000 | 0.475437500 | 0.930813419 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 4 | 16000 | 0.467437500 | 0.908977249 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 5 | 16000 | 0.469750000 | 0.915255379 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 6 | 16000 | 0.474500000 | 0.928237331 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 1 | 7 | 16000 | 0.474812500 | 0.929095516 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 0 | 16000 | 0.463687500 | 0.898854216 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 1 | 16000 | 0.468500000 | 0.911858403 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 2 | 16000 | 0.474562500 | 0.928408927 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 3 | 16000 | 0.475625000 | 0.931329189 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 4 | 16000 | 0.470187500 | 0.916446213 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 5 | 16000 | 0.471750000 | 0.920707233 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 6 | 16000 | 0.465750000 | 0.904413092 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 2 | 7 | 16000 | 0.472500000 | 0.922757001 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 0 | 16000 | 0.467125000 | 0.908130945 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 1 | 16000 | 0.465750000 | 0.904413092 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 2 | 16000 | 0.469312500 | 0.914065527 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 3 | 16000 | 0.459937500 | 0.888801719 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 4 | 16000 | 0.475062500 | 0.929782432 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 5 | 16000 | 0.471562500 | 0.920195245 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 6 | 16000 | 0.471500000 | 0.920024623 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 3 | 7 | 16000 | 0.472750000 | 0.923440905 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 0 | 16000 | 0.470375000 | 0.916956871 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 1 | 16000 | 0.469000000 | 0.913216234 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 2 | 16000 | 0.467625000 | 0.909485270 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 3 | 16000 | 0.470812500 | 0.918149111 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 4 | 16000 | 0.466687500 | 0.906946952 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 5 | 16000 | 0.467937500 | 0.910332370 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 6 | 16000 | 0.472687500 | 0.923269899 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 4 | 7 | 16000 | 0.470250000 | 0.916616412 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 0 | 15000 | 0.474800000 | 0.929061179 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 1 | 15000 | 0.472866667 | 0.923760171 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 2 | 15000 | 0.467666667 | 0.909598188 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 3 | 15000 | 0.476933333 | 0.934933260 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 4 | 15000 | 0.468066667 | 0.910682649 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 5 | 15000 | 0.469200000 | 0.913759724 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 6 | 15000 | 0.464400000 | 0.900772134 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 5 | 7 | 15000 | 0.472133333 | 0.921754528 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 0 | 15000 | 0.469533333 | 0.914665997 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 1 | 15000 | 0.471066667 | 0.918842198 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 2 | 15000 | 0.471533333 | 0.920115619 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 3 | 15000 | 0.468933333 | 0.913035116 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 4 | 15000 | 0.473333333 | 0.925037942 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 5 | 15000 | 0.468666667 | 0.912310871 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 6 | 15000 | 0.470000000 | 0.915935735 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 6 | 7 | 15000 | 0.465266667 | 0.903108483 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 0 | 15000 | 0.474266667 | 0.927596885 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 1 | 15000 | 0.465000000 | 0.902389203 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 2 | 15000 | 0.470533333 | 0.917388235 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 3 | 15000 | 0.471266667 | 0.919387812 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 4 | 15000 | 0.476800000 | 0.934565554 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 5 | 15000 | 0.471933333 | 0.921208018 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 6 | 15000 | 0.471866667 | 0.921025894 |
| restart_reduced_xor_random1_sampler_island_local_warmup11_all640_1000x125_strict_20260526.payload | 7 | 7 | 15000 | 0.475000000 | 0.929610672 |
