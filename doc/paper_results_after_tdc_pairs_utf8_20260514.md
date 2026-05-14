# TDC Pair 后论文结果整理 2026-05-14

这份文档是给论文写作和组会汇报用的干净 UTF-8 中文版。它只使用已经完成的硬件采集和离线分析，不额外启动 Vivado、COM3 或 JTAG。

## 一句话结论

当前数据已经足以支撑一个高水平论文方向：在同一块 Zynq-7020 FPGA、同一类 RO-TRNG 结构和相同采集链路下，placement 会导致原始随机性出现显著且可重复的差异；但当前 TDC pair 结果没有检测到强相位锁定，因此机制不能写成“近距离 RO 强锁定导致熵变化”，更稳妥的表述是 placement 改变了多 RO 网络的动态相互作用、频率拉拽、采样相位覆盖和序列相关结构。

## 已完成的硬件证据

主 fast-mode 队列已经完成，状态文件为 `doc/fast_mode_hardware_status_20260513.md`。重点包括：

| 类别 | 已完成数据 | 论文作用 |
| --- | --- | --- |
| TRNG placement matrix | compact、checker、sparse、far、same_column、cross_region、random1/2/3、row 等 formal/repeat | 证明 placement 改变原始随机性 |
| 原始 fpga1 baseline | `original_fpga1_run01_10mib`、`original_fpga1_repeat02_5mib` | 和用户原始工程对照 |
| RO_FREQ | `random1/random3` 多次 2MiB 与 5MiB 分析 | 诊断频率差、beat、sample pulling |
| TDC near/far | near/far baseline repeat | 诊断相位/bin 分布 |
| Pair-specific TDC | 6 个重点 pair，全部 2MiB | 验证强锁定假设是否成立 |

6 个 pair-specific TDC 已完成：

- `random1_ro4_ro5`
- `random1_ro0_ro1`
- `random1_ro2_ro4`
- `random3_ro3_ro7`
- `random3_ro3_ro5`
- `random3_ro0_ro6`

## 主要数值结果

TRNG placement 结果最强。`random1` 是稳定坏例，10MiB formal 的 `p1 = 0.337315512`，bit min-entropy `0.593605945`，5MiB repeat 仍为 `p1 = 0.337669373`、bit min-entropy `0.594376522`。这说明它不是一次采样偶然波动。

`random3` 是稳定好例，10MiB formal 的 `p1 = 0.499968565`，bit min-entropy `0.999909299`，5MiB repeat 为 `p1 = 0.499971128`、bit min-entropy `0.999916694`。它可以作为当前最好的候选 placement。

原始 `fpga1` baseline 也表现较好：10MiB `original_fpga1_run01_10mib` 的 `p1 = 0.500035894`，bit min-entropy `0.999896436`；5MiB repeat 的 `p1 = 0.500216961`，bit min-entropy `0.999374119`。

`same_column` 是一个很重要的反例：它的 p1 接近 0.5，但 runs p-value 为 0，adjacent-equal ratio 约 `0.50598`。论文中应把它作为“只看 bias 不够”的例子。

## TDC Pair 结果

6 个 pair-specific TDC 运行共 96 个窗口，没有任何窗口触发 conservative strong-lock 标志。

| 指标 | 结果 |
| --- | --- |
| pair runs | 6 |
| total windows | 96 |
| strong-lock windows | 0 |
| max small-lag abs correlation | 约 0.0318 |
| mean diff std | 约 2040 ps 到 2043 ps |

这部分的论文写法必须克制：当前结果是“在当前测量条件下未检测到强 pair-level phase locking”。它不能证明完全没有耦合，也不能证明随机性提升来自 TDC 观测到的 pair 锁定。

## 机制假设修正

不建议再把机制主线写成“手动 placement 让 RO 之间锁定/解锁”。这个说法太强，且和当前 TDC pair 数据不一致。

建议写成：

1. Placement 改变 RO 的局部布线延迟、频率分布和采样相位覆盖。
2. 多个 RO 同时运行时存在 all-on vs single-on 的频率拉拽和动态扰动。
3. 好 placement 可能让采样输出更接近对称，并降低 byte-level 偏置。
4. 坏 placement 可能引入稳定偏置或序列结构异常。
5. 当前 TDC pair 没有发现强锁定，所以机制更可能是弱耦合、多源动态交互或采样路径效应，而不是单个近邻 pair 的强同步。

## 现在可以主张什么

可以主张：

- Placement 是 RO-TRNG 原始随机性的关键工程变量。
- 同一个结构不同 placement 可以从接近理想到严重偏置，且 repeat 可复现。
- 粗粒度 placement 标签不足以解释结果，例如 `random1` 和 `random3` 都是 random 类，但质量完全不同。
- TDC 与 RO_FREQ 可以构成机制诊断链路，而不是只做黑盒统计测试。
- 当前 TDC pair 数据给出了重要负结果：未观察到强 pair locking，因此机制解释需要更谨慎。

不能主张：

- 不能说已经完成 SP800-90B 熵源认证。
- 不能说已经证明近距离 RO 强锁定导致熵变化。
- 不能把未校准 TDC bin 当作绝对线性时间。
- 不能把单板、常温、默认电压结果推广到所有 FPGA 和所有 PVT 条件。

## SP800-90B 状态

90B 输入已经准备了 smoke 版本，目录为 `data/sp800_90b/inputs_smoke_20260514`。但是本机当前缺少可用的 `g++`、`make/mingw32-make` 以及相关链接库，NIST EntropyAssessment 尚未编译运行。阻塞说明见 `doc/sp800_90b_blocker_20260514.md`。

论文中应写为：SP800-90B 输入转换流程已准备，non-IID/IID/restart/conditioning 评估仍是必须补齐项。不能把当前快速 `bit_min_entropy` 当成 90B 结果。

## 论文图表清单

已经生成的证据包位于 `data/experiments/paper_artifacts_20260514`，包括：

- `table_placement_trng_repeats.csv/md`
- `table_ro_freq_pulling_summary.csv/md`
- `table_tdc_pair_dynamics_summary.csv/md`
- `table_tdc_pair_dynamics_windows.csv/md`
- `claims_vs_evidence.csv/md`
- `fig_tdc_pair_best_lag_abs_r.svg`

建议论文核心图表：

| 编号 | 内容 | 目的 |
| --- | --- | --- |
| Fig. 1 | 实验流程：placement -> bitstream -> UART capture -> TRNG/RO_FREQ/TDC analysis | 交代方法 |
| Fig. 2 | placement 矩阵布局示意 | 说明物理变量 |
| Fig. 3 | 各 placement 的 p1、bit min-entropy 排名 | 主结果 |
| Fig. 4 | formal vs repeat 对比 | 证明可重复 |
| Fig. 5 | RO_FREQ pulling 和 closest beat | 支撑机制诊断 |
| Fig. 6 | 6 个 TDC pair 的 max small-lag correlation | 展示未检测到强锁定 |
| Table I | 实验配置、板卡、bitstream、采集大小、SHA256/metadata | 可复现 |
| Table II | 10MiB formal TRNG 指标 | 主结果表 |
| Table III | 5MiB repeat 指标 | 稳定性 |
| Table IV | TDC pair dynamics | 机制边界 |
| Table V | SP800-90B 状态与待补实验 | 合规路线 |

## 下一步优先级

P0：安装或配置 SP800-90B 工具链，至少跑 `random1`、`random3`、`original_fpga1` 的 non-IID smoke，再扩展到 formal 全集。

P0：把 `claims_vs_evidence` 写进论文初稿，避免过度主张。

P1：如果继续上板，优先追加 `random1` 坏例和 `random3` 好例的更长 TRNG/RO_FREQ repeat，而不是盲目扩大所有 placement。

P1：若冲顶刊，需要多板、温度、电压和 restart 数据。没有这些时，论文必须把结论限定为单板常温标称电压的 characterization study。

