# TVLSI Offline Model Plan

## Purpose

Build a compact interpretation model that connects four evidence families:

1. Reduced-XOR contributor decomposition.
2. Warmup-dependent restart behavior.
3. Board and sampler-placement differences.
4. Route, PIP, net-delay, and local-neighborhood audit features.

This is not yet a calibrated physical jitter model, a metastability transfer model, or a full timing-path proof. It is the bridge that makes those later extensions measurable.

## Variables

- `b`: board or device instance.
- `r`: implementation route/sampler context.
- `w`: warmup count.
- `i`: contributor index.
- `X_i(b,r,w)`: binary output stream from contributor `i`.
- `p_i(b,r,w) = Pr[X_i=1]`: observed contributor one-probability.
- `s_i = p_i - 0.5`: signed contributor bias.
- `beta_i = 1 - 2p_i`: signed XOR factor.
- `Y_S = xor_{i in S} X_i`: XOR aggregation over contributor set `S`.

Under an independence approximation:

```text
Pr[Y_S = 1] = (1 - product_i(1 - 2p_i)) / 2
```

Residuals between this approximation and measured aggregate outputs are interpreted as evidence of correlation, fixed-position startup structure, or unmodeled sampler-aperture effects.

## TVLSI Upgrade Path

The model becomes TVLSI-strength only if it supports held-out predictions:

- predict direction or magnitude of bias when sampler route context changes;
- predict which contributors become dominant after a sampler move;
- explain when XOR cancellation hides bad contributors;
- identify route/timing features that correlate with aperture-sensitive behavior.
