# IEEE TIM Submission-Readiness Audit

## Verdict

The project is suitable to write a first IEEE TIM-oriented draft now, provided the draft is framed as measurement-driven characterization and TDC-assisted diagnosis, not as certification or a general FPGA design rule. The current evidence is strong enough for a bounded single-project measurement paper about RO-TRNG placement sensitivity and sampler-side entropy-boundary effects on the recorded Zynq-7020 setup.

It is not yet ready for a final high-confidence TIM submission without additional packaging work: figure/table regeneration commands must be verified, related work and citations must be finalized, and the limitations around single-board evidence, PVT, restart interpretation, and TDC calibration must be made explicit.

## Strongest Contributions

1. **Sampler-side entropy-boundary evidence.** Bidirectional sample-RO counterfactuals show that moving only sampler-side physical implementation can pull a near-ideal restart passband into failure and repair a failing case back toward near ideal. Evidence: `doc/sample_ro_locked_passband_results_20260525.md`, `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`.
2. **Restart-aware measurement characterization.** Formal-size restart and warmup evidence shows that continuous-stream quality does not capture fixed-position startup bias. Evidence: `README.md`, `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`, `data/sp800_90b/results_full8m_20260514/summary.md`.
3. **TDC-assisted mechanism constraint.** Pairwise and clean/reset-aligned TDC evidence argues against a simple persistent pairwise hard-locking-only explanation under measured conditions. Evidence: `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`, `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`, `doc/tdc_code_density_calibration_status_20260525.md`.

## Most Dangerous Overclaims

1. **Complete SP800-90B certification.** The project has formal-size entropy-assessment and restart sanity-check evidence, but not a complete certification package with final module boundary, conditioning, health tests, and validation documentation.
2. **Universal FPGA/PVT behavior.** Current evidence is bounded to the recorded board, designs, placements, toolflow, and available runs. It does not support claims across FPGA families, boards, voltage, temperature, aging, or tool versions.
3. **Absolute TDC/jitter metrology.** TDC evidence is useful as diagnostic and relative mechanism evidence, but raw TDC bins should not be treated as calibrated ps-level jitter measurements without a stronger calibration and uncertainty package.

## Claims With Sufficient Evidence For A First TIM Draft

| Claim | Evidence | Allowed wording |
| --- | --- | --- |
| Placement changes RO-TRNG output quality in the recorded setup. | `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`; `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`; `README.md` | `measured placement-sensitive output quality on the recorded Zynq-7020 setup` |
| Continuous-stream quality alone does not characterize restart behavior. | `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`; `README.md`; `data/sp800_90b/results_full8m_20260514/summary.md` | `restart tests reveal fixed-position startup bias not visible from continuous-stream balance alone` |
| Simple persistent pairwise hard locking is not supported as the dominant measured mechanism. | `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`; `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md` | `TDC diagnostics do not support a simple pairwise hard-locking-only explanation under measured conditions` |
| Sampler-side physical implementation belongs in the measured entropy-source boundary. | `doc/sample_ro_locked_passband_results_20260525.md`; `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`; `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md` | `supports treating sampler-side physical implementation as part of the entropy-source boundary` |
| Reduced-XOR counterfactuals show structured sampler-vector effects. | `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md` | `final quality can depend on XOR cancellation among biased hardware directions` |

## Claims That Must Stay Observation, Indication, Or Hypothesis

| Claim area | Current status | Required phrasing |
| --- | --- | --- |
| Mechanism causality beyond sample-RO counterfactuals | Strong evidence for sample-RO physical implementation, but not exhaustive causality for every nearby route/control element. | Observation/indication: `consistent with sampler-side physical implementation shaping restart behavior`. |
| Restart warmup passband threshold | Warmup transition is observed for a specific board, placement, and auto-stream protocol. | Observation: `under this protocol, warmup11/12/16 pass while warmup8/10 fail`. |
| TDC diffusion explanation | TDC constrains hard-locking hypotheses and gives weak positive evidence in some matrices. | Indication: `TDC evidence constrains mechanism hypotheses`; avoid `proves startup diffusion mechanism`. |
| Placement-aware design rule | Current evidence identifies sensitive placement effects, but no predictive rule has been validated. | Hypothesis/future work: `a placement-aware rule may be possible after held-out validation`. |
| Security certification interpretation | Entropy-assessment evidence exists, but security boundary and conditioning package are incomplete. | Observation: `formal-size entropy-assessment evidence`; avoid compliance wording. |

## Claims Not Ready For The Paper

- Complete SP800-90B certification or compliance.
- Cross-board or cross-FPGA-family generalization.
- Robust PVT behavior.
- A validated placement-aware design rule.
- Absolute ps-level jitter or phase-noise metrology from current TDC data.
- A claim that pairwise RO hard locking never occurs.
- A claim that the sample RO is the only sampler-side contributor.
- Comparisons against all prior RO-TRNG designs unless `refs/references.bib` and related-work evidence are finalized.

## Risk Audit

| Risk area | Current risk | Mitigation |
| --- | --- | --- |
| SP800-90B | High if framed as certification. | Use `entropy-assessment`, `restart sanity-check`, and `formal-size evidence`; state incomplete certification package. |
| Restart | Medium. Strong results exist, but protocol and warmup dependence must be described carefully. | Put protocol, matrix size, warmup, and board/setup in captions and limitations. |
| Multi-board | High for generalization. | State single recorded board/setup; treat multi-board as strongly recommended before broader claims. |
| PVT | High for robustness claims. | Use after-only XADC metadata only as run context; do not claim systematic PVT coverage. |
| TDC interpretation | Medium. Good diagnostic evidence, but calibration limits remain. | Use TDC as relative/diagnostic evidence and cite code-density calibration boundary. |
| Reproducibility | Medium. Many artifacts exist, but generation commands need final verification. | Verify scripts and regenerate final tables/figures before submission. |
| Related work | Medium-high. Positioning is planned but final citations are not yet verified. | Complete related-work matrix and BibTeX before writing final related work. |

## Submission Readiness Checklist

| Item | Status | Before first draft | Before submission |
| --- | --- | --- | --- |
| TIM framing | Ready | Use measurement-driven characterization and diagnosis. | Re-check against final figures. |
| Core claim boundary | Ready with limits | Keep all claims scoped to recorded setup. | Confirm no abstract/conclusion overclaim. |
| Figures/tables | Partially ready | Select candidate tables and figures. | Regenerate and verify commands/source files. |
| SP800-90B wording | Ready with caution | Avoid certification language. | Add final limitation paragraph. |
| Multi-board/PVT | Not ready for broad claims | Keep as limitation. | Add experiments or avoid generalization. |
| TDC explanation | Ready as diagnostic evidence | Avoid ps-level metrology. | Include calibration boundary. |
| Related work | Not ready | Build comparison matrix. | Verify citations and claims. |
