# SP800-90B Restart 执行状态 - 2026-05-14

更新时间：2026-05-14 18:55。

## 当前结论

已经把 restart dataset 从“计划”推进到“可执行脚本 + 真实硬件 smoke”阶段。

新增脚本：

- `scripts/capture_90b_restart_dataset.ps1`
- `scripts/run_90b_restart.ps1`
- `scripts/convert_restart_bytes_to_bits.py`

真实硬件 smoke 已完成：

- bitstream：`data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit`
- 输出：`data\hardware\20260511_fpga1_board1\restart\random3_restart_smoke_2x16_20260514.bin`
- 规模：2 restarts x 16 symbols
- 输出大小：32 bytes
- SHA256：`29CE915227539459DEC278043F2A9E96A92D459FF175B6EDD5B3C0928DE532A9`
- metadata：`data\hardware\20260511_fpga1_board1\restart\random3_restart_smoke_2x16_20260514.metadata.json`
- 重试次数：0

这个 smoke 只证明控制链路可行：每行重新 program bitstream、等待 settle、清空串口缓冲、读取固定长度 row、写 row-major dataset、生成 SHA256 和 metadata。它不能作为正式 SP800-90B restart 结果。

真实硬件 10x1000 pilot 也已完成：

- bitstream：`data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit`
- 输出：`data\hardware\20260511_fpga1_board1\restart\random3_restart_pilot_10x1000_20260514.bin`
- 规模：10 restarts x 1000 UART byte symbols
- 输出大小：10,000 bytes
- SHA256：`65DB9381346C2CCB782DE4DD6425F80498A74F6C90437F10B751AA53D8E500AC`
- metadata：`data\hardware\20260511_fpga1_board1\restart\random3_restart_pilot_10x1000_20260514.metadata.json`
- 重试次数：0
- bit-symbol MSB 展开：`data\hardware\20260511_fpga1_board1\restart\random3_restart_pilot_10x1000_20260514_bps1_msb.bin`
- bit-symbol MSB SHA256：`40C99D88BAB33C7AE6B1B097244245C89B1771E03CEE324FBC87448DAF521538`

这个 pilot 验证了 1000-symbol 行长度的采集流程，但仍不能作为正式 SP800-90B restart 结果，因为 `ea_restart` 正式要求 1000 x 1000 samples。

## 关键时间成本

本次 2 行 smoke 的总耗时为 345.402 秒。

逐行耗时：

| restart index | bytes written | duration seconds |
| ---: | ---: | ---: |
| 0 | 16 | 178.296 |
| 1 | 16 | 166.804 |

10x1000 pilot 的总耗时为 3454.446 秒，约 57.57 分钟。

逐行耗时：

| restart index | bytes written | duration seconds |
| ---: | ---: | ---: |
| 0 | 1000 | 171.173 |
| 1 | 1000 | 231.627 |
| 2 | 1000 | 784.772 |
| 3 | 1000 | 245.158 |
| 4 | 1000 | 387.944 |
| 5 | 1000 | 169.097 |
| 6 | 1000 | 674.290 |
| 7 | 1000 | 316.463 |
| 8 | 1000 | 331.145 |
| 9 | 1000 | 142.613 |

按 10x1000 pilot 的实测均值估算，如果使用“每行 Vivado 重新配置 bitstream”作为 restart 方法，正式 1000 x 1000 restart dataset 约需 96 小时，且期间独占 JTAG、COM3 和 hw_server。

这个方法语义最清楚，但不适合“明天晚上前顺手补完”。如果必须在短时间内得到正式 restart 证据，需要增加一个可审计的 design-level reset 或 board-level reset 流程。

## ea_restart 工具约束

本地 `ea_restart.exe` 用法：

```powershell
ea_restart [-i|-n] [-v] [-q] [-s <simulation count>] <file_name> [bits_per_symbol] <H_I>
```

关键约束：

- 正式输入必须是 SP800-90B row dataset。
- 工具要求 1000 restarts x 1000 samples，即 1,000,000 个 one-byte symbols。
- `bits_per_symbol` 必须为 1 到 8。
- `<H_I>` 应来自对应 sequential dataset 的 non-IID 估计。
- 小规模 2x16、10x1000、100x1000 只能验证脚本和流程，不能报告为正式 restart test。

格式注意：

- `capture_90b_restart_dataset.ps1` 保存的是 UART 原始 byte row dataset。
- 若论文采用 bit-symbol entropy，即 `bits_per_symbol=1`，不能直接把 packed byte 文件传给 `ea_restart`。
- 应先用 `scripts/convert_restart_bytes_to_bits.py` 做 row-preserving 展开，生成 one-byte-per-bit 的 restart dataset，并在 metadata 中记录 MSB/LSB bit order。
- 展开后每行 symbol 数会变成原来的 8 倍；正式 `ea_restart` 仍要求总样本数为 1,000,000，因此若使用 bit-symbol 路线，采集规模要按目标 row/column 重新设计，不能随意混用。

## 下一步建议

P0：不要把已有连续 `.bin` 伪装成 restart dataset。

P0：短期论文中可以写：restart 采集协议与脚本已实现，并完成 2-row 硬件链路验证；正式 1000x1000 restart 尚未完成，因此不能声称完整 SP800-90B 认证。

P1：检查 RTL 是否能加入 design-level restart。这个 reset 必须覆盖：

- RO 使能/采样控制；
- TRNG 后处理或 XOR/采样状态；
- FIFO；
- UART 输出状态机；
- 任何计数器、valid/ready、缓存寄存器。

P1：如果能证明 design-level reset 等价于熵源 restart，则优先用它采集 1000x1000；否则只能安排约 2 天的 reprogram-based formal run。

P2：正式 `random3` restart 完成后，再决定是否给 `random1` 坏例也做 restart，形成好/坏 placement 的 restart 对照。

## Design-Level Restart 初步审计

已检查 `rtl\RO_TRNG_top.v` 和 `rtl\RO.v`。当前顶层有 `por_n_i`，但 `entropy_source.en` 固定为 `1'b1`，FIFO 也没有在顶层显式 reset 连接。因此它还不能直接作为严谨的快速 restart 方法。

详细分析见：

- `doc/sp800_90b_design_reset_feasibility_20260514.md`
