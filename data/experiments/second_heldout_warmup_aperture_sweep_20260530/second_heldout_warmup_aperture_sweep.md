# Second Held-Out Warmup Aperture Sweep

Analysis-only summary over raw restart captures already present on disk. Missing future captures are retained as rows with `status=missing`; no hardware capture is run by this script.

## Coverage

- Valid captures: 50
- Missing expected captures: 0
- Invalid captures: 0

| warmup | ok | missing | invalid |
| --- | --- | --- | --- |
| 0 | 3 | 0 | 0 |
| 4 | 3 | 0 | 0 |
| 5 | 3 | 0 | 0 |
| 8 | 3 | 0 | 0 |
| 9 | 3 | 0 | 0 |
| 10 | 23 | 0 | 0 |
| 11 | 3 | 0 | 0 |
| 12 | 3 | 0 | 0 |
| 13 | 3 | 0 | 0 |
| 16 | 3 | 0 | 0 |

## Observed Snapshot

| warmup | kind | index | run_id | status | p1 | abs_bias | aperture_class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | all640 | all | run01 | ok | 0.498869000 | 0.001131000 | near_balanced |
| 0 | data_ro | 0 | run01 | ok | 0.109904000 | 0.390096000 | strong_bias |
| 0 | data_ro | 4 | run01 | ok | 0.574779000 | 0.074779000 | moderate_bias |
| 4 | all640 | all | run01 | ok | 0.498470000 | 0.001530000 | near_balanced |
| 4 | data_ro | 0 | run01 | ok | 0.194568000 | 0.305432000 | strong_bias |
| 4 | data_ro | 4 | run01 | ok | 0.450769000 | 0.049231000 | mild_bias |
| 5 | all640 | all | run01 | ok | 0.363168000 | 0.136832000 | moderate_bias |
| 5 | data_ro | 0 | run01 | ok | 0.193084000 | 0.306916000 | strong_bias |
| 5 | data_ro | 4 | run01 | ok | 0.378073000 | 0.121927000 | moderate_bias |
| 8 | all640 | all | run01 | ok | 0.319806000 | 0.180194000 | strong_bias |
| 8 | data_ro | 0 | run01 | ok | 0.198508000 | 0.301492000 | strong_bias |
| 8 | data_ro | 4 | run01 | ok | 0.223243000 | 0.276757000 | strong_bias |
| 9 | all640 | all | run01 | ok | 0.499663000 | 0.000337000 | balanced |
| 9 | data_ro | 0 | run01 | ok | 0.283785000 | 0.216215000 | strong_bias |
| 9 | data_ro | 4 | run01 | ok | 0.552621000 | 0.052621000 | moderate_bias |
| 10 | all640 | all | run01 | ok | 0.500040000 | 0.000040000 | balanced |
| 10 | all640 | all | run02 | ok | 0.499083000 | 0.000917000 | balanced |
| 10 | all640 | all | run03 | ok | 0.499603000 | 0.000397000 | balanced |
| 10 | data_ro | 0 | run01 | ok | 0.264807000 | 0.235193000 | strong_bias |
| 10 | data_ro | 0 | run02 | ok | 0.266963000 | 0.233037000 | strong_bias |
| 10 | data_ro | 0 | run03 | ok | 0.266708000 | 0.233292000 | strong_bias |
| 10 | data_ro | 1 | run01 | ok | 0.434643000 | 0.065357000 | moderate_bias |
| 10 | data_ro | 2 | run01 | ok | 0.279127000 | 0.220873000 | strong_bias |
| 10 | data_ro | 3 | run01 | ok | 0.413600000 | 0.086400000 | moderate_bias |
| 10 | data_ro | 4 | run01 | ok | 0.553844000 | 0.053844000 | moderate_bias |
| 10 | data_ro | 4 | run02 | ok | 0.554183000 | 0.054183000 | moderate_bias |
| 10 | data_ro | 4 | run03 | ok | 0.554584000 | 0.054584000 | moderate_bias |
| 10 | data_ro | 5 | run01 | ok | 0.388732000 | 0.111268000 | moderate_bias |
| 10 | data_ro | 6 | run01 | ok | 0.266048000 | 0.233952000 | strong_bias |
| 10 | data_ro | 7 | run01 | ok | 0.518448000 | 0.018448000 | mild_bias |
| 10 | except_data_ro | 0 | run01 | ok | 0.498802000 | 0.001198000 | near_balanced |
| 10 | except_data_ro | 1 | run01 | ok | 0.626670000 | 0.126670000 | moderate_bias |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Transition Points

| kind | index | observed_warmups | missing_warmups | transition_bracket | strongest_abs_bias_warmup | min_abs_bias_warmup | bias_sign_changes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all640 | all | 0,4,5,8,9,10,11,12,13,16 |  | 8->9 | 8 | 9 | 0 |
| data_ro | 0 | 0,4,5,8,9,10,11,12,13,16 |  | no_observed_balanced_point | 13 | 16 | 0 |
| data_ro | 1 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| data_ro | 2 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| data_ro | 3 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| data_ro | 4 | 0,4,5,8,9,10,11,12,13,16 |  | no_observed_balanced_point | 8 | 13 | 3 |
| data_ro | 5 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| data_ro | 6 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| data_ro | 7 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 0 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 1 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 2 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 3 | 10 | 0,4,5,8,9,11,12,13,16 | balanced_at_first_observed | 10 | 10 | 0 |
| except_data_ro | 4 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 5 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 6 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |
| except_data_ro | 7 | 10 | 0,4,5,8,9,11,12,13,16 | no_observed_balanced_point | 10 | 10 | 0 |

## Boundary

Transition rows are descriptive brackets over observed warmups only. A missing warmup is treated as pending data, not as a pass, fail, or interpolation point.

