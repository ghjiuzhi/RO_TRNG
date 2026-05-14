# RO_TRNG 论文故事线与图表规划（2026-05-13）

本文档是论文写作与图表规划草稿，只基于已有文件和只读分析结果，不包含新的硬件采集、Vivado 运行或串口操作。

## 1. 核心故事线

论文主线可以写成四层递进：

1. **Placement 是 raw TRNG 质量的关键变量。** 在相同 FPGA、相同 RTL/采集流程、标称板级供电条件下，不同 RO placement 产生了显著不同的 raw bit 行为。10MiB 正式数据中，`random1_run01` 的 `p1=0.337316`、`bit_min_entropy=0.593606`，而 `random3_run01` 的 `p1=0.499969`、`bit_min_entropy=0.999909`。
2. **RO 物理行为假设：布局改变了振荡器间耦合、routing 相似性、局部电源/时钟/布线环境和相位关系。** 这些因素可能让两个或多个 RO 的相位差更稳定、采样输出偏向某一值，或让相邻 bit 出现相关性。当前数据支持“placement 影响 raw entropy”，但尚未证明某一个具体物理机制。
3. **Raw entropy 指标给出可重复的质量分层。** 以 10MiB 正式数据为主，bit bias、bit min-entropy、byte entropy、runs p-value 和 adjacent equal ratio 能把 placement 分成极差、高质量和中间梯度，并暴露 `same_column` 这类“balance 很好但相关性异常”的非单指标现象。
4. **TDC/频率/相位测量用于机制验证。** 已有 `tdc_near_run02` 与 `tdc_far_run01` 可作为 near/far baseline：两者有效 packets 接近 262k，phase Pearson r 都接近 0，`diff_std_ps` 约 1.92 ns。但它们还不是 `random1` / `random3` 的对应测量，不能直接解释 random placement 间的巨大差异。下一步需要对 `random1` 与 `random3` 做对应 TDC、RO frequency 或 counter 测量。

一句话版本：**同样是 FPGA RO-TRNG，placement 不只是工程细节，而是 raw entropy 的主要决定因素之一；论文先用正式 raw entropy 数据建立现象，再用 TDC/频率/相位实验收束到物理机制。**

## 2. 现在最强结果

### 2.1 10MiB 正式排名

| 分组 | run | p1 | bit_min_entropy | runs_p | adjacent_equal_ratio | 论文读法 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 极差反例 | `random1_run01` | 0.337316 | 0.593606 | 0 | 0.556740 | 当前最强负例：严重 bit bias，byte entropy 也明显下降 |
| 中间梯度 | `sparse_run01` | 0.464350 | 0.900637 | 0 | 0.506596 | 明显偏置但未像 random1 崩坏 |
| 中间梯度 | `row_run01` | 0.473580 | 0.925713 | 0 | 0.504304 | 偏置较 sparse 轻 |
| 中间梯度 | `random2_run01` | 0.491222 | 0.974892 | 0 | 0.501080 | 接近理想，但 formal 指标仍能看出偏差 |
| 中间梯度 | `far_run01` | 0.491508 | 0.975703 | 0 | 0.500726 | 接近理想，但仍非高质量组 |
| 高质量 | `checker_run01` | 0.499929 | 0.999796 | 0.149267 | 0.500079 | 可作为高质量布局样本 |
| 特殊样本 | `same_column_run01` | 0.499930 | 0.999799 | 0 | 0.505980 | balance 很好，但 runs/相邻相关性异常，不能只看 p1 |
| 高质量 | `cross_region_run02` | 0.499944 | 0.999839 | 0.719841 | 0.499980 | 高质量，正式有效 run 是 run02 |
| 高质量 | `compact_run01` | 0.499948 | 0.999850 | 0.263603 | 0.499939 | 高质量 |
| 高质量 | `random3_run01` | 0.499969 | 0.999909 | 0.184373 | 0.500072 | 当前 10MiB bit min-entropy 最好 |

### 2.2 关键观察

- `random1` 极差：`p1` 约 0.337，`bit_min_entropy` 约 0.594，`adjacent_equal_ratio` 约 0.557，是论文里最有力的失败样本。
- `random3` / `compact` / `cross_region` / `checker` 很好：`p1` 接近 0.5，`bit_min_entropy` 接近 1，且相邻 bit 比例接近 0.5。
- `sparse` / `row` / `far` / `random2` 构成中间梯度：说明 placement 影响不是“好/坏”二元分类，而是连续、多因素的质量变化。
- `same_column` 的 balance 很好，但 `runs_p=0`、`adjacent_equal_ratio=0.505980`，提示 raw TRNG 不能只用 p1 或 bit min-entropy 判断。
- smoke 与 formal 对比很有价值：例如 `random1_smoke01` 的 `p1=0.338280` 与 `random1_run01` 的 `p1=0.337316` 一致；`random3_smoke01` 与 `random3_run01` 也都接近理想。这可以支持 smoke run 作为快速筛查，但 formal 10MiB 仍是论文主结果。
- 已有 5MiB repeat02 对核心样本给出初步重复性线索：`random1_repeat02_5mib` 仍极差（`p1=0.337669`，`bit_min_entropy=0.594377`），`random3_repeat02_5mib` 与 `compact_repeat02_5mib` 仍很好，`sparse_repeat02_5mib` 仍处于中间偏差区。repeat 目前适合写成重复性补充，不应混入 10MiB 主排名。

## 3. 暂定题目、摘要与贡献

### 3.1 暂定题目

**面向 FPGA RO-TRNG 的布局敏感性实测分析：从 raw entropy 分层到相位机制验证**

备选英文题目：

**Placement-Sensitive Raw Entropy in FPGA Ring-Oscillator TRNGs: Empirical Stratification and Phase-Oriented Mechanism Validation**

### 3.2 摘要草稿

环形振荡器真随机数发生器（RO-TRNG）常被视为易于在 FPGA 上部署的轻量熵源，但其 raw entropy 可能强烈依赖物理布局与布线环境。本文在同一 FPGA 平台、相同 RTL 与采集流程下，对多种 RO placement 进行 10MiB raw bit 采集与统计分析。结果显示，不同 placement 的 raw bit 质量存在数量级差异：一个 random placement 出现严重偏置（`p1=0.337316`，bit min-entropy 为 `0.593606`），而另一个 random placement 以及 compact、cross-region、checker placement 接近理想随机比特流。中间梯度样本和 `same_column` 样本进一步说明，单纯的布局类别标签不足以预测熵质量，且 bit balance 良好并不保证相邻 bit 相关性正常。本文进一步使用 TDC near/far baseline 和后续计划中的 random1/random3 对应测量，将 raw entropy 现象与 RO 频率、相位差和耦合机制联系起来。该研究为 FPGA RO-TRNG 的布局约束、快速筛查和后处理前 raw entropy 评估提供了实测依据。

### 3.3 贡献点

1. 构建一组可对比的 FPGA RO-TRNG placement 实测数据，覆盖 random、compact、sparse、row、far、checker、same-column、cross-region 等布局。
2. 用 10MiB formal raw bit 指标展示 placement 对 bit bias、bit min-entropy、byte entropy 和相邻 bit 相关性的显著影响。
3. 揭示同属 random placement 的 `random1` 与 `random3` 可分别表现为严重失败和接近理想，说明粗粒度 placement 标签不足以解释熵质量。
4. 提出多指标评估路径：除 p1 与 bit min-entropy 外，引入 runs、adjacent equal ratio、byte entropy 与 smoke-vs-formal 一致性，避免单指标误判。
5. 设计 TDC/频率/相位机制验证闭环，将统计现象推进到可检验的物理解释。

## 4. 图表清单

| 编号 | 图表 | 数据源 | 目的 | 当前状态 |
| --- | --- | --- | --- | --- |
| Table 1 | 10MiB formal 主结果表 | `trng_formal_all_10mib_ranked.csv/md` | 展示所有 placement 的 p1、bit min-entropy、runs、adjacent equal ratio、byte entropy | 现在能画/能写 |
| Fig. 1 | `bit_min_entropy` 排序柱状图 | `trng_formal_all_10mib_ranked.csv` | 直观显示 random1 极差、中间梯度、高质量组 | 现在能画 |
| Fig. 2 | `abs(p1-0.5)` 排序图 | `trng_formal_all_10mib_ranked.csv` | 强调 bit bias 是 random1/sparse/row 的主要问题 | 现在能画 |
| Fig. 3 | `adjacent_equal_ratio` 偏离 0.5 图 | `trng_formal_all_10mib_ranked.csv` | 突出 same_column 的相关性异常和 random1 的相邻重复偏高 | 现在能画 |
| Fig. 4 | smoke-vs-formal 散点图 | `hardware_run_audit.csv` | 验证 1MiB smoke 对 10MiB formal 的快速筛查价值 | 现在能画 |
| Fig. 5 | placement map | XDC / placement metadata / bitstream run 路径 | 把 compact、sparse、row、far、checker、random、same_column、cross_region 放到器件坐标上 | 需要从现有 placement 文件整理坐标，不需要新硬件 |
| Fig. 6 | TDC near/far baseline 图 | `tdc_near_far_compare.csv` / audit | 展示 near/far 的 packets、seq gaps、phase std、phase correlation | 现在能画，但只能作为 baseline |
| Fig. 7 | random1 vs random3 TDC 机制图 | 后续对应 TDC 或频率/counter 测量 | 解释同为 random placement 却一坏一好的物理机制 | 未来关键图 |

建议图表顺序：先用 Table 1 和 Fig. 1/2 建立现象，再用 Fig. 3 打破“只看 balance”的直觉，接着用 Fig. 4 说明筛查流程可靠性，最后用 placement map 与 TDC 图导向机制解释。

## 5. 现在能写的边界

### 5.1 现在能写

- 在当前 FPGA1、当前 RTL 和标称板级供电条件下，RO placement 会显著影响 raw TRNG 的统计质量。
- `random1_run01` 是明确的失败样本，`random3_run01`、`compact_run01`、`cross_region_run02`、`checker_run01` 是明确的高质量样本。
- `sparse_run01`、`row_run01`、`far_run01`、`random2_run01` 呈现中间梯度，支持“placement 影响是连续、多因素”的叙事。
- `same_column_run01` 证明 p1/bit min-entropy 接近理想不等价于 raw stream 完全健康，runs 与相邻 bit 指标必须同时报告。
- smoke 与 formal 指标在多个样本上方向一致，可以作为快速预筛流程，但最终结论以 formal 10MiB 为准。
- 已有 near/far TDC baseline 显示当前 TDC 采集链路可获得有效 packets 与 phase 统计，并可作为后续机制验证的方法基础。

### 5.2 不能过度声称

- 不能说 `random1` 的失败已经由 TDC 相位锁定、频率接近、routing 耦合或电源噪声机制证明；当前还缺 `random1` / `random3` 对应的机制测量。
- 不能把 `tdc_near_run02` 与 `tdc_far_run01` 直接解释成 TRNG 高低质量的因果证据；它们是 near/far baseline，不是 random1/random3 的同位对照。
- 不能把 partial 或 invalid 数据当作 formal 结果。`tdc_near_run01` 因 packet/framing/seq gap 问题无效；`cross_region` formal 应使用 `cross_region_run02`。
- 不能宣称某一种布局类别必然好或必然坏。`random1` 与 `random3` 的对比恰好说明同一粗标签内部也可能差异巨大。
- 不能声称已经达到标准认证随机性。当前是 raw entropy 与基础统计分析，SP800-90B/NIST 仍需单独跑并按标准口径解释。

## 6. 下一步最少实验闭环

1. **repeat 统计收敛。** 将已完成的 5MiB repeat02 纳入重复性补充表，并至少对 `random1`、`random3`、`compact`、`sparse` 给出 run01 vs repeat02 的 p1、bit min-entropy、adjacent equal ratio 对照；如时间允许，再补 `same_column` repeat 以确认 runs/相关性异常是否稳定。
2. **random1/random3 机制对照。** 对 `random1` 与 `random3` 对应 placement 做 TDC、RO frequency 或 counter 测量，优先得到可与 raw entropy 一一对应的频率差、相位差扩散、phase correlation 或锁相/准锁相证据。
3. **SP800-90B / NIST。** 在 raw 数据保存和 metadata 完整的基础上，对主结果样本跑 SP800-90B 熵估计与 NIST STS。论文中要区分 raw entropy 指标、标准测试结果和经后处理输出结果。
4. **图表落地。** 先完成 Table 1、Fig. 1-4 和 Fig. 6；placement map 与 random1/random3 机制图随着坐标整理和新机制测量补齐。

最小可投稿闭环是：**10MiB formal 主结果 + 核心 repeat 一致性 + random1/random3 机制测量 + SP800-90B/NIST 标准口径**。如果缺机制测量，论文仍可写成 placement sensitivity 实测短文；如果补上机制图，则故事会从“现象观察”升级为“可解释的设计准则”。

## 7. 数据来源

- `doc\experiment_execution_status_20260513.md`
- `data\hardware\20260511_fpga1_board1\trng\trng_formal_all_10mib_ranked.md`
- `data\hardware\20260511_fpga1_board1\trng\trng_formal_all_10mib_ranked.csv`
- `data\hardware\20260511_fpga1_board1\hardware_run_audit.md`
- `data\hardware\20260511_fpga1_board1\hardware_run_audit.csv`
- `data\hardware\20260511_fpga1_board1\tdc\tdc_near_far_compare.csv`
- 只读参考：`random1_repeat02_5mib`、`random3_repeat02_5mib`、`compact_repeat02_5mib`、`sparse_repeat02_5mib` 的 `trng_summary.csv`
