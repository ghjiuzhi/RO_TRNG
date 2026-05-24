# New Conversation Bootstrap Prompt 20260523

Copy this prompt into a new conversation when handing off the project.

```text
你现在接手 `E:\Project\MLDSA\RO_TRNG` 这个 FPGA RO-TRNG 高水平论文项目。请先不要直接跑硬件实验，先读取并理解：

1. `E:\Project\MLDSA\RO_TRNG\doc\handoff_full_context_20260523.md`
2. `E:\Project\MLDSA\RO_TRNG\doc\fast_mode_status_20260523.md`
3. `E:\Project\MLDSA\RO_TRNG\doc\mechanism_hypothesis_goal_20260523.md`
4. `E:\Project\MLDSA\RO_TRNG\doc\random1_sampler_island_ablation_20260523.md`
5. `E:\Project\MLDSA\RO_TRNG\doc\tdc_sampler_mechanism_experiment_plan_20260523.md`
6. `E:\Project\MLDSA\RO_TRNG\data\experiments\tdc_sampler_data_20260523\tdc_sampler_data_summary.md`
7. `E:\Project\MLDSA\RO_TRNG\doc\restart_sampler_island_experiment_plan_20260523.md`
8. `E:\Project\MLDSA\RO_TRNG\doc\restart_sampler_island_capture_status_20260523.md`

项目目标：
我要发高水平论文。核心机制不是简单说 RO 之间 hard locking，而是证明/约束：RO-TRNG 的 entropy-source boundary 包含 sampler-side physical implementation。placement 通过 sample RO、sampling registers、routing、sampling aperture/metastability 影响随机性。TDC 目前主要是 negative-control / mechanism-bounding evidence：它排除了简单 pairwise strong locking，但还没有直接证明 sampler-island 修复来自某个具体 TDC 相位指标。

当前最强结果：
- `random1 baseline` 强偏置：p1 约 0.337669，bit min-entropy 约 0.594377。
- 固定 random1 data-RO placement，只移动 sample RO 到 `X45Y39`，20MiB 后 p1 约 0.484799，bit min-entropy 约 0.956792。
- 进一步把 sample RO 和 sampling registers/routing 做 sampler-island，20MiB 文件：
  `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\trng\random1_sampler_island_local_x45y39_regs_x45y31_program_20mib_20260523.bin`
  结果 near ideal：p1=0.5000507474，bit min-entropy=0.9998535814，runs p-value=0.6489840131，SHA256=C42E39A9BC46909105678F20EE918D054C82564FA344FA2F8E1A761D0E0D95E4。
- 六组 sampler-data TDC 已完成，phase_r 全部接近 0（约 -0.00247 到 0.00224），所以不能把机制写成简单 hard locking。TDC 现在支持“排除简单锁定”。
- sampler-island restart formal capture 目前只是诊断失败，不是有效 SP800-90B restart 数据。四个变体里 sample_ro_local warmup0/12 都 0 byte，sampler_island_local warmup0 只采到 36529 bytes，warmup12 0 byte。下一步不能盲目重跑，要先做 debug-header smoke。

硬件环境：
- Vivado: `C:\Programs\Xilinx2023\Vivado\2023.2`
- Board: 正点原子领航者 V2 / Zynq-7020
- COM: `COM3`
- Baud: `115200`
- 不要并行启动多个会抢 COM3/JTAG/hw_server 的任务。
- 每次硬件任务前先查进程：
  `Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'powershell|vivado|cmd|hw_server' -and ($_.CommandLine -match 'run_fast_hardware_queue|program_and_capture_uart|capture_uart|vivado|read_xadc|program_bitstream|hw_server') } | Select-Object ProcessId,Name,CommandLine | Format-List`
- 不要主动 push GitHub，除非我明确要求。

当前最佳下一步：
P0：实现 reset-aligned / warmup-aligned TDC debug line，而不是继续重复普通 sampler-data TDC。
建议新增 `rtl/tdc/RO_TDC_reset_aligned_top.v`，参数包括 `START_DELAY_CYCLES`、`RO_ENABLE_DELAY_CYCLES`、`WARMUP_PACKETS`、`CAPTURE_PACKETS`、`DEBUG_HEADER`、`RO_A_STAGES`、`RO_B_STAGES`、`PAIR_ID`、`FAMILY_ID`。行为是 reset/lock 后延迟、同步使能 RO、丢弃 warmup packets、输出 header、输出固定数量 TDC packets、然后停止。

P0 分析脚本：新增 `scripts/analyze_tdc_startup_diffusion.py`，计算 early-window bin entropy、transition entropy、residence time、longest same-bin run、small-lag autocorrelation、first-window vs later-window comparison。

实验矩阵：
- `random1 baseline`: warmup0 / warmup12-equivalent
- `random3 goodref`: warmup0 / warmup12-equivalent
- `random1 sampler-island`: warmup0 / warmup12-equivalent，但必须先做 debug-header smoke。

判据：
- 如果 warmup0 TDC bin 集中、warmup12 扩散，并且对应 restart pass/fail 或 fixed-column bias 改善，说明 startup transient 是强机制证据。
- 如果 TDC startup/diffusion 也不分离，但 TRNG/restart 分离，则 TDC 进一步把机制指向 sampling registers/routing/output sampling path，而不是 RO 相位层。

请用中文给我汇报。先总结你读到的项目状态，再给出你要做的下一步；如果可以离线实现，就直接实现。不要做无意义的盲目重复实验。
```

## Expected First Reply from the New Conversation

The new conversation should reply roughly:

```text
我已经把当前状态读成三层证据链：sampler-island 是核心正证据，sampler-data TDC 是排除简单 hard-locking 的负控制，restart fixed-column bias 是 startup transient 的切入点。下一步我会先离线实现 reset-aligned/warmup-aligned TDC 顶层和 startup diffusion 分析脚本；在真正上板前只做 tiny debug-header smoke，避免再浪费 COM3/JTAG 时间。
```

