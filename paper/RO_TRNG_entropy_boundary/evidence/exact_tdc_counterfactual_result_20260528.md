# Exact Counterfactual TDC Result 20260528

Purpose: measure a direct TDC diagnostic around the sampler-side counterfactual. Unlike the older sampler-data TDC variants, these two captures use the exact `Scompact` and `Srestart` sample-RO LOC/BEL assignments from the counterfactual table, with `data_ro0` held at the same random1 matrix placement.

This is a mechanism constraint, not a proof of root cause. It asks whether the counterfactual failure is accompanied by strong pairwise sample-RO/data-RO phase locking under this TDC measurement condition.

## Build Scope

- Top: `RO_TDC_reset_aligned_top`
- Pair: `u_ro_a = sample RO`, `u_ro_b = data_ro0`
- `RO_A_STAGES=9`, `RO_B_STAGES=2`
- `WARMUP_PACKETS=4`, `CAPTURE_PACKETS=32768`, `SAMPLE_DIV=5000`
- XDC files:
  - `data/experiments/xdc_tdc_sampler_data/tdc_counterfactual_scompact_ro0_warmup4_20260528.xdc`
  - `data/experiments/xdc_tdc_sampler_data/tdc_counterfactual_srestart_ro0_warmup4_20260528.xdc`

## Hardware Captures

| Variant | Run | Capture SHA256 | XADC after |
| --- | --- | --- | ---: |
| `Scompact` sample RO vs data_ro0 | `tdc_counterfactual_scompact_ro0_warmup4_32768_run01_20260528` | `23D0723BC2A86B80052B0FD1A7B13DFA6F442161B79848CA17056E4DB54DA190` | 46.8 C |
| `Srestart` sample RO vs data_ro0 | `tdc_counterfactual_srestart_ro0_warmup4_32768_run01_20260528` | `3F499A299E5B8FB37B265C1A2522391A83A2093C4154BE8E53262933674364E4` | 47.0 C |

## TDC Summary

| Variant | Packets | seq gaps | diff std ps | phase r | mean window phase r | max abs best-lag r | strong-lock windows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Scompact` vs data_ro0 | 32768 | 0 | 1965.500 | 0.004300 | 0.004173 | 0.059012 | 0/16 |
| `Srestart` vs data_ro0 | 32768 | 0 | 1955.612 | 0.011762 | 0.011803 | 0.057888 | 0/16 |

Startup-diffusion summaries:

| Variant | H(diff) | early H(diff) | warmup-4 H(diff) | same-diff ratio | longest same-diff run | lag-1 autocorr(diff) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Scompact` vs data_ro0 | 6.697480 | 6.651763 | 6.650433 | 0.010010 | 3 | 0.004248 |
| `Srestart` vs data_ro0 | 6.747712 | 6.720090 | 6.719745 | 0.009857 | 3 | 0.002808 |

## LOC/BEL Audit

The routed TDC checkpoints match the intended sample-RO LOC/BEL perturbation:

- `Scompact`: NAND `SLICE_X46Y34/B6LUT`, loop[1] `SLICE_X47Y33/A6LUT`, loop[7] `SLICE_X49Y45/A6LUT`
- `Srestart`: NAND `SLICE_X47Y33/A6LUT`, loop[1] `SLICE_X46Y32/B6LUT`, loop[7] `SLICE_X49Y45/B6LUT`
- data_ro0 is fixed in both TDC captures at `SLICE_X44Y39/A6LUT+B6LUT`

Audit files:

- `data/experiments/tdc_counterfactual_20260528/tdc_counterfactual_scompact_locbel_20260528.csv`
- `data/experiments/tdc_counterfactual_20260528/tdc_counterfactual_srestart_locbel_20260528.csv`

## Interpretation

This exact counterfactual TDC run does not show strong pairwise hard-lock behavior. Across 32 total windows, no window crosses the conservative `|r| >= 0.5` lag-correlation screen; the largest best-lag magnitude is about 0.059. The full-run phase correlations are also small: 0.0043 for `Scompact` and 0.0118 for `Srestart`.

Therefore, this result should be used as a negative mechanism constraint: the restart failure under `Srestart` is not accompanied by obvious strong sample-RO/data_ro0 pairwise phase locking in this TDC setup. It does not rule out weaker coupling, different data-RO directions, sampled-vector effects, or routed-neighborhood/reset interactions.
