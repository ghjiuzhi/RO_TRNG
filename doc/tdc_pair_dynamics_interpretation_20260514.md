# TDC Pair Dynamics Interpretation 20260514

This note is based only on completed offline TDC pair data in `data/hardware/20260511_fpga1_board1/tdc_pairs/analysis_*`.

## Key Result

- Maximum absolute zero-lag window phase correlation: `0.0265191`.
- Maximum absolute small-lag window phase correlation: `0.0317827`.
- Conservative strong-lock windows (`|r| >= 0.5` after small-lag scan): `0`.

The present captures do not support a strong locking claim. The paper should state that the selected RO pairs were monitored with TDC phase readout, but the observed windowed phase correlations remained near zero and the differential phase spread stayed consistent with weakly coupled or effectively independent sampling under this setup.

## Suggested Paper Wording

> We did not observe evidence of strong phase locking in the tested TDC pair captures. Across fixed-size time windows, zero-lag and small-lag phase correlations stayed low, while the differential phase standard deviation remained on the order expected for two broadly distributed phase samples. Therefore, these data are treated as a negative or null observation for strong synchronization, not as proof that coupling cannot occur under other placements, supply conditions, or longer observation windows.

## Reporting Guidance

- Use this as mechanism-validation evidence, not as a positive locking result.
- Report window size, lag search range, and the fact that full-run code-density calibration was reused for all windows.
- Avoid phrases such as `locked`, `synchronized`, or `entrained` unless repeated captures show sustained high correlation and reduced differential phase variance.
- A defensible claim is: `No strong TDC-level pair locking was detected in the tested 2 MiB captures.`

## Source Tables

- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.csv`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`

## Fixed-LUT Reanalysis 2026-05-25

为避免“每个 run 自己做 code-density lookup”带来的 ps 级可比性问题，已用 dedicated calibration 生成的 fixed LUT 对全部 pair-specific TDC 重新分析。

新增脚本：

```text
scripts/analyze_tdc_pair_dynamics_with_lut_20260525.py
```

输出：

```text
data/experiments/tdc_pair_dynamics_lut_reanalysis_20260525/a7_b11/
data/experiments/tdc_pair_dynamics_lut_reanalysis_20260525/a11_b7/
```

复算结果：

| LUT | runs | windows | max small-lag `|r|` | strong-lock windows |
| --- | ---: | ---: | ---: | ---: |
| a7/b11 fixed LUT | 12 | 192 | 0.0313742149 | 0 |
| a11/b7 fixed LUT | 12 | 192 | 0.0313610782 | 0 |

解释：

- fixed-LUT 复算后，所有 pair-specific TDC 窗口仍低于 `|r| >= 0.5` 的 conservative strong-lock threshold。
- 最大 small-lag 相关仍约为 0.031，与原始 pair-specific TDC 的结论一致。
- 因此，dedicated code-density calibration 与 fixed-LUT sensitivity check 没有推翻 “No strong TDC-level pair locking was detected” 这个结论。
- 这仍是机制约束证据，而不是证明所有条件下都不存在耦合。论文应写成排除简单 hard-locking 主导解释，而不是声称 RO 之间完全无耦合。
