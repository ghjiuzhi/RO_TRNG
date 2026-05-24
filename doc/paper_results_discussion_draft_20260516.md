# Results and Discussion Draft - 2026-05-16

本文档是面向论文正文的中文草稿，重点整理当前已经有真实硬件数据支撑的 Results/Discussion 叙事。文中所有结论都按“当前板卡、当前 RTL、当前采集流程”限定，避免把单板 fast-mode 结果写成完整认证或普适规律。

## 结果 1：placement 造成原始 bitstream 统计质量显著分层

在相同 FPGA 板卡、相同 RO-TRNG RTL 和相同 UART 采集/分析链路下，不同 placement 产生了显著不同的原始 bitstream 统计质量。10 MiB formal capture 的结果显示，`random1` placement 出现强 bias：`p1=0.337315512`，bit min-entropy 为 `0.593605945`，runs p-value 为 `0`，相邻 bit 相等比例达到 `0.556739754`。与此相对，`random3` placement 在同样采集规模下接近均衡：`p1=0.499968565`，bit min-entropy 为 `0.999909299`，runs p-value 为 `0.18437283`，相邻 bit 相等比例为 `0.500072473`。这一对照说明，在相同逻辑结构和采集链路下，placement 本身足以把 raw entropy source 从严重偏置推向接近理想的观测状态。

完整 placement matrix 进一步排除了只挑选两个极端样本的解释。`sparse` placement 的 bit min-entropy 为 `0.900637067`，`row` 为 `0.925712657`，`far/random2` 约为 `0.975`，而 `compact`、`checker`、`cross_region` 和 `random3` 均接近 `1.0`。这些结果更像一个 placement-induced quality spectrum，而不是单个异常 bitstream。尤其值得注意的是，`same_column` 的 `p1=0.499930251`，bit min-entropy 为 `0.99979876`，但 runs p-value 为 `0`，相邻 bit 相等比例为 `0.505979735`。这说明单看 bias 或一阶 min-entropy 可能会误判 TRNG 质量，序列结构指标必须和 bias 一起报告。

该结果的论文价值在于：placement 不应被看作“手动摆放技巧”，而应被看作 RO-TRNG entropy-source characterization 中的实验控制变量。本文不把某一种 placement 宣称为通用最优，而是证明在同一设计中，物理布局可显著改变输出统计质量，并且这种改变能被 continuous bitstream、repeat capture 和后续 restart 行为共同观察到。

## 结果 2：repeat 结果支持 placement-level 现象不是单次采集偶然

已有 repeat capture 支持 placement-level 现象具有重复性。`random1` 的 repeat 仍保持强 bias，repeat `p1_mean=0.338143095`，bit min-entropy mean 为 `0.595409129`，runs p-value mean 为 `0`。`random3` repeat 仍保持近均衡，repeat `p1_mean=0.499943098`，bit min-entropy mean 为 `0.999835828`。这说明 `random1` 和 `random3` 的差异不是一次串口采集、一次文件转换或一次分析脚本运行造成的偶然误差。

当前 repeat 矩阵仍不完整。多数 placement 仍只有 10 MiB formal 一次和少量 5 MiB repeat。因此论文中应将现有 repeat 写作“supporting repeat evidence”，而不是完整统计置信区间。下一轮硬件已经准备好 20 MiB placement repeat 队列，补齐 `same_column`、`sparse`、`far`、`compact`、`checker`、`random2`、`row`、`cross_region` 后，可以把该部分升级为更强的 statistical comparison。

## 结果 3：RO 全开产生可测频率拉拽，但不能单独解释所有随机性差异

RO_FREQ 结果显示，多 RO 同时运行时存在可测的频率扰动。`random1` 中 data RO 的 all-on vs single-on 平均频移为 `-0.185041 MHz`，mean absolute shift 为 `421.577 ppm`；sample RO 的 shift 为 `0.310931 MHz`，约 `3466.91 ppm`。`random3` 中 data RO 的平均频移为 `-0.209355 MHz`，mean absolute shift 为 `478.085 ppm`；sample RO 的 shift 为 `-0.075703 MHz`，约 `-824.556 ppm`。

这一结果支持一个较稳妥的机制判断：RO 阵列不是完全独立的理想振荡源，placement 可能通过局部布线、电源网络、衬底、逻辑资源邻近和采样路径改变振荡器的动态行为。与此同时，频率拉拽本身不能单独解释所有统计差异。`random1` 和 `random3` 都存在 all-on 频率扰动，但它们的 raw TRNG 质量截然不同。因此，论文中应把 RO_FREQ 作为机制诊断链的一环，而不是唯一因果证据。

## 结果 4：TDC pair 结果没有支持“强 pair-level 相位锁定”这一简单解释

为检查坏随机性是否可由近邻 RO 的强相位锁定解释，本文对六组 pair-specific TDC capture 做了窗口化分析。每组 capture 划分为 16 个窗口，共 96 个窗口。结果显示，`strong_lock_windows=0`，最大 small-lag absolute correlation 仅为 `0.0317827`，各组 `diff_std_ps_mean` 约为 `2040-2043 ps`。

因此，当前数据不支持把 placement 差异简单写成“近距离 RO 强锁定导致熵下降”。更稳妥的说法是：在已监测的六个 pair 和当前条件下，没有检测到强 pair-level locking；placement 对随机性的影响更可能来自多 RO 网络的弱耦合、频率接近、采样相位覆盖、启动瞬态和序列结构共同作用。TDC 结果的价值不是证明某个单一机制，而是限制机制解释空间，避免论文落入过强的锁定叙事。

还需要强调，当前 TDC 应表述为 relative/code-density-normalized diagnostic。除非后续完成 code-density calibration，否则不能把 TDC bin 当成严格线性的 ps 级时间轴。

## 结果 5：restart warmup 暴露 continuous stream 难以发现的固定列偏置

`random3` 是 continuous stream 中的好 placement，但 formal-size restart 实验揭示了更细的启动瞬态问题。每个 restart dataset 包含 1000 次 restart，每次输出 125 个 packed bytes，展开后为 1000 个 bit symbols。按 MSB-first 和 LSB-first 两种位序送入 `ea_restart` 后发现，不足 warmup 时存在固定 column/固定 raw byte-bit 位置偏置。

无 warmup 时，整体 `p1=0.497933000`，看似接近均衡，但最坏固定位置达到 `X=685`，超过 restart cutoff，说明 continuous stream 近均衡不能排除 restart 后相对位置上的稳定偏置。`WARMUP_BYTES=8` 时情况更糟，overall `p1=0.374385000`，超过 cutoff 的固定位置数达到 `893`，最坏 `X=721`。`WARMUP_BYTES=10` 仍失败，overall `p1=0.415017000`，超过 cutoff 的位置数为 `106`，最坏 `X=650`。当 warmup 增加到 11 bytes 后，超过 cutoff 的位置数降为 `0`，最坏 `X=583`，MSB/LSB 两种展开均通过；warmup12 和 warmup16 也保持通过。

边界附近的重复实验进一步支持该现象不是一次运行偶然。`WARMUP_BYTES=10` 的 run01 和 repeat02 均失败，最坏 `X` 分别为 `650` 和 `633`；`WARMUP_BYTES=11` 的 run01 和 repeat02 均通过，最坏 `X` 分别为 `583` 和 `588`；`WARMUP_BYTES=12` 的两次运行也均通过。因而，在当前板卡、当前 `random3` placement 和当前 auto-stream restart protocol 下，可以稳妥写作：观察到的 warmup transition 位于 `10 < WARMUP_BYTES <= 11`。

该结果是论文中最有机制价值的一段。它说明 high-quality continuous stream 并不保证 restart 条件下每个固定输出位置都稳定无偏；restart sanity 观察到的是“每次 restart 后相同相对位置”的列分布，这和普通连续流统计不同。warmup 的作用也不应被简单写成“提高随机性”，而应写成“移动或避开 restart 后早期不稳定/偏置采样窗口”。这种表述既准确，也能把 SP800-90B restart 的意义讲清楚。

## 机制解释：placement 改变的是 entropy-source dynamics，而不是单个指标

把上述结果合在一起，最稳妥的机制叙事是：

1. placement 改变 RO 的物理邻近、布线延迟、频率分布和采样相位覆盖；
2. RO 全开时存在可测频率拉拽，说明多 RO 阵列存在动态扰动；
3. TDC pair 未观察到强 pair locking，说明不能用单个强锁定机制解释全部现象；
4. continuous stream 和 restart dataset 观察到的是不同随机性切面，前者反映长流统计，后者暴露 restart 后固定位置偏置；
5. warmup 可以把早期偏置窗口移出观测矩阵，从而改善 restart sanity 行为。

因此，论文主张应聚焦于“placement-sensitive entropy-source characterization”，而不是“某个 placement 策略一定更优”或“某种耦合机制已被证明”。更高级的贡献点是建立一条跨层证据链：physical placement -> RO frequency behavior -> TDC phase diagnostic -> continuous TRNG statistics -> restart fixed-column behavior。

## 局限性

当前结果仍应主动声明以下局限：

1. 主要证据来自单块 Zynq-7020 板卡，不能外推到所有 FPGA、所有板卡和所有 PVT 条件。
2. 旧 capture 没有 XADC 温度/电压 metadata；后续补采已准备自动记录 XADC before/after。
3. TDC 尚未完成独立 code-density calibration，因此只能作为相对相位/bin 分布诊断。
4. 当前 SP800-90B 相关结果应称为 non-IID smoke / `ea_restart` restart evidence，不能称为完整 SP800-90B certification。
5. placement repeat 矩阵和 placement restart 矩阵仍需上板补齐，才能支撑更强统计比较。

## 可放入论文摘要的凝练版本

本文面向 FPGA RO-TRNG 熵源，研究 placement 对原始随机性、RO 频率扰动、TDC 相位动态和 SP800-90B restart 行为的影响。在相同 RTL 与采集流程下，不同 RO placement 产生显著分层的 bitstream 统计质量：一个 random placement 出现强 bias（`p1=0.3373`，bit min-entropy `0.5936`），而另一个 random placement 接近均衡（`p1=0.49997`，bit min-entropy `0.99991`）。`same_column` 布局进一步表明，单独依赖 p1 或 min-entropy 会掩盖 runs 结构缺陷。RO 频率测量显示全开状态存在可测频率拉拽；六组 pair-specific TDC 捕获未观察到强相位锁定。最后，restart 实验揭示了 continuous stream 难以暴露的固定 column 启动偏置，并显示 11 字节以上 warmup 可在重复实验中消除该 restart failure。结果表明，placement 与启动对齐应作为 FPGA RO-TRNG 熵源评估的一等控制变量。

