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
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 0 | 5.98207 | 5.90597 | 5.90597 | 11.9613 | 8.85185 | 0.0159474 | 0.0176125 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 12 | 5.98207 | 5.90597 | 5.89704 | 11.9613 | 8.84793 | 0.0159474 | 0.0176125 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 64 | 5.98207 | 5.90597 | 5.88113 | 11.9613 | 8.8455 | 0.0159474 | 0.0215264 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 256 | 5.98207 | 5.90597 | 5.87216 | 11.9613 | 8.86115 | 0.0159474 | 0.0215264 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 1024 | 5.98207 | 5.90597 | 5.87605 | 11.9613 | 8.86411 | 0.0159474 | 0.0156556 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 | tdc_mask_random3_ro0_ro6_all_data_on_repeat02_20260525 | 0 | 1048575 | 4096 | 5.98207 | 5.90597 | 5.90086 | 11.9613 | 8.89933 | 0.0159474 | 0.0234834 | 4 | 2 | 0.000825972 | -0.0082368 | 0.0505797 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 0 | 6.64861 | 6.39381 | 6.39381 | 13.287 | 8.93456 | 0.0111742 | 0.0215264 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 12 | 6.64861 | 6.39381 | 6.38166 | 13.287 | 8.94238 | 0.0111742 | 0.0215264 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 64 | 6.64861 | 6.39381 | 6.4219 | 13.287 | 8.93308 | 0.0111742 | 0.0176125 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 256 | 6.64861 | 6.39381 | 6.43559 | 13.287 | 8.89394 | 0.0111742 | 0.00782779 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 1024 | 6.64861 | 6.39381 | 6.4656 | 13.287 | 8.93064 | 0.0111742 | 0.0136986 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_neighbors_on | tdc_mask_random3_ro0_ro6_neighbors_on_20260525 | 0 | 1048575 | 4096 | 6.64861 | 6.39381 | 6.48547 | 13.287 | 8.93847 | 0.0111742 | 0.0195695 | 4 | 2 | -0.000817939 | -0.0272199 | 0.0628145 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 0 | 6.62633 | 6.51236 | 6.51236 | 13.2427 | 8.93847 | 0.0113382 | 0.0156556 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 12 | 6.62633 | 6.51236 | 6.51184 | 13.2427 | 8.9463 | 0.0113382 | 0.0156556 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 64 | 6.62633 | 6.51236 | 6.481 | 13.2427 | 8.9463 | 0.0113382 | 0.0117417 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 256 | 6.62633 | 6.51236 | 6.46689 | 13.2427 | 8.91351 | 0.0113382 | 0.00978474 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 1024 | 6.62633 | 6.51236 | 6.40127 | 13.2427 | 8.9189 | 0.0113382 | 0.00978474 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random3_ro0_ro6_pair_plus_sample | tdc_mask_random3_ro0_ro6_pair_plus_sample_20260525 | 0 | 1048576 | 4096 | 6.62633 | 6.51236 | 6.47694 | 13.2427 | 8.93064 | 0.0113382 | 0.0117417 | 4 | 2 | 0.000281253 | -0.0191574 | 0.0664216 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 0 | 6.69899 | 6.49786 | 6.49786 | 13.3871 | 8.95265 | 0.0106697 | 0.00587084 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 12 | 6.69899 | 6.49786 | 6.50015 | 13.3871 | 8.95656 | 0.0106697 | 0.00391389 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 64 | 6.69899 | 6.49786 | 6.49696 | 13.3871 | 8.94874 | 0.0106697 | 0.00195695 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 256 | 6.69899 | 6.49786 | 6.4974 | 13.3871 | 8.9316 | 0.0106697 | 0.00587084 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 1024 | 6.69899 | 6.49786 | 6.51035 | 13.3871 | 8.95265 | 0.0106697 | 0.00587084 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only | tdc_mask_random1_local_sample_ro0_ro1_pair_only_20260525 | 0 | 1048575 | 4096 | 6.69899 | 6.49786 | 6.48806 | 13.3871 | 8.94238 | 0.0106697 | 0.0117417 | 4 | 2 | -0.00163481 | -0.0377579 | 0.0650759 |

## Window Output

- summary rows: `24`
- window rows: `1024`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
