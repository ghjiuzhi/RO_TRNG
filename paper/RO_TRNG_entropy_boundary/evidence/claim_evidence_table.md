# Claim Evidence Table

| Claim | Evidence files | Status | Limits | Manuscript location |
| --- | --- | --- | --- | --- |
| FPGA RO-TRNG quality is strongly placement-sensitive in the measured setup. | `README.md`; `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`; `data/hardware/20260511_fpga1_board1/trng/` summaries | Partial draft | Single recorded board/setup unless more evidence is added. | Results |
| The sampler-side implementation should be treated as part of the entropy-source boundary. | `README.md`; `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`; `data/experiments/sample_ro_balanced_repeats_20260528/sample_ro_balanced_repeats_20260528.md`; `data/experiments/sample_ro_directive_variance_20260528/sample_ro_directive_variance_20260528.csv`; `paper/RO_TRNG_entropy_boundary/evidence/directive_variance_result_20260528.md`; `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md` | Supported for current setup | Current sampler/reduced-XOR experiments only; directive-controlled evidence strengthens implementation sensitivity but does not prove sample-RO-only causality. | Discussion |
| Simple pairwise RO hard locking alone does not explain the observed failures under measured conditions. | `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`; `doc/tdc_pair_dynamics_interpretation_20260514.md`; `README.md` | Partial draft | Does not rule out all coupling or all locking regimes. | Results/Discussion |
| Restart tests reveal fixed-position startup bias not visible from continuous-stream balance alone. | `doc/sp800_90b_restart_execution_status_20260514.md`; `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`; `data/sp800_90b/results_full8m_20260514/summary.md` | Partial draft | Formal-size assessment evidence, not full certification. | Results |

## Use Rules

- Upgrade a claim to `established` only after checking the cited files directly.
- Mark claims as `missing` if the manuscript needs a stronger statement than the local evidence supports.
- Add exact metric values only after verifying the source file and units.
- Use `venue/target_venue.md` and local venue plans to adjust framing, emphasis, and compression; do not change the evidence boundary or strengthen claims for a venue.
