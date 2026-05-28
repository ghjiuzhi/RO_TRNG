# TDC Pair Dynamics 20260514

Offline post-analysis of completed TDC pair captures. No hardware, Vivado, COM, JTAG, or hw_server access was used.

## Method

- Prefer existing `.tdc_packets.csv`; fall back to raw `.bin` only when packet CSVs are absent.
- Build one code-density phase lookup per lane from the full run, then compute windowed dynamics with the same phase scale.
- `strong_lock_window` is a conservative flag: max absolute lagged phase correlation >= 0.5 within the requested lag range.

## Run Summary

| run | windows | packets | mean phase r | max abs lag r | mean diff std ps | diff mean span ps | slope ps/window | strong lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| tdc_counterfactual_scompact_ro3_warmup4_32768_run01_20260528 | 16 | 32768 | 0.010091 | 0.0647687 | 1962.12 | 94.3586 | 2.15299 | 0 |
| tdc_counterfactual_srestart_ro3_warmup4_32768_run01_20260528 | 16 | 32768 | 0.000202033 | 0.066234 | 1970.82 | 211.557 | -3.58006 | 0 |

## Interpretation

No window crosses the conservative lag-correlation screen. The current data should be described as showing no strong pair locking under this measurement condition.

## Output

- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`
