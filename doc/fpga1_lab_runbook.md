# FPGA1 Lab Runbook: 正点原子领航者 V2

This directory treats `fpga1/xc7z020clg400` as the board-adapted project for the
Zynq-7020 正点原子领航者 V2 board. The original `rtl` and `fpga` project remain the
upstream/reference design.

## Board Assumptions

- FPGA part: `xc7z020clg400-2`
- Clock input: single-ended `sys_clk` on package pin `U18`
- Reset: `por_n_i` on `N16`
- UART TX: `J15`
- Clock wizard in `fpga1` is single-ended `clk_in1 -> clk_out1 = 200 MHz`.

## Existing Baseline

The existing `fpga1` bitstream is the manually reproduced TRNG:

```text
fpga1/xc7z020clg400/xc7z020clg400.runs/impl_1/RO_TRNG_top.bit
```

Do not overwrite it when running exploratory experiments.

## TDC Diagnostic Build

The TDC build is intentionally copied into `data/vivado_runs` so the original
project is not mutated.

Run from PowerShell:

```powershell
& 'C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat' -mode batch -source .\scripts\vivado\run_fpga1_tdc_sysclk.tcl
```

Expected outputs:

```text
data/vivado_runs/fpga1_tdc_sysclk/RO_TDC_sysclk_top.bit
data/vivado_runs/fpga1_tdc_sysclk/reports/
```

## UART Packet Format

The diagnostic top emits 8-byte frames:

```text
0xA5 seq_lo seq_hi coarse_lo coarse_hi bin_a bin_b flags
```

`flags` bits:

```text
bit7: both lanes valid
bit6: lane B bubble seen
bit5: lane A bubble seen
bit4: lane B full
bit3: lane A full
bit2: lane B empty
bit1: lane A empty
bit0: reserved
```

Analyze a capture:

```powershell
python .\scripts\analyze_tdc_uart.py .\data\tdc_capture.bin
```

## Next Hardware Steps

1. Program the baseline TRNG bitstream and capture at least 1 Mbyte raw UART data.
2. Program the TDC diagnostic bitstream and capture at least 100k packets.
3. Repeat for multiple placement XDC files: compact, row, checker, far-apart.
4. Record board, temperature, voltage setting, bitstream name, Vivado seed, and capture command.
5. Run SP800-90B on raw TRNG captures and `analyze_tdc_uart.py` on TDC captures.
