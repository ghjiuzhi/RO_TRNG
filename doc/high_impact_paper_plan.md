# RO-TRNG 顶刊论文与实验管理计划

更新时间：2026-05-10

本文档只管理论文叙事、实验矩阵、数据规范和下周执行路径，不修改 RTL。当前项目已有的 RTL、Vivado 工程、数据和脚本视为共同工作区资产；任何实验复现都应新增产物目录并保留原始记录。

## 一句话目标

把“基于 FPGA 反相器/LUT 环形振荡器的 TRNG”从常规随机性测试文章，推进为一篇解释物理机制、可复现实验方法和设计规则的高影响力论文：

> FPGA RO-TRNG 的安全熵不是由 RO 数量或频率差单独决定，而是由布局、路由、邻近开关活动、采样相位扩散和在线健康测试共同决定；通过布局感知的 TDC 诊断与统计认证，可以提前发现随机性测试难以解释的熵退化机制，并给出可复现的设计准则。

## 顶刊核心 Claim

### 主 Claim

本文提出并验证一种“布局-耦合-相位扩散-熵质量”的 RO-TRNG 评价框架。该框架将 FPGA 物理布局和邻近活动映射到 RO 频率、抖动、相位相关、健康测试触发率和 SP800-90B 熵估计，证明传统只看 NIST STS 通过率或只比较 RO 个数的实验不足以支撑高安全性结论。

### 可投稿级贡献点

1. **机制贡献**：把 RO-TRNG 的熵退化解释为可观测的物理时序现象，包括共模耦合、相位锁定倾向、确定性拍频和采样边界附近的相位扩散不足。
2. **测量贡献**：构建轻量级 CARRY4 TDC 诊断链路，直接采集 RO 相位分布、bin histogram、bubble 标志和粗细时间戳，而不是只观察最终 bitstream。
3. **数据贡献**：形成跨布局、RO 数量、选择结构、邻近 aggressor、环境条件和 Vivado seed 的公开式实验矩阵。
4. **方法贡献**：提出布局感知的 RO 选择/约束规则，将频率分离、TDC 相位扩散、pairwise correlation、在线健康测试稳定性和 SP800-90B min-entropy 合成评价。
5. **工程贡献**：给出 Zynq-7020 FPGA 上的复现流程、数据命名规范、图表模板和审稿可追溯证据链。

### 不应夸大的 Claim

- 不声称当前版本已经达到商用 TRNG 认证。
- 不把简单 inverter/LUT RO 结构本身包装为新架构。
- 不用 UART 抓取速率作为吞吐率 claim。
- 不只用 NIST STS 通过率证明安全熵。
- 不把单板单温度结果泛化为跨 FPGA 家族结论。

## 当前已有结果如何支撑

### 已有硬件与脚本基础

| 类别 | 已有资产 | 对论文的作用 |
| --- | --- | --- |
| 基线 TRNG RTL | `rtl/RO_TRNG_top.v`, `rtl/entropy_source.v` | 提供原始 RO-TRNG 输出链路 |
| RO 计数/抖动测量 | `rtl/jitter_measure.v`, `rtl/CU.v`, `rtl/counter.v` | 支撑频率、count variance、jitter 估计 |
| TDC 诊断 RTL | `rtl/tdc/*` | 支撑相位分布和 bubble 观察 |
| 板级工程 | `fpga1/xc7z020clg400` | Zynq-7020 实验平台 |
| 分析脚本 | `scripts/analyze_ro_counter.py`, `scripts/analyze_trng_dataset.py`, `scripts/analyze_tdc_uart.py` | 支撑快速筛查和图表生产 |
| 实验计划 | `doc/ro_tdc_layout_experiment_plan.md`, `doc/fpga1_lab_runbook.md` | 已定义 E0/E1/TDC 路径 |

### 已有数据的论文价值

| 数据来源 | 已观察现象 | 可支撑的叙事 |
| --- | --- | --- |
| `data/experiments/e0_lut_ro_counter.csv` | RO2 到 RO9 频率约 286.9 MHz 到 1061.2 MHz，jitter_std_ps 约 3.74 ps 到 8.43 ps，count min-entropy 差异明显 | 同一 FPGA 上不同 RO 的频率和时序噪声差异显著，不能只按 RO 数量建模 |
| `data/experiments/e1_sim_top/trng_summary.md` | `7sel_1sro7.DAT`、`8sel_1sro8.DAT` 等接近 p1=0.5，byte entropy 接近 8；`2fro2_1sro9.DAT` p1=0.61675 且 monobit/runs 失败 | 存在“同类结构下质量强烈分化”的现象，适合引出布局/采样/耦合机制 |
| `data/experiments/e1_sel_ro/trng_summary.md` | 16/32/42/56/64/128 mux 组总体较好，2/4/8 mux 部分样本 runs 失败或 byte min-entropy 较低 | RO 选择规模和组合结构会影响相关性与序列结构，不能只看 bit bias |
| `data/zynq7020_compare_20260415/result/summary.txt` | RO2-RO9 单 RO 数据 p1 偏离明显，byte entropy 约 0.83 到 1.49 | 单 RO 直接输出不可靠，可作为负例和 entropy source 设计动机 |
| `data/zynq7020_compare_20260420_xdat/result/summary.txt` | XDat 抓取 p1 从 0.389 到 0.517，byte min-entropy 从 3.40 到 6.57 不等 | 板级抓取条件对输出质量影响大，需要严谨 metadata 和重复实验 |
| `data/zynq7020_compare_* /fig/*.png` | 已有 p1、Shannon entropy、min-entropy 图 | 可作为论文早期 Figure 1/2 草图，但需升级成可投稿图 |

### 当前证据链缺口

- 现有结果多为筛查统计，尚不是正式 SP800-90B 和 NIST STS 认证级证据。
- 缺少严格的 metadata：bitstream hash、Vivado seed、XDC、温度、电压、板卡编号、采集命令、数据长度。
- 缺少跨 seed、跨布局、跨温度、跨 aggressor 的重复性。
- 缺少 TDC 相位证据与最终 bitstream 熵质量之间的定量关联。
- 缺少与主流 RO-TRNG 文献的公平 baseline 对照表。

## 实验矩阵

实验分成“筛查层、物理机制层、认证层、鲁棒性层”。顶刊论文至少要完成 E0-E6；E7 作为加分项。

| 编号 | 实验 | 自变量 | 固定条件 | 输出指标 | 最低样本量 | 论文用途 |
| --- | --- | --- | --- | --- | --- | --- |
| E0 | 单 RO counter 基线 | RO index, window_ns | 同板同温同电压 | freq, count variance, jitter_std_ps, count entropy | 每 RO 50k windows | 证明 RO 物理差异 |
| E1 | 已有 bitstream 筛查 | RO 组合、mux 规模、历史配置 | 使用现有数据 | p1, monobit_p, runs_p, byte entropy, min-entropy | 每配置现有全量 | 找正例/负例 |
| E2 | 布局模式 sweep | compact, row, checker, far-apart, random | 相同 RTL、RO 数、采样率、seed 记录 | raw entropy, STS, 90B, correlation | 每配置 >= 10 MB raw | 验证布局影响 |
| E3 | Vivado seed sweep | seed 1-10 | 同一 XDC 模式 | 频率漂移、熵稳定性、失败率 | 每 seed >= 5 MB raw | 排除工具偶然性 |
| E4 | 邻近 aggressor sweep | idle, low toggle, high toggle, PRBS toggle；near/far | 同 bitstream family | TDC phase collapse, correlation, min-entropy, health fail rate | 每模式 >= 10 MB raw + 100k TDC packets | 验证耦合机制 |
| E5 | TDC 相位诊断 | RO lane, layout, aggressor, temperature | CARRY4 chain 固定约束 | bin histogram, bubble rate, phase diffusion, pair correlation | 每配置 >= 100k packets | 建立物理解释 |
| E6 | 正式随机性认证 | 代表性好/坏/中等配置 | 原始数据不后处理或明确后处理 | SP800-90B IID/non-IID, NIST STS, AIS31 可选 | 每配置 >= 1 Mbit，建议 >= 100 MB | 支撑安全 claim |
| E7 | 环境鲁棒性 | temperature, voltage | 选 3 个代表布局 | entropy drift, health-test margin | 每点 >= 5 MB raw | 加强顶刊说服力 |

### 对照组设计

| 对照 | 目的 | 必须记录 |
| --- | --- | --- |
| 单 RO 直接输出 | 展示未经组合的弱随机源 | RO index, counter window, p1, entropy |
| 现有好样本 | 作为当前最佳基线 | 原始文件名、分析脚本版本 |
| 现有坏样本 | 用作熵退化案例 | 失败测试项和推测原因 |
| compact vs far-apart | 直接测试布局间距 | XDC 坐标、BEL、Pblock |
| aggressor near vs far | 分离局部耦合和全局噪声 | aggressor 坐标、toggle rate |
| 同 XDC 不同 seed | 评估工具路由扰动 | Vivado seed、route status、timing report |

## 审稿风险与应对

| 风险 | 审稿人可能质疑 | 应对证据 |
| --- | --- | --- |
| 题材成熟 | “RO-TRNG 已有大量工作，创新在哪里？” | 强调布局/耦合/TDC 机制证据和可复现实验方法，而非简单 RO 架构 |
| 数据不足 | “单板单次采样不具统计意义” | 加入 seed、布局、温度、电压和重复采样矩阵 |
| 只做 NIST | “NIST STS 不能证明 entropy” | 必做 SP800-90B IID/non-IID；NIST 只作为补充 |
| 后处理不清 | “随机性来自后处理而非 entropy source” | 分开报告 raw source、conditioning 后和 health-test 后结果 |
| UART 采集限制 | “吞吐率和数据完整性不可信” | UART 只用于 characterization；记录丢包检测、frame sync 和 capture hash |
| TDC 校准不足 | “TDC bin 宽不均会误导” | 固定 CARRY4 placement，报告 code density 校准或至少报告 bin occupancy 非均匀性 |
| 布局不可复现 | “手工布局依赖工具或器件” | 发布 XDC、Vivado 版本、seed、device part、bitstream hash |
| 环境干扰 | “温度/电压/外部噪声导致结果” | 记录环境条件，做短时间重复与跨条件对照 |
| Claim 过宽 | “结果只适用于 Zynq-7020” | 明确 scope：Zynq-7020 实证；跨器件作为未来工作或补充实验 |
| 文献对比弱 | “没有和最新 RO-TRNG/TDC-TRNG 比较” | 建立表格：器件、entropy estimate、throughput、area、health tests、是否有物理机制验证 |

## 数据命名规范

### 目录结构

建议所有新实验放入：

```text
data/paper_runs/
  YYYYMMDD_<board>_<experiment_id>_<short_tag>/
    raw/
    processed/
    fig/
    reports/
    metadata/
```

示例：

```text
data/paper_runs/20260510_z7020_E2_layout_compact/
```

### 原始数据文件名

统一格式：

```text
<date>_<board>_<exp>_<config>_<seed>_<tempC>_<volt>_<capture>.<ext>
```

示例：

```text
20260510_z7020_E2_compact_s03_25C_nom_cap01.bin
20260510_z7020_E5_tdc_checker_s07_25C_nom_cap02.bin
20260510_z7020_E4_aggrNearPrbs_s05_35C_nom_cap01.bin
```

字段约定：

| 字段 | 示例 | 说明 |
| --- | --- | --- |
| date | `20260510` | 采集日期 |
| board | `z7020b01` | 板卡编号，不只写 FPGA 型号 |
| exp | `E2` | 对应实验矩阵编号 |
| config | `compact`, `checker`, `far`, `aggrNearPrbs` | 关键配置 |
| seed | `s03` | Vivado seed |
| tempC | `25C`, `35C`, `unkC` | 温度未知必须写 `unkC` |
| volt | `nom`, `vccint095`, `vccint100` | 电压条件 |
| capture | `cap01` | 同配置重复采集编号 |
| ext | `bin`, `dat`, `csv`, `json` | 原始二进制优先保留 |

### Metadata 必填项

每个 raw 文件旁边必须有同名 `.json`：

```json
{
  "project": "RO_TRNG",
  "date": "2026-05-10",
  "board_id": "z7020b01",
  "fpga_part": "xc7z020clg400-2",
  "vivado_version": "2023.2",
  "bitstream": "RO_TRNG_top.bit",
  "bitstream_sha256": "<fill>",
  "xdc_files": ["<fill>"],
  "vivado_seed": 3,
  "rtl_commit_or_snapshot": "<fill>",
  "experiment_id": "E2",
  "config": "compact",
  "temperature_c": 25.0,
  "voltage_note": "nominal",
  "capture_command": "<fill>",
  "raw_file": "<fill>",
  "raw_sha256": "<fill>",
  "bytes": 0,
  "notes": ""
}
```

### 派生数据规则

- `raw/` 下文件永不覆盖，所有转换写入 `processed/`。
- `processed/` 文件名保留 raw stem，并追加分析名，例如 `_trng_summary.csv`、`_sp80090b_non_iid.txt`。
- `fig/` 只放论文图或图草稿；图数据源必须能在 `processed/` 或 `reports/` 找到。
- 所有 summary 表必须包含 `raw_sha256` 或可追溯到 metadata。

## 必须产出的图表

### 主文图

| 图号 | 图名 | 内容 | 数据来源 |
| --- | --- | --- | --- |
| Fig. 1 | 研究框架图 | layout/routing/aggressor -> phase/jitter/correlation -> entropy/health-test | 手绘或绘图脚本 |
| Fig. 2 | 已有样本正负例 | 好样本与坏样本的 p1、runs、byte entropy 对比 | `data/experiments/e1_*` |
| Fig. 3 | 单 RO 频率与 jitter 分布 | RO2-RO9 freq、jitter_std_ps、count entropy | `data/experiments/e0_lut_ro_counter.csv` |
| Fig. 4 | 布局 sweep 熵质量 | compact/row/checker/far 的 90B min-entropy 和 STS pass rate | E2/E6 |
| Fig. 5 | TDC phase histogram | 不同布局或 aggressor 下的 phase bin 分布和 bubble rate | E5 |
| Fig. 6 | 相位扩散与 entropy 关联 | phase diffusion/correlation vs min-entropy scatter | E4/E5/E6 |
| Fig. 7 | 邻近 aggressor 影响 | near/far/idle/PRBS 的 entropy 和 health fail rate | E4 |
| Fig. 8 | 设计准则收益 | baseline vs layout-aware selection 的稳定性和安全 margin | E2-E6 汇总 |

### 主文表

| 表号 | 表名 | 内容 |
| --- | --- | --- |
| Table 1 | 与相关工作的比较 | FPGA、RO 类型、是否测物理机制、90B、STS、area、throughput、health test |
| Table 2 | 实验平台与参数 | 板卡、器件、时钟、UART、TDC、Vivado、温度/电压 |
| Table 3 | 实验矩阵 | E0-E7 配置、样本量、输出指标 |
| Table 4 | 正式随机性认证结果 | 代表配置的 SP800-90B、NIST STS、失败项 |
| Table 5 | 资源与开销 | LUT/FF/CARRY4/BRAM、频率、diagnostic overhead |

### 补充材料

- 每个 raw 数据的 metadata 表。
- 每个 Vivado seed 的布局截图或 XDC 坐标表。
- SP800-90B 完整输出。
- NIST STS 完整输出。
- TDC bin occupancy 校准结果。
- 健康测试阈值、fail rate 和误报说明。

## 论文结构草案

1. Introduction：RO-TRNG 成熟但物理机制证据不足，提出 layout-aware characterization。
2. Background：RO entropy source、FPGA fabric、TDC、SP800-90B、health tests。
3. Threat and Measurement Model：内部局部耦合、邻近开关活动、非侵入式环境扰动；不声称覆盖强注入攻击。
4. Design and Instrumentation：基线 TRNG、counter、TDC、UART packet、metadata pipeline。
5. Experiment Methodology：E0-E7 矩阵、采样长度、工具版本、布局约束。
6. Results：从已有正负例到布局/耦合/TDC/认证结果。
7. Design Guidelines：RO 选择、布局间距、aggressor 隔离、健康测试配置。
8. Limitations：单器件家族、UART characterization、TDC calibration、长期老化未覆盖。
9. Conclusion：布局感知的物理测量能提升 RO-TRNG 证据质量。

## 下一周最快路径

目标不是“做完全部顶刊实验”，而是拿到一组足够清晰的“正例-负例-机制解释”闭环，为论文开题和后续大矩阵扩展定方向。

### Day 1：冻结数据规范与复用现有结果

- 新建 `data/paper_runs/202605xx_z7020_E1_existing_screen/`，把现有 `e0/e1` summary 复制或索引为论文筛查结果。
- 为已有关键文件补 metadata 草案，至少包括原文件路径、bytes、分析脚本、生成日期未知说明。
- 产出 Fig. 2 和 Fig. 3 草图。

验收标准：一页图能说明“同类 RO-TRNG 输出存在好坏分化，单 RO 与组合输出差异巨大”。

### Day 2：确认硬件抓取链路

- 按 `doc/fpga1_lab_runbook.md` 重新确认 Zynq-7020 bitstream、UART pin、时钟和抓取命令。
- 对 baseline TRNG 抓取至少 10 MB raw。
- 对 TDC diagnostic 抓取至少 100k packets。
- 每个 raw 文件生成 `.json` metadata 和 SHA256。

验收标准：raw 数据可被 `analyze_trng_dataset.py` 或 `analyze_tdc_uart.py` 正常解析。

### Day 3：做最小布局对照

- 只做两个布局：`compact` 和 `checker/far`，各 3 个 seed。
- 每个 seed 抓取至少 5 MB raw。
- 记录 XDC、seed、bitstream hash、Vivado reports。

验收标准：得到第一张布局 vs entropy/STS screening 对比图。

### Day 4：做最小 aggressor 对照

- 先不追求全矩阵，只做 `idle`、`near high toggle`、`far high toggle`。
- 每个配置抓取 raw bitstream 和 TDC packets。
- 如果 RTL 不方便变动，则暂时用现有可控邻近活动或板级重复采样替代，并在 notes 中声明。

验收标准：得到 aggressor 对 phase histogram 或 raw entropy 的方向性影响。

### Day 5：跑正式统计工具

- 对 3 个代表配置运行 SP800-90B：最佳、最差、中等。
- 对同样配置运行 NIST STS。
- 把筛查结果、90B 结果、STS 结果合并成 Table 4 草案。

验收标准：有可引用的正式测试输出，而不是只有自写脚本统计。

### Day 6：写论文骨架

- 完成 Introduction、Methodology、Experiment Setup 的中文/英文混合初稿。
- 把所有图表占位放入论文目录。
- 明确每张图还缺哪些数据。

验收标准：论文不是“等数据再写”，而是数据回填式结构。

### Day 7：复盘与扩展决策

- 对照审稿风险表打分：创新性、重复性、认证强度、机制证据。
- 决定下一轮主扩展方向：布局 sweep、aggressor sweep、温度/电压 sweep 三选一优先。
- 冻结第一版 artifact index。

验收标准：形成一页给导师/合作者看的路线图：核心 claim、已有证据、缺口、下一轮实验。

## 当前优先级清单

| 优先级 | 动作 | 原因 |
| --- | --- | --- |
| P0 | 建立 metadata + SHA256 规范 | 没有可追溯性，后续数据越多越乱 |
| P0 | 对已有好/坏样本做正式 90B/STS | 立刻把筛查结果升级为审稿可接受证据 |
| P1 | 最小 compact vs checker/far 布局对照 | 最快验证核心 claim |
| P1 | TDC packet 抓取和 phase histogram | 让文章从黑盒统计变成机制论文 |
| P2 | aggressor near/far | 增强安全与耦合讨论 |
| P2 | 温度/电压 | 增强鲁棒性，但不是第一周瓶颈 |

## Artifact Index 模板

每次实验结束后在对应目录补一份 `artifact_index.md`：

```text
# Artifact Index

Experiment ID:
Date:
Operator:
Board:
FPGA:
Vivado:
RTL snapshot:

## Raw Data

| file | bytes | sha256 | metadata | note |
| --- | --- | --- | --- | --- |

## Bitstreams

| file | sha256 | xdc | seed | note |
| --- | --- | --- | --- | --- |

## Reports

| file | tool | command | note |
| --- | --- | --- | --- |

## Figures

| file | source data | script | note |
| --- | --- | --- | --- |
```

## 写作口径

- 把已有成熟领域承认清楚：普通 RO-TRNG 不是新问题。
- 把文章价值放在“物理证据 + 可复现实验矩阵 + 设计规则”。
- 负结果同样重要：坏样本、runs 失败、min-entropy 崩塌，是机制论文的燃料。
- 所有图表必须能追溯到 raw 文件和 metadata。
- 每个结论都区分三类证据：筛查统计、正式认证、物理诊断。
