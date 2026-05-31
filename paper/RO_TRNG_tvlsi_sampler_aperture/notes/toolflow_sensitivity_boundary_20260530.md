# Toolflow Sensitivity Boundary

Date: 2026-05-31

This note records what the current repository can and cannot say about
toolflow, seed, and directive sensitivity for the TVLSI sampler-aperture track.

## Current Evidence

The repository already contains route-diff artifacts for a small directive
variance check:

- `data/experiments/sample_ro_directive_variance_route_diff_20260528/`
- `data/experiments/sample_ro_directive_variance_route_diff_20260528/sample_ro_route_evidence_summary_20260528.csv`
- `data/experiments/sample_ro_directive_variance_route_diff_20260528/sample_ro_route_evidence_summary_20260528.md`

Those artifacts are useful because they show that implementation choices can
move route/PIP/net-delay and neighborhood features. They are not yet the full
TVLSI seed/directive sensitivity matrix because they do not cover the planned
two contexts, three anchor bitstreams, and at least two implementation variants
with matched hardware captures.

## Boundary

Current TVLSI evidence can say:

- route/PIP/net-delay features are measurable and differ across implementation
  contexts;
- route features should be treated as implementation variables rather than
  hidden nuisance details;
- current route/audit features are proxy variables for sampler aperture, not a
  calibrated physical aperture shift.

Current evidence should not say:

- the Vivado seed/directive effect has been fully characterized;
- observed bias shifts are caused only by sampler-route movement;
- data-RO placement stability alone proves complete physical isolation;
- route-delay numbers directly equal effective sampler aperture delay.

## Minimum Matrix Still Missing

For a stronger TVLSI response to seed/directive questions, run the smallest
complete matrix:

| Dimension | Minimum values |
|---|---|
| Contexts | first held-out sampler and second `sample_ro_local` |
| Bitstreams | `all640`, `data_ro0`, `data_ro4` |
| Implementations | original route and one alternate seed/directive or placement-preserved reroute |
| Captures | `run01` for each row; repeat only if an anchor flips or looks anomalous |
| Route audit | LOC/BEL, PIP overlap, changed nets, net-delay mean/max, neighborhood rows |
| Metrics | WNS/WHS, power, route status, DRC status |

The acceptance criterion is not that every metric improves. The criterion is
that the paper can distinguish three cases:

1. data-RO cells fixed while sampler/local route changes;
2. sampler route fixed while broader control/FIFO/UART logic moves;
3. both data and sampler contexts move, making causal interpretation weak.

## How To Use In The Paper

Use this as a limitation and future validation hook unless the full matrix is
run. The current manuscript can include route sensitivity as partial
implementation evidence, but should reserve strong seed/directive claims for a
completed matrix with matched hardware captures.
