# 采样端 Passband 机制更新 2026-05-26

## 目的

这份文档记录 `random1` 采样端 passband 实验的最新结论，重点修正 `sampler_island_local warmup10` 的解释。

论文中不应再把 `warmup10` 写成稳定的 MSB-only failure 或稳定 bit-order defect。它更准确的定位是：

```text
sampler_island_local warmup10 是 restart passband 的近阈值边界点。
```

## Strict 8 点矩阵

所有正式结果都来自 strict capture：

```text
8-byte header + 1000 x 125-byte payload = 125008 bytes
header = A55A03E8007D01D0
```

| variant | warmup | MSB restart | LSB restart | X_max | packed p1 | 机制解释 |
| --- | ---: | --- | --- | ---: | ---: | --- |
| sample RO local only | 4 | pass | pass | 553 | 0.499286 | 只移动 sample RO 后，该启动窗口被修复 |
| sample RO local only | 5 | fail | fail | 713 | 0.410871 | 相邻 warmup 窗口强偏置 |
| sample RO local only | 10 | pass | pass | 550 | 0.500648 | 第二个被修复窗口 |
| sample RO local only | 11 | fail | fail | 666 | 0.422998 | 相邻 warmup 窗口再次失败 |
| sample RO + regs local | 4 | pass | pass | 551 | 0.499770 | sampler island 保持早期窗口可用 |
| sample RO + regs local | 5 | pass | pass | 549 | 0.500804 | sampler island 修复 sample-only 的 w5 失败 |
| sample RO + regs local | 10 | boundary | boundary | 610 / 599 / 593 | 0.451448 / 0.458774 / 0.457368 | 近阈值 passband-edge，见 repeat |
| sample RO + regs local | 11 | pass | pass | 594 | 0.470665 | sampler island 修复 sample-only 的 w11 失败 |

## Warmup10 单板 Repeat

| repeat | packed p1 | worst byte.bit | X_max | MSB restart | LSB restart | 解释 |
| --- | ---: | --- | ---: | --- | --- | --- |
| repeat01 | 0.451448 | 4.2 | 610 | fail, cutoff 605 | pass, cutoff 632 | 恰好高于 MSB cutoff、低于 LSB cutoff |
| repeat02 | 0.458774 | 4.4 | 599 | pass, cutoff 605 | pass, cutoff 632 | 低于两个 cutoff |
| repeat03 | 0.457368 | 18.0 | 593 | pass, cutoff 605 | pass, cutoff 632 | 再次低于两个 cutoff |

repeat02 和 repeat03 说明第一次的 MSB/LSB 分裂不是稳定的 bit-order 缺陷，而是由于 `X_max` 贴近 SP800-90B restart cutoff。这个点仍然有机制价值：它证明 sampler island 把启动窗口移动到了 restart sanity 边界附近，而不是简单、单调地“warmup 越多越好”。

## 论文表述建议

推荐写法：

```text
sampler-island warmup10 lies at the edge of the restart passband. In the first strict run, X_max=610 exceeded the MSB cutoff of 605 but remained below the LSB cutoff of 632, causing an apparent bit-order split. Two targeted repeats moved X_max to 599 and 593, passing both orders. This indicates a near-threshold startup window rather than a deterministic bit-order defect.
```

中文写法：

```text
sampler-island warmup10 位于 restart passband 边缘。第一次 strict run 中 X_max=610，高于 MSB cutoff=605、低于 LSB cutoff=632，因此表现为 MSB 失败、LSB 通过；两次定点 repeat 中 X_max 分别降至 599 和 593，MSB/LSB 均通过。这说明该点是近阈值 startup window，而不是稳定的 bit-order 缺陷。
```

避免写法：

```text
warmup10 always fails in MSB but passes in LSB.
warmup10 是稳定的 MSB-only failure。
```

## 对主机制的影响

这个结果没有削弱 sampler-side boundary 主张，反而让机制更可信：

- `sample_ro_local_only` 呈现非单调 passband：`w4/w10` pass，`w5/w11` fail；
- `sample_ro_plus_regs_local` 改写 passband：`w5/w11` 被修复，`w10` 移到 cutoff 附近；
- 因此 sample RO 不是唯一因素，采样寄存器、局部路由和采样孔径也会改变 restart startup window；
- TDC 已排除简单 hard locking 后，restart passband 迁移是目前最强的 sampler-side 机制证据之一。

## w10 对齐 TDC / Snapshot 结果

已经完成与 `sampler_island_local warmup10` 对齐的 reset-aligned TDC：

| label | H(diff) | early H(diff) | transition H(diff) | same diff ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| sampler_local_w0 | 6.654635 | 6.438881 | 12.943902 | 0.013031 | 3 | -0.000826 |
| sampler_local_w10 | 6.638003 | 6.444923 | 12.921799 | 0.011841 | 3 | 0.006609 |
| sampler_local_w12 | 6.733557 | 6.502390 | 13.099310 | 0.010651 | 3 | 0.001855 |

该结果没有显示 w10 存在明显 pairwise sample/data RO hard-lock signature。也就是说，w10 贴近 cutoff 不应被解释成 sample RO 和某个 data RO 的简单硬锁定。

同时，同一窗口的 direct sampler-register snapshot 显示：

| probe | rand p1 | rand min-H | stage_xor H | worst sampled bit | worst abs bias |
| --- | ---: | ---: | ---: | --- | ---: |
| regs_only_w10_cap1024 | 0.455078 | 0.875879 | 7.827542 | b6 line0/ro6 | 0.066406 |
| sampler_island_w10_cap1024 | 0.466797 | 0.907243 | 7.806656 | b10 line1/ro2 | 0.070313 |

这说明 TDC 的价值在这里是“排除项 + 定位项”：它排除了最简单的两 RO 锁定解释；而 sampler snapshot 在真实采样路径上仍然看到了固定 sampled-position bias。因此，w10 贴近 restart cutoff 更可能由采样寄存器、局部路由、采样孔径和 output packing 共同形成。

## w5/w10/w11 Snapshot 三点对照

为验证 w10 两侧 pass 点是否表现不同，已补充 `sampler_island_local w5/w11` 的同类 direct sampler-register snapshot：

| warmup | restart reference | rand p1 | rand min-H | sampled bit mean p1 | worst bit abs bias | bits p1 > 0.55 | stage_xor mean p1 | 解释 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 5 | pass | 0.509766 | 0.972094 | 0.523621 | 0.067383 | 9 | 0.498047 | pass 侧对照，最终 rand 接近 0.5 |
| 10 | boundary | 0.466797 | 0.907243 | 0.523178 | 0.070313 | 12 | 0.510132 | near-cutoff 边界，最终 rand 明显偏低 |
| 11 | pass | 0.500977 | 0.997185 | 0.524139 | 0.067383 | 13 | 0.499756 | pass 侧对照，最终 rand 几乎理想 |

这个结果把机制又推进了一步：w10 不是因为单个 sampled bit 突然更坏。三者的 worst bit abs bias 都在 `0.067` 到 `0.070` 附近，64 个 sampled bits 的平均 p1 也都偏高到约 `0.523`。真正区分 w10 与 w5/w11 的，是 sampled bits 之间的相关结构和组合关系。需要注意的是，snapshot 同一帧中的 `rand_bit` 是寄存器输出，不一定严格等于同一帧 `sampled_data` 的即时 XOR，因此 XOR 消融应解释为 sampled-state 组合结构诊断，而不是逐帧等式证明。

pairwise correlation / mutual information 分析进一步显示，w10 的增强主要集中在同一 `data_ro` 跨不同 sample line 的 bit pair：`same_data_ro` 类别的 mean abs r 从 w5/w11 的约 `0.493/0.497` 提高到 `0.538`，mean MI 从约 `0.274/0.275` 提高到 `0.304`；而 `same_line` 和 `diff_line_diff_ro` 的相关性仍很低。这说明 w10 near-cutoff 更像是多相采样下同一 data RO 的重复观测相关增强，并通过采样端组合路径影响最终输出。

因此，论文中可以把 w10 写成：

```text
The w10 boundary is not a single worst-bit effect. The sampled-register marginal biases remain comparable to the neighboring pass windows, but pairwise correlation and mutual information increase mainly among bits belonging to the same data RO and captured at different sample stages. This indicates a startup-window-dependent sampler-side correlation and XOR-combination effect rather than a single-bit bias or pairwise RO hard lock.
```

## Reduced-XOR 硬件反事实

新增 `RO_TRNG_restart_reduced_xor_top` 后，已经完成 `sampler_island_local w5/w10/w11` 的 `data_ro0` 与 `data_ro2` reduced-XOR 真实硬件 restart capture。这个实验只改变 FPGA 内部送入 FIFO 的输出函数，保留原 restart auto-stream/UART/header/row-major 流程，因此比 snapshot 事后 XOR 更直接。

结果显示，单个 `data_ro` 方向本身可以极强偏：

| group | w5 p1 | w10 p1 | w11 p1 |
| --- | ---: | ---: | ---: |
| data_ro0 | 0.206684 | 0.191877 | 0.208462 |
| data_ro2 | 0.232207 | 0.244002 | 0.230227 |

这把机制进一步推进了一层：`same_data_ro` cross-line 结构确实能被真实硬件输出函数放大，但 w10 near-cutoff 不能解释成“某一个 data_ro group 独坏”。更合理的说法是：多个 data_ro 方向的强偏在 all64 XOR 中发生抵消；warmup window 改变的是这些强偏 group 与 complement group 的组合抵消关系。下一步应做 `except_data_ro0/2 = all64 XOR data_ro0/2`，直接验证抵消链路是否在 w10 变弱。

## 后续最有价值实验

单板上不建议继续大量重复相同 `w10`。更有价值的后续实验是：

1. 多板重复 `sample_ro_local_only w5/w11` 与 `sampler_island_local w5/w10/w11`，验证 passband 迁移是否跨板保留；
2. 在同一单板上做 XADC 温度/电压记录下的短 repeat，观察 near-threshold `w10` 是否随温度轻微漂移；
3. 如果要进一步靠近物理机理，做与该 restart window 对齐的 TDC startup capture，而不是继续刷同一 restart 文件。
