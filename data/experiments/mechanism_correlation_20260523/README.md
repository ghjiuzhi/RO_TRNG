# Mechanism Correlation Audit 20260523

Offline-only audit of existing restart mechanism-correlation artifacts.

## Inputs

- existing restart mechanism link: `data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.csv`
- restart result summary: `data/experiments/restart_summary_20260515/restart_result_summary_20260522.csv`
- TRNG placement metrics: `data/experiments/paper_artifacts_20260514/table_placement_trng_repeats.csv`
- RO_FREQ random1/random3 features: `data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv`
- TDC pair dynamics summary: `data/experiments/paper_artifacts_20260514/table_tdc_pair_dynamics_summary.csv`

## Existing table coverage

| group | present / required columns | missing columns | populated cells | coverage |
| --- | ---: | --- | ---: | ---: |
| restart worst columns | 6 / 6 |  | 66 / 66 | 1 |
| TRNG entropy | 3 / 3 |  | 33 / 33 | 1 |
| RO_FREQ | 3 / 3 |  | 33 / 33 | 1 |
| TDC | 3 / 3 |  | 33 / 33 | 1 |

## Normalized restart summary

- Rows exported: `44` restart rows.
- Placements exported: `checker, compact, random1, random3, same_column, sparse`.
- TRNG placement metrics are available for all exported placements.
- RO_FREQ and TDC mechanism metrics are currently matched for `random1` and `random3` only.

| placement | restart rows | failed | passed | x_max mean | TRNG bit Hmin | RO min delta MHz | TDC pairs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| checker | 4 | 2 | 2 | 624.5 | 0.999795837 |  |  |
| compact | 4 | 2 | 2 | 638 | 0.999849695 |  |  |
| random1 | 6 | 0 | 6 | 591.333333 | 0.593605945 | 0.46619470080861447 | 6 |
| random3 | 22 | 8 | 14 | 603 | 0.999909299 | 0.6733958183129403 | 6 |
| same_column | 4 | 2 | 2 | 752.5 | 0.99979876 |  |  |
| sparse | 4 | 2 | 2 | 715 | 0.900637067 |  |  |

## Conclusion

- The existing `table_restart_mechanism_link.csv` already combines restart worst-column fields, TRNG entropy fields, RO_FREQ features, and TDC summaries.
- Its current populated rows cover `random1`/`random3`; the normalized export keeps the broader restart-summary rows and makes missing RO_FREQ/TDC coverage explicit.
- Treat the combined evidence as a case-comparison table, not a statistically significant correlation analysis.
