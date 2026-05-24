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
| random1_baseline_ro4_repeat02 | tdc_reset_enable_random1_baseline_ro4_repeat02_2mib | 9234 | 252909 | 6.60514 | 6.50542 | 6.50871 | 13.1651 | 9.88103 | 0.0123049 | 0.0136852 | 4 | 4 | -0.000544037 | -0.00437185 | 0.0333207 |
| random1_sampler_local_ro4_repeat02 | tdc_reset_enable_random1_sampler_local_ro4_repeat02_2mib | 9498 | 252645 | 6.70189 | 6.63041 | 6.63395 | 13.3589 | 9.90792 | 0.0109522 | 0.00879765 | 4 | 2 | 0.00135009 | -0.0153435 | 0.0349408 |

## Window Output

- summary rows: `2`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
