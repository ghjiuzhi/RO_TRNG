# sample RO locked passband 实验结果记录 2026-05-25

## 结论摘要

本轮实验把 `sample RO` 的作用从“可疑因素”推进到了更强的反事实证据：

> 在 compact FIFO diagnostic 结构中，仅把 sample RO 锁回 formal auto w4 retest 的 routed LOC/BEL，就能把原本 near-ideal 的 restart 输出重新拉回强偏置失败状态。  
> 因此，RO-TRNG 的熵源边界不能只画到 data RO 和 sampled-data registers，还必须包含 sample RO、采样路径局部路由，以及其附近的 readout/control 物理实现。

更关键的是，warmup5 原本在 compact diagnostic 中接近理想，但在 formal-routed sample RO locked 版本中也变成强低偏：

| design | sample RO | warmup | matrix | overall p1 | worst bit | worst p1 | worst x | interpretation |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | --- |
| compact FIFO diag | compact routed | 4 | `1000 x 125` | `0.498297000` | byte1 bit7 | `0.445` | `555` | near ideal |
| compact FIFO diag | compact routed | 5 | `1000 x 125` | `0.498316000` | byte26 bit1 | `0.549` | `549` | near ideal |
| compact FIFO diag | compact routed | 11 | `1000 x 125` | `0.498148000` | byte90 bit6 | `0.452` | `548` | near ideal |
| compact FIFO diag | formal-routed sample RO locked | 4 run01 | `1000 x 125` | `0.376796000` | byte0 bit5 | `0.195` | `805` | low-bias fail restored |
| compact FIFO diag | formal-routed sample RO locked | 4 repeat03 | `1000 x 125` | `0.376651000` | byte0 bit5 | `0.116` | `884` | low-bias fail reproduced |
| compact FIFO diag | formal-routed sample RO locked | 5 | `1000 x 125` | `0.373430000` | byte2 bit2 | `0.243` | `757` | original pass window pulled bad |
| compact FIFO diag | formal-routed sample RO locked | 11 | `1000 x 125` | `0.464819000` | byte18 bit4 | `0.424` | `576` | weaker but still biased |
| formal auto | compact-routed sample RO locked | 4 | `1000 x 125` | `0.499419000` | byte61 bit6 | `0.552` | `552` | formal w4 low-bias fail repaired |

这个结果支持更强的论文表述：

> Sample-RO physical implementation reshapes the restart warmup passband. A placement that is near ideal with a compact-routed sampler can become strongly biased when only the sampler RO is locked to the formal routed implementation.

## 关键文件

sample RO locked XDC：

```text
data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc
```

warmup4 repeat03 完整复现实验：

```text
bitstream:
data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_sample_ro_formal_locked_warmup4_1000x125/RO_TRNG_restart_fifo_compact_diag_top.bit

capture:
data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.bin

capture SHA256:
A34F4E7C6CD61C8EA9EE9C1C95DCDDEACBCA37ABC0F849093D5904B034B26033

bitstream SHA256:
0E0844FBEF68468AD545CC6B819B4F54F1EAA04AF1804E90EF5417A271420F69

summary:
data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.summary.md
```

warmup5 formal-routed sample RO locked：

```text
capture:
data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.bin

capture SHA256:
AF82E88A362F51624C88ACB63A23B7574A4245062E894A3DA1D47E962199BB85

bitstream SHA256:
D2A092A698F3185AB1A969C83792A0FF6AA2A684A48074E76EE53C766AC394E7

summary:
data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.summary.md
```

warmup11 formal-routed sample RO locked：

```text
capture:
data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.bin

capture SHA256:
714C29CB96098DF231C0D0FEAEB8C49CEFFC745A1E73AFE1F66D03381C8FB37C

bitstream SHA256:
E5E133A13C197402CA1ED842F37D32A78577DF06AB77DCB66C9CA114A55900E0

summary:
data/experiments/restart_fifo_diag_20260525/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.summary.md
```

队列汇总：

```text
data/experiments/restart_fifo_diag_20260525/sample_ro_locked_passband_queue_summary_20260525.csv
```

## XADC 采集顺序的重要发现

本轮还发现一个会影响 restart 实验有效性的工程问题：

```text
program bitstream -> read XADC before_capture -> open COM3
```

这个流程会破坏 restart auto-stream capture。现象是：

| run | XADC mode | result |
| --- | --- | --- |
| new w4 locked build run02 | before_capture | partial capture `10686` bytes, no valid header alignment |
| old exact w4 bitstream repeat02 | before_capture | partial capture `44279` bytes |
| old exact w4 bitstream repeat03 | no XADC before | complete `125016` bytes |
| w5 / w11 after-only | after_capture only | complete `125016` bytes |

原因判断：

- restart bitstream 在下载后会按内部 start delay 自动吐数据。
- 如果在串口打开前先用 Vivado 读 XADC，会延迟并干扰 PC 端打开串口的时刻。
- 对这种自动流式输出设计，PC 端可能错过 header 或错过前段数据，随后进入错位/断流/idle timeout。

因此脚本已经修改为支持：

```powershell
-RecordXadc -XadcMode after_only
```

后续 restart capture 默认应该使用 after-only XADC。若必须记录 before/after，应改 FPGA 端协议，例如先等待 PC 命令再启动 stream，而不是配置完成后自动开始。

相关脚本改动：

```text
scripts/capture_uart.ps1
scripts/program_and_capture_uart.ps1
scripts/run_sample_ro_locked_passband_queue_20260525.ps1
```

## 反向因果闭环：formal auto + compact sample RO

为了避免只得到“formal sample RO 能把 compact diagnostic 拉坏”的单向结论，本轮又做了反向实验：

```text
formal auto top + random1 regs-only placement + compact-routed sample RO locked + warmup4
```

新增 XDC：

```text
data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_compact_w4_locked.xdc
```

该 XDC 基于：

```text
data/experiments/xdc_sampler_island/random1_sampler_regs_only_x45y31.xdc
```

然后只把 sample RO 的 `RO_SAMPLE_NAND` 和 `RO_SAMPLE_LOOP[0..7]` 锁到 compact FIFO diagnostic w4 routed LOC/BEL。和 formal-routed sample RO 相比，实际关键差异只有三个 LUT：

| cell | formal routed | compact routed |
| --- | --- | --- |
| `RO_SAMPLE_NAND` | `SLICE_X47Y33/A6LUT` | `SLICE_X46Y34/B6LUT` |
| `RO_SAMPLE_LOOP[1]` | `SLICE_X46Y32/B6LUT` | `SLICE_X47Y33/A6LUT` |
| `RO_SAMPLE_LOOP[7]` | `SLICE_X49Y45/B6LUT` | `SLICE_X49Y45/A6LUT` |

反向实验结果：

```text
bitstream:
data/vivado_runs/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_20260525/RO_TRNG_restart_auto_top.bit

bitstream SHA256:
AE70EE95710E955760D7717E7D5439B6B6D6E5BD0F15DEF09587D1E874734862

capture:
data/hardware/20260511_fpga1_board1/restart/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run01_20260525.bin

capture format:
8-byte formal auto header + 125000-byte row-major restart body

capture SHA256:
6B8AE4FB0040029F41D6AE22A49A55BE8E9AEEEDA84CA6A2C6DF04B1CD4EECAD

packed body:
data/experiments/restart_fifo_diag_20260525/restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run01_20260525.send_packed.bin

packed SHA256:
046E4826BA5018828A2F488DE60F9A06609C118952F2576892FC261379BB3E4A
```

统计结果：

```text
overall p1 = 0.499419000
overall min-H = 0.998324562
row ones std = 16.521484165
worst position = byte 61 bit 6
worst p1 = 0.552000000
worst x = 552
```

这说明 formal auto w4 原本的低偏失败可以被 compact-routed sample RO 修复到接近理想。结合前面的单向实验：

```text
compact top + formal sample RO -> strong fail
formal top + compact sample RO -> near ideal
```

这形成了目前最强的双向反事实证据。论文中可以把它写成：

> Moving only a few sampler-RO LUT BEL/LOC assignments can flip the restart outcome in both directions. This is inconsistent with a model where the readout circuit is passive, and supports treating the sampler RO and its immediate physical neighborhood as part of the entropy-source boundary.

注意：这条 formal auto capture 是 `125008` bytes，不是脚本原本期待的 `125016` bytes。原因是 formal auto header 为 8 bytes，而 compact diagnostic header 为 16 bytes；capture 脚本按 16-byte compact 长度等待，导致最后 timeout，但文件本身包含完整 `8 + 125000` bytes，可以有效分析。后续应为 formal auto 和 compact diagnostic 分开设置 expected bytes。

## 复现实验命令

复现 warmup5 / warmup11 after-only XADC 队列：

```powershell
cd E:\Project\MLDSA\RO_TRNG
powershell -ExecutionPolicy Bypass -File scripts\run_sample_ro_locked_passband_queue_20260525.ps1 `
  -WarmupList "5,11" `
  -RecordXadc `
  -XadcMode after_only
```

复现旧 exact bitstream warmup4 repeat：

```powershell
cd E:\Project\MLDSA\RO_TRNG
powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart.ps1 `
  -VivadoBat C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat `
  -Bitstream data\vivado_runs\restart_fifo_compact_diag_random1_regs_only_sample_ro_formal_locked_warmup4_1000x125\RO_TRNG_restart_fifo_compact_diag_top.bit `
  -Port COM3 `
  -Baud 115200 `
  -Kind restart `
  -Run restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525 `
  -Bytes 125016 `
  -OutFile data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.bin `
  -MetadataDir data\hardware\20260511_fpga1_board1\metadata `
  -IdleTimeoutSec 300 `
  -BoardId z7020_b01
```

分析命令：

```powershell
python scripts\analyze_restart_fifo_compact_diag.py `
  --input data\hardware\20260511_fpga1_board1\restart_fifo_diag\<capture>.bin `
  --out-dir data\experiments\restart_fifo_diag_20260525 `
  --label <label>

python scripts\analyze_restart_matrix_columns.py `
  --input data\experiments\restart_fifo_diag_20260525\<label>.send_packed.bin `
  --restart-count 1000 `
  --bytes-per-restart 125 `
  --label <label> `
  --out-dir data\experiments\restart_fifo_diag_20260525\<label>.column_analysis
```

## 论文机制解释

目前证据链可以这样写：

1. Pair-TDC correlation 接近 0，排除了“简单 RO-RO hard locking 是主因”的解释。
2. sampler-register ablation 能把 random1 continuous stream 修到近理想，说明 sampler-side placement 是可控变量。
3. compact FIFO diagnostic 在 warmup4/5/11 都接近理想，说明 bias 不是 data byte generator 的简单统计失衡。
4. formal auto w4 retest 复现低偏失败，说明 formal restart failure 是真实可复现现象。
5. 只把 sample RO 锁回 formal routed implementation，就让 compact diagnostic 重新进入强低偏失败，并且 warmup5 也从 near-ideal 变为强低偏。
6. 反过来，只把 formal auto 的 sample RO 锁回 compact routed implementation，又把 formal warmup4 修回近理想。

因此当前最强主张是：

> TDC evidence rules out simple pairwise RO locking, while counterfactual restart placement experiments show that sampler-side physical implementation, especially the sample RO and its local routing/neighboring control logic, reshapes the restart startup passband. The sampler path must be treated as part of the physical entropy-source boundary rather than a passive readout circuit.

## 下一步建议

优先级最高的下一步不是盲目扩大量，而是补两个最小反事实：

1. `formal auto` 中把 sample RO 锁回 compact-routed LOC/BEL，测试 formal w4 是否被修好。
2. 对 locked w5 做一次 repeat，确认 warmup5 被拉坏不是单次构建偶然。

如果这两个也成立，论文机制会从“强证据”进一步接近“因果闭环”。
