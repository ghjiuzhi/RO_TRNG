# 机制验证阶段进展总结 2026-05-25

## 当前主线

现在最强、最适合写进论文的机制主张是：

> RO-TRNG 的 placement 敏感性不能只解释为 RO-RO 简单硬锁定。采样端物理实现本身，尤其 sample RO、采样寄存器、局部路由和采样孔径，是熵源边界的一部分。

这轮工作的关键价值是：把 TDC 从“可能有用但对齐不严谨的 raw packet 数据”推进到了“带 `TDCR` header 的 clean reset-aligned 六点矩阵”，同时把 sample RO 双向反事实结果和 TDC 结果合成了机制证据链表。

## 本轮完成的硬件实验

完成了 reset-aligned / warmup-aligned TDC clean32k 六点矩阵：

| placement | warmup | bytes | header | XADC after | status |
| --- | ---: | ---: | --- | --- | --- |
| random1 baseline | 0 | 262160 | TDCR OK | 47.0 C, VCCINT 1.000 V | complete |
| random1 baseline | 12 | 262160 | TDCR OK | 47.1 C, VCCINT 1.000 V | complete |
| random3 good reference | 0 | 262160 | TDCR OK | 47.4 C, VCCINT 1.000 V | complete |
| random3 good reference | 12 | 262160 | TDCR OK | 47.1 C, VCCINT 1.000 V | complete |
| random1 sampler-local | 0 | 262160 | TDCR OK | 47.2 C, VCCINT 1.000 V | complete |
| random1 sampler-local | 12 | 262160 | TDCR OK | 46.8 C, VCCINT 1.000 V | complete |

六个文件全部是 `16-byte TDCR header + 32768 x 8-byte TDC packet`，不再是之前那种中途截到的 `A5` packet stream。

## 这轮 TDC 证明了什么

TDC 的最稳结论是排除性/约束性证据：

- six-point clean TDC 里 same-diff transition ratio 约 1%。
- longest same-differential-bin run 都是 3。
- small-lag autocorrelation 接近 0。
- 因此不能把 bad placement 简单写成 RO-RO hard locking。

同时有一个弱正证据：

- `random1_sampler_local_warmup12` 的 `H(diff)=6.73356`，`transition H(diff)=13.0993`，在 clean 六点矩阵里最高。
- 这和“sampler-local placement 改善启动相位扩散/采样孔径”相容。
- 但这个 TDC 差异远小于 restart/TRNG 输出差异，所以不能单靠 TDC 宣称已经证明 startup diffusion 是唯一根因。

论文里更稳的写法是：

> TDC evidence rules out simple pairwise hard locking and weakly supports sampler-side diffusion differences. The dominant causal evidence comes from sampler-side counterfactual placement, especially the bidirectional sample-RO experiment.

## 最强证据仍然是什么

最强证据是 sample RO 双向反事实闭环：

| experiment | result | interpretation |
| --- | --- | --- |
| compact top + formal-routed sample RO | warmup4/5 从 near-ideal 被拉成强低偏失败 | 只移动 sample RO 可破坏 restart passband |
| formal top + compact-routed sample RO | warmup4 从失败修复到 near-ideal | 只移动 sample RO 可修复 restart passband |

这比 TDC 更接近因果证据，因为它不是相关性，而是“只改 sampler-side 物理实现就翻转输出结果”。

## 新增/更新的关键文件

构建和采集：

```text
scripts/build_tdc_reset_aligned_bitstreams.ps1
scripts/program_and_capture_uart_preopen.ps1
scripts/run_tdc_reset_aligned_preopen_queue_20260525.ps1
data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_clean32k_20260525.csv
data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_clean32k_remaining_20260525.csv
```

clean TDC 分析：

```text
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.summary.csv
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.summary.md
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.windows.csv
```

机制证据链：

```text
scripts/make_mechanism_evidence_chain_20260525.py
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.csv
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md
```

状态文档：

```text
doc/tdc_reset_aligned_clean32k_status_20260525.md
doc/mechanism_progress_summary_20260525_cn.md
```

## 下一步最值得做的事

优先级 1：多板复现 sample RO 双向反事实。

目的不是堆数据，而是回答审稿人最可能问的问题：这个 sample RO 反事实是不是单板偶然、单个温度点偶然、单次布局偶然。

最小矩阵：

```text
board A / board B / board C
compact top + formal sample RO warmup5
formal top + compact sample RO warmup4
每个至少 1 次，最好 2 次
```

优先级 2：做 TDC code-density calibration。

目的：现在 TDC 只能做 raw-bin 相对比较，不能声称 ps 级 jitter / phase drift。校准后才能把 bin 宽、非线性和实际 timing spread 说得更硬。

优先级 3：做 command-gated restart/TDC 架构。

目的：彻底避免 auto-stream 在 XADC/JTAG 操作期间提前输出的问题。现在 after-only XADC 已经可用，但如果要 before/after 都严谨，最好让 FPGA 等待 PC 命令后再开始 stream。

优先级 4：更多 placement 的 restart repeat。

目的：把 placement matrix 从现象展示变成统计比较，尤其 compact/checker/sparse/same_column/random1/random3 的 repeat 和多板复现。

## 论文写法建议

当前已经足够写一篇有机制亮点的会议/期刊初稿；冲高水平还需要多板复现和 calibration。

不要把论文写成：

```text
bad placement causes RO hard locking
```

更稳、更有新意的写法是：

```text
RO-TRNG placement sensitivity is dominated by sampler-side physical realization.
Pairwise TDC measurements do not show hard locking, while sample-RO and sampler-path counterfactual placements flip entropy outcomes. Therefore, the sampler path must be treated as part of the entropy-source boundary rather than a passive readout circuit.
```
