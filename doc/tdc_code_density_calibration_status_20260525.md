# TDC Code-Density Calibration Status 2026-05-25

## 当前目标

补 TDC 机制线的关键短板：当前 clean reset-aligned TDC 已经能排除简单 pairwise hard locking，但没有独立 code-density calibration 前，不能把 raw bin 当作线性 ps 级时间。当前已经从 2 MiB smoke 推进到 8 MiB formal calibration 与 A/B lane-swap calibration，并用生成的 LUT 对 clean32k TDC 做了离线敏感性复算。

## 已新增文件

RTL:

```text
rtl/tdc/RO_TDC_code_density_cal_sysclk_top.v
```

构建脚本：

```text
scripts/build_tdc_code_density_calibration_20260525.ps1
data/experiments/xdc_tdc_code_density/tdc_code_density_no_extra.xdc
```

分析脚本：

```text
scripts/analyze_tdc_code_density_calibration_20260525.py
```

## Bitstream 构建结果

构建命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_code_density_calibration_20260525.ps1 -Mode smoke
```

输出 bitstream：

```text
data/vivado_runs/fpga1_tdc_code_density_cal/tdc_code_density_cal_a7_b11_smoke_20260525/RO_TDC_code_density_cal_sysclk_top.bit
```

bitstream SHA256：

```text
9AC5E580FD97425E75F6A0FF893CC8BDC45E5E6D91351D615A767A80FE0BD846
```

Vivado 结果：

- route 成功；
- bitgen 成功；
- DRC 仅有预期中的 RO combinational loop allowed warning 和 Zynq PS7 warning。

## 真实硬件采集结果

采集命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart.ps1 `
  -VivadoBat C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat `
  -Bitstream data\vivado_runs\fpga1_tdc_code_density_cal\tdc_code_density_cal_a7_b11_smoke_20260525\RO_TDC_code_density_cal_sysclk_top.bit `
  -Port COM3 `
  -Baud 115200 `
  -Kind tdc `
  -Run tdc_code_density_cal_a7_b11_smoke_2mib_20260525 `
  -Bytes 2MiB `
  -OutFile data\hardware\20260511_fpga1_board1\tdc\tdc_code_density_cal_a7_b11_smoke_2mib_20260525.bin `
  -MetadataDir data\hardware\20260511_fpga1_board1\metadata `
  -IdleTimeoutSec 120 `
  -BoardId z7020_b01
```

采集文件：

```text
data/hardware/20260511_fpga1_board1/tdc/tdc_code_density_cal_a7_b11_smoke_2mib_20260525.bin
```

采集结果：

| item | value |
| --- | --- |
| bytes | `2097152` |
| SHA256 | `DE4E52D858D814BEA2B88AA564B51D94A35323A8D6C7D5A38ADDD6C4E736264B` |
| duration | `182.376 s` |
| throughput | `11499.057 bytes/s` |
| XADC | not requested for this smoke |

## 分析结果

分析命令：

```powershell
python scripts\analyze_tdc_code_density_calibration_20260525.py `
  --input data\hardware\20260511_fpga1_board1\tdc\tdc_code_density_cal_a7_b11_smoke_2mib_20260525.bin `
  --label tdc_code_density_cal_a7_b11_smoke_2mib_20260525 `
  --out-dir data\experiments\tdc_code_density_cal_20260525 `
  --bitstream data\vivado_runs\fpga1_tdc_code_density_cal\tdc_code_density_cal_a7_b11_smoke_20260525\RO_TDC_code_density_cal_sysclk_top.bit `
  --board-id z7020_b01
```

输出：

```text
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_a7_b11_smoke_2mib_20260525.lane_a_lut.csv
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_a7_b11_smoke_2mib_20260525.lane_b_lut.csv
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_a7_b11_smoke_2mib_20260525.manifest.json
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_a7_b11_smoke_2mib_20260525.summary.md
```

核心指标：

| lane | decoded packets | seq gaps | used bins | dead bins | H(bin) | min-H(bin) | max DNL | min DNL | peak abs INL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 262143 | 0 | 64 | 1 | 2.994386 | 1.414885 | 23.377573 | -1.000000 | 23.377573 |
| B | 262143 | 0 | 64 | 1 | 2.450985 | 1.261638 | 26.109555 | -1.000000 | 26.109555 |

## 解释

这次 smoke 有三个价值：

1. 证明 dedicated code-density calibration 顶层、bitstream、UART 采集和 LUT 后处理链路可跑通。
2. `seq gaps=0`，说明 2 MiB TDC calibration stream 没有明显包序号断裂。
3. lane A/B bin 分布明显非均匀，证明“不能把 raw bin 当作线性 ps 时间”不是形式限制，而是实际存在的 TDC 非线性问题。

## 论文写法边界

当前可以写：

```text
A dedicated TDC code-density calibration smoke was implemented and validated on hardware. The 2 MiB calibration stream had 262143 decoded packets and zero sequence gaps, and it produced lane-wise bin-width lookup tables.
```

当前不能写：

```text
The TDC is fully calibrated for ps-level jitter measurement.
```

高水平投稿前建议补：

1. calibration-before / calibration-after 或 command-gated capture，避免 XADC/校准读数干扰 auto-stream header；
2. 多板重复 dedicated calibration，确认 LUT 非线性结构是否跨板稳定；
3. 用 fixed LUT 继续重新分析 pair-specific TDC；
4. 若要写绝对 ps 级 jitter，应补更严格的 calibration 设计说明和不确定度边界。

## Formal calibration 与 lane-swap 结果

在 smoke 跑通后，已完成两组 8 MiB formal calibration：

| run | bytes | packets | seq gaps | XADC after | capture SHA256 |
| --- | ---: | ---: | ---: | --- | --- |
| `tdc_code_density_cal_a7_b11_formal_8mib_20260525` | 8,388,608 | 1,048,575 | 0 | 46.9 C, VCCINT 1.000 V | `FF7A25B3CBE5289A8A480A8D117C81A9C462713EB6DB7CD86183B2540A553B32` |
| `tdc_code_density_cal_a11_b7_formal_8mib_20260525` | 8,388,608 | 1,048,575 | 0 | 47.2 C, VCCINT 1.000 V | `1F4B6EA436524ABC500B5DCAB979D149E601EF383B2784C982870F645C26F415` |

生成的总表：

```text
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_compare_20260525.csv
data/experiments/tdc_code_density_cal_20260525/tdc_code_density_cal_compare_20260525.md
```

核心指标：

| run | lane | used/dead bins | H(bin) | min-H(bin) | max DNL | peak abs INL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| a7/b11 formal | A | 64/1 | 3.00171 | 1.42201 | 23.2575 | 23.2575 |
| a7/b11 formal | B | 64/1 | 2.46040 | 1.26189 | 26.1048 | 26.1048 |
| a11/b7 formal | A | 63/2 | 2.39701 | 1.24577 | 26.4094 | 26.4094 |
| a11/b7 formal | B | 64/1 | 3.11855 | 1.46653 | 22.5204 | 22.5204 |

解释：

1. 两组 8 MiB calibration 都是 `seq gaps=0`，说明 UART/TDC calibration stream 在正式规模下稳定。
2. lane-swap 后高熵 lane 发生反转：`a7/b11` 中 lane A 更高，`a11/b7` 中 lane B 更高。这说明观测到的非线性不是 PC 端解析假象，而与被驱动的 lane/RO 物理实现有关。
3. 所有 formal calibration 仍存在 dead codes 和较大 DNL/INL，因此 raw bin 不能直接当成线性时间；论文里可以更有底气地限制 TDC 结论边界。

## LUT-based clean32k 复算

已新增离线脚本：

```text
scripts/analyze_tdc_clean32k_with_lut_20260525.py
```

输出：

```text
data/experiments/tdc_clean32k_lut_reanalysis_20260525/a7_b11/
data/experiments/tdc_clean32k_lut_reanalysis_20260525/a11_b7/
```

两套 LUT 复算后，clean32k TDC 的校准相位差自相关仍接近 0，A/B Pearson 也接近 0：

| LUT | autocorr range | A/B Pearson range | raw same-ratio range | longest raw diff run |
| --- | ---: | ---: | ---: | ---: |
| a7/b11 | -0.00753 to 0.00123 | -0.00936 to -0.00362 | 0.01651 to 0.02057 | 3 |
| a11/b7 | -0.00790 to 0.00250 | -0.00983 to -0.00347 | 0.01651 to 0.02057 | 3 |

这说明：虽然不同 LUT 会改变绝对 `diff_std_ps` 数值，但不会推翻 clean32k TDC 对“无简单 pairwise hard locking”的负证据结论。当前仍不应写“已完成严格 ps 级 metrology”，但可以写“dedicated code-density calibration and LUT-based sensitivity reanalysis do not overturn the hard-lock exclusion conclusion.”
