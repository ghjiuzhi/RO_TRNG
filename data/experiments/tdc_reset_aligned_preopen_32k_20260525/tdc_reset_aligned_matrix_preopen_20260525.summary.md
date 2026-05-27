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
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 0 | 6.72673 | 6.56097 | 6.56097 | 13.0266 | 8.94482 | 0.0102841 | 0.0136986 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 12 | 6.72673 | 6.56097 | 6.55434 | 13.0266 | 8.94482 | 0.0102841 | 0.0136986 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 64 | 6.72673 | 6.56097 | 6.52487 | 13.0266 | 8.94482 | 0.0102841 | 0.0136986 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 256 | 6.72673 | 6.56097 | 6.51613 | 13.0266 | 8.92673 | 0.0102841 | 0.00978474 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.72673 | 6.56097 | 6.57891 | 13.0266 | 8.95413 | 0.0102841 | 0.0176125 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.72673 | 6.56097 | 6.55778 | 13.0266 | 8.92673 | 0.0102841 | 0.00587084 | 3 | 2 | -0.00245219 | -0.0192081 | 0.0657748 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 0 | 6.61333 | 6.45285 | 6.45285 | 12.8025 | 8.92917 | 0.0127865 | 0.00587084 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 12 | 6.61333 | 6.45285 | 6.45688 | 12.8025 | 8.93308 | 0.0127865 | 0.00587084 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 64 | 6.61333 | 6.45285 | 6.46165 | 12.8025 | 8.92917 | 0.0127865 | 0.00782779 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 256 | 6.61333 | 6.45285 | 6.43721 | 12.8025 | 8.92917 | 0.0127865 | 0.0136986 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.61333 | 6.45285 | 6.48631 | 12.8025 | 8.93456 | 0.0127865 | 0.0136986 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 | tdc_reset_random1_baseline_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.61333 | 6.45285 | 6.37358 | 12.8025 | 8.91447 | 0.0127865 | 0.00978474 | 4 | 2 | -0.00378227 | -0.0205391 | 0.0520708 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 0 | 6.67242 | 6.51726 | 6.51726 | 12.9222 | 8.93847 | 0.0125118 | 0.0156556 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 12 | 6.67242 | 6.51726 | 6.53054 | 12.9222 | 8.93847 | 0.0125118 | 0.0156556 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 64 | 6.67242 | 6.51726 | 6.54948 | 12.9222 | 8.94238 | 0.0125118 | 0.0117417 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 256 | 6.67242 | 6.51726 | 6.55836 | 12.9222 | 8.93064 | 0.0125118 | 0.0136986 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.67242 | 6.51726 | 6.46449 | 12.9222 | 8.92673 | 0.0125118 | 0.0176125 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.67242 | 6.51726 | 6.5095 | 12.9222 | 8.95413 | 0.0125118 | 0.00978474 | 3 | 2 | -0.00719821 | -0.0180217 | 0.0627043 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 0 | 6.66308 | 6.46228 | 6.46228 | 12.9327 | 8.9189 | 0.0119625 | 0.00978474 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 12 | 6.66308 | 6.46228 | 6.44394 | 12.9327 | 8.91499 | 0.0119625 | 0.00782779 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 64 | 6.66308 | 6.46228 | 6.40585 | 12.9327 | 8.93456 | 0.0119625 | 0.00782779 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 256 | 6.66308 | 6.46228 | 6.45637 | 12.9327 | 8.9463 | 0.0119625 | 0.00587084 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.66308 | 6.46228 | 6.49859 | 12.9327 | 8.94238 | 0.0119625 | 0.00587084 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 | tdc_reset_random3_goodref_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.66308 | 6.46228 | 6.49617 | 12.9327 | 8.94238 | 0.0119625 | 0.0117417 | 3 | 2 | 0.0102132 | -0.0228369 | 0.0609309 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 0 | 6.73289 | 6.47918 | 6.47918 | 13.0401 | 8.9463 | 0.0113522 | 0.0136986 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 12 | 6.73289 | 6.47918 | 6.47198 | 13.0401 | 8.94238 | 0.0113522 | 0.0136986 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 64 | 6.73289 | 6.47918 | 6.46384 | 13.0401 | 8.93847 | 0.0113522 | 0.0136986 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 256 | 6.73289 | 6.47918 | 6.48684 | 13.0401 | 8.90568 | 0.0113522 | 0.00782779 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.73289 | 6.47918 | 6.54816 | 13.0401 | 8.93064 | 0.0113522 | 0.00978474 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup0_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.73289 | 6.47918 | 6.55041 | 13.0401 | 8.93064 | 0.0113522 | 0.0195695 | 4 | 2 | 0.000382724 | -0.0221951 | 0.0654637 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 0 | 6.68621 | 6.50445 | 6.50445 | 12.9502 | 8.93699 | 0.011932 | 0.0136986 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 12 | 6.68621 | 6.50445 | 6.50408 | 12.9502 | 8.94091 | 0.011932 | 0.0136986 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 64 | 6.68621 | 6.50445 | 6.49837 | 12.9502 | 8.94482 | 0.011932 | 0.0136986 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 256 | 6.68621 | 6.50445 | 6.47405 | 12.9502 | 8.94238 | 0.011932 | 0.00978474 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 1024 | 6.68621 | 6.50445 | 6.47202 | 12.9502 | 8.9316 | 0.011932 | 0.0117417 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 | tdc_reset_random1_sampler_local_ro0_warmup12_32k._preopen_20260525 | 0 | 32770 | 4096 | 6.68621 | 6.50445 | 6.47523 | 12.9502 | 8.91742 | 0.011932 | 0.0136986 | 3 | 2 | 0.00603125 | -0.0431422 | 0.0653593 |

## Window Output

- summary rows: `36`
- window rows: `54`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
