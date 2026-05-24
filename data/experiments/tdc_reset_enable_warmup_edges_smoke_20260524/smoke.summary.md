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
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 4 | 6.60639 | 6.47378 | 6.47622 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 5 | 6.60639 | 6.47378 | 6.47724 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 10 | 6.60639 | 6.47378 | 6.47473 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 11 | 6.60639 | 6.47378 | 6.4738 | 13.167 | 9.81161 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_baseline_ro4_2mib | tdc_reset_enable_random1_baseline_ro4_2mib | 9293 | 252850 | 12 | 6.60639 | 6.47378 | 6.47196 | 13.167 | 9.80891 | 0.0125411 | 0.0156403 | 3 | 2 | 0.000597158 | -0.0181854 | 0.0347304 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 4 | 6.70052 | 6.63186 | 6.63515 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 5 | 6.70052 | 6.63186 | 6.63421 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 10 | 6.70052 | 6.63186 | 6.63071 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 11 | 6.70052 | 6.63186 | 6.63132 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |
| tdc_reset_enable_random1_sampler_local_ro4_2mib | tdc_reset_enable_random1_sampler_local_ro4_2mib | 9388 | 252756 | 12 | 6.70052 | 6.63186 | 6.63209 | 13.3568 | 9.90206 | 0.0110463 | 0.00782014 | 3 | 2 | 0.00208215 | 0.00397184 | 0.0344045 |

## Window Output

- summary rows: `10`
- window rows: `32`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
