# Sampler-Island w5/w10/w11 Snapshot Compare 2026-05-26

## 目的

补充 `sampler_island_local warmup5` 和 `warmup11` 的 direct sampler-register snapshot，作为 `warmup10` near-cutoff 窗口两侧的 pass 点对照。

## 硬件采集

| warmup | raw capture | bytes | header | SHA256 | XADC after |
| ---: | --- | ---: | --- | --- | --- |
| 5 | `data/hardware/20260511_fpga1_board1/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup5_cap1024_20260526.bin` | 16400 | `534E41500117000500000408080955AA` | `E78E35BC754AD1D1931332A18457816AA53D908AF623A915324CCE0EC3FD8804` | 46.6 C, VCCINT 1.000 V |
| 10 | `data/hardware/20260511_fpga1_board1/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup10_cap1024_20260526.bin` | 16400 | `534E4150011C000A00000408080955AA` | `7DAAE128F6516F573A9D65F037C200E7C3AA890825CF9351635A32DED151152A` | 46.1 C, VCCINT 1.000 V |
| 11 | `data/hardware/20260511_fpga1_board1/sampler_snapshot/sampler_snapshot_random1_sampler_island_warmup11_cap1024_20260526.bin` | 16400 | `534E4150011D000B00000408080955AA` | `FD313B99828EC88DE7279612C00D007BB3CF194D13FEEE57B06B0AEA6D6A8BB5` | 46.8 C, VCCINT 1.000 V |

## 三点对照

| warmup | restart reference | rand p1 | rand min-H | stage_xor H | sampled bit mean p1 | worst bit abs bias | bits p1 > 0.55 | stage_xor mean p1 | 解释 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 5 | pass | 0.509766 | 0.972094 | 7.773146 | 0.523621 | 0.067383 | 9 | 0.498047 | pass 侧对照，最终 rand 接近 0.5 |
| 10 | boundary | 0.466797 | 0.907243 | 7.806656 | 0.523178 | 0.070313 | 12 | 0.510132 | near-cutoff 边界，最终 rand 明显偏低 |
| 11 | pass | 0.500977 | 0.997185 | 7.783961 | 0.524139 | 0.067383 | 13 | 0.499756 | pass 侧对照，最终 rand 几乎理想 |

## 机制解释

这组三点对照说明，`w10` 贴近 restart cutoff 不是因为某一个 sampled register bit 的偏置突然变大：

- w5/w10/w11 的 worst sampled-bit abs bias 很接近，约 `0.067` 到 `0.070`；
- 三者 64 个 sampled bits 的平均 p1 都偏高，约 `0.523` 到 `0.524`；
- 但最终 `rand_bit = ^sampled_data` 的 p1 只有 w10 明显偏低，为 `0.466797`，而 w5/w11 分别为 `0.509766` 和 `0.500977`。

因此，更准确的解释是：warmup window 改变了 sampled bits 之间的相关结构和组合关系。注意，snapshot 同一帧中的 `rand_bit` 是寄存器输出，不一定严格等于同一帧 `sampled_data` 的即时 XOR；所以这里不把 XOR 消融解释成逐帧等式证明，而把它作为 sampled-state 组合结构诊断。后续 correlation/XOR 分析显示，w10 的主要差异集中在同一 `data_ro` 跨不同 sample line 的相关增强。

这与 w10-aligned TDC 的负结果是互补的：两路 TDC 没有看到 sample/data RO 的简单 hard-lock signature，但 direct sampler-register snapshot 显示完整 sampler path 中的 fixed sampled-position bias 和 XOR-combination effect。论文中应把机制写成 sampler-side physical path/window effect，而不是单个 pairwise RO lock。

进一步分析见：

```text
data/experiments/sampler_snapshot_island_w5_w11_20260526/correlation_xor/sampler_snapshot_correlation_xor_interpretation_20260526.md
```

## 复现入口

Build:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_sampler_snapshot_bitstreams_20260524.ps1 `
  -WarmupsCsv 5,11 `
  -VariantsCsv sampler_island `
  -CaptureSnapshots 1024 `
  -TopName RO_TRNG_sampler_snapshot_top `
  -OutPrefix sampler_snapshot
```

Capture:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_restart_preopen_queue_20260525.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_sampler_snapshot_island_w5_w11_20260526.csv `
  -OutRoot data\experiments\sampler_snapshot_island_w5_w11_20260526 `
  -RecordXadcAfter `
  -ContinueOnError
```

Analyze:

```powershell
python scripts\analyze_sampler_snapshot.py --input data\hardware\20260511_fpga1_board1\sampler_snapshot\sampler_snapshot_random1_sampler_island_warmup5_cap1024_20260526.bin --out-dir data\experiments\sampler_snapshot_island_w5_w11_20260526 --label sampler_snapshot_random1_sampler_island_warmup5_cap1024_20260526
python scripts\analyze_sampler_snapshot.py --input data\hardware\20260511_fpga1_board1\sampler_snapshot\sampler_snapshot_random1_sampler_island_warmup11_cap1024_20260526.bin --out-dir data\experiments\sampler_snapshot_island_w5_w11_20260526 --label sampler_snapshot_random1_sampler_island_warmup11_cap1024_20260526
```
