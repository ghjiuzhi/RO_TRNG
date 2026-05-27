# TDC Code-Density Calibration 设计规格 2026-05-25

## 当前 TDC 结论边界

当前 clean reset-aligned TDC 已经可以支持：

```text
没有观察到强 pairwise RO hard locking。
sampler-local warmup12 的 raw-bin diffusion 指标略好。
```

但当前不能支持：

```text
某个 bin 差值等于多少 ps。
某个 placement 的绝对 jitter 是多少 ps。
```

原因是还没有独立 code-density calibration。现有 pair/run 自身的 code-density normalization 会混合 TDC bin width、RO phase dynamics、placement coupling 和输入相位分布，不能作为独立校准。

## 校准目标

建立独立 LUT：

```text
raw TDC bin -> calibrated phase center
raw TDC bin -> estimated bin width
```

用于后续把 reset-aligned TDC / pair TDC 从 raw-bin 相对比较升级为 calibrated relative phase comparison。

## 推荐硬件设计

新增 sibling top：

```text
rtl/tdc/RO_TDC_code_density_cal_sysclk_top.v
```

设计要求：

1. 复用当前 `tdc_lane`、CARRY4 chain 数量、采样时钟和 UART packetizer。
2. TDC lane placement policy 尽量与 clean TDC / pair TDC 保持一致。
3. `hit_i` 不来自被研究的 random1/random3 RO pair，而来自独立 calibration RO。
4. calibration RO 与 `clk_200m` 异步，频率不要与采样时钟形成短周期锁相。
5. 可选支持 A/B lane swap，用来区分 source distribution 和 lane bin width。

最小模式：

```text
cal_ro_a -> tdc_lane_a
cal_ro_b -> tdc_lane_b
```

增强模式：

```text
cal_ro_a -> lane_a, cal_ro_b -> lane_b
cal_ro_b -> lane_a, cal_ro_a -> lane_b
common_cal_ro -> lane_a/lane_b
```

## 采集规模

最小 smoke：

```text
2 MiB per mode
约 262k packets
```

投稿建议：

```text
8 MiB 到 16 MiB per mode
至少 3 个 repeat 或 calibration-before / calibration-after
```

如果当前 TDC 物理 code space 约为 `0..64`，8 MiB 大约有 1,048,576 packets，均匀情况下每个 reachable code 约 16k counts，足够估计主要 DNL/INL 趋势。

## 分析输出

每个 lane 输出：

```text
bin
count
probability
width_ps_nominal
ideal_width_ps
DNL_lsb
INL_lsb
phase_center_ps_nominal
dead_code
```

注意这里的 `ps_nominal` 仍依赖 200 MHz sample period，即 5000 ps。它比 raw-bin 强，但仍要说明假设：校准输入相位在采样周期内近似均匀。

## 后处理脚本建议

现有：

```text
scripts/analyze_tdc_uart.py
```

已经有 code-density 函数，但默认是 same-run normalization。建议新增 wrapper：

```text
scripts/build_tdc_code_density_lut_20260525.py
scripts/apply_tdc_code_density_lut_20260525.py
```

第一个脚本：

```text
输入 calibration capture
输出 lane_a_lut.csv / lane_b_lut.csv / calibration_manifest.json
```

第二个脚本：

```text
输入 clean TDC 或 pair TDC packet CSV
输入 fixed LUT
输出 calibrated metrics
```

manifest 应记录：

```text
bitstream path
bitstream SHA256
capture SHA256
board id
mode
TDC lane placement
calibration source placement
capture bytes
packet count
XADC before/after 或 after-only
script version
```

## 和论文机制的关系

校准后可以增强两个论点：

1. 如果 calibrated TDC 仍不显示强 correlation/residence，则 hard-lock 排除更强。
2. 如果 sampler-local warmup12 在 calibrated phase diffusion 上仍更好，则 startup diffusion 解释更硬。

如果校准后 TDC 差异仍然很弱，也不是坏结果：

```text
TDC calibrated negative result further rules out RO phase locking/diffusion as the dominant factor, shifting the mechanism toward sampling-register/routing/aperture effects.
```

这仍然能服务论文，因为它把机制边界缩小了。

## 不要过度承诺

校准完成前：

```text
raw-bin relative TDC
code-density-normalized within-run TDC
```

校准完成后：

```text
dedicated code-density calibrated TDC
```

不要在当前数据上写：

```text
absolute ps-level jitter
```

