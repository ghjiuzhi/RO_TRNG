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
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 0 | 6.75886 | 6.53655 | 6.53655 | 13.1434 | 8.91351 | 0.00994903 | 0.0136986 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 12 | 6.75886 | 6.53655 | 6.5361 | 13.1434 | 8.91351 | 0.00994903 | 0.0136986 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 64 | 6.75886 | 6.53655 | 6.53168 | 13.1434 | 8.92525 | 0.00994903 | 0.0117417 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 256 | 6.75886 | 6.53655 | 6.57591 | 13.1434 | 8.95413 | 0.00994903 | 0.00782779 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 1024 | 6.75886 | 6.53655 | 6.60282 | 13.1434 | 8.95804 | 0.00994903 | 0.00782779 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup0 | tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 4096 | 6.75886 | 6.53655 | 6.53763 | 13.1434 | 8.94238 | 0.00994903 | 0.0136986 | 3 | 2 | -0.0082803 | -0.024197 | 0.0682199 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 0 | 6.66619 | 6.44347 | 6.44347 | 12.9741 | 8.91595 | 0.0116581 | 0.0156556 | 3 | 2 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 12 | 6.66619 | 6.44347 | 6.44145 | 12.9741 | 8.91986 | 0.0116581 | 0.0156556 | 3 | 2 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 64 | 6.66619 | 6.44347 | 6.43338 | 12.9741 | 8.91595 | 0.0116581 | 0.0176125 | 3 | 2 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 256 | 6.66619 | 6.44347 | 6.49078 | 12.9741 | 8.95413 | 0.0116581 | 0.0117417 | 3 | 2 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 1024 | 6.66619 | 6.44347 | 6.51477 | 12.9741 | 8.93064 | 0.0116581 | 0.0117417 | 3 | 3 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random1_baseline_warmup12 | tdc_reset_random1_baseline_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 4096 | 6.66619 | 6.44347 | 6.52268 | 12.9741 | 8.93456 | 0.0116581 | 0.0117417 | 3 | 2 | 3.71515e-06 | -0.0270031 | 0.0660575 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 0 | 6.61583 | 6.43642 | 6.43642 | 12.8973 | 8.9463 | 0.0131535 | 0.0195695 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 12 | 6.61583 | 6.43642 | 6.45356 | 12.8973 | 8.94238 | 0.0131535 | 0.0176125 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 64 | 6.61583 | 6.43642 | 6.44079 | 12.8973 | 8.93847 | 0.0131535 | 0.0156556 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 256 | 6.61583 | 6.43642 | 6.45193 | 12.8973 | 8.94238 | 0.0131535 | 0.0156556 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 1024 | 6.61583 | 6.43642 | 6.42045 | 12.8973 | 8.92134 | 0.0131535 | 0.0195695 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup0 | tdc_reset_random3_goodref_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 4096 | 6.61583 | 6.43642 | 6.45624 | 12.8973 | 8.96195 | 0.0131535 | 0.00782779 | 3 | 2 | -0.00921983 | -0.0380041 | 0.0677665 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 0 | 6.60778 | 6.46444 | 6.46444 | 12.8768 | 8.93064 | 0.0129398 | 0.0117417 | 3 | 2 | -0.00613231 | -0.0175444 | 0.0748465 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 12 | 6.60778 | 6.46444 | 6.45069 | 12.8768 | 8.93064 | 0.0129398 | 0.0117417 | 3 | 2 | -0.00613231 | -0.0175444 | 0.0748465 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 64 | 6.60778 | 6.46444 | 6.47747 | 12.8768 | 8.95021 | 0.0129398 | 0.0117417 | 3 | 2 | -0.00613231 | -0.0175444 | 0.0748465 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 256 | 6.60778 | 6.46444 | 6.42313 | 12.8768 | 8.9189 | 0.0129398 | 0.0156556 | 3 | 2 | -0.00613231 | -0.0175444 | 0.0748465 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 1024 | 6.60778 | 6.46444 | 6.39806 | 12.8768 | 8.90177 | 0.0129398 | 0.0215264 | 3 | 2 | -0.00613231 | -0.0175444 | 0.0748465 |
| random3_goodref_warmup12 | tdc_reset_random3_goodref_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 4096 | 6.60778 | 6.46444 | 6.37825 | 12.8768 | 8.8949 | 0.0129398 | 0.0156556 | 3 | 3 | -0.00613231 | -0.0175444 | 0.0748465 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 0 | 6.65464 | 6.43888 | 6.43888 | 12.9439 | 8.92282 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 12 | 6.65464 | 6.43888 | 6.43144 | 12.9439 | 8.91499 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 64 | 6.65464 | 6.43888 | 6.43453 | 12.9439 | 8.91499 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 256 | 6.65464 | 6.43888 | 6.50544 | 12.9439 | 8.9463 | 0.0130314 | 0.00978474 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 1024 | 6.65464 | 6.43888 | 6.41661 | 12.9439 | 8.90029 | 0.0130314 | 0.0136986 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup0 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup0._preopen_20260525 | 0 | 32768 | 4096 | 6.65464 | 6.43888 | 6.45233 | 12.9439 | 8.95021 | 0.0130314 | 0.0156556 | 3 | 2 | -0.000825613 | -0.00360712 | 0.0567104 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 0 | 6.73356 | 6.50239 | 6.50239 | 13.0993 | 8.91986 | 0.010651 | 0.00978474 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 12 | 6.73356 | 6.50239 | 6.50011 | 13.0993 | 8.91595 | 0.010651 | 0.0117417 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 64 | 6.73356 | 6.50239 | 6.49529 | 13.0993 | 8.92769 | 0.010651 | 0.0117417 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 256 | 6.73356 | 6.50239 | 6.50906 | 13.0993 | 8.91056 | 0.010651 | 0.0195695 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 1024 | 6.73356 | 6.50239 | 6.4872 | 13.0993 | 8.92525 | 0.010651 | 0.00782779 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |
| random1_sampler_local_warmup12 | tdc_reset_random1_sampler_local_ro0_clean32k_warmup12._preopen_20260525 | 0 | 32768 | 4096 | 6.73356 | 6.50239 | 6.52703 | 13.0993 | 8.9189 | 0.010651 | 0.00782779 | 3 | 2 | 0.00185527 | -0.0282377 | 0.0721261 |

## Window Output

- summary rows: `36`
- window rows: `48`
- CSV files are written next to this Markdown file in the selected `--out-dir`.
