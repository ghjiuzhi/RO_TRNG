# 面向采样端物理边界的 FPGA RO-TRNG 布局敏感性机理研究

> 版本：v3 初稿，2026-05-25  
> 状态：中文论文初稿。当前结果已足够支撑机制型初稿；已补 8 MiB dedicated TDC code-density calibration、A/B lane-swap calibration、clean32k LUT 敏感性复算、pair-specific TDC fixed-LUT 复算、sampler passband 对照和 reduced-XOR 硬件反事实。高水平投稿前最关键缺口是多板复现和更系统的 PVT / per-run calibration 对照。

## 摘要

环形振荡器真随机数发生器（RO-TRNG）常被认为主要由 RO 阵列本身提供物理噪声，而采样电路更多被视为读出路径。然而在 FPGA 中，RO、采样振荡器、采样寄存器、局部路由和读出控制逻辑共享可编程逻辑资源，其物理实现可能直接改变熵源边界。本文基于 Zynq-7020 FPGA 上的 RO-TRNG 复现实验，系统比较多种 placement 下的连续流随机性、RO 频率扰动、TDC 相位观测和 SP800-90B restart 行为。实验显示，同一 RTL 结构在不同 placement 下可从强偏置状态切换到接近理想状态；同时，reset-aligned TDC 并未观察到持续同 bin 驻留或强小滞后相关，说明不能将坏 placement 简单解释为 pairwise RO hard locking。进一步地，sample RO 双向反事实实验表明：在 compact diagnostic 结构中仅将 sample RO 锁回 formal-routed 物理位置，即可将原本 near-ideal 的 restart passband 拉回强偏置失败；反过来，在 formal restart 结构中仅将 sample RO 锁到 compact-routed 位置，又能将 warmup4 失败修复到接近理想。围绕 `sampler_island_local warmup10` 的 reduced-XOR 硬件反事实进一步显示：单个 same-data-RO 方向可以是强偏置的真实硬件输出函数，而完整 `all64` 输出质量来自多个方向在 XOR 组合边界上的抵消。该结果说明采样端物理实现不是被动读出电路，而是 RO-TRNG 物理熵源边界的一部分。本文据此提出一种面向 sampler-side boundary 的 RO-TRNG 评估流程，并讨论其对 FPGA TRNG placement、restart 评估和 TDC 机理诊断的影响。

关键词：RO-TRNG；FPGA；placement；TDC；SP800-90B；restart；sample RO；entropy-source boundary

## 1. 引言

基于环形振荡器（ring oscillator, RO）的真随机数发生器是 FPGA 上常用的物理熵源结构。传统解释通常强调 RO 抖动、频率差、相位漂移以及多个 RO 之间的耦合关系。由此得到的工程直觉是：若 RO 足够分散、频率不完全相同、互相不强锁定，则输出随机性应较好。然而，FPGA 的可编程逻辑结构使得这一直觉并不完整。RO-TRNG 的随机输出并不是由 RO 阵列单独决定，而是由数据 RO、sample RO、采样寄存器、局部路由、时序孔径和读出路径共同形成。

本项目最初的目标是通过 TDC 测量不同 RO placement 下的频率、抖动和相位差，并与随机性指标建立相关性。随着真实硬件实验推进，我们发现更强的论文主线不是“手动 placement 能改善随机性”，也不是“坏 placement 导致 RO-RO 强锁定”，而是：

> FPGA RO-TRNG 的 placement 敏感性很大程度上来自采样端物理实现。sample RO、采样寄存器、局部路由和采样孔径应被视为物理熵源边界的一部分，而不是被动读出电路。

本文的贡献包括：

1. 构建了面向 FPGA RO-TRNG 的自动化采集与分析流程，覆盖 bitstream 生成、UART 采集、SHA256、XADC、SP800-90B non-IID/restart 和 TDC 指标。
2. 在同一 Zynq-7020 FPGA 上验证了多种 placement 会显著改变连续流随机性，形成 random1 坏例、random3 好例以及 compact/checker/sparse/far 等对照。
3. 通过 pair-specific TDC 和 clean reset-aligned TDC 排除简单 pairwise hard locking 作为主导解释。
4. 通过 SP800-90B restart warmup 扫描发现固定采样位置偏置和 startup transient：连续流高熵并不保证 restart 初始固定位置稳定。
5. 通过 sample RO 双向反事实实验形成当前最强机制证据：只改变 sample RO 的 routed physical implementation，就能在 forward 和 reverse 两个方向翻转 restart outcome。
6. 通过 reduced-XOR 硬件反事实证明 same-data-RO 方向偏置和互补方向抵消是真实硬件现象，而不是离线 snapshot 分析伪影；最终随机性应建模为 sampler-side sampled-vector 的组合结果。

## 2. 背景与问题定义

### 2.1 RO-TRNG 与 FPGA placement

RO-TRNG 一般由多个自由振荡 RO 提供非确定性相位扰动，再由采样电路将其离散化为 bitstream。FPGA 中的 RO 通常由 LUT 组合环构成，其实际频率和抖动受 LUT BEL、slice、局部布线、邻近逻辑、电源噪声和温度影响。同一 RTL 在不同 placement 下可能映射到不同的物理路径，因此输出统计特征可能发生显著变化。

### 2.2 TDC 的角色

TDC 可以观测 RO 边沿相对采样时钟的 bin 分布、相位差、转移熵、驻留时间和小滞后相关。本文不把 TDC 当作“证明锁定”的唯一工具，而把它作为机理约束工具：

- 若 TDC 显示强同 bin 驻留、长 run、强相关，则支持锁定或慢扩散假设；
- 若 TDC 不显示这些特征，则应避免将坏 placement 简单写成 hard locking；
- 若 sampler-side placement 改变 TDC startup/diffusion 指标，则可辅助解释 restart transient；
- 若 TDC 仍无法分离好坏 placement，则机制更可能在采样寄存器、局部路由或采样孔径层面。

当前已完成 dedicated code-density calibration：包括 2 MiB smoke、8 MiB formal calibration 和 A/B lane-swap calibration。结果显示 TDC bin 分布明显不均匀，且 lane-swap 后高熵 lane 随被驱动的 RO/lane 物理实现发生转移。因此本文主体仍谨慎使用 raw-bin 相对比较，不把未说明不确定度的 TDC 结果写成严格绝对 ps 级 jitter；但已用固定 LUT 对 clean32k TDC 和 pair-specific TDC 做敏感性复算，验证其“不支持简单 hard locking”的结论没有被校准映射推翻。

### 2.3 SP800-90B restart 的意义

连续流 non-IID 估计可以反映长序列的整体熵水平，但不能完全覆盖 restart 后固定初始状态下的列偏置风险。SP800-90B restart 测试要求多次 restart 后形成行列矩阵，并检查固定位置是否出现异常偏置。对 RO-TRNG 来说，restart 测试能暴露上电/复位后的相位记忆、startup transient 和固定采样窗口问题。

## 3. 实验平台与方法

### 3.1 硬件与工程环境

实验平台为 Zynq-7020 FPGA 复现板，Vivado 版本为 2023.2。PC 端通过 COM3 串口以 115200 baud 采集 UART 数据。工程目录为：

```text
E:\Project\MLDSA\RO_TRNG
```

采集脚本自动记录：

- bitstream 路径；
- capture 文件大小；
- SHA256；
- metadata；
- XADC after-only 温度/电压读数；
- 分析输出目录。

当前 XADC 记录主要用于说明 on-chip die temperature 和 FPGA 电源轨状态，不等同于室温控制。

### 3.2 placement 矩阵

实验构建了多种 placement，包括 `random1`、`random2`、`random3`、`compact`、`checker`、`sparse`、`far`、`same_column`、`cross_region` 和 `row` 等。连续流数据覆盖 10 MiB/20 MiB repeat，用于比较：

- overall p1；
- bit min-entropy；
- runs p-value；
- adjacent-equal ratio；
- SP800-90B non-IID smoke。

### 3.3 TDC 测量

TDC 采用 CARRY4 chain + sampler + bubble correction + encoder + UART packetizer。已完成两类 TDC：

1. pair-specific TDC：测量重点 RO pair 的相位相关和小滞后窗口相关。
2. reset-aligned clean32k TDC：通过 `TDCR` header 对齐 reset/startup 采集，每个 run 采集 32768 packets。

clean32k 六点矩阵包括：

- `random1_baseline_warmup0`
- `random1_baseline_warmup12`
- `random3_goodref_warmup0`
- `random3_goodref_warmup12`
- `random1_sampler_local_warmup0`
- `random1_sampler_local_warmup12`

### 3.4 restart 数据集

为避免 reprogram-based restart 需要数十小时，本文实现了 restart auto-stream 顶层。FPGA 下载一次 bitstream 后自动输出 row-major restart 矩阵。已完成：

- 4x64 restart smoke；
- 1000x1000 byte-symbol capture；
- 1000x125 packed-byte capture 并展开为 1000x1000 bit-symbol 输入；
- random3 warmup0/8/10/11/12/16 扫描；
- warmup10/11/12 repeat02。

## 4. 实验结果

### 4.1 placement 显著改变连续流随机性

连续流 TRNG 结果显示 placement 对输出质量有显著影响。代表性结果如下：

| placement | 数据规模 | 代表结果 | 解释 |
| --- | ---: | --- | --- |
| random1 formal | 10 MiB | p1 = 0.337315512，bit min-entropy = 0.593605945 | 稳定坏例 |
| random3 formal | 10 MiB | p1 = 0.499968565，bit min-entropy = 0.999909299 | 稳定好例 |
| original fpga1 | 10 MiB | p1 = 0.500035894，bit min-entropy = 0.999896436 | 原始复现链路可输出近理想序列 |
| random3 repeat03 | 20 MiB | p1 = 0.499915，bit min-entropy = 0.999755 | 好例可重复 |

该结果说明同一 RTL 结构在不同 physical implementation 下可以表现出完全不同的随机性。placement 不是工程细节，而是熵源实现的一部分。

### 4.2 TDC 未支持简单 hard locking 解释

pair-specific TDC 共覆盖 6 个重点 pair。原始窗口分析与 fixed-LUT 复算均未观察到 strong-lock windows：fixed-LUT 复算覆盖 12 个 pair-specific runs 和 192 个窗口，两套 calibration LUT 下最大 small-lag absolute correlation 分别约为 0.03137 和 0.03136，strong-lock windows 均为 0。进一步的 sampler-data TDC 覆盖 6 个 runs 和 96 个窗口，fixed-LUT 复算后最大 small-lag absolute correlation 约为 0.0273，strong-lock windows 同样为 0。clean reset-aligned TDC 六点矩阵进一步显示：

| run | H(diff) | transition H(diff) | same ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: |
| random1 baseline warmup0 | 6.75886 | 13.1434 | 0.009949 | 3 | -0.00828 |
| random1 baseline warmup12 | 6.66619 | 12.9741 | 0.011658 | 3 | 0.000004 |
| random3 goodref warmup0 | 6.61583 | 12.8973 | 0.013153 | 3 | -0.00922 |
| random3 goodref warmup12 | 6.60778 | 12.8768 | 0.012940 | 3 | -0.00613 |
| random1 sampler-local warmup0 | 6.65464 | 12.9439 | 0.013031 | 3 | -0.00083 |
| random1 sampler-local warmup12 | 6.73356 | 13.0993 | 0.010651 | 3 | 0.00186 |

这些结果支持一个负结论：当前观测条件下，坏 placement 不能简单解释为两个 RO 长时间相位锁定。sampler-local warmup12 的 diffusion 指标在六点矩阵中最高，提供弱正证据，但不足以单独解释 restart/TRNG 的大幅差异。

此外，本文补充了 dedicated code-density calibration。新建 `RO_TDC_code_density_cal_sysclk_top`，用独立 calibration RO 驱动 TDC lane，先完成 2 MiB smoke，再完成 8 MiB formal calibration 与 A/B lane-swap calibration：

| calibration run | bytes | packets | seq gaps | lane A H(bin) | lane B H(bin) | XADC after |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| a7/b11 smoke | 2,097,152 | 262,143 | 0 | 2.994386 | 2.450985 | not recorded |
| a7/b11 formal | 8,388,608 | 1,048,575 | 0 | 3.001707 | 2.460396 | 46.9 C, VCCINT 1.000 V |
| a11/b7 formal | 8,388,608 | 1,048,575 | 0 | 2.397010 | 3.118547 | 47.2 C, VCCINT 1.000 V |

formal calibration 均为 `seq gaps=0`，说明正式规模下 UART/TDC calibration stream 稳定。lane-swap 后高熵 lane 发生反转：`a7/b11` 中 lane A 更高，而 `a11/b7` 中 lane B 更高。这说明观测到的 bin 非线性不是 PC 端解析假象，而与被驱动的 lane/RO 物理实现有关。进一步用两套 LUT 复算 clean32k TDC 后，校准相位差自相关仍接近 0，A/B Pearson 仍接近 0，最长 raw differential-bin run 仍为 3；用同样的 fixed-LUT 方法复算 12 个 pair-specific runs 后，192 个窗口中 strong-lock windows 仍为 0；复算 6 个 sampler-data runs 后，96 个窗口中 strong-lock windows 仍为 0。因此 code-density calibration 没有推翻“不支持简单 pairwise hard locking”的负证据结论，也没有把 sampler-side 修复解释成简单 sampler-data phase locking。不过，由于 LUT 来自 dedicated calibration top，而不是每个 placement capture 前后交错校准，本文仍不把这些结果写成严格的绝对 ps 级 metrology。

进一步，为了区分 hard locking 与局部开关扰动，本文新增 TDC mask-perturb 顶层。在该设计中，TDC lane A/B 固定观测同一对 RO，同时通过 enable mask 改变周围 data RO 或 sample RO 是否振荡。P0 矩阵完成 6 个 8MiB 真实硬件采集，每个 run 解码得到 `1,048,575` 个 packet。random1 RO0/RO1 在 `pair_only`、`all_data_on` 和 `pair_plus_sample` 之间只出现温和变化；random3 RO0/RO6 则在 `all_data_on` 下出现明显扰动，`H(diff)` 从 `6.697029` 降到 `5.982632`，`transition H(diff)` 从 `13.383203` 降到 `11.962490`。但该 run 的 lag autocorrelation 仍接近 0，最长同 differential-bin run 仅为 4。因此，邻近 RO 开关活动确实可能重塑 TDC phase/bin 分布，但这种现象不等价于 pairwise hard locking。这一结果将 TDC 从单纯“排除锁定”的负证据推进为“局部开关活动/负载扰动参与相位扩散边界”的机制约束证据。

针对 `sampler_island_local warmup10` 近阈值窗口，本文进一步做了与 startup window 对齐的 reset-aligned TDC。该 run 观测 local sample RO 与 `random1` data RO0，header 为 `5444435201E60501000A000080881352`，共采集 `32768` 个 packet。结果显示，w10 的 `H(diff)=6.638003`、`transition H(diff)=12.921799`、同 differential-bin 转移比例 `0.011841`、最长同 bin run 为 `3`、小滞后自相关 `0.006609`，均未表现出强 pairwise sample/data RO 锁定特征；w0 与 w12 对照的最长 run 同样为 `3`。但是，同一 w10 窗口的 direct sampler-register snapshot 仍显示固定 sampled-bit 偏置：`sampler_island_w10_cap1024` 的整体 `rand p1=0.466797`、`rand min-H=0.907243`，最坏 sampled bit 为 `b10 line1/ro2`，`p1=0.570313`。因此，w10 贴近 restart cutoff 更可能来自完整 sampler-side physical path 中的采样寄存器、局部路由、采样孔径和输出映射，而不是单个 sample/data RO pair 的直接硬锁定。

### 4.3 restart warmup 暴露固定位置偏置

random3 连续流表现接近理想，但 formal restart 在 warmup0/8/10 下失败，在 warmup11/12/16 下通过。repeat02 复现了 warmup10 fail、warmup11/12 pass 的边界。这说明 restart 后前若干 packed bytes 属于不稳定窗口，存在固定采样位置偏置热点。

该发现具有两点意义：

1. 连续流 non-IID 高熵估计不能保证 restart 初始状态安全；
2. warmup 可以通过跳过 startup transient 降低固定位置偏置，但需要设计级评估，而不能凭经验选择。

进一步地，本文对已有 `1000x125` packed restart 数据做 bit-order / packing 离线反事实分析。对 31 个有效 restart 数据，MSB-first、LSB-first 和 byte-order reversal 会把同一个物理 `byte.bit` 热点映射到不同 SP800-90B expanded column；31/31 个 run 的 MSB/LSB 列号均发生移动，31/31 个 run 的 byte-order reversal 列号也发生移动。这说明“第几列”本身不是稳定物理实体，而是固定采样位置经过输出 packing 后的投影。因此本文后续采用更谨慎的表述：restart 失败暴露的是 fixed sampled-position / fixed output-position bias，而不是某个 column number 的固有物理属性。该结论避免把后处理矩阵列号误写成 FPGA 物理位置，也使 restart 证据更适合与 sampler-side implementation 机制关联。

### 4.4 sample RO 双向反事实形成核心机制证据

为了区分 readout/control 与 sampler-side physical implementation，本文构建 compact FIFO diagnostic 与 formal auto restart 的反事实对照。结果如下：

| direction | top design | sample RO implementation | warmup | overall p1 | min-H | worst position | worst x |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 4 | 0.376651 | 0.681888 | byte0.bit5 | 884 |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 5 | 0.373430 | 0.674452 | byte2.bit2 | 757 |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 5 repeat | 0.373541 | 0.674708 | byte1.bit2 | 792 |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 11 | 0.464819 | 0.901901 | byte18.bit4 | 576 |
| reverse repair | formal auto restart | compact-routed sample RO locked | 4 | 0.499419 | 0.998325 | byte61.bit6 | 552 |
| reverse repair | formal auto restart | compact-routed sample RO locked | 4 repeat | 0.499754 | 0.999290 | byte109.bit4 | 552 |

forward 实验说明：在 compact diagnostic 结构中，仅将 sample RO 锁到 formal routed 位置，即可将原本 near-ideal 的 passband 拉回强偏置失败。reverse 实验说明：在 formal auto restart 中，仅将 sample RO 锁到 compact routed 位置，又能将 warmup4 失败修复到接近理想。

这形成了目前最强的因果闭环：

```text
compact top + formal sample RO -> strong fail
formal top + compact sample RO -> near ideal repair
```

因此，sample RO 及其局部物理邻域必须纳入 RO-TRNG 熵源边界。

### 4.5 采样端 passband 迁移进一步区分 sample RO 与 sampler island

为了进一步区分 sample RO 单独作用与采样寄存器/局部路由共同作用，本文补充了 `random1` 的 strict restart passband 实验。该实验使用 pre-open UART 协议，采集 `8-byte header + 1000 x 125-byte payload`，随后严格剥离 header，将 payload 展开为 MSB/LSB 两种 `1000 x 1000` bit-symbol restart 输入并运行 `ea_restart`。旧的 `125000` byte preopen capture 因包含 header 且少一行 payload，仅作为诊断数据，不作为正式 restart 证据。

结果如下：

| variant | warmup | MSB restart | LSB restart | X_max | packed p1 | 解释 |
| --- | ---: | --- | --- | ---: | ---: | --- |
| sample RO local only | 4 | pass | pass | 553 | 0.499286 | sample RO local 后该启动窗口被修复 |
| sample RO local only | 5 | fail | fail | 713 | 0.410871 | 相邻窗口强偏置 |
| sample RO local only | 10 | pass | pass | 550 | 0.500648 | 第二个可用窗口 |
| sample RO local only | 11 | fail | fail | 666 | 0.422998 | 相邻窗口再次失败 |
| sample RO + regs local | 4 | pass | pass | 551 | 0.499770 | sampler island 保持早期窗口可用 |
| sample RO + regs local | 5 | pass | pass | 549 | 0.500804 | sampler island 修复 sample-only 的 w5 失败 |
| sample RO + regs local | 10 | boundary | boundary | 610 / 599 / 593 | 0.451448 / 0.458774 / 0.457368 | 近阈值边界窗口，repeat01 因 cutoff 贴边出现 MSB/LSB 分裂，repeat02/03 双通过 |
| sample RO + regs local | 11 | pass | pass | 594 | 0.470665 | sampler island 修复 sample-only 的 w11 失败 |

该结果说明，restart warmup 不是“等待越久越好”的单调过程，而是一个由采样端物理实现决定的 startup passband。只移动 sample RO 时，`w4/w10` 通过而相邻的 `w5/w11` 失败；加入本地采样寄存器和局部路由后，`w5/w11` 被修复，而 `w10` 移动到 restart cutoff 附近。第一次 strict run 中 `X_max=610`，高于 MSB cutoff `605`、低于 LSB cutoff `632`，因此表现为 MSB 失败、LSB 通过；随后两次定点 repeat 的 `X_max` 分别为 `599` 和 `593`，MSB/LSB 均通过。因此 `w10` 应解释为 near-threshold startup window，而不是稳定的 bit-order 缺陷。这进一步支持：采样寄存器、局部路由和采样孔径不是被动读出路径，而会改变 restart 后固定采样位置的偏置窗口。

与 w10 对齐的 TDC/snapshot 结果进一步约束了这个解释：两路 TDC 没有看到 w10 的 sample/data hard-lock 异常，但真实 sampler-register snapshot 在 w10 仍能看到固定 sampled-position bias，且 sampler-island 会改变最坏 sampled bit 的位置。这说明 TDC 的负结果并不削弱 sampler-side boundary 主张，反而帮助排除了过度简单的 RO-RO 锁定故事，把机制定位到采样寄存器、局部路由和采样孔径这一层。

随后补充的 `sampler_island_local w5/w11` direct sampler-register snapshot 提供了 w10 两侧 pass 点对照。w5、w10、w11 的 worst sampled-bit abs bias 分别约为 `0.067383`、`0.070313`、`0.067383`，64 个 sampled bits 的平均 p1 也都在 `0.523` 附近；但最终 `rand_bit` p1 分别为 `0.509766`、`0.466797`、`0.500977`。进一步的 pairwise correlation / mutual information 分析显示，w10 的增强主要集中在同一 `data_ro` 跨不同 sample line 的 bit pair：`same_data_ro` 类别的 mean abs r 从 w5/w11 的约 `0.493/0.497` 提高到 `0.538`，mean MI 从约 `0.274/0.275` 提高到 `0.304`；而同一 line 内不同 RO 的相关性仍很低。因此，w10 的 near-cutoff 行为不是单个 sampled bit 突然恶化，而是 startup window 改变了同一 data RO 在多相采样路径中的重复观测相关结构，并通过采样端组合路径影响最终输出。该结果进一步支持 sampler-side physical path/window effect，而不是单个 RO pair 的直接锁定。

### 4.6 reduced-XOR 硬件反事实验证 sampler-vector 组合边界

为了验证 4.5 节中的 same-data-RO cross-line 相关结构是否只是离线 snapshot 分析现象，本文构建了 `RO_TRNG_restart_reduced_xor_top`。该 top 保留 restart auto-stream、UART header 和 `1000 x 125-byte` row-major payload 协议，只改变送入 FIFO 的 bit 函数：

- `all64`：原始 64 个 sampled bits 的 XOR；
- `data_ro[j]`：同一个 data RO index `j` 在 8 条 sample line 上的 XOR；
- `except_data_ro[j] = all64 XOR data_ro[j]`：去掉该 same-data-RO 方向后的互补组合。

所有 reduced-XOR capture 均为真实硬件 restart 数据，header 为 `A55A03E8007D01D0`。在最关键的 `sampler_island_local warmup10` 边界窗口，方向图结果如下：

| mode | index | p1 | abs bias | min-H | 解释 |
| --- | ---: | ---: | ---: | ---: | --- |
| all64 | all | 0.458617 | 0.041383 | 0.885279 | 完整组合轻度低偏，但远好于最坏单方向 |
| data_ro | 0 | 0.191877 | 0.308123 | 0.307353 | 强低偏方向 |
| data_ro | 2 | 0.244002 | 0.255998 | 0.403546 | 强低偏方向 |
| data_ro | 3 | 0.671833 | 0.171833 | 0.573825 | 强高偏方向 |
| except_data_ro | 0 | 0.501020 | 0.001020 | 0.997060 | 互补组合近理想 |
| except_data_ro | 2 | 0.499674 | 0.000326 | 0.999060 | 互补组合近理想 |
| except_data_ro | 6 | 0.501833 | 0.001833 | 0.994721 | 互补组合近理想 |

进一步的最小 repeat02 覆盖 `all64`、`data_ro0/2/3` 和 `except_data_ro0/2/6`。强低偏方向在 repeat02 中稳定复现：`data_ro0` 的 p1 从 `0.191877` 到 `0.187682`，`data_ro2` 从 `0.244002` 到 `0.244767`；强高偏方向 `data_ro3` 从 `0.671833` 到 `0.670937`。同时，互补组合仍接近理想：`except_data_ro0` 从 `0.501020` 到 `0.499872`，`except_data_ro2` 从 `0.499674` 到 `0.500863`，`except_data_ro6` 从 `0.501833` 到 `0.501224`。

该结果把机制证据从“相关结构观察”推进到“硬件反事实验证”。单个 same-data-RO 方向本身可以是严重偏置的真实硬件输出函数；但最终 `all64` 输出不是由某一个坏方向单独控制，而是由多个方向和其互补组合在 XOR 边界上的抵消关系决定。换言之，`sampler_island_local w10` 的 near-cutoff 行为应写成 sampler-side sampled-vector 的组合/抵消边界，而不是单个 RO pair hard-lock、单个 worst sampled bit 或单个 data_ro group 的失效。

论文图表由离线脚本生成：

```text
scripts/make_reduced_xor_paper_artifacts_20260527.py
data/experiments/reduced_xor_paper_artifacts_20260527/
```

## 5. 讨论

### 5.1 为什么不能写成“RO 硬锁定”

如果坏 placement 的主因是简单 pairwise RO hard locking，则 TDC 应出现持续同 bin 驻留、长 run 或明显小滞后相关。然而现有 pair-specific、sampler-data 和 clean reset-aligned TDC 均没有支持这一点。更合理的解释是：placement 通过 sampler-side physical implementation 改变采样相位覆盖、采样寄存器孔径、局部路由延迟和 startup transient；这些效应不一定表现为两个 RO 之间的强 Pearson correlation。reduced-XOR 结果进一步说明，即使没有强 pairwise hard-lock，不同 same-data-RO 方向仍可形成强偏置硬件函数，最终输出质量取决于采样向量内部的组合和抵消。

### 5.2 TDC 的真实作用

TDC 在本文中的角色是机制约束，而不是唯一因果证明。它排除了过度简单的解释，并帮助将机制定位到采样路径。dedicated code-density calibration 进一步说明 raw bin 非线性真实存在；LUT 敏感性复算也说明校准映射不会推翻当前 hard-lock 排除结论。但在没有 per-run before/after calibration 和不确定度评估前，本文仍避免把 TDC 写成严格绝对 ps 级 jitter 测量。

### 5.3 对 RO-TRNG 设计的启示

本文结果表明，RO-TRNG 设计不应只约束 data RO 阵列。至少应同时考虑：

- sample RO 的 LOC/BEL 和邻近资源；
- sampling registers 的 LOC/BEL；
- sample RO 到采样寄存器的局部路由；
- restart 后的 warmup window；
- 64-bit sampled-vector 的 XOR 组合边界，而不只是单个 RO 或单个 sampled bit；
- PVT 条件下 startup transient 的变化；
- placement matrix 的统计比较，而不是单个好 seed。

## 6. 局限性与下一步工作

当前结果仍有以下限制：

1. 主要数据来自单块 Zynq-7020 板卡。高水平投稿前需要多板复现 sample RO 双向反事实和 reduced-XOR 最小诊断集合。
2. TDC 已完成 8 MiB dedicated code-density calibration、lane-swap、clean32k LUT 复算和 pair-specific fixed-LUT 复算，但仍缺少 per-run before/after calibration 和多板 calibration。
3. XADC 主要为 after-only；auto-stream 与 before_capture XADC 存在时序冲突，后续应补 command-gated capture。
4. SP800-90B 结果应写成 entropy assessment / restart evidence，而不是完整认证。

下一步优先级：

1. 多板复现 `compact top + formal sample RO` forward fail、`formal top + compact sample RO` reverse repair，以及 `sampler_island_local w10` 的 reduced-XOR 最小集合：`all64`、`data_ro0/2/3`、`except_data_ro0/2/6`。
2. 补一组 calibration repeat 或多板 calibration，评估 LUT 非线性结构的跨时间/跨板稳定性。
3. 实现 command-gated restart/TDC，确保 before/after XADC 与 calibration 不干扰 UART header。
4. 增加 command-gated before/after XADC、all-on/single-on TDC 对照和 reduced-XOR 邻近 warmup 小集合，用于进一步区分采样孔径、输出映射、局部开关活动和 XOR 抵消边界。
5. 将当前中文初稿扩展为英文投稿稿，补充 related work 和 formal methodology。

截至 2026-05-27，restart bit-order/packing 反事实已完成，并已支持“fixed sampled-position bias exposed by packing”的谨慎表述；all-on/single-on 的 TDC mask-perturb 版本也已完成 RTL、XDC、bitstream 和 1MiB 硬件 smoke。smoke 数据显示新 top 可稳定输出 `131071` 个 TDC packet，`phase_pearson_r=-0.000707`，最长同 differential-bin run 为 3。reduced-XOR 方向图和最小 repeat02 已完成，支持“same-data-RO 方向偏置 + sampler-vector XOR 抵消”的机制表述。后续 P0 矩阵将比较 `pair_only`、`all_data_on` 和 `pair_plus_sample`，用于判断局部开关活动是否改变 phase diffusion；高水平投稿前更优先的是多板复现 reduced-XOR 最小诊断集合。

## 7. 结论

本文通过真实 FPGA 硬件实验表明，RO-TRNG 的 placement 敏感性不能只从 RO 阵列本身解释。TDC 结果未显示强 pairwise hard locking，排除了简单锁定故事；SP800-90B restart 暴露出连续流统计无法覆盖的 startup fixed-position bias；sample RO 双向反事实进一步证明，采样端物理实现可以在两个方向翻转 restart outcome；reduced-XOR 硬件反事实则说明，单个 same-data-RO 方向可以强偏置，而最终输出质量来自 sampled-vector 的 XOR 组合和抵消。由此可见，sample RO、采样寄存器、局部路由、采样孔径和组合边界应被视为物理熵源边界的一部分。该结论对 FPGA TRNG 的 placement 约束、restart 评估和机制验证方法具有直接意义。

## 附录 A：关键复现入口

```text
doc/reproduce_key_experiments_20260525.md
doc/sample_ro_locked_passband_results_20260525.md
doc/tdc_reset_aligned_clean32k_status_20260525.md
data/experiments/sample_ro_counterfactual_20260525/
data/experiments/tdc_clean32k_figures_20260525/
data/experiments/tdc_code_density_cal_20260525/
data/experiments/mechanism_evidence_chain_20260525/
doc/reduced_xor_counterfactual_status_20260526.md
data/experiments/reduced_xor_paper_artifacts_20260527/
```
