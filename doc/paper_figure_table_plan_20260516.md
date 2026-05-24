# Paper Figure and Table Plan - 2026-05-16

本文档把当前论文图表规划成“可直接使用 / 需要重画 / 等硬件补采”三类。它和 `doc/paper_evidence_package_20260516.md` 配套使用。

## A. 当前可直接使用的表格

| 编号 | 建议标题 | 状态 | 来源文件 | 论文作用 | 注意事项 |
| --- | --- | --- | --- | --- | --- |
| Table I | Experimental setup and acquisition flow | 可写，需手工整理 | `doc/board_connected_runbook_20260515.md`; `doc/next_hardware_experiment_design_20260515.md` | 说明板卡、Vivado、UART、bitstream、capture、SHA256、metadata | 旧数据 XADC 缺失要注明 |
| Table II | Placement-dependent TRNG statistics | 可直接用 | `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md` | 主结果表，展示 placement 分层 | formal/repeat 次数不均衡 |
| Table III | Ranked 10 MiB placement results | 可直接用 | `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md` | 按质量排序，突出 spectrum | 适合正文或补充材料 |
| Table IV | RO frequency all-on pulling | 可直接用 | `data/experiments/paper_artifacts_20260514/table_ro_freq_pulling_summary.md` | 支撑 RO 阵列存在动态扰动 | 不能写成唯一因果 |
| Table V | TDC pair dynamics summary | 可直接用 | `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md` | 说明未检测到强 pair locking | TDC 未完成 code-density calibration |
| Table VI | Restart warmup transition | 可直接用 | `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`; `data/experiments/restart_summary_20260515/restart_result_summary_20260515.md` | restart 主结果 | `with_repeats.csv` 当前只有表头，不能作为主表 |
| Table VII | Reviewer-risk and claim boundary | 可写 | `doc/paper_evidence_package_20260516.md`; `doc/delegated_reviews/reviewer_attack_list_20260514.md` | 主动声明限制，降低审稿风险 | 可放 Discussion 或 Supplement |

## B. 当前已有的图

| 编号 | 建议标题 | 状态 | 来源文件 | 用途 |
| --- | --- | --- | --- | --- |
| Fig. 1 | TDC pair best-lag absolute correlation | 已有 SVG | `data/experiments/paper_artifacts_20260514/fig_tdc_pair_best_lag_abs_r.svg` | 展示 `strong_lock_windows=0` 的负证据 |
| Fig. 2 | Restart warmup transition | 已有 PNG/SVG | `data/experiments/paper_artifacts_20260515/fig_restart_warmup_transition.png`; `fig_restart_warmup_transition.svg` | 展示 warmup10 fail、warmup11+ pass |
| Fig. 3 | Restart byte-bit heatmap: random3 warmup8/10/11/12/16 | 已有 SVG | `data/experiments/paper_artifacts_20260515/restart_column_bias_random3_formal_bits_warmup*/restart_byte_bit_heatmap.svg` | 展示固定位置偏置随 warmup 变化 |
| Fig. 4 | Restart byte-bit heatmap: random1/random3 no warmup | 已有 SVG | `data/experiments/paper_artifacts_20260515/restart_column_bias_random1_formal_bits/restart_byte_bit_heatmap.svg`; `restart_column_bias_random3_formal_bits/restart_byte_bit_heatmap.svg` | 对比坏例/好例在 restart 下都可能有固定位置行为 |

## C. 建议离线重画的图

这些图不需要硬件，只需要现有 CSV/MD。当前尚未统一生成成论文风格图。

| 编号 | 建议标题 | 数据源 | 建议图型 | 目的 |
| --- | --- | --- | --- | --- |
| Fig. A | Placement quality spectrum | `trng_formal_all_10mib_ranked.csv` | 横向 bar chart：bit min-entropy + p1 偏差 | 主视觉，展示 random1 到 random3 的 spectrum |
| Fig. B | Bias is not enough: same_column counterexample | `trng_repeats_by_placement.csv` | scatter：abs bias vs runs_p 或 adjacent_equal_ratio | 证明单看 p1 不够 |
| Fig. C | RO all-on pulling | `table_ro_freq_pulling_summary.csv` | grouped bar chart | 支撑频率扰动 |
| Fig. D | Restart warmup margin | `restart_result_summary_20260515.csv`; `table_restart_warmup_transition.csv` | `X_max - cutoff` vs warmup | 比 pass/fail 更直观 |

建议先重画 Fig. A 和 Fig. B，因为它们最直接支撑主贡献。

## D. 等硬件补采后再重画的图

| 编号 | 建议标题 | 需要补采 | 目的 |
| --- | --- | --- | --- |
| Fig. E | 20 MiB placement repeat confidence | placement repeat queue | 从“现象展示”升级为统计比较 |
| Fig. F | XADC before/after stability | XADC-enabled captures | 报告温度/电压条件，回应 PVT 质疑 |
| Fig. G | Placement restart contrast matrix | same_column/sparse/compact/checker warmup0/12 | 证明 restart fixed-column bias 不是 random3 单点现象 |
| Fig. H | Multi-board replication | z7020_b02/z7020_b03 | 冲高水平，回应 single-board criticism |
| Fig. I | Calibrated TDC bin width / phase metrics | code-density calibration | 支撑更强 TDC 时间解释 |

## E. 建议正文图表顺序

最低投稿版：

1. Fig. 1: 实验流程图，手工画或后续生成。
2. Fig. 2: placement quality spectrum。
3. Fig. 3: same_column counterexample。
4. Fig. 4: RO_FREQ pulling。
5. Fig. 5: TDC pair best-lag abs r。
6. Fig. 6: restart warmup transition。
7. Fig. 7: restart column-bias heatmap。

冲高水平版：

1. 加 placement repeat confidence。
2. 加 XADC before/after stability。
3. 加 placement restart contrast matrix。
4. 加 multi-board replication。
5. 加 calibrated TDC code-density figure。

## F. 关键写作边界

- `table_restart_warmup_transition_with_repeats.csv` 目前只有表头，不能作为证据。
- XADC 当前汇总为 `missing=120`，旧数据不能声称有温度/电压记录。
- TDC 图只能支撑“未检测到强 pair locking”，不能支撑“没有耦合”。
- SP800-90B 相关图表只能写作 `ea_restart` / restart evidence，不能写作完整认证。
- placement 图表必须展示完整 matrix 或至少包含中间例，避免被审稿人认为 cherry-picking。

