# RO_TRNG 关键机制实验复现指南

这个文档是 2026-05-15 之后关键实验的复现入口。它的目的不是替代论文正文，而是回答一个很实际的问题：

```text
如果以后要重做某个实验，应该看哪些 RTL / XDC / 脚本 / 结果摘要？
```

## 1. 仓库与环境

真实工作目录：

```text
E:\Project\MLDSA\RO_TRNG
```

干净 GitHub 导出仓库：

```text
E:\Project\MLDSA\RO_TRNG_github_export
```

Vivado 路径：

```text
C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat
```

开发板串口：

```text
COM3, 115200 baud
```

注意：`E:\Project\MLDSA\RO_TRNG` 不是独立 Git 仓库，它的 Git 根目录是 `E:\Project\MLDSA`。不要在父仓库里直接 `git add .`。需要给 GitHub 或 GPT/Claude 分析时，应使用 `E:\Project\MLDSA\RO_TRNG_github_export`。

## 2. 当前论文主线

目前最有价值的论文主张是：

```text
RO-TRNG 的 placement 敏感性不能简单归因于 RO-RO 硬锁定。
TDC 结果弱化了强锁定解释；sampler-side ablation 和 sample-RO locked 实验证明，
采样端物理实现本身应被视为熵源边界的一部分。
```

也就是说，文章不应只写成“手动 placement 改善 TRNG”，而应写成：

```text
FPGA RO-TRNG 的 entropy-source boundary 包含 sample RO、采样寄存器、
局部路由和附近读出/控制逻辑。placement 会通过这些采样端物理因素改变
连续流随机性和 SP800-90B restart 行为。
```

## 3. 关键证据 1：Pair-TDC 排除简单强锁定解释

### 实验目的

验证坏 placement 是否可以简单解释成两个 RO 之间发生强相位锁定。

### 当前结论

已有 pair-specific TDC 结果中，相关系数接近 0，没有观察到保守意义上的强锁定窗口。因此论文里不能武断写成：

```text
bad placement = RO-RO hard locking
```

更合适的写法是：

```text
TDC evidence weakens the simple pairwise hard-locking explanation.
```

### 重要文件

```text
rtl/tdc/
scripts/analyze_tdc_pair_dynamics.py
scripts/analyze_tdc_startup_diffusion.py
doc/tdc_hypotheses_and_validation_20260523.md
doc/tdc_pair_dynamics_interpretation_20260514.md
data/experiments/tdc_pair_dynamics/
data/hardware/20260511_fpga1_board1/tdc_pairs/
```

### 常用离线刷新命令

```powershell
python scripts/analyze_tdc_pair_dynamics.py
```

## 4. 关键证据 2：Sampler-register-only ablation 修复连续流

### 实验目的

验证 random1 的坏结果是否和采样端物理实现有关。

### 当前结论

`random1_sampler_regs_only_x45y31` 连续流接近理想，说明仅改变 sampler-side 的一部分物理实现，就能把原本强偏置的 random1 连续流修好。

这说明采样端不是一个无关的 readout circuit，而是参与了熵源形成。

### 重要文件

```text
doc/random1_sampler_island_ablation_20260523.md
doc/sampler_regs_only_status_20260524.md
doc/sampler_regs_only_20mib_status_20260524.md
scripts/build_sampler_ablation_trng_20260524.ps1
scripts/update_sampler_ablation_summary_20260524.py
data/experiments/xdc_sampler_island/
data/experiments/sampler_regs_only_20260524/
data/hardware/20260511_fpga1_board1/trng/analysis_random1_sampler_regs_only_x45y31_20mib/
```

## 5. 关键证据 3：SP800-90B restart warmup pass/fail 窗口

### 实验目的

验证“连续流看起来好”是否足以说明 restart 安全。

### 当前结论

不够。`random1_sampler_regs_only_x45y31` 连续流很好，但 formal restart 测试存在明显 warmup 依赖：

```text
warmup 4 失败
warmup 5 通过
warmup 10 通过
warmup 11 失败
```

这说明 restart startup transient 或固定采样位置偏置仍然非常关键。

### 重要文件

```text
rtl/restart/RO_TRNG_restart_auto_top.v
scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl
scripts/capture_90b_restart_dataset.ps1
scripts/convert_restart_bytes_to_bits.py
scripts/summarize_restart_formal_windows_20260524.py
scripts/run_90b_restart.ps1
doc/regs_only_restart_breakthrough_20260524.md
doc/sp800_90b_restart_execution_status_20260514.md
data/experiments/restart_summary_20260524/
data/experiments/paper_artifacts_20260524/
```

## 6. 关键证据 4：FIFO / compact diagnostic 区分读出逻辑和采样物理

### 实验目的

formal auto restart 的失败可能来自很多因素：采样端、FIFO、UART、FSM、读出节奏、综合布局变化等。FIFO/compact diagnostic 的目的就是拆开这些因素。

### 当前结论

compact diagnostic 在 warmup4 下本身可以得到接近平衡的结果，说明失败不是简单由 UART、PC 采集、分析脚本或所有 readout/control 逻辑共同必然导致。

同时，formal auto 和 compact diagnostic 的 routed cell diff 显示：

```text
data RO 位置基本不变
sampled-data regs 位置基本不变
sample RO 有 LOC/BEL 变化
FIFO / UART / FSM 等读出控制逻辑大量变化
```

因此下一步合理怀疑点集中到 sample RO 及其局部物理实现。

### 重要文件

```text
rtl/restart/RO_TRNG_restart_fifo_diag_top.v
rtl/restart/RO_TRNG_restart_fifo_compact_diag_top.v
scripts/analyze_restart_fifo_diag.py
scripts/analyze_restart_fifo_compact_diag.py
scripts/summarize_restart_fifo_diag_matrix.py
scripts/compare_fifo_diag_to_formal_restart_20260524.py
scripts/postprocess_restart_fifo_diag_20260524.ps1
scripts/run_restart_fifo_diag_regs_only_queue_20260524.ps1
doc/restart_fifo_diag_queue_status_20260524.md
doc/restart_fifo_diag_mechanism_update_20260524.md
data/experiments/restart_fifo_diag_20260524/
```

### compact diagnostic 常用分析命令

```powershell
python scripts/analyze_restart_fifo_compact_diag.py --input <capture.bin> --out-dir data\experiments\restart_fifo_diag_20260524 --label <label>
python scripts/analyze_restart_matrix_columns.py --input data\experiments\restart_fifo_diag_20260524\<label>.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label <label> --out-dir data\experiments\restart_fifo_diag_20260524\<label>.column_analysis
```

## 7. 关键证据 5：sample-RO locked 因果实验

### 实验目的

这是目前最强的机制证据。问题是：

```text
如果 compact diagnostic 本来 warmup4 接近平衡，
但把 sample RO 锁回 formal auto 的物理位置，
坏结果会不会回来？
```

### 当前结论

会。

sample-RO locked compact diagnostic 在 warmup4 下重新出现强失败：

```text
restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc
p1 ~= 0.376796
worst byte 0 bit 5 p1 ~= 0.195
worst x ~= 805
```

这个结果非常关键，因为它说明：

```text
即使用 compact diagnostic 的读出/控制路径，只要把 sample RO 锁回 formal auto 的物理实现，
restart failure 就会被恢复。
```

因此可以写成：

```text
The physical implementation of the sample RO is a decisive component of the entropy-source boundary.
```

### 重要文件

```text
data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc
data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.md
data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.csv
doc/restart_fifo_diag_mechanism_update_20260524.md
doc/restart_fifo_diag_queue_status_20260524.md
```

## 8. 重跑硬件实验前的注意事项

不要同时运行多个会抢占以下资源的任务：

```text
COM3
JTAG
hw_server
Vivado hardware manager
```

重跑前先检查进程：

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'vivado|hw_server|powershell' }
```

如果要跑 capture，统一使用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart.ps1 `
  -VivadoBat 'C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat' `
  -Bitstream '<bitstream.bit>' `
  -Port COM3 `
  -Baud 115200 `
  -Bytes <byte_count> `
  -OutFile '<output.bin>' `
  -MetadataDir 'data\hardware\20260511_fpga1_board1\metadata' `
  -Kind restart `
  -Run '<run_id>' `
  -IdleTimeoutSec 90
```

如果 bitstream 有上电延迟，例如 restart auto-stream 的 60 秒 delay，`IdleTimeoutSec` 不能太短。

## 9. GitHub 导出与备份

刷新干净 GitHub 导出仓库：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\update_github_export_snapshot.ps1 -SnapshotTag 20260525 -MaxFileMiB 5
```

然后检查：

```powershell
cd E:\Project\MLDSA\RO_TRNG_github_export
git status --short
git diff --stat
```

当前策略：

```text
默认不 push。
只有你明确要求“推送 GitHub”时，才在 RO_TRNG_github_export 里 commit/push。
```

## 10. 后续最值得补的实验

如果继续冲高水平论文，优先级如下：

```text
1. sample-RO locked warmup4 repeat：确认最关键因果结果可重复。
2. sample-RO locked warmup5 / warmup11：判断 formal sample RO 是否只恢复 w4 fail，还是改变整个 warmup passband。
3. 多板重复：验证 sample-side boundary 不是单板偶然现象。
4. TDC calibration：如果要写绝对 ps 级 jitter/phase，需要 code-density calibration；否则只写 raw-bin 相对比较。
5. 官方 SP800-90B 报告整理：把 restart / non-IID 结果整理成正式附录或 artifact。
```
