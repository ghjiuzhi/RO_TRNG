# TDC Pair Dynamics 20260514

Offline post-analysis of completed TDC pair captures. No hardware, Vivado, COM, JTAG, or hw_server access was used.

## Method

- Prefer existing `.tdc_packets.csv`; fall back to raw `.bin` only when packet CSVs are absent.
- Build one code-density phase lookup per lane from the full run, then compute windowed dynamics with the same phase scale.
- `strong_lock_window` is a conservative flag: max absolute lagged phase correlation >= 0.5 within the requested lag range.

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | slope ps/window | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_pair_random1_ro0_ro1_repeat02_2mib | 16 | 262143 | 0.0022153 | 0.0233717 | 2038.11 | 33.7272 | 0.19032 | 0 |
| tdc_pair_random1_ro0_ro1_run01_2mib | 16 | 262142 | -0.00246724 | 0.0215993 | 2042.86 | 67.3975 | 0.382658 | 0 |
| tdc_pair_random1_ro2_ro4_repeat02_2mib | 16 | 262143 | 0.000935983 | 0.024083 | 2039.03 | 46.9661 | 0.36017 | 0 |
| tdc_pair_random1_ro2_ro4_run01_2mib | 16 | 262138 | -0.00223571 | 0.0317827 | 2042.29 | 55.2974 | -0.0716226 | 0 |
| tdc_pair_random1_ro4_ro5_repeat02_2mib | 16 | 262144 | -0.00294471 | 0.0265191 | 2043.22 | 49.4854 | 0.81489 | 0 |
| tdc_pair_random1_ro4_ro5_run01_2mib | 16 | 262143 | -0.00120253 | 0.0224973 | 2041.5 | 43.5713 | -0.275657 | 0 |
| tdc_pair_random3_ro0_ro6_repeat02_2mib | 16 | 262143 | -0.00251103 | 0.0227691 | 2043.01 | 59.444 | 0.848645 | 0 |
| tdc_pair_random3_ro0_ro6_run01_2mib | 16 | 262143 | -0.0014587 | 0.0239274 | 2041.92 | 57.0657 | -1.12701 | 0 |
| tdc_pair_random3_ro3_ro5_repeat02_2mib | 16 | 262144 | 0.00272779 | 0.0270783 | 2037.47 | 54.9898 | 0.0639716 | 0 |
| tdc_pair_random3_ro3_ro5_run01_2mib | 16 | 262143 | -3.51032e-05 | 0.0276158 | 2040.24 | 65.5298 | -0.0635312 | 0 |
| tdc_pair_random3_ro3_ro7_repeat02_2mib | 16 | 262143 | -0.000306843 | 0.0276015 | 2040.68 | 60.9292 | 1.04565 | 0 |
| tdc_pair_random3_ro3_ro7_run01_2mib | 16 | 262142 | -1.30365e-05 | 0.0229113 | 2040.43 | 53.1182 | 0.848703 | 0 |

## Interpretation

No window crosses the conservative lag-correlation screen. The current data should be described as showing no strong pair locking under this measurement condition.

## Output

- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`
