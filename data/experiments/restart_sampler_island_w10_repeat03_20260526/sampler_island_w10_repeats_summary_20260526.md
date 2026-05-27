# Sampler-Island Warmup10 Repeat Summary 2026-05-26

This file consolidates the single-board repeats of `random1_sampler_island_local warmup10`.
All valid rows use strict restart capture format:

```text
8-byte header + 1000 x 125-byte payload = 125008 bytes
header = A55A03E8007D01D0
```

| repeat | bytes | XADC after | packed p1 | worst byte.bit | worst x | MSB restart | LSB restart | interpretation |
| --- | ---: | --- | ---: | --- | ---: | --- | --- | --- |
| repeat01 | 125008 | not recorded in this table | 0.451448 | 4.2 | 610 | failed, cutoff 605 | passed, cutoff 632 | split because the run landed just above the MSB cutoff and below the LSB cutoff |
| repeat02 | 125008 | 46.3 C, VCCINT 1.000 V | 0.458774 | 4.4 | 599 | passed, cutoff 605 | passed, cutoff 632 | moved below both cutoffs |
| repeat03 | 125008 | 45.6 C, VCCINT 1.000 V | 0.457368 | 18.0 | 593 | passed, cutoff 605 | passed, cutoff 632 | again below both cutoffs |

## Interpretation

`sampler_island_local warmup10` is a near-threshold restart passband-edge point, not a deterministic MSB-only or bit-order-specific failure.

The evidence is:

- repeat01: `X_max=610`, above the MSB cutoff `605` but below the LSB cutoff `632`, so it failed MSB and passed LSB;
- repeat02: `X_max=599`, below both cutoffs, so both orders passed;
- repeat03: `X_max=593`, below both cutoffs, so both orders passed again.

This preserves the mechanism claim while making the wording more careful: the sampler-island implementation changes the startup passband, and warmup10 sits close to the SP800-90B restart sanity boundary. The repeat-to-repeat variation should be treated as physical startup-window variability near the cutoff, not as a stable output-packing defect.

## Reproduction Entry Points

Capture queue:

```text
data/experiments/fast_mode/hardware_queue_restart_sampler_island_w10_repeat03_20260526.csv
```

Raw capture:

```text
data/hardware/20260511_fpga1_board1/restart/restart_random1_sampler_island_local_warmup10_1000x125_strict_repeat03_20260526.bin
```

Postprocessed summary:

```text
data/experiments/restart_sampler_island_w10_repeat03_20260526/restart_sampler_island_w10_repeat03_summary_20260526.md
```
