# Sampler Snapshot Correlation/XOR Interpretation 2026-05-26

## 目标

对 `sampler_island_local w5/w10/w11` 的 64-bit sampler snapshot 做离线机制分析：

- pairwise Pearson correlation；
- pairwise mutual information；
- line/data_ro/stage XOR 消融；
- 判断 w10 near-cutoff 是否来自 marginal bit bias，还是 sampled-bit correlation / XOR-combination structure。

## 关键结论

结果支持“相关结构改变”而不是“单点 bit bias 变坏”：

1. w5/w10/w11 的 sampled-bit marginal bias 很接近，平均 p1 都约为 `0.523`；
2. w10 的 pairwise correlation / MI 更高，尤其集中在同一个 `data_ro` 跨不同 `sample line` 的 bit pair；
3. 同 line 内不同 data RO 的相关性很低，说明主要不是同一 sample-stage 内所有 RO 一起锁住；
4. data_ro 方向的跨 line XOR 在 w10 更容易偏离 0.5，说明 startup window 更可能改变同一个 data RO 被多个 sampler stages 捕获时的相位/相关结构。

## Pairwise Aggregate

| label | category | mean abs r | median abs r | p95 abs r | mean MI | median MI | p95 MI |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| w5 | same_line | 0.012783 | 0.009534 | 0.033242 | 0.000228 | 0.000066 | 0.000797 |
| w10 | same_line | 0.015514 | 0.011071 | 0.047872 | 0.000371 | 0.000088 | 0.001654 |
| w11 | same_line | 0.013815 | 0.010360 | 0.043446 | 0.000249 | 0.000077 | 0.001362 |
| w5 | same_data_ro | 0.493098 | 0.505072 | 0.900247 | 0.273632 | 0.192998 | 0.714758 |
| w10 | same_data_ro | 0.537687 | 0.569382 | 0.905533 | 0.304056 | 0.247391 | 0.742157 |
| w11 | same_data_ro | 0.496967 | 0.506978 | 0.900340 | 0.275121 | 0.194364 | 0.715494 |
| w5 | diff_line_diff_ro | 0.012891 | 0.009517 | 0.036952 | 0.000233 | 0.000065 | 0.000985 |
| w10 | diff_line_diff_ro | 0.015008 | 0.009834 | 0.050376 | 0.000350 | 0.000070 | 0.001832 |
| w11 | diff_line_diff_ro | 0.014964 | 0.010904 | 0.047032 | 0.000305 | 0.000086 | 0.001596 |

最强信号是 `same_data_ro` 类别：w10 的 mean abs r 从 w5/w11 的约 `0.49` 提高到 `0.538`，mean MI 从约 `0.274/0.275` 提高到 `0.304`。这说明 w10 的 near-cutoff 行为更像“同一 data RO 在多个 sampler stage 上的重复采样相关增强”。

## Top Pairwise Examples

w10 的 top pairwise MI 大多是同一 `data_ro` 跨多个 sample line：

| bit_i | bit_j | line_i | line_j | data_ro | r | MI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 60 | 2 | 7 | 4 | 0.974825 | 0.909029 |
| 29 | 53 | 3 | 6 | 5 | -0.972684 | 0.896473 |
| 5 | 37 | 0 | 4 | 5 | 0.965026 | 0.876292 |
| 8 | 16 | 1 | 2 | 0 | 0.953238 | 0.841401 |
| 14 | 38 | 1 | 4 | 6 | 0.946699 | 0.816767 |

这些 top pair 不是同一 line 内的不同 RO，而是同一 data RO 在不同 line 上的状态关系。这与 sample RO 多个 stage 对同一 data RO 进行多相采样的结构一致。

## XOR Ablation

注意：由于 `rand_bit` 在 RTL 中是寄存器，snapshot 同一帧记录的 `rand_bit` 不一定严格等于同一帧 `sampled_data` 的即时 XOR。因此 XOR 消融应解释为 sampled-state 组合结构诊断，而不是逐帧等式证明。

仍然可以看到结构差异：

| warmup | selected data_ro group_xor p1 | line group_xor behavior | interpretation |
| ---: | --- | --- | --- |
| 5 | ro5=0.211914, ro2=0.341797, ro7=0.341797, ro6=0.541016 | line XOR mostly near 0.5 | pass window, line-level mixture cancels in final output |
| 10 | ro0=0.297852, ro2=0.236328, ro7=0.317383, ro6=0.429688 | line XOR all near 0.5 | data_ro-direction cross-line structure is more distorted |
| 11 | ro5=0.174805, ro2=0.323242, ro7=0.342773, ro6=0.522461 | line XOR near 0.5 with mixed signs | pass window, final rand remains near ideal |

w10 的 line-level XOR 没有明显爆掉，但 data_ro-direction XOR 更偏。这进一步支持：问题不在“某个 sample line 同时采坏所有 RO”，而在“同一 data RO 被不同 sample stages 捕获后的跨 line 相关/相位结构”。

## 论文表述

可以写：

```text
The sampler snapshot analysis shows that the w10 boundary is not explained by a larger marginal bias of individual sampled bits. Instead, pairwise correlation and mutual information increase mainly among bits belonging to the same data RO but captured at different sample stages. This points to a startup-window-dependent multi-phase sampling correlation: the sample RO and local sampler path determine how repeated observations of the same data RO combine through the XOR network. Therefore, the boundary behavior is better described as a sampler-side correlation/XOR-combination effect rather than a single-bit bias or a pairwise RO hard lock.
```

中文写法：

```text
sampler snapshot 分析显示，w10 边界不能由单个 sampled bit 的 marginal bias 增大解释。pairwise correlation 和 mutual information 的增强主要出现在同一 data RO、不同 sample stage/line 的 bit pair 上，而同一 line 内不同 RO 的相关性仍很低。这说明 restart startup window 改变的是多相采样下同一 data RO 的重复观测相关结构，并通过 XOR 组合影响最终输出。因此，w10 near-cutoff 更适合解释为 sampler-side correlation / XOR-combination effect，而不是单 bit 偏置或 pairwise RO hard lock。
```

## 复现入口

```powershell
python scripts\analyze_sampler_snapshot_correlation_xor_20260526.py `
  --run w5=data\experiments\sampler_snapshot_island_w5_w11_20260526\sampler_snapshot_random1_sampler_island_warmup5_cap1024_20260526.frames.csv `
  --run w10=data\experiments\sampler_snapshot_island_w10_20260526\sampler_snapshot_random1_sampler_island_warmup10_cap1024_20260526.frames.csv `
  --run w11=data\experiments\sampler_snapshot_island_w5_w11_20260526\sampler_snapshot_random1_sampler_island_warmup11_cap1024_20260526.frames.csv `
  --out-dir data\experiments\sampler_snapshot_island_w5_w11_20260526\correlation_xor
```
