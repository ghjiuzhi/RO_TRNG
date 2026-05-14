# SP800-90B Restart Script Plan 2026-05-14

## Executive Summary

- 现有连续 `.bin` 不能作为 SP800-90B restart dataset；restart 需要 1000 次独立重启 x 每次 1000 个 symbol 的二维矩阵。
- 建议新增独立采集脚本 `scripts/capture_90b_restart_dataset.ps1`，不要复用普通连续采集脚本直接拼文件。
- 第一版 restart 采集优先支持“每次重新 program bitstream”的强 restart 方式，虽然慢，但语义最清楚，最适合论文审稿。
- 文件格式固定为 raw binary、row-major、一字节一个 symbol，大小必须精确等于 `RestartCount * SymbolsPerRestart`。
- 每一行采集失败时必须重采该行，不能补零、不能跳过、不能把 partial 行写入正式 dataset。
- `ea_restart.exe` 已能编译；正式运行命令形态是 `ea_restart.exe -n <restart.bin> <bits_per_symbol> <H_I>`，其中 `<H_I>` 应来自对应 sequential dataset 的 non-IID 估计。
- conditioning 目前不应作为论文主张，除非 RTL 明确定义 conditioning function，并补齐 MPFR/GMP 后构建 `ea_conditioning.exe`。

## Inputs Read

- `doc/fast_mode_master_status_20260514.md`
- `doc/sp800_90b_blocker_20260514.md`
- `doc/sp800_90b_integration_plan_20260514.md`
- `doc/sp800_90b_restart_protocol_20260514.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`
- `scripts/capture_uart.ps1`
- `scripts/program_and_capture_uart.ps1`
- `scripts/run_fast_hardware_queue.ps1`
- `scripts/build_90b_mingw.ps1`

## Findings

当前项目已经完成 sequential non-IID smoke、核心 8M non-IID、repeat smoke 和 IID diagnostic，但还没有 restart dataset。这个缺口不能靠已有 `random1_run01.bin`、`random3_run01.bin`、`random*_repeat03.bin` 弥补，因为它们都是连续运行流。

restart dataset 的关键不是“总样本数够 1,000,000”，而是样本组织方式：第 `r` 行必须来自第 `r` 次独立 restart 后的前 `c` 个 symbol。这样 `ea_restart` 才能检查同一列，即“每次重启后的第 j 个输出”是否有启动相关偏置。

当前最稳妥的 restart 定义是每行重新配置 FPGA bitstream：

1. 使用同一个 TRNG bitstream。
2. Program FPGA。
3. 等待固定 settle time。
4. 清空串口缓冲。
5. 采集固定数量 symbol。
6. 将该行写入临时 row 文件。
7. 行长度校验通过后 append 到正式矩阵。

这种方式慢，但审稿解释最干净。后续可增加 board reset 或 design reset 模式，但必须证明 reset 覆盖 RO、采样 FSM、FIFO 和 UART 输出状态。

## Recommended Actions

P0：新增脚本 `scripts/capture_90b_restart_dataset.ps1`。

建议参数：

```powershell
param(
  [string]$Bitstream,
  [string]$Port = "COM3",
  [int]$Baud = 115200,
  [string]$OutFile,
  [string]$MetadataFile = "",
  [int]$RestartCount = 1000,
  [int]$SymbolsPerRestart = 1000,
  [int]$BitsPerSymbol = 8,
  [int]$SettleMs = 500,
  [int]$WarmupSymbols = 0,
  [string]$RestartMethod = "program_bitstream",
  [string]$HwServerUrl = "localhost:3122",
  [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
  [string]$Python = "python"
)
```

P0：脚本必须保证正式输出文件原子化。建议先写 `OutFile.tmp`，全部行采完、大小校验和 SHA256 完成后再 rename 为正式 `.bin`。

P0：每一行 restart 建议先写到内存或临时 row 文件。只有长度恰好等于 `SymbolsPerRestart + WarmupSymbols` 时才取有效 symbol 并 append。若超时或长度不足，重试该行，最多 `MaxRetriesPerRestart` 次。

P0：metadata 必须记录：

- bitstream path 和 SHA256
- output SHA256
- restart count
- symbols per restart
- bits per symbol
- restart method
- settle time
- warmup discarded symbols
- UART port/baud/format
- start/end time
- failed/retried row count
- capture script SHA256
- `ea_restart` command line

P1：新增 `scripts/run_90b_restart.ps1`，读取 metadata 中的 `<H_I>` 或由参数传入，保存 stdout/stderr：

```powershell
.\sim\SP800-90B_EntropyAssessment\cpp\ea_restart.exe `
  -n data\sp800_90b\restart\random3_restart_1000x1000_bps1.bin `
  1 `
  0.856158 `
  *> data\sp800_90b\restart\random3_restart_1000x1000_bps1_ea_restart.log
```

P1：先做 smoke：

- `10 x 1000`：验证流程和文件格式，不用于论文。
- `100 x 1000`：验证稳定性和脚本可靠性，不作为正式 SP800-90B 结果。
- `1000 x 1000`：正式数据。

P2：conditioning 仅在 RTL 或系统设计确实有后处理/调理函数时才做。当前 raw RO-TRNG 输出不应强行声明 conditioning。

## Proposed Script Flow

```text
resolve repo root
resolve bitstream path
compute bitstream SHA256
open/create temporary output file
for restart_index in 0..RestartCount-1:
    if RestartMethod == program_bitstream:
        call Vivado program_bitstream.tcl
    wait SettleMs
    open serial COM3
    discard host serial input buffer
    read WarmupSymbols + SymbolsPerRestart bytes with timeout
    close serial
    if row length invalid:
        retry row
    else:
        append valid SymbolsPerRestart bytes to output temp file
        record row timing and retry count
verify temp file size == RestartCount * SymbolsPerRestart
compute SHA256
rename temp to final OutFile
write metadata JSON
```

## File Format

正式文件：

```text
raw binary
no header
no separator
uint8 per symbol
row-major
size = RestartCount * SymbolsPerRestart bytes
```

偏移公式：

```text
offset = restart_index * SymbolsPerRestart + symbol_index
```

若使用 bit-symbol 模式，应另建 prepared file，将每个 bit 展开成一字节 `0x00/0x01`，并在 metadata 中记录 bit order。不要把 packed byte 和 bit-symbol 文件混在同一个 dataset 名称下。

## Conditioning Dependency Plan

当前 MinGW route 已能构建：

- `ea_non_iid.exe`
- `ea_iid.exe`
- `ea_restart.exe`

尚不能构建：

- `ea_conditioning.exe`

原因：当前 `D:\Toolsapp\MinGW` 缺少 MPFR/GMP 头文件和库，例如 `mpfr.h`。

若后续必须做 conditioning，推荐两条路：

1. 使用 MSYS2 MinGW64：

```bash
pacman -S --needed mingw-w64-x86_64-gcc mingw-w64-x86_64-mpfr mingw-w64-x86_64-gmp mingw-w64-x86_64-bzip2
```

2. 使用 WSL/Linux：

```bash
sudo apt-get install build-essential libmpfr-dev libgmp-dev libbz2-dev
```

论文中只有在明确说明 conditioning function 的输入宽度、输出宽度、函数类型、是否 vetted/non-vetted 后，才运行 `ea_conditioning`。否则应写“本工作评估 raw entropy source output，不声明 conditioning gain”。

## Snippets For Paper

中文：

```text
为避免将连续运行序列误用为 restart 数据，本文将 restart dataset 单独采集为二维矩阵。每一行对应一次独立 FPGA 重新配置后的输出序列，每行记录前 1000 个原始 symbol，最终形成 1000 x 1000 的 row-major raw binary 文件，并使用 EntropyAssessment 的 ea_restart 工具进行验证。
```

英文：

```text
The restart dataset was collected independently from the sequential datasets. Each row corresponds to one independent FPGA reconfiguration, followed by a fixed settling interval and the acquisition of the first 1000 raw output symbols. The resulting 1000 x 1000 row-major binary matrix was evaluated using the NIST SP 800-90B EntropyAssessment ea_restart tool.
```

限制说明：

```text
The restart result is reported as a complement to the non-IID sequential entropy estimate. It should not be interpreted as a complete SP 800-90B certification in the absence of a full health-test and conditioning assessment.
```

## Open Questions

- restart 应该选 `random3` 一个好例，还是同时测 `random1` 坏例和 `random3` 好例？建议正式论文至少测 `random3`，若时间允许加 `random1` 作反例。
- restart 时是否丢弃 warm-up symbols？如果真实系统启动后不丢弃，则正式评估应先用 `WarmupSymbols=0`。
- 是否需要 RTL 支持更快的 design-level reset？如果没有，先用重新 program bitstream 的慢但清晰方案。
- 当前 UART 输出到底是 raw byte symbol 还是 packed bitstream？restart 文件的 `bits_per_symbol` 必须与论文定义一致。
- conditioning 是否真的存在？若只是 raw TRNG 输出，不应为追求 90B“更硬”而虚构 conditioning stage。

