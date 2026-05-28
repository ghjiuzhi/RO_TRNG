# Reduced-XOR data_ro3 Warmup-Neighbor Summary

## Mechanism Question

This experiment tests whether the strongest high-biased warmup-10 direction, `data_ro3`, is a warmup-10-only artifact or a stable same-data-RO direction whose complement/cancellation behavior changes with the restart warmup window.

## Results

| warmup | data_ro3 p1 | data_ro3 min-H | except_ro3 p1 | except_ro3 min-H | interpretation |
| ---: | ---: | ---: | ---: | ---: | --- |
| 5 | 0.576638 | 0.794262182 | 0.503005 | 0.991355354 | high-biased direction persists; complement is near balanced |
| 10 | 0.671833 | 0.573825433 | 0.55393 | 0.85222442 | high-biased direction peaks; complement remains moderately high-biased |
| 11 | 0.54456 | 0.87683708 | 0.501558 | 0.995511552 | high-biased direction persists; complement is near balanced |

## Interpretation

`data_ro3` is high-biased at all three warmups, but the bias is strongest at warmup 10. Its complement is near balanced at warmup 5 and warmup 11, while warmup 10 leaves a moderate high bias. This supports a sampler-vector cancellation model rather than a single bad direction model: individual directions can be stable biased hardware functions, but the final all64 quality depends on how the remaining directions cancel or reinforce them under a specific startup/warmup condition.

## Execution Note

The first hardware queue attempted `RecordXadc` before capture and produced zero-byte captures because the additional Vivado/XADC step missed the auto-stream UART window for this 60 s start-delay bitstream. A no-XADC sanity capture of the existing warmup-10 all64 bitstream succeeded, and the four target captures were then rerun without pre-capture XADC. XADC readings taken immediately before the failed queue were around 43.7-43.9 C with nominal rails, so they are contextual only, not per-capture measurements.

## Source Files

- `data/experiments/restart_reduced_xor_w10_direction_map_20260526/summary/w10_direction_map_combined.csv`
- `data/experiments/restart_reduced_xor_w5_w11_data_ro3_except3_20260528/profile/restart_reduced_xor_strict_20260526_summary.csv`
- `data/experiments/fast_mode/hardware_queue_restart_reduced_xor_w5_w11_data_ro3_except3_20260528.csv`

## Detailed Rows

| mode | warmup | p1 | abs bias | min-H | row ones std | worst byte.bit | worst x | worst p1 | source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| data_ro | 5 | 0.576638 | 0.076638 | 0.794262182 | 8.852511282 | 1.7 | 769 | 0.769 | w5_w11_ro3_warmup_neighbors_20260528 |
| except_data_ro | 5 | 0.503005 | 0.003005 | 0.991355354 | 16.05867289 | 50.7 | 557 | 0.557 | w5_w11_ro3_warmup_neighbors_20260528 |
| data_ro | 10 | 0.671833 | 0.171833 | 0.573825433 | 11.445833784 | 2.5 | 804 | 0.804 | w10_direction_map_20260526 |
| except_data_ro | 10 | 0.55393 | 0.05393 | 0.85222442 | 18.397801499 | 3.3 | 603 | 0.603 | w10_direction_map_20260526 |
| data_ro | 11 | 0.54456 | 0.04456 | 0.87683708 | 8.132428911 | 0.5 | 730 | 0.73 | w5_w11_ro3_warmup_neighbors_20260528 |
| except_data_ro | 11 | 0.501558 | 0.001558 | 0.995511552 | 14.921214294 | 89.3 | 560 | 0.56 | w5_w11_ro3_warmup_neighbors_20260528 |
