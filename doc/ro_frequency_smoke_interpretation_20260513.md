# random1 / random3 fixed frequency smoke 解释

日期：2026-05-13

范围：本文只解释已经生成的 `random1/random3` fixed RO frequency smoke 结果。本文未执行 COM3、JTAG、`hw_server`、Vivado 或任何硬件采集操作。结论均按 smoke 证据处理，不能写成最终机制定论。

## 1. 输入与数据质量

使用的数据：

- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_smoke/random1_random3_fixed_smoke_summary.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_smoke/random1_random3_fixed_smoke_pairwise_all_on.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_smoke/random1_random3_fixed_smoke_pulling.csv`
- 同目录 `random1_random3_fixed_smoke_measurements.csv` 用于核对 valid frame 数。
- `doc/mechanism_validation_plan_random1_random3_20260513.md`
- `doc/paper_results_update_20260513.md`
- `doc/experiment_execution_status_20260513.md` 中记录的 fixed smoke 解析摘要。

解析质量：

| capture | raw size | valid frames | framed bytes | dropped / unframed bytes |
| --- | ---: | ---: | ---: | ---: |
| `random1_ro_freq_fixed_smoke01_512k.bin` | 512 KiB | 37448 | 524272 | 16 |
| `random3_ro_freq_fixed_smoke01_512k.bin` | 512 KiB | 37442 | 524188 | 100 |
| 合计 | 1024 KiB | 74890 | 1048460 | 116 |

每个 UART frame 为 14 byte。`dropped / unframed bytes` 是 `scripts/analyze_ro_frequency_matrix.py` 在 magic/checksum 同步过程中跳过或尾部未成帧的字节数，不应直接解释成完整 frame 丢失数。

每个 family、mode、target 的有效样本数约为 2078 到 2082。测量窗口为 `window_cycles=100`、`window_ns=500.0 ns`，所以单帧 count 到频率的量化步长为 2 MHz；这里的 `freq_std_mhz` 同时包含短窗口量化、抖动和 smoke 捕获噪声。由于每个 family 只有一个 512 KiB smoke capture，本结果只能说明 fixed probe 和分析链路可用，并提供机制线索，不能给出置信区间、长期稳定性或统计显著性。

## 2. all-on 频率分布对比

all-on 下 8 个 data RO 的均值如下：

| family | data0 | data1 | data2 | data3 | data4 | data5 | data6 | data7 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| random1 MHz | 413.999 | 413.058 | 454.859 | 433.671 | 456.778 | 457.266 | 403.319 | 446.412 |
| random3 MHz | 460.875 | 448.967 | 412.495 | 439.514 | 396.312 | 437.222 | 457.769 | 440.215 |

分布摘要：

| family | data RO min | data RO max | span | across-RO std | mean per-target std | sample all-on |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| random1 | 403.319 MHz | 457.266 MHz | 53.947 MHz | 20.684 MHz | 1.071 MHz | 89.922 MHz |
| random3 | 396.312 MHz | 460.875 MHz | 64.562 MHz | 20.665 MHz | 0.904 MHz | 91.717 MHz |

解释：

- random1 并不是整体频率更窄的一组。它的 data RO span 为 53.947 MHz，random3 为 64.562 MHz；across-RO std 几乎相同。
- random1 有两个明显的近频簇：`data4/data5`，以及 `data0/data1`；还存在 `data2/data4/data5` 的高频簇。
- random3 也有近频结构：`data3/data7`，`data3/data5/data7`，以及 `data0/data6`。因此“存在近频 pair”不是 random1 独有现象。
- random3 的 per-target short-window std 平均值略低于 random1，但差异仍处在 smoke 线索层面，不能直接解释 TRNG 质量差异。

## 3. 最近频率 pair、beat period 与 pulling

all-on data-data 最近 pair：

| family | pair | delta f | beat period |
| --- | --- | ---: | ---: |
| random1 | data4 / data5 | 0.488 MHz | 2048.23 ns |
| random1 | data0 / data1 | 0.941 MHz | 1062.82 ns |
| random1 | data2 / data4 | 1.918 MHz | 521.29 ns |
| random1 | data2 / data5 | 2.407 MHz | 415.54 ns |
| random3 | data3 / data7 | 0.701 MHz | 1426.14 ns |
| random3 | data3 / data5 | 2.293 MHz | 436.17 ns |
| random3 | data5 / data7 | 2.994 MHz | 334.02 ns |
| random3 | data0 / data6 | 3.105 MHz | 322.01 ns |

data-data pairwise 摘要：

| family | min delta f | max delta f | mean delta f |
| --- | ---: | ---: | ---: |
| random1 | 0.488 MHz | 53.947 MHz | 26.127 MHz |
| random3 | 0.701 MHz | 64.562 MHz | 25.509 MHz |

fundamental data-sample 差频最近项：

| family | nearest fundamental data-sample pair | delta f | beat period |
| --- | --- | ---: | ---: |
| random1 | data6 / sample | 313.396 MHz | 3.191 ns |
| random3 | data4 / sample | 304.595 MHz | 3.283 ns |

按 fundamental frequency 看，data RO 与 sample RO 没有低 beat-frequency 关系；它们都相差约 300 MHz 以上。另一个需要后续正式分析的点是 sample RO 约 90 MHz，data RO 约 400 到 460 MHz，可能存在 `f_data` 与 `5 * f_sample` 的 alias / harmonic 关系。用本次 summary 粗算 all-on 下 `abs(f_data - 5*f_sample)`，random1 最近为 data7 的 3.199 MHz，random3 最近为 data6 的 0.818 MHz。也就是说，若只看 5x sample harmonic 距离，较接近的反而是高质量 random3，这不支持简单的“data-sample harmonic 越近越差”的单因子解释。

all-on 相对 single-on 的 pulling / shift：

| family | data RO shift 范围 | data RO mean shift | data RO mean abs ppm | data RO worst | sample shift |
| --- | ---: | ---: | ---: | --- | ---: |
| random1 | -0.298 到 -0.042 MHz | -0.166 MHz | 377.4 ppm | data4: -653.0 ppm | +0.304 MHz / +3388.4 ppm |
| random3 | -0.280 到 -0.110 MHz | -0.195 MHz | 446.3 ppm | data0: -606.5 ppm | -0.230 MHz / -2497.9 ppm |

解释：

- 两组 data RO 在 all-on 下相对 single-on 都整体变慢，说明 enable state 对频率有可观影响；这与存在负载、供电、routing 或 RO 间相互作用的假设相容。
- 但 data RO pulling 的幅度并不是 random1 明显大于 random3。random3 的 data RO mean abs ppm 还略大。因此本 smoke 不支持“random1 因 data RO pulling 更强而失败”的简单解释。
- sample RO 的 shift 在 random1 中为正，在 random3 中为负，且 ppm 绝对值较大。但 sample RO 只有一个 smoke capture，不能据此判断 sample relation 的因果方向。

## 4. 对 coupling / beat 假设的支持与限制

能支持的现象：

- fixed probe 与解析链路工作正常：两个 512 KiB capture 解析出 74890 个有效 frame，未成帧/丢弃字节只有 116。
- random1 存在非常近的 data-data pair，尤其 `data4/data5` 的 0.488 MHz，对应约 2.05 us beat period；这为“近频 pair 可能影响 sampled XOR 输出”提供了候选对象。
- all-on 与 single-on 之间存在可测 shift，且 data RO shift 方向一致为负；这说明 enable 状态确实会改变 RO 频率，和 coupling / pulling 的物理图景相容。
- random1 的高频簇 `data2/data4/data5` 与低频近 pair `data0/data1` 可作为后续 TDC pair 或 longer frequency capture 的优先目标。

不能支持或尚不能支持的现象：

- 不能说 random1 失败已经由频率聚集证明。random3 也有 0.701 MHz 的近频 pair，且 data-data mean delta f 与 random1 接近。
- 不能说 random1 的 RO 频率分布更窄导致 entropy 失败。random1 的 span 反而小于 random3，但 across-RO std 基本相同。
- 不能说 data-sample fundamental beat 解释了 random1 的强 bias。fundamental data-sample 差频都在 300 MHz 量级。
- 不能说 5x sample harmonic 解释了 random1 的强 bias。按 smoke summary 粗算，random3 的 `data6` 距 `5*sample` 更近，但 random3 的 TRNG 指标更好。
- 不能说 pulling 是 random1 独有异常。data RO pulling 在 random1 和 random3 中量级相近，random3 的 mean abs ppm 略大。
- 不能证明 locking、phase correlation 或相位扩散不足。本实验是 frequency counter smoke，不是 colocated TDC 或 phase measurement；没有 phase histogram、diff std、lag correlation 或 pairwise phase Pearson。

因此，当前最稳妥表述是：本 smoke 发现了 random1 中可疑的近频 pair 和 enable-dependent frequency shift，但这些现象也部分出现在 random3 中。它们支持继续验证 coupling / beat 假设，却不足以把 random1 的 `p1 ~= 0.337` 归因于单一的近频、pulling 或 sample harmonic 机制。

## 5. 下一步正式实验建议

建议把后续实验写成 formal mechanism measurement，而不是继续扩大 smoke 结论。

1. 5MiB frequency capture

   使用 fixed bitstream：`data/vivado_runs/fpga1_ro_freq_probe_fixed/random1_seed1_x36y35/RO_FREQ_trng_probe_top.bit` 和 `data/vivado_runs/fpga1_ro_freq_probe_fixed/random3_seed3_x36y35/RO_FREQ_trng_probe_top.bit`。每个 family 至少采 5MiB。按 14-byte frame 估算，单个 5MiB capture 约 374k 个 frame，每个 target/mode 约 20k 个样本，能把 smoke 中 2k 样本级别的不确定性压低一个量级。

2. 多次 repeat

   random1 和 random3 至少各做 3 次，最好 5 次；采集顺序使用交错方式，例如 `random1 -> random3 -> random1 -> random3`，避免时间漂移只落在某一个 family 上。输出每个 target 的 mean、std、run-to-run std、置信区间，以及 pairwise delta f / beat period 的 repeat 稳定性。

3. 温度不测时的替代控制

   如果没有温度传感或温度记录，不要声称温度稳定。可替代做法是记录绝对时间、采集顺序、bitstream SHA256、capture SHA256、板卡状态说明，并用交错采集降低单调漂移偏置。分析上可把 sample RO frequency、全体 data RO mean frequency、全体 RO common-mode shift 当作 on-chip drift proxy；若所有 RO 同向漂移而 pairwise delta f 稳定，则机制指标更可信。也可以在同一轮中重复采一个 reference capture，用前后差估计漂移上界。

4. 扩展机制指标

   正式输出至少包括：

   - per-RO all-on / single-on mean frequency、per-target std、run-to-run std。
   - data-data min delta f、top-k close pairs、delta-f heatmap。
   - `abs(f_data - n*f_sample)` 的 alias / harmonic ranking，建议覆盖 `n=4,5,6`，不要只看 fundamental data-sample delta。
   - all-on vs single-on shift：max abs ppm、mean abs ppm、sample shift、data RO shift direction consistency。
   - 若后续做 TDC pair，再加入 `diff_std_ps`、phase Pearson、lag correlation、phase-drift 指标。

5. 与 TRNG 指标做相关

   对 random1/random3，先做 anchor-pair 对照：把机制指标与已有 TRNG 指标并排展示，例如 `abs(p1-0.5)`、bit min-entropy、byte min-entropy、adjacent equal ratio、runs 指标。需要注意，只有 random1 和 random3 两点时不能做有意义的相关系数，只能做机制解释对照。若要形成论文中的 correlation plot，应扩展到更多 placement，至少覆盖 `compact`、`sparse`、`row`、`far`、`checker`、`same_column` 等已有 TRNG 指标的样本。

推荐的论文边界表述：

> The 512 KiB fixed-frequency smoke run validates the frequency probe and reveals candidate close-frequency pairs and enable-dependent shifts. However, similar close-pair and pulling signatures also appear in the high-quality random3 layout, so this smoke evidence should be treated as hypothesis-generating rather than causal proof. Formal 5MiB repeated frequency captures, harmonic data-sample analysis, and correlation with TRNG quality metrics are required before attributing the random1 bias to coupling, beat, or pulling mechanisms.

