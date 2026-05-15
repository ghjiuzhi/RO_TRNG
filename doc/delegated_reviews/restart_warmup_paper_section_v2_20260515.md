# Restart sanity / warm-up transition / fixed-column bias mechanism 小节草稿

## 可放入论文的中文结果段落

为检查 restart 后早期固定采样位置是否存在可重复偏置，本文在同一 FPGA 板卡、同一 `random3` placement 和同一 auto-stream design-level restart protocol 下构造 formal-size restart matrix。每个数据集包含 1000 次 restart；每次 restart 输出 125 个 packed bytes，即展开后每行为 1000 个 bit symbols。随后分别按 MSB-first 与 LSB-first 两种位序展开并送入 `ea_restart`，以避免把位序解释本身误认为物理偏置来源。需要强调的是，本节结果只刻画当前板卡、当前 placement 和当前 auto-stream protocol 下的 restart sanity 行为；它不构成跨板卡、跨 placement、跨 PVT 的通用阈值，也不应表述为完整 SP800-90B 认证结论。

在不丢弃 restart 后早期 packed bytes 时，`random3` 的整体 1 比例接近均衡（overall `p1=0.497933`），但固定列上仍出现显著偏置：最坏位置位于原始 `byte 0, bit 0`，`X_max=685`，超过该口径下的 restart cutoff `605`，因此 MSB/LSB 两种展开均未通过 restart sanity check。该现象说明，连续长流测试中的近均衡比例和较高 sequential non-IID 熵估计，并不能单独排除 restart 初始相位或早期固定输出位置中的稳定偏置风险。换言之，restart sanity check 暴露的是“同一 restart 后相对位置”的列偏置，而不是普通连续流统计可以完全覆盖的随机性问题。

进一步的 warm-up 扫描显示，丢弃少量早期 packed bytes 后，restart 行为并非单调地立即改善。当 `WARMUP_BYTES=8` 时，overall `p1` 降至 `0.374385`，超过 cutoff 的固定位置数增至 `893`，最坏位置达到 `X_max=721`，MSB/LSB 均失败；当 `WARMUP_BYTES=10` 时，偏置有所缓和，但仍有 `106` 个固定位置超过 cutoff，最坏位置 `X_max=650`，两种位序仍未通过。相反，当 warm-up 增加到 `11` 个 packed bytes 后，超过 cutoff 的位置数降为 `0`，最坏位置为 `X_max=583`，MSB 与 LSB 均通过；`WARMUP_BYTES=12` 和 `16` 也保持通过，最坏位置分别约为 `562` 和 `549`。因此，在本板、本 placement、本 auto-stream restart protocol 下，观测到的通过边界位于 `10 < WARMUP_BYTES <= 11`。

重复实验支持上述边界不是单次运行偶然结果。在边界附近，`WARMUP_BYTES=10` 的两次运行均失败：run01 的 overall `p1=0.415017`、超过 cutoff 位置数为 `106`、最坏 `X=650`；repeat02 的 overall `p1=0.415849`、超过 cutoff 位置数为 `89`、最坏 `X=633`。`WARMUP_BYTES=11` 的两次运行均通过：run01 的最坏 `X=583`，repeat02 的最坏 `X=588`，超过 cutoff 位置数均为 `0`。`WARMUP_BYTES=12` 的两次运行也均通过，overall `p1` 均回到约 `0.4995`，超过 cutoff 位置数为 `0`。这些重复结果使论文中可以较稳妥地写作“当前实验条件下观察到 warm-up transition”，但仍不应外推为通用设计阈值。

从机制角度看，结果更支持一种“restart 后早期采样窗口偏置”的解释，而不是位序展开或文件转换造成的伪象。失败样本的异常集中在固定采样列，但最坏列会随 warm-up 设置和重复初始化状态发生漂移：例如 `WARMUP_BYTES=8` 的最坏位置为 `byte 2, bit 2`，`X=721`；`WARMUP_BYTES=10` 的两次运行分别落在 `byte 1, bit 4` 与 `byte 6, bit 0`；通过边界后的 `WARMUP_BYTES=11/12` 虽仍可定义最坏列，但其 `X_max` 已低于 cutoff。MSB/LSB 对照进一步表明，观察到的是可映射回原始 packed byte 内固定 bit 位置的列偏置，位序展开只是观察口径，不是偏置的充分解释。

该机制解释也与 placement 级别的辅助观测相一致。对 `random3`，连续流 TRNG bit min-entropy mean 约为 `0.999916694`，RO 数据振荡器中最近的数据-数据频差约为 `0.673 MHz`，TDC 观测包含 3 个 pair；这些指标提示当前 placement 在连续流条件下表现较好，但 restart 初期仍可能受初始化相位、RO 频差/placement 耦合和早期采样窗口共同影响。作为对照，`random1` 在相同 restart 口径下的 continuous-flow TRNG bit min-entropy mean 较低（约 `0.594376522`），且 formal pass/fail 又受 sequential 熵估计与 cutoff 共同影响。因此，本文不把 random1/random3 的差异写成单一优劣判断，而将其作为 restart 固定列偏置、连续流熵估计和 placement 机制之间并不等价的证据。

从熵估计边界看，`WARMUP_BYTES=11` 虽已通过 restart sanity check，但其 restart min-entropy margin 仍较窄：run01 中 MSB/LSB min-entropy 分别为 `0.743385` 与 `0.753865`，repeat02 中分别为 `0.765014` 与 `0.746636`。`WARMUP_BYTES=12` 的两次运行给出更宽的观察裕量，MSB min-entropy 分别约为 `0.849807` 和 `0.813237`，LSB 侧均不低于 `0.828444`。因此，论文中可将 warmup11 表述为当前条件下的边界通过点，将 warmup12 或 warmup16 表述为同一条件下具有更宽 restart margin 的观测点，而不宜把 warmup11 称为工程上充分的最终配置。

综上，restart 实验揭示了三个结果。第一，在当前板卡与 placement 中，连续流近均衡并不能排除 restart 后固定列偏置；未 warm-up 或 warm-up 不足时，formal-size restart sanity check 仍会失败。第二，warm-up 扫描显示偏置窗口可被移出被观测的 restart 输出矩阵，并在重复实验中给出一致的边界：`WARMUP_BYTES=10` 失败，`WARMUP_BYTES=11/12` 通过。第三，该现象更适合被解释为 restart 初始相位和早期固定采样窗口相关的实验性证据，而非完整认证结论或跨实现的通用 warm-up 阈值。后续若要形成更强结论，仍需跨板卡、跨 bitstream/placement、跨 PVT 条件和更多重复采集来验证该边界的稳定性。

## 建议论文表格

| WARMUP_BYTES | repeat | overall p1 | positions over cutoff | worst byte.bit | worst X | worst p1 | MSB status | MSB Xmax/cutoff | MSB min-H | LSB status | LSB Xmax/cutoff | LSB min-H | 建议解释 |
| ---: | --- | ---: | ---: | --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| 0 | run01 | 0.497933 | 1 | 0.0 | 685 | 0.315 | Fail | 685/605 | NA | Fail | 685/605 | NA | no-warmup fixed-column bias |
| 8 | run01 | 0.374385 | 893 | 2.2 | 721 | 0.279 | Fail | 721/605 | NA | Fail | 721/632 | NA | stronger biased window |
| 10 | run01 | 0.415017 | 106 | 1.4 | 650 | 0.350 | Fail | 650/605 | NA | Fail | 650/632 | NA | pre-transition fail |
| 10 | repeat02 | 0.415849 | 89 | 6.0 | 633 | 0.367 | Fail | 633/605 | NA | Fail | 633/632 | NA | repeated fail near boundary |
| 11 | run01 | 0.469088 | 0 | 1.3 | 583 | 0.417 | Pass | 583/605 | 0.743385 | Pass | 583/632 | 0.753865 | boundary pass |
| 11 | repeat02 | 0.469261 | 0 | 68.3 | 588 | 0.412 | Pass | 588/605 | 0.765014 | Pass | 588/632 | 0.746636 | repeated boundary pass |
| 12 | run01 | 0.499478 | 0 | 88.3 | 562 | 0.562 | Pass | 562/605 | 0.849807 | Pass | 562/632 | 0.828444 | wider margin |
| 12 | repeat02 | 0.499506 | 0 | 118.1 | 549 | 0.451 | Pass | 556/605 | 0.813237 | Pass | 556/632 | 0.828444 | repeated wider margin |
| 16 | run01 | 0.499126 | 0 | 43.7 | 547 | 0.547 | Pass | 549/605 | 0.868735 | Pass | 549/632 | 0.820090 | farther warm-up pass |

注：上表将 MSB cutoff 记为 `605`、LSB cutoff 记为 `632`，与机制关联表中的 formal `ea_restart` 口径一致。若最终论文主表采用 warmup transition CSV 中的统一 cutoff 展示口径，应在投稿前从归档 `ea_restart` stdout 复核并统一 cutoff 来源。

## 建议图注

图 X. Warm-up bytes 对 restart 固定列偏置的影响。横轴为每次 restart 后丢弃的 packed bytes 数，左纵轴为最坏固定位置计数 `X_max`，右纵轴为超过 restart cutoff 的固定位置数。`WARMUP_BYTES=0, 8, 10` 时仍存在超过 cutoff 的固定采样位置，其中 warmup8 暴露出更强且更广泛的偏置；从 `WARMUP_BYTES=11` 开始，超过 cutoff 的位置数降为 0，MSB/LSB formal-size restart sanity check 均通过。该图展示的是本板、本 placement、本 auto-stream restart protocol 下的 warm-up transition，而非跨芯片、跨 placement 或跨 PVT 的通用阈值。

## 建议审稿风险措辞

1. 避免写成“通过 SP800-90B 认证”。建议写成“在本实验条件下通过 `ea_restart` restart sanity check”。
2. 避免写成“warmup11 是通用阈值”。建议写成“在本板、本 placement、本 auto-stream restart protocol 下，观测到通过边界位于 `10 < WARMUP_BYTES <= 11`”。
3. 避免把 warmup8 失败解释为采集链路错误。更稳妥的表述是“warm-up 改变了 restart 后被观察的相位/状态窗口，并可能暴露不同的强偏置窗口”。
4. 避免声称 MSB/LSB 位序导致或消除了现象。建议写成“MSB/LSB 对照排除了单纯位序展开造成假象的解释，偏置可映射回原始 packed byte 内固定 bit 位置”。
5. 对机制解释使用“支持”“提示”“一致于”，避免“证明”。当前数据支持 restart 初始相位、RO 频差/placement 耦合与早期采样窗口相关的解释，但仍需更多重复、PVT 和设计级可观测量排除其他因素。
