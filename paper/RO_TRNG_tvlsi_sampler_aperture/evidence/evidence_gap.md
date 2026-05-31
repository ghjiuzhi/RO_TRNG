# TVLSI Evidence Gap

## Already Useful

- Contributor-level reduced-XOR tables.
- Board1 balanced counterfactual repeats.
- Board2 counterfactual and held-out sampler summaries.
- Route/PIP/net-delay audit summaries.
- First offline TVLSI normalized outputs in `data/experiments/tvlsi_sampler_aperture_model_20260530/`.
- Held-out sampler routed-DCP audit in `data/experiments/heldout_sampler_route_diff_20260530/`.
- Per-bitstream held-out route audit for all 17 reduced-XOR bitstreams: `data/experiments/heldout_sampler_route_diff_20260530/heldout_per_bitstream_route_audit_20260530.csv`.
- Standardized implementation metrics for original and held-out variants: `data/experiments/tvlsi_sampler_aperture_model_20260530/implementation_metrics_20260530.csv`.
- Held-out prediction and route/result correlation outputs: `prediction_vs_observed.csv`, `route_result_correlation.csv`, and `input_source_status.csv`.
- Schema-stable frozen-prediction outputs are ready for the second held-out context: `frozen_prediction_vs_observed.csv`, `prediction_metrics_summary.csv`, and `mechanism_ablation_summary.csv`.
- Second held-out `sample_ro_local` full map and anchor repeats are captured: `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/second_heldout_reduced_xor_full_map.csv` and `board2_second_heldout_sample_ro_local_anchor_repeats_aggregate.csv`.
- Second held-out per-bitstream route/PIP/net-delay audit and implementation metrics cover all 17 reduced-XOR bitstreams: `data/experiments/second_heldout_sampler_route_diff_20260530/second_heldout_per_bitstream_route_audit_20260530.csv` and `second_heldout_implementation_metrics_20260530.csv`.
- Frozen second-held-out prediction is now evaluated across 68 rows and four baselines: `data/experiments/tvlsi_sampler_aperture_model_20260530/frozen_prediction_vs_observed.csv`, `prediction_metrics_summary.csv`, and `mechanism_ablation_summary.csv`.
- Second held-out warmup/aperture anchor sweep is complete for 10 warmup points over `all640`, `data_ro0`, and `data_ro4`, with no expected anchor captures missing: `data/experiments/second_heldout_warmup_aperture_sweep_20260530/second_heldout_warmup_aperture_sweep.csv`.
- Mechanism-validation summary tables now join warmup/aperture behavior, route-delay proxy features, frozen prediction metrics, and PVT/XADC boundary cases: `data/experiments/tvlsi_mechanism_validation_20260531/`.
- Toolflow/directive sensitivity matrix now covers 2 contexts x 3 anchors x original/Explore implementations with 12/12 valid captures and 6/6 route-pair diffs: `data/experiments/toolflow_sensitivity_matrix_20260531/`.
- Board2 XADC invalidity has been checked against a historical Board1 TRNG bitstream programmed on Board2; it still returns sentinel temperature and zero rails, so the failure is not explained by the current reduced-XOR bitstream alone: `data/experiments/xadc_summary/board2_bitstream_xadc_compare_20260531.csv`.
- Physical mechanism scaffold separating directly estimable, proxy-estimable, and non-identifiable parameters: `paper/RO_TRNG_tvlsi_sampler_aperture/notes/physical_mechanism_scaffold_20260530.md`.

## Offline Model Result So Far

- Board1 full 8-data-RO independence approximation predicts XOR `p1 = 0.500001394`, but measured all64 is `p1 = 0.458617000`. This residual is useful because it exposes what the simple independent-contributor model cannot explain.
- With the full held-out map present, Board2 held-out sampler uses eight measured data-RO contributors and the independent-XOR approximation predicts `p1 = 0.499996685` versus measured aggregate `p1 = 0.500718000`.
- The Board1-prior held-out prediction table has 17 Board1-to-Board2 rows; it keeps sign mismatches and residuals explicit rather than treating the simple prior as calibrated.
- The second-held-out frozen prediction tables now evaluate four baselines. Contributor-only independent XOR gives the best sign accuracy among the current baselines (`0.6667`) and class accuracy (`1.0000`) but worse MAE than aggregate-only; contributor plus warmup plus route/aperture gives sign accuracy `0.6471`, class accuracy `0.6471`, and MAE `0.0858`. This is useful evidence, but not a calibrated physical model.
- Board1 same-condition reduced-XOR repeat preserves bias sign for 8/8 data-RO contributors and 8/8 except-data-RO complements.
- Board2 restart counterfactuals now have seven target aggregate conditions at `n = 3`, including compact baseline w4/w5/w11, forward Srestart w4/w5/w11, and reverse Scompact w4.
- Held-out route audit keeps data-RO cells fixed at 0/16 LOC changes while moving 9/9 sample-RO cells and changing 27/36 sample-RO nets.
- Per-bitstream held-out route audit covers 17/17 usable routed DCPs and 16/16 all640-to-subset pairwise comparisons; data-RO cells remain LOC/BEL stable in every held-out comparison.
- Second held-out route audit covers 17/17 routed DCPs and 16/16 all640-to-subset pairwise comparisons. The route features vary strongly across subset bitstreams; the implementation metrics table reports LUT/FF/BRAM, WNS/WHS, power, route status, and DRC counts for all 17.
- Route/result correlation is a mixed table: Board1 route rows can join to Board1 observed summaries, held-out all640 rows join to held-out full-map observations, per-bitstream held-out rows expose route/PIP/net-delay features, implementation metrics add resource/timing/power/status, and route-lock feasibility rows remain implementation-gate evidence.
- The second held-out warmup/aperture sweep adds a stronger mechanism signal than another same-warmup repeat: `all640` moves from a biased point at `w8` (`abs_bias=0.180194`) to near-balanced points at `w9/w10`, while `data_ro4` changes signed-bias direction three times across the observed warmups.
- The mechanism-validation output currently supports a falsifiable startup/aperture interpretation, not a calibrated physical model: warmup transition and contributor sign reversal are established; route/PIP/net-delay remains a proxy; PVT is invalid; frozen prediction has useful sign/class signal but weak rank correlation.
- The toolflow/directive matrix separates stable-route and route-movement cases: four pairs with no sample/data/sampled-data route changes have small absolute-bias shifts (`0.000100` to `0.000896`), while heldout `all640` has a broad route shift with `delta_abs_bias=0.009047` and second-heldout `data_ro4` has a sampler-route shift with `delta_abs_bias=0.012461`.

## Missing for Strong TVLSI

- Valid PVT readings tied to each capture. A PVT manifest exists for the second held-out run, but current XADC values are invalid (`-273.1 C`, zero rails) across the current 112 manifest rows and remain invalid after programming a historical Board1 TRNG bitstream onto Board2, so this is structural logging rather than usable physical PVT evidence.
- Targeted phase/aperture/coupling experiments needed to identify the non-identifiable parameters listed in the mechanism scaffold.

## Keep as Future Work Unless Validated

- Calibrated physical jitter propagation.
- Metastability S-curve or logistic transfer fitting.
- Formal RTL/Vivado timing-to-sampler-aperture derivation.
- Full probabilistic graphical model with identified parameters.
