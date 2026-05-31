# Toolflow Sensitivity Boundary

Date: 2026-05-31

This note records what the current repository can and cannot say about
toolflow, seed, and directive sensitivity for the TVLSI sampler-aperture track.

## Current Evidence

The repository now contains the minimum TVLSI toolflow/directive matrix:

- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_sensitivity_matrix.csv`
- `data/experiments/toolflow_sensitivity_matrix_20260531/route_overlap_vs_bias_shift.csv`
- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_route_pair_diff_summary.csv`
- `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_sensitivity_summary.md`
- `data/experiments/toolflow_sensitivity_matrix_20260531/route_extract/`

Coverage:

- 2 contexts: first held-out sampler and second `sample_ro_local`.
- 3 anchors per context: `all640`, `data_ro0`, and `data_ro4`.
- 2 implementation settings per anchor: original and
  `Explore/Explore/Explore`.
- 12/12 matched hardware captures are valid.
- 6/6 original-vs-Explore route-pair diffs are present.

Main result:

| Context | Anchor | Original p1 | Explore p1 | Delta abs bias | Route movement class |
|---|---:|---:|---:|---:|---|
| heldout_x36y35 | all640 | 0.499624 | 0.490577 | 0.009047 | broad_route_shift |
| heldout_x36y35 | data_ro0 | 0.298739 | 0.297843 | 0.000896 | no_route_shift |
| heldout_x36y35 | data_ro4 | 0.395325 | 0.395775 | -0.000450 | no_route_shift |
| sample_ro_local | all640 | 0.499545 | 0.499445 | 0.000100 | no_route_shift |
| sample_ro_local | data_ro0 | 0.268654 | 0.267883 | 0.000771 | no_route_shift |
| sample_ro_local | data_ro4 | 0.554421 | 0.566882 | 0.012461 | sampler_route_shift |

This supports a bounded statement: the mechanism is not explained away as a
blanket directive artifact, because stable-route original-vs-Explore pairs
remain bias-stable. When the extracted route moves, larger bias shifts are
observed and should be reported as implementation-context sensitivity.

## Boundary

Current TVLSI evidence can say:

- route/PIP/net-delay features are measurable and differ across implementation
  contexts;
- route features should be treated as implementation variables rather than
  hidden nuisance details;
- stable extracted routes in this minimum matrix correspond to small observed
  original-vs-Explore bias shifts;
- route/audit features are proxy variables for sampler aperture, not a
  calibrated physical aperture shift.

Current evidence should not say:

- the Vivado seed/directive effect has been fully characterized;
- observed bias shifts are caused only by sampler-route movement;
- data-RO placement stability alone proves complete physical isolation;
- route-delay numbers directly equal effective sampler aperture delay.

## Matrix Interpretation

The completed matrix distinguishes three cases:

1. data-RO cells fixed while sampler/local route changes;
2. sampler route fixed while broader control/FIFO/UART logic moves;
3. both data and sampler contexts move, making causal interpretation weak.

In the current data, four pairs are `no_route_shift` and show small
`delta_abs_bias` magnitudes (`0.000100` to `0.000896`). One pair is
`sampler_route_shift` (`sample_ro_local`/`data_ro4`, `delta_abs_bias=0.012461`)
and one pair is `broad_route_shift` (`heldout_x36y35`/`all640`,
`delta_abs_bias=0.009047`).

## How To Use In The Paper

Use this as a mechanism-boundary validation table. The paper can state that the
selected sampler-aperture observations survive a minimal directive perturbation
when the extracted local routes remain stable, while also acknowledging that
route-moving cases remain implementation-sensitive and do not provide isolated
causal proof.
