# RO_TRNG Access Fallback Plan

This file is local to the RO_TRNG entropy-boundary paper.

## IEEE Access Framing

Frame the paper as a complete engineering study of FPGA RO-TRNG placement sensitivity, reproducible experiment workflow, and broad implications for hardware security practice.

## Emphasis

- Engineering completeness across design, build scripts, capture flow, analysis scripts, and evidence tables.
- Reproducibility and open experiment workflow within the curated project package.
- Broad FPGA/security relevance: placement, sampler implementation, restart behavior, and measurement limits.
- Clear evidence boundaries and limitations, especially certification, multi-board, and PVT scope.

## Risks To Control

- Avoid making the paper feel like a loose collection of experiments.
- Keep a strong central thesis: sampler-side implementation can be part of the entropy boundary.
- Use figures/tables to make the workflow inspectable rather than verbose.
- Preserve the same claim-evidence discipline as the TIM version.
