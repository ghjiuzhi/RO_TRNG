# Mechanism Validation Plan and Current Status

Date: 2026-05-31

This note tracks the TVLSI mechanism-validation path after the first and second
held-out sampler contexts. It is scoped to the independent TVLSI directory and
does not modify or reinterpret the TIM manuscript.

## Goal

Move from a descriptive sampler-aperture interpretation to a falsifiable
mechanism evidence chain:

```text
contributor decomposition
-> XOR cancellation and residual
-> repeat stability
-> route/aperture proxy linkage
-> frozen held-out prediction
-> warmup/aperture transition behavior
-> minimal toolflow/directive sensitivity matrix
-> explicit PVT and model boundaries
```

The target is not to claim a calibrated physical jitter, coupling, or
metastability model. The target is to show that the measured behavior is
consistent with a startup-phase and sampler-aperture mechanism, while keeping
the current non-identifiable parameters separate.

## Current Evidence State

| Evidence item | Current state | Primary files |
|---|---|---|
| Full reduced-XOR map | Two held-out contexts available | `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/second_heldout_reduced_xor_full_map.csv` |
| Anchor repeats | `all640`, strongest-low, and strongest-high at `n=3` for second held-out context | `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/board2_second_heldout_sample_ro_local_anchor_repeats_aggregate.csv` |
| Route audit | 17/17 second-heldout routed bitstreams audited | `data/experiments/second_heldout_sampler_route_diff_20260530/second_heldout_per_bitstream_route_audit_20260530.csv` |
| Frozen prediction | Four baselines evaluated | `data/experiments/tvlsi_sampler_aperture_model_20260530/prediction_metrics_summary.csv` |
| Warmup/aperture sweep | Ten anchor warmup points complete, no expected anchor missing | `data/experiments/second_heldout_warmup_aperture_sweep_20260530/second_heldout_warmup_aperture_sweep.csv` |
| Toolflow/directive sensitivity | 12/12 captures and 6/6 original-vs-Explore route-pair diffs complete | `data/experiments/toolflow_sensitivity_matrix_20260531/toolflow_sensitivity_matrix.csv` |
| Mechanism summary | Warmup, route proxy, prediction, toolflow boundary, and PVT boundaries joined | `data/experiments/tvlsi_mechanism_validation_20260531/mechanism_validation_summary.csv` |
| PVT logging | Structurally logged but physically invalid on Board2 | `data/experiments/xadc_summary/pvt_xadc_manifest_validation_20260531.csv` |

## Key Mechanism Observations

- `all640` has an observed transition bracket from `w8` to `w9`: the aggregate
  changes from a biased point at `w8` to near-balanced points at `w9/w10`.
- `data_ro4` changes signed-bias direction three times across the observed
  warmups, which is stronger evidence for startup/aperture sensitivity than a
  single same-warmup repeat.
- `data_ro0` remains biased but its bias magnitude shifts strongly across
  warmup, so it is useful as a magnitude-sensitive anchor even without a sign
  reversal.
- Frozen prediction has useful sign/class signal but weak rank correlation, so
  it should be reported as partial transfer rather than calibrated prediction.
- Route/PIP/net-delay features are available as implementation proxies, but
  they are not calibrated sampler-aperture delays.
- The minimal original-vs-Explore toolflow matrix preserves bias under stable
  extracted routes (`0.000100` to `0.000896` absolute-bias shift magnitude) and
  shows larger shifts only in route-moving cases.
- Board2 PVT cannot be used as a covariate in the current setup.

## Paper Use

The TVLSI manuscript can safely claim:

- reduced-XOR decomposition exposes contributor-level bias hidden by XOR
  aggregation;
- selected contributor and aggregate behaviors are repeatable enough to support
  mechanism tests;
- route and sampler context are measurable implementation variables;
- warmup/aperture sweep produces a falsifiable mechanism signal;
- stable-route directive perturbation does not explain away the observed
  sampler-aperture behavior, while route-moving rows remain implementation
  boundary cases;
- the current model has explicit boundaries: weak rank prediction, invalid
  Board2 PVT, proxy-only route timing, and no full seed sweep.

The manuscript should not claim:

- calibrated physical jitter propagation;
- fitted metastability transfer constants;
- identified coupling coefficients;
- formal timing-path-to-aperture derivation;
- PVT dependence on Board2;
- complete Vivado seed/directive invariance.

## Next Proof Step

The highest-value route-sensitivity perturbation has now been run as the
minimal toolflow/directive matrix. The next proof step should be manuscript
integration and export, not more immediate hardware expansion:

1. Use `toolflow_sensitivity_manuscript_table_20260531.md` as the table source.
2. Keep the claim bounded to stable-route robustness plus route-moving
   implementation sensitivity.
3. Preserve PVT as a limitation until Board2 XADC is physically valid.
4. Add a larger seed/directive sweep only if reviewers specifically require
   toolflow breadth beyond the current minimal matrix.
