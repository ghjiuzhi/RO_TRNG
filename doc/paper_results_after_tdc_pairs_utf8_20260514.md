# TDC Pair 后论文结果整理 - 2026-05-14

这份文档用于论文写作和组会汇报。它只汇总已经完成的硬件采集、离线分析和 SP800-90B smoke 结果，不额外启动 Vivado、COM3 或 JTAG。

## 一句话结论

当前数据已经能支撑一个明确论文方向：在同一块 Zynq-7020 FPGA、同一类 RO-TRNG 结构和相同采集链路下，placement 会导致原始随机性出现显著且可重复的差异。TDC pair 结果没有检测到强相位锁定，因此机制不能写成“近距离 RO 强锁定导致熵变化”，更稳妥的表述是 placement 改变了多 RO 网络的动态相互作用、频率接近、采样相位覆盖和序列相关结构。

## 已完成证据

| 类别 | 数据 | 论文作用 |
| --- | --- | --- |
| TRNG placement matrix | compact、checker、sparse、far、same_column、cross_region、random1/2/3、row | 证明 placement 改变原始随机性 |
| 原始 fpga1 baseline | `original_fpga1_run01_10mib`、`original_fpga1_repeat02_5mib` | 和原始工程对照 |
| RO_FREQ | random1/random3 多次 repeat | 诊断频率差、beat、sample pulling |
| TDC near/far | near/far baseline repeat | 诊断相位/bin 分布 |
| Pair-specific TDC | 6 个重点 pair，每个 2 MiB | 验证强锁定假设是否成立 |
| SP800-90B smoke | 11 个布局，MSB/LSB bit-symbol non-IID smoke；random1/random3/original IID 诊断 | 作为独立 conservative entropy screening |

## 主要数值结果

TRNG placement：

- `random1` 是稳定坏例：10 MiB formal `p1 = 0.337315512`，快速 bit min-entropy `0.593605945`；5 MiB repeat 仍接近同一水平。
- `random3` 是稳定好例：10 MiB formal `p1 = 0.499968565`，快速 bit min-entropy `0.999909299`；5 MiB repeat 接近理想。
- 原始 `fpga1` baseline 较好：10 MiB `p1 = 0.500035894`，快速 bit min-entropy `0.999896436`。
- `same_column` 是重要反例：p1 接近 0.5，但 runs p-value 为 0，说明只看 bias 不够。

TDC pair dynamics：

| 指标 | 结果 |
| --- | --- |
| pair runs | 6 |
| total windows | 96 |
| strong-lock windows | 0 |
| max small-lag abs correlation | 约 0.0318 |
| mean diff std | 约 2040 ps 到 2043 ps |

SP800-90B non-IID smoke：

| dataset | MSB H_original | LSB H_original |
| --- | ---: | ---: |
| `random1_run01` | 0.385385 | 0.383737 |
| `random3_run01` | 0.869064 | 0.828444 |
| `random2_run01` | 0.863906 | 0.824495 |
| `compact_run01` | 0.872029 | 0.834591 |
| `checker_run01` | 0.863144 | 0.865884 |
| `original_fpga1_run01_10mib` | 0.834723 | 0.821566 |
| `same_column_run01` | 0.834068 | 0.834502 |
| `far_run01` | 0.820724 | 0.847848 |
| `cross_region_run02` | 0.818336 | 0.861193 |
| `row_run01` | 0.783063 | 0.770955 |
| `sparse_run01` | 0.734432 | 0.742313 |

这个结果很关键：`random1` 在两个 bit order 下都明显偏低，说明 placement 差异不是简单的打包 bit 顺序假象。

核心 8M bit-symbol non-IID 结果进一步支持主结论：

| dataset | 8M MSB H_original |
| --- | ---: |
| `random1_run01` | 0.389520 |
| `random3_run01` | 0.902345 |
| `original_fpga1_run01_10mib` | 0.877727 |

`random1_repeat03` 的 1M repeat smoke 为 MSB `0.390399`、LSB `0.390783`，与 `random1_run01` 保持一致，是坏例可重复性的强证据。

IID 诊断结果也支持采用 non-IID 路线：`random1`、`random3` 和原始 `fpga1` baseline 的 MSB-first 1M smoke 均未通过 LRS 检查。因此论文不能主张这些输出满足 IID 假设；应把 non-IID `H_original` 作为更保守的主结果。

## 机制假设修正

不建议把机制主线写成“手动 placement 让 RO 之间锁定/解锁”。这个说法太强，且和当前 TDC pair 数据不一致。

建议写成：

1. Placement 改变 RO 的局部布线延迟、频率分布和采样相位覆盖。
2. 多个 RO 同时运行时存在 all-on vs single-on 的频率拉拽和动态扰动。
3. 好 placement 可能让采样输出更接近对称，并降低 byte-level 偏置和序列相关。
4. 坏 placement 可能引入稳定偏置或序列结构异常。
5. 当前 TDC pair 没有发现强锁定，所以机制更可能是弱耦合、多源动态交互或采样路径效应，而不是单个近邻 pair 的强同步。

## 可以主张什么

可以主张：

- Placement 是 RO-TRNG 原始随机性的关键工程变量。
- 同一结构不同 placement 可以从接近理想到严重偏置，且 repeat 可复现。
- 粗粒度 placement 标签不足以解释结果，例如 `random1` 和 `random3` 都是 random 类，但质量完全不同。
- TDC 与 RO_FREQ 可以构成机制诊断链路。
- SP800-90B non-IID smoke 独立支持 placement-dependent quality gap。

不能主张：

- 不能说已经完成完整 SP800-90B 认证。
- 不能说已经证明近距离 RO 强锁定导致熵变化。
- 不能把未校准 TDC bin 当作绝对线性时间。
- 不能把单板、常温、默认电压结果推广到所有 FPGA 和所有 PVT 条件。

## 论文图表建议

| 编号 | 内容 | 目的 |
| --- | --- | --- |
| Fig. 1 | placement -> bitstream -> UART capture -> TRNG/RO_FREQ/TDC/90B analysis 流程 | 交代方法 |
| Fig. 2 | placement 矩阵布局示意 | 说明物理变量 |
| Fig. 3 | 各 placement 的 p1、快速 min-entropy 排名 | 主结果 |
| Fig. 4 | formal vs repeat 对比 | 证明可重复 |
| Fig. 5 | RO_FREQ pulling 和 closest beat | 支撑机制诊断 |
| Fig. 6 | 6 个 TDC pair 的 max small-lag correlation | 展示未检测到强锁定 |
| Table I | 实验配置、板卡、bitstream、采集大小、SHA256/metadata | 可复现 |
| Table II | 10 MiB formal TRNG 指标 | 主结果表 |
| Table III | SP800-90B non-IID smoke | 独立熵估计 |
| Table IV | TDC pair dynamics | 机制边界 |
| Table V | 局限与待补实验 | 避免过度主张 |

## 下一步

P0：等待短硬件队列完成，补 `random1_repeat03/random3_repeat03` 的 20 MiB repeat。

P0：队列完成后刷新 repeat 表、paper artifacts、SP800-90B repeat smoke。

P0：把干净文档、脚本、CSV/MD/SVG 结果同步到 GitHub export，供 GPT/Claude 深度分析。

P1：设计 restart dataset 采集，不要把顺序流当 restart。

P1：如果冲顶刊，后续必须补多板、温度/电压/运行时间漂移，或者在论文中清楚限定为单板常温标称电压 characterization study。
