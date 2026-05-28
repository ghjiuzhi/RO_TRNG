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
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 0 | 6.69748 | 6.65176 | 6.65176 | 13.0398 | 10.7892 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 4 | 6.69748 | 6.65176 | 6.65043 | 13.0398 | 10.7892 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 8 | 6.69748 | 6.65176 | 6.65128 | 13.0398 | 10.7892 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 16 | 6.69748 | 6.65176 | 6.64923 | 13.0398 | 10.7862 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 32 | 6.69748 | 6.65176 | 6.64982 | 13.0398 | 10.7876 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| scompact_ro0_w4 | tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 64 | 6.69748 | 6.65176 | 6.64883 | 13.0398 | 10.7854 | 0.0100101 | 0.00928188 | 3 | 2 | 0.00424799 | -0.0461471 | 0.0932943 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 0 | 6.74771 | 6.72009 | 6.72009 | 13.1273 | 10.7856 | 0.00985748 | 0.011236 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 4 | 6.74771 | 6.72009 | 6.71974 | 13.1273 | 10.7831 | 0.00985748 | 0.011236 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 8 | 6.74771 | 6.72009 | 6.72262 | 13.1273 | 10.784 | 0.00985748 | 0.0117245 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 16 | 6.74771 | 6.72009 | 6.72398 | 13.1273 | 10.784 | 0.00985748 | 0.0117245 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 32 | 6.74771 | 6.72009 | 6.7211 | 13.1273 | 10.7844 | 0.00985748 | 0.0117245 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |
| srestart_ro0_w4 | tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 0 | 32768 | 64 | 6.74771 | 6.72009 | 6.72152 | 13.1273 | 10.7875 | 0.00985748 | 0.0117245 | 3 | 3 | 0.00280759 | -0.0263047 | 0.0988932 |

## Window Output

- summary rows: `12`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
