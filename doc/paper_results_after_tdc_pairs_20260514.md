# Pair-specific TDC 完成后的论文结果整合

日期：2026-05-14  
范围：仅整合既有离线材料与数据文件；未接触硬件、Vivado、COM/JTAG 或 `hw_server`。

## 1. 硬件实验完成情况

截至 2026-05-14 11:50，pair-specific TDC 六个目标 pair 已全部完成 2 MiB 采集，并生成离线分析目录。最新完成状态应以 `doc/fast_mode_tdc_pair_status_20260514.md`、`data/hardware/20260511_fpga1_board1/tdc_pairs/analysis_*` 和 `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md` 为准。早前 `doc/tdc_pair_fast_mode_status_20260514.md` 中的 4/6 状态是中间状态：当时两个 random3 pair 因 Vivado/hw_server 初始化停滞尚未完成；后续数据目录显示这两个 pair 已补齐。

已完成的 pair-specific TDC 数据如下：

| placement | pair | packets | seq gaps | diff std ps | phase r | max abs lag r | strong lock windows |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| random1 | RO0/RO1 | 262142 | 67 | 2042.90 | -0.002491 | 0.021599 | 0 |
| random1 | RO2/RO4 | 262138 | 122 | 2042.29 | -0.002237 | 0.031783 | 0 |
| random1 | RO4/RO5 | 262143 | 124 | 2041.51 | -0.001195 | 0.022497 | 0 |
| random3 | RO0/RO6 | 262143 | 8 | 2041.96 | -0.001465 | 0.023927 | 0 |
| random3 | RO3/RO5 | 262143 | 4 | 2040.26 | -0.000020 | 0.027616 | 0 |
| random3 | RO3/RO7 | 262142 | 120 | 2040.45 | -0.000037 | 0.022911 | 0 |

六个 pair 的共同特征是：单次 2 MiB 采集中有效包数约 262k，TDC 差分相位标准差稳定在约 2040--2043 ps，零延迟相位相关系数接近 0；16 个固定窗口的小滞后扫描也没有任何窗口达到 `|r| >= 0.5` 的强锁定筛选阈值。离线动态分析给出的全局最大绝对零延迟窗口相关为 0.0170543，最大绝对小滞后窗口相关为 0.0317827，强锁定窗口数为 0。

与前面的 fast-mode 结果结合，硬件证据链现在可以写成三层：

1. TRNG 输出层：10 MiB placement matrix 显示不同布局之间输出质量差异很大。非 original 布局的 `bit_min_entropy` 均值约 0.93697，其中 random1 最差约 0.59361，random3 最好约 0.99991；original fpga1 baseline 的 10 MiB run01 约 0.99990。
2. RO_FREQ 机制层：random1/random3 均出现近频 pair，且 random1 在 5 MiB all-on 场景中有更强 sample-RO pulling 个案信号，例如 `sample_shift_ppm_vs_single` 约 4067 ppm，而 random3 约 1113 ppm。
3. pair-specific TDC 机制层：针对可疑近频 pair 的直接相位读出没有发现强同步或强相位锁定。

## 2. Pair-specific TDC 的正/负结果如何写进论文

正结果不是“发现锁定”，而是“完成了更有针对性的机制验证”。论文中建议把 pair-specific TDC 放在结果或讨论中的 mechanism validation 小节，作用是把原本只基于布局、频率接近和输出退化的推断，推进到对具体 RO pair 的直接相位观测。

可写的正面贡献：

- 工程上完成了 pair-specific bitstream 与约束流，针对 random1 和 random3 各选择三个可疑 RO pair，而不是只比较 generic near/far TDC。
- 每个 pair 都有 2 MiB TDC 捕获、code-density 校准、包序号检查、lane phase 分布、diff phase 和窗口化 lag-correlation 分析。
- 该实验给出了一个重要的排除性结论：在当前采集条件下，random1 的熵退化不能简单归因于“被选中的近频 RO pair 出现持续强相位锁定”。

需要明确写成负结果或 null observation 的部分：

- 六个 pair 的 `phase_pearson_r` 均接近 0，最大绝对值仅约 0.00249。
- 窗口化小滞后相关最大绝对值约 0.03178，远低于强锁定阈值 0.5。
- `diff_std_ps` 在六个 pair 间高度一致，约 2040--2043 ps，没有显示锁定时预期的差分相位收缩。

建议论文措辞：

> We further instrumented the selected close-frequency RO pairs using a pair-specific TDC readout. Across six 2 MiB captures, the calibrated phase streams showed near-zero zero-lag correlation and no window satisfying a conservative lag-correlation locking criterion. Thus, the TDC data are treated as a null observation for strong pair-level synchronization under this measurement setup, rather than evidence of sustained phase locking.

中文讨论可写为：

> pair-specific TDC 实验没有观察到强相位锁定。该结果并不否定布局相关耦合对熵的影响，而是约束了机制解释：random1 的显著退化更可能来自近频条件、供电/布线扰动、采样 RO pulling、瞬态相互作用或多 RO 集体效应的组合，而非单一 pair 的静态零延迟同步。

## 3. 对原耦合/锁定猜想的修正

原始猜想可以从“近频 RO pair 导致锁定，进而导致熵下降”修正为更稳健的两段式机制假说：

1. 物理布局和近频关系会改变 RO 阵列的动态工作点，表现为部分 pair 的频率接近、sample-RO pulling 以及 TRNG 输出统计退化。
2. 当前 pair-specific TDC 没有检测到持续强相位锁定，因此“锁定”不能作为主结论；更合理的解释是弱耦合、动态 pulling、瞬态 beat、供电/地弹噪声或多振荡器集体交互共同影响采样随机性。

论文主线建议从“证明锁定”改为“发现并定位布局敏感性，并用 TDC 约束机制边界”。这样写更抗审稿：

- 保留强结果：不同布局在同一 FPGA/同一采集协议下产生显著 TRNG 质量差异，random1 与 random3 形成鲜明对照。
- 保留机制证据：RO_FREQ 显示 close pair 和 pulling，与 TRNG 退化方向一致，尤其 random1 个案更强。
- 主动承认 TDC null result：没有检测到强 pair-level phase locking，因此不夸大因果链。
- 把机制表述降级为“consistent with dynamic coupling/pulling”而非“caused by locking”。

建议避免的表述：

- “RO pair is locked/synchronized/entrained.”
- “TDC proves coupling causes the entropy loss.”
- “Close frequency alone explains random1 failure.”

建议使用的表述：

- “No strong TDC-level pair locking was detected.”
- “The evidence constrains, rather than proves, the synchronization hypothesis.”
- “The degradation is consistent with placement-dependent dynamic interaction, including frequency proximity and sample-RO pulling.”

## 4. 下一步 90B 和审稿风险

SP800-90B 是下一步必须补上的主证据。现有 `bit_min_entropy`、monobit/runs、byte entropy、STS 或 TDC/RO_FREQ 结果只能作为筛选和机制支持，不能替代 SP800-90B entropy-source assessment。

近期离线行动建议：

1. 使用 `scripts/prepare_90b_inputs.py` 为完整 10 MiB formal captures 生成 1-bit symbol 和 byte-symbol 输入，并保存 manifest、SHA-256、转换模式和命令行。
2. 先跑 `ea_non_iid`，把 conservative non-IID min-entropy per bit 作为主表；`ea_iid` 仅作为诊断，不轻易宣称 IID。
3. 对 5 MiB repeat captures 做复核，报告 placement 之间的重复性或波动。
4. 当前顺序采集文件不能当作 restart dataset。若论文要靠 90B 完整路径说服审稿人，需要后续单独采集 restart matrix，例如 1000 restarts by 1000 symbols。
5. 若设计声称有 conditioning，需要明确定义 conditioning stage，并运行 `ea_conditioning`；若输出是 raw/unconditioned，应明确不声明 conditioning 增益。

主要审稿风险与应对：

| 风险 | 可能质疑 | 建议应对 |
| --- | --- | --- |
| 90B 缺失 | 统计测试和 min-entropy quick bound 不等于 entropy-source validation | 以 `ea_non_iid` 主表补齐，并把 STS/monobit/runs 降为辅助 |
| TDC null result | 既然没有锁定，机制是否站不住 | 主动将结论从“锁定因果”改为“布局敏感和动态交互”，强调 TDC 是约束机制边界 |
| 单板单日数据 | random1/random3 对比可能是板级偶然性 | 标注为 fpga1 board1 结果；后续如有条件补多板/多温度/多电压 |
| 近频 pair 因果性 | close pair 与熵退化可能只是相关 | 把 RO_FREQ、pulling、TRNG、TDC 作为多模态证据链，避免单因果断言 |
| TDC 方法限制 | code-density 校准、窗口大小、lag range 会影响结论 | 报告窗口数、lag scan、校准方法，并声明“当前测量条件下未检测到强锁定” |
| 数据规模和重复性 | 2 MiB TDC 和 10 MiB TRNG 是否足够 | 90B 用完整 formal captures；TDC 作为机制辅助，不作为熵估计 |

## 可直接进入论文的结论句

本文当前最稳妥的结果表述是：

> The placement study revealed a large entropy-quality spread across RO layouts, with random1 showing severe degradation and random3 remaining close to the original baseline. RO-frequency measurements indicated close-frequency pairs and stronger sample-RO pulling in the degraded case. However, pair-specific TDC measurements on six selected pairs did not reveal strong phase locking. These results suggest that the degradation is not explained by a simple static locking event, but is consistent with placement-dependent dynamic interaction in the RO array.

对应中文：

> 布局实验表明 RO-TRNG 输出质量对物理布局高度敏感，random1 出现显著熵退化，而 random3 接近原始基线。RO 频率测量显示退化场景中存在近频 pair 和更强的 sample-RO pulling；但针对六个可疑 pair 的 pair-specific TDC 并未检测到强相位锁定。因此，当前证据不支持“单一 pair 静态锁定”作为主因，而更支持“布局相关动态交互”这一更保守的机制解释。

## 主要依据文件

- `doc/tdc_pair_fast_mode_status_20260514.md`
- `doc/tdc_pair_dynamics_interpretation_20260514.md`
- `doc/sp800_90b_integration_plan_20260514.md`
- `doc/fast_mode_tdc_pair_status_20260514.md`
- `doc/fast_mode_results_summary_20260514.md`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/hardware/20260511_fpga1_board1/tdc_pairs/analysis_*`
