# Restart warmup 论文素材（2026-05-15）

## 1. 可直接进论文的中文结果段落

为检验 restart 后早期固定采样位置是否存在可重复偏置，本文在 `random3` placement 上采用 auto-stream design-level restart 协议构造 formal-size bit-symbol restart matrix。每个数据集包含 1000 次 restart，每次 restart 输出 125 个 packed bytes，并按 MSB/LSB 两种位序展开为 1000 个 one-byte bit symbols 后输入 `ea_restart`。在未丢弃 restart 后早期 packed bytes 时，整体 1 比例接近均衡（`p1=0.497933`），但固定列上仍出现强偏置，最坏位置为原始 `byte 0, bit 0`，`X_max=685`，超过 `X_cutoff=605`，导致 restart sanity check 失败。这说明连续流 sequential non-IID 熵估计不能单独覆盖 restart 初始相位或早期固定输出位置的稳定性风险。

进一步的 warmup 扫描显示，简单丢弃少量早期 packed bytes 并不必然改善 restart 行为。`WARMUP_BYTES=8` 时，overall `p1` 下降至 `0.374385`，超过 cutoff 的位置数增至 893，最坏固定位置达到 `X_max=721`，MSB/LSB restart 均失败；`WARMUP_BYTES=10` 时偏置有所缓和，但仍有 106 个位置超过 cutoff，最坏位置 `X_max=650`，仍未通过 restart sanity check。相反，当 warmup 增加到 11 packed bytes 后，超过 cutoff 的位置数降为 0，最坏位置 `X_max=583`，MSB 与 LSB 均通过；`WARMUP_BYTES=12` 与 `16` 也保持通过，且 overall `p1` 分别回到 `0.499478` 与 `0.499126`。在本板、本 placement、本 auto-stream restart 协议下，观测到的通过边界收窄为 `10 < WARMUP_BYTES <= 11`。

这些结果支持一个更谨慎的机制解释：restart 后前若干 packed bytes 处于不稳定或强偏置窗口，偏置热点集中在固定采样位置，但最强热点会随 warmup 设置或重新初始化状态发生漂移。足够的 warmup 可在该实验条件下移出早期偏置窗口，使 formal-size restart sanity check 通过；然而，warmup8 的负结果也表明，warmup 不是可凭经验任意选取的补救措施，而应作为需要系统扫描和审计记录的实验变量。

从熵估计角度看，`WARMUP_BYTES=11` 通过时 MSB/LSB 的 restart min-entropy 分别为 `0.743385` 与 `0.753865`，低于 `WARMUP_BYTES=12` 的 `0.849807`/`0.828444` 以及 `WARMUP_BYTES=16` 的 `0.868735`/`0.820090`。因此，warmup11 可作为当前边界点证据，而 warmup12/16 更适合表述为在相同条件下具有更宽裕 restart margin 的观测点。论文中不宜将单次 formal-size 通过写成最终 SP800-90B 认证结论，而应写成对 restart 初期相位风险和 warmup 缓解窗口的实验性证据。

## 2. 建议表格字段

建议表题：不同 warmup 设置下 `random3` formal-size restart sanity check 的转折行为。

| 字段 | 含义 | 建议展示格式 |
| --- | --- | --- |
| `WARMUP_BYTES` | 每次 restart 后丢弃的 packed bytes 数 | 整数：0, 8, 10, 11, 12, 16 |
| `Packed SHA256` | row-major packed restart matrix 的完整性标识 | 截断显示前 8-12 hex，脚注给完整值或数据归档路径 |
| `Overall p1` | 展开前/诊断口径下的整体 1 比例 | 小数 6 位 |
| `Positions over cutoff` | 超过 restart cutoff 的固定位置数 | 整数 |
| `Worst byte.bit` | 最坏原始 packed byte 和 bit 位置 | 例如 `1.3` |
| `Worst X` | 最坏固定位置上的最大 0/1 计数 | 整数 |
| `Worst p1` | 最坏位置的 1 比例 | 小数 3 位 |
| `MSB status` | MSB 展开位序下的 `ea_restart` 结果 | `Pass`/`Fail` |
| `MSB Xmax / cutoff` | MSB 结果的最坏计数与 cutoff | `583 / 605` |
| `MSB min-entropy` | MSB restart 输出熵下界 | 失败时留空或标注 NA |
| `LSB status` | LSB 展开位序下的 `ea_restart` 结果 | `Pass`/`Fail` |
| `LSB Xmax / cutoff` | LSB 结果的最坏计数与 cutoff | `583 / 632` 或按实际 LSB cutoff |
| `LSB min-entropy` | LSB restart 输出熵下界 | 失败时留空或标注 NA |
| `Interpretation` | 对该 warmup 点的简短解释 | `early biased window`, `boundary pass`, `stable pass` |

可直接填表的核心数据如下：

| WARMUP_BYTES | Overall p1 | Positions over cutoff | Worst byte.bit | Worst X | Worst p1 | MSB status | MSB Xmax/cutoff | MSB min-H | LSB status | LSB Xmax/cutoff | LSB min-H |
| ---: | ---: | ---: | --- | ---: | ---: | --- | --- | ---: | --- | --- | ---: |
| 0 | 0.497933 | 1 | 0.0 | 685 | 0.315 | Fail | 685/605 | NA | Fail | 685/605 | NA |
| 8 | 0.374385 | 893 | 2.2 | 721 | 0.279 | Fail | 721/605 | NA | Fail | 721/605 | NA |
| 10 | 0.415017 | 106 | 1.4 | 650 | 0.350 | Fail | 650/605 | NA | Fail | 650/605 | NA |
| 11 | 0.469088 | 0 | 1.3 | 583 | 0.417 | Pass | 583/605 | 0.743385 | Pass | 583/605 | 0.753865 |
| 12 | 0.499478 | 0 | 88.3 | 562 | 0.562 | Pass | 562/605 | 0.849807 | Pass | 562/605 | 0.828444 |
| 16 | 0.499126 | 0 | 43.7 | 547 | 0.547 | Pass | 549/605 | 0.868735 | Pass | 549/605 | 0.820090 |

注：汇总表中 LSB cutoff 字段与机制关联表中的 LSB formal cutoff 口径存在差异；若论文最终表同时展示 MSB/LSB，应以最终 `ea_restart` stdout 或归档结果目录为准统一口径。当前 warmup transition CSV 给出的 MSB/LSB cutoff 均为 605，可用于内部素材，但投稿表格建议在复核后定稿。

## 3. 建议图 caption

图 X. Restart warmup 对固定位置偏置的影响。横轴为每次 restart 后丢弃的 packed bytes 数，左纵轴为最坏固定位置计数 `X_max`，右纵轴为超过 restart cutoff 的位置数；虚线表示 MSB restart sanity cutoff。`WARMUP_BYTES=0,8,10` 时仍存在超过 cutoff 的固定采样位置，其中 warmup8 暴露出更强且更广泛的偏置；从 `WARMUP_BYTES=11` 开始，超过 cutoff 的位置数降为 0，MSB/LSB formal-size restart sanity check 均通过。该图展示的是本板、本 placement、本 auto-stream restart 条件下的 warmup 转折，而非跨芯片或跨 PVT 的通用阈值。

## 4. 审稿风险和谨慎措辞

1. 不要写成“通过 SP800-90B 认证”。当前结果是指定板卡、指定 placement、指定 auto-stream restart 协议、指定 warmup 设置下的 formal-size restart sanity check 结果。建议措辞为“通过本实验条件下的 `ea_restart` sanity check”。

2. 不要写成“warmup 11 bytes 是通用阈值”。建议写为“在本板、本 placement、本次 auto-stream restart 条件下，观测到通过边界位于 `10 < WARMUP_BYTES <= 11`；该阈值仍需跨板卡、跨 bitstream、跨 PVT 和重复实验确认”。

3. 不要把 warmup8 的失败解释为采集链路错误。CSV 与执行状态均显示该点是 formal-size 数据集上的负结果，更稳妥的表述是“warmup 改变了 restart 后被观察的相位/状态窗口，并可能暴露新的强偏置窗口”。

4. 不要声称 MSB/LSB 位序导致或消除了现象。未 warmup 与 repeat 结果显示异常可映射回原始 packed byte 内的固定物理 bit 位置，位序展开只是观察口径。建议写为“MSB/LSB 对照排除了单纯位序展开造成假象的解释”。

5. 对 random1/random3 对照应避免价值判断过强。`random1` 通过 restart sanity check 的一部分原因是 sequential non-IID `H_I` 较低导致 cutoff 更宽；但其 restart 初期固定位置偏置仍存在。建议写为“formal pass/fail 与 sequential 熵估计、cutoff 及 restart 矩阵固定列偏置共同相关”。

6. 对机制解释使用“支持”“提示”“一致于”，避免“证明”。当前数据支持 restart 初始相位、RO 频差/placement 耦合与早期采样窗口相关的解释，但仍需要更多重复、PVT 和设计级可观测量来排除其他因素。

7. 表格中的 cutoff 和 min-entropy 应在投稿前从最终 `ea_restart` 归档 stdout 复核。尤其是 LSB cutoff 在不同汇总表中可能有 605 与 632 两种口径，最终论文应保持同一计算来源。

## 核心结论

`random3` 的 formal-size restart warmup 扫描显示：不 warmup、warmup8、warmup10 均失败；warmup11、warmup12、warmup16 均通过。在当前实验条件下，restart 初期至少前若干 packed bytes 可视为不稳定/偏置窗口，且通过边界被观测在 `10 < WARMUP_BYTES <= 11`。该结论适合写成 restart 初始相位风险与 warmup 缓解效果的实验素材，但不应扩展为最终认证或通用设计阈值。
