# TDC Pair Dynamics 20260514

Offline post-analysis of completed TDC pair captures. No hardware, Vivado, COM, JTAG, or hw_server access was used.

## Method

- Prefer existing `.tdc_packets.csv`; fall back to raw `.bin` only when packet CSVs are absent.
- Build one code-density phase lookup per lane from the full run, then compute windowed dynamics with the same phase scale.
- `strong_lock_window` is a conservative flag: max absolute lagged phase correlation >= 0.5 within the requested lag range.

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | slope ps/window | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_pair_random1_ro0_ro1_run01_2mib | 16 | 262142 | -0.00246724 | 0.0215993 | 2042.86 | 67.3975 | 0.382658 | 0 |
| tdc_pair_random1_ro2_ro4_run01_2mib | 16 | 262138 | -0.00223571 | 0.0317827 | 2042.29 | 55.2974 | -0.0716226 | 0 |
| tdc_pair_random1_ro4_ro5_run01_2mib | 16 | 262143 | -0.00120253 | 0.0224973 | 2041.5 | 43.5713 | -0.275657 | 0 |
| tdc_pair_random3_ro0_ro6_run01_2mib | 16 | 262143 | -0.0014587 | 0.0239274 | 2041.92 | 57.0657 | -1.12701 | 0 |
| tdc_pair_random3_ro3_ro5_run01_2mib | 16 | 262143 | -3.51032e-05 | 0.0276158 | 2040.24 | 65.5298 | -0.0635312 | 0 |
| tdc_pair_random3_ro3_ro7_run01_2mib | 16 | 262142 | -1.30365e-05 | 0.0229113 | 2040.43 | 53.1182 | 0.848703 | 0 |

## Interpretation

No window crosses the conservative lag-correlation screen. The current data should be described as showing no strong pair locking under this measurement condition.

## Output

- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`
