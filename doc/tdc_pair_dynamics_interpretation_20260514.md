# TDC Pair Dynamics Interpretation 20260514

This note is based only on completed offline TDC pair data in `data/hardware/20260511_fpga1_board1/tdc_pairs/analysis_*`.

## Key Result

- Maximum absolute zero-lag window phase correlation: `0.063178`.
- Maximum absolute small-lag window phase correlation: `0.0836128`.
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
