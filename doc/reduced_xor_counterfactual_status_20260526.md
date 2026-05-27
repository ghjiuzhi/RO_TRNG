# Reduced-XOR 反事实硬件实验状态 2026-05-26

## 目的

验证 `sampler_island_local warmup10` 的 near-cutoff 行为是否能由同一 `data_ro` 跨 8 个 sample line 的相关增强直接控制。

这不是 PC 端事后 XOR，而是新增硬件 top：

- `rtl/entropy_source_reduced_probe.v`
- `rtl/restart/RO_TRNG_restart_reduced_xor_top.v`

新 top 保留原 restart auto-stream/UART/header/row-major 流程，只替换 FIFO 输入 bit：

- `REDUCED_MODE=1`: `data_ro[j] = XOR(sampled_data[0..7][j])`
- `REDUCED_MODE=3`: `except_data_ro[j] = all64 XOR data_ro[j]`，已实现，待采集

## 已完成硬件结果

所有 capture 都是 `1000 x 125 bytes + 8-byte header`，header 均为 `A55A03E8007D01D0`。XADC 记录显示温度约 `46.1-46.3 C`，`VCCINT≈1.000 V`、`VCCAUX≈1.796-1.797 V`。

### data_ro2 reduced-XOR

| warmup | p1 | abs bias | min-H | worst X | worst p1 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.232207 | 0.267793 | 0.381211 | 885 | 0.115000 |
| 10 | 0.244002 | 0.255998 | 0.403546 | 847 | 0.153000 |
| 11 | 0.230227 | 0.269773 | 0.377495 | 863 | 0.137000 |

对应 snapshot 预测：

| warmup | snapshot data_ro2 group_xor p1 |
| ---: | ---: |
| 5 | 0.341797 |
| 10 | 0.236328 |
| 11 | 0.323242 |

硬件 `w10/data_ro2` 的 `p1=0.244002` 与 snapshot 的 `0.236328` 方向一致，证明 data_ro 方向 reduced-XOR 偏置是真实硬件输出函数可复现的，不只是 snapshot 分析伪影。但 `w5/w11 data_ro2` 也强偏，说明 `data_ro2` 不是 w10 near-cutoff 的唯一控制旋钮。

### data_ro0 reduced-XOR

| warmup | p1 | abs bias | min-H | worst X | worst p1 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.206684 | 0.293316 | 0.334032 | 992 | 0.008000 |
| 10 | 0.191877 | 0.308123 | 0.307353 | 897 | 0.103000 |
| 11 | 0.208462 | 0.291538 | 0.337269 | 914 | 0.086000 |

对应 snapshot 预测：

| warmup | snapshot data_ro0 group_xor p1 |
| ---: | ---: |
| 5 | 0.419922 |
| 10 | 0.297852 |
| 11 | 0.388672 |

`data_ro0` 三点都强偏，且 `w10` 最低。它支持 w10 的方向性异常，但也显示单一 data_ro 方向本身远比最终 all64 输出更坏。

## 当前机制判断

最初的简单假设是：

> w10 near-cutoff 由某一个 same-data-RO cross-line group 直接控制。

现在应修正为更强、更准确的机制：

> 单个 data_ro 方向的 reduced-XOR 在真实硬件输出中天然可以严重偏置；原始 all64 输出之所以接近理想，依赖多个 data_ro 方向与其 complement 之间的 XOR 抵消。warmup window 改变的不是某一个 group 是否坏，而是这些强偏 group 在最终 all64 组合中的抵消关系。`sampler_island_local w10` 贴近 cutoff，可能是组合抵消在该 startup window 变弱或相位关系改变。

因此 reduced-XOR 实验已经给出两个论文价值：

1. 证明 snapshot 里看到的 same-data-RO cross-line 结构不是纯软件分析伪影，能被硬件输出函数直接放大。
2. 证明最终 TRNG 不能只看 marginal bias 或单个 data_ro group，必须把 sampler-side combination boundary 写进熵源模型。

## 下一步

最有价值的后续反事实是 `except_data_ro`：

- `except_data_ro0 = all64 XOR data_ro0`
- `except_data_ro2 = all64 XOR data_ro2`

目标：

- 如果 `data_ro0/2` 强偏，但 `except_data_ro0/2` 以相反方向或近似互补方式抵消，说明 all64 近理想来自组合抵消；
- 如果 `w10` 的 `except_data_ro` 抵消能力弱于 w5/w11，则可直接解释 w10 near-cutoff；
- 如果 `except_data_ro` 也不分离，则机制应继续推向多组 data_ro 之间的高阶相关，而不是单组 complement。

建议最小硬件矩阵：

```text
sampler_island_local
warmup = 5,10,11
mode = except_data_ro
index = 0,2
```

相关文件：

- `data/experiments/restart_reduced_xor_w5_w10_w11_data_ro0_20260526`
- `data/experiments/restart_reduced_xor_w5_w10_w11_data_ro2_20260526`
- `data/experiments/fast_mode/hardware_queue_restart_reduced_xor_w5_w10_w11_data_ro0_20260526.csv`
- `data/experiments/fast_mode/hardware_queue_restart_reduced_xor_w5_w10_w11_data_ro2_20260526.csv`

## Update 2026-05-26: except_data_ro0 complement result

The first complement counterfactual has completed on real hardware:

`except_data_ro0 = all64 XOR data_ro0`

All captures used the same restart auto-stream protocol, `1000 x 125` bytes plus the 8-byte header. Headers were valid.

| warmup | p1 | abs bias | min-H | row ones std | worst X | worst p1 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.488326 | 0.011674 | 0.966703 | 15.794927 | 563 | 0.437 |
| 10 | 0.501020 | 0.001020 | 0.997060 | 15.997737 | 571 | 0.571 |
| 11 | 0.540569 | 0.040569 | 0.887449 | 18.178593 | 594 | 0.594 |

This is the strongest reduced-XOR result so far. The single group `data_ro0` is severely biased, while its complement is near ideal for warmup5 and warmup10 and still much better than the single group at warmup11. Therefore the original `all64` output quality cannot be explained by any one data_ro group alone. It depends on XOR cancellation between physically biased same-data-RO groups and their complements.

Revised mechanism statement:

> Same-data-RO cross-line groups can be strongly biased as real FPGA output functions. The full 64-sample XOR becomes usable only because biased groups are combined with other biased groups and complements. The warmup window changes this cancellation boundary, so `sampler_island_local w10` should be treated as a sampler-side combination/cancellation near-boundary, not as a single data_ro failure.

Immediate next experiment:

`except_data_ro2 = all64 XOR data_ro2` for warmup 5, 10, and 11. If it also restores near-ideal output, the complement/cancellation explanation becomes much stronger. If it does not, the next model should move from single-group complements to higher-order interactions among multiple data_ro groups.

## Update 2026-05-26: except_data_ro2 complement result

The second complement counterfactual has also completed on real hardware:

`except_data_ro2 = all64 XOR data_ro2`

XADC remained stable during capture: temperature `46.3-46.5 C`, `VCCINT=1.000-1.001 V`, `VCCAUX=1.796-1.797 V`, and `VCCBRAM=1.000 V`. All captures had valid `A55A03E8007D01D0` headers.

| warmup | p1 | abs bias | min-H | row ones std | worst X | worst p1 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.599459 | 0.099459 | 0.738267 | 19.267027 | 654 | 0.654 |
| 10 | 0.499674 | 0.000326 | 0.999060 | 16.104028 | 557 | 0.557 |
| 11 | 0.669279 | 0.169279 | 0.579320 | 17.756665 | 718 | 0.718 |

Comparison with `data_ro2`:

| warmup | data_ro2 p1 | except_data_ro2 p1 | interpretation |
| ---: | ---: | ---: | --- |
| 5 | 0.232207 | 0.599459 | complement is biased in the opposite direction, not enough to make the pair ideal |
| 10 | 0.244002 | 0.499674 | complement nearly cancels the biased group at the w10 boundary |
| 11 | 0.230227 | 0.669279 | complement is strongly opposite-biased, so cancellation is poor |

This is a sharper result than a simple "remove one bad group" story. `data_ro2` alone is low-biased at all three warmups, but its complement changes with warmup: near ideal at `w10`, moderately high-biased at `w5`, and strongly high-biased at `w11`. Therefore the warmup passband is governed by how biased data_ro-direction groups combine, not by the marginal quality of a single group.

Paper-facing mechanism update:

> The reduced-XOR hardware counterfactuals show that same-data-RO directions are real biased hardware functions. However, full-output quality is controlled by warmup-dependent XOR cancellation between biased directions and their complements. The near-cutoff `w10` behavior is therefore a sampler-side combination boundary: the sampled-bit correlation structure determines whether biased local groups cancel or reinforce.

Next control:

Build and capture `REDUCED_MODE=all64` for warmup `5,10,11` in the same reduced-probe top. This checks whether the reduced-probe top reproduces the original all64 passband closely enough for strict comparisons.

## Update 2026-05-26: all64 same-top control

The same `RO_TRNG_restart_reduced_xor_top` was also run in `REDUCED_MODE=all64` for warmup 5, 10, and 11. This is a control for whether the reduced-probe RTL/top changes the all64 behavior enough to invalidate the counterfactuals.

All captures completed with valid headers and stable XADC readings around `46.6-46.8 C`.

| warmup | all64 p1 | abs bias | min-H | row ones std | worst X | worst p1 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.499323 | 0.000677 | 0.998048 | 16.052124 | 560 | 0.440 |
| 10 | 0.458617 | 0.041383 | 0.885279 | 16.927738 | 590 | 0.410 |
| 11 | 0.470488 | 0.029512 | 0.917265 | 15.721764 | 584 | 0.416 |

Interpretation:

- The same-top all64 control remains much closer to ideal than `data_ro0` and `data_ro2`, so the reduced-XOR top is not simply broken.
- The reduced-probe top shows a mild low-bias at w10/w11. This is acceptable for the counterfactual claim because the single-group outputs are far more biased, and complements can move the output in either direction.
- The all64 control strengthens the claim that final output quality is a combination/cancellation property of the sampler-side sampled-bit vector.

Condensed counterfactual table:

| warmup | all64 | data_ro0 | except_ro0 | data_ro2 | except_ro2 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.499323 | 0.206684 | 0.488326 | 0.232207 | 0.599459 |
| 10 | 0.458617 | 0.191877 | 0.501020 | 0.244002 | 0.499674 |
| 11 | 0.470488 | 0.208462 | 0.540569 | 0.230227 | 0.669279 |

Current conclusion:

> Single same-data-RO directions are strongly biased. Their complements are not uniformly ideal; instead, complement behavior is warmup-dependent and can either cancel or reinforce the single-direction bias. The all64 output is therefore an emergent XOR-combination result over the sampler-side sampled-bit correlation structure.

Recommended next hardware sweep:

Scan all `data_ro[j]` and `except_data_ro[j]` for `j=0..7` at warmup10 first. Warmup10 is the most valuable boundary point, and a full direction map will show whether `ro0/ro2` are special or part of a broader alternating/complement structure. Only after the w10 direction map should we decide whether to extend all eight directions to warmup5 and warmup11.

## Update 2026-05-26: warmup10 full direction map

The warmup10 direction map has completed on real hardware. This combines:

- same-top `all64`;
- all `data_ro[0..7]`;
- all `except_data_ro[0..7] = all64 XOR data_ro[j]`.

All new captures completed successfully with valid restart headers. During the missing-direction queue, XADC ranged from `43.1 C` to `46.0 C`, with `VCCINT=1.000-1.001 V`, `VCCAUX=1.797-1.798 V`, and `VCCBRAM=1.000 V`.

Combined table: `data/experiments/restart_reduced_xor_w10_direction_map_20260526/summary/w10_direction_map_combined.csv`

| mode | data_ro | p1 | abs bias | min-H | row ones std | worst byte.bit | worst X | worst p1 |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| all64 | all | 0.458617 | 0.041383 | 0.885279 | 16.927738 | 83.7 | 590 | 0.410 |
| data_ro | 0 | 0.191877 | 0.308123 | 0.307353 | 7.764398 | 0.6 | 897 | 0.103 |
| data_ro | 1 | 0.518915 | 0.018915 | 0.946430 | 6.529608 | 1.3 | 632 | 0.368 |
| data_ro | 2 | 0.244002 | 0.255998 | 0.403546 | 9.811014 | 1.3 | 847 | 0.153 |
| data_ro | 3 | 0.671833 | 0.171833 | 0.573825 | 11.445834 | 2.5 | 804 | 0.804 |
| data_ro | 4 | 0.424639 | 0.075361 | 0.797461 | 8.340304 | 1.5 | 807 | 0.193 |
| data_ro | 5 | 0.409454 | 0.090546 | 0.759879 | 6.594079 | 0.6 | 806 | 0.194 |
| data_ro | 6 | 0.375380 | 0.124620 | 0.678949 | 9.667347 | 0.1 | 839 | 0.161 |
| data_ro | 7 | 0.549958 | 0.049958 | 0.862607 | 7.478251 | 1.2 | 644 | 0.644 |
| except_data_ro | 0 | 0.501020 | 0.001020 | 0.997060 | 15.997737 | 12.5 | 571 | 0.571 |
| except_data_ro | 1 | 0.550312 | 0.050312 | 0.861678 | 17.376727 | 83.3 | 597 | 0.597 |
| except_data_ro | 2 | 0.499674 | 0.000326 | 0.999060 | 16.104028 | 121.7 | 557 | 0.557 |
| except_data_ro | 3 | 0.553930 | 0.053930 | 0.852224 | 18.397801 | 3.3 | 603 | 0.603 |
| except_data_ro | 4 | 0.520205 | 0.020205 | 0.942848 | 15.844336 | 68.5 | 570 | 0.570 |
| except_data_ro | 5 | 0.565521 | 0.065521 | 0.822347 | 17.326441 | 122.5 | 620 | 0.620 |
| except_data_ro | 6 | 0.501833 | 0.001833 | 0.994721 | 15.984027 | 111.3 | 556 | 0.556 |
| except_data_ro | 7 | 0.542602 | 0.042602 | 0.882034 | 17.085655 | 6.2 | 598 | 0.598 |

Key finding:

> The eight same-data-RO directions have a clear directional bias map: `data_ro0` and `data_ro2` are strongly low-biased, `data_ro3` is strongly high-biased, and the other directions range from near-ideal to moderately low/high. Yet several complements, especially `except_data_ro0`, `except_data_ro2`, and `except_data_ro6`, are almost exactly balanced. This proves that warmup10 all64 behavior is not controlled by one bad group. It is an XOR-cancellation result over a structured, direction-dependent sampler vector.

Paper-level claim strengthened:

> Placement and warmup shape a vector entropy source at the sampler boundary. Individual sampled directions can be poor entropy sources, but their combination can be good when biased directions cancel. The entropy-source boundary must therefore include the sampler RO, sampled registers, local routing, and XOR combining path.

Recommended next step:

Run a minimal repeat for `w10` on the most diagnostic modes only: `all64`, `data_ro0`, `data_ro2`, `data_ro3`, `except_data_ro0`, `except_data_ro2`, and `except_data_ro6`. This repeat tests reproducibility of the direction-map mechanism without wasting board time on a full re-sweep.

## Update 2026-05-27: minimal repeat confirms mechanism

The minimal repeat queue has completed on real hardware:

- `all64`
- `data_ro0`, `data_ro2`, `data_ro3`
- `except_data_ro0`, `except_data_ro2`, `except_data_ro6`

All captures completed with valid headers. XADC during repeat02 was `42.0-44.9 C`, `VCCINT=1.000 V`, `VCCAUX=1.796-1.797 V`, `VCCBRAM=1.000 V`.

Repeat comparison table:

`data/experiments/restart_reduced_xor_w10_direction_repeat02_minimal_20260526/summary/w10_direction_repeat_compare_wide.csv`

| mode | data_ro | p1 run01 | p1 run02 | delta p1 | abs bias run01 | abs bias run02 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all64 | all | 0.458617 | 0.443194 | -0.015423 | 0.041383 | 0.056806 |
| data_ro | 0 | 0.191877 | 0.187682 | -0.004195 | 0.308123 | 0.312318 |
| data_ro | 2 | 0.244002 | 0.244767 | 0.000765 | 0.255998 | 0.255233 |
| data_ro | 3 | 0.671833 | 0.670937 | -0.000896 | 0.171833 | 0.170937 |
| except_data_ro | 0 | 0.501020 | 0.499872 | -0.001148 | 0.001020 | 0.000128 |
| except_data_ro | 2 | 0.499674 | 0.500863 | 0.001189 | 0.000326 | 0.000863 |
| except_data_ro | 6 | 0.501833 | 0.501224 | -0.000609 | 0.001833 | 0.001224 |

Reproducibility conclusion:

> The most diagnostic reduced-XOR effects are reproducible. `data_ro0` and `data_ro2` remain strongly low-biased, `data_ro3` remains strongly high-biased, and the complements `except_data_ro0/2/6` remain almost perfectly balanced. This confirms that the w10 mechanism is not a one-off capture artifact. The stable result is directional sampler-vector bias plus XOR-complement cancellation.

This is now a paper-grade hardware mechanism result. Further full sweeps should be driven by a specific paper question, not by repetition. The next useful work is figure/table generation and integrating this result with the sampler snapshot pairwise-correlation and TDC exclusion evidence.

## Update 2026-05-27: paper artifacts and evidence chain integration

Reduced-XOR has now been integrated into the paper-facing artifact flow.

Generated artifacts:

- `scripts/make_reduced_xor_paper_artifacts_20260527.py`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_direction_paper.csv`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_direction_paper.md`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_direction_bias.png`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_direction_bias.svg`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_repeat_paper.csv`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_repeat_paper.md`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_repeat_p1.png`
- `data/experiments/reduced_xor_paper_artifacts_20260527/reduced_xor_w10_repeat_p1.svg`

The mechanism evidence chain script now includes two reduced-XOR rows:

- `reduced_xor_w10_direction_map_data_ro_bias`
- `reduced_xor_w10_complement_cancellation`

Updated files:

- `scripts/make_mechanism_evidence_chain_20260525.py`
- `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.csv`
- `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`
- `doc/paper_draft_cn_v3_20260525.md`

Paper draft integration:

- Added `### 4.6 reduced-XOR 硬件反事实验证 sampler-vector 组合边界`.
- Updated the abstract, contribution list, discussion, design implications, limitations, next steps, conclusion, and reproduction appendix.

Current experiment-management decision:

> On the current single board, the reduced-XOR mechanism is no longer bottlenecked by more blind repetition. The next hardware work should be question-driven: multi-board reproduction of the minimal diagnostic set, or a small neighboring-warmup control if the paper needs to connect the XOR-cancellation boundary more directly to the passband window.

Recommended next hardware set when another board is available:

```text
sampler_island_local warmup10
mode = all64, data_ro0, data_ro2, data_ro3, except_data_ro0, except_data_ro2, except_data_ro6
capture = 1000 x 125 bytes + 8-byte header
record = XADC before/after if command-gated capture is available, otherwise after-only metadata
```

Optional same-board set only if the paper needs a stronger warmup-window story:

```text
sampler_island_local warmup5 and warmup11
mode = all64, data_ro0, data_ro2, data_ro3, except_data_ro0, except_data_ro2
purpose = distinguish stable direction bias from warmup-dependent complement cancellation
```
