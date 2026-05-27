# w10 Startup Window 对齐 TDC 状态 2026-05-26

## 目标

解释 `random1 sampler_island_local warmup10` 为什么贴近 SP800-90B restart cutoff。具体问题是：

```text
w10 的 near-threshold 行为是否能在 sample RO 与 data RO0 的 reset-aligned TDC 中看到相位扩散不足或硬锁定？
```

## 已完成硬件 capture

### 1. reset-aligned TDC

- bitstream: `data/vivado_runs/fpga1_tdc_reset_aligned/tdc_reset_random1_sampler_local_ro0_clean32k_warmup10/RO_TDC_reset_aligned_top.bit`
- raw capture: `data/hardware/20260511_fpga1_board1/tdc_reset_aligned/tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525.bin`
- bytes: `262160`
- header: `5444435201E60501000A000080881352`
- SHA256: `771CF7F6EEB6973703D31AD8F1987C4F78764BFCD0CA403EF8D9BFE32930709A`
- XADC after: `45.6 C`, `VCCINT=1.000 V`, `VCCAUX=1.797 V`, `VCCBRAM=1.000 V`

该 TDC 观测：

```text
lane A = local sample RO at x45y39
lane B = random1 data RO0 at x44y39
warmup packets = 10
capture packets = 32768
sample divider = 5000
```

### 2. direct sampler-register snapshot

- bitstream: `data/vivado_runs/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup10_cap1024/RO_TRNG_sampler_snapshot_top.bit`
- raw capture: `data/hardware/20260511_fpga1_board1/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup10_cap1024_20260526.bin`
- bytes: `16400`
- header: `534E4150011C000A00000408080955AA`
- SHA256: `7DAAE128F6516F573A9D65F037C200E7C3AA890825CF9351635A32DED151152A`
- XADC after: `46.1 C`, `VCCINT=1.000 V`, `VCCAUX=1.797 V`, `VCCBRAM=1.000 V`

## 关键结果

### TDC 对照

| label | H(diff) | early H(diff) | transition H(diff) | same diff ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| sampler_local_w0 | 6.654635 | 6.438881 | 12.943902 | 0.013031 | 3 | -0.000826 |
| sampler_local_w10 | 6.638003 | 6.444923 | 12.921799 | 0.011841 | 3 | 0.006609 |
| sampler_local_w12 | 6.733557 | 6.502390 | 13.099310 | 0.010651 | 3 | 0.001855 |

结论：w10 没有表现出强 pairwise sample/data RO 锁定、长同-bin 驻留或明显小滞后自相关。因此，不能把 w10 贴近 restart cutoff 简单解释为 sample RO 与某个 data RO 的硬锁定。

### Sampler snapshot 对照

| probe | rand p1 | rand min-H | stage_xor H | worst sampled bit | worst bit p1 | worst abs bias |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| regs_only_w10_cap1024 | 0.455078 | 0.875879 | 7.827542 | b6 line0/ro6 | 0.566406 | 0.066406 |
| sampler_island_w10_cap1024 | 0.466797 | 0.907243 | 7.806656 | b10 line1/ro2 | 0.570313 | 0.070313 |

结论：直接观察真实 sampler-register path 时，w10 仍存在固定 sampled-bit 偏置，而且 sampler-island 会改变最坏 bit 的物理位置。这比两路 TDC 更贴近 restart 失败模式。

## 机制解释

w10 的证据链现在应写成：

1. strict restart repeat 证明 w10 是 near-threshold startup window：`X_max=610/599/593`，贴近 MSB cutoff `605`；
2. w10-aligned TDC 排除了最简单的 sample/data pairwise hard locking 解释；
3. w10 sampler snapshot 显示真实采样寄存器路径仍有固定 sampled-position bias；
4. 因此，w10 贴近 cutoff 更可能来自完整 sampler-side physical implementation：sample RO、sampling registers、local routing、aperture 和 output packing 的共同作用。

这让 TDC 的角色更清晰：TDC 不是单独证明 restart 失败原因，而是把错误解释排除掉，并把机制定位到 sampler-side boundary。

## 下一步建议

单板上不建议继续重复相同 w10 TDC。更有价值的后续实验是：

1. `sampler_island_local w5/w11` 的同类 direct sampler snapshot 已完成，见 `data/experiments/sampler_snapshot_island_w5_w11_20260526/sampler_island_w5_w10_w11_snapshot_compare_20260526.md`；
2. 多板重复 `sample_ro_local_only w5/w11` 与 `sampler_island_local w5/w10/w11`，确认 passband 迁移是否跨板成立；
3. 如果要进一步增强 TDC 正证据，做 full-sampler-aware TDC 或 command-gated before/after calibration，而不是继续只看单个 sample/data RO pair。

## 2026-05-26 补充：w5/w11 snapshot 对照

新增 `sampler_island_local w5/w11` direct sampler-register snapshot 后，三点对照如下：

| warmup | restart reference | rand p1 | rand min-H | sampled bit mean p1 | worst bit abs bias | stage_xor mean p1 | 解释 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 5 | pass | 0.509766 | 0.972094 | 0.523621 | 0.067383 | 0.498047 | pass 侧对照，最终 rand 接近 0.5 |
| 10 | boundary | 0.466797 | 0.907243 | 0.523178 | 0.070313 | 0.510132 | near-cutoff 边界，最终 rand 明显偏低 |
| 11 | pass | 0.500977 | 0.997185 | 0.524139 | 0.067383 | 0.499756 | pass 侧对照，最终 rand 几乎理想 |

这个结果进一步说明：w10 的边界性不是某个 sampled register bit 的偏置突然变大，因为 w5/w10/w11 的 worst bit bias 很接近。差异出现在 64 个 sampled bits 被 XOR 成 `rand_bit` 的组合层：w5/w11 中偏置大体抵消，而 w10 中相关结构/相位窗口让最终输出偏低。因此机制应写成 sampler-side startup window + XOR-combination/correlation effect。
