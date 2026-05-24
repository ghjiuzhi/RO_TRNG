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
| random3_goodref_ro3 | tdc_reset_enable_random3_goodref_ro3_2mib | 9869 | 252274 | 6.67248 | 6.54411 | 6.54869 | 13.2987 | 9.84827 | 0.0113845 | 0.0136852 | 4 | 2 | 0.00038593 | -0.0202451 | 0.038354 |
| random3_goodref_ro3_repeat02 | tdc_reset_enable_random3_goodref_ro3_repeat02_2mib | 9944 | 252199 | 6.67484 | 6.55376 | 6.54804 | 13.3026 | 9.86196 | 0.0112769 | 0.0136852 | 3 | 2 | -0.00206804 | -0.0075708 | 0.0344149 |

## Window Output

- summary rows: `2`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
