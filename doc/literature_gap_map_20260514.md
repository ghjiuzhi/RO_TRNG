# Literature Gap Map 2026-05-14

用途：给论文引言、相关工作和贡献边界使用。这里不是完整文献综述，而是把当前实验能打的位置讲清楚。

## 必须对齐的标准

NIST SP 800-90B 是熵源验证必须对齐的标准，不能只用 NIST SP 800-22/STs 或简单 p-value 证明安全熵。论文中应把当前 bitstream 原始数据、90B 输入格式、IID/Non-IID 估计和重启/健康测试计划分开写。

参考：

- NIST SP 800-90B, Recommendation for the Entropy Sources Used for Random Bit Generation: https://doi.org/10.6028/NIST.SP.800-90B
- NIST 官方页面：https://www.nist.gov/publications/recommendation-entropy-sources-used-random-bit-generation-0

## 和传统 RO-TRNG 工作的差异

传统 RO-TRNG 论文通常关注：

- 提出新的 RO/TERO/SR/LRO/FiGaRO 等结构。
- 通过 XOR、采样、后处理或 DRBG 改善统计测试。
- 给出吞吐率、资源、NIST STS/AIS-31/90B 等结果。

本项目不应把“手动 placement”包装成创新点。更强的说法是：

- 固定或接近固定的 RO-TRNG 结构，在不同 placement 下表现出显著且可重复的原始随机性差异。
- 论文重点不是提出一个更花的新 TRNG 单元，而是建立 placement -> 物理测量 -> 原始随机性指标之间的可复现实验证据链。
- TDC 与 RO_FREQ 不是“装饰性测量”，而是用于约束机制假设：频率拉拽、相位漂移、jitter/bin entropy、bias、min-entropy 是否同向变化。

## 和 injection locking / coupling 文献的关系

已有工作表明 RO-TRNG 可能受到注入锁定、供电扰动、频率拉拽或 oscillator interaction 影响。我们的实验不能直接复述“近距离一定锁定”，因为当前 6 个 pair-specific TDC 结果没有观察到强锁定窗口。

更稳妥的贡献表述：

- 我们把“锁定/耦合”从口头猜想拆成可测假设。
- 当前数据支持 placement-dependent dynamic interaction 的存在，但强静态 pair locking 在本测试条件下未被 TDC 检出。
- 这反而是论文价值：它把一个常见但模糊的解释收窄了，说明随机性退化可能来自更复杂的系统级相互作用，而不是单一近邻 RO 同步。

可引用方向：

- Markettos and Moore, CHES 2009, frequency injection attack on RO-based TRNGs, DOI: https://doi.org/10.1007/978-3-642-04138-9_23
- IACR 论文 PDF：https://www.iacr.org/archive/ches2009/57470316/57470316.pdf

## 和 placement/routing 敏感性文献的关系

已有 FPGA RO 类工作会提到 placement/routing、device-dependent 或 portability 问题，但很多论文把 placement 当成实现细节，或者只做通过/不通过统计测试。

本项目可以强调：

- placement 是自变量，而不是被动实现细节。
- 使用 compact、checker、sparse、far、same_column、cross_region、random、多 seed 等矩阵化布局。
- 不只看最终 bitstream 统计，还采 RO_FREQ 与 TDC 原始物理观测。
- `same_column` 案例说明 bias 接近 0.5 也可能存在序列结构异常，因此单一统计指标不够。

可引用方向：

- Wold/Tan 一类关于 oscillator ring interaction、频率分散、相关性的工作。
- FiGaRO/FPGA TRNG 论文中关于 placement 影响和 device-dependent 的讨论。

## 当前论文最有希望的贡献句

建议主贡献写成：

1. 提出一个面向 FPGA RO-TRNG 的 placement sensitivity characterization flow，把 placement 矩阵、RO frequency probing、TDC phase/bin probing 和原始 entropy analysis 统一到同一块板上的可复现实验。
2. 证明不同 placement 会导致同一 RO-TRNG 原始输出从接近理想到严重偏置的可重复变化，例如 `random1` 与 `random3` 的强对比。
3. 发现 coarse placement label 和简单近频率 pair 都不足以解释随机性退化，必须联合 sample pulling、相位动态和序列结构指标。
4. 给出一个重要负结果：在 6 个重点 pair-specific TDC 测试中未检测到强 pair locking，因此机制应表述为 placement-dependent dynamic interaction，而不是直接宣称邻近 RO 同步。
5. 提供可复现实验脚本、bitstream 队列、metadata、hash 和后处理流程，为后续多板/温压/90B 完整验证打基础。

## 需要避免的高风险表述

- 不写“首次发现 RO placement 会影响随机性”，除非后续文献检索能证明。
- 不写“证明耦合导致熵下降”，当前证据不足。
- 不写“通过 NIST 测试所以安全”，应写“统计现象”和“90B 熵估计/合规验证仍需完成或补充”。
- 不把 TDC bin 未校准值当作绝对线性时间；需要 code-density calibration 后再讨论绝对时间含义。

