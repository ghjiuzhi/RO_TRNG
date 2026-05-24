# Restart FIFO 诊断机制证据链更新 20260524

## 当前判断

这一轮证据链的重点不是证明某两个 RO 发生了强锁定，而是把机制边界逐步收紧：

1. pair-TDC 重复实验排除了“简单 RO-RO 强锁定”作为主因。
2. `random1_sampler_regs_only_x45y31` 只移动 sampling registers/routing，就把 20MiB 连续流修到近理想，说明采样端物理实现本身属于熵源边界。
3. 同一个 regs-only 设计在 SP800-90B restart 中仍出现非单调 warmup passband，说明连续流通过不等于 restart 通过。
4. formal restart profile 显示 warmup4 是全局低偏，warmup11 是全局高偏，而 warmup5/10 接近平衡，说明问题不是单一固定 bit 异常，而是启动后正式输出窗口的整体状态发生偏移。
5. FIFO diagnostic smoke 已经能观察正式 `fifo_generator_0` 读出的 warmup/send byte 事件，因此下一步应直接比较 warmup4/5/10/11 的正式 FIFO byte 矩阵。

## 为什么 TDC 排除强锁定

现有 pair-TDC 结果已经覆盖 random1/random3 的多组近频 RO pair，并完成 repeat02 复验。汇总结果中 `strong_lock_windows=0`，最大 small-lag correlation 约为 `0.0318`，zero-lag 最大相关也只有约 `0.0265`。这说明在当前板卡、电压、温度和采集长度下，被监控 RO pair 没有表现出持续、强烈、可解释 TRNG 退化的 pairwise hard locking。

因此论文不能写成“bad placement 导致两个 RO 互锁，所以熵下降”。更稳妥、更有价值的说法是：

> TDC evidence rules out simple pairwise RO locking as the dominant cause under the tested pairs and operating conditions.

这个结论是负证据，但很关键。它把机制解释从“单一 RO pair 锁定”推向“采样关系、startup transient、输出窗口和采样端物理实现共同影响熵源”。

同时要保留边界：当前 TDC 是 raw-bin 相对证据，未完成 code-density calibration，因此不应声称绝对 ps 级 jitter 数值。

## 为什么 sampler-regs continuous pass 仍不足

`random1_sampler_regs_only_x45y31` 是目前最强的因果消融之一：它保持 sample RO 基本结构不变，只移动 sampling registers/routing，连续流结果达到：

| 指标 | 结果 |
| --- | ---: |
| 20MiB continuous p1 | `0.499809736` |
| bit min-H | `0.999451119` |

这说明 sampling registers/routing 不是普通 readout 附属电路，而会改变 RO-TRNG 的稳态输出质量。换句话说，采样端物理实现应该被纳入 entropy source boundary。

但同一个 regs-only 设计在 restart 中不是稳定通过，而是出现非单调 passband：

| warmup | restart 结果 |
| ---: | --- |
| 0 | failed |
| 4 | failed |
| 5 | passed |
| 6 | passed |
| 8 | passed |
| 10 | passed |
| 11 | failed |
| 12 | failed |
| 16 | failed |

这说明 continuous stream 的稳态统计不能替代 SP800-90B restart。连续流 pass 只证明长期运行状态下 bias 被修复；restart 还会检验每次复位/启动后固定输出位置是否稳定偏置。对论文来说，这是一个很好的机制点：

> Steady-state entropy quality and restart robustness are related but not equivalent.

## formal restart profile 暗示的机制

formal restart profile 对 warmup4/5/10/11 做了更贴近 SP800-90B 输入的剖面。结果非常有区分度：

| warmup | status | p1 范围 | min-H 范围 | row ones std | worst x 范围 | 机制指向 |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 4 | failed | `0.407103-0.407970` | `0.754147-0.756258` | `16.7-17.1` | `733-751` | 全局低偏 |
| 5 | passed | `0.497894-0.498602` | `0.993936-0.995972` | `15.9-16.0` | `558-561` | 接近平衡 |
| 10 | passed | `0.499174-0.500018` | `0.997619-0.999948` | `15.9-16.3` | `547-565` | 接近平衡 |
| 11 | failed | `0.558805-0.559210` | `0.838538-0.839583` | `32.5-32.9` | `613-618` | 全局高偏 |

这里最重要的不是某一个 worst column，而是 warmup4 和 warmup11 呈现相反方向的整体偏移：warmup4 明显偏 0，warmup11 明显偏 1。warmup5/10 又恢复到接近平衡。这说明 restart failure 可能来自启动后某些正式输出窗口落入了确定性较强的相位/采样状态，而不是“等待越久越好”的单调扩散过程。

也就是说，当前机制应表述为：

> Restart bias appears as a warmup-window-dependent global shift plus column/window hotspots in the formal output stream.

这比“某个固定 column 坏了”更准确。column/worst-position 仍然重要，但它是在全局低/高偏背景上的局部最坏位置。

## FIFO diag smoke 的意义

之前的 sampler snapshot 只观察旁路采样位置，不能完全复现 formal restart pass/fail。现在 FIFO diagnostic smoke 的价值在于：它已经进入正式数据路径，能观察正式 `fifo_generator_0` 的 byte 事件。

当前 smoke：

| 项目 | 结果 |
| --- | ---: |
| restart_count | `32` |
| row_bytes | `16` |
| warmup_bytes | `4` |
| frames | `640` |
| warmup frames | `128` |
| send frames | `512` |
| warmup fifo_byte p1 | `0.375000000` |
| send fifo_byte p1 | `0.377197266` |

这说明诊断链路已经能把正式 FIFO readout 事件带出来，并区分 warmup/send phase、row index、event index 和 fifo byte。这个 smoke 规模还不能直接替代 `1000 x 125` formal restart，但它证明了下一步矩阵实验的可行性。

最关键的下一步不是再泛泛做 TDC，而是跑同一 regs-only 设计的 FIFO diag 矩阵：

| warmup | 目的 |
| ---: | --- |
| 4 | 对应 formal 全局低偏 fail |
| 5 | 对应 formal pass |
| 10 | 对应 formal pass |
| 11 | 对应 formal 全局高偏 fail |

如果 FIFO diag 在 send phase 中复现 warmup4 低偏、warmup11 高偏、warmup5/10 平衡，那么机制链条会非常强：

> regs-only 修复 steady-state continuous stream，但正式 restart 输出窗口仍会因 warmup alignment 进入低偏/高偏状态；这些状态已经能在正式 FIFO byte readout 事件中观察到。

如果 FIFO diag 不复现 formal profile，结论也有价值：问题可能进一步位于完整 formal run 长度、1000-row 统计、UART pacing、或更长运行下的 row/column accumulation，而不是短 smoke 的 FIFO byte 事件本身。

## 论文可写的证据链

目前可以把论文机制写成四层证据：

1. **TDC 排除简单强锁定。** pair-TDC 多组重复没有 strong-lock windows，说明不能把 random1 退化简单归因于 pairwise hard locking。
2. **采样端有因果作用。** regs-only 只移动 sampling registers/routing，就把 continuous TRNG 修到近理想，证明 sampler path 是 entropy source boundary 的一部分。
3. **restart 暴露 startup/window 风险。** 同一 regs-only 设计 restart 仍出现非单调 passband，warmup4 全局低偏、warmup11 全局高偏、warmup5/10 通过，说明稳态随机性和启动鲁棒性不是同一个性质。
4. **FIFO diag 正在连接 formal 数据路径。** smoke 已经能观察正式 FIFO byte 事件，下一步 w4/w5/w10/w11 矩阵将决定 formal restart bias 是否直接出现在正式 FIFO readout 窗口。

## 当前结论边界

已经可以主张：

- 当前证据不支持“简单 RO-RO 强锁定是主因”。
- sampling registers/routing placement 对 continuous entropy 有因果影响。
- regs-only restart passband 是非单调的，且 fail 模式包括 warmup-dependent global low/high bias。
- FIFO diag smoke 已能观察正式 FIFO byte 事件，具备继续验证 formal output-window 机制的条件。

还不能主张：

- raw TDC 已经给出绝对 ps 级 jitter 结论。
- FIFO diag 已经完整解释 warmup4/5/10/11 pass/fail。
- sampler snapshot 单独解释了 formal restart 失败。

## 下一步最小任务

1. 跑 `random1_sampler_regs_only_x45y31` FIFO diag 矩阵：warmup `4/5/10/11`。
2. 每个 warmup 至少先做小规模稳定复验，再扩大到能和 formal restart column profile 对齐的行数。
3. 对每个 run 输出 send phase 的 byte/bit p1、row ones、event-index profile、byte-phase profile。
4. 把 FIFO diag send 矩阵和 formal restart profile 的 warmup4/5/10/11 对齐比较。

如果这一步打通，论文主张可以提升为：

> Pairwise TDC excludes hard locking, sampler-register ablation proves sampler-side causality, and FIFO-level restart diagnostics localize the remaining failure to warmup-aligned formal output windows. Therefore, the physical entropy source boundary includes the sampler registers, local routing, and output packing/readout timing, not only the RO array.

## Compact FIFO diagnostic warmup5 update

新增 compact FIFO diagnostic warmup5 `1000 x 125` 真实采集已经成功：

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.bin`
- capture size: `125016` bytes
- capture SHA256:
  `70B8335811743DB6853119D4A256E8B89E33AE0C450547A1F7810300E6CFD77D`
- packed p1: `0.498316000`
- worst x: `549`
- column worst: byte `26`, bit `1`, x `549`, p1 `0.549`

和此前 compact warmup4 `1000 x 125` 结果对齐后：

| diagnostic | warmup | matrix | packed p1 | worst x | interpretation |
| --- | ---: | --- | ---: | ---: | --- |
| compact FIFO diag | 4 | `1000 x 125` | `0.498297000` | `555` | near ideal |
| compact FIFO diag | 5 | `1000 x 125` | `0.498316000` | `549` | near ideal |

这说明 compact w4/w5 都近理想；formal restart 中 w4 fail / w5 pass 的差异没有在 compact real-time FIFO diagnostic 路径中复现。因此当前机制应进一步指向 formal auto-stream、bitstream-specific behavior、readout scheduling、或精确约束差异，而不是原始 FIFO byte generation 的简单失衡。

这也收紧了论文表述边界：可以说 raw FIFO byte generation 在 compact real-time diagnostic 里没有表现出 formal warmup4 的全局低偏；不能再把 formal w4 fail 简化解释成 FIFO 输出字节本身天然失衡。

采集教训：

- `program_and_capture_uart.ps1` 的 `-VivadoBat` 参数应传 `vivado.bat`，不应传 `settings64.bat`。
- 带 `60s START_DELAY` 的 bitstream 采集时，`-IdleTimeoutSec` 应设为 `90` 或更长，避免开始延迟尚未结束就被 idle timeout 截断。
## Formal auto retest breakthrough

为了排除旧 formal `warmup4` 结果只是 stale bitstream、采集错位或偶然状态，
重新构建并采集了同一 placement、同一参数的 `RO_TRNG_restart_auto_top`
复验版本：

| item | value |
| --- | --- |
| placement | `data/experiments/xdc_sampler_island/random1_sampler_regs_only_x45y31.xdc` |
| top | `RO_TRNG_restart_auto_top` |
| matrix | `1000 x 125` |
| warmup | `4` |
| capture | `data/hardware/20260511_fpga1_board1/restart/random1_sampler_regs_only_restart_auto_formal_1000x125_warmup4_retest01_20260524.bin` |
| capture SHA256 | `AC3D7D6D9A9531B86947EB69495CD27C62EFE554C6FF052F2D2D254146AFCBC2` |
| header | `A55A03E8007D01D0` |
| packed SHA256 | `E65394FB07B954C4A6021C1CBEA9602D83400DB35A26EA00DB5A281205793A58` |
| packed p1 | `0.406735000` |
| row ones std | `17.174713244` |
| worst position | byte `0`, bit `2`, p1 `0.297000000`, x `703` |

这个结果非常关键：fresh same-night formal auto retest 仍然复现了
`warmup4` 的整体低偏。因此，formal w4 fail 不是旧文件偶然坏掉，而是
`RO_TRNG_restart_auto_top` 这个实现态在该 placement/warmup 下真实可复现。

与 compact FIFO diagnostic 对照：

| design | warmup | packed p1 | worst x | interpretation |
| --- | ---: | ---: | ---: | --- |
| formal auto retest | 4 | `0.406735000` | `703` | reproducible low-bias fail |
| compact FIFO diag | 4 | `0.498297000` | `555` | near ideal |
| compact FIFO diag | 5 | `0.498316000` | `549` | near ideal |

这说明 compact diagnostic 不是完全非侵入探针。它改变了 top-level
protocol/header 和周边逻辑，实现后可能改变熵源附近的物理扰动、控制路径、
FIFO/UART 布线和 sample-RO 的局部实现态。

## Routed implementation evidence

对 formal auto w4 retest 与 compact w4 的 routed checkpoint 做了 cell LOC/BEL
导出和 diff：

- formal dump:
  `data/experiments/restart_fifo_diag_20260524/formal_auto_w4_retest_routed_cells.csv`
- compact dump:
  `data/experiments/restart_fifo_diag_20260524/compact_w4_routed_cells.csv`
- summary:
  `data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.md`
- csv:
  `data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.csv`

核心结果：

| group | common cells | LOC changed | BEL changed |
| --- | ---: | ---: | ---: |
| entropy_source.data_ro | 48 | 0 | 0 |
| entropy_source.sampled_data_regs | 64 | 0 | 0 |
| entropy_source.sample_ro | 27 | 2 | 3 |
| fifo_generator | 241 | 195 | 151 |
| top_fsm_counters | 236 | 234 | 159 |
| uart_tx | 249 | 247 | 227 |

这个 diff 给出了非常有论文价值的边界结论：数据 RO 和 sampled-data
registers 的显式 placement 没变，但 FIFO、UART、FSM 以及少量 sample-RO
实现发生了大范围变化。也就是说，restart 统计不仅由 RO array 和采样寄存器
决定，还受到完整 readout/control/sampler-side physical implementation 的影响。

更准确的论文表述应为：

> The entropy source boundary includes not only the RO array and sampling
> registers, but also sampler-side routing and the nearby readout/control
> implementation state. A diagnostic top can perturb this boundary enough to
> mask a formal restart failure.
## Sample-RO locked compact causal test

为了区分 compact diagnostic 遮蔽 formal restart failure 的原因，做了一个更尖锐
的因果实验：保持 compact FIFO diagnostic 的 readout/control 结构不变，只把
sample RO 锁回 formal auto w4 retest 的 routed LOC/BEL。

新增 XDC：

- `data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc`

该 XDC 复制 `random1_sampler_regs_only_x45y31.xdc`，然后额外约束
`RO_SAMPLE_NAND` 和 `RO_SAMPLE_LOOP[0..7]` 到 formal auto w4 retest 中观察到的
sample-RO 物理位置。

结果：

| design | sample RO | warmup | packed p1 | worst x | interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| formal auto retest | formal routed | 4 | `0.406735000` | `703` | low-bias fail |
| compact FIFO diag | compact routed | 4 | `0.498297000` | `555` | near ideal |
| compact FIFO diag | compact routed | 11 | `0.498148000` | `548` | near ideal |
| compact FIFO diag | formal-routed sample RO locked | 4 | `0.376796000` | `805` | low-bias fail restored |

关键文件：

- bitstream:
  `data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_sample_ro_formal_locked_warmup4_1000x125/RO_TRNG_restart_fifo_compact_diag_top.bit`
- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.bin`
- capture SHA256:
  `1A79DC13BE9FC2596F4FB60255D50C96E5BE5D3A5EEE83A3B24A35FD3DC26428`
- analysis summary:
  `data/experiments/restart_fifo_diag_20260524/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.summary.md`

这个结果把机制从“compact top 改变了很多周边逻辑，所以不知道哪里导致差异”
推进到更强的因果判断：sample RO 的物理实现态本身足以决定 restart warmup4
是否进入强低偏状态。也就是说，sampler-side physical implementation 不是附属
readout，而是 entropy source boundary 的核心部分。

论文主张可以升级为：

> Pairwise TDC rules out simple hard locking; sampler-register ablation shows
> sampler-side placement can repair steady-state output; and the sample-RO
> locked compact restart test causally restores the formal warmup4 failure.
> Therefore, RO-TRNG entropy-source evaluation must include the sampler RO,
> sampling registers, local routing, and nearby readout/control implementation
> as a coupled physical boundary.
