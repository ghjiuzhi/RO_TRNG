# Experiment Priority Plan

This plan prioritizes evidence needed for an IEEE TIM submission of the RO_TRNG entropy-boundary paper. It does not define new claims; it maps evidence gaps to submission risk.

## Must-Have Before Submission

| Priority | Experiment/task | Why it is required | Evidence target |
| --- | --- | --- | --- |
| P0 | Verify final figure/table generation commands. | TIM requires traceable measurement evidence; current figure plan still marks several commands as `verify`. | Re-run or document scripts for placement table, restart warmup table, TDC summaries, sample-RO counterfactual summaries, and reduced-XOR artifacts. |
| P0 | Final claim-evidence audit for abstract/conclusion-level claims. | Prevents overclaiming SP800-90B, PVT, multi-board, and TDC interpretation. | Update `tim_claim_evidence_table.md` before drafting final abstract/conclusion. |
| P0 | Confirm restart protocol wording and matrix dimensions for every restart figure/table. | Restart results are central and easy to overstate. | Captions must state board/setup, warmup bytes, matrix size, bit-symbol expansion, and whether result is sanity-check evidence. |
| P0 | Complete related-work and comparison table. | TIM reviewers will ask what measurement gap this paper fills relative to existing RO-TRNG work. | Fill `related_work_matrix.md` and `refs/references.bib` with verified citations. |
| P0 | Decide whether TIM submission waits for balanced counterfactual repeats. | Completed for the highest-risk current setup: compact baseline w4, forward fail w4/w5, and reverse repair w4 now have three rows each; compact baseline w5/w11 and forward fail w11 have two rows each. | Use `data/experiments/sample_ro_balanced_repeats_20260528/`; keep limitations for reverse-only-w4, two-run w11 evidence, and forward-w4 old-bit provenance. |

## Strongly Recommended

| Priority | Experiment/task | Why it matters | Evidence target |
| --- | --- | --- | --- |
| P1 | Multi-board repeat of the strongest placement/sampler-side counterfactual. | Reduces the largest generalization risk. | At least one additional board showing whether sampler-side counterfactual direction persists or changes. |
| P1 | Additional placement repeats for the TIM core cases. | Strengthens repeatability beyond current available repeats. | Repeat random1/random3, sample-RO forward-fail, reverse-repair, and reduced-XOR key modes where feasible. |
| P1 | Route-locked or directive-controlled route-variance repeat for locked sample-RO variants. | Local route/PIP and net-delay extraction now exists, but it shows route-level residual confounding even when cell placement is localized in the forward comparison. Vivado 2023.2 non-project implementation does not expose a true placement/routing seed in the current flow, so directive-controlled variance is the honest fast control. | Completed W4 `Explore/Explore/Explore` compact and formal-sample hardware captures. Compact remained near balanced (`p1=0.496761`), while formal-sample remained biased (`p1=0.375294`). See `paper/RO_TRNG_entropy_boundary/evidence/directive_variance_result_20260528.md`. Full route-locking remains future work. |
| P1 | Systematic PVT sweep or controlled temperature/voltage subset. | Current XADC metadata is contextual, not systematic robustness evidence. | Small controlled sweep or clearly documented reason PVT remains out of scope. |
| P1 | TDC calibration and uncertainty note. | Supports TIM measurement rigor and avoids ps-level overclaiming. | Short calibration boundary table using code-density calibration artifacts. |
| P1 | Resource/timing/power extraction for final builds. | Helps reviewers understand hardware cost and implementation context even if TVLSI is not the target. | Vivado utilization/timing/power summary for core variants, with caveats. |

## Nice-To-Have

| Priority | Experiment/task | Why it helps | Evidence target |
| --- | --- | --- | --- |
| P2 | More placement variants around sampler-side neighborhoods. | Helps move from observation toward a placement-aware design rule. | Held-out placements showing whether the boundary hypothesis predicts behavior. |
| P2 | Additional TDC matrices around sample-RO counterfactuals. | Links TDC diagnosis more tightly to the strongest sampler-side causal evidence. | TDC before/after sample-RO lock or repair cases. |
| P2 | Complete reduced-XOR repeat coverage. | Current manuscript includes the full warmup-10 run01 8+8 map, but repeat02 covers only a diagnostic subset. | Add repeat rows for all eight `data_ro` and all eight `except_ro` directions, or keep repeat claims limited to the existing subset. |
| P2 | Re-run reduced-XOR under another warmup setting. | Partially addressed by the targeted `data_ro3`/`except_data_ro3` warmup5/11 controls, which show a stable high-biased direction but warmup-dependent complement behavior. | Full all-direction warmup5/warmup11 maps remain future work; current evidence is enough for a bounded mechanism statement. |
| P2 | Clean up reproducibility package. | Helps IEEE Access fallback and TIM artifact confidence. | Script manifest, exact commands, and generated output hashes. |

## Future Work

| Topic | Needed before claiming | Best future venue fit |
| --- | --- | --- |
| Multi-board general FPGA behavior | Multiple boards and possibly multiple FPGA parts. | TIM extension, TVLSI, JCEN |
| PVT robustness | Controlled voltage/temperature sweeps. | TIM, TVLSI |
| Placement-aware design rule | Predictive rule validated on held-out placements and tool runs. | TVLSI, TCAS-II if compact |
| Full SP800-90B/security package | Final entropy-source boundary, health tests, conditioning, documentation, and validation argument. | JCEN |
| Circuit-level compact mechanism | A concise, validated mechanism centered on sampler-side placement and restart behavior. | TCAS-II |

## Evidence Area Assessment

| Area | Current strength | Submission role |
| --- | --- | --- |
| Multi-board experiments | Missing | Do not generalize; strongly recommended if time permits. |
| PVT | Weak/context only | Limitation unless new controlled sweep is added. |
| Multi-placement repeats | Moderate | Usable for first draft; strengthen before submission where possible. |
| SP800-90B restart evidence | Strong as entropy-assessment evidence | Central result, but not certification. |
| TDC measurement evidence | Moderate-strong as diagnostic evidence | Supports mechanism constraints; not absolute jitter metrology. |
| Reduced-XOR counterfactual | Strong for mechanism support, now with orthogonal row/column controls | Use full warmup-10 run01 map; repeat claims only for the existing diagnostic subset plus targeted line6 and ro3 controls. The new line map supports a data-RO-direction anisotropy interpretation rather than a generic sampler-phase line failure. |
| Sampler-side counterfactual | Strongest causal evidence, now backed by three-run compact-baseline, forward-fail, and reverse-repair core repeats | Core contribution for TIM; use the repeat aggregate while keeping reverse repair scoped to warmup4 and longer-warmup repeatability bounded to the available evidence. |
| Resource/timing/power/locality | Moderate-strong for traceability, bounded for causality | Current WNS/LUT/FF/power/routed status plus local route/PIP/net-delay extraction supports a sampler-side/local-routed-context claim. It still does not prove sample-RO-only causality. |
| Existing RO-TRNG comparison | Underdeveloped | Must finish related-work matrix and BibTeX before submission. |
