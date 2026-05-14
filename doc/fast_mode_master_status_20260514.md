# Fast Mode Master Status 2026-05-14

更新时间：2026-05-14 约 12:10，主控线程离线汇总。  
硬件链路：当前只保留 `hw_server` 常驻，未发现正在运行的 Vivado 编程、串口采集或 fast-mode 队列。为避免抢占 COM3/JTAG，后续硬件任务仍然只允许单队列串行执行。

## 当前阶段判断

现在已经从“抢硬件数据”阶段进入“论文证据链整理 + 合规随机性验证准备”阶段。

已经完成的硬件实验足以支撑一个明确结论：同一个 RO-TRNG 结构在不同 placement 下会出现显著且可重复的原始随机性差异；但是还不足以支撑“近距离 RO 一定发生强锁定/同步”的强机制结论。当前 TDC pair 数据更像是一个重要的反证边界：在 6 个重点 pair、当前 TDC 观测方式和运行条件下，没有检测到强 pair locking。

## 硬件采集完成情况

主 fast-mode 队列完成，状态文件为 `doc/fast_mode_hardware_status_20260513.md`。

已完成：

- RO_FREQ：`random1/random3` 多次重复采样，包含 2MiB repeat 与 5MiB 扩展样本。
- TDC baseline：`tdc_near_run03_2mib`、`tdc_far_run02_2mib`。
- TRNG baseline：原始 `fpga1` 工程 10MiB 与 5MiB 重复采样。
- Pair-specific TDC：6/6 完成，状态文件为 `doc/fast_mode_tdc_pair_status_20260514.md`。

Pair-specific TDC 已完成列表：

- `random1_ro4_ro5`
- `random1_ro0_ro1`
- `random1_ro2_ro4`
- `random3_ro3_ro7`
- `random3_ro3_ro5`
- `random3_ro0_ro6`

## 已看到的核心结果

TRNG placement 矩阵：

- `random1` 是稳定坏例：10MiB formal `p1 = 0.337315512`，bit min-entropy `0.593605945`；5MiB repeat 仍接近同一水平。
- `random3` 是稳定好例：10MiB formal `p1 = 0.499968565`，bit min-entropy `0.999909299`；5MiB repeat 仍接近理想。
- `same_column` 的 p1 接近 0.5，但 runs p-value 为 0、相邻结构异常，说明只看 bias 不够。
- 原始 `fpga1` baseline 表现良好：10MiB `p1 = 0.500035894`，bit min-entropy `0.999896436`；5MiB repeat `p1 = 0.500216961`，bit min-entropy `0.999374119`。

RO_FREQ：

- `random1` 和 `random3` 都存在较近 data/data beat，因此“近频率 pair 存在”不是充分因果解释。
- `random1` 的 sample RO pulling 在部分运行中明显更强，提示可能存在 placement-dependent dynamic interaction，而不是简单的静态近距离锁定。

TDC pair dynamics：

- 6 个 pair、96 个窗口，strong-lock windows = 0。
- 最大绝对 zero/small-lag 相关量级仍很低，当前应表述为“未检测到强 pair locking”，不能写成“证明没有耦合”。

## 论文主张边界

可以主张：

- Placement 对 RO-TRNG 原始随机性有显著、可重复影响。
- “compact/checker/random/far”等粗标签不足以解释结果，必须引入物理测量和 placement 细节。
- TDC/RO_FREQ 能作为机制诊断工具，帮助区分 bias、相邻结构、频率拉拽、相位相关等不同现象。
- 当前数据支持“placement-dependent dynamic interaction / frequency proximity / sample pulling / weak or transient coupling”的机制假设。

不能主张：

- 不能说已经证明近距离 RO 发生强锁定。
- 不能把 TDC bin 当作未校准的线性时间直接做绝对时延结论。
- 不能把单板、常温、默认电压结果直接推广到所有 FPGA、所有环境。
- 不能用 smoke 或 STS 结果替代 NIST SP800-90B 熵评估。

## 正在并行推进的任务

主控线程：

- 维护本状态文件。
- 根据子任务输出决定是否追加硬件队列。
- 保证不会并行启动多个抢 COM3/JTAG 的硬件任务。

子任务 A：

- 已完成。输出干净 UTF-8 中文论文结果文档：`doc/paper_results_after_tdc_pairs_utf8_20260514.md`。第一次子任务输出出现编码乱码，主控线程已重写为可读中文版本。

子任务 B：

- 已完成并验收。生成论文图表/表格证据包：`data/experiments/paper_artifacts_20260514`。
- 关键产物：`claims_vs_evidence.csv/md`、`table_placement_trng_repeats.csv/md`、`table_ro_freq_pulling_summary.csv/md`、`table_tdc_pair_dynamics_summary.csv/md`、`fig_tdc_pair_best_lag_abs_r.svg`。

子任务 C：

- 已完成。当前不是数据阻塞，而是工具链阻塞：PowerShell 环境缺少 `g++`、`make/mingw32-make` 以及可验证的链接库环境。
- blocker 文档：`doc/sp800_90b_blocker_20260514.md`。
- smoke 输入已存在：`data/sp800_90b/inputs_smoke_20260514`。

## 下一步优先级

P0：完成论文证据包和中文结果总结。  
P0：跑通或明确阻塞 SP800-90B，至少形成可复现输入和执行说明。当前已明确阻塞，需要安装 MSYS2/WSL 依赖后继续。  
P1：如果还有时间上板，追加最有价值的硬件任务不是“更多随机扫”，而是对 `random1` 坏例和 `random3` 好例做更长时长重复，优先 10MiB/20MiB 原始 bitstream 与 RO_FREQ repeat。  
P1：多板、温度、电压属于冲顶刊的强加分项；若当前硬件条件不足，应作为 limitation 和 future validation 写清楚。

## 子任务关闭状态

- 图表证据包子任务：已关闭。
- SP800-90B 工具链子任务：已关闭。
- 中文论文结果子任务：因输出乱码，已关闭；主控线程已接管并修复。

## 是否需要立即继续硬件实验

当前不建议盲目启动新的硬件长队列。理由：

- 已规划 fast-mode 硬件和 6 个 pair TDC 均已完成。
- 论文当前最大缺口不是更多 COM3 数据，而是 SP800-90B 运行环境、论文叙事、以及如果冲顶刊才需要的多板/PVT。
- 如果今天继续上板，最有价值的追加队列应很短，只围绕 `random1` 与 `random3` 做更长 repeat 和 restart 数据准备。
