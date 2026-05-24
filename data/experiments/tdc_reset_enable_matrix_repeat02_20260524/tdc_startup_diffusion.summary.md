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
| random1_baseline_repeat02 | tdc_reset_enable_random1_baseline_ro0_repeat02_2mib | 5701 | 256442 | 6.67673 | 6.55711 | 6.55446 | 13.3062 | 9.85097 | 0.0115972 | 0.0117302 | 4 | 2 | -0.00149368 | -0.00792956 | 0.0372148 |
| random3_goodref_repeat02 | tdc_reset_enable_random3_goodref_ro0_repeat02_2mib | 7743 | 254400 | 6.69607 | 6.63509 | 6.64063 | 13.3488 | 9.90914 | 0.010853 | 0.0146628 | 3 | 2 | 0.00104278 | -0.0112044 | 0.0360032 |
| random1_sampler_local_repeat02 | tdc_reset_enable_random1_sampler_local_ro0_repeat02_2mib | 9141 | 253002 | 6.71952 | 6.64656 | 6.64163 | 13.3913 | 9.88077 | 0.0106956 | 0.0107527 | 3 | 2 | -0.000126278 | 0.000779792 | 0.0349437 |

## Window Output

- summary rows: `3`
- window rows: `48`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
