# 无多板阶段下一步工作清单 2026-05-25

## 当前判断

现在暂时没有多板可用时，不建议继续做大量相似的单板重复采集。当前单板数据已经能支持一个清晰的机制故事：

> RO-TRNG 的 placement 敏感性不能简单解释为 RO-RO hard locking。采样端物理实现，尤其 sample RO、采样寄存器、局部路由和采样孔径，是熵源边界的一部分。

这一主张的证据强度并不平均：

| 证据层 | 当前强度 | 结论 |
| --- | --- | --- |
| sample RO 双向反事实 | 强 | 只改变 sample RO 物理实现即可把 restart 结果拉坏或修好，这是目前最像因果证据的部分 |
| clean reset-aligned TDC | 中，偏约束性 | 没看到强 pairwise hard locking，能排除简单锁定故事，但不能单独证明 sampler-side 机制 |
| restart fixed-column bias | 中到强 | 说明连续流非 IID 指标好不等于 restart 初始固定位置也安全 |
| XADC | 中，条件记录 | 新采集有 after-only XADC，可说明温度/电压没有明显异常；旧数据缺失不能硬补 |
| 多板复现 | 暂缺 | 冲高水平期刊时必须补，不然审稿人会说 single-board anecdote |
| 独立 TDC code-density calibration | 暂缺 | 没有校准前不能写 ps 级 jitter/phase 绝对量 |

## 现在最值得做的事

### P0：把论文证据链压实

目标不是生成更多数据，而是把已有数据变成审稿人能读懂、能复查、能复现的证据包。

应完成：

1. 更新论文图表计划，把 2026-05-25 的 sample RO 双向反事实、clean32k TDC 图和机制证据链表列为正文候选。
2. 写 claim/evidence/limitation 对照表，明确每句话由哪个实验支撑、不能过度声称什么。
3. 给每个关键实验保留 bitstream SHA256、capture SHA256、metadata、分析脚本、输出表。
4. 在论文草稿中采用谨慎表述：TDC rules out simple hard locking，而不是 TDC proves sampler mechanism。

### P0：把复现实验入口固定下来

目标是以后想重做某个实验时，不靠记忆找文件。

应固定的实验入口：

| 实验 | 用途 | 当前入口 |
| --- | --- | --- |
| sample RO forward fail | 证明 formal-routed sample RO 可把 compact passband 拉坏 | `doc/sample_ro_locked_passband_results_20260525.md` |
| sample RO reverse repair | 证明 compact-routed sample RO 可修复 formal warmup4 | `doc/sample_ro_locked_passband_results_20260525.md` |
| clean reset-aligned TDC | 排除简单 hard locking，观察 warmup/alignment 差异 | `doc/tdc_reset_aligned_clean32k_status_20260525.md` |
| 关键实验复现 | 给 GPT/Claude/新对话接手用 | `doc/reproduce_key_experiments_20260525.md` |

### P1：设计 command-gated capture

现在 restart/TDC 很多设计是 auto-stream：bitstream 下载后等固定延时自动吐数据。这能跑通，但对 XADC before/after 和 PC 打开串口时机不友好。

下一步应该设计命令触发版本：

```text
PC 打开 COM3
PC 发送启动命令，例如 A5 C3
FPGA 收到命令
FPGA 输出 header
FPGA 开始 stream
PC capture
PC 读 XADC after
```

这样可以解决：

- Vivado 读 XADC before_capture 时错过 UART header；
- START_DELAY_CYCLES 需要调很大；
- 每次采集是否真正从 reset/restart 对齐开始难以证明。

注意：当前 fpga1 明确可用的约束里只有 `UART_TX_o` 在 `J15`，尚未确认 PL 侧 `UART_RX` 板级引脚。因此不要直接把原始 `fpga/` 工程的 `UART_RX_i=B9` 移植到 fpga1。命令触发设计前应先做 UART RX pin smoke。

### P1：设计独立 TDC code-density calibration

当前 TDC 只能写 raw-bin relative comparison 或 per-run normalization。不能写：

```text
这个 bin 差等于多少 ps 的真实 jitter
```

要写绝对时间或更强 TDC 机制，需要独立校准：

1. 保持同样 TDC lane、CARRY4 数量、采样时钟和 UART packet 格式。
2. 用独立异步校准 RO 或 phase-walk source 驱动 TDC input，而不是用正在研究的 RO pair 本身。
3. 每个 lane 至少采 2 MiB，推荐 8 MiB 到 16 MiB。
4. 生成 bin count、probability、width、DNL、INL、phase center。
5. 用固定校准 LUT 重新分析 pair TDC 和 reset-aligned TDC。

论文边界：

```text
校准前：raw-bin / code-density-normalized relative TDC evidence
校准后：calibrated code-density TDC evidence
```

### P1：写 reviewer-risk audit

审稿人最可能攻击的点：

| 攻击点 | 现在怎么回应 | 还要补什么 |
| --- | --- | --- |
| 单板偶然性 | 当前只能承认 single-board mechanistic study | 多板复现 sample RO 双向反事实 |
| TDC 未校准 | 只做 raw-bin 相对比较，不写 ps 级绝对时间 | 独立 code-density calibration |
| XADC 不完整 | 新采集有 after-only XADC，旧数据不强称 | command-gated 后补 before/after |
| cherry-picking placement | 已有 placement matrix 和 20 MiB repeat | 整理成完整 spectrum 图和 supplement |
| SP800-90B 不等于完整认证 | 写成 entropy assessment / restart evidence | 需要时补完整 IID/non-IID/restart 报告包 |

## 当前不建议做的事

### 不建议盲目继续单板重复

如果没有新假设，继续重复 random1/random3 或相同 placement 的 20 MiB capture，论文收益很低。它会增加文件量，但不会明显增强机制解释。

### 不建议过度修改 RTL 主线

当前 sample RO 双向反事实已经是强结果。除非为了 command-gated 或 calibration，不应大范围改动可复现实验的 RTL，否则会让“这个结果到底来自哪个版本”变得更难解释。

### 不建议把 TDC 写成唯一根因

clean32k TDC 的强结论是排除简单 hard locking；弱结论是 sampler-local warmup12 的 diffusion 指标略好。真正的因果主证据来自 sample RO 反事实，不是 TDC 单独证明。

## 等多板恢复后的最小矩阵

多板恢复后，不需要马上跑全量 placement matrix。先跑最能回答审稿人的最小矩阵：

| board | experiment | warmup | repeats | 目的 |
| --- | --- | ---: | ---: | --- |
| board B/C | compact top + formal sample RO locked | 5 | 2 | 验证 forward fail 是否跨板复现 |
| board B/C | formal top + compact sample RO locked | 4 | 2 | 验证 reverse repair 是否跨板复现 |
| board B/C | clean reset-aligned TDC sampler-local | 0/12 | 1 | 验证 hard-lock exclusion 和 sampler-local 弱趋势 |
| board B/C | XADC after-only 或 command-gated before/after | all | all | 报告每次实验条件 |

若这四组跨板成立，论文质量会明显上一个台阶。

## 当前论文定位

以现有单板结果，已经可以写一篇有机制亮点的会议论文或期刊初稿。冲高水平期刊还需要：

1. 多板复现 sample RO 双向反事实；
2. 独立 TDC code-density calibration；
3. command-gated capture，保证 before/after XADC 和 reset alignment 更严谨；
4. 完整图表包和 claim boundary，避免过度声称。

