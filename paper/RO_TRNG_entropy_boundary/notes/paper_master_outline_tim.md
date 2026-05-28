# IEEE TIM Master Outline

This is an outline and evidence plan, not manuscript body text. Do not turn these bullets into full prose until the user asks for drafting.

## 1. Introduction

- **Core task:** Define the measurement problem: FPGA RO-TRNG quality depends on physical implementation, and continuous-stream tests alone can miss restart/early-sampling behavior.
- **Allowed evidence:** High-level pointers to placement sensitivity, restart warmup behavior, TDC diagnosis, and sampler-side counterfactuals from `README.md` and TIM evidence tables.
- **Forbidden overclaims:** No SP800-90B certification; no universal FPGA claim; no final security proof; no ps-level jitter claim.
- **Figure/table plan:** None required in this section; optionally preview Figure 1 boundary diagram after it exists.

## 2. Background And Measurement Gap

- **Core task:** Explain RO-TRNG measurement, placement sensitivity, restart tests, TDC diagnosis, and why sampler-side implementation is usually treated too narrowly.
- **Allowed evidence:** Verified related work from future `related_work_matrix.md`; local evidence only as motivation.
- **Forbidden overclaims:** Do not criticize prior work without direct citation; do not claim all prior RO-TRNG evaluations ignore sampler-side implementation.
- **Figure/table plan:** Related-work comparison table after citations are verified.

## 3. Device, RTL, And Measurement Workflow

- **Core task:** Describe the recorded board/setup, RTL variants, placement variants, UART capture flow, SP800-90B input preparation, TDC captures, and offline analysis scripts.
- **Allowed evidence:** `README.md`, `scripts/`, `rtl/`, `data/experiments/`, `data/hardware/20260511_fpga1_board1/`, `sim/SP800-90B_EntropyAssessment/`.
- **Forbidden overclaims:** Do not present excluded raw captures as included artifacts; do not imply all scripts are hardware-free; do not claim certification workflow.
- **Figure/table plan:** Measurement workflow diagram; table of datasets and scripts if space permits.

## 4. Placement-Sensitive Continuous-Stream Characterization

- **Core task:** Establish measured placement sensitivity and repeatability boundary.
- **Allowed evidence:** `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`, `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`.
- **Forbidden overclaims:** No cross-board/PVT generalization; no claim that continuous-stream quality is sufficient.
- **Figure/table plan:** Table 1: placement quality spectrum.

## 5. Restart And Warmup Characterization

- **Core task:** Show that restart behavior reveals fixed-position startup bias and warmup-dependent pass/fail behavior.
- **Allowed evidence:** `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`, `data/sp800_90b/results_full8m_20260514/summary.md`, `doc/sp800_90b_restart_execution_status_20260514.md`.
- **Forbidden overclaims:** No complete SP800-90B certification; no universal warmup threshold; no claim that passing one warmup means robust entropy source.
- **Figure/table plan:** Figure/Table 2: restart warmup transition.

## 6. TDC-Assisted Diagnosis

- **Core task:** Use TDC measurements to constrain mechanism hypotheses and argue against simple persistent pairwise hard-locking-only explanations under measured conditions.
- **Allowed evidence:** `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`, `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`, `doc/tdc_code_density_calibration_status_20260525.md`.
- **Forbidden overclaims:** No absolute ps-level jitter metrology; no claim that pairwise hard locking never occurs; no sole-cause proof.
- **Figure/table plan:** Table 3: TDC pair dynamics; Figure/Table 4: clean reset-aligned TDC matrix; Table 5: TDC calibration boundary.

## 7. Sampler-Side Counterfactuals

- **Core task:** Present the strongest causal evidence that sampler-side physical implementation changes restart outcomes.
- **Allowed evidence:** `doc/sample_ro_locked_passband_results_20260525.md`, `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`.
- **Forbidden overclaims:** Do not claim the sample RO is the only contributor; do not generalize beyond tested designs and board.
- **Figure/table plan:** Figure/Table 6: sample-RO bidirectional counterfactual.

## 8. Reduced-XOR Mechanism Evidence

- **Core task:** Show that final output quality can depend on XOR cancellation among biased sampler-vector directions.
- **Allowed evidence:** `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md`, `reduced_xor_w10_direction_paper.md`, `reduced_xor_w10_repeat_paper.md`.
- **Forbidden overclaims:** No universal XOR cancellation model; no claim that one data-RO direction fully determines final quality.
- **Figure/table plan:** Figure/Table 7: reduced-XOR direction and complement evidence.

## 9. Entropy-Source Boundary Discussion

- **Core task:** Synthesize placement, restart, TDC, sampler-side, and reduced-XOR evidence into the bounded boundary claim.
- **Allowed evidence:** `tim_claim_evidence_table.md`, `tim_paper_positioning.md`, `mechanism_evidence_chain_20260525.md`.
- **Forbidden overclaims:** No certification; no cross-device rule; no final placement-aware design rule.
- **Figure/table plan:** Figure 8: entropy-source boundary diagram.

## 10. Limitations And Submission-Readiness Boundaries

- **Core task:** State the limits that protect the paper from overclaiming.
- **Allowed evidence:** `tim_evidence_gap.md`, `experiment_priority_plan.md`, `evidence_gap.md`.
- **Forbidden overclaims:** Do not bury single-board, PVT, certification, and related-work gaps.
- **Figure/table plan:** Optional compact limitations table.

## 11. Conclusion

- **Core task:** Restate only evidence-backed measurement contributions after all figures/tables are finalized.
- **Allowed evidence:** Final `tim_claim_evidence_table.md`.
- **Forbidden overclaims:** No new claims; no complete SP800-90B certification; no universal security statement.
- **Figure/table plan:** None.

## Recommended Figure/Table Order

| Order | Item | Section |
| --- | --- | --- |
| 1 | Placement quality spectrum | Section 4 |
| 2 | Restart warmup transition | Section 5 |
| 3 | TDC pair dynamics summary | Section 6 |
| 4 | Clean reset-aligned TDC diagnostic matrix | Section 6 |
| 5 | TDC code-density calibration boundary | Section 6 |
| 6 | Sample-RO bidirectional counterfactual | Section 7 |
| 7 | Reduced-XOR direction and complement evidence | Section 8 |
| 8 | Entropy-source boundary diagram | Section 9 |
