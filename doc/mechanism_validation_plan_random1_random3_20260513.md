# random1 / random3 机制验证方案

日期：2026-05-13  
范围：只设计下一步 TDC / RO frequency 机制验证，不触碰硬件、Vivado、COM3、JTAG，不启动采集。

## 1. 背景与现象

当前最强对照是同属 `random` placement 族的两个 bitstream：

| 对照 | placement XDC | 现象 |
| --- | --- | --- |
| `random1` | `data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc` | `random1_run01`：`p1=0.337316`，bit min-entropy `0.593606`；`random1_repeat02_5mib`：`p1=0.337669`，bit min-entropy `0.594377`。严重偏置且可重复。 |
| `random3` | `data/experiments/xdc_matrix/ro_random_seed3_x36y35.xdc` | `random3_run01`：`p1=0.499969`，bit min-entropy `0.999909`；`random3_repeat02_5mib`：`p1=0.499971`，bit min-entropy `0.999917`。接近理想且可重复。 |

两者 RTL 与 Vivado flow 相同，manifest 均指向 `RO_TRNG_top`、`xc7z020clg400-2`、Vivado `2023.2`、`seed=1`，主要差异来自 RO placement XDC。TRNG 实例为 `u_entropy_source`，`RO_NUM=8`，`RO_STAGES=2`，`SAMPLE_STAGES=9`。

random1 的 8 个 RO 坐标：

| RO | SLICE |
| ---: | --- |
| 0 | `SLICE_X44Y39` |
| 1 | `SLICE_X52Y42` |
| 2 | `SLICE_X67Y63` |
| 3 | `SLICE_X66Y59` |
| 4 | `SLICE_X49Y41` |
| 5 | `SLICE_X67Y36` |
| 6 | `SLICE_X60Y62` |
| 7 | `SLICE_X36Y63` |

random3 的 8 个 RO 坐标：

| RO | SLICE |
| ---: | --- |
| 0 | `SLICE_X51Y43` |
| 1 | `SLICE_X59Y65` |
| 2 | `SLICE_X40Y35` |
| 3 | `SLICE_X66Y51` |
| 4 | `SLICE_X50Y47` |
| 5 | `SLICE_X66Y65` |
| 6 | `SLICE_X61Y44` |
| 7 | `SLICE_X50Y44` |

## 2. 为什么当前 TDC near/far 不能解释 random1 / random3

当前 TDC near/far 只能作为 baseline，不能直接解释 random1 极差、random3 优秀，原因如下。

第一，测量对象不同。已有 TDC top 是 `rtl/tdc/RO_TDC_sysclk_top.v`，只实例化两个独立 probe RO：`u_ro_a` 为 9-stage，`u_ro_b` 为 7-stage；而 TRNG 里的熵源是 `u_entropy_source` 下 8 个 2-stage RO，再加 9-stage sample RO。当前 TDC 没有测 `random1/random3` 那 8 个实际 RO，也没有测 sample RO 与 data RO 的相位关系。

第二，placement 不对应。已有 TDC XDC 只有：

| TDC case | 位置 |
| --- | --- |
| `tdc_ro_near_x36y35` | `u_ro_a` 从 `SLICE_X36Y35` 起，`u_ro_b` 从 `SLICE_X39Y35` 起 |
| `tdc_ro_far_x24y25` | `u_ro_a` 从 `SLICE_X24Y25` 起，`u_ro_b` 从 `SLICE_X54Y55` 起 |

这两个位置不是 random1 / random3 的 8 个 RO 坐标，也没有覆盖两组内部的关键 RO pair、RO 到 sample RO、或相邻 routing 关系。

第三，指标暂时只说明 near/far baseline 相近。已有正式 TDC 统计：

| run | packets | seq_gaps | lane A std phase | lane B std phase | diff std | phase Pearson r |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `tdc_near_run02` | 262143 | 0 | 1350.48 ps | 1379.85 ps | 1927.59 ps | 0.00328 |
| `tdc_far_run01` | 262132 | 43 | 1350.52 ps | 1361.22 ps | 1915.29 ps | 0.00230 |

near 与 far 的 `diff_std_ps` 和相关系数差异很小，说明这组 9/7-stage probe 在这两个位置下没有表现出强相关或相位坍缩。但这不能推出 random1 失败不是耦合/锁定，也不能推出 random3 好是因为相位扩散更好。它只说明：当前 probe 与当前 near/far 位置没有复现 random1/random3 的差异。

第四，TDC 现有分析没有覆盖频率分布与 beat 关系。`scripts/analyze_tdc_uart.py` 能给 phase bin、code density、phase std、pairwise correlation；但 random1 的主要失败可能来自 RO 频率过近、beat-frequency 与 sample RO 形成稳定偏置、局部锁定/拉拽，或 sample edge 长期落在某些 data RO 的确定性区间。仅看当前两个 probe 的 near/far phase histogram 不足以判断。

结论：当前 TDC 数据是“平台 TDC baseline”，不是 random1/random3 的机制证据。论文中不能写成“random1 已由 TDC 证明是耦合/锁定导致”；只能写成“TRNG 结果提示 placement-sensitive behavior，TDC baseline 表明测量链路可用，下一步需要 colocated pair / frequency evidence”。

## 3. 机制假设

建议把机制假设写成可证伪的层级，而不是一次性下定论：

H1：random1 的 8 个 2-stage RO 中存在频率过近或 beat 频率落入不利区间的 pair，使 XOR / sampled-data 组合后出现稳定 bit bias。

H2：random1 中部分 RO 与 sample RO 的相位漂移较慢，sample edge 看到的 RO 状态更确定；random3 中相位扩散更快或频率差更分散，因此输出接近 0.5。

H3：局部布局和 routing 引起的耦合、供电扰动或 injection-pulling 使若干 RO 的相位噪声出现 common-mode 成分。若该成分增强同步或降低独立性，会降低 min-entropy。

H4：random1/random3 的差异不是由粗粒度 “random placement” 标签决定，而是由实际坐标、RO 频率、pairwise phase relation、sample relation 和 routing 共同决定。

## 4. 路线 A：生成 random1 / random3 对应 TDC pair placement bitstream

目标：把 TDC probe 放到 random1/random3 的真实 RO 坐标上，测量 phase、jitter、pairwise correlation 和可能的相位坍缩。

### A1. 最小 TDC pair 设计

每次 build 两个 probe RO，对应 random1 或 random3 的某个 RO pair。输出沿用现有 8-byte TDC UART packet：

- `bin_a`：RO i 的 phase bin。
- `bin_b`：RO j 的 phase bin。
- `flags`：bubble、empty/full、valid 等已有状态。
- 分析继续复用 `scripts/analyze_tdc_uart.py`。

优先测这些 pair：

| 分组 | 优先 pair | 原因 |
| --- | --- | --- |
| random1 | `(0,4)`、`(0,1)`、`(2,3)`、`(2,6)`、`(3,6)` | 空间上较近或同一区域聚集，若存在 pulling/correlation，最可能先出现。 |
| random3 | `(0,7)`、`(0,4)`、`(4,7)`、`(1,5)`、`(3,6)` | 包含优秀组里较近 pair 和跨区域 pair，可检验“近并不必然差”。 |

建议每组至少保留一个跨区域 pair 作为内部对照，例如 random1 `(0,2)` 或 `(1,7)`，random3 `(2,5)` 或 `(1,2)`。

### A2. 关键实现点

当前可复用：

- `rtl/tdc/carry4_tdc_chain.v`
- `rtl/tdc/tdc_lane.v`
- `rtl/tdc/tdc_sampler.v`
- `rtl/tdc/tdc_bubble_correct.v`
- `rtl/tdc/tdc_encoder.v`
- `rtl/tdc/tdc_uart_packetizer.v`
- `rtl/tdc/RO_TDC_sysclk_top.v`
- `scripts/generate_tdc_ro_placement_xdc.py`
- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`
- `scripts/analyze_tdc_uart.py`

需要新增或扩展：

1. 新增 `scripts/generate_tdc_ro_pair_from_matrix_xdc.py`。输入 random1/random3 的 RO placement XDC 或坐标表、`--pair i,j`，输出 TDC pair XDC。它应把 `u_ro_a` 和 `u_ro_b` 的 LUT 固定到对应 RO 的 SLICE/BEL 附近。

2. 扩展 TDC top 的 RO stage 参数。当前 `u_ro_a=9-stage`、`u_ro_b=7-stage`，更像通用 probe。为了对应 TRNG，应增加参数或新 top，例如 `RO_TDC_pair_sysclk_top.v`，支持 `RO_A_STAGES=2`、`RO_B_STAGES=2`。这样测的是与 TRNG data RO 同阶数的 probe。

3. 约束 TDC carry chain 位置。当前 generator 只约束两个 RO，不约束 `carry4_tdc_chain`。若要跨 build 比较 bin width / DNL / INL，应固定 TDC carry chain 到同一列或至少记录其 placement。否则不同 build 的 TDC 量化非均匀性会混进 RO 差异。

4. 输出 run manifest。每个 bitstream 应记录：`placement_family=random1/random3`、`pair=(i,j)`、两个 RO 坐标、RO stage、TDC carry-chain 坐标、Vivado seed、bitstream SHA256、采集文件 SHA256。

### A3. TDC 指标与判据

对每个 pair 输出：

- `lane_a_std_phase_ps`、`lane_b_std_phase_ps`：单 RO phase spread / jitter proxy。
- `diff_std_ps`：pairwise relative phase spread。偏小可能表示相对相位更稳定或被拉住；偏大通常表示相位扩散更充分。
- `phase_pearson_r` / `bin_pearson_r`：两 RO 是否存在同步或 common-mode 相关。
- `lane_a/b_min_entropy_bin`、used bins、dead bins、DNL/INL：TDC 码密度质量和 phase occupancy。
- lag correlation / Allan-like phase-difference drift：建议后续在 `analyze_tdc_uart.py` 上新增，因为只看 zero-lag Pearson 可能漏掉慢 beat 或准周期。

判据建议：

- 若 random1 的关键 pair 比 random3 出现显著更高 `phase_pearson_r`、更低 `diff_std_ps`、更强周期性 lag correlation，则支持耦合/锁定/拉拽假设。
- 若 random1 与 random3 的 TDC pair 指标相近，则说明失败更可能来自 sample RO beat、XOR 组合、routing 延迟或特定多 RO 交互，需要路线 B 或扩展到 sample relation。

### A4. 扩展到 sample relation

仅测 data RO pair 仍可能不够。TRNG 的 `rand_bit` 来自 8 个 data RO 被 8 条 sample phase line 采样后 XOR，再由 sample RO 输出。因此建议第二阶段增加：

- data RO i vs sample RO phase。
- sample RO frequency / phase stability。
- data RO i 在 sample edge 上的 sampled 0/1 probability。

这可能需要一个 `RO_TDC_trng_probe_top.v`：复用 `entropy_source` 的 RO 结构，但把选中的 `ro_chain[i][RO_STAGES-1]` 和 `ro_sample_chain[k]` 暴露给 TDC lane。这个 RTL 不是本次要改的内容，但应列入机制验证需要新增项。

## 5. 路线 B：RO frequency counter 或 beat-frequency 测量

目标：直接比较 random1/random3 的 8 个 RO 频率分布、频率差、beat 关系，以及是否存在锁定/拉拽。

### B1. 为什么频率路线优先

random1 的 `p1≈0.337` 是强 DC bias，且 repeat 稳定；这种现象未必需要强 zero-lag phase correlation 才会出现。若某些 data RO 与 sample RO 的频差很小，或多个 data RO 频率形成稳定 beat，sampled bit 的 0/1 占空可能长期偏向一侧。频率计数能先回答三个低成本问题：

1. random1 的 8 个 RO 是否比 random3 更集中、更接近、或有异常离群？
2. random1 是否存在 data RO 与 sample RO 的低 beat-frequency 组合？
3. 在开/关其他 RO、改变窗口长度时，频率是否发生可测漂移，提示 pulling 或 coupling？

### B2. 可复用内容

当前已有：

- `rtl/jitter_measure.v`：单 RO counter + UART 输出框架。
- `rtl/CU.v`：窗口控制，默认输出 1,000,000 个 8-bit count。
- `rtl/counter.v`：RO clock domain counter。
- `rtl/RO.v`：可参数化 RO。
- `scripts/analyze_ro_counter.py`：从 counter dump 估计 `ro_freq_mhz`、count-derived jitter、count entropy。

这些模块可作为 RO frequency counter 的起点，但当前 `jitter_measure.v` 只测一个 9-stage RO，且输入时钟接口是差分 `clk_100M_p/n`，不等价于当前 random1/random3 里 8 个 2-stage RO。

### B3. 需要新增或扩展

1. 新增 `RO_FREQ_matrix_sysclk_top.v` 或 `RO_FREQ_trng_probe_top.v`。建议使用和 `RO_TRNG_top` 一致的 8 个 2-stage data RO 加一个 9-stage sample RO，按 random1/random3 XDC 固定 data RO 坐标。用 mux 选择一个 RO 接入 counter，避免一次开太多 counter 引入额外负载。

2. 新增 per-RO placement XDC generator。可扩展 `scripts/generate_ro_placement_xdc.py` 或新增 `scripts/generate_ro_freq_probe_xdc.py`，从 `ro_random_seed1_x36y35.xdc` / `ro_random_seed3_x36y35.xdc` 派生同坐标约束。若新增 sample RO 约束，应单独记录其坐标。

3. 新增 capture protocol 描述和 metadata schema。虽然本 session 不采集，但后续硬件 session 每个 run 应记录：selected RO index、其他 RO 是否 enabled、window size、样本数、温度、电压、bitstream SHA256。

4. 扩展 `scripts/analyze_ro_counter.py`。当前输入按文件粒度分析单通道 count。建议新增：
   - 多 RO 汇总表：`freq_mean_mhz`、`freq_std_ppm`、`jitter_std_ps`。
   - pairwise `abs(delta_f)`、`beat_period=1/abs(delta_f)`。
   - data RO vs sample RO 的 beat ranking。
   - 不同 enable 模式下的 frequency shift，用 ppm 表示 pulling。

### B4. 推荐测量矩阵

最小矩阵：

| design | 测量对象 | enable 模式 | 输出 |
| --- | --- | --- | --- |
| `random1_freq` | data RO0..RO7 + sample RO | all-on，逐个 mux 到 counter | 9 个频率分布、jitter、count entropy |
| `random3_freq` | data RO0..RO7 + sample RO | all-on，逐个 mux 到 counter | 同上 |
| `random1_freq_single_on` | data RO0..RO7 | 只开被测 RO | 与 all-on 比较 pulling |
| `random3_freq_single_on` | data RO0..RO7 | 只开被测 RO | 同上 |

若资源和时间允许，再加 pair-on 模式：

- random1 的 `(0,4)`、`(0,1)`、`(2,3)`、`(2,6)`。
- random3 的 `(0,7)`、`(0,4)`、`(4,7)`、`(1,5)`。

判据：

- random1 若出现更小的 pairwise `abs(delta_f)`，尤其是 data RO vs sample RO 的低 beat-frequency 组合，支持 beat-dominated bias 假设。
- random1 若 all-on 与 single-on 的频率差显著大于 random3，支持 pulling/coupling 假设。
- random1 若频率分布与 random3 相近，但 bias 仍极差，则需看 phase relation、routing delay、sampled-data XOR 结构，而不是只看频率。

## 6. 推荐优先级与最小闭环实验

推荐优先级：

1. **优先做路线 B：RO frequency / beat-frequency。** 它最直接、实现风险较低，能快速判断 random1 是否存在频率聚集、低 beat、或 all-on pulling。对解释 `p1=0.337` 这种强偏置，频率证据通常比 pair TDC 更先给方向。

2. **并行准备路线 A 的 TDC pair generator，但先只 build 少量关键 pair。** TDC 能补相位扩散和 pairwise correlation 证据，但需要更谨慎地固定 carry chain，并处理不同 build 的 TDC bin calibration。

3. **第二阶段再测 sample relation。** 若 frequency 发现 data-sample 低 beat，或 pair TDC 没解释 bias，应优先做 data RO vs sample RO TDC，而不是继续盲目扩展 data-data pair。

最小闭环实验：

1. 对 random1 和 random3 各生成一个 RO frequency probe bitstream，保持 8 个 data RO 坐标与 TRNG XDC 一致。
2. 测 8 个 data RO 与 sample RO 的频率、count jitter、all-on vs single-on frequency shift。
3. 从频率表计算 pairwise `abs(delta_f)` 和 data-vs-sample beat ranking。
4. 对 random1 和 random3 各选 2 个最可疑 pair 做 TDC pair 测量，例如 random1 `(0,4)`、`(2,3)`；random3 `(0,7)`、`(4,7)`。
5. 将机制指标与已有 TRNG 指标关联：
   - x 轴：最小 data-sample `abs(delta_f)`、最小 data-data `abs(delta_f)`、最大 all-on pulling ppm、最大 TDC `phase_pearson_r`、最小 `diff_std_ps`。
   - y 轴：`abs(p1-0.5)`、bit min-entropy、byte min-entropy、adjacent_equal_ratio。

最小成功标准：

- 如果 random1 在 frequency/beat 或 TDC correlation 上明显异常，而 random3 正常，则形成“机制证据链”。
- 如果 random1 不异常，仍有价值：可以排除简单频率聚集和二元 pair 锁定，把后续焦点转向 sample RO、multi-RO XOR、routing asymmetry 或 FIFO/packing 之外的采样结构。

## 7. 需要新增与复用清单

### 已存在可复用

| 类别 | 文件 | 用途 |
| --- | --- | --- |
| TRNG RTL | `rtl/RO_TRNG_top.v`、`rtl/entropy_source.v`、`rtl/RO.v` | 确认 8 个 2-stage data RO 与 9-stage sample RO 结构。 |
| TDC RTL | `rtl/tdc/*.v` | 现有双 lane carry-chain TDC、bubble correction、encoder、UART packetizer。 |
| TDC placement | `scripts/generate_tdc_ro_placement_xdc.py` | 可作为 pair placement generator 的模板。 |
| TRNG placement | `scripts/generate_ro_placement_xdc.py` | 已能复现 random1/random3 坐标。 |
| Vivado flow | `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl` | 支持传入 extra XDC 和 out_dir，可复用生成 TDC bitstream。 |
| TDC analysis | `scripts/analyze_tdc_uart.py` | 现有 phase / correlation / code-density 分析。 |
| Counter RTL | `rtl/jitter_measure.v`、`rtl/CU.v`、`rtl/counter.v` | 可改造成多 RO frequency probe。 |
| Counter analysis | `scripts/analyze_ro_counter.py` | 可复用并扩展为多 RO / beat summary。 |
| 结果表 | `data/hardware/20260511_fpga1_board1/hardware_run_audit.csv` | 提供 random1/random3 的 p1、bit min-entropy、已有 TDC baseline。 |

### 需要新增

| 类别 | 建议文件 | 内容 |
| --- | --- | --- |
| TDC pair XDC generator | `scripts/generate_tdc_ro_pair_from_matrix_xdc.py` | 从 random1/random3 坐标派生 `u_ro_a/u_ro_b` LOC/BEL。 |
| TDC pair top | `rtl/tdc/RO_TDC_pair_sysclk_top.v` | 参数化 `RO_A_STAGES/RO_B_STAGES`，默认 2-stage；保留现有 UART packet 格式。 |
| TDC carry-chain XDC | `data/experiments/xdc_tdc/tdc_chain_fixed_*.xdc` 或 generator | 固定 `carry4_tdc_chain`，降低跨 build TDC 非均匀性干扰。 |
| RO frequency top | `rtl/debug/RO_FREQ_trng_probe_top.v` 或 `rtl/tdc/RO_FREQ_trng_probe_top.v` | 8 data RO + sample RO，mux 到 counter，支持 all-on/single-on/pair-on。 |
| RO frequency XDC generator | `scripts/generate_ro_freq_probe_xdc.py` | 复用 random1/random3 的 RO 坐标，并记录 sample RO 坐标。 |
| Frequency analysis 扩展 | `scripts/analyze_ro_frequency_matrix.py` 或扩展 `analyze_ro_counter.py` | 生成 per-RO frequency、pairwise delta_f、beat ranking、pulling ppm。 |
| 实验 manifest | `data/experiments/mechanism_random1_random3_manifest.csv` | 记录每个 mechanism bitstream 的 pair、坐标、stage、seed、bitstream、采集文件。 |

## 8. 论文中如何表述机制假设与证据链

建议论文文字避免从当前数据直接跳到“锁定导致 random1 失败”。更稳妥的表达：

1. **观察层。** “在相同 RTL、相同 board、相同采集协议下，placement alone 造成了可重复的 raw entropy 差异。random1 表现为稳定严重 bias，random3 接近理想。”

2. **假设层。** “我们假设该差异来自 RO network 的物理时序状态，而不是 random 标签本身：包括 per-RO frequency spread、data-sample beat relationship、pairwise phase diffusion，以及由局部 routing / supply / substrate coupling 引起的 pulling 或 common-mode phase noise。”

3. **测量层。** “为检验该假设，我们不只做 NIST / min-entropy 黑盒测试，而是构建 colocated TDC pair probe 和 RO frequency probe，使 probe RO 的 placement 对应到 TRNG 中的实际 RO 坐标。”

4. **证据链。** 推荐图表链路：
   - placement map：random1 / random3 的 8 个 RO 坐标。
   - TRNG quality：`p1`、bit min-entropy、byte min-entropy、repeat error bar。
   - frequency evidence：per-RO frequency distribution、pairwise delta_f heatmap、data-sample beat ranking。
   - phase evidence：关键 pair 的 TDC phase histogram、`diff_std_ps`、lag correlation、phase Pearson。
   - correlation plot：机制指标 vs `abs(p1-0.5)` / bit min-entropy。

5. **结论层。** 若后续数据支持假设，可以写：“The poor random1 layout is associated with lower effective phase diversity / smaller beat separation / stronger pulling signatures, which predicts its reduced min-entropy.” 若数据不完全支持，应写：“The evidence rules out a simple near/far explanation and suggests that sample relation or multi-RO interactions dominate.”

推荐用语：

- 可以说：`random1/random3` 是 “placement-controlled counterexample pair”。
- 可以说：当前 near/far TDC 是 “measurement baseline and sanity check”。
- 可以说：机制验证目标是建立 “placement -> frequency/phase/correlation -> entropy” 的证据链。
- 不要说：当前 TDC near/far 已经证明 random1 是 coupling / locking 导致。

## 9. 建议执行顺序

1. 新增 RO frequency probe top 和 XDC generator，优先生成 `random1_freq`、`random3_freq`。
2. 扩展 counter analysis，输出 per-RO frequency、pairwise beat、all-on/single-on pulling。
3. 依据 frequency 结果选择每组 2 个 TDC pair，而不是先全量测 28 个 pair。
4. 新增 TDC pair XDC generator 和 2-stage pair top，固定 TDC carry chain。
5. 用已有 `analyze_tdc_uart.py` 先产出 baseline metrics，再补 lag correlation / phase-drift analysis。
6. 将 mechanism metrics 与已有 `hardware_run_audit.csv` 中的 `p1`、bit min-entropy、byte min-entropy 汇总成论文图表输入。

最小优先级一句话：**先测 random1 vs random3 的 RO 频率/beat 和 all-on pulling，再用少量 TDC pair 验证相位/相关性，最后把这些机制指标关联到 `p1` 与 min-entropy。**
