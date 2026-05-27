# Sample-RO Counterfactual Table 20260525

- CSV: `E:/Project/MLDSA/RO_TRNG/data/experiments/sample_ro_counterfactual_20260525/sample_ro_counterfactual_table_20260525.csv`
- rows: `6`

## Main Interpretation

The bidirectional sample-RO counterfactual is currently the strongest mechanism evidence. In the forward direction, a compact diagnostic topology becomes biased when only the sample RO is locked to the formal routed implementation. In the reverse direction, the formal warmup4 failure is repaired when only the sample RO is locked to the compact-routed implementation.

## Paper-Facing Table

| direction | top_design | sample_ro_implementation | warmup | overall_p1 | overall_min_entropy | worst_position | worst_p1 | worst_x | xadc_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 4 | 0.376651000 | 0.681887971 | byte0.bit5 | 0.116000000 | 884 | see metadata/log |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 5 | 0.373430000 | 0.674452399 | byte2.bit2 | 0.243000000 | 757 | see metadata/log |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 5 | 0.373541000 | 0.674708003 | byte1.bit2 | 0.208000000 | 792 | see metadata/log |
| forward fail | compact FIFO diagnostic | formal-routed sample RO locked | 11 | 0.464819000 | 0.901901197 | byte18.bit4 | 0.424000000 | 576 | see metadata/log |
| reverse repair | formal auto restart | compact-routed sample RO locked | 4 | 0.499419000 | 0.998324562 | byte61.bit6 | 0.552000000 | 552 | see metadata/log |
| reverse repair | formal auto restart | compact-routed sample RO locked | 4 | 0.499754000 | 0.999290369 | byte109.bit4 | 0.448000000 | 552 | see metadata/log |

## Forward Fail Cases

- warmup4: overall p1=0.376651000, worst=byte0.bit5 x=884 p1=0.116000000
- warmup5: overall p1=0.373430000, worst=byte2.bit2 x=757 p1=0.243000000
- warmup5: overall p1=0.373541000, worst=byte1.bit2 x=792 p1=0.208000000
- warmup11: overall p1=0.464819000, worst=byte18.bit4 x=576 p1=0.424000000

## Reverse Repair Cases

- warmup4: overall p1=0.499419000, min-H=0.998324562, worst=byte61.bit6 x=552 p1=0.552000000
- warmup4: overall p1=0.499754000, min-H=0.999290369, worst=byte109.bit4 x=552 p1=0.448000000

## Claim Boundary

This table supports sampler-side physical realization as part of the entropy-source boundary. It does not prove that the sample RO is the only relevant sampler-side element; sampling registers, local routing, control placement, and aperture effects remain part of the mechanism boundary.
