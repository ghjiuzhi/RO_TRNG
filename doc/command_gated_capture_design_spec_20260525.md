# Command-Gated Capture 设计规格 2026-05-25

## 为什么需要 command-gated

当前 restart/TDC 多数设计采用 auto-stream：bitstream 下载完成后，FPGA 等待固定 `START_DELAY_CYCLES`，然后自动输出 header 和数据。这已经能完成真实硬件采集，但有一个工程弱点：

```text
program bitstream -> read XADC before_capture -> open COM3
```

如果 XADC 读取或 Vivado/JTAG 操作耗时超过 start delay，PC 端会错过 UART header 或前段数据，导致 partial capture、错位、idle timeout。这个问题已经在 sample RO locked passband 实验里观察到。

command-gated 的目标是让 FPGA 下载后先等待 PC 命令，PC 准备好串口后再开始 stream。

## 推荐协议

最小协议：

```text
PC -> FPGA: A5 C3
FPGA -> PC: design-specific header
FPGA -> PC: payload stream
```

可扩展协议：

```text
PC -> FPGA:
  A5 C3
  command_id
  run_options

FPGA -> PC:
  magic
  design_id
  restart_count / packet_count
  row_bytes / warmup
  version
  payload
```

建议先做最小协议，不要一开始做复杂命令集。

## fpga1 当前限制

fpga1 当前已确认 UART TX 约束：

```text
fpga1/xc7z020clg400/lab_xdc/uart_selftest_pin.xdc
UART_TX_o -> J15
sys_clk   -> U18
```

当前没有可靠确认的 PL UART_RX pin。原始 `fpga/` 工程里曾有：

```text
UART_RX_i -> B9
UART_TX_o -> C9
```

但这属于原始板级工程，不应直接移植到 正点原子领航者 v2 / fpga1 复现工程。实施 command-gated 前必须先确认 fpga1 的 PL UART_RX 引脚。

## 分阶段实现

### Stage 1：UART RX pin smoke

目的：确认 PC 可以通过 COM3 向 FPGA 发送字节。

最小 RTL：

```text
UART RX 收到一个字节
UART TX 回显该字节，或回显 byte ^ FF
```

通过条件：

```text
PC 发送 A5
PC 收到 A5 或 5A
```

如果这一步失败，不继续改 restart/TDC。

### Stage 2：command-gated restart 4x64 smoke

目的：验证 command gate 不破坏已打通的 restart auto-stream 逻辑。

参数：

```text
RESTART_COUNT = 4
ROW_BYTES = 64
warmup = 0 或已知可跑配置
```

通过条件：

```text
下载 bitstream 后，FPGA 不主动输出
PC 打开 COM3
PC 发送 A5 C3
FPGA 输出 header + 256 bytes payload
SHA256/metadata 正常
```

### Stage 3：command-gated formal restart

目的：替代长 `START_DELAY_CYCLES`，让 1000x125 / 1000x1000 restart 采集可严格配合 XADC before/after。

推荐采集流程：

```text
program bitstream
read XADC before
open COM3
send A5 C3
capture payload
read XADC after
analyze restart
```

### Stage 4：command-gated reset-aligned TDC

目的：让 clean TDCR header 一定出现在文件开头，并降低大 delay 依赖。

通过条件：

```text
下载 bitstream 后无输出
发送 A5 C3 后，文件从 TDCR header 开始
文件大小 = 16 + packet_count * 8
```

## RTL 实现边界

推荐新增 sibling top，不改已经可复现实验的原 top：

```text
rtl/restart/RO_TRNG_restart_auto_cmd_top.v
rtl/tdc/RO_TDC_reset_aligned_cmd_top.v
```

内部复用：

```text
rtl/uart_rx.v
已有 UART TX / packetizer
已有 restart/TDC stream FSM
```

关键原则：

1. 不改变 sample RO / data RO / TDC lane 的 placement-critical 逻辑。
2. 只在 stream FSM 前面加 `WAIT_CMD` 状态。
3. 收到命令后再释放原本的 start pulse。
4. Header 增加 `cmd_gated=1` 或 version 字段，避免和 auto-stream 混淆。

## 脚本修改建议

新增或扩展：

```text
scripts/program_and_capture_uart_preopen.ps1
scripts/capture_uart.ps1
```

新增参数：

```powershell
-SendStartCommand
-StartCommandHex A5C3
-ExpectHeader TDCR
```

默认不要影响现有 auto-stream 队列。只有命令触发 bitstream 才加 `-SendStartCommand`。

## 论文收益

command-gated 本身不是论文创新点，但能提升实验严谨性：

1. before/after XADC 不再干扰 UART header；
2. reset/restart alignment 更容易证明；
3. 重做实验更稳定；
4. 审稿人质疑采集时序时，有明确工程回应。

