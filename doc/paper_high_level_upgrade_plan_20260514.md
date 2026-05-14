# RO_TRNG 高水平论文升级计划（2026-05-14）

本文档基于现有离线文档和汇总数据整理，不执行 Vivado、COM、JTAG、`hw_server` 或任何硬件采集操作。目标是把当前中文论文草稿从“结果整理”升级为面向高水平论文的结构化论证蓝图，并严格区分已具备证据、机制线索和仍需补齐的最低证据。

已读取并综合的材料：

- `doc/paper_draft_cn_20260513.md`
- `doc/paper_results_update_20260513.md`
- `doc/mechanism_correlation_status_20260513.md`
- `doc/offline_tests_and_figures_fast_mode_20260513.md`

## 1. 论文核心定位

建议把论文定位为：

> 一项面向 FPGA RO-TRNG 的 placement-sensitive raw entropy 实测研究：在相同 FPGA、RTL 和采集流程下，系统展示 RO placement 会导致后处理前 raw bitstream 质量发生数量级可见的分层差异，并提出从 placement、RO frequency/beat、sample relation 到 phase/correlation 的机制验证路线。

这个定位有三个好处：

1. 不把当前证据过度包装成“完整机制已证明”。
2. 能突出当前最强证据，即 10MiB formal 数据中的显著分层和 random1/random3 强对照。
3. 能自然承接后续机制实验、标准测试和多次 repeat，形成可投稿的完整证据链。

当前不建议把论文主线写成“提出一种新 TRNG 结构”或“给出最终 placement 设计准则”。现有结果更强的是测量研究、反例构造、证据链设计和 raw entropy 评估方法，而不是已验证的设计优化规则。

## 2. 核心贡献如何表述

### 2.1 可作为主贡献的表述

贡献 1：构建了同平台、同 RTL、同采集流程下的多 placement RO-TRNG raw entropy 实测矩阵。

- 已有证据：10MiB formal 结果覆盖 `random1`、`random2`、`random3`、`compact`、`sparse`、`row`、`far`、`checker`、`same_column`、`cross_region` 等 placement。
- 写法边界：强调“受控测量矩阵”，不要声称覆盖了所有 FPGA、所有 Vivado seed 或所有板卡。

贡献 2：发现并量化 placement-induced raw entropy stratification。

- 已有证据：`random1_run01` 的 `p1=0.337315512`、`bit_min_entropy=0.593605945`、`byte_min_entropy=4.80160868`，与 `random3_run01` 的 `p1=0.499968565`、`bit_min_entropy=0.999909299`、`byte_min_entropy=7.98455010` 形成强对照。
- 写法边界：可说“当前平台和实验条件下 placement 对 raw entropy 有显著影响”，不要说“某类 placement 必然失败或必然可靠”。

贡献 3：证明粗粒度 placement 标签不足以预测 raw entropy。

- 已有证据：`random1` 和 `random3` 同属 random placement 家族，但一个严重偏置，一个接近理想。
- 高水平写法：把这组对照写成 placement-controlled counterexample pair，说明真实坐标、频率、sample relation、routing/coupling 才是下一层解释变量。

贡献 4：展示单指标 raw entropy 评估的风险。

- 已有证据：`same_column_run01` 的 p1 和 bit min-entropy 接近理想，但 `runs_p=0` 且 adjacent equal ratio 异常。
- 写法边界：用它支持“必须联合报告 balance、runs、adjacent correlation proxy、byte-level entropy”，不要把它写成安全失效或标准测试失败，除非后续标准测试补齐。

贡献 5：给出从现象到机制的候选证据链。

- 已有证据：random1/random3 已有匹配的 RO frequency 线索。`random1` 的最近 all-on data-data pair 为 `data4/data5`，`delta_f=0.466195 MHz`，sample pulling 为 `+3466.91 ppm`；`random3` 最近 pair 为 `data3/data7`，`delta_f=0.673396 MHz`，sample pulling 为 `-824.56 ppm`。
- 写法边界：只能说这些线索“motivate close-pair and sample-relation mechanisms”，不能说已经证明因果。尤其 `random3` 也存在 close pair，因此 close pair alone 不能解释 random1 失败。

## 3. 实验矩阵是否足够

### 3.1 当前足够支撑的论文层级

当前矩阵足够支撑一篇扎实的 measurement-oriented workshop、短文或阶段性论文：

- 10MiB formal 主表完整，能建立 placement-sensitive raw entropy 现象。
- 8 个 placement 的 5MiB repeat 已能支持“趋势可重复”的初步说法。
- random1/random3 的 RO frequency 机制线索能支持机制假设，而非因果结论。
- TDC near/far baseline 能证明离线 TDC 指标链路可用，但不能解释 random1/random3。

### 3.2 面向高水平会议/顶刊的不足

若目标是高水平会议或顶刊，当前实验矩阵还不够。主要不足不是数据量本身，而是证据链闭环尚未完成：

1. 统计重复不足：多数 placement 仍是 1 个 10MiB formal 加 1 个 5MiB repeat，不能给强置信区间、方差或显著性检验。
2. 机制闭环不足：已有 frequency 线索只覆盖 random1/random3 两例，且缺少 pair-specific TDC、sample relation 和 phase/lag correlation。
3. 标准测试不足：尚未给出 SP800-90B / NIST STS 的正式口径，当前主要是 raw entropy 和轻量统计。
4. 泛化边界不足：缺少跨 Vivado seed、跨板卡、跨电压/温度/时间漂移的系统性验证。
5. 设计准则不足：当前能说 placement 是核心变量，但还不能给出可验证的 placement rule 或 screening rule。

## 4. 缺口与补救

| 缺口 | 当前状态 | 风险 | 最小补救 |
| --- | --- | --- | --- |
| 多次 repeat | 已有 8 个 placement 的 5MiB repeat，但每类次数有限 | 审稿人会质疑偶然性和方差 | 对 `random1`、`random3`、`same_column`、`compact`、`sparse` 至少补到多次 repeat，报告均值、标准差、误差条 |
| 机制因果 | 只有 random1/random3 frequency 线索和 TDC near/far baseline | 审稿人会质疑“为何 random1 坏、random3 好” | 补 random1/random3 对应真实 pair 的 TDC phase、lag correlation、sample relation |
| close pair 解释 | random1 和 random3 都有 close pair | close pair alone 无法解释失败 | 增加 sample RO relation、all-on/single-on shift、pairwise phase coherence 的联合指标 |
| 标准随机性 | 目前是轻量 raw tests | 安全/硬件随机数方向审稿人会要求标准口径 | 对关键样本跑 SP800-90B / NIST STS，区分 raw source 与 post-processed output |
| 物理坐标 | placement 标签仍偏粗 | 难以形成设计启示 | 整理 XDC/metadata，输出 RO 坐标、距离、region、可能 routing 特征 |
| 泛化 | 当前集中在单 FPGA/单流程 | 顶刊会质疑外推 | 至少补 Vivado seed 或时间漂移；若资源允许，再补板卡/电压/温度 |

## 5. 推荐论文结构

1. 引言：从 FPGA RO-TRNG 易部署但 raw entropy 对物理实现敏感切入，提出 placement 不能只看成实现细节。
2. 背景与威胁模型：说明 RO-TRNG raw source、sampled XOR、placement/routing/coupling 可能影响 entropy；明确本文研究 raw stream，而非完整密码系统安全证明。
3. 实验平台与数据筛选规则：写清 FPGA、RTL、placement families、10MiB formal、5MiB repeat、partial/invalid 排除规则。
4. 指标定义：p1、monobit、runs、adjacent equal ratio、bit min-entropy、byte entropy、byte min-entropy。
5. 主结果一：placement-induced raw entropy stratification，用 Table 1 和 Fig. 1/2 建立主现象。
6. 主结果二：random1/random3 counterexample pair，强调粗粒度 random 标签不足以预测质量。
7. 主结果三：单指标不足，用 `same_column_run01` 展示 p1 近似理想但相邻相关/runs 异常。
8. repeat 结果：把 5MiB repeat 写成 reproducibility check，不混入 10MiB formal 主排名。
9. 机制线索：报告 random1/random3 frequency/beat/pulling 对照，同时明确它不是因果证明。
10. TDC baseline 与机制补证计划：展示 TDC 指标链路可用，说明为什么还需要 pair-specific TDC。
11. 讨论：placement 设计启示、raw entropy 评估流程、当前边界和泛化限制。
12. 结论：谨慎收束为“现象已建立，机制和泛化仍需补证”。

## 6. 图表列表

### 6.1 正文最低图表

| 编号 | 图表 | 作用 | 当前状态 |
| --- | --- | --- | --- |
| Table 1 | 10MiB formal TRNG metrics | 主结果表，报告所有有效 placement 的 p1、runs、adjacent、bit/byte entropy | 已具备 |
| Fig. 1 | bit min-entropy by placement | 直观展示质量分层 | 已具备脚本输出 |
| Fig. 2 | abs(p1 - 0.5) by placement | 展示 bit bias 贡献 | 已具备脚本输出 |
| Fig. 3 | adjacent equal deviation | 突出 `same_column` 和 `random1` 的相关性问题 | 已具备脚本输出 |
| Table 2 | formal vs repeat | 支持趋势可重复 | 已具备，但只能谨慎解释 |
| Fig. 4 | formal vs repeat scatter | 视觉化 repeat 一致性 | 可由现有 CSV 生成 |
| Table 3 | random1/random3 RO frequency mechanism features | 展示 nearest beat、sample pulling、TRNG quality 联合对照 | 已具备 |
| Fig. 5 | closest beat / sample pulling bar plot | 展示机制线索，而非因果证明 | 已具备脚本输出 |
| Table 4 | TDC near/far baseline | 说明 TDC 分析链路可用 | 已具备 |

### 6.2 高水平版本建议补充图表

| 编号 | 图表 | 需要补的数据 | 审稿价值 |
| --- | --- | --- | --- |
| Fig. 6 | placement coordinate map | XDC/metadata 坐标整理 | 把 placement 标签变成物理变量 |
| Fig. 7 | random1/random3 pair-specific TDC phase histograms | 对应 RO pair TDC | 支撑或排除 coupling/locking/phase diffusion 假设 |
| Fig. 8 | mechanism metric vs entropy scatter | 更多 placement 的 frequency/TDC 特征 | 从 case study 升级为相关性证据 |
| Fig. 9 | repeat error-bar plot | 多次 repeat | 支撑统计稳定性 |
| Table 5 | SP800-90B / NIST results | 标准测试输出 | 给安全随机数领域必要口径 |
| Table 6 | threat-to-validity summary | 无需新采集，但需严谨整理 | 提高论文可信度 |

## 7. 威胁有效性

### 7.1 内部有效性

风险：不同 placement 之外可能还存在采集时刻、环境、bitstream 生成细节、串口采集完整性等混杂因素。

缓解：

- 强调相同 FPGA、相同 RTL、相同采集流程。
- formal 主表只使用 complete valid 10MiB capture。
- partial、invalid、audit-only 数据不进入主结论。
- repeat 只作为趋势复现，不替代 formal ranking。

### 7.2 构念有效性

风险：p1 或 bit min-entropy 不能完整代表 raw TRNG 健康度。

缓解：

- 同时报告 runs、adjacent equal ratio、byte entropy、byte min-entropy。
- 使用 `same_column_run01` 作为单指标不足的正面例证。
- 将 raw-source tests 与标准后续测试分开表述。

### 7.3 结论有效性

风险：当前 repeat 次数有限，random1/random3 机制特征样本数只有 2，不能支持显著相关或回归结论。

缓解：

- 不报告 Pearson/Spearman 显著性。
- 不把 frequency 线索写成因果证明。
- 把机制部分写成 matched case comparison 和 hypotheses。

### 7.4 外部有效性

风险：结果可能依赖当前 FPGA、板卡、Vivado seed、温度、电压和实验流程。

缓解：

- 在结论中限定“当前平台与实验条件下”。
- 把跨 seed、跨板卡、温压、时间漂移列为高水平版本最低补证。

## 8. 审稿人可能质疑点

1. “为什么 random1 坏而 random3 好？机制证据在哪里？”
   - 回答策略：已有 frequency/beat/pulling 线索，但明确还需 pair-specific TDC 和 sample relation。不要硬说已证明。

2. “只有一块 FPGA 或一个 Vivado seed，能泛化吗？”
   - 回答策略：当前贡献是 measurement evidence 和 counterexample pair；泛化需要跨 seed/板卡/环境扩展。高水平版应至少补一个泛化维度。

3. “10MiB 是否足够？”
   - 回答策略：10MiB 足够展示大幅 raw quality 分层，但不足以完成长期稳定性证明。用 repeat 和标准测试补强。

4. “p1 接近 0.5 是否就说明好？”
   - 回答策略：用 `same_column_run01` 反驳，强调多指标。

5. “close pair 是否就是原因？”
   - 回答策略：不是。`random3` 也有 close pair，因此必须联合 sample relation、pulling、phase/correlation。

6. “TDC near/far 为什么能解释 TRNG？”
   - 回答策略：不能解释。它只是 baseline，说明 TDC metric path 可用。

7. “为什么没有 SP800-90B / NIST？”
   - 回答策略：当前稿件阶段聚焦 raw source phenomenon；高水平版本必须补标准测试表，并把 raw 与 post-processed tests 分开。

## 9. 顶刊/高水平会议所需最低证据

若目标是顶刊或强会议，最低证据建议如下：

1. 完整 raw entropy 主矩阵：保留当前 10MiB formal 主表，并清晰给出数据排除规则。
2. 多次 repeat：关键 placement 至少覆盖失败、高质量、边界和单指标异常样本，即 `random1`、`random3`、`same_column`、`compact`、`sparse`。输出均值、标准差、误差条。
3. 标准测试：对 `random1_run01`、`random3_run01`、`same_column_run01`、`compact_run01` 或 `cross_region_run02` 运行 SP800-90B / NIST STS，报告 raw source 和 post-processing 前后的差异。
4. 机制闭环：对 random1/random3 的真实关键 pair 补 TDC phase histogram、diff std、phase Pearson、lag correlation，并联动 RO frequency / beat / pulling 指标。
5. 物理 placement map：从 XDC/metadata 输出实际坐标、距离和 region 关系，避免只用 `random`、`compact` 这类粗标签。
6. 至少一个泛化维度：推荐优先跨 Vivado seed 或时间漂移；若条件允许，再补电压/温度或第二板卡。
7. 可复现实验包：脚本、输入 CSV、生成图表和数据筛选规则固定化，使审稿人能追踪每张图表来源。

## 10. 推荐投稿口径

### 当前证据下的稳妥标题方向

- Placement-Sensitive Raw Entropy in FPGA Ring-Oscillator TRNGs: Empirical Stratification and Mechanism Evidence
- Empirical Evidence of Placement-Induced Raw Entropy Variation in FPGA RO-TRNGs
- From Placement to Raw Entropy: A Measurement Study of FPGA Ring-Oscillator TRNGs

### 摘要中应出现的句子

- “We observe a large placement-dependent raw entropy stratification under the same FPGA, RTL, and capture flow.”
- “The random1/random3 pair shows that a coarse placement label is insufficient to predict raw TRNG quality.”
- “Current RO-frequency features provide mechanism evidence but not causal proof; pair-specific phase measurements remain required.”

### 摘要中不应出现的句子

- “We prove the physical cause of random1 failure.”
- “Random placement is unreliable while compact placement is reliable.”
- “The current data generalizes to all FPGA devices and all implementation seeds.”
- “The TRNG has passed standard certification.”

## 11. 下一步离线优先级

在仍不触碰硬件/Vivado/COM/JTAG/hw_server 的前提下，最值得先做的离线工作是：

1. 整理 placement map：从现有 XDC/metadata 提取坐标、距离、region。
2. 固化图表脚本输出：把现有 fast-mode SVG/CSV 对应到论文 Fig./Table 编号。
3. 准备标准测试清单：列出要输入 SP800-90B / NIST 的 raw capture 文件和报告模板。
4. 重写中文草稿摘要、贡献和威胁有效性章节：把本文档中的边界直接迁入草稿。
5. 为机制补证设计最小实验矩阵：只列计划，不在本文档中执行任何采集或 Vivado 操作。

## 12. 结论性建议

当前论文最强的卖点不是“已经解释所有物理机制”，而是“用受控实测矩阵证明 FPGA RO-TRNG raw entropy 对 placement 高度敏感，并给出一个粗 placement 标签失效的强反例”。高水平版本应围绕这个卖点补足三类证据：多次 repeat 的统计稳定性、random1/random3 的 pair-specific 机制闭环、以及标准随机性测试口径。只要这三类证据补齐，论文可以从阶段性测量报告升级为有说服力的高水平硬件安全/随机数实证研究。
