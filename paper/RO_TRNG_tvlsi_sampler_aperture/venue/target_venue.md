# Target Venue: IEEE TVLSI

Target: IEEE Transactions on Very Large Scale Integration Systems.

Current status: exploratory/offline-model stage.

## Fit Argument

The TVLSI version should be framed as an implementation methodology paper: how sampler placement/routing and timing context affect restart behavior, how reduced-XOR decomposition exposes contributor-level behavior, and how route/timing audit features can become design-rule inputs.

## Required Before Serious Submission

- Resource, timing, and ideally power characterization for all main implementation variants.
- Repeatability across boards, warmup settings, and sampler placements.
- Route/PIP/net-delay/local-neighborhood features connected to measured restart behavior.
- Clear separation between observed evidence and design rules.
- A credible comparison baseline or ablation against conventional RO-TRNG implementation choices.

## Main Risk

The current evidence is strong as a measurement and interpretation story, but TVLSI will expect implementation-depth validation. A stochastic model alone is not enough; it must drive falsifiable implementation predictions or design rules.
