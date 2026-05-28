# TIM Contribution Statement

## One-Paragraph Contribution

This paper presents a measurement-driven characterization of an FPGA RO-TRNG in which placement, restart behavior, TDC-assisted diagnosis, and sampler-side counterfactual experiments are analyzed together to define the practical entropy-source boundary. The central contribution is the observation, under the recorded Zynq-7020 setup, that sampler-side physical implementation is not merely passive readout: changing the sample RO and nearby sampler implementation can reshape the restart warmup passband and flip measured outcomes. The paper therefore argues that FPGA RO-TRNG evaluation should include sampler-side physical implementation inside the measured entropy-source boundary.

## Contribution Bullets For A TIM Draft

1. A placement-sensitive measurement study of FPGA RO-TRNG output quality, showing repeatable quality differences across placement variants in the recorded hardware setup.
2. A restart and warmup characterization showing that continuous-stream entropy estimates do not by themselves capture fixed-position startup bias.
3. A TDC-assisted diagnostic layer that constrains the mechanism by showing no evidence of simple persistent pairwise hard locking under the measured clean/reset-aligned TDC conditions.
4. A sampler-side counterfactual study in which sample-RO physical implementation changes can move restart behavior from near ideal to biased failure and back toward near ideal.
5. A boundary argument for FPGA RO-TRNG measurement practice: the entropy-source boundary should include sampler-side RO, routing, and nearby implementation details, not only the nominal data RO array.

## What The Paper Should Not Claim

- It should not claim complete SP800-90B certification.
- It should not claim universal behavior across FPGA families, boards, voltage, temperature, aging, or tool versions.
- It should not claim ps-level calibrated jitter metrology unless the TDC calibration uncertainty is strengthened and documented.
- It should not claim that pairwise RO hard locking never occurs; the present TDC evidence argues against it as the dominant explanation in the measured cases.
- It should not claim the sample RO is the only sampler-side contributor; registers, local routing, readout/control logic, and physical neighborhood remain part of the boundary.

## Abstract-Level Claim Boundary

Safe abstract-level wording:

```text
Measurements on the recorded FPGA setup indicate that sampler-side physical implementation can reshape restart behavior and should be included in the measured entropy-source boundary of FPGA RO-TRNGs.
```

Unsafe abstract-level wording:

```text
We certify an FPGA RO-TRNG entropy source under SP800-90B and prove that sampler placement universally determines RO-TRNG security.
```

## Future Rewrite Paths

TCAS-II rewrite: compress the paper around a sharp circuits-and-systems message, such as sampler-side counterfactual placement as a compact physical mechanism result. This would need a shorter narrative and stronger mechanistic clarity.

TVLSI rewrite: expand implementation evidence, including multi-board/PVT results, placement-aware design rules, resource/timing/power tables, routed-design constraints, and validation that the rules predict or prevent failure modes.

JCEN rewrite: expand the cryptographic-engineering argument, including entropy-source modeling, health-test and conditioning boundaries, a formal SP800-90B evidence package, and a clearer security interpretation of restart and sampler-vector effects.
