# TDC Startup Diffusion Summary

Offline analysis of existing TDC UART captures. No RTL, Vivado, COM, JTAG, or hardware queue access is used.

## Method

- Decode raw TDC UART frames with the same 8-byte `0xA5` packet format used by `scripts/analyze_tdc_uart.py`, or read existing `.tdc_packets.csv` files.
- Compute entropy on lane A bins, lane B bins, and signed wrapped `A-B` differential bins.
- Treat the first `--early-packets` packets as the startup slice, and the first `--window-packets` packets as the first-window comparator against all later packets.
- Transition entropy is measured on consecutive differential-bin pairs; residence metrics summarize consecutive runs of identical differential bins.

## Run Summary

| label | run | enable edge | post packets | H(diff) | early H(diff) | warmup H(diff) | transition H(diff) | warmup transition H(diff) | same diff ratio | warmup same ratio | longest diff run | warmup longest run | diff autocorr | first-later H(diff) | first-later TVD(diff) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1_baseline | tdc_reset_enable_random1_baseline_ro0_2mib | 9595 | 252548 | 6.67227 | 6.54038 | 6.54209 | 13.2961 | 9.85683 | 0.0113444 | 0.0146628 | 4 | 2 | -0.00117893 | -0.0165102 | 0.0359183 |
| random3_goodref | tdc_reset_enable_random3_goodref_ro0_2mib | 9582 | 252561 | 6.6945 | 6.58148 | 6.58243 | 13.3466 | 9.89424 | 0.0109954 | 0.0117302 | 3 | 2 | 0.000272926 | -0.011996 | 0.033525 |
| random1_sampler_local | tdc_reset_enable_random1_sampler_local_ro0_2mib | 9644 | 252499 | 6.71817 | 6.60532 | 6.60266 | 13.3895 | 9.85561 | 0.0109585 | 0.00977517 | 3 | 2 | -0.000525189 | -0.000619033 | 0.0364251 |

## Window Output

- summary rows: `3`
- window rows: `48`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
