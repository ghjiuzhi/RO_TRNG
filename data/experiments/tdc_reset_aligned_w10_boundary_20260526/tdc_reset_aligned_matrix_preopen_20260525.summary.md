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
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 0 | 6.638 | 6.44492 | 6.44492 | 12.9218 | 8.9189 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 12 | 6.638 | 6.44492 | 6.45441 | 12.9218 | 8.92282 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 64 | 6.638 | 6.44492 | 6.44304 | 12.9218 | 8.91499 | 0.0118412 | 0.00978474 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 256 | 6.638 | 6.44492 | 6.41747 | 12.9218 | 8.91499 | 0.0118412 | 0.00782779 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 1024 | 6.638 | 6.44492 | 6.43866 | 12.9218 | 8.92377 | 0.0118412 | 0.0156556 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup10_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 4096 | 6.638 | 6.44492 | 6.43172 | 12.9218 | 8.89394 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |

## Window Output

- summary rows: `6`
- window rows: `8`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
