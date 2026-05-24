# Sample-RO locked passband goal 2026-05-25

## Goal

验证 sample RO 物理实现对 restart failure 是否具有可重复、可反事实解释的因果作用。

当前最强结果是：

```text
compact diagnostic + formal-auto sample RO locked + warmup4
=> p1 ~= 0.376796, worst x ~= 805
```

下一步不做泛泛 placement 扩展，而是围绕这个结果做最小高信息量矩阵。

## Hypotheses

- H1: 如果 locked warmup4 repeat 仍失败，说明 sample-RO locked 结果可重复，不是偶然采集。
- H2: 如果 locked warmup5 也失败，说明 formal sample RO 可能重塑整个 warmup passband。
- H3: 如果 locked warmup5 通过但 warmup4/11 失败，说明 sample RO 主要恢复 formal restart 的 warmup-window 敏感性。
- H4: 如果 locked repeat 不稳定，先检查 routed LOC/BEL、XADC、bitstream manifest 和 capture metadata，不继续盲目重复。

## Immediate matrix

| run | purpose |
| --- | --- |
| locked warmup4 repeat02 | 验证最关键因果结果可重复 |
| locked warmup5 run01 | 测原本 pass 窗口是否被 formal sample RO 拉坏 |
| locked warmup11 run01 | 测 formal 高偏 fail 窗口是否也被 sample RO 控制 |

## Script

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_sample_ro_locked_passband_queue_20260525.ps1 -WarmupList "4,5,11" -RecordXadc
```

Note: use `-WarmupList "4,5,11"` rather than relying on PowerShell comma binding.

输出目录：

```text
data\experiments\restart_fifo_diag_20260525
data\hardware\20260511_fpga1_board1\restart_fifo_diag
```

## Stop conditions

- 如果 warmup4 repeat 复现强失败：继续做 warmup5/11 和 local-good 反事实。
- 如果 warmup4 repeat 不复现：暂停扩展，优先查 bitstream、routing、XADC、metadata。
- 如果 warmup5/11 与 formal passband 对齐：论文主张可提升为 sample RO physical implementation reshapes restart passband。
- 如果 warmup5/11 不对齐：论文主张收敛为 sample RO 是关键边界因素之一，但 readout/control/full-top 仍参与。
