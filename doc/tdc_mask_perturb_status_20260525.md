# TDC Mask-Perturb 机制实验状态 2026-05-25

## 目标

验证“局部开关活动 / 邻近 RO 负载扰动”是否会改变 TDC phase diffusion，而不是继续重复 pairwise hard-locking 检查。

机制问题：

```text
同一对被 TDC 观测的 RO，在 only-pair、all-data-on、pair+sample-RO 等开关模式下，
TDC bin 分布、diff entropy、transition entropy、residence time、small-lag autocorrelation 是否改变？
```

如果 mode 改变会影响 TDC diffusion，但相关性仍接近 0，则说明机制更像局部供电/路由负载/采样孔径扰动，而不是 RO-RO hard locking。

## 新增实现

- RTL:
  - `rtl/tdc/RO_TDC_pair_mask_perturb_top.v`
  - `rtl/tdc/tdc_ro_mask_matrix.v`
- XDC 生成:
  - `scripts/generate_tdc_mask_perturb_xdc_20260525.py`
  - 输出目录：`data/experiments/xdc_tdc_mask_perturb/`
- bitstream 构建:
  - `scripts/build_tdc_mask_perturb_bitstreams_20260525.ps1`
- 硬件队列:
  - smoke: `data/experiments/fast_mode/hardware_queue_tdc_mask_perturb_smoke_20260525.csv`
  - P0: `data/experiments/fast_mode/hardware_queue_tdc_mask_perturb_p0_20260525.csv`
- 队列运行:
  - `scripts/run_tdc_mask_perturb_queue_20260525.ps1`

## Mode 编码

`PERTURB_MODE`：

- `0`: only measured pair enabled
- `1`: all 8 data ROs enabled
- `2`: measured pair plus `PERTURB_MASK`
- `3`: measured pair plus sample RO enabled

UART packet format 仍是原来的 8-byte `0xA5` TDC frame。`flags` 低位编码：

- bit0: `ro_enable`
- bit1-bit2: `PERTURB_MODE`
- bit3: sample RO enabled
- 高位仍保留 valid / bubble / full / empty 信息

## 已构建 bitstream

目录：`data/vivado_runs/fpga1_tdc_mask_perturb/`

已完成：

- `tdc_mask_random1_ro0_ro1_pair_only_smoke`
- `tdc_mask_random1_ro0_ro1_pair_only`
- `tdc_mask_random1_ro0_ro1_all_data_on`
- `tdc_mask_random1_ro0_ro1_pair_plus_sample`
- `tdc_mask_random3_ro0_ro6_pair_only`
- `tdc_mask_random3_ro0_ro6_all_data_on`
- `tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample`

每个 bitstream 大小均约 `4,045,688 bytes`，Vivado bitgen 通过。RO 组合环通过 XDC `ALLOW_COMBINATORIAL_LOOPS` 明确 acknowledge，与既有 RO 设计一致。

## Smoke 硬件结果

已采集：

```text
data/hardware/20260511_fpga1_board1/tdc_mask_perturb/tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525.bin
```

结果：

- bytes: `1,048,576`
- SHA256: `3025557A33BC73A80C2C8B61B45001CF14A5F235F45A5C5099948DB97EFF115D`
- decoded packets: `131071`
- `seq_gaps=1`，由于 pre-open 从 UART 流中间截入，作为 smoke 可接受
- `phase_pearson_r=-0.000707`
- `diff_std_ps=4082.091`
- startup diffusion: `H(diff)=6.64193`
- `transition H(diff)=13.1974`
- `same_diff_transition_ratio=0.01126`
- `longest_same_diff_bin_run=3`

解释：

新 top 在真实硬件上能稳定输出 TDC packet，没有出现明显卡死或强锁定。该结果使 P0 8MiB mode 对照具备运行资格。

## P0 采集矩阵

下一步硬件队列：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_tdc_mask_perturb_queue_20260525.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_mask_perturb_p0_20260525.csv `
  -RecordXadcAfter `
  -ContinueOnError
```

P0 包含：

| run | family | pair | mode | 目的 |
| --- | --- | --- | --- | --- |
| `tdc_mask_random1_ro0_ro1_pair_only` | random1 | RO0/RO1 | pair only | bad reference 的低扰动基线 |
| `tdc_mask_random1_ro0_ro1_all_data_on` | random1 | RO0/RO1 | all data on | 测邻近 data RO 开关活动 |
| `tdc_mask_random1_ro0_ro1_pair_plus_sample` | random1 | RO0/RO1 | pair + baseline sample | 测 sample RO 开关活动 |
| `tdc_mask_random3_ro0_ro6_pair_only` | random3 | RO0/RO6 | pair only | good reference 低扰动基线 |
| `tdc_mask_random3_ro0_ro6_all_data_on` | random3 | RO0/RO6 | all data on | good reference 的开关扰动 |
| `tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample` | random1 local sample | RO0/RO1 | pair + local sample | 对照 sampler-local placement |

## P0 正式结果

已完成 P0 6 个 8MiB 真实硬件采集，全部成功：

```text
data/experiments/tdc_mask_perturb_20260525/tdc_mask_perturb_queue_summary_20260525.csv
data/experiments/tdc_mask_perturb_20260525/tdc_mask_perturb_p0_20260525.summary.csv
data/experiments/tdc_mask_perturb_20260525/tdc_mask_perturb_p0_mode_compare_20260525.md
```

每个 run 解码得到 `1,048,575` 个 TDC packets。每个 run 的 `seq_gaps=1`，这是 pre-open capture 从 UART stream 中间截入造成的边界效应，可接受。每次采集后 XADC 温度约 `46.4-46.8 C`，VCCINT `1.000 V`。

核心 mode 对比：

| run | H(diff) | transition H(diff) | same ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: |
| random1 RO0/RO1 pair_only | 6.686386 | 13.362153 | 0.010857 | 3 | 0.000874 |
| random1 RO0/RO1 all_data_on | 6.747066 | 13.482718 | 0.010303 | 4 | -0.000932 |
| random1 RO0/RO1 pair_plus_sample | 6.646222 | 13.282559 | 0.010963 | 4 | -0.000067 |
| random3 RO0/RO6 pair_only | 6.697029 | 13.383203 | 0.010748 | 4 | 0.000729 |
| random3 RO0/RO6 all_data_on | 5.982632 | 11.962490 | 0.016026 | 4 | -0.001284 |
| random1 local-sample RO0/RO1 pair_plus_sample | 6.668195 | 13.325698 | 0.011060 | 4 | -0.000176 |

最重要的新发现：

- random1 RO0/RO1 在 `pair_only`、`all_data_on`、`pair_plus_sample` 之间只有温和变化，仍不支持 hard locking。
- random3 RO0/RO6 在 `all_data_on` 下出现强变化：`H(diff)` 相比 pair-only 下降 `0.714397` bit，`transition H(diff)` 下降 `1.420713` bit。
- 但是 random3 all-data-on 的 `autocorr=-0.001284`，最长同 differential-bin run 仍只有 `4`，没有表现出 pairwise hard locking。

因此 P0 支持一个更细的机制判断：

```text
邻近 RO 开关活动可以重塑 TDC phase/bin 分布，但这种扰动不等价于 RO-RO hard locking。
```

这给论文增加了一层正证据：TDC 不只是排除 hard locking，还能说明局部开关活动/负载扰动可能参与 sampler-side entropy-source boundary。

## 论文用途

若 all-data-on 或 sample-on 显著改变 TDC diffusion，但仍没有强相关或长 residence，则可写成：

```text
Local switching activity modifies delay/phase diffusion without producing pairwise hard locking.
```

若 mode 切换几乎不改变 TDC，而 TRNG/restart 仍强烈受 sampler-side placement 影响，则可写成：

```text
TDC further excludes RO phase-layer explanations; the dominant effect is likely in sampling registers, local routing, or sampling aperture.
```

两种结果都对论文有价值，关键是不要把 TDC 强行写成“证明锁定”。
