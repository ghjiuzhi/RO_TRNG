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
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 0 | 6.66547 | 6.63328 | 6.63328 | 12.9872 | 10.7517 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 4 | 6.66547 | 6.63328 | 6.63448 | 12.9872 | 10.7517 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 8 | 6.66547 | 6.63328 | 6.6344 | 12.9872 | 10.7507 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 16 | 6.66547 | 6.63328 | 6.63286 | 12.9872 | 10.7494 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 32 | 6.66547 | 6.63328 | 6.63342 | 12.9872 | 10.7478 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| scompact_ro3_w4 | tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 64 | 6.66547 | 6.63328 | 6.63694 | 12.9872 | 10.7536 | 0.0111698 | 0.00635076 | 3 | 2 | -0.00753148 | -0.0315707 | 0.0875977 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 0 | 6.70017 | 6.6345 | 6.6345 | 13.044 | 10.7495 | 0.0110477 | 0.00879336 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 4 | 6.70017 | 6.6345 | 6.63676 | 13.044 | 10.7495 | 0.0110477 | 0.00879336 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 8 | 6.70017 | 6.6345 | 6.63542 | 13.044 | 10.7495 | 0.0110477 | 0.00879336 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 16 | 6.70017 | 6.6345 | 6.6358 | 13.044 | 10.7505 | 0.0110477 | 0.00879336 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 32 | 6.70017 | 6.6345 | 6.63559 | 13.044 | 10.7472 | 0.0110477 | 0.00879336 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |
| srestart_ro3_w4 | tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 0 | 32768 | 64 | 6.70017 | 6.6345 | 6.64228 | 13.044 | 10.752 | 0.0110477 | 0.00928188 | 3 | 2 | -0.00554115 | -0.0672658 | 0.0923177 |

## Window Output

- summary rows: `12`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
