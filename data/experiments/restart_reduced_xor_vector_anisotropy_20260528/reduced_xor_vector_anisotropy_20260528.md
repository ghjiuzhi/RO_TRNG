# Reduced-XOR Warmup10 Vector Anisotropy

## Mechanism Question

This experiment asks whether the sampled 8 x 8 vector is biased primarily along same-data-RO directions, along sampler-phase line directions, or both. It uses the same warmup-10 reduced-XOR top as the full direction map.

## Group Summary

| group | rows | p1 range | mean abs bias | max abs bias | min min-H | max worst x | max-bias member |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| data_ro | 8 | 0.191877-0.671833 | 0.13691925 | 0.308123 | 0.3073532 | 897 | data_ro0 (0.191877) |
| line | 8 | 0.486473-0.501004 | 0.00211225 | 0.013527 | 0.961487963 | 701 | line6 (0.486473) |
| except_data_ro | 8 | 0.499674-0.565521 | 0.029468625 | 0.065521 | 0.822347497 | 620 | except_data_ro5 (0.565521) |

## Interpretation

The warmup-10 row/column control is strongly anisotropic. Same-data-RO directions span p1=0.191877 to 0.671833, with maximum absolute bias 0.308123. Sampler-phase line directions stay close to balance, spanning p1=0.486473 to 0.501004, with maximum absolute bias 0.013527. Therefore the dominant marginal reduced-XOR structure in this warmup-10 run is not a generic per-sampler-phase line failure. It is concentrated in same-data-RO directions and then reshaped by XOR complements.

Line6 has the largest line-direction deviation and a large worst fixed-position count, so it was repeated as a targeted mechanism check. The repeat stayed close in overall p1 and hit the same worst byte.bit position. Thus line6 looks like a stable fixed-position startup outlier with weak global bias, not a row-direction analogue of the strong data-RO direction bias.

## Line6 Repeat Check

| run | p1 | abs bias | min-H | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| run01 | 0.486473 | 0.013527 | 0.961487963 | 0.3 | 701 | 0.299 |
| repeat02 | 0.487182 | 0.012818 | 0.963481193 | 0.3 | 714 | 0.286 |

## Detailed Rows

| group | index | p1 | abs bias | min-H | row ones std | worst byte.bit | worst x | worst p1 | source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| all64 | all | 0.458617 | 0.041383 | 0.885278509 | 16.927737917 | 83.7 | 590 | 0.41 | w10_direction_map_20260526 |
| data_ro | 0 | 0.191877 | 0.308123 | 0.3073532 | 7.764397659 | 0.6 | 897 | 0.103 | w10_direction_map_20260526 |
| data_ro | 1 | 0.518915 | 0.018915 | 0.946429855 | 6.529607569 | 1.3 | 632 | 0.368 | w10_direction_map_20260526 |
| data_ro | 2 | 0.244002 | 0.255998 | 0.403545677 | 9.811014015 | 1.3 | 847 | 0.153 | w10_direction_map_20260526 |
| data_ro | 3 | 0.671833 | 0.171833 | 0.573825433 | 11.445833784 | 2.5 | 804 | 0.804 | w10_direction_map_20260526 |
| data_ro | 4 | 0.424639 | 0.075361 | 0.797460661 | 8.340304491 | 1.5 | 807 | 0.193 | w10_direction_map_20260526 |
| data_ro | 5 | 0.409454 | 0.090546 | 0.759878654 | 6.594079466 | 0.6 | 806 | 0.194 | w10_direction_map_20260526 |
| data_ro | 6 | 0.37538 | 0.12462 | 0.67894933 | 9.667347102 | 0.1 | 839 | 0.161 | w10_direction_map_20260526 |
| data_ro | 7 | 0.549958 | 0.049958 | 0.86260665 | 7.478250865 | 1.2 | 644 | 0.644 | w10_direction_map_20260526 |
| line | 0 | 0.499648 | 0.000352 | 0.9989847 | 14.52673728 | 0.1 | 652 | 0.348 | w10_line_map_20260528 |
| line | 1 | 0.499561 | 0.000439 | 0.99873387 | 15.144315072 | 2.0 | 658 | 0.658 | w10_line_map_20260528 |
| line | 2 | 0.500273 | 0.000273 | 0.999212503 | 16.223762541 | 1.3 | 583 | 0.417 | w10_line_map_20260528 |
| line | 3 | 0.500945 | 0.000945 | 0.99727588 | 15.685278926 | 1.6 | 665 | 0.665 | w10_line_map_20260528 |
| line | 4 | 0.501004 | 0.001004 | 0.997105973 | 14.119135384 | 0.3 | 618 | 0.618 | w10_line_map_20260528 |
| line | 5 | 0.500182 | 0.000182 | 0.999474955 | 14.666317738 | 0.0 | 560 | 0.56 | w10_line_map_20260528 |
| line | 6 | 0.486473 | 0.013527 | 0.961487963 | 15.810922522 | 0.3 | 701 | 0.299 | w10_line_map_20260528 |
| line | 7 | 0.500176 | 0.000176 | 0.999492261 | 13.930865874 | 0.4 | 585 | 0.585 | w10_line_map_20260528 |
| except_data_ro | 0 | 0.50102 | 0.00102 | 0.9970599 | 15.99773734 | 12.5 | 571 | 0.571 | w10_direction_map_20260526 |
| except_data_ro | 1 | 0.550312 | 0.050312 | 0.861678307 | 17.376727425 | 83.3 | 597 | 0.597 | w10_direction_map_20260526 |
| except_data_ro | 2 | 0.499674 | 0.000326 | 0.999059669 | 16.104028192 | 121.7 | 557 | 0.557 | w10_direction_map_20260526 |
| except_data_ro | 3 | 0.55393 | 0.05393 | 0.85222442 | 18.397801499 | 3.3 | 603 | 0.603 | w10_direction_map_20260526 |
| except_data_ro | 4 | 0.520205 | 0.020205 | 0.942847829 | 15.844335739 | 68.5 | 570 | 0.57 | w10_direction_map_20260526 |
| except_data_ro | 5 | 0.565521 | 0.065521 | 0.822347497 | 17.326441037 | 122.5 | 620 | 0.62 | w10_direction_map_20260526 |
| except_data_ro | 6 | 0.501833 | 0.001833 | 0.994720751 | 15.984026745 | 111.3 | 556 | 0.556 | w10_direction_map_20260526 |
| except_data_ro | 7 | 0.542602 | 0.042602 | 0.88203373 | 17.085654685 | 6.2 | 598 | 0.598 | w10_direction_map_20260526 |
