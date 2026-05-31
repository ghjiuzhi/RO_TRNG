# TVLSI Toolflow Sensitivity Matrix 20260531

This summary joins the original and Explore/Explore/Explore directive builds for the two held-out sampler contexts. PVT rows are logged for traceability but are not used as covariates.

## Coverage

- Valid captures: 12/12.
- Missing captures: 0/12.
- Invalid captures: 0/12.
- Route pair diffs: 6/6 original-vs-explore1 pairs.

## Matrix

| context_label | anchor | original_status | explore1_status | original_p1 | explore1_p1 | delta_abs_bias_explore1_minus_original | movement_class | sample_ro_route_changed | data_ro_route_changed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| heldout_x36y35 | all640 | ok | ok | 0.499624000 | 0.490577000 | 0.009047000 | broad_route_shift | 9 | 11 |
| heldout_x36y35 | data_ro0 | ok | ok | 0.298739000 | 0.297843000 | 0.000896000 | no_route_shift | 0 | 0 |
| heldout_x36y35 | data_ro4 | ok | ok | 0.395325000 | 0.395775000 | -0.000450000 | no_route_shift | 0 | 0 |
| sample_ro_local | all640 | ok | ok | 0.499545000 | 0.499445000 | 0.000100000 | no_route_shift | 0 | 0 |
| sample_ro_local | data_ro0 | ok | ok | 0.268654000 | 0.267883000 | 0.000771000 | no_route_shift | 0 | 0 |
| sample_ro_local | data_ro4 | ok | ok | 0.554421000 | 0.566882000 | 0.012461000 | sampler_route_shift | 9 | 0 |

## Interpretation Boundary

A stable bias under changed directives supports sampler-aperture robustness, while large bias movement with broad route changes bounds the mechanism claim to a placed/routed physical context. Missing route or capture rows are reported explicitly and are not interpolated.

