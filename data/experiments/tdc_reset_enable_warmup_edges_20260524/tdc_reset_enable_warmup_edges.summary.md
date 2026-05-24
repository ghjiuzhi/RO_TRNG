# TDC Startup Diffusion Summary

Offline analysis of existing TDC UART captures. No RTL, Vivado, COM, JTAG, or hardware queue access is used.

## Method

- Decode raw TDC UART frames with the same 8-byte `0xA5` packet format used by `scripts/analyze_tdc_uart.py`, or read existing `.tdc_packets.csv` files.
- Compute entropy on lane A bins, lane B bins, and signed wrapped `A-B` differential bins.
- Treat the first `--early-packets` packets as the startup slice, and the first `--window-packets` packets as the first-window comparator against all later packets.
- `warmup H(diff)` is computed from each requested `--warmup-starts` offset after the enable edge, using the same `--early-packets` window length.
- Transition entropy is measured on consecutive differential-bin pairs; residence metrics summarize consecutive runs of identical differential bins.

## Run Summary

| label | run | enable edge | post packets | warmup start | H(diff) | early H(diff) | warmup H(diff) | transition H(diff) | warmup transition H(diff) | same diff ratio | warmup same ratio | longest diff run | warmup longest run | diff autocorr | first-later H(diff) | first-later TVD(diff) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_reset_enable_random1_baseline_ro0_2mib | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 4 | 6.67227 | 6.54038 | 6.54241 | 13.2961 | 9.86074 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| tdc_reset_enable_random1_baseline_ro0_2mib | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 5 | 6.67227 | 6.54038 | 6.54241 | 13.2961 | 9.86074 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| tdc_reset_enable_random1_baseline_ro0_2mib | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 10 | 6.67227 | 6.54038 | 6.54124 | 13.2961 | 9.85683 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| tdc_reset_enable_random1_baseline_ro0_2mib | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 11 | 6.67227 | 6.54038 | 6.54004 | 13.2961 | 9.85683 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| tdc_reset_enable_random1_baseline_ro0_2mib | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 12 | 6.67227 | 6.54038 | 6.54209 | 13.2961 | 9.85683 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 4 | 6.67673 | 6.55711 | 6.55718 | 13.3062 | 9.84901 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 5 | 6.67673 | 6.55711 | 6.55907 | 13.3062 | 9.85097 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 10 | 6.67673 | 6.55711 | 6.55816 | 13.3062 | 9.85097 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 11 | 6.67673 | 6.55711 | 6.55567 | 13.3062 | 9.85097 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 12 | 6.67673 | 6.55711 | 6.55446 | 13.3062 | 9.85097 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| tdc_reset_enable_random1_sampler_local_ro0_2mib | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 4 | 6.71817 | 6.60532 | 6.60164 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |
| tdc_reset_enable_random1_sampler_local_ro0_2mib | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 5 | 6.71817 | 6.60532 | 6.60328 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |
| tdc_reset_enable_random1_sampler_local_ro0_2mib | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 10 | 6.71817 | 6.60532 | 6.60498 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |
| tdc_reset_enable_random1_sampler_local_ro0_2mib | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 11 | 6.71817 | 6.60532 | 6.60469 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |
| tdc_reset_enable_random1_sampler_local_ro0_2mib | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 12 | 6.71817 | 6.60532 | 6.60266 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 4 | 6.71952 | 6.64656 | 6.64656 | 13.3913 | 9.88273 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 5 | 6.71952 | 6.64656 | 6.6444 | 13.3913 | 9.88273 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 10 | 6.71952 | 6.64656 | 6.64365 | 13.3913 | 9.88273 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 11 | 6.71952 | 6.64656 | 6.64331 | 13.3913 | 9.88077 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 12 | 6.71952 | 6.64656 | 6.64163 | 13.3913 | 9.88077 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 4 | 6.60639 | 6.47378 | 6.47622 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 5 | 6.60639 | 6.47378 | 6.47724 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 10 | 6.60639 | 6.47378 | 6.47473 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 11 | 6.60639 | 6.47378 | 6.4738 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 12 | 6.60639 | 6.47378 | 6.47196 | 13.167 | 9.80891 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 4 | 6.60514 | 6.50542 | 6.50869 | 13.1651 | 9.87907 | 0.0123049 | 0.0156403 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 5 | 6.60514 | 6.50542 | 6.51 | 13.1651 | 9.87907 | 0.0123049 | 0.0156403 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 10 | 6.60514 | 6.50542 | 6.50904 | 13.1651 | 9.88103 | 0.0123049 | 0.0136852 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 11 | 6.60514 | 6.50542 | 6.50887 | 13.1651 | 9.88103 | 0.0123049 | 0.0136852 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 12 | 6.60514 | 6.50542 | 6.50871 | 13.1651 | 9.88103 | 0.0123049 | 0.0136852 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 4 | 6.70052 | 6.63186 | 6.63515 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 5 | 6.70052 | 6.63186 | 6.63421 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 10 | 6.70052 | 6.63186 | 6.63071 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 11 | 6.70052 | 6.63186 | 6.63132 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 12 | 6.70052 | 6.63186 | 6.63209 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 4 | 6.70189 | 6.63041 | 6.62963 | 13.3589 | 9.90597 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 5 | 6.70189 | 6.63041 | 6.63058 | 13.3589 | 9.90597 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 10 | 6.70189 | 6.63041 | 6.6362 | 13.3589 | 9.90792 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 11 | 6.70189 | 6.63041 | 6.63653 | 13.3589 | 9.90792 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 12 | 6.70189 | 6.63041 | 6.63395 | 13.3589 | 9.90792 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |
| tdc_reset_enable_random3_goodref_ro0_2mib | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 4 | 6.6945 | 6.58148 | 6.5826 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| tdc_reset_enable_random3_goodref_ro0_2mib | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 5 | 6.6945 | 6.58148 | 6.5826 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| tdc_reset_enable_random3_goodref_ro0_2mib | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 10 | 6.6945 | 6.58148 | 6.58238 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| tdc_reset_enable_random3_goodref_ro0_2mib | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 11 | 6.6945 | 6.58148 | 6.58332 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| tdc_reset_enable_random3_goodref_ro0_2mib | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 12 | 6.6945 | 6.58148 | 6.58243 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 4 | 6.69607 | 6.63509 | 6.63328 | 13.3488 | 9.90523 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 5 | 6.69607 | 6.63509 | 6.63629 | 13.3488 | 9.90523 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 10 | 6.69607 | 6.63509 | 6.63884 | 13.3488 | 9.90718 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 11 | 6.69607 | 6.63509 | 6.64024 | 13.3488 | 9.90718 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 12 | 6.69607 | 6.63509 | 6.64063 | 13.3488 | 9.90914 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| tdc_reset_enable_random3_goodref_ro3_2mib | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 4 | 6.67248 | 6.54411 | 6.54416 | 13.2987 | 9.85023 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| tdc_reset_enable_random3_goodref_ro3_2mib | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 5 | 6.67248 | 6.54411 | 6.54244 | 13.2987 | 9.85023 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| tdc_reset_enable_random3_goodref_ro3_2mib | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 10 | 6.67248 | 6.54411 | 6.54609 | 13.2987 | 9.84827 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| tdc_reset_enable_random3_goodref_ro3_2mib | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 11 | 6.67248 | 6.54411 | 6.54632 | 13.2987 | 9.84827 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| tdc_reset_enable_random3_goodref_ro3_2mib | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 12 | 6.67248 | 6.54411 | 6.54869 | 13.2987 | 9.84827 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 4 | 6.67484 | 6.55376 | 6.55468 | 13.3026 | 9.86391 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |
| tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 5 | 6.67484 | 6.55376 | 6.55447 | 13.3026 | 9.86391 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |
| tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 10 | 6.67484 | 6.55376 | 6.55073 | 13.3026 | 9.86391 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |
| tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 11 | 6.67484 | 6.55376 | 6.54846 | 13.3026 | 9.86391 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |
| tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 12 | 6.67484 | 6.55376 | 6.54804 | 13.3026 | 9.86196 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |

## Window Output

- summary rows: `60`
- window rows: `192`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
