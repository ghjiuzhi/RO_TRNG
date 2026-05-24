# Mechanism Hypothesis Evidence Table

Offline placement-level evidence chain assembled from existing CSV artifacts.

## Outputs

- `mechanism_hypothesis_evidence_by_placement.csv`: one row per placement with continuous TRNG, restart, RO_FREQ, and TDC evidence where available.
- `README.md`: this summary.

## Inputs

- `data/experiments/position_structure_20260523/position_structure_summary.csv`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.csv`
- `data/experiments/restart_summary_20260515/restart_result_summary_20260522.csv`
- `data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv`
- `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.csv`
- `data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv`

## Notes

- Continuous fields come from `position_structure_summary.csv`: `bit_min_entropy`, `p1`, `adjacent_equal`, and `lag1_phi`.
- Restart fields are placement summaries: fail/pass counts, observed warmups, warmup transition text, and the row with the largest `worst_x`/`x_max`.
- RO_FREQ fields are prefixed with `rofreq_` and are present only for placements covered by the correlation table.
- TDC fields are grouped by parsing `tdc_pair_<placement>_...` from run names.
- Sampler-ablation fields summarize the `random1` sampler-side causal experiment.
- `failure_mode_guess` is a heuristic label for triage, not a statistical proof.
- This script is offline-only and does not start hardware, Vivado, UART, JTAG, or capture jobs.

## Failure Mode Guess Counts

- `continuous_bias`: 5
- `continuous_only_no_restart`: 1
- `repeat_summary_only`: 1
- `warmup_sensitive_restart_bias`: 4
