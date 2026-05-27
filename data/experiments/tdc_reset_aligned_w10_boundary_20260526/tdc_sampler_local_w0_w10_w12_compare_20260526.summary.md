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
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 0 | 6.65464 | 6.43888 | 6.43888 | 12.9439 | 8.92282 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 10 | 6.65464 | 6.43888 | 6.43436 | 12.9439 | 8.91499 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 12 | 6.65464 | 6.43888 | 6.43144 | 12.9439 | 8.91499 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 64 | 6.65464 | 6.43888 | 6.43453 | 12.9439 | 8.91499 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 256 | 6.65464 | 6.43888 | 6.50544 | 12.9439 | 8.9463 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 1024 | 6.65464 | 6.43888 | 6.41661 | 12.9439 | 8.90029 | 0.0130314 | 0.0136986 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 4096 | 6.65464 | 6.43888 | 6.45233 | 12.9439 | 8.95021 | 0.0130314 | 0.0156556 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 0 | 6.638 | 6.44492 | 6.44492 | 12.9218 | 8.9189 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 10 | 6.638 | 6.44492 | 6.45042 | 12.9218 | 8.92282 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 12 | 6.638 | 6.44492 | 6.45441 | 12.9218 | 8.92282 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 64 | 6.638 | 6.44492 | 6.44304 | 12.9218 | 8.91499 | 0.0118412 | 0.00978474 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 256 | 6.638 | 6.44492 | 6.41747 | 12.9218 | 8.91499 | 0.0118412 | 0.00782779 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 1024 | 6.638 | 6.44492 | 6.43866 | 12.9218 | 8.92377 | 0.0118412 | 0.0156556 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w10 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525 | 0 | 32768 | 4096 | 6.638 | 6.44492 | 6.43172 | 12.9218 | 8.89394 | 0.0118412 | 0.0136986 | 3 | 2 | 0.00660909 | -0.0433649 | 0.0631278 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 0 | 6.73356 | 6.50239 | 6.50239 | 13.0993 | 8.91986 | 0.010651 | 0.00978474 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 10 | 6.73356 | 6.50239 | 6.50379 | 13.0993 | 8.91595 | 0.010651 | 0.0117417 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 12 | 6.73356 | 6.50239 | 6.50011 | 13.0993 | 8.91595 | 0.010651 | 0.0117417 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 64 | 6.73356 | 6.50239 | 6.49529 | 13.0993 | 8.92769 | 0.010651 | 0.0117417 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 256 | 6.73356 | 6.50239 | 6.50906 | 13.0993 | 8.91056 | 0.010651 | 0.0195695 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 1024 | 6.73356 | 6.50239 | 6.4872 | 13.0993 | 8.92525 | 0.010651 | 0.00782779 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| sampler_local_w12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 4096 | 6.73356 | 6.50239 | 6.52703 | 13.0993 | 8.9189 | 0.010651 | 0.00782779 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |

## Window Output

- summary rows: `21`
- window rows: `24`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
