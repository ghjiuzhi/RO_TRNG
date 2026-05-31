# Board2 second held-out sample_ro_local W10 reduced-XOR map

Status: complete; observed 17/17 expected run01 full-map conditions.

Context: random1 data-RO matrix with sample-RO constrained near the local sampler region (`sample_ro_local`). This is used as the second held-out context for frozen-prediction validation.

Aggregate all640 run01: p1=0.500040, abs_bias=0.000040, min-H=0.999885.

Independent XOR from eight data_ro contributors predicts p1=0.499999; measured all640 p1=0.500040; residual=+0.000041.

Strongest low contributor: ro0 p1=0.264807. Strongest high contributor: ro4 p1=0.553844.

## Full Map

| kind | index | p1 | signed bias | min-H | first held-out p1 | delta | worst bit p1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| all640 | all | 0.500040 | +0.000040 | 0.999885 | 0.500718 | -0.000678 | 0.554 |
| data_ro | 0 | 0.264807 | -0.235193 | 0.443805 | 0.303427 | -0.038620 | 0.090 |
| data_ro | 1 | 0.434643 | -0.065357 | 0.822766 | 0.456671 | -0.022028 | 0.353 |
| data_ro | 2 | 0.279127 | -0.220873 | 0.472183 | 0.431770 | -0.152643 | 0.153 |
| data_ro | 3 | 0.413600 | -0.086400 | 0.770043 | 0.658159 | -0.244559 | 0.209 |
| data_ro | 4 | 0.553844 | +0.053844 | 0.852448 | 0.396274 | +0.157570 | 0.687 |
| data_ro | 5 | 0.388732 | -0.111268 | 0.710123 | 0.273096 | +0.115636 | 0.209 |
| data_ro | 6 | 0.266048 | -0.233952 | 0.446242 | 0.344886 | -0.078838 | 0.067 |
| data_ro | 7 | 0.518448 | +0.018448 | 0.947729 | 0.577178 | -0.058730 | 0.769 |
| except_data_ro | 0 | 0.498802 | -0.001198 | 0.996547 | 0.691067 | -0.192265 | 0.547 |
| except_data_ro | 1 | 0.626670 | +0.126670 | 0.674222 | 0.499526 | +0.127144 | 0.690 |
| except_data_ro | 2 | 0.510841 | +0.010841 | 0.969054 | 0.731959 | -0.221118 | 0.598 |
| except_data_ro | 3 | 0.499979 | -0.000021 | 0.999939 | 0.499791 | +0.000188 | 0.442 |
| except_data_ro | 4 | 0.510065 | +0.010065 | 0.971247 | 0.498472 | +0.011593 | 0.573 |
| except_data_ro | 5 | 0.498690 | -0.001310 | 0.996225 | 0.500389 | -0.001699 | 0.442 |
| except_data_ro | 6 | 0.463716 | -0.036284 | 0.898931 | 0.499245 | -0.035529 | 0.406 |
| except_data_ro | 7 | 0.483647 | -0.016353 | 0.953570 | 0.500549 | -0.016902 | 0.435 |

## Anchor Repeats

| kind | index | n | p1 mean | p1 std | sign stability | complete |
|---|---:|---:|---:|---:|---:|---|
| all640 | all | 3 | 0.499575333 | 0.000479100 | 2/3 | True |
| data_ro | 0 | 3 | 0.266159333 | 0.001178075 | 3/3 | True |
| data_ro | 4 | 3 | 0.554203667 | 0.000370433 | 3/3 | True |

## Interpretation Boundary

This table is a held-out validation input. Prediction rules should be frozen before using this context as evidence. If the frozen model underperforms, the residuals should be reported as model boundary evidence rather than edited away.
