# RO_TRNG Entropy Boundary Evidence Map

This paper workspace belongs only to the RO_TRNG project at the current repository root. Do not use this directory as a template source for other projects.

## Project Scope

- Repository: RO_TRNG placement/TDC mechanism study.
- Manuscript workspace: `paper/RO_TRNG_entropy_boundary/`.
- Evidence rule: manuscript claims must be traceable to files in this repository.
- Venue rule: current RO_TRNG submission planning lives in `venue/`; reusable venue profiles belong to the future global `ieee-paper-writer` skill.

## Primary Entry Points

| Source | Role in the paper |
| --- | --- |
| `README.md` | Current research position, repository layout, key findings, caveats. |
| `doc/paper_claim_evidence_boundary_20260525.md` | Claim boundaries and limitations for paper-level statements. |
| `doc/paper_draft_cn_v3_20260525.md` | Existing Chinese draft material to mine cautiously. |
| `doc/sp800_90b_restart_execution_status_20260514.md` | SP800-90B restart-test status and interpretation. |
| `data/sp800_90b/results_full8m_20260514/summary.md` | Formal-size SP800-90B result summary. |
| `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md` | Existing claim/evidence table. |
| `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md` | Placement repeat table. |
| `data/experiments/paper_artifacts_20260514/table_ro_freq_pulling_summary.md` | RO frequency/pulling summary. |
| `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md` | TDC pair dynamics summary. |
| `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md` | Restart warmup transition table. |
| `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md` | Mechanism evidence chain. |
| `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_paper_summary.md` | Reduced-XOR counterfactual evidence summary. |

## Local Boundaries To Preserve

- Current evidence is measured on the recorded Zynq-7020 board and associated captured datasets.
- Treat SP800-90B results as formal-size entropy-assessment evidence, not complete certification.
- Keep multi-board, PVT, long-term aging, and certification claims out unless new local evidence is added.
- Do not import claims from external papers without citation and explicit comparison context.

## Next Writing Pass

1. Populate `evidence/claim_evidence_table.md` from the primary entry points.
2. Fill `evidence/evidence_gap.md` before making abstract-level claims.
3. Build figures/tables from existing paper artifacts where possible.
4. Use `venue/target_venue.md` to select the active framing before drafting venue-specific text.
