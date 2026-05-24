# Paper Evidence Package - 2026-05-16

本文档把当前已经完成的实验结果整理成论文证据包。它的用途不是替代论文正文，而是给后续写作、补实验、让 GPT/Claude 复核时提供统一入口。

当前硬件暂不可用，因此本轮只整理离线证据，不启动 COM3、JTAG、Vivado 或 hw_server 采集任务。

## 1. 当前主线结论

### Claim A: RO-TRNG 原始随机性对 placement 明显敏感

可支撑表述：

> 在相同板卡、相同 RTL/串口采集流程下，不同 RO placement 产生了显著不同的原始 bitstream 统计质量；这种差异不仅体现在 bit bias，也体现在 runs、相邻相关性和 byte-level min-entropy。

核心证据：

- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`
- `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`

关键数字：

| placement | role | p1_mean | bit_min_entropy_mean | runs_p_mean | adjacent_equal_ratio_mean | byte_min_entropy_mean | 论文含义 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `random1` | formal | 0.337315512 | 0.593605945 | 0 | 0.556739754 | 4.80160868 | 坏随机种子/坏布局，强 bias |
| `random3` | formal | 0.499968565 | 0.999909299 | 0.18437283 | 0.500072473 | 7.9845501 | 好随机种子/好布局 |
| `same_column` | formal | 0.499930251 | 0.99979876 | 0 | 0.505979735 | 7.86432277 | bias 看似好，但结构相关性坏 |
| `sparse` | formal | 0.464349854 | 0.900637067 | 0 | 0.506596333 | 7.1440609 | 稀疏布局仍可退化 |
| `compact` | formal | 0.499947906 | 0.999849695 | 0.263603273 | 0.499938983 | 7.97683476 | 紧凑布局在当前板上表现好 |
| `checker` | formal | 0.499929237 | 0.999795837 | 0.149267368 | 0.500078744 | 7.97278511 | checker 布局在当前板上表现好 |

谨慎边界：

- 目前是 fast-mode 统计和部分重复采集，不等于完整 SP800-90B 认证。
- 不能写成“紧凑 placement 总是更好”或“稀疏 placement 总是更差”；当前只能说在这块正点原子领航者 V2 / xc7z020 / 当前 RTL 和种子集合下观察到明显分层。
- `same_column` 是很重要的反例：单看 p1 或 bit min-entropy 会误判，需要把 runs/相邻相关性纳入证据链。

建议图表：

- Figure 1: placement vs bit min-entropy / abs bias / runs p-value 三联图。
- Table 1: placement summary，突出 `random1`、`random3`、`same_column`、`compact/checker`。
- Supplementary Table: all placement formal/repeat rows。

## 2. Claim B: 同一 placement 下 repeat 具有一定一致性，但仍需扩展 repeat 矩阵

可支撑表述：

> 已完成的 formal/repeat 样本显示 placement-level 统计特征具有重复性；例如 `random1` repeat 仍保持强 bias，`random3` repeat 仍保持接近均衡，说明观察不是单次串口采集偶然错误。

核心证据：

- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`

关键数字：

- `random1 repeat`: `p1_mean=0.338143095`, `bit_min_entropy_mean=0.595409129`, `runs_p_mean=0`。
- `random3 repeat`: `p1_mean=0.499943098`, `bit_min_entropy_mean=0.999835828`。
- claims 表中已有配对 formal-repeat 最大 bit min-entropy 均值差：`0.000770577`。

待补实验：

- 已准备但待上板：`compact_repeat03_20mib`、`checker_repeat03_20mib`，以及 `same_column/sparse/far/random2/row/cross_region` 的 20 MiB repeat 队列。
- 队列文件：`data/experiments/fast_mode/hardware_queue_placement_repeat_20260515.csv`
- 运行入口：`doc/board_connected_runbook_20260515.md`

谨慎边界：

- 当前每个 placement 的 formal 样本多数只有 1 次，repeat 样本也不完整。最低投稿版可用作“初步重复性”，冲高水平需要 20 MiB repeat 矩阵补齐。

## 3. Claim C: RO 全开会导致可测的频率拉拽/扰动

可支撑表述：

> RO 全开状态相对于单 RO 测量状态存在可测的频率偏移，说明 RO 阵列不是完全独立的理想振荡源；placement 可能通过资源邻近、电源/衬底/布线耦合改变熵源动力学。

核心证据：

- `data/experiments/paper_artifacts_20260514/table_ro_freq_pulling_summary.md`

关键数字：

| family | data_shift_mean_mhz | data_mean_abs_ppm | sample_shift_mhz | sample_shift_ppm |
| --- | ---: | ---: | ---: | ---: |
| `random1` | -0.185041 | 421.577 | 0.310931 | 3466.91 |
| `random3` | -0.209355 | 478.085 | -0.075703 | -824.556 |

谨慎边界：

- 这能支撑“存在可测拉拽/扰动”，不能单独证明随机性退化完全由频率拉拽造成。
- 需要和 TRNG 指标、TDC 指标、restart fixed-column bias 放在一起，形成“机制假设链”，不要写成单因果结论。

建议图表：

- Figure 2: all-on vs single-on frequency shift bar chart。
- Discussion inset: coupling hypothesis schematic。

## 4. Claim D: 已监测 TDC pair 未出现强相位锁定，是对强锁定假设的负证据

可支撑表述：

> 在目前选取的六组 pair-specific TDC 捕获中，没有观察到强 pair-level phase locking；这说明当前随机性差异不能简单归因于被测 pair 出现强相位锁定，但不排除其他 placement、pair、PVT 或更长捕获下存在弱耦合。

核心证据：

- `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.md`
- `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_windows.md`
- `data/experiments/paper_artifacts_20260514/fig_tdc_pair_best_lag_abs_r.svg`

关键数字：

- 6 组 pair-specific TDC capture。
- 每组 16 个 windows，共 96 个 windows。
- `strong_lock_windows=0`。
- 最大 small-lag absolute correlation: `0.0317827`。
- `diff_std_ps_mean` 约 `2040-2043 ps`。

谨慎边界：

- 当前 TDC 仍应称为 relative/code-density-normalized TDC 指标，不能声称已经完成严格 ps 级 code-density calibration。
- 不能写“没有耦合”；只能写“未检测到强 pair-level phase locking”。

建议图表：

- Figure 3: TDC pair lag-correlation heatmap 或 best-lag abs r bar chart。
- Table 2: TDC pair dynamics summary。

待补实验：

- TDC code-density calibration。
- 多 placement / 多 pair / 多 board 的 TDC repeat。

## 5. Claim E: SP800-90B restart 暴露了 continuous-stream 统计难以发现的固定位置偏置

可支撑表述：

> `random3` continuous stream 在 non-IID 统计中表现较好，但 SP800-90B restart 结构揭示了固定 column/固定 bit 位置偏置；适当 warmup 后 restart sanity check 通过，说明 restart 初始瞬态与输出对齐位置是该熵源设计必须控制的因素。

核心证据：

- `data/experiments/restart_summary_20260515/restart_result_summary_20260515.md`
- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`
- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.csv`
- `data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.md`
- `data/experiments/paper_artifacts_20260515/fig_restart_warmup_transition.png`
- `data/experiments/paper_artifacts_20260515/fig_restart_warmup_transition.svg`
- `data/experiments/paper_artifacts_20260515/restart_column_bias_random3_formal_bits_warmup*/restart_byte_bit_heatmap.svg`
- `doc/restart_auto_stream_plan_20260514.md`
- `doc/sp800_90b_restart_execution_status_20260514.md`
- `doc/restart_warmup_repeat02_status_20260515.md`

关键数字：

| placement | warmup_bytes | repeat_tag | bit_order | ea_status | H_I | X_cutoff | X_max | min_h | worst_byte_index | worst_bit_index |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `random3` | 8 | run01 | msb | failed | 0.902345 | 605 | 721 |  | 2 | 2 |
| `random3` | 8 | run01 | lsb | failed | 0.828444 | 632 | 721 |  | 2 | 2 |
| `random3` | 10 | run01 | msb/lsb | failed | 0.902345 / 0.828444 | 605 / 632 | 650 |  | 1 | 4 |
| `random3` | 10 | repeat02 | msb/lsb | failed | 0.902345 / 0.828444 | 605 / 632 | 633 |  | 6 | 0 |
| `random3` | 11 | run01 | msb/lsb | passed | 0.902345 / 0.828444 | 605 / 632 | 583 | 0.743385 / 0.753865 | 1 | 3 |
| `random3` | 11 | repeat02 | msb/lsb | passed | 0.902345 / 0.828444 | 605 / 632 | 588 | 0.765014 / 0.746636 | 68 | 3 |
| `random3` | 12 | run01/repeat02 | msb/lsb | passed | 0.902345 / 0.828444 | 605 / 632 | 556-562 | 0.813237-0.849807 | 88/118 | 1/3 |
| `random3` | 16 | run01 | msb/lsb | passed | 0.902345 / 0.828444 | 605 / 632 | 549 | 0.820090 / 0.868735 | 43 | 7 |

核心解释：

- 当前观察到的 warmup 边界是 `10 < WARMUP_BYTES <= 11`，这是当前板卡/bitstream/采集流程下的经验边界。
- `random3` continuous stream 高质量不保证 restart 初始位置稳定。
- 固定 column 偏置比“整体随机性差”更有机制价值：它指向 restart 后初始相位、采样对齐、RO settle/warmup 的瞬态问题。
- `paper_artifacts_20260515` 中已有可直接入论文的 warmup transition 图和 restart column-bias heatmap；论文 restart 小节应优先使用这些 2026-05-15 产物，而不是只引用原始 summary 表。

更紧凑的 transition 表：

| warmup bytes | overall p1 | positions over cutoff | worst x | MSB restart | LSB restart |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 0.497933000 | 1 | 685 | unknown | unknown |
| 8 | 0.374385000 | 893 | 721 | failed | failed |
| 10 | 0.415017000 | 106 | 650 | failed | failed |
| 11 | 0.469088000 | 0 | 583 | passed | passed |
| 12 | 0.499478000 | 0 | 562 | passed | passed |
| 16 | 0.499126000 | 0 | 547 | passed | passed |

谨慎边界：

- 不能写成“SP800-90B 已认证通过”。当前是围绕 `ea_restart` 的 restart sanity / restart dataset 证据。
- `random3` 的 warmup 边界不能外推到其他 board、placement、温度、电压。
- 旧 capture 的 XADC 状态为 `missing`，不能声称这些 restart 结果已经附带温度/电压记录。
- `table_restart_warmup_transition_with_repeats.csv` 当前只有表头，不能作为主证据；repeat 证据应引用 `restart_result_summary_20260515.md` 中的 `run01/repeat02` 行。

建议图表：

- Figure 4: warmup bytes vs `X_max - X_cutoff` 或 pass/fail strip plot。
- Figure 5: worst column/bit heatmap，展示固定位置偏置如何随 warmup 消失。

## 6. XADC 温度/电压证据状态

当前状态：

- 自动化脚本已具备 XADC before/after 记录能力。
- 汇总脚本已完成：`scripts/summarize_xadc_metadata.py`
- 当前汇总：`data/experiments/xadc_summary/xadc_capture_summary_20260515.md`
- 已扫描 metadata: `120`
- 当前状态计数：`missing=120`

论文可写：

> 后续所有正式补采均记录 FPGA on-chip XADC 温度和电压 before/after，用于报告实验条件和排除明显 PVT 漂移。

当前不能写：

- 不能说已有所有结果都记录了温度/电压。
- 不能说记录的是室温；XADC 是片上 die temperature 和 FPGA 电源轨，不是外界环境温度。

上板后第一步：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
  -OutCsv data\hardware\20260511_fpga1_board1\metadata\xadc_smoke_20260515.csv `
  -HwServerUrl localhost:3122
```

## 7. 论文结构建议

### Introduction

写作目标：

- FPGA RO-TRNG 的随机性不只是 RTL 结构问题，也受到 placement 和启动瞬态影响。
- 许多工作只报告最终随机性测试，缺少 placement、TDC 动态、RO frequency、restart 之间的关联证据。
- 本文贡献：可复现实验流、placement matrix、TDC/RO_FREQ/restart 多视角证据，以及 warmup 对 restart fixed-column bias 的消除。

### Method

应包含：

- 板卡：正点原子领航者 V2 / xc7z020。
- RTL 来源：原始工程 `fpga`，复现工程 `fpga1`。
- placement 类别：`compact`、`checker`、`sparse`、`far`、`same_column`、`cross_region`、`random1/2/3`、原始 baseline。
- 数据类别：continuous TRNG bitstream、RO_FREQ、TDC pair dynamics、SP800-90B restart dataset。
- 自动化：bitstream programming、UART capture、SHA256、metadata、XADC before/after。

### Results

推荐顺序：

1. placement matrix 显示 raw bitstream 质量分层。
2. `random1` vs `random3` 说明随机 seed 可造成极端差异。
3. `same_column` 说明 p1/min-entropy 不足以评价结构质量。
4. RO_FREQ all-on shift 说明 RO 阵列存在可测扰动。
5. TDC pair null evidence 排除“所测 pair 强锁定”这一简单解释。
6. Restart warmup 结果揭示 fixed-column bias 和启动瞬态。

### Discussion

建议论点：

- placement 不是“手动摆放技巧”，而是一个可测的 entropy-source control factor。
- restart 数据给出了比 continuous stream 更严格的初始条件视角。
- TDC 的当前结果是负证据，但它帮助限制机制解释空间。
- 设计启示：RO-TRNG 需要把 placement、warmup、sampling alignment、restart behavior 纳入工程约束。

### Limitations

必须主动写：

- 单板结果仍需多板验证。
- 当前 XADC 对旧数据缺失；正式补采需要 before/after 记录。
- TDC 尚未完成独立 code-density calibration。
- 部分 placement repeat 仍待补齐。
- 当前 `ea_restart` 结果不能等价于完整 SP800-90B 认证。

## 8. 最低投稿版还缺什么

P0 必补：

1. `random1` restart warmup contrast：warmup 8/11/12。
2. `random3` repeat03：warmup 10/11/12。
3. XADC smoke，并在后续 capture 中记录 before/after。

P1 强化：

1. `same_column/sparse/compact/checker` restart warmup0 vs warmup12。
2. 20 MiB placement repeat queue。
3. 更新 XADC/restart/TRNG summary。

P2 冲高水平：

1. 多板：至少 `z7020_b02`、`z7020_b03` 复现 `random1/random3/restart warmup`。
2. TDC code-density calibration。
3. 更多 pair/placement 的 TDC repeat。
4. 把 TDC metrics、RO_FREQ shifts、TRNG metrics、restart column bias 做相关性分析。

## 9. 上板后一键路径

入口文档：

- `doc/board_connected_runbook_20260515.md`
- `doc/next_hardware_experiment_design_20260515.md`
- `doc/next_hardware_readiness_20260515.md`

上板前只读检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_next_hardware_readiness.ps1
```

完成硬件队列后刷新：

```powershell
python scripts\summarize_xadc_metadata.py --tag 20260515
python scripts\summarize_restart_results.py --tag 20260515
python scripts\summarize_trng_repeats.py
python scripts\analyze_fast_mode_results.py
```

## 10. 审稿风险与应对

| 审稿质疑 | 当前应对 | 还需补强 |
| --- | --- | --- |
| 只是 placement 工程调参，不是科学贡献 | 用 TDC/RO_FREQ/restart 多视角说明 placement 改变 entropy-source dynamics | 相关性分析和多板复现 |
| 只测一块板，偶然性太强 | 当前只作为 board-specific evidence | 多板同 bitstream 复现 |
| 没有温度/电压控制 | 后续使用 XADC before/after 记录 | 所有正式补采都带 XADC |
| TDC 未校准 | 只称 relative/code-density-normalized metrics | code-density calibration |
| continuous stream 通过不代表 restart 通过 | restart warmup fixed-column bias 正是本文亮点 | placement restart matrix |
| SP800-90B 证据不完整 | 明确写 `ea_restart` restart dataset evidence，不声称认证 | conditioning/full 90B pipeline |

## 11. 当前最适合写入摘要的版本

可用草稿：

> We present a placement-aware empirical study of ring-oscillator TRNG entropy sources on an FPGA. Under the same RTL and capture flow, different RO placements produce sharply stratified raw bitstream statistics: one random placement shows severe bias (`p1=0.3373`, bit min-entropy `0.5936`), whereas another reaches near-balanced output (`p1=0.49997`, bit min-entropy `0.99991`). A same-column placement further demonstrates that near-zero bias alone is insufficient, as it exhibits strong runs-test failure. RO frequency measurements show measurable all-on pulling, while six pair-specific TDC captures provide negative evidence for strong phase locking in the monitored pairs. Finally, SP800-90B restart-style experiments reveal a fixed-column startup bias in an otherwise high-quality continuous stream; adding 11 or more warmup bytes removes the observed restart failure in repeated captures. These results indicate that placement and startup alignment should be treated as first-class controls in FPGA RO-TRNG entropy-source evaluation.

中文对应：

> 本文面向 FPGA RO-TRNG 熵源，研究 placement 对原始随机性、RO 频率扰动、TDC 相位动态和 SP800-90B restart 行为的影响。在相同 RTL 与采集流程下，不同 RO placement 产生显著分层的 bitstream 统计质量：一个 random placement 出现强 bias（`p1=0.3373`，bit min-entropy `0.5936`），而另一个 random placement 接近均衡（`p1=0.49997`，bit min-entropy `0.99991`）。`same_column` 布局进一步表明，单独依赖 p1 或 min-entropy 会掩盖 runs 结构缺陷。RO 频率测量显示全开状态存在可测频率拉拽；六组 pair-specific TDC 捕获未观察到强相位锁定。最后，restart 实验揭示了 continuous stream 难以暴露的固定 column 启动偏置，并显示 11 字节以上 warmup 可在重复实验中消除该 restart failure。结果表明，placement 与启动对齐应作为 FPGA RO-TRNG 熵源评估的一等控制变量。
