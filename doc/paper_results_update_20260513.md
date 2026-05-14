# RO_TRNG 论文结果更新与图表清单（2026-05-13）

本文档仅基于现有文档和只读数据汇总整理，未执行 COM3、JTAG、`hw_server`、Vivado 或任何硬件采集操作。本文档目标是把当前可以写进论文的结果段落、repeat evidence、图表清单和禁止过度声称的句子集中到一处，并严格区分已有证据与待补证据。

## 1. 证据边界

### 已有证据

- 10MiB formal TRNG 主结果：`data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md` 与 `.csv`。
- complete formal/repeat 汇总：`data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.md` 与 `trng_repeats_by_placement.md`。
- 当前 repeat 汇总中已有 8 个 placement 的 5MiB repeat：`random1`、`random2`、`random3`、`compact`、`sparse`、`row`、`far`、`checker`。
- TDC near/far baseline 的表述来自 `doc/paper_draft_cn_20260513.md`、`doc/paper_story_and_figures_20260513.md`，数据源指向 `data/hardware/20260511_fpga1_board1/tdc/tdc_near_far_compare.csv`。
- 论文叙事与边界来自 `doc/experiment_execution_status_20260513.md`、`doc/paper_draft_cn_20260513.md`、`doc/paper_story_and_figures_20260513.md`。

### 待补证据

- `random1/random3` 对应真实 placement 的 RO frequency、beat-frequency、TDC pair 或 sample relation 机制测量。
- 每个 placement 的多次 repeat 均值、标准差、误差条、置信区间或统计显著性。
- SP800-90B / NIST STS 标准口径测试。
- 温度、电压、时间漂移、跨板卡、跨 FPGA 型号、跨 Vivado seed 的泛化验证。
- `cross_region` 和 `same_column` 的 complete 5MiB repeat 尚未出现在当前 repeat 汇总表中，因此不能引用为已完成 repeat evidence。

### 不能用于主结论的数据

- `tdc_near_run01`：TDC packet/framing/seq gap 问题，不能作为正式 TDC 结果。
- `cross_region_run01`：partial capture，formal 主结果必须使用 `cross_region_run02`。
- `random1_run02_partial_timeout_8692840.bin`：partial timeout，只能作为采集故障记录。
- 任何未出现在 `trng_repeats_by_run.md` / `trng_repeats_by_placement.md` complete 汇总中的 repeat 文件，不进入论文 repeat 证据表。

## 2. 当前可写进论文的结果段落

### 2.1 Placement 导致 raw entropy 显著分层

在相同 FPGA、相同 RTL 和统一采集流程下，不同 RO placement 的 10MiB formal raw bitstream 呈现出显著质量分层。最强负例是 `random1_run01`，其 `p1=0.337315512`，`bit_min_entropy=0.593605945`，`adjacent_equal_ratio=0.556739754`，`byte_min_entropy=4.80160868`，说明该 placement 下 raw bitstream 存在严重 bit bias 和相邻 bit 相关性偏高。与之相对，`random3_run01` 在同属 random placement 粗标签下达到当前最好的 bit-level 指标，`p1=0.499968565`，`bit_min_entropy=0.999909299`，`adjacent_equal_ratio=0.500072473`，`byte_min_entropy=7.9845501`。这组对照说明，粗粒度的 placement 类别标签不足以预测 RO-TRNG 的 raw entropy；实际坐标、路由、RO 频率、相位关系和耦合环境仍需进一步量化。

除 `random1/random3` 的强对照外，formal 结果还显示出连续的质量梯度。`compact_run01`、`checker_run01`、`cross_region_run02` 与 `random3_run01` 构成高质量组，其 `p1` 接近 0.5、bit min-entropy 接近 1，且 adjacent equal ratio 接近 0.5；`sparse_run01`、`row_run01`、`far_run01` 与 `random2_run01` 构成中间梯度组，其 bit bias 和 min-entropy 退化程度低于 `random1_run01`，但仍可与高质量组区分。该结果支持“placement 是 raw TRNG 质量核心变量之一”的论文主线，但尚不能推出某类 placement 必然好或必然坏。

### 2.2 单指标不足以评估 raw stream 健康程度

`same_column_run01` 是当前结果中最适合说明单指标风险的样本。它的 bit balance 指标接近理想，`p1=0.499930251`，`bit_min_entropy=0.99979876`，但 `runs_p=0`，`adjacent_equal_ratio=0.505979735`，`byte_min_entropy=7.86432277`。因此，论文中不能只报告 p1 或 bit min-entropy，而应同时报告 runs、adjacent equal ratio、byte-level entropy 等指标。这个样本可以放在“多指标评估必要性”段落中，用来说明 bit balance 好不等价于 raw stream 完全健康。

### 2.3 5MiB repeat 提供趋势可重复的初步证据

当前 repeat 证据应写成“趋势可重复”而不是“统计显著性已经充分”。`trng_repeats_by_placement.md` 中已有 8 个 placement 的 complete 5MiB repeat。repeat 与 formal 的方向一致：严重失败样本 `random1` 在 repeat 中仍然严重偏置；高质量样本 `random3`、`compact`、`checker` 在 repeat 中仍接近理想；中间梯度样本 `sparse`、`row`、`far`、`random2` 在 repeat 中仍保持相近偏差水平。这支持主要现象不是一次性采集偶然事件，但每个 placement 当前仍只有一个 formal 和一个 repeat，不能写强置信区间、显著性检验或长期稳定性结论。

### 2.4 TDC baseline 只能说明测量链路可用

当前 TDC near/far 数据应作为 measurement baseline，而不是 `random1/random3` 质量差异的因果解释。已有文档给出 `tdc_near_run02` 与 `tdc_far_run01` 的有效 packets 均约 262k，`diff_std_ps` 约 1.92 ns，phase Pearson r 接近 0。该结果可以说明 TDC 采集与分析链路能够产生有效 phase 统计，并为后续机制实验提供方法基础；但由于它们不是 random1/random3 的同位 RO pair 或 sample relation 测量，不能用来证明 random1 的失败由耦合、锁定、频率接近、routing 或电源噪声导致。

## 3. Repeat evidence 可用文字

可直接写入论文的谨慎版本：

> 为避免将 5MiB repeat 与 10MiB formal 主排名混合，本文将 repeat 仅作为重复性补充。当前已有 complete repeat 的 8 个 placement 均表现出与 formal capture 一致的主要趋势：`random1` 在 5MiB repeat 中仍呈现严重偏置，`random3`、`compact` 与 `checker` 仍保持接近理想的 bit balance 与 min-entropy，而 `sparse`、`row`、`far` 与 `random2` 仍处于中间偏差区间。该结果支持 placement-induced raw entropy 差异具有可重复线索，但由于每个 placement 的 repeat 次数仍有限，本文不将其解释为充分的统计显著性或长期稳定性证明。

可用于表格说明的短版本：

> 5MiB repeat02 captures are used as reproducibility checks, not as replacements for the 10MiB formal ranking. The repeated captures preserve the qualitative ordering observed in the formal data, while additional repeats are required for confidence intervals and statistical significance.

### 3.1 Formal 与 repeat 对照摘要

| placement | formal p1 | repeat p1 | formal bit min-entropy | repeat bit min-entropy | 论文读法 |
| --- | ---: | ---: | ---: | ---: | --- |
| `random1` | 0.337315512 | 0.337669373 | 0.593605945 | 0.594376522 | 严重偏置趋势可重复 |
| `random2` | 0.491222239 | 0.491030312 | 0.974892483 | 0.974348355 | 轻中度偏差趋势可重复 |
| `random3` | 0.499968565 | 0.499971128 | 0.999909299 | 0.999916694 | 高质量趋势可重复 |
| `compact` | 0.499947906 | 0.500059223 | 0.999849695 | 0.999829128 | 高质量趋势可重复 |
| `sparse` | 0.464349854 | 0.464140511 | 0.900637067 | 0.900073341 | 中间偏差趋势可重复 |
| `row` | 0.473579586 | 0.473337555 | 0.925712657 | 0.925049507 | 中间偏差趋势可重复 |
| `far` | 0.491507936 | 0.491642475 | 0.975702835 | 0.976084602 | 轻中度偏差趋势可重复 |
| `checker` | 0.499929237 | 0.499947119 | 0.999795837 | 0.999847425 | 高质量趋势可重复 |

## 4. 需要画的图表及数据源路径

| 编号 | 图表 | 目的 | 数据源路径 | 当前证据属性 |
| --- | --- | --- | --- | --- |
| Table 1 | 10MiB formal 主结果表 | 展示所有有效 placement 的 p1、bit min-entropy、runs、adjacent equal ratio、byte min-entropy | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv`，`data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md` | 已有证据，可立即写 |
| Table 2 | formal vs repeat 对照表 | 展示 8 个 complete repeat 与 formal 的方向一致性 | `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.csv`，`data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md` | 已有证据，但 repeat 次数有限 |
| Fig. 1 | bit min-entropy 排序柱状图 | 直观展示 `random1` 极差、中间梯度和高质量组 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv` | 已有证据 |
| Fig. 2 | `abs(p1-0.5)` 排序图 | 展示 bit bias 是 `random1/sparse/row` 等样本的主要退化来源 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv` | 已有证据 |
| Fig. 3 | adjacent equal ratio 偏离 0.5 图 | 突出 `same_column` 和 `random1` 的相邻 bit 相关性问题 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv` | 已有证据 |
| Fig. 4 | byte min-entropy 对照图 | 显示 bit-level 退化是否同步反映到 byte-level 指标 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv` | 已有证据 |
| Fig. 5 | formal vs repeat 散点图 | 用 p1 或 bit min-entropy 展示 repeat 与 formal 的一致性 | `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.csv` 或 `trng_repeats_by_placement.csv` | 已有证据，但只能写趋势一致 |
| Fig. 6 | smoke vs formal 散点图 | 说明 smoke capture 可作为快速筛查线索，formal 仍为主结果 | `data/hardware/20260511_fpga1_board1/hardware_run_audit.csv`，可参考 `data/hardware/20260511_fpga1_board1/trng/trng_smoke_matrix_compare.csv` | 已有证据，需整理 |
| Fig. 7 | TDC near/far baseline 图 | 展示 packets、seq gaps、phase std、diff std、phase Pearson r | `data/hardware/20260511_fpga1_board1/tdc/tdc_near_far_compare.csv` | 已有证据，仅 baseline |
| Fig. 8 | placement map | 把各 placement 的实际 RO 坐标和区域关系可视化 | XDC、placement metadata、Vivado run 路径；需从现有文件整理，不需新硬件 | 待整理证据 |
| Fig. 9 | random1/random3 frequency heatmap | 解释同属 random placement 却一坏一好的候选频率机制 | 后续 RO frequency / beat-frequency measurement | 待补证据 |
| Fig. 10 | random1/random3 TDC pair phase/correlation 图 | 验证 phase diffusion、pairwise correlation、coupling/locking 假设 | 后续对应 TDC pair measurement | 待补证据 |
| Table 3 | SP800-90B / NIST 结果表 | 给出标准口径随机性或熵评估 | 后续标准测试输出 | 待补证据 |

建议正文顺序：先放 Table 1 与 Fig. 1/2 建立主现象，再放 Fig. 3/4 说明多指标必要性，随后放 Table 2 或 Fig. 5 作为 repeat evidence，最后放 TDC baseline 和待补机制图作为“机制验证缺口与下一步”。

## 5. 不能写成定论的句子

以下句子不要写入论文主结论，除非后续补齐对应证据。

| 禁写或需改写的句子 | 为什么不能写成定论 | 建议改写 |
| --- | --- | --- |
| `random1` 的失败已经由 TDC 证明是耦合或锁定导致。 | 当前 TDC near/far 只是 baseline，不对应 `random1/random3` 的真实 RO placement 或 sample relation。 | 当前结果显示 `random1` 失败具有重复性线索，其物理机制需要对应 placement 的 frequency/TDC 测量进一步验证。 |
| random placement 不可靠，compact/checker/cross_region 必然可靠。 | `random1` 与 `random3` 同属 random 粗标签但表现相反；当前每类样本数有限。 | 不同 placement 实例呈现显著差异，粗粒度 placement 标签不足以预测 raw entropy。 |
| 当前数据已经证明某类布局设计准则。 | 仍缺实际坐标量化、RO frequency、phase relation、routing/coupling 指标。 | 当前数据提示 placement 是关键变量，后续需要机制测量将现象转化为设计准则。 |
| 当前结果已经达到标准认证随机性。 | 尚未完成 SP800-90B/NIST 标准测试；当前主要是 raw entropy 和基础统计。 | 当前结果是后处理前 raw entropy 分析，标准随机性评估需要单独报告。 |
| 所有 placement 的统计显著性、方差和置信区间已经充分。 | 当前每个 placement 主要是 1 个 10MiB formal 加有限 repeat，尚不足以形成强统计结论。 | 当前 repeat 支持趋势可重复，更多 repeat 将用于估计方差、误差条和置信区间。 |
| TDC near/far 差异解释了 TRNG 高低质量。 | near/far TDC probe 与 TRNG entropy source 的对应关系尚未建立。 | TDC near/far 只能作为测量链路 baseline，为后续 random1/random3 机制测量提供方法基础。 |
| partial capture 可以补充 formal 排名。 | partial 文件采集规模不完整或 audit 不可用，会破坏 formal 对比公平性。 | formal 主表仅使用 complete、valid、10MiB captures；partial 只作为故障或过程记录。 |
| 当前结论可直接推广到所有 FPGA、所有板卡或所有 Vivado seed。 | 当前实验集中在 FPGA1、当前 RTL、当前采集流程。 | 当前结论限定在本平台与本实验条件下，跨平台泛化需要扩展实验。 |

## 6. 可直接放入论文的谨慎句子

- 在相同 RTL 与采集流程下，不同 RO placement 造成了可观测且在多个关键样本上可重复的 raw entropy 差异。
- `random1` 与 `random3` 构成强对照：二者同属 random placement 粗标签，却分别表现为严重偏置与接近理想。
- 当前 10MiB formal 结果中，bit min-entropy 从 `random1_run01` 的 `0.593605945` 到 `random3_run01` 的 `0.999909299`，体现出明显质量分层。
- `same_column_run01` 说明 p1 和 bit min-entropy 接近理想并不保证 raw stream 在 runs 或相邻 bit 相关性上正常。
- 当前 TDC near/far 结果应解释为 measurement baseline，而不是 `random1/random3` entropy gap 的因果证据。
- 本研究当前建立的是 placement-sensitive raw entropy 现象和重复性线索；完整物理机制仍需 colocated frequency、beat-frequency 和 phase measurements 补证。

## 7. 后续最小补证闭环

1. 对 `random1/random3` 补 RO frequency / beat-frequency：输出 per-RO frequency、pairwise delta-f heatmap、data-vs-sample beat ranking、all-on vs single-on pulling。
2. 对 `random1/random3` 补对应 TDC pair：输出 phase histogram、`diff_std_ps`、`phase_pearson_r`、lag correlation。
3. 对关键 placement 补更多 repeat：至少覆盖 `random1`、`random3`、`compact`、`sparse`、`same_column`，形成均值、标准差和误差条。
4. 跑 SP800-90B / NIST：把 raw entropy 基础统计与标准口径随机性评估分开表述。
5. 整理 placement map：从 XDC/metadata 提取实际坐标、距离、区域关系，为机制解释提供物理布局变量。

## 8. 本文档使用的数据源

- `doc/experiment_execution_status_20260513.md`
- `doc/paper_draft_cn_20260513.md`
- `doc/paper_story_and_figures_20260513.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv`
- `data/hardware/20260511_fpga1_board1/hardware_run_audit.csv`
- `data/hardware/20260511_fpga1_board1/tdc/tdc_near_far_compare.csv`

