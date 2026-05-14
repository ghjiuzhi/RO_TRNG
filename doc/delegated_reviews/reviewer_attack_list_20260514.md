# Reviewer Attack List 2026-05-14

## Executive Summary

下面是审稿人最可能攻击的点，以及当前应对策略。最危险的不是“结果不够漂亮”，而是过度声称：把 smoke 当 formal、把 TDC bin 当绝对时间、把单板结果外推成通用规律。

## Findings

| Attack | Risk | Best response |
| --- | --- | --- |
| Single board, nominal voltage, room temperature only | High | 主张限定为 board-local evidence；把 PVT/multi-board列为扩展验证，不做普适性声称。 |
| No full SP800-90B certification | High | 明确区分 non-IID estimates、restart pilot、formal restart、conditioning；当前不写“certified”。 |
| TDC code-density not fully calibrated | Medium | 把 TDC 用作 relative/bin-distribution diagnostic；不把 bin 直接解释为线性绝对时间。 |
| Pair TDC did not show strong locking | Medium | 将机制叙事从“强锁定”改为 placement-dependent dynamic interaction、frequency proximity、weak/transient coupling。 |
| Manual placement is not innovation | Medium | 创新点写成 placement-sensitivity measurement methodology plus cross-layer evidence chain，不把手动 PR 本身当贡献。 |
| 90B restart pilot too small | Medium | 明确 pilot only；给出 formal 1000x1000脚本和实际 reprogram 成本；若能补 design-reset formal，再升级。 |
| Random1 is cherry-picked | Medium | 展示完整 placement matrix，包括 compact/checker/sparse/far/same_column/cross_region/random seeds，不只报 random1/random3。 |
| UART/data path may alter randomness | Medium | 说明同一 UART/FIFO链路下比较不同 placement；绝对熵声明仍需端到端验证。 |
| RO_FREQ/TDC causality weak | Medium | 写为 correlation/mechanism diagnostics；避免单因果归因。 |

## Recommended Actions

- P0: 在摘要和结论中避免“proof/certification/guarantee”。
- P0: 图表里保留坏例、好例和中间例，避免 cherry-picking 印象。
- P0: 把 restart pilot 和 formal restart 缺口写进 limitations。
- P1: 争取补 design-level reset formal restart；这对安全类审稿人很有杀伤力。
- P1: 增加 RTL reset coverage 图或表，说明 reset 覆盖哪些模块。
- P2: 温度/电压如果做不了，不要硬写；可补运行时间漂移作为低成本替代。

## Snippets For Paper

```text
Manual placement is used here as an experimental control knob, not as the claimed contribution. The contribution is the placement-sensitivity evidence chain that links raw TRNG quality, RO-frequency behavior, and TDC-observed phase dynamics under matched acquisition conditions.
```

```text
The current TDC implementation is used for relative distributional and correlation diagnostics. We do not interpret uncalibrated TDC bins as a calibrated linear time axis.
```

## Open Questions

- 目标期刊是否要求完整 SP800-90B restart 和 health-test discussion？
- 是否有第二块同型号板可做一组 minimal replication？
- 是否能把 `por_n_i` 或 PS GPIO 做成可脚本控制的 design-level restart？
