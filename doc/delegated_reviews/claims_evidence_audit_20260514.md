# Claims Evidence Audit 2026-05-14

## Executive Summary

当前证据链足以支撑“placement 显著影响同一 RO-TRNG 结构的原始随机性，并且 TDC/RO_FREQ 能作为机制诊断工具”。但还不能支撑“完整 SP800-90B 认证”“近距离 RO 必然强锁定”“结果可外推到多板/PVT”的强主张。

## Inputs Read

- `doc/fast_mode_master_status_20260514.md`
- `doc/sp800_90b_restart_execution_status_20260514.md`
- `doc/sp800_90b_design_reset_feasibility_20260514.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`
- `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`
- `data/experiments/paper_artifacts_20260514/table_ro_freq_pulling_summary.md`
- `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`

## Findings

1. Placement-quality gap is strongly supported.

   Evidence: `random1` formal p1 is `0.337316`, abs bias `0.162684`, bit min-entropy `0.593606`; `random3` formal p1 is `0.499969`, abs bias `0.0000314`, bit min-entropy `0.999909`. Repeats preserve the same qualitative gap.

2. Repeatability is supported for the current board and nominal lab condition.

   Evidence: formal/repeat deltas are small for the placements with paired data. But this is not multi-board or PVT repeatability.

3. RO_FREQ pulling is supported as a mechanism diagnostic, not as sole causality proof.

   Evidence: all-on vs single-on shifts show data RO shifts around hundreds of ppm and sample RO shift up to `3466.91 ppm` for `random1`.

4. Strong pair-level phase locking is not supported.

   Evidence: six pair-specific TDC captures, 96 windows, `strong_lock_windows=0`, max small-lag abs correlation `0.0317827`. This is a negative result for strong locking under current conditions.

5. SP800-90B evidence is partial.

   Sequential non-IID smoke/core/repeat estimates are useful. `ea_restart.exe` builds and restart capture scripts now exist. Real 2x16 and 10x1000 restart pilots ran successfully, but formal 1000x1000 restart dataset is not complete.

## Recommended Actions

- P0: In the paper, phrase the main claim as placement-sensitive entropy-source behavior, not a complete certified TRNG.
- P0: Add a “claim boundary” paragraph explicitly separating fast statistics, 90B non-IID estimates, restart pilot, and full SP800-90B validation.
- P1: Implement restart-capable RTL or schedule a multi-day reprogram-based formal restart run.
- P1: Add one summary table with `random1`, `random3`, and original baseline across fast bit min-entropy, 90B non-IID H, RO_FREQ, and TDC pair conclusion.
- P2: Add PVT/multi-board results only if time allows; otherwise label them future validation.

## Snippets For Paper

```text
The evidence supports a placement-sensitive entropy-source effect rather than a claim of universal FPGA TRNG robustness. We therefore report fast statistical metrics, SP800-90B non-IID estimates, RO-frequency diagnostics, and TDC pair measurements as complementary evidence, while explicitly separating these results from full SP800-90B certification.
```

```text
Pair-specific TDC measurements did not reveal strong phase locking in the six monitored pairs. This negative result suggests that the observed entropy degradation is not explained by a single persistent pair-level lock in the measured configurations, but it does not rule out weaker, transient, multi-oscillator, or PVT-dependent coupling mechanisms.
```

## Open Questions

- Can a reset-capable RTL variant be built quickly enough to collect formal 1000x1000 restart data?
- Should the final paper include `random1` as a deliberately bad placement case, or treat it as an empirical placement outlier?
- What venue target determines whether multi-board/PVT is mandatory or a limitation?
