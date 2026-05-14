# RO_TRNG 中文论文初稿 v2 框架（2026-05-14）

本文档用于整合当前已有论文材料，形成一版可继续扩写的中文论文初稿 v2。本文档不引入新的硬件采集，不把尚未完成的 SP800-90B、跨板卡、温压扫描或更长重复实验写成已完成结论。所有结论均限定在当前 Zynq-7020 FPGA、当前 RTL、当前 fast-mode 采集链路和已完成离线分析范围内。

## 1. 标题候选

### 中文标题候选

1. **FPGA RO-TRNG 原始随机性的布局敏感性表征：从 placement 矩阵到频率与相位诊断**
2. **同构 FPGA RO-TRNG 在不同布局下的原始熵分层与机制边界**
3. **面向 FPGA RO-TRNG 的 placement-sensitive characterization：原始随机性、重复性与负向 TDC 证据**
4. **FPGA 环形振荡器 TRNG 的布局诱导随机性差异：实测分层与机制诊断**

### 英文标题候选

1. **Placement-Sensitive Raw Entropy in FPGA Ring-Oscillator TRNGs: Characterization, Repeatability, and Mechanism Boundaries**
2. **A Measurement Study of Placement-Induced Raw Randomness Variation in FPGA RO-TRNGs**
3. **From Placement to Raw Entropy: Empirical Stratification and Null TDC Evidence in FPGA RO-TRNGs**

当前建议优先采用中文标题候选 1 或英文标题候选 1。它们强调“表征”和“机制边界”，避免把当前 TDC pair 负结果误写成已证明的物理机制。

## 2. 摘要草稿

环形振荡器真随机数发生器（RO-TRNG）常被视为适合 FPGA 实现的轻量级熵源，但其后处理前的 raw bitstream 可能强烈依赖实际 placement、routing、频率分布和采样相位关系。本文在同一块 Zynq-7020 FPGA、相同 RO-TRNG RTL、相同采集链路和统一离线分析流程下，构建多组 RO placement，并对其 raw output 进行 10MiB formal capture、部分 5MiB repeat capture、RO frequency 诊断和 TDC pair 相位诊断。

当前结果显示，不同 placement 会导致可观测且在关键样本上可重复的原始随机性差异。典型负例 `random1` 在 10MiB formal capture 中表现出严重偏置，`p1=0.337315512`，bit min-entropy 为 `0.593605945`；其 5MiB repeat 仍为 `p1=0.337669373`、bit min-entropy `0.594376522`。相反，同属 random placement 类别的 `random3` 在 10MiB formal capture 中接近理想，`p1=0.499968565`，bit min-entropy 为 `0.999909299`，repeat 中也保持接近理想。这一对照说明，粗粒度 placement 标签不足以解释或预测 RO-TRNG 的 raw entropy 质量。

本文还观察到 `same_column` 的 p1 接近 0.5，但 runs p-value 为 0，adjacent-equal ratio 约为 `0.50598`，说明单独依赖 bit balance 或 bit min-entropy 不足以评估 raw stream 的序列健康程度。机制诊断方面，RO_FREQ 结果显示 all-on 操作会带来可测的频率 pulling，而 6 个重点 pair-specific TDC 测试共 96 个窗口均未触发 conservative strong-lock 标志，最大 small-lag 绝对相关约为 `0.0317827`。因此，当前 TDC pair 结果应被解释为对“强 pair-level phase locking”假设的负结果，而不能被写成耦合完全不存在，也不能被写成 random1/random3 差异已经由 TDC 因果解释。

本文的贡献在于给出 FPGA RO-TRNG placement-sensitive raw entropy 的实测分层、关键样本 repeat 证据、RO_FREQ/TDC 机制诊断链路以及明确的负结果边界。SP800-90B 输入转换流程目前已准备 smoke 版本，但 EntropyAssessment 尚未完成编译运行，因此本文当前不能声称完成 90B 熵源认证或标准合规评估。

## 3. 贡献点

本文当前可稳妥主张的贡献如下：

1. **构建同平台同 RTL 下的 placement-sensitive RO-TRNG 表征流程。** 在同一 FPGA、相同 RTL、相同 bitstream 生成与采集流程下改变 RO placement，并对 raw bitstream、RO frequency 和 TDC phase/bin 行为进行统一离线分析。

2. **给出 placement 导致 raw randomness 显著分层的实测证据。** 10MiB formal capture 显示 bit min-entropy 从 `0.593605945` 到 `0.999909299`，不同 placement 在 p1、bit min-entropy、runs p-value、adjacent-equal ratio、byte-level 指标上呈现明显差异。

3. **发现 coarse placement label 不足以解释质量差异。** `random1` 与 `random3` 均属于 random placement 类别，但前者稳定表现为严重偏置，后者稳定接近理想，说明实际坐标、routing、频率、相位和采样关系可能共同决定 raw entropy。

4. **用 repeat capture 支持关键现象不是单次采样偶然波动。** `random1`、`random3`、`compact`、`sparse` 等关键样本的 5MiB repeat 与 10MiB formal 方向一致。该结论仅支持“趋势可重复”，尚不足以给出强置信区间或跨条件泛化。

5. **给出重要的机制负结果。** 6 个重点 TDC pair、共 96 个分析窗口未检测到 conservative strong-lock；因此当前数据不支持把随机性退化直接归因于单个近邻 RO pair 的强相位锁定。

6. **明确标准评估与论文结论的边界。** 当前结果是 raw entropy 与机制诊断层面的 characterization，不能替代 SP800-90B、NIST STS、AIS-31 或跨 PVT/跨板卡评估。

## 4. 方法框架

### 4.1 研究问题

本文围绕三个问题展开：

1. 在相同 FPGA、相同 RTL 和相同采集链路下，仅改变 RO placement 是否会显著改变 raw bitstream 质量？
2. 这种差异是否能在关键 placement 的 repeat capture 中保持方向一致？
3. RO_FREQ 与 TDC pair 诊断是否能支持或排除某些简单机制假设，特别是“单个 pair 强相位锁定导致熵退化”这一解释？

### 4.2 实验控制变量

当前实验限定在同一块 Zynq-7020 FPGA、同一类 RO-TRNG 结构和相同采集链路上。已有 metadata 显示 random1/random3 等关键样本使用相同 top、相同器件、相同 Vivado 版本和相同 Vivado seed，主要差别来自 RO placement XDC。

TRNG 实例配置保持一致：`RO_NUM=8`、`RO_STAGES=2`、`SAMPLE_STAGES=9`。论文中应写作“在当前控制变量下观察到 placement-sensitive raw entropy”，而不是写作“所有 FPGA 或所有 Vivado seed 上均成立”。

### 4.3 Placement 组别

当前 formal/repeat 数据覆盖如下组别：

| 组别 | 论文角色 |
| --- | --- |
| `random1` | 稳定坏例，严重 bit bias |
| `random2` | 中间梯度 |
| `random3` | 稳定好例，当前 bit min-entropy 最好 |
| `compact` | 高质量样本 |
| `sparse` | 中间偏差样本 |
| `row` | 中间偏差样本 |
| `far` | 轻中度偏差样本 |
| `checker` | 高质量样本 |
| `same_column` | p1 接近理想但序列相关性异常的反例 |
| `cross_region` | 高质量样本，formal 有效 run 使用 run02 |
| `original_fpga1` | 原始工程 baseline，对照样本 |

`partial`、`invalid` 或 audit-only 数据不进入主结论。`cross_region_run01` 等 partial capture 不应混入 formal 排名。

### 4.4 指标体系

主结果以 10MiB formal capture 为准，部分 5MiB repeat 只作为趋势重复性证据。当前使用的 raw bitstream 指标包括：

- `p1`
- `abs(p1-0.5)`
- `bit_min_entropy`
- `monobit_p`
- `runs_p`
- `adjacent_equal_ratio`
- `byte_entropy`
- `byte_min_entropy`

论文应强调多指标联合评估。`same_column` 的反例说明，p1 接近 0.5 并不保证 runs 或相邻 bit 结构正常。

### 4.5 机制诊断链路

当前机制诊断包括两类：

1. **RO_FREQ 诊断。** 用于观察 random1/random3 中 all-on vs single-on 频率 shift、sample pulling、data RO 频率分布和 beat 关系。
2. **TDC pair 诊断。** 用于观察选定 RO pair 的 phase/bin 动态、小滞后相关和 strong-lock 标志。

TDC pair 的定位应是“约束机制假设”，不是“已经解释熵变化”。当前 TDC 结果是负结果：未发现强 pair-level phase locking。

## 5. 实验设计

### 5.1 TRNG placement matrix

对 compact、checker、sparse、far、same_column、cross_region、random1/2/3、row、original_fpga1 等 placement 进行 formal 或 repeat capture。主表应以 10MiB formal capture 为核心，并把 repeat 单独放在稳定性表中。

建议正文图表：

| 图表 | 内容 | 目的 |
| --- | --- | --- |
| Fig. 1 | 实验流程：placement -> bitstream -> UART capture -> TRNG/RO_FREQ/TDC analysis | 交代方法链路 |
| Fig. 2 | placement 矩阵或坐标示意 | 说明 placement 是自变量 |
| Fig. 3 | p1 与 bit min-entropy 排名 | 展示主现象 |
| Fig. 4 | formal vs repeat 对比 | 展示关键趋势可重复 |
| Fig. 5 | RO_FREQ pulling 与 closest beat | 支持机制诊断 |
| Fig. 6 | 6 个 TDC pair 的 max small-lag correlation | 展示未检测到强锁定 |
| Table I | 实验配置、bitstream、采集大小、metadata/hash | 支持可复现 |
| Table II | 10MiB formal TRNG 指标 | 主结果 |
| Table III | 5MiB repeat 指标 | 稳定性 |
| Table IV | TDC pair dynamics | 机制边界 |
| Table V | SP800-90B 状态与待补实验 | 合规路线 |

### 5.2 Repeat capture

当前 repeat 的角色是“有限重复性检查”，不是完整统计显著性证明。可写作：

> 对关键 placement 的 5MiB repeat capture 显示，严重偏置样本、高质量样本和中间偏差样本的主要趋势与 10MiB formal capture 一致，说明主现象不太可能只是单次采集偶然波动。但由于 repeat 次数有限，本文暂不报告跨 placement 的强置信区间或方差模型。

### 5.3 RO_FREQ 与 TDC pair

RO_FREQ 用于检查 frequency pulling、sample shift 和 beat 关系。当前 claims_vs_evidence 显示：

- all-on operation measurably pulls RO frequencies；
- 最大 `|sample_shift_ppm|=3466.91`；
- 最大 `data_mean_abs_ppm=478.085`；
- 该结论只总结 random1/random3 RO_FREQ run，不能泛化到所有 placement。

TDC pair 用于检查强 pair-level phase locking。当前 6 个 pair-specific TDC run 覆盖：

- `random1_ro4_ro5`
- `random1_ro0_ro1`
- `random1_ro2_ro4`
- `random3_ro3_ro7`
- `random3_ro3_ro5`
- `random3_ro0_ro6`

共 96 个窗口中 strong-lock windows 为 0，max small-lag `|r|=0.0317827`。这应写成负结果或 null evidence：当前测量条件下未检测到强锁定，但不能排除更弱耦合、其他 pair、其他温压条件或更长采样下的相互作用。

### 5.4 SP800-90B 状态

SP800-90B 输入转换流程已准备 smoke 版本，目录为 `data/sp800_90b/inputs_smoke_20260514`。但当前机器缺少可用 `g++`、`make/mingw32-make` 及相关链接环境，NIST EntropyAssessment 尚未完成编译运行。论文中只能写：

> 本研究已准备 SP800-90B 输入转换流程，后续需完成 IID/Non-IID、restart 和 conditioning 相关评估。当前 bit min-entropy 是本文离线统计指标，不能替代 SP800-90B 估计结果。

不能写“已通过 SP800-90B”或“已完成标准熵源认证”。

## 6. 结果组织

### 6.1 Placement 导致 raw entropy 分层

当前最核心的结果是 10MiB formal capture 中，placement 对 raw bit quality 的影响很大。可在正文中这样组织：

| placement/run | p1 | bit min-entropy | 论文解读 |
| --- | ---: | ---: | --- |
| `random1` formal | 0.337315512 | 0.593605945 | 严重偏置，当前最强坏例 |
| `sparse` formal | 约 0.464350 | 约 0.900637 | 中间偏差 |
| `row` formal | 约 0.473580 | 约 0.925713 | 中间偏差 |
| `random2` formal | 约 0.491222 | 约 0.974892 | 接近 0.5 但仍低于高质量组 |
| `far` formal | 约 0.491508 | 约 0.975703 | 轻中度偏差 |
| `checker` formal | 约 0.499929 | 约 0.999796 | 高质量 |
| `same_column` formal | 约 0.499930 | 约 0.999799 | p1 好但 runs/adjacent 异常 |
| `cross_region` formal valid run | 约 0.499944 | 约 0.999839 | 高质量 |
| `compact` formal | 约 0.499948 | 约 0.999850 | 高质量 |
| `random3` formal | 0.499968565 | 0.999909299 | 当前稳定好例 |
| `original_fpga1` formal | 0.500035894 | 0.999896436 | 原始工程 baseline，表现较好 |

正文应避免写成“某一类 placement 必然好/坏”。更稳妥的说法是：在当前矩阵中，不同 placement 实例形成从严重偏置到接近理想的连续分层。

### 6.2 random1/random3 强对照

`random1` 与 `random3` 是当前论文最有力的对照样本。可写作：

> `random1` 与 `random3` 同属 random placement 类别，却在 raw bitstream 上呈现相反表现。`random1` 在 formal 和 repeat 中均保持约 0.337 的 p1，而 `random3` 在 formal 和 repeat 中均接近 0.5。这说明 coarse placement label 不能作为 raw entropy 质量的充分解释变量；实际 RO 坐标、routing、频率关系、sample relation 与多源动态相互作用需要被进一步量化。

### 6.3 Repeat 支持趋势可重复

可写入正文的 repeat 结论：

| placement | formal p1 / bit min-entropy | repeat p1 / bit min-entropy | 结论 |
| --- | --- | --- | --- |
| `random1` | 0.337315512 / 0.593605945 | 0.337669373 / 0.594376522 | 严重偏置趋势可重复 |
| `random3` | 0.499968565 / 0.999909299 | 0.499971128 / 0.999916694 | 高质量趋势可重复 |
| `compact` | 约 0.499948 / 0.999850 | 约 0.500059 / 0.999829 | 高质量趋势可重复 |
| `sparse` | 约 0.464350 / 0.900637 | 约 0.464141 / 0.900073 | 中间偏差趋势可重复 |
| `original_fpga1` | 0.500035894 / 0.999896436 | 0.500216961 / 0.999374119 | baseline 表现较好 |

边界：当前 repeat 次数仍有限，不能写成“已完成稳定性充分证明”。

### 6.4 same_column 说明单指标不足

`same_column` 的 p1 与 bit min-entropy 接近理想，但 runs p-value 为 0，adjacent-equal ratio 约为 `0.50598`。这可作为正文中“单指标不足”的关键例子：

> `same_column` 表明 bit balance 不是 raw entropy 健康程度的充分条件。即使 p1 接近 0.5，序列仍可能存在相邻相关或 runs 异常。因此本文同时报告 bit-level、byte-level 和序列结构指标。

### 6.5 TDC pair 是负结果

TDC pair 结果必须作为负结果写清楚：

> 6 个重点 pair-specific TDC run 共 96 个窗口均未触发 conservative strong-lock 标志，最大 small-lag 绝对相关约为 `0.0317827`。因此，在当前测量条件和已选 pair 上，未检测到强 pair-level phase locking。该结果不支持把 random1 的退化直接归因为某个被测 RO pair 的强锁定，也不能排除弱耦合、多源动态相互作用、sample relation、routing 或供电扰动等更复杂机制。

不能写：

- “TDC 证明 random1 是由强锁定导致。”
- “TDC 证明不存在耦合。”
- “near/far 或 pair TDC 已经完整解释 random1/random3 的熵差异。”

## 7. 机制讨论

当前机制部分应写为“可检验假设与已排除的简单解释”，而不是“已证明机制”。

### 7.1 已有机制线索

当前支持的线索包括：

1. Placement 会改变 raw bitstream 的统计质量，并且该差异在关键样本 repeat 中方向一致。
2. RO_FREQ 显示 all-on 操作存在可测频率 pulling，说明多 RO 同时运行时并非完全独立的静态频率源。
3. TDC pair 未检测到强 pair-level phase locking，说明“单个被测近邻 pair 强锁定”不是当前数据支持的主解释。

### 7.2 更稳妥的机制表述

建议正文写成：

> 当前数据更支持一种 placement-dependent dynamic interaction 的解释框架：placement 可能通过局部布线延迟、频率分布、all-on pulling、采样相位覆盖、routing/coupling 和序列相关结构共同影响 raw output。当前证据尚不能把该框架收敛到单一物理原因。

### 7.3 可检验假设

H1：不同 placement 改变 data RO 与 sample RO 的频率差和 beat relation，使采样边沿长期覆盖到不同相位区域。

状态：部分有 RO_FREQ 线索，但仍需更系统的 data-vs-sample frequency/TDC evidence。

H2：多 RO all-on operation 引入 frequency pulling 或动态扰动，影响 XOR/sample 组合后的 bit bias 和 byte-level distribution。

状态：RO_FREQ 已显示 pulling 存在，但与 entropy 指标的因果关系仍需更强关联分析。

H3：强 pair-level phase locking 不是当前 random1/random3 差异的主要解释。

状态：当前 6 个 TDC pair 未检测到 strong-lock，是负结果；但只能限定在当前 pair、采样长度、温压和分析阈值下。

H4：coarse placement label 不足以解释 raw entropy，需要实际坐标、pair distance、routing、frequency、phase 和 sample relation 联合建模。

状态：已有 random1/random3 强对照支持该判断，但具体模型仍待补充。

## 8. 相关工作与定位

论文定位应避免把“手动 placement”包装成全新的 TRNG 单元。更稳妥的定位是：

1. 传统 RO-TRNG 工作多关注新型 RO/TERO/SR/LRO/FiGaRO 结构、XOR/采样/后处理或标准测试结果；本文关注固定或近似固定结构下 placement 作为自变量导致的 raw entropy 变化。
2. 已有 injection locking/coupling 文献提示 RO-TRNG 可能受注入锁定、供电扰动、frequency pulling 或 oscillator interaction 影响；本文把这些解释拆成可测假设，并报告当前 pair-specific TDC 未检测到强锁定的负结果。
3. 本文强调 raw entropy characterization 与 SP800-90B 合规评估的区别。NIST SP 800-90B 是后续必须对齐的标准，当前 quick bit min-entropy 不能替代 90B entropy estimate。

可引用方向包括：

- NIST SP 800-90B, Recommendation for the Entropy Sources Used for Random Bit Generation.
- Markettos and Moore, CHES 2009, frequency injection attack on RO-based TRNGs.
- 关于 FPGA RO interaction、frequency dispersion、placement/routing sensitivity、FiGaRO 或 device-dependent behavior 的相关工作。

## 9. 限制

本文当前限制必须在正文或结论前明确写出：

1. 当前实验集中在单板、当前 FPGA 型号、当前 RTL、当前采集流程和常温标称电压条件下，不能直接推广到所有 FPGA、所有板卡、所有 Vivado seed 或所有 PVT 条件。
2. 当前主结果是 raw bitstream 统计和机制诊断，不是完整 SP800-90B 熵源认证。
3. 多数 placement 的 formal capture 仍以单个 10MiB run 为主，repeat 次数有限，尚不能给出充分置信区间、方差模型或跨条件统计显著性。
4. TDC pair 结果是负结果，但仅覆盖 6 个重点 pair 和当前窗口设置；它不能排除未测 pair、弱耦合、低频扰动、供电噪声或采样路径效应。
5. TDC bin 未完成更严格的 code-density calibration 时，不应把所有 bin-derived 时间量写成绝对线性时间证据。
6. 当前机制解释仍是“受证据约束的假设框架”，不是完整因果模型。

## 10. 下一步

建议优先级如下：

1. **完成 SP800-90B 工具链。** 安装或配置可用 `g++`、`make/mingw32-make` 与链接环境，至少先跑 `random1`、`random3`、`original_fpga1` 的 non-IID smoke，再扩展到 formal 全集。
2. **扩展关键 placement repeat。** 优先增加 `random1`、`random3`、`compact`、`sparse`、`same_column`、`original_fpga1` 的 repeat，而不是盲目扩大所有 placement。
3. **补充 random1/random3 的 RO_FREQ 重复与关联分析。** 重点输出 all-on vs single-on shift、data/sample beat ranking、frequency pulling 与 raw entropy 指标的相关图。
4. **补充 sample relation 测量。** 当前 pair TDC 主要约束 data-data pair locking，后续需要 data RO vs sample RO 的 frequency/TDC evidence。
5. **整理 placement map 与坐标特征。** 从 XDC/metadata 提取实际坐标、pair distance、region、routing 相关可观测特征，把 coarse label 转换为可解释变量。
6. **按投稿目标决定是否补多板、温度、电压与 restart 数据。** 若冲击更高水平安全/硬件 venue，这些扩展将决定结论外推范围。

## 11. 不应写入主结论的表述

以下表述风险过高，当前不应写入摘要、贡献或结论：

1. “random1 的失败已经由 TDC 证明是强耦合/强锁定导致。”
2. “TDC 证明不存在 coupling 或 locking。”
3. “某类 placement 必然好或必然坏。”
4. “当前数据已经通过 SP800-90B 或完成熵源认证。”
5. “当前结果可直接推广到所有 FPGA、所有板卡、所有 Vivado seed 或所有 PVT 条件。”
6. “bit min-entropy 就是 90B min-entropy estimate。”
7. “near/far 或 pair TDC 已经建立 placement 与 TRNG 质量之间的完整因果关系。”

## 12. 结论草稿

本文在同一 FPGA、相同 RO-TRNG RTL 和统一采集链路下，对多种 RO placement 的 raw output、repeat behavior、RO frequency 和 TDC pair dynamics 进行了表征。当前结果显示，placement 是影响 FPGA RO-TRNG 原始随机性的关键工程变量：不同 placement 可使 raw bitstream 从接近理想到严重偏置，并且该差异在 `random1`、`random3` 等关键样本上具有 repeat 方向一致性。

`random1` 与 `random3` 的强对照说明，coarse placement label 不足以预测 raw entropy，实际坐标、routing、频率分布、采样相位关系和多 RO 动态相互作用需要被纳入诊断流程。`same_column` 进一步表明，仅依赖 p1 或 bit min-entropy 会遗漏序列结构异常，raw TRNG 评估应同时报告 bias、min-entropy、runs、adjacent correlation 和 byte-level 指标。

机制方面，RO_FREQ 结果表明 all-on operation 会引入可测频率 pulling；但 6 个重点 TDC pair 在 96 个窗口中未检测到 conservative strong-lock。因此，当前证据不支持把随机性退化简单归因于单个 RO pair 的强相位锁定。更稳妥的解释是 placement-dependent dynamic interaction 可能通过频率、采样相位、弱耦合、routing 和序列结构共同影响 raw output。SP800-90B 评估、跨 PVT/跨板卡验证和更系统的机制测量仍是后续必须完成的工作。

## 13. 本稿依据的材料

- `doc/paper_draft_cn_20260513.md`
- `doc/paper_results_after_tdc_pairs_utf8_20260514.md`
- `doc/literature_gap_map_20260514.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`
- `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`
- `data/experiments/paper_artifacts_20260514/table_ro_freq_pulling_summary.md`
- `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`

本文档未执行 Vivado、JTAG、COM3、hw_server 或任何新的硬件采集操作。
