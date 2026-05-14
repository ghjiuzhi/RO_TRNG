# RO_TRNG 实验执行状态（2026-05-13）

最后更新时间：2026-05-13 15:15 +08:00

## 当前一句话状态

现在没有正在跑的采集任务。COM3/JTAG 当前空闲，`hw_server.exe` 仍在 `localhost:3122` 监听。

所有子 session 当前状态：

| 子 session | 职责 | 当前状态 |
| --- | --- | --- |
| 主对话 | 架构、论文逻辑、调度 | 活跃 |
| Russell | 硬件执行：Vivado/JTAG/COM3/采集 | 已完成当前队列 |
| Nietzsche | 实验状态文档 | 已完成本文档 |
| Carver | 数据分析、论文边界 | 已完成只读分析 |
| Darwin | 论文故事线和图表规划 | 已完成文档 |

## 最新硬件执行结果

Russell 已完成 4 个 5MiB repeat，用来验证最关键的好/坏对照是否可重复。

| Run | 状态 | bytes | SHA256 | p1 | bit min-entropy | 解释 |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `random1_repeat02_5mib` | 成功 | 5,242,880 | `FAC1A5CFCDA3A82ACEA1D8C3503F4CED49B6070FDCEF9F5C054B03CA92A3A470` | 0.337669 | 0.594377 | 与 `random1_run01` 一致，严重偏置可重复 |
| `random3_repeat02_5mib` | 成功 | 5,242,880 | `3DC7AE9DFC0E718F87E2E4F851061F6D1817CDD72C0D3FA0798F3357D536D359` | 0.499971 | 0.999917 | 与 `random3_run01` 一致，优秀结果可重复 |
| `compact_repeat02_5mib` | 成功 | 5,242,880 | `EB601E16DC5E287778BD73AFD7D10DAE7ABA3BFD2A04937BF1117D28641AD917` | 0.500059 | 0.999829 | 与 `compact_run01` 一致，优秀结果可重复 |
| `sparse_repeat02_5mib` | 成功 | 5,242,880 | `DC9AC7B1EC34F7A64EC8530BAC3C59F5D3D3BEA81ECD7D796E21834FF4BE41B5` | 0.464141 | 0.900073 | 与 `sparse_run01` 一致，偏置可重复 |

## 10MiB 正式结果排名

来源：`data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.md`

| 排名 | run | p1 | bit min-entropy | 解释 |
| ---: | --- | ---: | ---: | --- |
| 1 | `random1_run01` | 0.337316 | 0.593606 | 当前最差，严重偏置 |
| 2 | `sparse_run01` | 0.464350 | 0.900637 | 强偏置 |
| 3 | `row_run01` | 0.473580 | 0.925713 | 中等偏置 |
| 4 | `random2_run01` | 0.491222 | 0.974892 | 轻中度偏置 |
| 5 | `far_run01` | 0.491508 | 0.975703 | 轻中度偏置 |
| 6 | `checker_run01` | 0.499929 | 0.999796 | 优秀 |
| 7 | `same_column_run01` | 0.499930 | 0.999799 | bit bias 好，但 runs/相邻相关需谨慎 |
| 8 | `cross_region_run02` | 0.499944 | 0.999839 | 优秀 |
| 9 | `compact_run01` | 0.499948 | 0.999850 | 优秀 |
| 10 | `random3_run01` | 0.499969 | 0.999909 | 当前最好 |

## 不能用于主结论的数据

| 数据 | 状态 | 处理 |
| --- | --- | --- |
| `tdc_near_run01` | TDC packet framing 坏，audit 标记 `valid_for_paper=no` | 不进正式 TDC 统计 |
| `cross_region_run01` | partial，只有约 1.70MiB | 正式结果使用 `cross_region_run02` |
| `random1_run02_partial_timeout_8692840.bin` | partial timeout，8,692,840 bytes | 只作为采集故障记录，不进主排名 |

## 目前能写进论文的结论

- RO placement 会显著影响 raw TRNG 的 `p1`、bit min-entropy、byte entropy 和相邻 bit 相关性。
- `random1` 与 `random3` 是最强对照：同属 random placement 族，一个严重失败，一个接近理想，而且 5MiB repeat 已确认趋势可重复。
- `compact`、`checker`、`cross_region`、`random3` 形成优秀组；`random1` 是严重失败组；`sparse/row/far/random2` 提供中间梯度。
- 不能只写 “compact/sparse/far/random” 粗标签，必须进一步量化实际物理位置、路由、RO 频率、相位和耦合关系。

## 现在还不能过度声称

- 不能说 `random1` 的失败已经由 TDC 证明是耦合/锁定导致。当前 TDC near/far 只是 baseline，还没有对应到 `random1/random3`。
- 不能把 partial 文件混入正式排名。
- 多数 placement 仍需要更多 repeat 才能写强统计显著性和置信区间。

## 下一步队列建议

1. 更新 aggregate 表，把 5MiB repeat 和 10MiB formal 分开汇总。
2. 对 `random1/random3` 做对应 TDC 或 RO frequency/counter 测量，补机制证据。
3. 对 `compact/sparse/random1/random3` 做至少 3 次 repeat，形成均值和方差。
4. 准备 SP800-90B/NIST 数据路径，先对极好和极差样本跑。
5. 生成论文图：min-entropy 排序图、`abs(p1-0.5)` 图、相邻相关图、smoke-vs-formal 散点图、placement map、TDC baseline 图。

## 相关文档

- 论文故事线：[paper_story_and_figures_20260513.md](paper_story_and_figures_20260513.md)
- 详细结果：[hardware_results_20260511_live.md](hardware_results_20260511_live.md)
- 手把手流程：[fpga1_ro_trng_tdc_手把手实验流程_20260510.md](fpga1_ro_trng_tdc_手把手实验流程_20260510.md)

## 2026-05-13 主会话主动调度记录

更新时间：2026-05-13 15:25 +08:00

当前不是空闲状态，已经主动启动三条并行工作线：

| 工作线 | 子 session | 当前任务 | 是否碰硬件 |
| --- | --- | --- | --- |
| 硬件 repeat 队列 | Wegener | 依次补 `far/row/random2/checker/cross_region/same_column` 的 `repeat02_5mib` | 是，唯一允许碰 COM3/JTAG |
| 数据汇总 | Chandrasekhar | 生成 `trng_repeats_by_run` 和 `trng_repeats_by_placement` 汇总表 | 否 |
| 机制验证设计 | Goodall | 写 `random1/random3` 的 TDC/RO frequency 机制验证方案 | 否 |

当前完成度判断：

- 实验没有做完：已有强现象和部分 repeat，但还缺机制验证、更多 repeat、SP800-90B/NIST。
- 数据没有完全分析完：已有 ranked table 和初步分层，正在补 repeat 聚合表和图表输入。
- 论文没有写完：已有故事线和图表规划，还需要机制数据和正式统计后才能写完整主文。

主会话职责：持续调度、同步状态、决定下一步；不再等用户说“继续”才推进。
## 2026-05-13 15:22 主会话总控状态

结论先写清楚：实验还没有全部做完，数据还没有最终分析完，论文还没有到可投稿定稿状态。现在已经完成的是 placement 矩阵第一轮 10MiB 正式 TRNG 采集、部分 5MiB repeat、TDC near/far baseline、初步统计汇总、论文故事线草稿和 random1/random3 机制验证方案。正在进行的是第二轮 5MiB repeat 硬件采集。

当前分工：

| 会话 | 职责 | 当前状态 |
| --- | --- | --- |
| 主会话 | 架构、监控、汇总、文档、论文逻辑、下一步调度 | 正在监控硬件进度并更新本文档 |
| Wegener | 唯一硬件执行会话，占用 Vivado/JTAG/COM3 | 正在采 `far_repeat02_5mib`，命令为 `program_and_capture_uart.ps1`，COM3，115200 baud，目标 5MiB |
| Chandrasekhar | 重复采样统计汇总 | 已完成 `scripts/summarize_trng_repeats.py` 及 repeat 汇总表 |
| Goodall | random1/random3 机制验证方案 | 已完成 `doc/mechanism_validation_plan_random1_random3_20260513.md` |
| Hubble | RO frequency / beat-frequency 机制实验准备 | 已完成 RTL、XDC 生成、分析脚本、机制实验文档 |
| Godel | 中文论文初稿骨架 | 已完成 `doc/paper_draft_cn_20260513.md` |
| Sagan | RO frequency probe 离线 Vivado build | 运行中，只允许 synth/impl/write_bitstream，不碰 COM3/JTAG/hw_server |

硬件实时状态：

| 项目 | 状态 |
| --- | --- |
| `hw_server` | 运行中，`localhost:3122` |
| 当前采集文件 | `far_repeat02_5mib` 已完成；Wegener 正在编程 `row_pitch3_x38y43`，准备采 `row_repeat02_5mib` |
| 15:21 文件大小 | 约 735264 bytes，说明串口已经有数据，不是死等 0 字节 |
| 15:24 文件大小 | 2652536 / 5242880 bytes，约 50.59%，仍在增长 |
| 15:28 完成状态 | `far_repeat02_5mib.bin` 达到 5242880 bytes，metadata、sha256、analysis 已生成 |
| `far_repeat02_5mib` 初步结果 | `p1=0.491642475`，`bit_min_entropy=0.976084602`，与 `far_run01` 趋势一致 |
| 15:31 队列状态 | Vivado 正在编程 `data/vivado_runs/fpga1_ro_trng_matrix/row_pitch3_x38y43/seed_1/RO_TRNG_top.bit` |
| 预计耗时 | 115200 baud 下采 5MiB 原始串口数据通常是小时级，后续 `row/random2/checker/cross_region/same_column` 还会继续排队 |

现在不能声称已经完成的部分：

| 事项 | 原因 |
| --- | --- |
| 顶刊级完整实验 | 还缺每种 placement 多次 repeat，缺 TDC 对应 placement 机制测量，缺温压/时间漂移等扩展维度 |
| TDC 证明耦合/锁定 | 现有 TDC near/far 只是 baseline，不是 random1/random3 的同位置 RO pair 测量 |
| 论文定稿 | 现在只能写初稿和图表框架，核心机制证据还需要 frequency / beat-frequency / TDC pair 补强 |

下一步自动动作：

1. 持续监控 `far_repeat02_5mib.bin` 是否增长，完成后让 Wegener 自动进入 `row_repeat02_5mib`、`random2_repeat02_5mib`、`checker_repeat02_5mib`、`cross_region_repeat02_5mib`、`same_column_repeat02_5mib`。
2. 每完成一个 repeat，就重新跑 `scripts/summarize_trng_repeats.py`，更新 `trng_repeats_by_run.csv/md` 与 `trng_repeats_by_placement.csv/md`。
3. 按 Goodall 方案准备下一批机制实验：优先做 random1/random3 的 RO frequency / beat-frequency，再选关键 pair 做对应 placement TDC。
4. 主会话继续维护本文档作为总控面板。

快速查看当前采集状态可以运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\show_capture_status.ps1 -Run far_repeat02_5mib -Bytes 5MiB
```

新增工具：

| 文件 | 作用 |
| --- | --- |
| `scripts/show_capture_status.ps1` | 不碰硬件，只读取文件系统和进程，显示当前 `.bin` 大小、目标进度、metadata、sha256、analysis 是否已生成 |

15:33 已执行一次 repeat 汇总：

| 输出 | 状态 |
| --- | --- |
| `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.md` | 已更新，纳入 15 条 complete formal/repeat captures |
| `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md` | 已更新，`far` 已有 formal + repeat 对照 |

15:42 `row_repeat02_5mib` 已完成并纳入汇总：

| 指标 | 数值 |
| --- | ---: |
| bytes | 5242880 |
| p1 | 0.473337555 |
| bit min-entropy | 0.925049507 |
| adjacent equal ratio | 0.504302442 |

row 的 repeat 与 formal 很接近：formal `p1=0.473579586`、`bit_min_entropy=0.925712657`，repeat `p1=0.473337555`、`bit_min_entropy=0.925049507`。这支持“row placement 的偏置可重复”，可以进入论文的 repeat evidence。

15:45 repeat 汇总已再次执行：

| 输出 | 状态 |
| --- | --- |
| `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.md` | 已更新，纳入 16 条 complete formal/repeat captures |
| `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md` | 已更新，`far` 和 `row` 均已有 formal + repeat 对照 |

## 2026-05-13 15:40 调度策略更新

用户希望掌控大方向，不需要每几十秒看一次文件增长。因此后续只记录和汇报关键节点：

| 节点 | 是否汇报 |
| --- | --- |
| 子会话启动/完成/失败 | 是 |
| 某个 5MiB repeat 完成、失败、卡住 | 是 |
| 汇总表或论文文档更新 | 是 |
| Vivado build 开始/完成/失败 | 是 |
| `.bin` 文件每隔几十秒增长多少 | 否，除非用于判断卡住或恢复 |

Hubble 已新增机制实验材料：

| 文件/目录 | 作用 |
| --- | --- |
| `doc/random1_random3_ro_frequency_beat_experiment_20260513.md` | random1/random3 RO frequency / beat-frequency 实验说明 |
| `rtl/debug/RO_FREQ_trng_probe_top.v` | frequency probe 顶层 |
| `rtl/debug/ro_freq_entropy_probe.v` | 复用 TRNG RO 结构的频率/beat probe |
| `scripts/generate_ro_freq_probe_xdc.py` | 生成 random1/random3 probe XDC |
| `scripts/analyze_ro_frequency_matrix.py` | 解析 14-byte UART 帧，输出 per-frame、per-RO、beat、pulling CSV |
| `scripts/vivado/run_fpga1_ro_freq_probe_inmem.tcl` | 离线 build frequency probe bitstream |
| `data/experiments/xdc_ro_freq/` | random1/random3 probe placement XDC |

Sagan 已被调度去 build：

```powershell
vivado -mode batch -source scripts\vivado\run_fpga1_ro_freq_probe_inmem.tcl `
  -tclargs data\experiments\xdc_ro_freq\ro_freq_random1_seed1_x36y35_sample_x36y35.xdc `
  data\vivado_runs\fpga1_ro_freq_probe\random1_seed1_x36y35 1 100

vivado -mode batch -source scripts\vivado\run_fpga1_ro_freq_probe_inmem.tcl `
  -tclargs data\experiments\xdc_ro_freq\ro_freq_random3_seed3_x36y35_sample_x36y35.xdc `
  data\vivado_runs\fpga1_ro_freq_probe\random3_seed3_x36y35 3 100
```

## 2026-05-13 20:15 主会话接管状态

子会话 Wegener 与 Sagan 因额度限制退出。主会话已经接管执行，不再依赖子会话继续推进。

接管时的节点状态：

| 事项 | 状态 |
| --- | --- |
| `random1` RO frequency probe bitstream | 已生成：`data/vivado_runs/fpga1_ro_freq_probe/random1_seed1_x36y35/RO_FREQ_trng_probe_top.bit` |
| `random3` RO frequency probe bitstream | 已由主会话启动后台 Vivado build，PID 31208 |
| TRNG repeat | 已完成到 `row_repeat02_5mib`，已纳入汇总 |
| `checker_repeat02_5mib` | 发现一个约 1.35MiB 的部分文件，无 metadata，不进入正式统计 |
| `random2/checker/cross_region/same_column` repeat | 主会话已建立接管队列，等待当前 `random3` 离线 Vivado build 结束后自动重新采集 |

新增接管脚本：

| 文件 | 作用 |
| --- | --- |
| `scripts/run_takeover_remaining_repeats.ps1` | 等待指定 Vivado PID 结束后，顺序采 `random2_repeat02_5mib`、`checker_repeat02_5mib`、`cross_region_repeat02_5mib`、`same_column_repeat02_5mib` |

当前后台队列日志：

| 日志 | 状态 |
| --- | --- |
| `data/hardware/20260511_fpga1_board1/logs/takeover_remaining_repeats_20260513_201414.log` | 已启动，正在等待 Vivado PID 31208 |

20:20 节点更新：

| 事项 | 状态 |
| --- | --- |
| `random3` RO frequency probe build | 首次重跑失败，原因是 Vivado 未找到 `data/vivado_runs/xc7z020clg400.gen/sources_1/ip/clk_wiz_0/clk_wiz_0.dcp` |
| 修复 | 已更新 `scripts/vivado/run_fpga1_ro_freq_probe_inmem.tcl`，当 shared generated IP DCP 缺失时，从原始 `fpga1/xc7z020clg400/xc7z020clg400.gen/sources_1/ip/` 拷贝 fallback DCP |
| 当前硬件采集 | `random2_repeat02_5mib.bin` 正在增长，尚未生成 metadata |
| 下一步 | 等硬件接管队列空闲后，重跑 `random3` frequency probe build |

20:24 节点更新：

| 事项 | 状态 |
| --- | --- |
| `random2_repeat02_5mib` | 已完成，SHA256 `BA89FBA3927D03108EFC6CC0506761055F1C3BBADB00083FBF9DF037D8CF0221` |
| `random2` repeat 指标 | `p1=0.491030312`，`bit_min_entropy=0.974348355`，`adjacent_equal_ratio=0.501148617` |
| 汇总表 | 已重跑，纳入 17 条 complete formal/repeat captures |
| 当前硬件队列 | 已进入 `checker_repeat02_5mib`，会覆盖之前无 metadata 的部分文件 |

random2 的 repeat 与 formal 接近：formal `p1=0.491222239`、`bit_min_entropy=0.974892483`，repeat `p1=0.491030312`、`bit_min_entropy=0.974348355`。这支持 random2 的偏置可重复。

20:41 节点更新：

| 事项 | 状态 |
| --- | --- |
| `checker_repeat02_5mib` | 已完成并纳入汇总 |
| `checker` repeat 指标 | `p1=0.499947119`，`bit_min_entropy=0.999847425`，`adjacent_equal_ratio=0.500090802` |
| 汇总表 | 已重跑，纳入 18 条 complete formal/repeat captures |
| 当前硬件队列 | Vivado 正在编程 `cross_region_repeat02_5mib` |

checker 的 repeat 与 formal 接近：formal `p1=0.499929237`、`bit_min_entropy=0.999795837`，repeat `p1=0.499947119`、`bit_min_entropy=0.999847425`。

21:02 节点更新：

| 事项 | 状态 |
| --- | --- |
| `cross_region_repeat02_5mib` | 已完成并纳入汇总 |
| `cross_region` repeat 指标 | `p1=0.500011396`，`bit_min_entropy=0.999967117`，`adjacent_equal_ratio=0.500044811` |
| 汇总表 | 已重跑，纳入 19 条 complete formal/repeat captures |
| 当前硬件队列 | 剩余 `same_column_repeat02_5mib` |
| 论文结果更新 | Ampere 已完成 `doc/paper_results_update_20260513.md` |

cross_region 的 repeat 与 formal 接近：formal `p1=0.499944150`、`bit_min_entropy=0.999838861`，repeat `p1=0.500011396`、`bit_min_entropy=0.999967117`。

21:10 节点更新：

| 事项 | 状态 |
| --- | --- |
| 数据审计 | Hypatia 已完成 `doc/data_audit_20260513.md` |
| `random1` RO frequency probe bit | 已生成：`data/vivado_runs/fpga1_ro_freq_probe/random1_seed1_x36y35/RO_FREQ_trng_probe_top.bit` |
| `random3` RO frequency probe bit | 已生成：`data/vivado_runs/fpga1_ro_freq_probe/random3_seed3_x36y35/RO_FREQ_trng_probe_top.bit` |
| 当前硬件队列 | `same_column_repeat02_5mib` 正在采集，约 4MiB，尚未生成 metadata |

至此，下一阶段的 random1/random3 频率/beat 机制实验所需 bitstream 已准备好。等当前 `same_column` repeat 完成后，可以安排采集：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\capture_uart.ps1 `
  -Port COM3 -Baud 115200 -Kind raw -Run random1_ro_freq_run01 -Bytes 5MiB `
  -OutFile data\hardware\20260511_fpga1_board1\ro_freq\random1_ro_freq_run01.bin `
  -Bitstream data\vivado_runs\fpga1_ro_freq_probe\random1_seed1_x36y35\RO_FREQ_trng_probe_top.bit `
  -MetadataDir data\hardware\20260511_fpga1_board1\metadata
```

注意：frequency probe 输出是 14-byte 帧，采集后要用 `scripts/analyze_ro_frequency_matrix.py`，不是 TRNG bitstream 统计脚本。

21:22 机制 smoke 发现并修复：

| 事项 | 状态 |
| --- | --- |
| `random1_ro_freq_run01_2mib` | 已采 2MiB，SHA256 `08717B60A524112830E81E61E166D43B14D45A143C6197F02421C8B6BA72D21C` |
| 解析结果 | `scripts/analyze_ro_frequency_matrix.py` 未找到有效 14-byte 帧 |
| 根因 | 实际 UART 字节呈 7-byte 周期 `14 52 01 mode mask 64 count`，说明 `RO_FREQ_trng_probe_top` 的 `tx_data/tx_valid` 同周期握手导致 `uart_tx` 锁存旧字节、帧错位/丢半 |
| 修复 | 已修改 `rtl/debug/RO_FREQ_trng_probe_top.v`，发送状态机改为 `SEND_LOAD -> WAIT_LOW -> WAIT_HIGH`，等待 `tx_ready` 完成一个完整字节后再发送下一个字节 |
| 当前动作 | 已要求 Volta 重建 fixed random1/random3 frequency bitstream 到 `data/vivado_runs/fpga1_ro_freq_probe_fixed/` |

结论：旧 `fpga1_ro_freq_probe/random*_seed*_x36y35/RO_FREQ_trng_probe_top.bit` 不应用于正式机制采集；需要使用 fixed 目录下的新 bitstream。

21:27 fixed bitstream 完成：

| bitstream | 状态 |
| --- | --- |
| `data/vivado_runs/fpga1_ro_freq_probe_fixed/random1_seed1_x36y35/RO_FREQ_trng_probe_top.bit` | 成功，Vivado 0 ERROR / 0 CRITICAL，timing met，WNS 1.538 ns |
| `data/vivado_runs/fpga1_ro_freq_probe_fixed/random3_seed3_x36y35/RO_FREQ_trng_probe_top.bit` | 成功，Vivado 0 ERROR / 0 CRITICAL，timing met，WNS 1.250 ns |

后续正式机制采集必须使用 `fpga1_ro_freq_probe_fixed` 目录下的 bitstream。

21:34 fixed frequency smoke 完成：

| 事项 | 状态 |
| --- | --- |
| `random1_ro_freq_fixed_smoke01_512k` | 采集完成，SHA256 `F0E280B401EBBB72577DBF9EC96EB8876E077C078C4111EDD9FDC7E1EBC6CEF1` |
| `random3_ro_freq_fixed_smoke01_512k` | 采集完成，SHA256 `C42BB8DF443DC3244CDD5523687AA75260334A52CB23657049BF3C519CE0E99E` |
| 合并解析 | `valid_frames=74890`，`dropped_or_unframed_bytes=116` |
| 分析输出 | `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_smoke/` |

初步机制线索：

| family | 最近 all-on pair | 频差 | beat period |
| --- | --- | ---: | ---: |
| random1 | data4 / data5 | 0.488 MHz | 2048.23 ns |
| random1 | data0 / data1 | 0.941 MHz | 1062.82 ns |
| random3 | data3 / data7 | 0.701 MHz | 1426.14 ns |
| random3 | data3 / data5 | 2.293 MHz | 436.17 ns |

pulling 初步线索：

| family | 最大 shift 对象 | shift ppm vs single |
| --- | --- | ---: |
| random1 | sample | 3388.4 ppm |
| random3 | sample | -2497.9 ppm |

解释边界：这只是 512KiB smoke，用于证明 fixed probe 和分析链路可用，并提供机制假设线索；还不能作为最终机制结论。已启动 Ramanujan 子会话专门整理 `doc/ro_frequency_smoke_interpretation_20260513.md`。

22:04 fixed frequency run01 2MiB 完成：

| 事项 | 状态 |
| --- | --- |
| `random1_ro_freq_fixed_run01_2mib` | 完整采集 2MiB，SHA256 `2E06E59CF3A38BB3C4B4BD5CFFF2409A9C8A19FD4BF3B25B048EBAF00273E3BB` |
| `random3_ro_freq_fixed_run01_2mib` | 完整采集 2MiB，SHA256 `AE6C877269AEA5679791B4E9F530CBCF1430F7CE9BE9438398C75426D6F0F2CA` |
| 合并解析 | `valid_frames=299546`，`dropped_or_unframed_bytes=660` |
| 分析输出 | `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/` |

run01 最近 all-on pair：

| family | 最近 pair | 频差 | beat period |
| --- | --- | ---: | ---: |
| random1 | data4 / data5 | 0.466 MHz | 2145.03 ns |
| random1 | data0 / data1 | 0.979 MHz | 1021.36 ns |
| random3 | data3 / data7 | 0.673 MHz | 1485.01 ns |
| random3 | data3 / data5 | 2.327 MHz | 429.81 ns |

run01 pulling 线索：

| family | 最大 shift 对象 | shift ppm vs single |
| --- | --- | ---: |
| random1 | sample | +3466.9 ppm |
| random3 | sample | -824.6 ppm |

解释边界：run01 已经是完整 2MiB 机制采集，能作为论文机制线索；但仍需 repeat 和 TDC pair 对应验证，才能把“频率接近/all-on pulling 导致 TRNG 退化”写成强因果结论。

21:15 节点更新：

| 事项 | 状态 |
| --- | --- |
| `same_column_repeat02_5mib` | 已完成并纳入汇总 |
| 汇总表 | 已重跑，纳入 20 条 complete formal/repeat captures，即 10/10 formal + 10/10 repeat |
| 当前 TRNG repeat 矩阵 | 第一轮 10MiB + 第二轮 5MiB 全覆盖完成 |
| 当前机制 bitstream | `random1` 与 `random3` RO frequency probe bit 均已生成 |

`same_column` repeat 指标：

| 指标 | 数值 |
| --- | ---: |
| p1 | 0.499835944 |
| bit min-entropy | 0.999526713 |
| runs_p | 0 |
| adjacent equal ratio | 0.506032288 |
| byte min-entropy | 7.866729325 |

same_column 的核心现象复现：bit bias 接近理想，但 runs/adjacent 结构异常持续存在。formal `adjacent_equal_ratio=0.505979735`、repeat `0.506032288`，说明只看 p1/min-entropy 会漏掉布局引入的结构相关性风险。
