# TIM Figure And Table Plan

| Item | TIM message | Source files | Generation command | Status |
| --- | --- | --- | --- | --- |
| Table 1: Placement quality spectrum | Placement materially changes output quality in the recorded FPGA setup. | `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`; `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md` | Verify from artifact-generation scripts before final manuscript. | Candidate |
| Figure/Table 2: Restart warmup transition | Restart behavior exposes fixed-position startup bias and a warmup transition not captured by continuous-stream balance alone. | `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`; `data/experiments/paper_artifacts_20260515/fig_restart_warmup_transition.svg` | Verify source command and regenerate if needed. | Candidate |
| Table 3: TDC pair dynamics summary | Pairwise TDC evidence does not support simple persistent pairwise RO hard locking as the dominant mechanism. | `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`; `doc/tdc_pair_dynamics_interpretation_20260514.md` | Verify analysis command from `scripts/analyze_tdc_pair_dynamics.py`. | Candidate |
| Table 3b: exact counterfactual TDC check | Exact `Scompact`/`Srestart` sample-RO TDC captures against the same data_ro0 show no strong pairwise hard-lock windows. | `paper/RO_TRNG_entropy_boundary/evidence/exact_tdc_counterfactual_result_20260528.md`; `data/experiments/tdc_counterfactual_20260528/` | Commands recorded in `exact_tdc_counterfactual_result_20260528.md`. | New candidate; likely text-only for TIM |
| Figure/Table 4: Clean reset-aligned TDC diagnostic matrix | Clean/reset-aligned TDC constrains the mechanism and supports a diagnostic rather than hard-locking-only interpretation. | `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`; `data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.summary.csv` | Verify analysis command from clean32k TDC scripts. | Candidate |
| Table 5: TDC code-density calibration boundary | Raw TDC bins are nonlinear; TDC evidence should be used with calibrated or relative interpretation. | `doc/tdc_code_density_calibration_status_20260525.md`; `data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_compare_20260525.md` | Verify `scripts/analyze_tdc_code_density_calibration_20260525.py`. | Candidate |
| Figure/Table 6: Sample-RO bidirectional counterfactual | Moving the sample-RO implementation can pull a near-ideal passband into failure and repair a formal failure back toward near ideal; compact-baseline w4, forward-fail w4/w5, and reverse warmup-4 cases now have three-run support. | `doc/sample_ro_locked_passband_results_20260525.md`; `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`; `data/experiments/sample_ro_balanced_repeats_20260528/sample_ro_balanced_repeats_20260528.md` | `python scripts/make_balanced_counterfactual_repeat_table_20260528.py` for aggregate repeat table; verify exact manuscript capture labels before final. | High-priority candidate |
| Figure/Table 6b: Directive-controlled route-variance check | Under independent implementation directives, W4 compact remains near balanced while the sampler-side forward lock remains biased; this supports the counterfactual beyond one default implementation. | `paper/RO_TRNG_entropy_boundary/evidence/directive_variance_result_20260528.md`; `data/experiments/sample_ro_directive_variance_20260528/sample_ro_directive_variance_20260528.csv`; `data/experiments/sample_ro_directive_variance_route_diff_20260528/sample_ro_route_evidence_summary_20260528.md` | Captures and analysis commands are recorded in `directive_variance_result_20260528.md`. | New candidate; likely best as a short text note or one routed-audit table row |
| Figure/Table 7: Reduced-XOR direction and complement evidence | Final output quality can reflect same-data-RO direction anisotropy and warmup-dependent complement cancellation. | `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md`; `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_direction_paper.md`; `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_repeat_paper.md`; `data/experiments/restart_reduced_xor_vector_anisotropy_20260528/reduced_xor_vector_anisotropy_20260528.md`; `data/experiments/restart_reduced_xor_ro3_warmup_neighbors_20260528/reduced_xor_ro3_warmup_neighbors_20260528.md` | `python scripts/make_reduced_xor_paper_artifacts_20260527.py`; `python scripts/make_reduced_xor_vector_anisotropy_20260528.py`; `python scripts/make_reduced_xor_ro3_warmup_summary_20260528.py`. | Candidate |
| Figure 8: Entropy-source boundary diagram | The measured entropy-source boundary includes data ROs, sampled-data registers, sample RO, sampler routing, and restart/warmup/reset timing directly affecting sampling; post-XOR FIFO, UART, host capture, and offline analysis remain measurement/readout elements. | Derived from `notes/tim_paper_positioning.md`, `evidence/tim_claim_evidence_table.md`, and RTL paths under `rtl/`. | Create only after manuscript outline stabilizes. | Planned |

## Caption Rules

- State board/setup, placement, warmup, capture size, and protocol where relevant.
- Do not imply SP800-90B certification from formal-size entropy-assessment evidence.
- Describe TDC plots as diagnostic or relative unless calibration supports stronger timing claims.
- Keep sampler-side counterfactual captions explicit about what changed and what did not change.

## Venue-Specific Reuse

For TIM, prioritize Tables/Figures 1, 2, 4, 6, and 7 as measurement and diagnosis evidence.

For IEEE Access fallback, keep more implementation and reproducibility tables.

For TCAS-II, compress to the boundary diagram, one counterfactual table, and one diagnostic TDC result.

For TVLSI, add resource/timing/power, placement-rule validation, and multi-board/PVT tables.

For JCEN, add SP800-90B boundary, health-test, conditioning, and security-interpretation tables.
