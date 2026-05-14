# random1 / random3 fixed RO frequency run01 机制证据整理

日期：2026-05-13

范围：本文只整理已经完成的 `random1/random3` fixed frequency 2MiB run01 采集与离线分析结果。本文未执行 COM3、JTAG、`hw_server`、Vivado 或任何新的硬件采集操作。所有结论均应写作 **run01 机制证据**，不能写成因果证明。

## 1. 输入与采集完整性

本次整理使用的分析输出：

- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_summary.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_pairwise_all_on.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_pulling.csv`
- `doc/ro_frequency_smoke_interpretation_20260513.md`
- `doc/paper_results_update_20260513.md`

采集完整性如下：

| family | capture | raw size | SHA256 | valid frames in summary |
| --- | --- | ---: | --- | ---: |
| random1 | `data/hardware/20260511_fpga1_board1/ro_freq/random1_ro_freq_fixed_run01_2mib.bin` | 2 MiB | `2E06E59CF3A38BB3C4B4BD5CFFF2409A9C8A19FD4BF3B25B048EBAF00273E3BB` | 149750 |
| random3 | `data/hardware/20260511_fpga1_board1/ro_freq/random3_ro_freq_fixed_run01_2mib.bin` | 2 MiB | `AE6C877269AEA5679791B4E9F530CBCF1430F7CE9BE9438398C75426D6F0F2CA` | 149796 |
| combined | - | 4 MiB | - | 299546 |

合并解析记录为 `valid_frames=299546`、`dropped_or_unframed_bytes=660`。这里的 dropped/unframed 是解析器在 magic/checksum 同步和尾部处理时跳过或未成帧的字节数，不应直接解释为完整 frame 丢失数。

测量窗口为 `window_cycles=100`、`window_ns=500.0 ns`，因此频率量化步长为 2 MHz。均值来自大量短窗口 frame 的平均，`freq_std_mhz` 同时包含短窗口量化、抖动、采集链路噪声和真实频率波动。

## 2. all-on 频率表

`all_on` 模式下，8 个 data RO 与 1 个 sample RO 的频率均值如下：

| target | random1 samples | random1 mean MHz | random1 std MHz | random3 samples | random3 mean MHz | random3 std MHz |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| data0 | 8320 | 413.931 | 0.672 | 8322 | 460.806 | 0.988 |
| data1 | 8320 | 412.951 | 0.999 | 8322 | 448.923 | 0.999 |
| data2 | 8320 | 454.782 | 1.246 | 8322 | 412.485 | 0.895 |
| data3 | 8320 | 433.606 | 0.941 | 8322 | 439.533 | 1.010 |
| data4 | 8323 | 456.762 | 0.984 | 8322 | 396.306 | 0.805 |
| data5 | 8318 | 457.228 | 0.989 | 8322 | 437.206 | 0.979 |
| data6 | 8316 | 403.203 | 1.635 | 8322 | 457.728 | 0.763 |
| data7 | 8319 | 446.321 | 1.055 | 8322 | 440.206 | 0.854 |
| sample | 8320 | 89.996 | 1.666 | 8322 | 91.735 | 1.328 |

直接观察：

- random1 的 data RO 覆盖约 403.203 到 457.228 MHz；random3 的 data RO 覆盖约 396.306 到 460.806 MHz。
- random1 存在非常近的 `data4/data5` 与 `data0/data1`；random3 也存在近频 pair，例如 `data3/data7`。
- sample RO 在两组中都约为 90 MHz 量级，和 data RO 的 fundamental 频率相差约 300 MHz 以上；它不构成简单的 fundamental data-sample 近 beat 关系。

## 3. 最近 pair / beat 对比

all-on data-data 最近 pair 如下，按 `abs_delta_f_mhz` 从小到大列出：

| family | pair | freq A MHz | freq B MHz | delta f MHz | beat period ns |
| --- | --- | ---: | ---: | ---: | ---: |
| random1 | data4 / data5 | 456.762 | 457.228 | 0.466 | 2145.027 |
| random1 | data0 / data1 | 413.931 | 412.951 | 0.979 | 1021.360 |
| random1 | data2 / data4 | 454.782 | 456.762 | 1.980 | 505.170 |
| random1 | data2 / data5 | 454.782 | 457.228 | 2.446 | 408.876 |
| random3 | data3 / data7 | 439.533 | 440.206 | 0.673 | 1485.011 |
| random3 | data3 / data5 | 439.533 | 437.206 | 2.327 | 429.811 |
| random3 | data5 / data7 | 437.206 | 440.206 | 3.000 | 333.333 |
| random3 | data0 / data6 | 460.806 | 457.728 | 3.078 | 324.926 |

机制含义要谨慎写：

- random1 的最近 pair 更近，尤其 `data4/data5` 的 `delta f=0.466 MHz`，对应约 `2.145 us` beat period；这是一个值得后续 TDC pair 或更长频率 repeat 验证的候选。
- random3 也有 `delta f=0.673 MHz` 的近频 pair，且 TRNG 结果接近理想。因此，仅凭“存在近频 pair”不能解释 random1 的强偏置。
- 本表反映的是短窗口 frequency counter 的 run01 统计，不含相位锁定、phase diffusion、lag correlation 或 sampled XOR 输出同步关系的直接证据。

fundamental data-sample 最近项如下：

| family | nearest data-sample pair | delta f MHz | beat period ns |
| --- | --- | ---: | ---: |
| random1 | data6 / sample | 313.207 | 3.193 |
| random3 | data4 / sample | 304.571 | 3.283 |

这说明按 fundamental frequency 看，data RO 与 sample RO 不是低 beat 关系。若要讨论 sample harmonic 或 alias，需要另做 `abs(f_data - n*f_sample)` 的系统排序，不能从本 fundamental 表直接推出因果结论。

## 4. all-on vs single-on pulling / shift

`all_on_freq_mhz - single_on_freq_mhz` 的 per-target shift 如下：

| family | target | all-on MHz | single-on MHz | shift MHz | shift ppm vs single |
| --- | --- | ---: | ---: | ---: | ---: |
| random1 | data0 | 413.931 | 413.988 | -0.057 | -138.8 |
| random1 | data1 | 412.951 | 413.102 | -0.150 | -364.1 |
| random1 | data2 | 454.782 | 454.985 | -0.203 | -445.9 |
| random1 | data3 | 433.606 | 433.831 | -0.225 | -518.1 |
| random1 | data4 | 456.762 | 457.077 | -0.316 | -690.4 |
| random1 | data5 | 457.228 | 457.436 | -0.208 | -455.8 |
| random1 | data6 | 403.203 | 403.375 | -0.172 | -426.0 |
| random1 | data7 | 446.321 | 446.470 | -0.149 | -333.6 |
| random1 | sample | 89.996 | 89.685 | +0.311 | **+3466.9** |
| random3 | data0 | 460.806 | 461.116 | -0.310 | -672.8 |
| random3 | data1 | 448.923 | 449.132 | -0.209 | -465.5 |
| random3 | data2 | 412.485 | 412.728 | -0.243 | -588.1 |
| random3 | data3 | 439.533 | 439.765 | -0.232 | -528.5 |
| random3 | data4 | 396.306 | 396.485 | -0.179 | -452.2 |
| random3 | data5 | 437.206 | 437.319 | -0.113 | -258.3 |
| random3 | data6 | 457.728 | 457.982 | -0.253 | -553.1 |
| random3 | data7 | 440.206 | 440.341 | -0.135 | -306.2 |
| random3 | sample | 91.735 | 91.811 | -0.076 | **-824.6** |

汇总：

| family | data RO shift range MHz | data RO mean shift MHz | data RO mean abs ppm | sample shift |
| --- | ---: | ---: | ---: | ---: |
| random1 | -0.316 to -0.057 | -0.185 | 421.6 ppm | +0.311 MHz / **+3466.9 ppm** |
| random3 | -0.310 to -0.113 | -0.209 | 478.1 ppm | -0.076 MHz / **-824.6 ppm** |

这里最突出的 run01 现象是 sample RO 的方向和幅度不同：random1 sample 在 all-on 下相对 single-on 上移 `+3466.9 ppm`，random3 sample 下移 `-824.6 ppm`。这支持“sample relation / enable-dependent interaction 需要重点验证”的机制线索。

但 data RO pulling 并不是 random1 独有异常：两组 data RO 在 all-on 下相对 single-on 均整体变慢，random3 的 data RO mean abs ppm 还略高。因此不能写成“random1 因 data RO pulling 更强而失败”。

## 5. 与 TRNG 结果的关联

已有 10MiB formal TRNG 结果给出强对照：

| run | p1 | abs bias | bit min-entropy | adjacent equal ratio | byte min-entropy | 解释 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| random1_run01 | 0.337315512 | 0.162684488 | 0.593605945 | 0.556739754 | 4.80160868 | 强偏置，当前最强负例 |
| random3_run01 | 0.499968565 | 0.000031435 | 0.999909299 | 0.500072473 | 7.9845501 | 接近理想，当前高质量样本 |

本次 frequency run01 与 TRNG 结果可以并排形成机制线索：

- random1 的 TRNG 输出存在稳定强偏置，同时 fixed frequency run01 中出现更近的 data-data pair，尤其 `data4/data5` 的 `0.466 MHz`。
- random1 的 sample RO 在 all-on 下出现明显正向 shift：`+3466.9 ppm`；random3 sample 为负向 shift：`-824.6 ppm`。
- random3 虽然 TRNG 结果接近理想，但同样存在近频 pair 和 data RO pulling，因此这些机制指标不是充分条件。

最稳妥的论文表述是：**本 run01 fixed frequency 结果为解释 random1/random3 的 raw entropy 差异提供了候选机制证据，尤其指向近频 pair 与 sample enable-dependent shift；但它还不是因果证明。** 因果链还需要 repeat 稳定性、sample placement 变体、对应 TDC pair 和跨 placement 相关性图来闭合。

## 6. 下一步

建议按以下顺序把 run01 线索推进为更强证据：

1. **repeat**：对 random1/random3 fixed frequency 至少做多次 repeat，交错采集顺序，报告 per-target mean/std、run-to-run std、top close pairs 稳定性和 sample shift 稳定性。
2. **采 sample placement 变体**：保持 data RO placement 尽量不变，改变 sample RO 位置或 sample relation，观察 `p1`、sample frequency、sample pulling 和近 beat 排名是否同步变化。
3. **TDC pair 对应验证**：优先测 random1 `data4/data5`、`data0/data1`，以及 random3 `data3/data7` 等 anchor pair，输出 phase histogram、`diff_std_ps`、phase Pearson、lag correlation 和 drift 指标。
4. **相关性图**：扩展到更多 placement，把 `abs(p1-0.5)`、bit min-entropy、adjacent equal ratio 与 min delta f、top-k close pair、sample shift ppm、harmonic distance、TDC phase/correlation 指标并排作图。只有 random1/random3 两点时不要计算有意义的相关系数。

## 7. 当前可引用的一句话

The 2MiB fixed-frequency run01 captures for random1 and random3 are complete and parseable, with 299546 valid frames and 660 dropped/unframed bytes in the combined analysis. The run reveals candidate close-frequency pairs and a notably different sample-RO pulling signature, especially random1 sample `+3466.9 ppm` versus random3 sample `-824.6 ppm`. These observations are mechanism evidence for follow-up, not causal proof of the random1 TRNG bias.
