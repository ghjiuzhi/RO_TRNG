# TVLSI Sampler-Aperture Offline Model

Generated from existing CSV summaries and routed-DCP audit CSVs. No hardware capture was run by this script; the held-out sampler route audit was extracted from existing routed DCPs.

## Model

For contributor bitstream `X_i(b,r,w)`, define:

- `p_i = Pr[X_i=1]`
- signed bias `s_i = p_i - 0.5`
- XOR factor `beta_i = 1 - 2p_i`

For an XOR over contributor set `S`, the independence approximation is:

```text
Pr[Y_S=1] = (1 - product_i(1 - 2p_i)) / 2
```

The approximation is intentionally limited. Residuals should be interpreted as correlation, fixed-position restart structure, or unmodeled sampler-aperture effects, not as a calibrated physical proof.

## Generated Tables

| Table | Rows | Path |
|---|---:|---|
| Contributor dataset | 110 | `data\experiments\tvlsi_sampler_aperture_model_20260530\contributor_dataset.csv` |
| XOR cancellation model | 6 | `data\experiments\tvlsi_sampler_aperture_model_20260530\xor_cancellation_model.csv` |
| Repeat stability summary | 7 | `data\experiments\tvlsi_sampler_aperture_model_20260530\repeat_stability_summary.csv` |
| Warmup neighbor summary | 6 | `data\experiments\tvlsi_sampler_aperture_model_20260530\warmup_neighbor_summary.csv` |
| Route feature summary | 8 | `data\experiments\tvlsi_sampler_aperture_model_20260530\route_feature_summary.csv` |
| Held-out sampler route audit | 2 | `data\experiments\tvlsi_sampler_aperture_model_20260530\heldout_sampler_route_audit_summary.csv` |
| Held-out sampler route pair diff | 6 | `data\experiments\tvlsi_sampler_aperture_model_20260530\heldout_sampler_route_pair_diff_summary.csv` |
| Sampler counterfactual board summary | 18 | `data\experiments\tvlsi_sampler_aperture_model_20260530\sampler_counterfactual_board_summary.csv` |
| Prediction versus observed | 23 | `data\experiments\tvlsi_sampler_aperture_model_20260530\prediction_vs_observed.csv` |
| Frozen prediction versus observed | 68 | `data\experiments\tvlsi_sampler_aperture_model_20260530\frozen_prediction_vs_observed.csv` |
| Prediction metrics summary | 4 | `data\experiments\tvlsi_sampler_aperture_model_20260530\prediction_metrics_summary.csv` |
| Mechanism ablation summary | 4 | `data\experiments\tvlsi_sampler_aperture_model_20260530\mechanism_ablation_summary.csv` |
| Route/result correlation | 102 | `data\experiments\tvlsi_sampler_aperture_model_20260530\route_result_correlation.csv` |
| Input source status | 14 | `data\experiments\tvlsi_sampler_aperture_model_20260530\input_source_status.csv` |

## First Offline Highlights

- Board1 full 8-data-RO independence approximation predicts p1=0.500001394 versus measured all64 p1=0.458617000, leaving residual -0.041384394.
- Board2 held-out sampler uses 8 data-RO contributors and predicts p1=0.499996685 versus measured aggregate p1=0.500718000.
- Board1 data_ro repeat has same bias sign 8/8 with Pearson r=0.999678268.
- Held-out prediction table contains 17 Board1-prior-to-Board2 rows with 10 sign matches; this is a falsification-oriented prior, not a calibrated transfer model.
- Second held-out frozen prediction evaluated 68 rows across 4 baselines; see prediction metrics for accuracy and residuals.
- Held-out route audit keeps data-RO cells fixed (0/16 LOC changes) while moving sample-RO cells (9/9 LOC changes) and changing 27/36 sample-RO nets.
- Route/result correlation table has 102 rows, with observed p1 joined for 10; unmatched rows are retained as route-only or implementation-gate evidence.
- Forward sampler counterfactual remains biased in both balanced summaries: Board1 w4 mean p1=0.377401333 over n=3; Board2 w4 mean p1=0.450792000 over n=3.

## Interpretation

The useful TVLSI-level story is not simply that one run is biased. The stronger story is that the contributor distribution, warmup setting, board instance, and sampler route context jointly determine the effective sampling aperture. XOR aggregation can hide biased contributors through cancellation, so aggregate pass/fail metrics alone are not enough for implementation guidance.

## Current Limits

- The XOR model assumes independent contributors and therefore cannot explain correlation or deterministic startup-position structure by itself.
- Route/PIP/net-delay linkage is extracted for the original sampler-island, first held-out sample-x36y35, and second held-out sample_ro_local contexts when those routed-DCP audits are present.
- Route/result correlation remains mixed evidence: per-bitstream route rows are available, but the route/aperture proxy is not yet a calibrated causal model.
- Frozen second-held-out prediction is evaluated when the second full map is present; weak baselines and residuals are retained as model-boundary evidence.
- This report is an interpretation scaffold. TVLSI-strength mechanism claims still need targeted phase/PVT/coupling experiments.

## Missing Optional Inputs

- None of the tracked optional inputs are missing.
