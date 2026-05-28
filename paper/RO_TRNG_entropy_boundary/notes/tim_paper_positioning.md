# TIM Paper Positioning

## Active Target

The current primary target is IEEE Transactions on Instrumentation and Measurement. The paper should be positioned as a measurement-driven characterization and TDC-assisted diagnosis study of FPGA RO-TRNG entropy-source boundaries.

IEEE Access remains a fallback if the manuscript is expanded toward engineering completeness and broad reproducibility. IEEE TCAS-II, IEEE TVLSI, and Journal of Cryptographic Engineering are future possible targets only after adding stronger evidence.

## Central Thesis

The paper should argue that the sampler-side physical implementation should be included in the measured entropy-source boundary of the evaluated FPGA RO-TRNG. In the current evidence, the relevant boundary is not limited to data ROs and sampled-data registers; it includes the sample RO, sampler-side routing, and restart/warmup/reset timing that directly shapes early-sampling behavior. Post-XOR FIFO buffering, UART transport, host capture, and offline analysis should remain outside the entropy-source boundary and be treated as measurement/readout elements or residual routed-neighborhood confounders where their implementation changes.

This thesis is supported as a bounded measurement claim, not as a universal cross-device rule.

## TIM Framing

The TIM-oriented framing should emphasize:

- hardware measurement across placement variants, restart warmup settings, TDC observations, and sampler-side counterfactuals;
- diagnostic use of TDC evidence to constrain mechanism hypotheses;
- evidence-backed boundary definition for what should be measured when evaluating FPGA RO-TRNG entropy sources;
- repeatability and reproducibility within the recorded Zynq-7020 board/setup;
- explicit uncertainty around multi-board, PVT, and certification-level claims.

The paper should avoid a pure cryptographic-compliance framing. SP800-90B restart and non-IID results can be used as entropy-assessment evidence, but not as a claim of complete SP800-90B certification.

## Measurement Storyline

1. Placement materially changes measured output quality in the recorded FPGA setup.
2. Continuous-stream quality alone is not enough to characterize restart and early-sampling behavior.
3. Restart warmup scans expose fixed-position startup bias and a transition between failing and passing warmup settings under the measured protocol.
4. Pairwise and reset-aligned TDC measurements argue against a simple pairwise RO hard-locking explanation as the dominant mechanism.
5. Sample-RO placement counterfactuals flip restart outcomes in both directions, giving the strongest evidence that sampler-side physical implementation is part of the entropy-source boundary.
6. Reduced-XOR counterfactuals show that final output quality can depend on sampler-vector XOR cancellation among biased directions, further supporting a boundary broader than individual data ROs.

## Evidence Tone

Use conservative measurement language:

- `observed`, `measured`, `indicates`, `suggests`, `is consistent with`;
- `rules out a simple hard-locking-only explanation` only for the measured TDC conditions;
- `supports treating sampler-side implementation as part of the boundary` rather than `proves all sampler circuits are entropy sources`.

Avoid:

- complete SP800-90B certification claims;
- cross-board or cross-PVT generalization;
- ps-level jitter metrology claims from raw TDC bins;
- statements that bad placement is simply RO-to-RO hard locking.

## Venue Adaptation

Venue adaptation should remain data-driven and should use `venue/target_venue.md` together with reusable venue profiles. Do not create separate skills for IEEE TIM, IEEE Access, TCAS-II, TVLSI, or JCEN.

For the current TIM target, emphasize characterization, measurement protocol, diagnosis, and boundary definition.

For IEEE Access fallback, expand implementation completeness, reproducibility, open evidence mapping, and broad FPGA/security relevance.

For TCAS-II, a future version would need a compressed circuits-and-systems message, likely around sampler-side counterfactuals and a concise physical mechanism.

For TVLSI, a future version would need stronger implementation evidence: multi-board/PVT, resource/timing/power, placement-aware design rules, and design-rule validation.

For JCEN, a future version would need stronger entropy-source modeling, security argumentation, health-test integration, conditioning discussion, and a clearer SP800-90B boundary package.
