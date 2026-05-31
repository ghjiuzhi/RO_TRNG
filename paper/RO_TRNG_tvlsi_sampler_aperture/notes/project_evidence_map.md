# Project Evidence Map

This map lists local evidence sources for the independent TVLSI track.

## Board1 Reduced-XOR and Repeat Evidence

- `data/experiments/restart_reduced_xor_vector_anisotropy_20260528/reduced_xor_vector_anisotropy_detail_20260528.csv`
- `data/experiments/restart_reduced_xor_vector_anisotropy_20260528/reduced_xor_vector_anisotropy_group_20260528.csv`
- `data/experiments/restart_reduced_xor_w10_direction_repeat02_full_20260528/summary/w10_direction_repeat02_full_compare_r01.csv`
- `data/experiments/restart_reduced_xor_w10_direction_repeat02_full_20260528/summary/w10_direction_repeat02_full_summary.csv`

Supports contributor-level bias, XOR cancellation interpretation, and same-condition repeat stability for one Board1 setting.

## Board1 Warmup Neighbor Evidence

- `data/experiments/restart_reduced_xor_ro3_warmup_neighbors_20260528/reduced_xor_ro3_warmup_neighbors_20260528.csv`

Supports warmup-sensitive behavior around a strong contributor and neighboring warmup counts.

## Route and Locality Audit Evidence

- `data/experiments/sample_ro_route_diff_20260528/sample_ro_route_evidence_summary_20260528.csv`
- `data/experiments/sample_ro_directive_variance_route_diff_20260528/`

Supports the existence of sampler-side route/PIP/net-delay/local-neighborhood differences across implementation variants. Does not by itself prove complete isolation from FIFO/control/UART movement.

## Balanced Sampler Counterfactual Repeats

- `data/experiments/sample_ro_balanced_repeats_20260528/sample_ro_balanced_repeats_aggregate_20260528.csv`

Supports repeated Board1 sampler counterfactual behavior for compact baseline, forward fail, and reverse repair settings.

## Board2 Evidence

- `data/hardware/20260529_fpga1_board2/restart_counterfactual/summary/board2_restart_counterfactual_summary_20260529.csv`
- `data/hardware/20260529_fpga1_board2/restart_reduced_xor_heldout_sampler_20260530/summary/board2_heldout_sampler_w10_reduced_xor_subset.csv`
- `data/hardware/20260529_fpga1_board2/tdc_counterfactual/summary/`
- `data/hardware/20260529_fpga1_board2/xadc_readings.csv`

Supports two-board extension and held-out sampler interpretation, with current limits on repeat count and full route-feature linkage.
