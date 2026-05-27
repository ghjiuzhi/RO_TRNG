# w10 Startup Window Mechanism Evidence Chain 2026-05-26

## 结论

`sampler_island_local warmup10` 已被定位为 restart passband 的近阈值边界点。与该窗口对齐的 reset-aligned TDC 没有显示强 pairwise sample/data RO phase locking、长同-bin 驻留或显著小滞后自相关。因此，w10 贴近 SP800-90B restart cutoff 的原因不应写成“两个 RO 直接硬锁定”。

更合理的机制解释是：w10 位于采样端 startup passband 边缘；真实 restart sampler path 中的采样寄存器、局部路由、采样孔径和 output packing 共同决定固定采样位置偏置。直接 sampler-register snapshot 在同一 w10 窗口仍能看到固定 sampled-bit 偏置，这解释了为什么 restart sanity 会贴近 cutoff，而两路 TDC 只看到正常的相位扩散指标。

## Restart 边界证据

| run | packed p1 | worst byte.bit | X_max | MSB restart | LSB restart | 解释 |
| --- | ---: | --- | ---: | --- | --- | --- |
| repeat01 | 0.451448 | 4.2 | 610 | fail, cutoff 605 | pass, cutoff 632 | 刚好高于 MSB cutoff、低于 LSB cutoff |
| repeat02 | 0.458774 | 4.4 | 599 | pass, cutoff 605 | pass, cutoff 632 | 移到两个 cutoff 以下 |
| repeat03 | 0.457368 | 18.0 | 593 | pass, cutoff 605 | pass, cutoff 632 | 再次位于两个 cutoff 以下 |

这说明 w10 是 near-threshold startup window，而不是稳定的 MSB-only 或 bit-order 缺陷。

## 对齐 TDC 证据

| label | H(diff) | early H(diff) | transition H(diff) | same diff ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| sampler_local_w0 | 6.654635 | 6.438881 | 12.943902 | 0.013031 | 3 | -0.000826 |
| sampler_local_w10 | 6.638003 | 6.444923 | 12.921799 | 0.011841 | 3 | 0.006609 |
| sampler_local_w12 | 6.733557 | 6.502390 | 13.099310 | 0.010651 | 3 | 0.001855 |

w10 的 TDC 指标没有出现特别的长驻留、低 transition entropy 或强 autocorrelation。该结果是机制上有价值的负证据：它把解释从“简单 pairwise phase lock”推向“完整 sampler path 的固定采样位置偏置”。

## Sampler Snapshot 证据

| probe | rand p1 | rand min-H | stage_xor H | worst sampled bit | worst bit p1 | worst abs bias |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| regs_only_w10_cap1024 | 0.455078 | 0.875879 | 7.827542 | b6 line0/ro6 | 0.566406 | 0.066406 |
| sampler_island_w10_cap1024 | 0.466797 | 0.907243 | 7.806656 | b10 line1/ro2 | 0.570313 | 0.070313 |

直接 sampler-register snapshot 比两路 TDC 更贴近 restart 真实采样路径。它显示 w10 的固定 sampled-bit 偏置仍存在，而且 sampler-island 会改变最坏物理 bit 位置。这支持 sampler-side boundary 解释：采样寄存器和局部路由不是被动读出路径，而是熵源边界的一部分。

## 论文可用表述

可以写：

```text
For the sampler-island warmup10 boundary point, reset-aligned TDC did not reveal a pairwise sample/data RO hard-lock signature: the differential-bin residence time, transition entropy and small-lag autocorrelation remained comparable to warmup0 and warmup12 controls. However, direct sampler-register snapshots at the same startup window still exposed fixed sampled-position bias. This indicates that the near-cutoff restart behavior is more likely produced by the full sampler-side physical path, including sampling registers, local routing and aperture effects, than by simple two-RO phase locking.
```

中文写法：

```text
对 sampler-island warmup10 近阈值窗口进行 reset-aligned TDC 后，并未观察到 sample/data 两个 RO 之间的硬锁定特征：differential-bin 驻留、transition entropy 和小滞后自相关均与 warmup0/warmup12 对照接近。然而，同一窗口的直接 sampler-register snapshot 仍暴露出固定 sampled-position 偏置。因此，w10 贴近 restart cutoff 更可能来自完整采样端物理路径，包括采样寄存器、局部路由和采样孔径，而不是简单的两 RO 相位锁定。
```

## 复现入口

- TDC queue: `data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_w10_boundary_20260526.csv`
- TDC raw: `data/hardware/20260511_fpga1_board1/tdc_reset_aligned/tdc_reset_random1_sampler_local_ro0_clean32k_warmup10._preopen_20260525.bin`
- TDC summary: `data/experiments/tdc_reset_aligned_w10_boundary_20260526/tdc_sampler_local_w0_w10_w12_compare_20260526.summary.md`
- Snapshot raw: `data/hardware/20260511_fpga1_board1/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup10_cap1024_20260526.bin`
- Snapshot summary: `data/experiments/sampler_snapshot_island_w10_20260526/sampler_snapshot_random1_sampler_island_warmup10_cap1024_20260526.summary.md`
- Restart repeat summary: `data/experiments/restart_sampler_island_w10_repeat03_20260526/sampler_island_w10_repeats_summary_20260526.md`
