# 论文主张、证据和边界 2026-05-25

## 核心写法

建议论文主张写成：

> RO-TRNG 的 placement 敏感性不仅来自 RO 阵列本身，也来自采样端物理实现。sample RO、采样寄存器、局部路由和采样孔径应被视为熵源边界的一部分。TDC 结果排除了简单 pairwise hard locking 作为主导解释，而 sample RO 双向反事实实验提供了最强的因果证据。

不建议写成：

> bad placement causes RO hard locking。

这个写法太窄，而且与 clean TDC 结果不一致。

## Claim-Evidence-Boundary 表

| 论文主张 | 当前证据 | 证据强度 | 可写程度 | 不能过度声称 |
| --- | --- | --- | --- | --- |
| placement 会显著影响 RO-TRNG 输出质量 | 10/20 MiB placement repeats、random1/random3/compact/checker/sparse/far 等结果 | 强 | 正文主结果 | 不能只展示两个极端例子，要给 spectrum |
| sample RO 是熵源边界的一部分 | sample RO forward fail 和 reverse repair 双向反事实 | 强 | 核心创新点 | 不能说只有 sample RO 起作用，sampling regs/routing 也可能参与 |
| bad placement 不是简单 pairwise hard locking | clean reset-aligned TDC same-bin ratio 约 1%、longest run 3、autocorr 接近 0 | 中强，偏排除性 | 机制约束结果 | 不能说完全不存在任何耦合 |
| warmup 改变 restart 固定位置偏置 | SP800-90B restart / column-bias / warmup transition | 强 | 正文机制结果 | 不能把连续流非 IID 指标等同于 restart 安全 |
| sampler-local placement 可能改善 startup phase diffusion | clean32k TDC 中 sampler-local warmup12 指标最高 | 弱到中 | Discussion 或辅助机制 | 不能作为唯一因果证明 |
| XADC 条件没有明显异常漂移 | 新采集 after-only XADC 大约 46-47 C，VCCINT 约 1.000 V | 中 | 实验条件说明 | 旧数据缺失 XADC，不能补称 |
| TDC 可用于相位/抖动机制推断 | raw-bin / code-density-normalized TDC 指标 | 中 | 相对比较 | 没有独立 calibration 前不能写 ps 级绝对 jitter |
| 结果可跨板推广 | 暂无多板 | 弱 | 只能列 limitation | 多板前不能声称普适 |

## 最强结果应该怎么写

### sample RO 双向反事实

推荐表述：

```text
By changing only the physical implementation of the sample RO, the restart warmup passband can be either destroyed or repaired. This bidirectional counterfactual indicates that the sampler-side implementation is not a passive readout path, but part of the physical entropy-source boundary.
```

中文解释：

```text
只改变 sample RO 的物理实现，就能把原本接近理想的 compact passband 拉成强偏置，也能把 formal warmup4 的失败修到接近理想。这比相关性分析更强，因为它形成了双向反事实闭环。
```

### TDC 机制定位

推荐表述：

```text
The clean reset-aligned TDC matrix does not show persistent same-bin residence or small-lag autocorrelation, which argues against simple pairwise RO hard locking as the dominant mechanism. The TDC result therefore constrains the mechanism rather than serving as the sole causal proof.
```

中文解释：

```text
TDC 的主要价值是排除“坏 placement 就是 RO-RO 硬锁定”这种过度简单的解释。它让论文机制更准确：问题更可能出在 sampler-side phase relation、采样孔径、寄存器和局部路由，而不是两个 RO 长时间锁死。
```

## 审稿风险和回应

| 风险 | 可能审稿意见 | 回应策略 |
| --- | --- | --- |
| 单板 | 只有一块板，是否偶然？ | 承认 single-board mechanistic study；多板补采作为高水平投稿前 P0 |
| TDC calibration | TDC bin 非线性，不能代表真实时间 | 所有当前 TDC 只写 raw-bin relative；不写 ps 级绝对量 |
| auto-stream | XADC/JTAG 会不会错过 header？ | 已发现并记录；后续 after-only 或 command-gated；已有完整 capture 带 header/SHA256 |
| cherry-picking | 是否只挑了好看的 placement？ | 给完整 placement matrix、repeat、ranking 和失败例 |
| SP800-90B | 是否完成了认证？ | 写 entropy assessment/restart evidence，不写完整认证 |
| RTL 版本 | 每次实验代码是否可复现？ | 用 reproduce doc、bitstream SHA256、capture SHA256、脚本入口和 git snapshot 管理 |

## 下一阶段可以产生的论文贡献

无多板阶段：

1. 完整图表包；
2. claim/evidence/limitation 表；
3. command-gated 和 TDC calibration 设计；
4. 中文/英文初稿 results 和 discussion。

多板恢复后：

1. sample RO 双向反事实跨板复现；
2. TDC calibration；
3. command-gated before/after XADC；
4. placement matrix 统计置信度补强。

