# Toolflow Sensitivity Manuscript Table

Date: 2026-05-31

Purpose: provide a manuscript-ready table and conservative wording for the
minimal original-vs-Explore directive sensitivity matrix. This note belongs to
the TVLSI sampler-aperture track and does not modify or depend on the TIM
manuscript.

## Manuscript-Ready Table

| Context | Anchor | Original p1 | Explore p1 | Delta p1 | Delta abs bias | Route movement |
|---|---:|---:|---:|---:|---:|---|
| heldout_x36y35 | all640 | 0.499624 | 0.490577 | -0.009047 | 0.009047 | broad_route_shift |
| heldout_x36y35 | data_ro0 | 0.298739 | 0.297843 | -0.000896 | 0.000896 | no_route_shift |
| heldout_x36y35 | data_ro4 | 0.395325 | 0.395775 | 0.000450 | -0.000450 | no_route_shift |
| sample_ro_local | all640 | 0.499545 | 0.499445 | -0.000100 | 0.000100 | no_route_shift |
| sample_ro_local | data_ro0 | 0.268654 | 0.267883 | -0.000771 | 0.000771 | no_route_shift |
| sample_ro_local | data_ro4 | 0.554421 | 0.566882 | 0.012461 | 0.012461 | sampler_route_shift |

Source files:

- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_sensitivity_matrix.csv`
- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_route_pair_diff_summary.csv`
- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_sensitivity_summary.md`

## Conservative Claim Text

The minimal directive-sensitivity matrix separates route-stable and
route-moving cases. In the four original-vs-Explore pairs where the extracted
sample, sampled-data, and data routes did not change, the absolute-bias shift
remained small (`0.000100` to `0.000896`). The two larger shifts occurred only
when extracted routes moved: heldout `all640` under broad route movement
(`0.009047`) and second-heldout `data_ro4` under sampler-route movement
(`0.012461`). Thus the observed sampler-aperture behavior is not explained away
as a blanket Vivado directive artifact, but the route-moving rows remain
implementation-context boundary cases.

## Must Not Claim

- Do not claim that every Vivado seed or directive has been characterized.
- Do not claim that route movement alone proves calibrated physical aperture
  delay.
- Do not use Board2 XADC/PVT as a covariate; the current toolflow run still
  logged sentinel temperature and zero rails.

## Paper Placement

Use this as a validation/limitation table near the mechanism-validation
discussion. It should support a bounded robustness claim, while preserving the
distinction between stable-route directive perturbation and route-moving
implementation sensitivity.
