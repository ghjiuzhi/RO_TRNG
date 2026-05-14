# FPGA1 RO-TRNG/TDC 手把手实验流程

日期：2026-05-10  
目标板：正点原子领航者 V2 / Zynq-7020  
工程目录：`E:\Project\MLDSA\RO_TRNG`  
Vivado：`C:\Programs\Xilinx2023\Vivado\2023.2`

这份文档的目标是告诉你：板子接上以后，从烧录 bit、采集 UART、记录实验元数据，到跑分析脚本、整理论文表格，应该一步一步怎么做。

## 0. 先明确你要得到什么

这篇论文现在的实验主线是：

1. 不同 RO 布局会改变频率、抖动、相位差、耦合/锁定行为。
2. TDC 用来观测这些物理量。
3. RO_TRNG 原始随机流用来做 bias、entropy、min-entropy、相关性分析。
4. 最后把 TDC 指标和随机性指标关联起来，说明“布局如何影响熵源质量”。

所以你不是只采一个 NIST 结果，而是要采两类数据：

- TDC 数据：看 RO 的相位、抖动、bin 分布、相关性。
- TRNG 原始数据：看 bias、min-entropy、byte entropy、自相关。

### 0.1 TDC 到底是什么

TDC 是 **Time-to-Digital Converter，时间数字转换器**。它的作用不是产生随机数，而是把一个很短的时间差转换成数字码。你可以把它理解成 FPGA 里的“时间尺子”。

在这个工程里，TDC 主要用来测 RO 边沿相对于系统时钟的位置。做法大概是：

1. RO 输出一个不断翻转的边沿。
2. 这个边沿进入 FPGA 内部的 carry chain 延迟链。
3. 系统时钟 `sys_clk` 在某一刻把整条延迟链的状态采下来。
4. 如果边沿已经传播到第 80 个 delay tap，但还没传播到第 81 个 tap，那么采样结果就会形成类似 thermometer code 的码型。
5. 编码器把这个码型转换成一个 bin 编号，比如 `80`。

这个 bin 编号代表“RO 边沿落在系统时钟周期内的哪个时间位置”。如果 RO 相位一直在漂移，bin 会在不同位置游走；如果 RO 被某种耦合拉住，bin 分布可能变窄、出现固定峰，或者两个 RO 的 bin 序列相关性增强。

所以 TDC 在论文里的定位是：

```text
TDC = 熵源物理行为观测仪器
RO_TRNG bitstream = 最终随机输出被测对象
```

TDC 不能替代随机性测试，但它能解释随机性为什么变好或变差。顶刊/高水平论文需要的不是“某个 bitstream 通过 NIST”，而是要回答：

```text
为什么这个布局更随机？
为什么另一个布局熵下降？
熵下降之前，物理层面有没有可观测征兆？
```

TDC 就是用来回答这些问题的。

### 0.2 为什么 TDC bin 不能直接当成线性时间

FPGA carry chain 的每个 delay tap 并不完全一样宽。也就是说，bin 0 到 bin 1 可能是 15 ps，bin 80 到 bin 81 可能是 25 ps。布局、布线、温度、电压也会让这些 bin 宽度变化。

所以不能简单说：

```text
bin 编号越大，时间就严格按固定 ps/bin 线性增加。
```

更严谨的做法是 **code-density calibration**：

1. 用大量异步 RO 边沿去打 TDC。
2. 统计每个 bin 被命中的次数。
3. 命中次数多的 bin 说明实际时间宽度更大。
4. 根据 bin 命中概率估计 bin width、DNL、INL。
5. 后续 jitter、phase spread、entropy 分析都基于校准后的理解来解释。

第一轮实验可以先看原始 bin 分布和相关性，但论文正式写法里要说明 TDC bin 存在非线性，并用 code-density calibration 做校准或至少做误差说明。

### 0.3 每个实验步骤的目的

| 步骤 | 做什么 | 目的 | 对应论文问题 |
| --- | --- | --- | --- |
| 0 | 明确实验主线 | 避免只做 NIST 测试，要把物理指标和随机性指标连起来 | 本文研究的不是单个 TRNG 是否通过测试，而是布局如何影响熵源 |
| 1 | 检查板卡、JTAG、UART、管脚 | 排除硬件连接、串口、时钟版本错误 | 保证实验对象确实是 `fpga1` 单端 `sys_clk` 版本 |
| 2 | 建立实验目录 | 保证原始数据、metadata、分析结果可追溯 | 审稿人或自己以后能复现实验 |
| 3 | 先烧 TDC bit | 先观测 RO 的物理相位/抖动/相关性 | 布局是否改变 RO 的底层行为 |
| 4 | 采集 TDC 数据 | 获得足够多的 TDC packet，避免小样本误判 | near/far 是否存在相位相关、bin 分布、jitter 差异 |
| 5 | 分析 TDC 数据 | 提取 bin entropy、DNL/INL、phase spread、correlation、jitter proxy | TDC 指标能否提前预测熵源质量 |
| 6 | 烧不同 RO_TRNG 布局并采原始流 | 测最终随机输出，而不是只看物理层 | compact/sparse/far 等布局是否导致 bias/min-entropy 变化 |
| 7 | 记录 metadata | 控制环境、bitstream、串口、时间、hash | 排除“数据来自不同条件”的质疑 |
| 8 | 分析 RO_TRNG 原始流 | 得到 bias、min-entropy、byte entropy、自相关等随机性指标 | 布局是否真的影响随机性质量 |
| 9 | 合并 TDC 与 TRNG 结果 | 把物理指标和随机性指标放到同一张表 | jitter/phase/correlation 与 min-entropy 是否相关 |
| 10 | 判断论文价值 | 验证或修正耦合/锁定假设 | 支持“布局感知熵源设计”的核心论点 |
| 11 | 第一天冒烟实验 | 先确认 bit、串口、脚本全链路通 | 避免采集大量无效数据 |
| 14 | 最小实验包 | 在时间紧张时保证有可写结果 | 形成初版论文实验章节 |
| 15 | 完整实验包 | 扩大布局、seed、重复次数、环境条件 | 支撑更高水平论文的统计说服力 |
| 16 | 温度实验，可选 | 看环境扰动下趋势是否稳定 | 证明或限制说明温度鲁棒性 |
| 17 | 电压记录/实验，可选 | 控制供电变量，避免误把电压漂移当成布局效应 | 说明实验在 nominal voltage 下完成 |

如果你暂时不测温度，不影响主线。写法要变成：

```text
本文在 nominal laboratory condition 下固定环境变量，重点研究 placement-induced entropy variation。
温度和电压不作为主动变量，只记录实验期间的室温、板卡预热时间和可获得的 XADC 读数。
```

这样不会把论文做散，主线会更清楚。

## 1. 插板前检查

本步骤目的：确认硬件连接、时钟版本和串口链路正确，避免后面采到的数据其实来自错误 bitstream、错误串口或错误板卡状态。

### 1.1 硬件连接

你需要连接：

- FPGA 板供电。
- USB-JTAG，用于 Vivado 烧 bit。
- USB-UART，用于采集 `UART_TX_o` 输出。

`fpga1` 当前约束里重要引脚是：

| 信号 | 管脚 | 用途 |
| --- | --- | --- |
| `sys_clk` | `U18` | 单端系统时钟 |
| `UART_TX_o` | `J15` | FPGA 发给电脑的 UART |
| `por_n_i` | `N16` | 复位 |

注意：这里用的是 `fpga1` 单端 `sys_clk` 版本，不是原始工程的差分时钟版本。

### 1.2 找到串口号

Windows 打开设备管理器，找到 USB 串口，比如：

```text
COM3
COM3
COM7
```

后面所有采集命令都要把 `COMx` 替换成你自己的串口。

默认 UART 参数：

```text
115200 baud
8 data bits
no parity
1 stop bit
no flow control
```

## 2. 建立本次实验目录

本步骤目的：把原始数据、metadata 和分析结果放在固定结构里，保证论文实验可追溯、可复查、可复现。

打开 PowerShell：

```powershell
cd E:\Project\MLDSA\RO_TRNG
```

建议每次上板实验建一个独立目录。比如今天：

```powershell
$DAY = "20260510_fpga1_board1"
New-Item -ItemType Directory -Force "data\hardware\$DAY"
New-Item -ItemType Directory -Force "data\hardware\$DAY\tdc"
New-Item -ItemType Directory -Force "data\hardware\$DAY\trng"
New-Item -ItemType Directory -Force "data\hardware\$DAY\metadata"
```

以后所有采集文件都放在：

```text
data\hardware\20260510_fpga1_board1\
```

不要把原始数据放在桌面、微信文件夹、临时目录里。论文实验必须能追溯。

## 3. 先烧 TDC bit

TDC 是第一优先级。它告诉你 RO 的物理行为是否真的随布局变化。

本步骤目的：先不用看最终随机数，而是先用 TDC 观察 RO 边沿相位、抖动和相关性，确认布局是否真的改变了熵源的物理行为。

### 3.0 这个 TDC bit 是怎么生成的

`data\vivado_runs\fpga1_tdc_sysclk_inmem\RO_TDC_sysclk_top.bit` 不是从一个固定 `.xpr` GUI 工程里点按钮生成的，而是用 Vivado **in-memory project** 脚本生成的。

生成脚本是：

```text
scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl
```

这个脚本会自动做这些事：

1. 创建临时内存工程：`create_project ... -in_memory`。
2. 读取 `fpga1` 里已经适配领航者 V2 的 RTL/IP。
3. 读取 `rtl\tdc\` 里的 TDC RTL。
4. 读取 `fpga1\xc7z020clg400\lab_xdc\tdc_sysclk_*.xdc` 约束。
5. 跑 `synth_design`、`opt_design`、`place_design`、`phys_opt_design`、`route_design`。
6. 输出 bit、DCP checkpoint 和 timing/utilization/DRC report。

所以它没有传统 GUI 工程文件，但不是不可复现的临时产物。它的工程信息保存在脚本、RTL、XDC、IP 和 `data\vivado_runs\fpga1_tdc_sysclk_inmem\reports\` 里。

重新生成默认 TDC bit：

```powershell
cd E:\Project\MLDSA\RO_TRNG
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  -mode batch `
  -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl
```

重新生成 near TDC bit：

```powershell
cd E:\Project\MLDSA\RO_TRNG
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  -mode batch `
  -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
  -tclargs data\experiments\xdc_tdc\tdc_ro_near_x36y35.xdc `
           data\vivado_runs\fpga1_tdc_matrix\tdc_ro_near_x36y35
```

重新生成 far TDC bit：

```powershell
cd E:\Project\MLDSA\RO_TRNG
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  -mode batch `
  -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
  -tclargs data\experiments\xdc_tdc\tdc_ro_far_x24y25.xdc `
           data\vivado_runs\fpga1_tdc_matrix\tdc_ro_far_x24y25
```

如果你想在 GUI 里看布局，可以用 Vivado 打开对应 routed checkpoint，而不是找 `.xpr`：

```powershell
& "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  data\vivado_runs\fpga1_tdc_sysclk_inmem\checkpoints\RO_TDC_sysclk_top_routed.dcp
```

### 3.1 先烧默认 TDC

bit 路径：

```text
data\vivado_runs\fpga1_tdc_sysclk_inmem\RO_TDC_sysclk_top.bit
```

Vivado GUI 操作：

1. 打开 Vivado 2023.2。
2. `Open Hardware Manager`。
3. `Open Target`。
4. `Auto Connect`。
5. 右键 FPGA device。
6. `Program Device`。
7. 选择上面的 `.bit`。
8. 点击 `Program`。

烧录完成后，板子会开始通过 UART 输出 TDC packet。

### 3.2 再烧 TDC near/far 对照

后面要验证“近距离 RO 是否更容易耦合”。所以还要烧两个 TDC 布局版本。

near：

```text
data\vivado_runs\fpga1_tdc_matrix\tdc_ro_near_x36y35\RO_TDC_sysclk_top.bit
```

far：

```text
data\vivado_runs\fpga1_tdc_matrix\tdc_ro_far_x24y25\RO_TDC_sysclk_top.bit
```

建议顺序：

1. 默认 TDC。
2. near TDC。
3. far TDC。
4. 再回到 near TDC 复测一次。

这样能看出环境漂移是否明显。

## 4. 采集 TDC 数据

本步骤目的：采集足够多的 TDC packet，让 bin 分布、phase spread、correlation、jitter proxy 这些指标具有统计意义。

### 4.1 推荐采集量

每个 TDC bit 至少采：

```text
200000 packets
```

当前 TDC packet 是 8 字节，所以至少采：

```text
200000 * 8 = 1600000 bytes
```

建议实际采 `2 MiB`，留一点余量：

```text
2097152 bytes
```

### 4.2 用串口工具采集

如果你用 Xcom、SSCOM33、MobaXterm、TeraTerm、PuTTY 都可以，但必须满足：

- 保存为二进制文件，不要保存成文本。
- 不要自动加时间戳。
- 不要把字节转成十六进制文本。

`.xdat`、`.dat` 扩展名本身不是问题。真正的问题是文件内容：

| 情况 | 能不能用 | 说明 |
| --- | --- | --- |
| 原始二进制字节，只是后缀叫 `.dat` 或 `.xdat` | 可以 | 可以直接分析，必要时改名为 `.bin` |
| 文本内容类似 `A5 01 00 FF` | 不建议 | 这是十六进制文本，不是原始 UART 字节 |
| 每行带时间戳、方向标记、换行 | 不可以 | 会污染随机流和 TDC packet |

为了避免串口助手保存格式不确定，推荐直接用我写好的自动采集脚本：

```text
scripts\capture_uart.ps1
```

UART 参数：

```text
115200 baud
8 data bits
no parity
1 stop bit
no flow control
```

`10 MiB` 的意思是：

```text
10 * 1024 * 1024 = 10485760 bytes
```

`2 MiB` 的意思是：

```text
2 * 1024 * 1024 = 2097152 bytes
```

注意：115200 baud 很慢。串口 1 个字节通常约 10 bit，包括 start/stop bit，所以：

```text
2 MiB  约 3.0 分钟
10 MiB 约 15.2 分钟
```

先设置当天目录：

```powershell
cd E:\Project\MLDSA\RO_TRNG
$DAY = "20260511_fpga1_board1"
New-Item -ItemType Directory -Force "data\hardware\$DAY\tdc"
New-Item -ItemType Directory -Force "data\hardware\$DAY\trng"
New-Item -ItemType Directory -Force "data\hardware\$DAY\metadata"
```

采 TDC，自动保存、算 SHA256、写 metadata、跑 TDC 分析：

```powershell
.\scripts\capture_uart.ps1 `
  -Port COM3 `
  -Baud 115200 `
  -Kind tdc `
  -Run tdc_near_run01 `
  -Bytes 2MiB `
  -OutFile "data\hardware\$DAY\tdc\tdc_near_run01.bin" `
  -Bitstream "data\vivado_runs\fpga1_tdc_matrix\tdc_ro_near_x36y35\RO_TDC_sysclk_top.bit" `
  -MetadataDir "data\hardware\$DAY\metadata" `
  -Analyze
```

采 TRNG，自动保存、算 SHA256、写 metadata、跑 TRNG 分析：

```powershell
.\scripts\capture_uart.ps1 `
  -Port COM3 `
  -Baud 115200 `
  -Kind trng `
  -Run compact_run01 `
  -Bytes 10MiB `
  -OutFile "data\hardware\$DAY\trng\compact_run01.bin" `
  -Bitstream "data\vivado_runs\fpga1_ro_trng_sweep\ro_compact_x44y43\seed_1\RO_TRNG_top.bit" `
  -MetadataDir "data\hardware\$DAY\metadata" `
  -Analyze
```

如果脚本 30 秒收不到任何字节，会报错并提示检查 COM 口、bitstream、UART 管脚、波特率和复位。

如果你想按必采列表批量采，可以用：

```text
scripts\fpga1_capture_required_bits.ps1
```

先做 TDC 冒烟，每个 TDC bit 采 1 次，每次 2 MiB，并自动分析：

```powershell
cd E:\Project\MLDSA\RO_TRNG
powershell -ExecutionPolicy Bypass -File scripts\fpga1_capture_required_bits.ps1 `
  -Port COM3 `
  -Day 20260511_fpga1_board1 `
  -Set tdc `
  -TdcRuns 1 `
  -TdcBytes 2MiB `
  -Analyze
```

这个模式下脚本会提示你烧哪个 bitstream。你在 Vivado GUI 里烧完后按回车，脚本就开始采集。

如果 USB-JTAG 连接稳定，也可以让脚本自动调用 Vivado 烧 bit：

```powershell
cd E:\Project\MLDSA\RO_TRNG
powershell -ExecutionPolicy Bypass -File scripts\fpga1_capture_required_bits.ps1 `
  -Port COM3 `
  -Day 20260511_fpga1_board1 `
  -Set tdc `
  -TdcRuns 1 `
  -TdcBytes 2MiB `
  -ProgramWithVivado `
  -Analyze
```

第一轮 TRNG 冒烟，每个布局先采 1 次，每次 1 MiB：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\fpga1_capture_required_bits.ps1 `
  -Port COM3 `
  -Day 20260511_fpga1_board1 `
  -Set trng `
  -TrngRuns 1 `
  -TrngBytes 1MiB `
  -Analyze
```

正式采集可以改成每布局 5 次、每次 10 MiB：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\fpga1_capture_required_bits.ps1 `
  -Port COM3 `
  -Day 20260511_fpga1_board1 `
  -Set trng `
  -TrngRuns 5 `
  -TrngBytes 10MiB `
  -Analyze
```

文件命名建议：

```text
data\hardware\20260510_fpga1_board1\tdc\tdc_near_run01.bin
data\hardware\20260510_fpga1_board1\tdc\tdc_near_run02.bin
data\hardware\20260510_fpga1_board1\tdc\tdc_far_run01.bin
data\hardware\20260510_fpga1_board1\tdc\tdc_far_run02.bin
```

### 4.3 采集后立刻算 SHA256

每采完一个文件，马上执行：

```powershell
Get-FileHash data\hardware\$DAY\tdc\tdc_near_run01.bin -Algorithm SHA256
```

把 hash 复制到 metadata 里。这样以后论文审稿时数据可追溯。

## 5. 分析 TDC 数据

本步骤目的：把 UART 原始 packet 转换成可写进论文的物理指标，包括 bin 分布、DNL/INL、相位扩散、抖动代理量和两个 RO 之间的相关性。

假设你采到了：

```text
data\hardware\20260510_fpga1_board1\tdc\tdc_near_run01.bin
```

运行：

```powershell
python scripts\analyze_tdc_uart.py `
  data\hardware\$DAY\tdc\tdc_near_run01.bin `
  --clock-period-ps 5000 `
  --bins 256 `
  --run tdc_near_run01 `
  --out-dir data\hardware\$DAY\tdc\analysis_tdc_near_run01
```

说明：

- `clock-period-ps 5000` 对应 200 MHz 采样时钟。
- 输出目录里会有 packet CSV、bin CSV、metrics CSV、summary Markdown。

你重点看这些指标：

| 指标 | 意义 |
| --- | --- |
| bin 分布 | TDC 输出是否集中、是否均匀 |
| DNL/INL | TDC bin 是否严重非线性 |
| lane A/B jitter | 两个 RO 各自抖动 |
| differential jitter | 两个 RO 相对相位抖动 |
| Pearson correlation | 两个 RO 是否相关增强 |
| flag ratio | empty/full/bubble 是否过多 |

如果 near 的 correlation 明显高于 far，或者 differential jitter 明显变小/变异常，就可能是耦合或锁定迹象。

## 6. 烧 RO_TRNG bit 并采原始随机流

TDC 采完后，开始烧 RO_TRNG 的布局矩阵。

本步骤目的：验证 TDC 看到的物理差异是否会传导到最终随机输出上，也就是布局变化是否真的改变 bias、min-entropy 和相关性。

### 6.1 必采 bitstream 列表

建议第一轮至少采这些：

这些 bit 的联系是：RTL 结构基本相同，板卡、UART、时钟和 TRNG 逻辑相同；主要区别是 RO 的 `LOC/BEL` placement 不同。这样才能把输出差异尽量归因到布局。

| ID | bitstream | 作用 |
| --- | --- | --- |
| compact | `data\vivado_runs\fpga1_ro_trng_sweep\ro_compact_x44y43\seed_1\RO_TRNG_top.bit` | 把 RO 放得很紧，最大化近距离耦合/锁定风险，是“坏情况”候选 |
| checker | `data\vivado_runs\fpga1_ro_trng_sweep\ro_checker_pitch3_x44y43\seed_1\RO_TRNG_top.bit` | 棋盘式间隔放置，既保持同一区域，又减少直接相邻影响 |
| same_column | `data\vivado_runs\fpga1_ro_trng_matrix\same_column_pitch3_x44y35\seed_1\RO_TRNG_top.bit` | 同一列纵向排布，用来测试列资源、局部电源/布线相关影响 |
| row | `data\vivado_runs\fpga1_ro_trng_matrix\row_pitch3_x38y43\seed_1\RO_TRNG_top.bit` | 同一行横向排布，用来和 same_column 对比方向性影响 |
| sparse | `data\vivado_runs\fpga1_ro_trng_matrix\sparse_pitch6_x36y35\seed_1\RO_TRNG_top.bit` | 同一区域内拉大间距，测试“距离变远后耦合是否减弱” |
| cross_region | `data\vivado_runs\fpga1_ro_trng_matrix\cross_region_x36y25\seed_1\RO_TRNG_top.bit` | 跨更大资源区域放置，测试区域差异、布线差异和局部环境差异 |
| far | `data\vivado_runs\fpga1_ro_trng_matrix\far_x20y25\seed_1\RO_TRNG_top.bit` | 尽量分散，是 compact 的主要对照组 |
| random1 | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit` | 随机 placement 基线 seed 1 |
| random2 | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed2_x36y35\seed_1\RO_TRNG_top.bit` | 随机 placement 基线 seed 2 |
| random3 | `data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit` | 随机 placement 基线 seed 3 |

最重要的对照关系：

| 对照 | 想回答的问题 |
| --- | --- |
| compact vs far | RO 放得近是否导致熵下降或相关性增强 |
| compact vs sparse | 同一区域内只改变距离，随机性是否改善 |
| same_column vs row | 布局方向是否影响 RO 行为 |
| checker vs compact | 保持局部区域类似，但减少直接相邻，是否能改善 |
| random1/random2/random3 vs 手工布局 | 手工 placement 是否真的优于/劣于随机 placement |
| TDC near vs TDC far | 物理层是否能观测到近距离耦合迹象 |

### 6.2 每个布局采几次

第一轮建议：

```text
每个布局采 5 次
每次至少 10 MiB
```

也就是每个布局：

```text
run01.bin
run02.bin
run03.bin
run04.bin
run05.bin
```

命名例子：

```text
data\hardware\$DAY\trng\compact_run01.bin
data\hardware\$DAY\trng\compact_run02.bin
data\hardware\$DAY\trng\checker_run01.bin
data\hardware\$DAY\trng\same_column_run01.bin
data\hardware\$DAY\trng\sparse_run01.bin
```

不要只采一次。只采一次没有统计说服力，也很难支撑高水平论文。

## 7. 每次采集都要记录 metadata

本步骤目的：记录 bitstream、采集时间、串口、hash、环境条件等上下文，防止后面无法证明某个数据文件到底是怎么来的。

每烧一个 bit、采一个文件，都建一个 JSON。比如：

```text
data\hardware\$DAY\metadata\compact_run01.json
```

模板：

```json
{
  "capture_id": "compact_run01",
  "board": "navigator_v2_zynq7020_board1",
  "bitstream": "data/vivado_runs/fpga1_ro_trng_sweep/ro_compact_x44y43/seed_1/RO_TRNG_top.bit",
  "uart_port": "COM3",
  "baud": 115200,
  "bytes_requested": 10485760,
  "bytes_captured": 10485760,
  "sha256": "填这里",
  "room_temperature_c": "填这里",
  "board_temperature_c": "如果能读就填",
  "core_voltage_v": "如果能测就填",
  "start_time": "2026-05-10 14:00:00",
  "end_time": "2026-05-10 14:15:00",
  "notes": "例如风扇开/关、板子是否预热"
}
```

高水平论文最怕实验不可复现。metadata 很烦，但必须做。

## 8. 分析 RO_TRNG 原始流

本步骤目的：从最终输出的随机 bitstream 中提取随机性指标，判断不同布局是否导致偏置、熵下降或相关性增强。

假设你采到了：

```text
data\hardware\$DAY\trng\compact_run01.bin
```

运行：

```powershell
python scripts\analyze_trng_dataset.py `
  data\hardware\$DAY\trng `
  --glob compact_run01.bin `
  --out-dir data\hardware\$DAY\trng\analysis_compact_run01
```

每个 run 都跑一遍。后面也可以按布局批量跑：

```powershell
python scripts\analyze_trng_dataset.py `
  data\hardware\$DAY\trng `
  --glob compact_run*.bin `
  --out-dir data\hardware\$DAY\trng\analysis_compact
```

重点看：

| 指标 | 意义 |
| --- | --- |
| `p1` | bit 1 比例，越接近 0.5 越好 |
| bit min-entropy | 单 bit 最小熵 |
| byte entropy | 字节熵 |
| byte min-entropy | 字节最小熵 |
| autocorrelation | 是否有周期相关 |
| run statistics | 是否存在明显长串偏差 |

如果 compact 明显比 sparse/far 差，说明近距离布局可能导致耦合或相位相关，从而降低随机性。

## 9. 合并 TDC 与 TRNG 结果

本步骤目的：把“物理层 TDC 指标”和“随机性统计指标”放到同一张表里，做相关性分析，形成论文的核心证据链。

等你有了：

- TDC metrics CSV
- TRNG summary CSV
- Vivado timing/utilization report

就运行：

```powershell
python scripts\merge_experiment_tables.py `
  --tdc data\hardware\$DAY\tdc\analysis_tdc_near_run01\tdc_near_run01.tdc_metrics.csv `
  --trng data\hardware\$DAY\trng\analysis_compact\trng_summary.csv `
  --vivado-runs data\vivado_runs\fpga1_ro_trng_matrix `
  --out-csv data\hardware\$DAY\paper_experiment_table.csv `
  --out-md data\hardware\$DAY\paper_experiment_table.md
```

第一轮表可能不完美，但先合出来。论文后面所有图表都从这些 CSV 出，不要手抄数据。

## 10. 怎么判断结果有没有论文价值

本步骤目的：不是为了强行证明原假设，而是根据数据判断布局影响到底来自耦合/锁定、路径延迟差异、局部资源差异，还是环境漂移。

你要找的不是“某个布局 NIST 过了”，而是这些现象：

### 10.1 支持耦合假设的现象

如果出现下面情况，就很有价值：

- near TDC 的 A/B correlation 明显高于 far。
- near 的 differential jitter 比 far 小很多，像被锁住。
- compact/same_column 的 TRNG bias 比 sparse/far 更严重。
- compact/same_column 的 min-entropy 低于 sparse/far。
- 某些布局 TDC phase 分布变窄或出现固定峰。

这些可以写成：

> RO 的物理邻近性增强了相位相关或耦合趋势，导致熵源有效随机扰动下降。

### 10.2 不支持耦合假设也有价值

如果结果是：

- near/far TDC 差异不明显；
- 但是不同布局频率差、jitter 差异明显；
- TRNG 熵仍随布局变化；

那也能写：

> 布局影响主要来自路径延迟/局部资源差异，而不是强耦合锁定。

这依然是论文结果。

## 11. 推荐第一天实验顺序

本步骤目的：先做最小闭环，确认烧录、UART 采集、二进制保存、脚本解析全都正常，再扩大采集规模。

第一天不要贪多。按这个顺序：

1. 烧 `tdc_ro_near_x36y35`，采 `tdc_near_run01.bin`。
2. 烧 `tdc_ro_far_x24y25`，采 `tdc_far_run01.bin`。
3. 跑 `analyze_tdc_uart.py`，确认 packet 能解码。
4. 烧 `compact`，采 `compact_run01.bin`，先采 1 MiB 冒烟。
5. 跑 `analyze_trng_dataset.py`，确认数据不是全 0、全 FF 或乱码。
6. 如果冒烟通过，再每个布局采 10 MiB。
7. 每个布局先采 1 次，确认流程通。
8. 流程通了以后，再补到每布局 5 次。

这样最稳，不会一上来采一晚上才发现串口参数错了。

## 12. 最容易出错的地方

### 12.1 串口保存成文本

错误：

```text
A5 01 00 ...
```

这是十六进制文本，不是原始字节。

正确：

```text
保存为 .bin 原始二进制
```

### 12.2 忘记记录 bitstream

如果你只写“采了 compact”，但没写具体 bit 路径和 SHA256，后面就很难复现。

### 12.3 只看 NIST

NIST 通过不等于论文有贡献。你必须同时看：

- TDC 物理指标；
- TRNG 熵指标；
- 布局差异；
- 统计相关性。

### 12.4 每种布局只采一次

一次采样不能说明稳定性。至少 5 次。

### 12.5 温度漂移不记录

RO 对温度敏感。如果你不记录温度，审稿人会质疑变化是不是温漂导致的。

## 13. 第一轮完成后你应该给我什么

第一轮上板后，把这些文件路径告诉我：

```text
data\hardware\$DAY\tdc\
data\hardware\$DAY\trng\
data\hardware\$DAY\metadata\
```

或者直接说：

```text
我已经采完 20260510_fpga1_board1，数据在 data\hardware\20260510_fpga1_board1
```

然后我可以继续帮你：

- 批量跑分析；
- 合并所有表；
- 找 near/far/compact/sparse 的差异；
- 判断是否有耦合/锁定迹象；
- 画论文图；
- 写实验结果章节。

## 14. 最小可发表实验包

本步骤目的：在时间有限时，保证至少有 near/far TDC 对照、compact/sparse/far TRNG 对照和重复采样，可以支撑初版实验章节。

如果时间很紧，至少完成：

| 类别 | 最低要求 |
| --- | --- |
| TDC | near 3 次、far 3 次 |
| TRNG | compact/checker/sparse/far 各 5 次 |
| 每次大小 | TRNG 每次 10 MiB，TDC 每次约 2 MiB |
| metadata | 每次都有 JSON |
| 分析 | TDC metrics + TRNG summary + 合表 |

这个是“能开始写论文实验结果”的最低线。

## 15. 冲高水平的完整实验包

本步骤目的：扩大布局矩阵、随机 seed、重复次数和环境控制，让结论从“个例现象”变成“统计稳定的规律”。

完整版本建议：

| 类别 | 完整要求 |
| --- | --- |
| TDC | default/near/far/vertical_far 各 5 次 |
| TRNG | 10 个布局全部采，每布局 5 次 |
| 温度 | 室温、升温、降温至少 3 个环境点 |
| 电压 | 默认电压，低/高电压如果条件允许 |
| 统计 | min-entropy、bias、autocorrelation、TDC jitter、phase correlation |
| 对照 | 原始 manual fpga1 bitstream 也采 |

完整包才比较像高水平论文的实验规模。

## 16. 温度怎么做

本步骤目的：温度不是主线时可以不主动扰动；如果要做，它用于检验布局结论是否在不同热条件下仍然稳定。

温度实验的原则是：先记录，再扰动；先小范围，再大范围。不要一开始就用很激进的方法。

### 16.1 最推荐的三个温度点

第一轮建议做三个温度条件：

| 条件 | 做法 | 目的 |
| --- | --- | --- |
| 室温稳定 | 板子裸放，运行 10 分钟后开始采 | baseline |
| 风扇降温 | 小风扇对着 FPGA/散热片吹 5 到 10 分钟 | 低温/散热增强对照 |
| 自热升温 | 关风扇，让 FPGA 连续跑 10 到 20 分钟后采 | 轻度高温对照 |

这三个点最安全，也最容易复现。

### 16.2 更强一点的升温方法

如果自热不够明显，可以用：

- 热风枪低档、远距离吹。
- 恒温热台。
- 小型恒温箱。
- 吹风机低温档、远距离吹。

但要注意：

- 不要直吹到烫手。
- 不要让热风吹到塑料接口、排线、杜邦线。
- 每升一点温度就停下来记录。
- 温度稳定 3 到 5 分钟后再采数据。
- 不要追求极限温度，论文要的是趋势，不是把板子烤坏。

建议温度点：

```text
室温：约 25 C
中温：约 40 C
较高温：约 55 C
```

这只是实验目标，不是硬性值。实际以板上读到的温度为准。

### 16.3 降温能不能用冰箱

不建议第一轮用冰箱。

原因是：

- 容易结露。
- 水汽会伤板。
- 从低温拿到室温时尤其容易凝水。

如果以后真的要做低温，需要：

- 干燥环境。
- 密封袋。
- 干燥剂。
- 回温后确认无冷凝水再上电。

第一篇论文实验不需要这么冒险。

### 16.4 温度怎么记录

优先记录三类温度：

1. 室温：普通温度计即可。
2. FPGA 片上温度：Vivado Hardware Manager / XADC / System Monitor。
3. 板面温度：红外测温枪或热电偶测 FPGA 封装/散热片附近。

metadata 里至少填：

```json
{
  "room_temperature_c": 25.3,
  "fpga_temperature_c": 39.8,
  "board_temperature_c": 37.5,
  "temperature_method": "Vivado XADC + infrared thermometer",
  "thermal_condition": "fan_off_self_heating_15min"
}
```

如果只能记录室温，也比完全不记录强。但最好用 Vivado 读片上温度。

## 17. 电压怎么做

本步骤目的：电压第一轮主要作为受控变量记录，避免把供电漂移误判成布局效应；不建议在没确认电源树前主动调压。

电压比温度危险得多。第一轮不要主动改电压，先只记录电压。

### 17.1 为什么不建议直接调电压

正点原子领航者 V2 这类开发板通常有板载稳压器。你给板子输入 5V，板上再生成：

- FPGA core voltage。
- auxiliary voltage。
- I/O bank voltage。
- DDR/PS 相关电压。

所以你调外部 5V 输入，并不等于调 FPGA 的 VCCINT。多数情况下稳压器会把内部电压维持不变；如果你调得太低，板子掉电不稳定；调得太高，可能烧板。

结论：

```text
不要通过乱调 5V 输入来做“电压实验”。
```

### 17.2 第一轮应该怎么做

第一轮只记录电压，不改电压：

- 记录板子输入电压，比如 USB/电源适配器电压。
- 用 Vivado XADC/System Monitor 记录片上电压，如 VCCINT、VCCAUX 等。
- 如果有万用表，测开发板测试点上的核心电压/辅助电压。

metadata 示例：

```json
{
  "voltage_condition": "nominal_board_power",
  "input_voltage_v": 5.08,
  "vccint_v": 1.00,
  "vccaux_v": 1.80,
  "voltage_method": "Vivado XADC + multimeter test point"
}
```

注意：上面的数值只是例子，实际以你的板子读数为准。

### 17.3 如果以后必须做电压扰动

只有在满足下面条件时才做：

- 你能确认板上哪个电源轨对应 FPGA VCCINT/VCCAUX。
- 你有原理图。
- 你知道稳压芯片能不能调。
- 你有可限流的实验电源。
- 你知道 FPGA datasheet 推荐电压范围。
- 你能实时监控电流和芯片温度。

可以选择的安全方案：

| 方案 | 推荐程度 | 说明 |
| --- | --- | --- |
| 只记录 XADC 电压 | 最推荐 | 零风险 |
| 使用开发板支持的软件/PMBus 调压 | 推荐，但看板子是否支持 | 最干净 |
| 改可调稳压器反馈电阻 | 不推荐第一轮 | 有硬件风险 |
| 外接核心电源轨 | 高风险 | 需要断开原板电源轨 |
| 调 5V 输入 | 不推荐 | 通常不能有效改变 VCCINT |

### 17.4 论文里电压实验可以先不做

如果条件不成熟，电压不要硬做。高水平论文不一定必须有电压扫描。

更稳的说法是：

> 本文主要控制并记录电源条件，在 nominal voltage 下研究布局和温度对 RO 熵源的影响。

也就是说，先把电压作为“受控变量”记录清楚，而不是把它作为“主动变量”乱调。

## 18. 推荐你的第一版环境实验

本步骤目的：如果你决定加入环境变量，就先选少量代表性布局做验证；如果暂时不测温度，这一节可以跳过，只记录 nominal condition。

第一版按这个做就够了：

| 环境 | 温度方法 | 电压方法 | 是否推荐 |
| --- | --- | --- | --- |
| E0 | 室温，板子预热 10 分钟 | nominal，只记录 | 必做 |
| E1 | 小风扇吹 FPGA 10 分钟 | nominal，只记录 | 必做 |
| E2 | 关风扇，自热 20 分钟 | nominal，只记录 | 必做 |
| E3 | 低档热风/恒温箱到约 40 C | nominal，只记录 | 可选 |

每个环境下不需要把全部 10 个布局都采满。第一轮可以先采：

- TDC near。
- TDC far。
- TRNG compact。
- TRNG sparse。
- TRNG far。

如果这几个已经显示明显趋势，再扩展到全部布局。
