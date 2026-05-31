# TVLSI Mechanism Validation 20260531

Generated from existing warmup/aperture captures, Board2 XADC diagnostics, route audit, and frozen-prediction outputs.

## Summary

- warmup_aperture_sweep: established (anchor warmup points = 10). 10-point anchor sweep completed for all640, data_ro0, and data_ro4
- aggregate_transition: established (all640 transition bracket = 8->9). aggregate p1 shifts from biased at w8 to near-balanced at w9/w10
- contributor_warmup_sensitivity: established (data_ro4 sign changes = 3). data_ro4 reverses signed bias across warmup, supporting startup/aperture sensitivity
- pvt_manifest: invalid_for_physical_covariate (PVT row validity = invalid=112). PVT rows are parseable but physically invalid and must remain a limitation
- board2_bitstream_xadc_compare: invalid_for_physical_covariate (XADC compare validity = invalid_sentinel_temperature=3). Board2 remains at sentinel XADC values even after programming a historical Board1 TRNG bitstream
- frozen_prediction: mixed (best sign/class/rank = sign=0.666666667, class=1.000000000, rank=0.071428571). sign/class transfer has signal, but rank correlation remains weak
- route_delay_bias_proxy: proxy_only (route rows = 17). route/PIP/net-delay features are available but not calibrated to aperture delay
- toolflow_directive_sensitivity: established_boundary (valid captures / route pairs / stable-route max shift / route-moving max shift = 12/12; pairs=6/6; stable_max=0.000896; moving_max=0.012461). minimal original-vs-Explore matrix preserves bias when extracted routes are stable and bounds larger shifts to route-moving cases

## Interpretation Boundary

The warmup sweep strengthens the startup/aperture mechanism evidence, especially the all640 transition between w8 and w9 and the data_ro4 sign reversals. The toolflow/directive matrix shows that stable-route original-vs-Explore pairs preserve bias within the current measurement scale, while route-moving pairs are treated as implementation-boundary cases. Board2 PVT remains unusable because the same sentinel values appear even after programming a historical Board1 TRNG bitstream.
