# RO_TRNG 中文论文初稿骨架（2026-05-13）

本文档目标：基于当前已有数据与文档，整理一版面向高水平论文的中文初稿骨架。所有表述严格区分“已有证据”和“待补证据”；不得把尚未完成的机制测量、标准测试或多次重复统计写成已验证结论。

证据标记规则：

- **已有证据**：当前文件中已有的 10MiB formal TRNG 结果、已完成 5MiB repeat、TDC near/far baseline、只读统计汇总。
- **待补证据**：尚未完成或尚未进入正式汇总的数据，包括 random1/random3 对应 RO frequency/TDC 机制测量、更多 repeat、SP800-90B/NIST、温压/时间漂移等扩展实验。
- **不能使用**：partial、invalid 或 audit 标记不可用于论文主结论的数据，例如 `tdc_near_run01`、`cross_region_run01`、`random1_run02_partial_timeout_8692840.bin`。

## 1. 题目候选

中文题目候选：

1. **FPGA RO-TRNG 原始熵的布局敏感性实测分析：从质量分层到机制验证**
2. **面向 FPGA 环形振荡器真随机数发生器的布局敏感性研究：raw entropy、重复性与相位机制**
3. **同一 FPGA 上 RO-TRNG 布局对 raw entropy 的影响：可重复失效样本与机制验证路径**
4. **FPGA RO-TRNG 中 placement-induced entropy collapse 的实测证据与机制假设**

英文题目候选：

1. **Placement-Sensitive Raw Entropy in FPGA Ring-Oscillator TRNGs: Empirical Stratification and Mechanism Validation**
2. **Empirical Evidence of Placement-Induced Entropy Variation in FPGA RO-TRNGs**
3. **From Layout to Raw Entropy: A Measurement Study of FPGA Ring-Oscillator TRNGs**

当前最稳妥版本建议使用候选 1，因为它同时覆盖“已有现象”和“待补机制”，但不会提前声称机制已经证明。

## 2. 摘要草稿

环形振荡器真随机数发生器（RO-TRNG）常被视为易于在 FPGA 上部署的轻量级熵源，但其后处理前的 raw entropy 可能强烈依赖物理布局和布线环境。本文在同一 FPGA 平台、相同 RTL、相同采集流程下，对多种 RO placement 进行 10MiB raw bit 采集与统计分析。已有结果表明，placement 对 raw bit 质量具有显著影响：`random1_run01` 出现严重偏置，`p1=0.337316`，bit min-entropy 为 `0.593606`；而同属 random placement 族的 `random3_run01` 接近理想，`p1=0.499969`，bit min-entropy 为 `0.999909`。`compact`、`checker`、`cross_region` 与 `random3` 形成高质量组，`sparse`、`row`、`far` 与 `random2` 呈现中间梯度，说明 placement 影响不是简单的二元好坏分类。已有 5MiB repeat 进一步显示 `random1`、`random3`、`compact` 与 `sparse` 的主要趋势可重复。与此同时，`same_column_run01` 虽然 bit balance 接近理想，但 runs 与相邻 bit 指标异常，提示 raw TRNG 评估不能只依赖 p1 或 bit min-entropy。当前 TDC near/far 数据只能作为测量链路 baseline，尚不能解释 random1/random3 的差异；后续需要通过对应 placement 的 RO frequency、beat-frequency 与 TDC pair 测量建立从布局到频率/相位行为再到 raw entropy 的证据链。本文的当前贡献是给出 FPGA RO-TRNG placement-sensitive raw entropy 的实测分层、重复性线索和机制验证路线，为后续布局约束、快速筛查和标准化随机性评估提供依据。

摘要中可写的边界：

- **已有证据**：10MiB formal 指标、部分 5MiB repeat、一组 TDC near/far baseline。
- **待补证据**：random1/random3 的对应机制测量、SP800-90B/NIST、更多 repeat 后的置信区间。

## 3. 贡献点草稿

已有证据支撑的贡献：

1. 在同一 FPGA、相同 RTL 与相同采集流程下，构建并比较多种 RO placement 的 10MiB formal raw bit 数据集，覆盖 `random`、`compact`、`sparse`、`row`、`far`、`checker`、`same_column`、`cross_region` 等布局。
2. 证明 placement 会显著影响 raw TRNG 的 `p1`、bit min-entropy、byte entropy、runs p-value 与 adjacent equal ratio。当前结果中 bit min-entropy 从 `0.593606` 到 `0.999909`，呈现明显质量分层。
3. 发现同属 random placement 族的 `random1` 与 `random3` 表现出强烈反差：前者严重偏置且 repeat 可重复，后者接近理想且 repeat 可重复，说明粗粒度 placement 标签不足以预测 raw entropy。
4. 通过 `same_column_run01` 展示单指标评估风险：p1 与 bit min-entropy 接近理想并不保证 runs 或相邻 bit 相关性正常。
5. 给出 smoke/formal/repeat/TDC baseline 组合的实验叙事：先用 formal raw entropy 建立现象，再用 repeat 检查稳定性，最后用 frequency/TDC 机制测量解释原因。

需要待补证据后才能升级为正式贡献的内容：

1. 建立 `placement -> frequency/phase/correlation -> entropy` 的机制证据链。
2. 用 SP800-90B/NIST 对主样本给出标准口径的随机性或熵评估。
3. 用多次 repeat 给出每类 placement 的均值、方差、置信区间或统计显著性。
4. 给出可操作的 placement 设计准则，例如哪些坐标关系、频率关系或 coupling 指标应避免。

## 4. 实验设计骨架

### 4.1 平台与控制变量

已有证据：

- 实验在同一 FPGA 平台与相同 RTL/采集流程下进行。
- random1/random3 机制文档记录两者 manifest 均指向 `RO_TRNG_top`、`xc7z020clg400-2`、Vivado `2023.2`、Vivado seed `1`。
- TRNG 实例为 `u_entropy_source`，配置为 `RO_NUM=8`、`RO_STAGES=2`、`SAMPLE_STAGES=9`。
- random1 与 random3 的主要差异来自 RO placement XDC。

论文写法：

> 为隔离 placement 对 raw entropy 的影响，本研究在同一 FPGA、相同 RTL、相同 bitstream 生成流程和相同采集协议下改变 RO placement，并对采集得到的 raw bitstream 进行统一统计分析。

待补证据：

- 温度、电压、时间漂移等环境变量尚未系统扫描。
- 当前没有跨板卡、跨 FPGA 型号、跨 Vivado seed 的完整扩展实验。

### 4.2 Placement 组别

已有证据覆盖：

| 组别 | formal run | 当前角色 |
| --- | --- | --- |
| random1 | `random1_run01` | 极差反例，严重 bit bias |
| random2 | `random2_run01` | 中间梯度 |
| random3 | `random3_run01` | 高质量样本，当前 bit min-entropy 最好 |
| compact | `compact_run01` | 高质量样本 |
| sparse | `sparse_run01` | 中间偏差样本 |
| row | `row_run01` | 中间偏差样本 |
| far | `far_run01` | 轻中度偏差样本 |
| checker | `checker_run01` | 高质量样本 |
| same_column | `same_column_run01` | balance 好但相关性异常的特殊样本 |
| cross_region | `cross_region_run02` | 高质量样本，formal 有效 run 使用 run02 |

注意：

- `cross_region_run01` 是 partial，不进入 formal 主表。
- 不能把 “random placement” 写成必然好或必然坏；random1 与 random3 已经显示同一粗标签内部差异巨大。

### 4.3 数据规模与指标

已有证据：

- formal 主结果均为 10MiB，`bytes=10485760`。
- 已完成部分 5MiB repeat，`bytes=5242880`。
- formal 指标包括 `p1`、`bit_min_entropy`、`monobit_p`、`runs_p`、`adjacent_equal_ratio`、`byte_entropy`、`byte_min_entropy`。
- repeat 汇总当前只对已完成样本给出 n=1 的 repeat 补充，不应与 10MiB formal 主排名混合。

论文写法：

> 本文主结果以 10MiB formal capture 为准，5MiB repeat 仅用于检查关键样本的趋势是否可重复。所有 partial 或 invalid capture 均不进入主结论。

## 5. 已完成结果表述

### 5.1 10MiB formal 主结果

已有证据：

| 分层 | run | p1 | bit_min_entropy | runs_p | adjacent_equal_ratio | byte_min_entropy | 可写结论 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 严重失败 | `random1_run01` | 0.337316 | 0.593606 | 0 | 0.556740 | 4.80161 | 当前最强负例，bit bias 与 byte min-entropy 均明显恶化 |
| 中间梯度 | `sparse_run01` | 0.464350 | 0.900637 | 0 | 0.506596 | 7.14406 | 明显偏置，但未达到 random1 的失效程度 |
| 中间梯度 | `row_run01` | 0.473580 | 0.925713 | 0 | 0.504304 | 7.36646 | 偏置较 sparse 轻 |
| 中间梯度 | `random2_run01` | 0.491222 | 0.974892 | 0 | 0.501080 | 7.77684 | 接近 0.5，但 formal 指标仍显示偏差 |
| 中间梯度 | `far_run01` | 0.491508 | 0.975703 | 0 | 0.500726 | 7.79616 | 接近 0.5，但仍低于高质量组 |
| 高质量 | `checker_run01` | 0.499929 | 0.999796 | 0.149267 | 0.500079 | 7.97279 | p1、min-entropy 与相邻比例均接近理想 |
| 特殊样本 | `same_column_run01` | 0.499930 | 0.999799 | 0 | 0.505980 | 7.86432 | balance 好，但 runs/相邻相关异常 |
| 高质量 | `cross_region_run02` | 0.499944 | 0.999839 | 0.719841 | 0.499980 | 7.98368 | 高质量，有效 formal run 为 run02 |
| 高质量 | `compact_run01` | 0.499948 | 0.999850 | 0.263603 | 0.499939 | 7.97683 | 高质量 |
| 高质量 | `random3_run01` | 0.499969 | 0.999909 | 0.184373 | 0.500072 | 7.98455 | 当前 bit min-entropy 最好 |

可写的核心结果：

- **已有证据**：placement 对 raw bit quality 的影响很大，当前 10MiB formal 中 `random1_run01` 与 `random3_run01` 的对比最强。
- **已有证据**：高质量组、中间梯度组、严重失败组同时存在，说明 placement 影响是连续、多因素现象。
- **已有证据**：`same_column_run01` 显示 p1/bit min-entropy 不能单独代表 raw stream 健康程度，必须同时报告 runs 与 adjacent equal ratio。

不能写成：

- 不能写“random placement 不可靠”或“compact placement 必然可靠”。当前只能说不同 placement 实例表现不同。
- 不能写“random1 的失败机制已经被证明”。当前只有现象和重复性线索，机制还待补。

### 5.2 5MiB repeat 重复性线索

已有证据：

| placement | formal run p1 / bit_min_entropy | repeat02 p1 / bit_min_entropy | 当前读法 |
| --- | --- | --- | --- |
| random1 | 0.337316 / 0.593606 | 0.337669 / 0.594377 | 严重偏置趋势可重复 |
| random3 | 0.499969 / 0.999909 | 0.499971 / 0.999917 | 高质量趋势可重复 |
| compact | 0.499948 / 0.999850 | 0.500059 / 0.999829 | 高质量趋势可重复 |
| sparse | 0.464350 / 0.900637 | 0.464141 / 0.900073 | 中间偏差趋势可重复 |

论文写法：

> 5MiB repeat02 未被混入 10MiB formal 主排名，而是作为重复性补充。当前四个关键样本的 repeat 与 formal 方向一致，支持主要现象不是一次性采集偶然事件。

边界：

- 当前 repeat 对每个 placement 仍只有有限次数，不能写强统计显著性或置信区间。
- 后续至少需要更多 repeat 才能给出均值、方差和误差条。

### 5.3 TDC near/far baseline

已有证据：

| run | packets | seq_gaps | lane A std phase | lane B std phase | diff std | phase Pearson r |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `tdc_near_run02` | 262143 | 0 | 1350.48 ps | 1379.85 ps | 1927.59 ps | 0.00328 |
| `tdc_far_run01` | 262132 | 43 | 1350.52 ps | 1361.22 ps | 1915.29 ps | 0.00230 |

可写结论：

- **已有证据**：TDC near/far baseline 表明当前 TDC 采集和分析链路可以产生有效 packets 与 phase 统计。
- **已有证据**：当前 near/far probe 的 `diff_std_ps` 与 `phase Pearson r` 差异很小，没有在这两个 baseline placement 上观察到明显 phase correlation 差异。

不能写成：

- 不能说当前 TDC 数据解释了 `random1` 或 `random3` 的 TRNG 质量。
- 不能说 TDC 已证明或排除了 coupling、locking、routing 或 power noise 机制。

## 6. 机制假设

当前机制部分应写成“可检验假设”，不能写成“已证明机制”。

H1：`random1` 的 8 个 2-stage data RO 中可能存在频率过近或 beat frequency 落入不利区间的 pair，使 XOR 或 sampled-data 组合后出现稳定 bit bias。

- 当前状态：**待补证据**。需要 RO frequency/counter 数据、pairwise `abs(delta_f)` 和 data-vs-sample beat ranking。

H2：`random1` 中部分 data RO 与 sample RO 的相位漂移较慢，sample edge 看到的 RO 状态更确定；`random3` 中相位扩散更充分或频率差更分散，因此输出接近 0.5。

- 当前状态：**待补证据**。需要 data RO vs sample RO 的 frequency 或 TDC phase relation。

H3：局部布局、routing、供电扰动或 injection-pulling 可能引入 common-mode phase noise 或 pulling，使部分 RO 的独立性降低，从而降低 raw entropy。

- 当前状态：**待补证据**。需要 all-on vs single-on frequency shift、TDC pair correlation 或 lag correlation。

H4：`random1/random3` 的差异不是由粗粒度 “random placement” 标签决定，而是由实际坐标、RO 频率、pairwise phase relation、sample relation 和 routing 共同决定。

- 当前状态：**已有证据 + 待补机制**。已有 evidence 支持同一 random 标签内存在巨大质量差异；具体物理原因仍需 frequency/TDC 测量。

## 7. 待补实验

优先级建议：

1. **更多 repeat 与聚合统计**
   - 目标：对 `random1`、`random3`、`compact`、`sparse` 以及 `same_column` 等关键样本补足多次 repeat。
   - 输出：均值、标准差、误差条、repeat-by-placement 表。
   - 论文作用：把“趋势可重复”升级为“统计上稳定”。

2. **random1/random3 RO frequency / beat-frequency 测量**
   - 目标：测 8 个 data RO 与 sample RO 的频率、jitter、all-on vs single-on frequency shift。
   - 输出：per-RO frequency table、pairwise delta-f heatmap、data-sample beat ranking、pulling ppm。
   - 论文作用：给 `p1≈0.337` 的强 bias 提供最直接的候选机制证据。

3. **random1/random3 对应 TDC pair 测量**
   - 目标：把 TDC probe 放到 random1/random3 的真实 RO 坐标或关键 pair 上。
   - 推荐 pair：random1 `(0,4)`、`(0,1)`、`(2,3)`、`(2,6)`、`(3,6)`；random3 `(0,7)`、`(0,4)`、`(4,7)`、`(1,5)`、`(3,6)`。
   - 输出：phase histogram、`diff_std_ps`、`phase_pearson_r`、lag correlation、TDC bin quality。
   - 论文作用：验证相位扩散、pairwise correlation、coupling/locking 假设。

4. **sample relation 测量**
   - 目标：测 data RO 与 sample RO 的相位/频率关系，而不只测 data-data pair。
   - 输出：data-vs-sample TDC 或 frequency evidence。
   - 论文作用：解释 sample edge 是否长期落入某些 data RO 的确定性区间。

5. **SP800-90B / NIST**
   - 目标：对主结果样本跑标准测试。
   - 输出：标准熵估计、NIST STS 结果与 pass/fail 口径。
   - 论文作用：把 raw entropy 现象与标准随机性评估区分开。

6. **Placement map 与坐标量化**
   - 目标：从现有 XDC/metadata 整理各 placement 的实际坐标、距离、区域关系。
   - 输出：器件坐标图、RO pair distance table、可能的 routing/region 特征。
   - 论文作用：把粗标签转化为可解释的物理布局变量。

## 8. 图表清单

| 编号 | 图表 | 数据源 | 当前状态 | 证据属性 |
| --- | --- | --- | --- | --- |
| Table 1 | 10MiB formal 主结果表 | `trng_formal_all_10mib_ranked.md/csv` | 可立即写入 | 已有证据 |
| Table 2 | 5MiB repeat 对照表 | `trng_repeats_by_placement.md` | 可作为补充表 | 已有证据，但 repeat 次数有限 |
| Fig. 1 | bit min-entropy 排序柱状图 | formal ranked CSV | 可立即生成 | 已有证据 |
| Fig. 2 | `abs(p1-0.5)` 排序图 | formal ranked CSV | 可立即生成 | 已有证据 |
| Fig. 3 | adjacent equal ratio 偏离图 | formal ranked CSV | 可立即生成 | 已有证据 |
| Fig. 4 | byte min-entropy / byte entropy 对照 | formal ranked CSV | 可立即生成 | 已有证据 |
| Fig. 5 | smoke-vs-formal 散点图 | `hardware_run_audit.csv` | 可生成，但需引用 audit | 已有证据，需整理 |
| Fig. 6 | TDC near/far baseline 图 | `tdc_near_far_compare.csv` 或文档表 | 可生成 | 已有证据，仅 baseline |
| Fig. 7 | placement map | XDC/placement metadata | 需要整理坐标 | 已有文件可整理，不需新采集 |
| Fig. 8 | random1/random3 frequency heatmap | 后续 frequency measurement | 尚无 | 待补证据 |
| Fig. 9 | random1/random3 TDC pair phase/correlation | 后续 TDC pair measurement | 尚无 | 待补证据 |
| Fig. 10 | 机制指标 vs entropy 指标相关图 | 后续机制汇总 + formal 指标 | 尚无 | 待补证据 |
| Table 3 | SP800-90B / NIST 结果 | 后续标准测试 | 尚无 | 待补证据 |

建议正文图表顺序：

1. Table 1 + Fig. 1：建立 placement-sensitive raw entropy 的主现象。
2. Fig. 2 + Fig. 3：分别展示 bias 与相邻相关性，说明多指标必要性。
3. Table 2：补充关键样本 repeat 一致性。
4. Fig. 5：说明 smoke 可作为快速筛查，但 formal 仍是主结果。
5. Fig. 6：说明 TDC baseline 可用，但不是机制证明。
6. Fig. 7-10：待机制实验完成后，用于把现象推进到物理解释。

## 9. 章节骨架建议

### 9.1 引言

主线：

- RO-TRNG 在 FPGA 上部署简单，但 raw entropy 易受物理实现影响。
- 现有工作常关注结构、后处理或标准测试，但实际 placement 对 raw entropy 的影响需要实测量化。
- 本文提出一个 placement-sensitive measurement study：用同一平台和同一 RTL 下的多 placement 数据建立现象，再用 repeat 和机制测量推进解释。

边界写法：

- 当前可以强调 placement 是重要变量。
- 不要在引言中过早宣称已经得到了完整物理机制。

### 9.2 方法

内容：

- FPGA/RTL/采集流程控制变量。
- placement 矩阵设计。
- formal 10MiB、repeat 5MiB、TDC baseline 的角色分工。
- 指标定义：p1、bit min-entropy、monobit_p、runs_p、adjacent_equal_ratio、byte_entropy、byte_min_entropy。
- 数据筛选规则：partial/invalid 不进入主表。

### 9.3 结果一：Placement 导致 raw entropy 分层

内容：

- 使用 Table 1 和 Fig. 1/2 展示 `random1` 到 `random3` 的巨大差异。
- 强调高质量组、中间梯度组、失败组。
- 写明 10MiB formal 是主结果。

### 9.4 结果二：单指标不足与 repeat 线索

内容：

- `same_column_run01` 作为“p1 好但相关性异常”的案例。
- 5MiB repeat 表明关键好/坏样本趋势一致。
- 明确 repeat 次数仍不足以支持强置信区间。

### 9.5 结果三：TDC baseline 与机制验证缺口

内容：

- 当前 TDC near/far baseline 的 packets、diff std、phase Pearson。
- 强调该 baseline 只能证明链路可用，不能解释 random1/random3。
- 引出机制假设与下一步实验。

### 9.6 机制验证计划

内容：

- RO frequency/beat-frequency 优先。
- 少量关键 TDC pair。
- sample relation。
- 机制指标与 entropy 指标关联。

### 9.7 讨论

内容：

- placement 标签不足以预测质量，需要实际坐标、频率、相位和 routing/coupling 证据。
- raw entropy 评估需要多指标，不应只看 p1。
- 当前研究对 FPGA RO-TRNG 设计流程的启示：先 smoke 筛查，再 formal 验证，再机制测量，最后标准测试。

### 9.8 结论

当前安全结论：

- 在当前平台和实验条件下，RO placement 显著影响 raw TRNG 质量。
- random1/random3 是强对照，显示同类 placement 标签内部也可能产生巨大差异。
- 多指标评估和 repeat 是必要的。
- 机制解释和标准认证仍需后续补证。

## 10. 不能夸大的结论

以下表述不要写入论文主结论：

1. “random1 的失败已经由 TDC 证明是耦合/锁定导致。”
   - 原因：当前 TDC near/far 是 baseline，不对应 random1/random3 的实际 RO 坐标或 sample relation。

2. “near/far placement 与 TRNG 质量之间已建立因果关系。”
   - 原因：当前 near/far TDC probe 与 TRNG entropy source 结构和位置不一致。

3. “某类 placement 必然好或必然坏。”
   - 原因：`random1` 与 `random3` 同属 random placement，却一坏一好。

4. “当前数据已经达到标准认证随机性。”
   - 原因：尚未完成 SP800-90B/NIST 标准口径测试，当前主要是 raw entropy 和基础统计。

5. “所有 placement 的统计显著性和置信区间已经充分。”
   - 原因：多数 placement 只有一个 10MiB formal，repeat 次数仍不足。

6. “partial 数据可补充 formal 排名。”
   - 原因：`cross_region_run01`、`random1_run02_partial_timeout_8692840.bin` 等不能进入主排名。

7. “当前结果可直接推广到所有 FPGA、所有 Vivado seed 或所有板卡。”
   - 原因：当前实验集中在当前 FPGA1、当前 RTL 与当前采集流程，跨平台泛化仍需补证。

## 11. 可直接放进论文的谨慎表述

可用表述：

- “在相同 RTL 与采集流程下，不同 RO placement 造成了可观测且在关键样本上可重复的 raw entropy 差异。”
- “`random1` 与 `random3` 构成 placement-controlled counterexample pair：它们同属 random placement 族，却分别表现为严重偏置与接近理想。”
- “当前 TDC near/far 结果作为 measurement baseline，说明 TDC 链路可产生有效 phase 统计，但尚不能作为 random1/random3 质量差异的因果解释。”
- “这些结果提示 FPGA RO-TRNG 的 placement 不能被视为实现细节，而应作为 raw entropy 设计和验证流程中的核心变量。”

谨慎英文表述备用：

- “The current evidence establishes a placement-sensitive raw entropy phenomenon, while the physical mechanism remains to be validated by colocated frequency and phase measurements.”
- “The near/far TDC data should be interpreted as a measurement baseline rather than causal evidence for the random1/random3 entropy gap.”

## 12. 数据来源

本草稿基于以下已有文件整理：

- `doc/experiment_execution_status_20260513.md`
- `doc/paper_story_and_figures_20260513.md`
- `doc/mechanism_validation_plan_random1_random3_20260513.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`

未执行任何 Vivado、JTAG、COM3、hw_server 或硬件采集操作。
