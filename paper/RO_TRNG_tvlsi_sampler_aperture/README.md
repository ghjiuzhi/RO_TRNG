# TVLSI Track: Sampler-Aperture-Aware RO-TRNG Implementation

This is a separate TVLSI-oriented paper workspace for a higher-risk, higher-ceiling version of the RO-TRNG restart work.

The working thesis is that sampler-side implementation changes can shift the effective sampling aperture seen by the restarted RO population, reshaping contributor bias and XOR cancellation behavior. The current stage is offline modeling from existing summaries only.

This directory does not replace the TIM manuscript in `paper/RO_TRNG_entropy_boundary`.

## Current Scope

- Build a stochastic contributor and sampler-aperture interpretation model.
- Normalize Board1, Board2, reduced-XOR, warmup, repeat, and route-audit evidence into TVLSI-specific result tables.
- Identify what is already supported, what is only interpretive, and what needs additional validation before TVLSI submission.

## Offline Results

Primary generated output lives outside the paper tree:

`data/experiments/tvlsi_sampler_aperture_model_20260530/`

Generation script:

`scripts/tvlsi_build_sampler_aperture_model_20260530.py`
