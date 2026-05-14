# Fast Mode 总状态 - 2026-05-14

更新时间：2026-05-14 约 12:55。

## 当前阶段

项目已经从“能不能采到数据”进入“证据链补强和论文可复现打包”阶段。

当前硬件短队列仍在运行，必须继续保持 COM3/JTAG/Vivado 串行：

- 队列：`data/experiments/fast_mode/hardware_queue_short_20260514.csv`
- 状态文档：`doc/fast_mode_short_queue_status_20260514.md`
- 当前运行：`random1_repeat03`
- 目标大小：20 MiB
- 当前观察：文件正在增长，说明串口采集链路正常

不要并行启动第二个 Vivado/program/capture 队列，否则会抢 COM3、JTAG 或 `hw_server`。

## 已完成硬件证据

主 fast-mode 硬件队列已经完成，详见：

- `doc/fast_mode_hardware_status_20260513.md`
- `doc/fast_mode_tdc_pair_status_20260514.md`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`

已经完成的数据类型：

- TRNG placement matrix：`compact`、`checker`、`sparse`、`far`、`same_column`、`cross_region`、`random1/2/3`、`row` 等。
- 原始 `fpga1` baseline：10 MiB formal 和 5 MiB repeat。
- RO_FREQ：`random1/random3` 多次 repeat。
- TDC near/far baseline。
- Pair-specific TDC：6 个重点 pair，全部完成。

6 个 pair-specific TDC：

- `random1_ro4_ro5`
- `random1_ro0_ro1`
- `random1_ro2_ro4`
- `random3_ro3_ro7`
- `random3_ro3_ro5`
- `random3_ro0_ro6`

## 主要结论边界

可以主张：

- 同一块 Zynq-7020、同一 RO-TRNG 结构、同一 UART 采集链路下，placement 会显著改变原始随机性。
- `random1` 是稳定坏例：10 MiB formal 中 `p1 = 0.337315512`，快速 bit min-entropy 为 `0.593605945`。
- `random3` 是稳定好例：10 MiB formal 中 `p1 = 0.499968565`，快速 bit min-entropy 为 `0.999909299`。
- 原始 `fpga1` baseline 表现也较好：10 MiB `p1 = 0.500035894`，快速 bit min-entropy 为 `0.999896436`。
- TDC/RO_FREQ 可作为机制诊断工具，而不是只做黑盒随机性测试。

不能主张：

- 不能说已经证明“近距离 RO 必然强锁定”。
- 不能把未校准 TDC bin 当作绝对线性时间。
- 不能把单板、常温、默认电压结果直接推广到所有 FPGA/PVT 条件。
- 不能把 smoke 90B 或 STS 结果写成完整 SP800-90B 认证。

## TDC Pair 结果

当前 pair-specific TDC 是一个重要的负结果：

- pair runs：6
- total windows：96
- strong-lock windows：0
- max small-lag abs correlation：约 0.0318
- mean diff std：约 2040 ps 到 2043 ps

论文中应表述为：在当前观测方式和实验条件下，没有检测到强 pair-level phase locking。它不能证明完全没有耦合，也不能证明随机性差异来自单个近邻 pair 的强同步。

更稳妥的机制叙事是：placement 改变多 RO 网络的动态相互作用、频率接近程度、采样相位覆盖、局部布线延迟和序列相关结构。

## SP800-90B 当前进展

MinGW 路线已经跑通：

- build script：`scripts/build_90b_mingw.ps1`
- executable：`sim/SP800-90B_EntropyAssessment/cpp/ea_non_iid.exe`、`ea_iid.exe`、`ea_restart.exe`
- input preparation：`scripts/prepare_90b_inputs.py`
- smoke runner：`scripts/run_90b_smoke.ps1`
- result parser：`scripts/summarize_90b_results.py`
- summary：`data/sp800_90b/results_smoke_20260514/summary.md`
- status：`doc/sp800_90b_blocker_20260514.md`

已经完成 11 个布局的 1,000,000-symbol non-IID smoke，包含 MSB-first 和 LSB-first 两种 bit-order 敏感性检查。另对 `random1/random3/original` 做了 IID smoke 诊断，三个流都未通过 IID 路线的 LRS 检查，因此论文主线应使用 non-IID 估计。

核心 8M bit-symbol non-IID 也已补完：

- `random1_run01`：`H_original = 0.389520`
- `random3_run01`：`H_original = 0.902345`
- `original_fpga1_run01_10mib`：`H_original = 0.877727`

`random1_repeat03` 的 repeat smoke 已补完：MSB `0.390399`，LSB `0.390783`，进一步说明坏 placement 的低熵表现可重复。

关键观察：

- `random1` 在 MSB/LSB 下都是明显低熵离群点：约 0.385/0.384。
- `random3`、`random2`、`compact`、`checker` 等在 MSB-first smoke 下约 0.86 到 0.87。
- `sparse`、`row` 较低，说明 placement 差异不仅表现为单比特偏置，也会被 90B non-IID 估计器捕捉。

仍然缺口：

- 这是 smoke，不是完整 formal 90B。
- `ea_restart.exe` 已经能编译，但还没有真正的 restart dataset；现有顺序 `.bin` 不能替代 restart 矩阵。
- 最终投稿前建议用更现代的 MSYS2/WSL 工具链复现 headline 结果。

## 正在进行的短队列

短队列目标是补强两个核心对照：

1. `random1_repeat03`：20 MiB TRNG，已完成，验证坏例长时间稳定性。
2. `random3_repeat03`：20 MiB TRNG，正在采集，验证好例长时间稳定性。
3. `random1_ro_freq_fixed_run04_5mib`：RO_FREQ repeat。
4. `random3_ro_freq_fixed_run04_5mib`：RO_FREQ repeat。

队列完成后立即做：

```powershell
python scripts\summarize_trng_repeats.py
python scripts\analyze_fast_mode_results.py
python scripts\make_paper_artifacts_20260514.py
```

然后将 `random1_repeat03`、`random3_repeat03` 加入 SP800-90B smoke repeat。

## 下一步优先级

P0：等短队列完成，不抢硬件。

P0：持续更新 GitHub export，给 GPT/Claude 分析使用，但不上传大体积原始 `.bin`、`.bit`、`.dcp`。

P0：把 SP800-90B smoke 结果纳入论文证据表，措辞为“non-IID smoke supports the placement-dependent gap”，不要写成认证。

P1：设计 restart capture protocol。现有顺序流不能直接冒充 restart dataset。

P1：如果冲更高水平，后续补多板、温度、电压、运行时间漂移；如果做不到，写成 limitation 和 future validation。
