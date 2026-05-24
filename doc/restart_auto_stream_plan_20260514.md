# Restart Auto-Stream 方案状态 - 2026-05-14

更新时间：2026-05-14 22:40。

## 为什么新增这条方案

前面的真实硬件 pilot 已经证明：

- `scripts/capture_90b_restart_dataset.ps1` 的 row-major restart 采集协议是可执行的。
- 但 `program_bitstream` 逐行 restart 的正式 `1000 x 1000` 成本过高，实测推算约 `70-96` 小时。

因此，当前最值得推进的工程动作不是继续硬跑 reprogram-based formal run，而是做一个**单次下载 bitstream、板上自动按行 restart 并连续吐出 row-major 数据**的新实验顶层。

这个方案的目标不是替代原始 baseline `RO_TRNG_top`，而是提供一条专门用于 `SP800-90B restart dataset` 的快速采集路径。

## 当前已完成的实现

本轮已新增：

- `rtl/restart/RO_TRNG_restart_auto_top.v`
- `data/experiments/xdc_restart/restart_sysclk_base.xdc`
- `scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl`
- `scripts/capture_90b_restart_dataset.ps1` 新增 `-RestartMethod auto_stream_once`

## 顶层行为

`RO_TRNG_restart_auto_top` 使用现有可确认的 `fpga1` 引脚：

- `sys_clk -> U18`
- `por_n_i -> N16`
- `UART_TX_o -> J15`

不依赖当前仓库中缺失的 `UART_RX_i` 板级约束。

设计行为是：

1. 上电后先 `HOLD`，关闭 RO。
2. `DRAIN` 掉 FIFO 残留。
3. 进入 `SETTLE`，打开 RO，等待固定周期。
4. 可选 `WARMUP` 丢弃若干字节。
5. 进入 `SEND`，连续输出一行 `ROW_BYTES` 数据。
6. 自动再次 `HOLD`，重复直到完成 `RESTART_COUNT` 行。

因此，host 侧不需要每行重新 program bitstream；只需要：

- 下载一次 `.bit`
- 打开串口
- 读取总计 `RESTART_COUNT * ROW_BYTES` 字节

## 当前构建状态

已完成一次 `random3` placement 的实现 smoke：

- placement XDC：`data/experiments/xdc_matrix/ro_random_seed3_x36y35.xdc`
- out dir：`data/vivado_runs/restart_auto_random3_smoke`
- smoke generics：`RESTART_COUNT=4`、`ROW_BYTES=64`

当前已确认产出：

- bitstream：`data\vivado_runs\restart_auto_random3_smoke\RO_TRNG_restart_auto_top.bit`
- manifest：`data\vivado_runs\restart_auto_random3_smoke\manifest.txt`

这说明：

- 新增 RTL 能通过综合、布局布线和 bitstream 导出主流程；
- base XDC 与 placement XDC 组合可以用于实际实现；
- restart-only 顶层方向在工程上已经落地，不再只是方案草图。

## 当前硬件 smoke 状态

已完成一次真实硬件 auto-stream smoke：

- bitstream：`data\vivado_runs\restart_auto_random3_smoke\RO_TRNG_restart_auto_top.bit`
- 输出：`data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_smoke_4x64_20260514.bin`
- metadata：`data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_smoke_4x64_20260514.metadata.json`
- 规模：`4 x 64` bytes
- 输出大小：`256` bytes
- SHA256：`64C9A4405903F888115729018B532EE7B837E0F7AC72F73DB0FC89BFE070F340`
- 方法：`RestartMethod=auto_stream_once`

这次 smoke 的关键意义：

1. 真实证明了“单次下载 bitstream -> 板上自动循环 restart -> UART 连续输出 row-major 数据”是可行的。
2. 证明当前 `fpga1` 环境下，不依赖 `UART_RX_i` 也能完成 design-level restart 快路径。
3. 证明问题主矛盾已经从“有没有快路径”转移到“是否直接放大到 1000 x 1000 formal run”。

基本数据形态检查显示：

- 4 行数据互不相同；
- 每行字节取值多样，不是全零或重复缓存包；
- 每行的 bit-1 比例约在 `0.369` 到 `0.436` 之间；
- 因此它更像真实 restart rows，而不是串口残留或固定模板。

这仍然只是 smoke，不是正式 `ea_restart` 结果。

## Formal-size 现状

本轮已经继续推进到 formal-size 尝试，并得到一个很重要的阶段性结论：

- `1000 x 1000` auto-stream bitstream 已成功编译
- 已分别对两个 formal-size bitstream 做了真实硬件采集尝试
- 但两次尝试都在 `0 byte` 阶段超时，没有收到首批 UART 数据

涉及文件：

- `data\vivado_runs\restart_auto_random3_formal_1000x1000\RO_TRNG_restart_auto_top.bit`
- `data\vivado_runs\restart_auto_random3_formal_1000x1000_syncreset\RO_TRNG_restart_auto_top.bit`

失败痕迹：

- `data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_formal_1000x1000_20260514.bin.tmp`
- `data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_formal_1000x1000_syncreset_20260514.bin.tmp`

二者大小都为 `0`，这说明问题不是“长流过程中断”，而是**formal-size 参数版本没有开始输出第一批字节**。

## 本轮诊断动作

为缩小问题范围，本轮已经做过一次 RTL 修正：

- 将 `RO_TRNG_restart_auto_top.v` 中基于 `rst_n_200m` 的主状态机从“异步复位写法”改为“同步复位写法”

这个修正有效降低了 formal build 中的部分 `REQP-1840 RAMB async control` 警告数量，但**没有让 `1000 x 1000` 板级采集直接恢复输出**。

因此当前更稳妥的判断是：

- 小规模参数下，auto-stream 路径已经真实可用；
- 大规模参数下，当前 restart-only 顶层还存在启动/排空/写读配合方面的问题；
- 需要做参数分界实验，而不是继续盲目重跑完整 `1000 x 1000`。

## 已知边界

1. 这个 auto-stream 顶层是 restart 专用实验 bitstream，不是原始 baseline bitstream。
2. 它共享原始 `entropy_source` 与 `fifo_generator_0 -> uart_tx` 数据通路，但顶层控制语义已经改变。
3. 论文中应把它写成：
   - “用于快速采集 restart matrix 的专用 design-level restart variant”
   - 而不是“与原始 baseline bitstream 完全等价”
4. 它比 `UART_RX` 命令触发方案更现实，因为 `fpga1` 仓库内没有明确的 `UART_RX_i` XDC。

## 下一步

P0：

- 把当前 `4 x 64` smoke 作为方法学证据写入 restart 状态文档和论文实验记录。

P1：

- 做参数分界实验，优先测试：
  - `4 x 1000`
  - `10 x 1000`
  - `100 x 1000`

  目的是确认问题到底由：

  - `ROW_BYTES=1000`
  - `RESTART_COUNT=1000`
  - 还是两者叠加

  中的哪一个触发。

P1：

- 如果 `4 x 1000` 或 `10 x 1000` 能通，则继续扩大；
- 如果 `4 x 1000` 也不通，则应优先检查顶层状态机/FIFO 交互，而不是继续堆硬件时间。

P1：

- 正式采集后，把输出送入：
  - `scripts/convert_restart_bytes_to_bits.py`
  - `scripts/run_90b_restart.ps1`

## 已验证可行的板级 smoke 命令

本次已成功执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\capture_90b_restart_dataset.ps1 `
  -Bitstream "data\vivado_runs\restart_auto_random3_smoke\RO_TRNG_restart_auto_top.bit" `
  -OutFile "data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_smoke_4x64_20260514.bin" `
  -Port COM3 `
  -Baud 115200 `
  -RestartCount 4 `
  -SymbolsPerRestart 64 `
  -RestartMethod auto_stream_once `
  -Run random3_restart_auto_smoke_4x64_20260514 `
  -MetadataFile "data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_smoke_4x64_20260514.metadata.json"
```

这条命令的目的只是验证整条快路径，不是正式 `ea_restart`。

## 2026-05-15 参数分界与调试头结果

本轮新增了两个对 formal-size 失败定位非常关键的 RTL/脚本机制：

- `RO_TRNG_restart_auto_top.v` 增加 `START_DELAY_CYCLES`，用于在下载 bitstream 后延迟启动 UART 输出，避免 FPGA 在 Vivado 退出和 PC 脚本尚未进入读循环时已经吐出大量数据。
- `RO_TRNG_restart_auto_top.v` 增加 `DEBUG_HEADER`，上电启动后先输出 8 字节头：
  - `A5 5A`
  - `RESTART_COUNT[15:0]`
  - `ROW_BYTES[15:0]`
  - version `01`
  - tag `D0`
- `capture_90b_restart_dataset.ps1` 增加 `-HeaderBytes` 和更大的串口读缓冲设置，并把 header 内容写入 metadata。

这一步的目的不是提高随机性，而是把 `0 byte` 超时分成两类：

- 如果 header 都没有，优先查 bitstream 下载、顶层复位、UART/FSM 启动；
- 如果 header 有但数据没有，优先查 restart/row/FIFO/采样路径；
- 如果 header 和完整数据都有，说明前一轮 formal-size `0 byte` 更可能是 PC 端读取时机或串口缓冲边界问题。

已完成两个真实硬件边界实验：

| 实验 | 文件 | 结果 | 结论 |
| --- | --- | --- | --- |
| `4 x 1000` | `data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_boundary_4x1000_header_20260515.bin` | 成功采集 `4000` bytes，header=`A55A000403E801D0`，SHA256=`5610489EE06496789587956091103EC6DAB39DDB43A30F705EC9DEDF79D51F93` | `ROW_BYTES=1000` 单独不会导致无输出 |
| `1000 x 64` | `data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_boundary_1000x64_header_20260515.bin` | 成功采集 `64000` bytes，header=`A55A03E8004001D0`，SHA256=`671EFEEB6B81240D0F76070360FFB300C0328638B586367C45F421C9C53761C8` | `RESTART_COUNT=1000` 单独不会导致无输出 |

因此，当前判断已经从“可能是 `ROW_BYTES` 或 `RESTART_COUNT` 位宽边界 bug”更新为：

1. `ROW_BYTES=1000` 单独通过；
2. `RESTART_COUNT=1000` 单独通过；
3. 早先 `1000 x 1000` 两版 `0 byte` 更可能与启动时机/串口缓冲、总长度长流、或二者叠加有关；
4. 下一步应直接构建并采集 `1000 x 1000` 的 `DEBUG_HEADER=1` + `START_DELAY_CYCLES=2000000000` 版本。

若该版本成功，将得到正式 `1000 x 1000` restart matrix，可继续进入 `convert_restart_bytes_to_bits.py` 与 `ea_restart`。若仍失败，再补 `1000 x 128` 与 LED/FSM 状态指示版本。

## 2026-05-15 formal-size 长流打通

第一次 `START_DELAY_CYCLES=2000000000` 版本仍然读到错误 header：

- 期望：`A55A03E803E801D0`
- 实际：`190BB210C20BEF99`

这说明问题已经不是“无输出”，而是 PC 侧读到了数据流中的错误位置。根因判断为：Vivado 下载/退出耗时可能超过 10 秒启动延迟，导致 debug header 在采集脚本真正等待 header 前已经经过串口缓冲边界。为此做了两个修正：

- `capture_90b_restart_dataset.ps1` 在 `auto_stream_once` 编程完成后再次 `DiscardInBuffer()`；
- `capture_90b_restart_dataset.ps1` 对 8 字节 debug header 强制校验 magic、`RESTART_COUNT` 和 `ROW_BYTES`；
- `RO_TRNG_restart_auto_top.v` 将 `START_DELAY_CYCLES` 和 `state_count` 扩展为 64 位，以支持超过 32 位的启动延迟。

随后构建并采集了 60 秒启动延迟版本：

- bitstream：`data\vivado_runs\restart_auto_random3_formal_1000x1000_header_delay60s\RO_TRNG_restart_auto_top.bit`
- 参数：`RESTART_COUNT=1000`，`ROW_BYTES=1000`，`START_DELAY_CYCLES=12000000000`，`DEBUG_HEADER=1`
- 输出：`data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_formal_1000x1000_header_delay60s_20260515.bin`
- header：`A55A03E803E801D0`
- 大小：`1000000` bytes
- SHA256：`7789491D1DFE5E3C21225F6574D3C00D85800258B4CE930C89545CD3BA59E3D6`

结论：

1. restart auto-stream 架构可以在真实 FPGA 上完成 `1000 x 1000` 长流采集；
2. 早先 `0 byte`/错误 header 的主因是启动时机与串口缓冲边界，而不是 `ROW_BYTES=1000` 或 `RESTART_COUNT=1000` 的 RTL 计数器硬伤；
3. 当前 `1000 x 1000` 文件是 byte-symbol 矩阵，适合证明长流链路和 byte-symbol restart 采集能力；
4. 若论文主线采用 bit-symbol SP800-90B restart，则还需要采 `1000 x 125` 原始 bytes，再展开为 `1000 x 1000` bit symbols 后运行 `ea_restart`。
