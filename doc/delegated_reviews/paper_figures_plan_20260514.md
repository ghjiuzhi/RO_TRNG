# Paper Figures Plan 2026-05-14

## Executive Summary

论文图表应围绕一条主线组织：placement 改变原始随机性，RO_FREQ/TDC 解释这种改变不是单纯黑盒统计现象，SP800-90B 结果给安全评估边界。不要堆所有实验图，优先给审稿人一眼看懂的证据链。

## Core Figures

1. Placement matrix schematic.

   Show compact、checker、sparse、far、same column、cross region、random seeds on the same FPGA fabric sketch. Purpose: explain experimental control variable.

2. TRNG quality by placement.

   Use bar/point plot of bit min-entropy or abs bias from `table_placement_trng_repeats`. Highlight `random1` and `random3`; include formal/repeat markers.

3. SP800-90B non-IID comparison.

   Table or compact bar chart: `random1`, `random3`, `original_fpga1`, plus selected placements. Label as non-IID estimate/smoke unless formal language is justified.

4. RO_FREQ pulling summary.

   Plot all-on vs single-on ppm shift for `random1` and `random3`, using `table_ro_freq_pulling_summary`. Purpose: show physical diagnostic signal.

5. TDC pair dynamics summary.

   Use existing `fig_tdc_pair_best_lag_abs_r.svg` and/or table of max small-lag abs r. Purpose: show no strong pair-level lock was detected.

6. Claim boundary / evidence map.

   A small flow diagram: placement -> RO frequency/phase diagnostics -> raw statistics -> 90B non-IID/restart status. Purpose: prevent overclaiming.

## Required Tables

- Placement/TRNG metrics table: p1, abs bias, bit min-entropy, byte min-entropy.
- 90B table: H_original for random1/random3/original and repeats.
- TDC pair table: windows, packets, max small-lag abs r, strong-lock windows.
- Restart status table: 2x16 smoke, 10x1000 pilot, formal 1000x1000 not complete or future/ongoing.

## Recommended Actions

- P0: Add `random1` vs `random3` headline figure, because it is the cleanest story.
- P0: Put “strong-lock windows = 0” in a figure caption or table note, not buried in prose.
- P1: Add a reset/restart protocol figure if design-level restart is implemented.
- P1: If formal restart is not complete, include restart only in limitations/status, not main result claims.
- P2: Add appendix plots for all placements to avoid cherry-picking criticism.

## Caption Snippets

```text
Raw TRNG quality varies strongly with placement despite the same entropy-source RTL and acquisition chain. `random1` shows persistent bias across repeat captures, whereas `random3` remains close to balanced.
```

```text
Pair-specific TDC measurements did not detect strong phase locking in the monitored RO pairs. The result narrows the mechanism hypothesis toward weaker or multi-oscillator placement-dependent interactions.
```

## Open Questions

- Should figures use Chinese labels for thesis-style drafting or English labels for journal submission?
- Should restart pilot appear in the main paper or appendix unless formal 1000x1000 is completed?
