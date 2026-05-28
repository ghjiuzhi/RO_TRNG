# RO_TRNG TIM Plan

This file is local to the RO_TRNG entropy-boundary paper.

## IEEE TIM Framing

Frame the paper as measurement-driven characterization of FPGA RO-TRNG entropy-source behavior, using instrumentation-style evidence to diagnose where the entropy boundary should be drawn.

## Emphasis

- Measurement-driven characterization rather than only a new TRNG architecture.
- TDC-assisted diagnosis of placement-sensitive behavior.
- Sampler-side entropy boundary and how implementation choices affect measured entropy behavior.
- Restart evidence as a measurement of startup-position bias and entropy-source stability.
- Reduced-XOR counterfactual evidence as a diagnostic experiment, not a broad universal claim.

## Risks To Control

- Avoid presenting formal-size SP800-90B results as complete certification.
- Avoid overgeneralizing from one board or one FPGA family.
- Make every measurement claim traceable to local scripts, data summaries, or documented experiment logs.
- Keep claims bounded to the observed setup unless additional evidence is added.
