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

`random1` 10x1000 对照 pilot 已完成：

- bitstream：`data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit`
- 输出：`data\hardware\20260511_fpga1_board1\restart\random1_restart_pilot_10x1000_20260514.bin`
- 规模：10 restarts x 1000 UART byte symbols
- 输出大小：10,000 bytes
- SHA256：`C96F94F6529ACD50A7E70D20154F4E25DDC111732BC066F4ACB05352A2FF3428`
- metadata：`data\hardware\20260511_fpga1_board1\restart\random1_restart_pilot_10x1000_20260514.metadata.json`
- 重试次数：0
- bit-symbol MSB 展开：`data\hardware\20260511_fpga1_board1\restart\random1_restart_pilot_10x1000_20260514_bps1_msb.bin`
- bit-symbol MSB SHA256：`F0D399BC8EDB350BA45D4ED36E19404BB526F03BAB9F4E407A4F3BA97953F105`

至此，`random1` 坏 placement 和 `random3` 好 placement 都有同协议 restart pilot，可用于证明采集流程可复现，但仍不能写成正式 `ea_restart` 结果。

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

`random1` 10x1000 pilot 的总耗时为 2540.081 秒，约 42.33 分钟；但第 8、9 行仍出现明显 Vivado 初始化长尾，分别为 814.428 秒和 537.874 秒。按这个实测均值估算，正式 1000 行约 70.56 小时。

综合 `random1/random3` 两个 10x1000 pilot，reprogram-based formal restart 的合理预期是约 70-96 小时，取决于 Vivado/hw_server 初始化长尾。

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

## 2026-05-15 auto-stream formal restart 结果

为避免每行 Vivado 重新配置导致的 70-96 小时耗时，已实现并验证 `RO_TRNG_restart_auto_top`：

- 一次下载 bitstream；
- FPGA 内部执行 `HOLD -> DRAIN -> SETTLE -> SEND` 的 design-level restart 循环；
- UART 输出 row-major restart matrix；
- debug header 用于校验采集是否从矩阵起点开始。

关键工程修复：

- `START_DELAY_CYCLES` 扩展为 64 位，支持 60 秒启动延迟；
- `capture_90b_restart_dataset.ps1` 在 Vivado 编程完成后再次清串口输入缓冲；
- 采集脚本强制校验 8 字节 debug header，避免把旧 bitstream 残留数据当作矩阵起点。

已完成的真实硬件采集：

| 数据集 | 规模 | header | bytes | SHA256 | 用途 |
| --- | ---: | --- | ---: | --- | --- |
| `random3_restart_auto_formal_1000x1000_header_delay60s_20260515.bin` | `1000 x 1000` byte symbols | `A55A03E803E801D0` | `1000000` | `7789491D1DFE5E3C21225F6574D3C00D85800258B4CE930C89545CD3BA59E3D6` | 证明 auto-stream 长流采集能力；byte-symbol restart 数据 |
| `random3_restart_auto_formal_bits_1000x125_header_delay60s_20260515.bin` | `1000 x 125` packed bytes | `A55A03E8007D01D0` | `125000` | `A9B7BD143BE83CF63F7EF793B6D8409011A03EB8E70DE6828D1EFA4388A59338` | 展开为 `1000 x 1000` bit symbols |
| `random3_restart_auto_formal_bits_1000x125_header_delay60s_20260515_bps1_msb.bin` | `1000 x 1000` bit symbols | NA | `1000000` | `8C927742F11564F08722BDCC09616A2A15619038E4AC362D0C327C5B81706726` | `ea_restart` 输入 |

`ea_restart` 工具链也已在 Windows/MinGW 下修通：

- 原 NIST 代码在 Windows 中无法打开 `/dev/urandom` 后直接 `exit(-1)`；
- 已改为 deterministic seed fallback；
- `run_90b_restart.ps1` 已改为 `Start-Process` 捕获 stdout/stderr，避免 stderr 提示导致 PowerShell 误中断。

正式 non-IID restart 结果：

- 输入：`random3_restart_auto_formal_bits_1000x125_header_delay60s_20260515_bps1_msb.bin`
- `bits_per_symbol=1`
- `H_I=0.902345`，来源为 `random3_run01` full 8M bit-symbol MSB non-IID sequential 结果
- 输出目录：`data\sp800_90b\restart_results_20260515\random3_header_delay60s_bps1_msb_non_iid`
- 结果：**Restart Sanity Check Failed**
- `X_cutoff=605`
- `X_max=685`

矩阵诊断：

- overall `p1=0.497933`
- row 最大偏置：`row_x_max=545`，没有 row 超过 `605`
- column 最大偏置：`col_x_max=685`，发生在 `column 7`，该列 `ones=315`
- 超阈值来源：`cols_over_605=1`，`rows_over_605=0`
- 诊断文件：`data\sp800_90b\restart_results_20260515\random3_header_delay60s_bps1_msb_non_iid\restart_matrix_diagnostics.json`

解释：

这不是采集链路失败，而是一个有论文价值的负结果：`random3` 的 sequential bit-symbol non-IID 熵估计达到 `0.902345`，但 design-level restart matrix 在固定 column 上出现强偏置，导致 SP800-90B restart sanity check 失败。也就是说，普通连续流熵估计不能覆盖 restart 初始相位/早期采样位置的稳定性风险。该结果可作为“placement/RO 相互作用与 restart 相位动力学会影响熵源可信度”的核心证据之一。

LSB 位序对照也已完成：

- 输入：`random3_restart_auto_formal_bits_1000x125_header_delay60s_20260515_bps1_lsb.bin`
- `bits_per_symbol=1`
- `H_I=0.828444`，来源为 `random3_run01` smoke bit-symbol LSB non-IID sequential 结果
- 输出目录：`data\sp800_90b\restart_results_20260515\random3_header_delay60s_bps1_lsb_non_iid`
- 结果：**Restart Sanity Check Failed**
- `X_cutoff=632`
- `X_max=685`
- `col_x_max=685`，发生在 LSB 展开后的 `column 0`，该列 `ones=315`

MSB 中异常发生在 `column 7`，LSB 中异常发生在 `column 0`，二者对应同一个原始 UART byte 内的同一物理 bit 位置。因此该现象不是 MSB/LSB 展开顺序造成的假象，而是 restart 后固定 byte/bit 位置存在稳定偏置。后续高水平论文中应把它作为“restart 初期固定相位/固定输出位置风险”的核心实验观察，并与 TDC 相位漂移、RO_FREQ 频差以及 placement 耦合指标关联分析。

## 2026-05-15 random1 对照与 random3 repeat

已补 `random1` 同协议 bit-symbol formal restart，用于和 `random3` 形成 placement 对照：

| 数据集 | 规模 | header | bytes | SHA256 | 结果 |
| --- | ---: | --- | ---: | --- | --- |
| `random1_restart_auto_formal_bits_1000x125_header_delay60s_20260515.bin` | `1000 x 125` packed bytes | `A55A03E8007D01D0` | `125000` | `A9A4FFEAD5EA6CA15E74F13B3A068FFC59A156AEF28112F7D4B968E10470C512` | 展开为 formal bit-symbol restart |
| `random1_restart_auto_formal_bits_1000x125_header_delay60s_20260515_bps1_msb.bin` | `1000 x 1000` bit symbols | NA | `1000000` | `20BA93F6C3330A3DF9167BB590209A3BEB7BD57A420E3EB2B9BCF1236D37DE16` | `ea_restart` 通过 |
| `random1_restart_auto_formal_bits_1000x125_header_delay60s_20260515_bps1_lsb.bin` | `1000 x 1000` bit symbols | NA | `1000000` | `6961FEA5A07AED881C91DEAB6C0BAB8A27451F84FFCC4DAE7086EF9239444314` | `ea_restart` 通过 |

`random1` 的 `ea_restart` 结果：

- MSB：`H_I=0.389520`，`X_cutoff=821`，`X_max=680`，Validation Test Passed。
- LSB：`H_I=0.383737`，`X_cutoff=824`，`X_max=680`，Validation Test Passed。
- 列诊断：最坏原始位置仍是 `byte 0, bit 0`，`ones=320`，`zeros=680`，`p1=0.320`。

这说明 `random1` 因连续流 non-IID `H_I` 很低，restart sanity check 的 cutoff 更宽，所以 formal restart 通过；但 restart 初期固定位置偏置本身仍存在。

另补 `random3` 同 bitstream repeat02：

| 数据集 | 规模 | header | bytes | SHA256 | 结果 |
| --- | ---: | --- | ---: | --- | --- |
| `random3_restart_auto_formal_bits_1000x125_header_delay60s_repeat02_20260515.bin` | `1000 x 125` packed bytes | `A55A03E8007D01D0` | `125000` | `7CE2161474009731EA7AC3C7ACBD7E38443DD55AC6881DAA5D2F2FAAB4D10ED5` | 展开为 formal bit-symbol restart |
| `random3_restart_auto_formal_bits_1000x125_header_delay60s_repeat02_20260515_bps1_msb.bin` | `1000 x 1000` bit symbols | NA | `1000000` | `FDE530F346A969CC9BF1469184CDB417879654F16DABCDC698AC17755F1224D5` | restart sanity failed |
| `random3_restart_auto_formal_bits_1000x125_header_delay60s_repeat02_20260515_bps1_lsb.bin` | `1000 x 1000` bit symbols | NA | `1000000` | `78E5F2C380E7383214A26034EDC03245B6EE5EF0796A45202BC0B4922BA76AE4` | restart sanity failed |

`random3` repeat02 的 `ea_restart` 结果：

- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=680`，Restart Sanity Check Failed。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=680`，Restart Sanity Check Failed。
- 列诊断：最坏原始位置为 `byte 2, bit 7`，`ones=680`；`byte 0, bit 0` 仍明显偏置，`x=642`，也超过 MSB cutoff。

机制解释需要从“单一固定列绝对复现”修正为更稳妥的表述：

> auto-stream restart 后的早期 packed bytes 中存在可重复的强偏置热点。热点集中在 restart 初期若干固定采样位置，但最强位置可能随重新配置/初态发生漂移。连续流 non-IID 高熵估计不能保证 restart 初期固定输出位置稳定。

新增离线诊断与表格：

- `scripts/analyze_restart_matrix_columns.py`
- `scripts/make_restart_mechanism_table.py`
- `data\experiments\paper_artifacts_20260515\restart_column_bias_random3_formal_bits`
- `data\experiments\paper_artifacts_20260515\restart_column_bias_random1_formal_bits`
- `data\experiments\paper_artifacts_20260515\restart_column_bias_random3_formal_bits_repeat02`
- `data\experiments\paper_artifacts_20260515\table_restart_mechanism_link.csv`

## 2026-05-15 warmup8 初步结果

已补 `random3` 的 `WARMUP_BYTES=8` auto-stream formal bit-symbol restart，用于检查“简单丢弃 restart 后最早 8 个 packed bytes”是否足以消除早期固定位置偏置。

数据文件：

- packed 输入：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_20260515.bin`
- 规模：`1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols
- header：`A55A03E8007D01D0`
- packed bytes：`125000`
- packed SHA256：`4ECD7CCE25B950BE4F1B6715BD877B2D7A4CA1286D04B6B397D2BC0FB4357423`
- MSB bps1 SHA256：`C99D78E132F6CF6C01A9E29D80A7705960B7BA2478B05F02AD292ACA1C13C8E2`
- LSB bps1 SHA256：`20B43E5E28B65FFAED027F9931A212AC2A703A084E012C00A5A26CEA76532785`

`ea_restart` 结果：

- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=721`，Restart Sanity Check Failed。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=721`，Restart Sanity Check Failed。
- 最坏原始位置：`byte 2, bit 2`，`ones=279`，`zeros=721`，`p1=0.279`，`x=721`。
- 展开后位置：MSB `column 21`，LSB `column 18`。
- overall `p1=0.374385`。
- `positions_over_x_cutoff=893`。

谨慎结论：warmup8 不支持“简单丢弃最早 8 packed bytes 即可修复 restart 偏置”的说法。相反，它提示 restart 后状态/相位窗口可能会随 warmup 设置改变，并在新的采样窗口中暴露更强、更广泛的偏置。论文和状态文档里应把它写成初步负结果：warmup 是一个需要系统扫描的实验变量，不能作为未经验证的补救措施。

## 2026-05-15 warmup10 formal-size restart 结果

已补 `random3` 的 `WARMUP_BYTES=10` auto-stream formal-size bit-symbol restart。该结果只表示本板、本 placement、本次 auto-stream restart 条件下，丢弃前 10 个 packed bytes 仍不足以稳定通过 restart sanity check。

数据文件：
- packed 输入：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_20260515.bin`
- 规模：`1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols
- header：`A55A03E8007D01D0`
- packed bytes：`125000`
- packed SHA256：`90810C80B5936DF71B184D37E357E85FE05D33ED83CB0E5D0748906FF9BC6597`
- MSB bps1 SHA256：`597D930EACFFEACD5E18662DD668379B354B598BAB6C366CE718FED57EC13658`
- LSB bps1 SHA256：`65D98ED5D6B7F4E0DE0735D19559B7FB3C8A6C8817759452A5A197AB3102519D`

`ea_restart` 结果：
- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=650`，Restart Sanity Check Failed。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=650`，Restart Sanity Check Failed。

列诊断：

- overall `p1=0.415017`。
- `positions_over_x_cutoff=106`。
- 最坏原始位置：`byte 1, bit 4`，`ones=350`，`zeros=650`，`p1=0.350`，`x=650`。
- 展开后位置：MSB `column 11`，LSB `column 12`。

## 2026-05-15 warmup12 formal-size restart 结果

已补 `random3` 的 `WARMUP_BYTES=12` auto-stream formal-size bit-symbol restart。该结果与 warmup16 一样只表示本板、本 placement、本次 auto-stream restart 条件下的一次 formal-size restart 通过，不能写成最终 SP800-90B 认证或跨板/PVT 结论。

数据文件：

- packed 输入：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_20260515.bin`
- 规模：`1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols
- header：`A55A03E8007D01D0`
- packed bytes：`125000`
- packed SHA256：`E5F690CF5545F5EBF7271175472F2B2D36033E750C060F569B196CC08CB3B2C0`
- MSB bps1 SHA256：`BDB6521AFF45F2FDC9F489CDB4AF2E4019E33241BA6D0EAE72CC20EE1FB6D297`
- LSB bps1 SHA256：`E32B02B0E8ECA8FB0CF31B6803F3B4E545279640E35D30B2E2BB08FD2F22D299`

`ea_restart` 结果：
- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=562`，Validation Test Passed，`H_r=0.867146`，`H_c=0.849807`，`min=0.849807`。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=562`，Validation Test Passed，`H_r=0.866043`，`H_c=0.836130`，`min=0.828444`。

列诊断：

- overall `p1=0.499478`。
- `positions_over_x_cutoff=0`。
- 最坏原始位置：`byte 88, bit 3`，`ones=562`，`zeros=438`，`p1=0.562`，`x=562`。
- 展开后位置：MSB `column 708`，LSB `column 707`。

## 2026-05-15 warmup16 formal-size restart 结果

已补 `random3` 的 `WARMUP_BYTES=16` auto-stream formal-size bit-symbol restart。该结果只表示本板、本 placement、本次 auto-stream restart 条件下的一次 formal-size restart 通过，不能写成最终 SP800-90B 认证或跨板/PVT 结论。

数据文件：

- packed 输入：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup16_header_delay60s_20260515.bin`
- 规模：`1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols
- header：`A55A03E8007D01D0`
- packed bytes：`125000`
- packed SHA256：`8084E1AB95062564ACE582113520A54163CADA96E12C1A2211DE2C044AC860E7`
- MSB bps1 SHA256：`16776DFF817D178B05C8479C634469C55B130740F7719412A5D0257DBD384D0B`
- LSB bps1 SHA256：`EFF66AE869332A04F38FE3F1FB93DCE1D398ACAEC57C6126CFDECBA0AF3DD1B5`

`ea_restart` 结果：

- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=549`，Validation Test Passed，`H_r=0.871037`，`H_c=0.868735`，`min=0.868735`。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=549`，Validation Test Passed，`H_r=0.820090`，`H_c=0.830192`，`min=0.820090`。

列诊断：

- overall `p1=0.499126`。
- `positions_over_x_cutoff=0`。
- 最坏原始位置：`byte 43, bit 7`，`ones=547`，`zeros=453`，`p1=0.547`，`x=547`。
- 展开后位置：MSB `column 344`，LSB `column 351`。

当前 warmup 扫描结论：warmup0/warmup8/warmup10 失败，warmup11/warmup12/warmup16 通过，说明 restart 初期至少前若干 packed bytes 属于不稳定或偏置窗口，并存在可通过 sufficient warmup 消除的相变。当前在本板、本 placement、本 auto-stream restart 协议下，可把通过阈值收窄为 `10 < WARMUP_BYTES <= 11`；不能写成最终 SP800-90B 认证或跨板/PVT 结论。

## 2026-05-15 warmup11 formal-size restart 结果

已补 `random3` 的 `WARMUP_BYTES=11` auto-stream formal-size bit-symbol restart。该点是当前 warmup 边界扫描的关键分界点：warmup10 仍失败，而 warmup11 已经通过。

数据文件：

- packed 输入：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_20260515.bin`
- 规模：`1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols
- header：`A55A03E8007D01D0`
- packed bytes：`125000`
- packed SHA256：`4418C3D6550684637B56121F96A906F48B128B63139991A3B8C827D2C30A6BA9`
- MSB bps1 SHA256：`4EBF7244063138838227327180911E4F2F69D4D30299A8D9D5875810ECF7E5A1`
- LSB bps1 SHA256：`573A87D6E22F0B14485AD3657BB9E0C4A2C9B4FB3AD499065100F9E0AD248E33`

`ea_restart` 结果：

- MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=583`，Validation Test Passed，`H_r=0.743385`，`H_c=0.756293`，`min=0.743385`。
- LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=583`，Validation Test Passed，`H_r=0.753865`，`H_c=0.759525`，`min=0.753865`。

列诊断：

- overall `p1=0.469088`。
- `positions_over_x_cutoff=0`。
- 最坏原始位置：`byte 1, bit 3`，`ones=417`，`zeros=583`，`p1=0.417`，`x=583`。
- 展开后位置：MSB `column 12`，LSB `column 11`。

论文用汇总表：

- `data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.csv`
- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.csv`
