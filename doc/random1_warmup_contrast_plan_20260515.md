# Random1 Warmup Contrast Plan - 2026-05-15

## Purpose

The `random3` warmup sweep now has a repeated boundary observation: `warmup10` fails while `warmup11/12` pass. The next useful hardware contrast is `random1`, because its sequential non-IID entropy estimate is much lower and its restart cutoff is therefore wider. This contrast tests whether restart fixed-position bias is truly removed by warmup, or merely hidden by a lower `H_I` threshold.

## Current State

- Existing `random1` warmup0 restart bitstream:
  `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_header_delay60s/RO_TRNG_restart_auto_top.bit`
- Existing placement:
  `data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc`
- Existing `random1` warmup0 restart observation:
  `ea_restart` passed, but fixed-position bias remained visible with worst raw position `byte0 bit0`, `x=680`.
- A worker has been started to build `random1` warmup8/11/12 bitstreams using the same auto-stream parameters as `random3`.

## Build Status

As of the latest check:

| warmup | bitstream status | path |
| ---: | --- | --- |
| 8 | built | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup8_header_delay60s/RO_TRNG_restart_auto_top.bit` |
| 11 | built | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup11_header_delay60s/RO_TRNG_restart_auto_top.bit` |
| 12 | building | `data/vivado_runs/restart_auto_random1_formal_bits_1000x125_warmup12_header_delay60s/RO_TRNG_restart_auto_top.bit` |

Do not start `random1` hardware capture until the build worker has either completed warmup12 or the queue is intentionally reduced to warmup8/11.

## Planned Hardware Queue

Run only after the `random1` warmup bitstreams exist and after confirming no other Vivado/COM3/JTAG task is active.

Candidate captures:

- `random1_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_20260515.bin`
- `random1_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_20260515.bin`
- `random1_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_20260515.bin`

For each capture:

1. Program once and auto-stream `1000 x 125` packed bytes.
2. Verify header `A55A03E8007D01D0`.
3. Expand MSB/LSB to `1000 x 1000` bit-symbol files.
4. Run `ea_restart` with the existing `random1` initial entropy values:
   - MSB `H_I=0.389520`
   - LSB `H_I=0.383737`
5. Run packed byte/bit column-bias analysis with `x_cutoff=821` for a conservative random1 view, while keeping raw `X` values comparable against random3.

## Expected Paper Value

This contrast can separate three effects:

- sequential entropy level and restart cutoff width,
- fixed-position restart bias magnitude,
- warmup-driven movement out of the early transient window.

The safe claim should be mechanism-oriented: `random1` may pass `ea_restart` because its cutoff is wider, while raw column bias can still exist. That contrast helps explain why pass/fail alone is not enough for a high-level placement/TRNG paper.
