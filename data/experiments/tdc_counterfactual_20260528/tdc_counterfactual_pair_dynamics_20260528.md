# TDC Pair Dynamics 20260514

Offline post-analysis of completed TDC pair captures. No hardware, Vivado, COM, JTAG, or hw_server access was used.

## Method

- Prefer existing `.tdc_packets.csv`; fall back to raw `.bin` only when packet CSVs are absent.
- Build one code-density phase lookup per lane from the full run, then compute windowed dynamics with the same phase scale.
- `strong_lock_window` is a conservative flag: max absolute lagged phase correlation >= 0.5 within the requested lag range.

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | slope ps/window | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528 | 16 | 32768 | 0.00417253 | 0.0590124 | 1965.36 | 172.478 | -3.4963 | 0 |
| tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528 | 16 | 32768 | 0.0118032 | 0.0578878 | 1955.47 | 156.862 | 0.0320292 | 0 |

## Interpretation

No window crosses the conservative lag-correlation screen. The current data should be described as showing no strong pair locking under this measurement condition.

## Output

- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`
