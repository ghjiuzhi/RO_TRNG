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
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 0 | 6.68639 | 6.50702 | 6.50702 | 13.3622 | 8.95021 | 0.0108566 | 0.0117417 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 12 | 6.68639 | 6.50702 | 6.5038 | 13.3622 | 8.95413 | 0.0108566 | 0.0117417 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 64 | 6.68639 | 6.50702 | 6.50954 | 13.3622 | 8.95804 | 0.0108566 | 0.0117417 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 256 | 6.68639 | 6.50702 | 6.42932 | 13.3622 | 8.95265 | 0.0108566 | 0.00782779 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 1024 | 6.68639 | 6.50702 | 6.48095 | 13.3622 | 8.94238 | 0.0108566 | 0.00391389 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_pair_only | tdc_mask_random1_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 4096 | 6.68639 | 6.50702 | 6.51171 | 13.3622 | 8.97761 | 0.0108566 | 0.00391389 | 3 | 2 | 0.000874177 | -0.0113822 | 0.0592529 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 0 | 6.74707 | 6.52701 | 6.52701 | 13.4827 | 8.91499 | 0.0103026 | 0.00978474 | 4 | 3 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 12 | 6.74707 | 6.52701 | 6.55237 | 13.4827 | 8.92134 | 0.0103026 | 0.00587084 | 4 | 2 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 64 | 6.74707 | 6.52701 | 6.56648 | 13.4827 | 8.93064 | 0.0103026 | 0.00782779 | 4 | 2 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 256 | 6.74707 | 6.52701 | 6.53298 | 13.4827 | 8.94482 | 0.0103026 | 0.00978474 | 4 | 2 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 1024 | 6.74707 | 6.52701 | 6.50166 | 13.4827 | 8.96978 | 0.0103026 | 0.0156556 | 4 | 2 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_all_data_on | tdc_mask_random1_ro0_ro1_all_data_on_20260525 | 0 | 1048575 | 4096 | 6.74707 | 6.52701 | 6.56447 | 13.4827 | 8.94238 | 0.0103026 | 0.0117417 | 4 | 2 | -0.000931813 | -0.0261851 | 0.0742116 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 0 | 6.64622 | 6.45488 | 6.45488 | 13.2826 | 8.93456 | 0.0109625 | 0.00587084 | 4 | 2 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 12 | 6.64622 | 6.45488 | 6.45368 | 13.2826 | 8.93847 | 0.0109625 | 0.00587084 | 4 | 2 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 64 | 6.64622 | 6.45488 | 6.4299 | 13.2826 | 8.93456 | 0.0109625 | 0.00587084 | 4 | 2 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 256 | 6.64622 | 6.45488 | 6.45299 | 13.2826 | 8.96587 | 0.0109625 | 0.00391389 | 4 | 2 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 1024 | 6.64622 | 6.45488 | 6.48735 | 13.2826 | 8.9737 | 0.0109625 | 0.0136986 | 4 | 2 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random1_ro0_ro1_pair_plus_sample | tdc_mask_random1_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 4096 | 6.64622 | 6.45488 | 6.46808 | 13.2826 | 8.92134 | 0.0109625 | 0.0176125 | 4 | 3 | -6.68543e-05 | -0.0200149 | 0.0669065 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 0 | 6.69703 | 6.616 | 6.616 | 13.3832 | 8.93699 | 0.0107479 | 0.00782779 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 12 | 6.69703 | 6.616 | 6.60321 | 13.3832 | 8.93699 | 0.0107479 | 0.00587084 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 64 | 6.69703 | 6.616 | 6.56271 | 13.3832 | 8.94091 | 0.0107479 | 0.00782779 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 256 | 6.69703 | 6.616 | 6.5141 | 13.3832 | 8.94238 | 0.0107479 | 0.00391389 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 1024 | 6.69703 | 6.616 | 6.55261 | 13.3832 | 8.92917 | 0.0107479 | 0.00587084 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_pair_only | tdc_mask_random3_ro0_ro6_pair_only_20260525 | 0 | 1048575 | 4096 | 6.69703 | 6.616 | 6.51811 | 13.3832 | 8.93847 | 0.0107479 | 0.00978474 | 4 | 2 | 0.000729496 | -0.0119531 | 0.0615001 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 0 | 5.98263 | 5.88684 | 5.88684 | 11.9625 | 8.85628 | 0.0160256 | 0.0215264 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 12 | 5.98263 | 5.88684 | 5.89193 | 11.9625 | 8.86411 | 0.0160256 | 0.0215264 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 64 | 5.98263 | 5.88684 | 5.88335 | 11.9625 | 8.84845 | 0.0160256 | 0.0176125 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 256 | 5.98263 | 5.88684 | 5.88493 | 11.9625 | 8.82888 | 0.0160256 | 0.0195695 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 1024 | 5.98263 | 5.88684 | 5.89081 | 11.9625 | 8.9189 | 0.0160256 | 0.0136986 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random3_ro0_ro6_all_data_on | tdc_mask_random3_ro0_ro6_all_data_on_20260525 | 0 | 1048575 | 4096 | 5.98263 | 5.88684 | 5.88896 | 11.9625 | 8.84697 | 0.0160256 | 0.0215264 | 4 | 2 | -0.00128411 | -0.0125321 | 0.0447299 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 0 | 6.6682 | 6.54007 | 6.54007 | 13.3257 | 8.93847 | 0.0110598 | 0.0136986 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 12 | 6.6682 | 6.54007 | 6.54371 | 13.3257 | 8.94238 | 0.0110598 | 0.0136986 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 64 | 6.6682 | 6.54007 | 6.5003 | 13.3257 | 8.9189 | 0.0110598 | 0.0156556 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 256 | 6.6682 | 6.54007 | 6.43669 | 13.3257 | 8.91499 | 0.0110598 | 0.0117417 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 1024 | 6.6682 | 6.54007 | 6.45615 | 13.3257 | 8.91499 | 0.0110598 | 0.0156556 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample | tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample_20260525 | 0 | 1048575 | 4096 | 6.6682 | 6.54007 | 6.43257 | 13.3257 | 8.91203 | 0.0110598 | 0.00978474 | 4 | 2 | -0.000176228 | -0.0164798 | 0.0701492 |

## Window Output

- summary rows: `36`
- window rows: `1536`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
