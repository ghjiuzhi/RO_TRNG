# 下一批机制实验路线图 2026-05-25

## 当前结论状态

本轮补充后，TDC 的角色已经更清楚：

1. pair-specific TDC：12 个 runs、192 个窗口，fixed-LUT 复算后 strong-lock windows = 0，最大 small-lag `|r|` 约 0.03137。
2. sampler-data TDC：6 个 runs、96 个窗口，fixed-LUT 复算后 strong-lock windows = 0，最大 small-lag `|r|` 约 0.0273。
3. clean reset-aligned TDC：6 点矩阵，LUT 复算后相位差自相关仍接近 0，raw longest differential-bin run 仍为 3。
4. sample RO 双向反事实：仍是当前最强因果证据；只改变 sampler-side physical implementation 就能翻转 restart outcome。

因此，下一步不应继续盲目重复同类 TDC。更好的策略是围绕“采样端物理边界”做能区分机制的实验。

## 机制判断

当前最稳的论文写法是：

```text
TDC evidence rules out simple pairwise RO hard locking and simple sampler-data phase locking as dominant explanations. The decisive effect is more likely in sampler-side implementation: sample RO, sampling registers, local routing, and sampling aperture.
```

中文表述：

```text
TDC 排除了简单 RO-RO hard locking 和简单 sampler-data phase locking 作为主导解释。真正主导 placement 敏感性的机制更可能位于采样端物理实现，包括 sample RO、采样寄存器、局部路由和采样孔径。
```

## P0：restart bit-order / packing 反事实

### 假设

restart fixed-column failure 可能由两类因素造成：

1. 物理采样时刻本身有固定偏置热点；
2. 输出 bit packing / bit order 把某些固定采样位置暴露成 SP800-90B column failure。

### 实验目标

不改 entropy source，只改变输出映射或后处理映射，观察 worst column 是否跟随 bit-order/packing 移动。

### 执行状态

已完成。脚本：

```text
scripts/analyze_restart_packing_counterfactual_20260525.py
```

输出：

```text
data/experiments/restart_packing_counterfactual_20260525/
```

有效数据 31 个，跳过 4 个不满足 `1000x125` packed-byte 大小约束的数据。31/31 个有效 run 在 MSB-first 与 LSB-first 展开下会把同一个 packed `byte.bit` 热点映射到不同 expanded column；31/31 个有效 run 在 byte-order reversal 下也会移动列号。

### 离线实验定义

输入：

```text
data/hardware/20260511_fpga1_board1/restart/*1000x125*.bin
```

处理：

1. MSB-first 展开。
2. LSB-first 展开。
3. byte 内 bit-reversal 后展开。
4. byte-order reversal 后展开。
5. 可选：固定 cyclic bit shift。

输出：

```text
data/experiments/restart_packing_counterfactual_20260525/
```

判据：

- 若 worst column 跟着 bit-order/byte-order 映射移动，说明 output mapping 暴露了固定采样位置。
- 若 worst physical byte/bit 不随映射解释而移动，说明偏置更接近物理采样窗口。

论文价值：

这是解释 SP800-90B restart fixed-column bias 的高价值补充，且不需要新硬件。当前结论是：论文中不应把固定列号写成物理实体，而应写成固定采样位置或固定输出位置偏置被 packing 映射投影到 SP800-90B matrix column。

## P1：sampler-only / registers-only 小扰动

### 假设

sample RO 不是唯一因素；sampling registers 和 routing island 可能才是更关键的采样孔径边界。

### 当前证据

已有结果显示：

- sample RO 双向反事实能翻转 restart outcome；
- sampler-data TDC 没有显示直接相位锁定；
- 因此机制更可能在 sampling register/routing/aperture。

### 新硬件矩阵

最小矩阵：

| run | data RO | sample RO | sampling regs | 目的 |
| --- | --- | --- | --- | --- |
| baseline | random1 | baseline | baseline | 坏例 |
| sample-only local | random1 | local | baseline | 测 sample RO 单独贡献 |
| regs-only local | random1 | baseline | local | 测寄存器/路由单独贡献 |
| sample+regs local | random1 | local | local | 测完整 sampler island |

每个 run 优先：

```text
20 MiB continuous TRNG
1000x125 restart warmup4/11 或 warmup0/12
XADC after-only；command-gated 完成后再补 before/after
```

判据：

- sample-only 修复但 regs-only 不修复：sample RO 主导。
- regs-only 修复但 sample-only 不修复：sampling register/routing 主导。
- 两者都部分修复，sample+regs 最好：sampler-side physical boundary 是组合效应。

## P2：all-on / single-on 局部开关扰动

### 假设

RO 群同时振荡造成局部供电/开关活动扰动，影响 sample RO 或采样孔径。该机制不一定表现为 hard locking。

### 执行状态

已启动 TDC mask-perturb 版本，优先在 TDC 层验证该机制，避免直接大改 TRNG 主链路。新增状态文档：

```text
doc/tdc_mask_perturb_status_20260525.md
```

已完成：

- 新增 `RO_TDC_pair_mask_perturb_top` 和 `tdc_ro_mask_matrix`；
- 生成 random1/random3 full-matrix TDC placement XDC；
- 构建 P0 bitstream；
- 完成 `random1 RO0/RO1 pair_only` 1MiB 硬件 smoke；
- smoke 解码得到 `131071` packets，`phase_pearson_r=-0.000707`，`longest_same_diff_bin_run=3`。

结论：新 top 能在真实硬件上稳定输出，P0 8MiB mode 对照可以进入正式采集。

### 实验目标

同一 TDC pair 或 RO_FREQ probe 下，改变周围 RO 是否开启。

矩阵：

| mode | 说明 |
| --- | --- |
| single-on | 只开被测 sample/data RO |
| neighbor-on | 开邻近 RO |
| all-on | 开全部 data RO + sample RO |

指标：

- RO_FREQ sample shift ppm；
- TDC bin distribution / phase_diff_std；
- TRNG p1 / min-H；
- XADC after temperature/voltage。

判据：

若 all-on 与 single-on 相比改变 sample frequency 或 TDC distribution，而 TRNG bias 同步变化，说明局部开关活动/供电扰动参与机制。

## P3：command-gated capture

command-gated 不是论文创新点，但它能提高采集严谨性，尤其用于：

- before/after XADC；
- restart header 不丢失；
- reset-aligned TDC 精确触发。

前置条件：

1. 确认 fpga1 PL UART_RX pin。
2. 做 UART RX echo smoke。
3. 再移植到 restart/TDC command-gated top。

## 当前不建议

1. 不建议继续对同一 pair 做更多 2 MiB TDC repeat，除非已有结果出现矛盾。
2. 不建议把 TDC 写成“证明 sampler-side 机制”的唯一证据。
3. 不建议大改已经可复现的 restart/sample RO 反事实 RTL。

## 立即执行顺序

1. 先做 P0 restart packing 离线反事实。
2. 同时梳理 sampler-only / regs-only 已有 bitstream 与缺口。
3. 若硬件空闲且 bitstream 已存在，优先跑 P1 中缺失的 sampler-only/regs-only 20 MiB 或 restart warmup 对照。
4. P2 all-on/single-on 需要确认现有 RO_FREQ/TDC top 是否已支持 enable mode；若不支持，先写设计规格，不急着上板。
