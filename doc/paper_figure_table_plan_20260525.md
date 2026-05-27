# 论文图表计划 2026-05-25

本文档更新 2026-05-16 版本，加入 2026-05-25 完成的 sample RO 双向反事实、clean reset-aligned TDC 六点矩阵、TDC code-density calibration、fixed-LUT TDC 复算、机制证据链和 clean TDC 图表。

## 建议正文主图

| 编号 | 标题 | 状态 | 数据源 | 论文作用 |
| --- | --- | --- | --- | --- |
| Fig. 1 | Experimental flow and entropy-source boundary | 待画 | 本文档 + `doc/reproduce_key_experiments_20260525.md` | 说明 data RO、sample RO、采样寄存器、TDC、restart/SP800-90B 的关系 |
| Fig. 2 | Placement quality spectrum | 可离线重画 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv` 或相关 summary | 证明 placement 影响连续流 TRNG 质量 |
| Fig. 3 | Sample-RO bidirectional counterfactual | 当前最重要，建议新画 | `data/experiments/sample_ro_counterfactual_20260525/sample_ro_counterfactual_table_20260525.csv` | 核心机制图：只改 sample RO 可 forward fail / reverse repair |
| Fig. 4 | Restart warmup and fixed-column bias | 已有基础图，建议整合 | `data/experiments/paper_artifacts_20260515/`，restart column-bias summaries | 说明 restart startup transient 和固定位置偏置 |
| Fig. 5 | Clean reset-aligned TDC entropy metrics | 已生成 | `data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_entropy.svg` | 展示 warmup/alignment 下的 raw-bin entropy |
| Fig. 6 | Clean reset-aligned TDC hard-lock indicators | 已生成 | `data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_hard_lock_indicators.svg` | 排除简单 hard locking |
| Fig. 7 | Clean reset-aligned TDC window stability | 已生成 | `data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_window_entropy.svg` | 展示 TDC 结果不是单个窗口偶然 |
| Fig. 8 | TDC code-density calibration / fixed-LUT sensitivity | 已有表，可画图 | `data/experiments/tdc_code_density_cal_20260525/`; `data/experiments/tdc_pair_dynamics_lut_reanalysis_20260525/`; `data/experiments/tdc_sampler_data_lut_reanalysis_20260525/` | 说明 raw bin 非线性真实存在，且校准映射没有推翻 hard-lock 排除结论 |
| Fig. 9 | XADC condition summary | 可做 supplement | `data/experiments/xadc_summary/xadc_capture_summary_20260525.csv` | 报告温度/电压记录状态 |

## 建议正文主表

| 编号 | 标题 | 状态 | 数据源 | 论文作用 |
| --- | --- | --- | --- | --- |
| Table I | Experimental setup and capture protocol | 可写 | `doc/board_connected_runbook_20260515.md`; `doc/reproduce_key_experiments_20260525.md` | 说明板卡、Vivado、UART、XADC、SHA256 |
| Table II | Placement-dependent TRNG statistics | 已有数据 | placement repeat summaries | 主结果表 |
| Table III | Restart assessment and worst-column bias | 已有数据 | restart summary / SP800-90B outputs | 说明 restart 比连续流更严格 |
| Table IV | Sample-RO counterfactual summary | 已生成 | `data/experiments/sample_ro_counterfactual_20260525/sample_ro_counterfactual_table_20260525.csv` | 核心贡献表 |
| Table V | Clean reset-aligned TDC six-point matrix | 已有 | `data/experiments/tdc_clean32k_figures_20260525/tdc_clean32k_main_metrics.csv` | TDC 机制约束 |
| Table VI | Mechanism evidence chain | 已生成 | `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.csv` | 把 TRNG/restart/TDC/XADC 合并 |
| Table VII | Claim boundary and reviewer risk | 已写 | `doc/paper_claim_evidence_boundary_20260525.md` | Discussion 或 supplement |
| Table VIII | TDC calibration and fixed-LUT reanalysis | 已生成 | `data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_compare_20260525.csv`; fixed-LUT summaries | 回应 TDC calibration 风险 |

## 当前可直接引用的新产物

clean TDC 图：

```text
data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_entropy.svg
data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_hard_lock_indicators.svg
data/experiments/tdc_clean32k_figures_20260525/fig_tdc_clean32k_window_entropy.svg
```

clean TDC 表：

```text
data/experiments/tdc_clean32k_figures_20260525/tdc_clean32k_main_metrics.csv
data/experiments/tdc_clean32k_figures_20260525/tdc_clean32k_warmup_deltas.csv
data/experiments/tdc_clean32k_figures_20260525/tdc_clean32k_window_stats.csv
```

TDC calibration 与 fixed-LUT 复算：

```text
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_compare_20260525.md
data/experiments/tdc_clean32k_lut_reanalysis_20260525/
data/experiments/tdc_pair_dynamics_lut_reanalysis_20260525/
data/experiments/tdc_sampler_data_lut_reanalysis_20260525/
```

机制证据链：

```text
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.csv
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md
```

sample RO 反事实记录：

```text
doc/sample_ro_locked_passband_results_20260525.md
data/experiments/sample_ro_counterfactual_20260525/sample_ro_counterfactual_table_20260525.csv
data/experiments/sample_ro_counterfactual_20260525/sample_ro_counterfactual_table_20260525.md
```

## 图表叙事顺序

推荐正文顺序：

1. 先展示 placement spectrum，让读者相信现象真实存在。
2. 再展示 restart fixed-column bias，让读者看到连续流统计不能覆盖 restart startup。
3. 然后给出 sample RO 双向反事实，这是最强因果证据。
4. 接着用 clean TDC 排除简单 hard locking，让机制解释更准确。
5. 最后给机制证据链总表和 reviewer-risk boundary。

这个顺序比“先 TDC 后 TRNG”更稳，因为 TDC 当前不是主因果证据，而是机制约束证据。

## 高水平投稿前还缺的图

| 图 | 缺什么 | 为什么重要 |
| --- | --- | --- |
| Multi-board sample-RO counterfactual | 至少 board B/C 的 forward fail 和 reverse repair | 回应 single-board criticism |
| Dedicated TDC code-density calibration | 已完成 8 MiB formal + lane-swap；还缺多板/repeat/per-run before-after | 支撑 calibrated phase/jitter 边界表述 |
| Command-gated before/after XADC | UART RX pin smoke + command-gated top | 让 XADC before/after 不干扰 auto-stream |
| Placement matrix confidence intervals | 更完整 repeats 或 bootstrap 图 | 避免被认为 cherry-picking |

## 图注写法边界

raw TDC 图注应写：

```text
Raw-bin clean reset-aligned TDC metrics. No independent code-density calibration is applied; these results are used for relative comparison and hard-lock exclusion.
```

fixed-LUT TDC 图注应写：

```text
Fixed-LUT sensitivity reanalysis using dedicated code-density calibration. The calibration changes absolute phase-spread values but does not reveal hidden strong-lock windows; therefore it does not overturn the hard-lock exclusion conclusion.
```

sample RO 图注应写：

```text
Only the sample-RO routed implementation is changed while the remaining restart topology is kept fixed. The bidirectional flip of restart outcome supports sampler-side physical realization as part of the entropy-source boundary.
```

XADC 图注应写：

```text
XADC reports on-chip die temperature and FPGA supply telemetry. It is not an ambient temperature measurement.
```
