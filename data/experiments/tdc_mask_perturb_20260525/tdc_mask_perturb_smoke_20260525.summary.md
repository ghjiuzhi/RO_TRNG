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
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 0 | 6.64193 | 6.51851 | 6.51851 | 13.1974 | 8.95413 | 0.0112612 | 0.0136986 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 12 | 6.64193 | 6.51851 | 6.51229 | 13.1974 | 8.95021 | 0.0112612 | 0.0136986 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 64 | 6.64193 | 6.51851 | 6.49174 | 13.1974 | 8.93847 | 0.0112612 | 0.0136986 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 256 | 6.64193 | 6.51851 | 6.43482 | 13.1974 | 8.93847 | 0.0112612 | 0.0117417 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 1024 | 6.64193 | 6.51851 | 6.4398 | 13.1974 | 8.94482 | 0.0112612 | 0.0176125 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 | 0 | 131071 | 4096 | 6.64193 | 6.51851 | 6.42969 | 13.1974 | 8.91203 | 0.0112612 | 0.00978474 | 3 | 2 | -0.000492782 | -0.00850459 | 0.0678906 |

## Window Output

- summary rows: `6`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
