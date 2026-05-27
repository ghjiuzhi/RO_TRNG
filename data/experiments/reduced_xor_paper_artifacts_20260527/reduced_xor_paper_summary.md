# Reduced-XOR Paper Artifacts 2026-05-27

## Key Result

The reduced-XOR hardware counterfactual shows that same-data-RO directions are real biased hardware output functions, while the final all64 output is an XOR-cancellation result over a structured sampler vector.

- all64 at w10: p1=0.458617, abs_bias=0.041383, min-H=0.885278509.
- strongest low-biased direction: data_ro0 p1=0.191877, abs_bias=0.308123.
- strongest high-biased direction: data_ro3 p1=0.671833, abs_bias=0.171833.
- best cancelling complement: except_ro2 p1=0.499674, abs_bias=0.000326.
- largest repeat delta among diagnostic modes: all64 delta_p1=-0.015423.

## Files

- `reduced_xor_w10_direction_paper.csv`
- `reduced_xor_w10_direction_paper.md`
- `reduced_xor_w10_direction_bias.png` / `.svg`
- `reduced_xor_w10_repeat_paper.csv`
- `reduced_xor_w10_repeat_paper.md`
- `reduced_xor_w10_repeat_p1.png` / `.svg`
