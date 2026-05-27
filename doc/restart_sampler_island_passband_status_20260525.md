# Restart Sampler-Island Passband Status 2026-05-25

## Purpose

This experiment tests whether the sampler-side repair/failure mechanism is driven mainly by the sample RO alone or by the combined sampler island, including sample RO, sampling registers, local routing, and aperture.

Matrix:

| variant | warmup bytes | target |
| --- | ---: | --- |
| `random1_sample_ro_local` | 4 / 5 / 10 / 11 | isolate sample RO placement change |
| `random1_sampler_island_local` | 4 / 5 / 10 / 11 | test sample RO plus local sampling registers/routing |

Each strict run should capture `8-byte header + 1000 x 125-byte payload = 125008 bytes`.

## Current Status

- Initial `preopen` retry completed 8/8 UART captures, but the queue requested only `125000` bytes.
- The files start with restart header `A55A03E8007D01D0`; therefore they contain header plus only `999` complete payload rows and cannot be used as formal SP800-90B restart evidence.
- They were retained only for diagnostic profiling under:
  - `data/experiments/restart_sampler_island_passband_preopen_20260525/diagnostic_payloads/`
  - `data/experiments/restart_sampler_island_passband_preopen_20260525/diagnostic_profile999/`
- A strict queue has been generated:
  - `data/experiments/fast_mode/hardware_queue_restart_sampler_island_passband_strict_20260525.csv`
- Strict hardware capture completed 8/8 on COM3/JTAG. Every strict file is exactly `125008` bytes and starts with `A55A03E8007D01D0`.
- Strict postprocessing completed:
  - payload extraction: `data/experiments/restart_sampler_island_passband_strict_20260525/payloads/`
  - MSB/LSB bit-symbol inputs: `data/experiments/restart_sampler_island_passband_strict_20260525/bit_symbols/`
  - `ea_restart` outputs: `data/experiments/restart_sampler_island_passband_strict_20260525/ea_restart/`
  - summary table: `data/experiments/restart_sampler_island_passband_strict_20260525/restart_sampler_island_passband_strict_summary_20260525.md`

## Diagnostic-Only Observation

The 999-row diagnostic profile suggests a potentially valuable non-monotonic passband:

| variant | warmup | diagnostic p1 | diagnostic worst x |
| --- | ---: | ---: | ---: |
| sample RO local only | 4 | 0.498192 | 571 |
| sample RO local only | 5 | 0.407392 | 738 |
| sample RO local only | 10 | 0.500172 | 561 |
| sample RO local only | 11 | 0.420273 | 648 |
| sample RO + regs local | 4 | 0.499893 | 548 |
| sample RO + regs local | 5 | 0.500122 | 552 |
| sample RO + regs local | 10 | 0.459546 | 593 |
| sample RO + regs local | 11 | 0.471592 | 575 |

Interpretation is intentionally cautious: this is not formal restart evidence because one payload row is missing. It is only a strong reason to repeat the strict 125008-byte captures.

## Strict Formal Restart Result

| variant | warmup | MSB restart | LSB restart | X_max | packed p1 | interpretation |
| --- | ---: | --- | --- | ---: | ---: | --- |
| sample RO local only | 4 | pass | pass | 553 | 0.499286 | local sample RO repairs this startup window |
| sample RO local only | 5 | fail | fail | 713 | 0.410871 | adjacent warmup window becomes strongly biased |
| sample RO local only | 10 | pass | pass | 550 | 0.500648 | second repaired window |
| sample RO local only | 11 | fail | fail | 666 | 0.422998 | adjacent warmup window fails again |
| sample RO + regs local | 4 | pass | pass | 551 | 0.499770 | sampler island keeps early window good |
| sample RO + regs local | 5 | pass | pass | 549 | 0.500804 | sampler island fixes the sample-only w5 failure |
| sample RO + regs local | 10 | boundary | boundary | 610 -> 599 -> 593 | 0.451448 -> 0.458774 -> 0.457368 | passband-edge point; repeat02/repeat03 passed both MSB/LSB |
| sample RO + regs local | 11 | pass | pass | 594 | 0.470665 | sampler island fixes the sample-only w11 failure |

This is a mechanism-positive result:

- sample RO placement alone can move the restart passband: `w4/w10` pass while adjacent `w5/w11` fail.
- adding local sampling registers/routing changes the passband again: `w5` and `w11` are repaired, while `w10` sits near the restart cutoff boundary. In repeat01 it split by bit order because `X_max=610` exceeded the MSB cutoff but remained below the LSB cutoff; repeat02 and repeat03 moved to `X_max=599` and `X_max=593`, passing both orders.
- therefore the sampler-side physical implementation affects restart startup windows; the effect is not a monotonic function of warmup count.
- this strengthens the paper claim that sample RO, sampling registers, local routing, and sampling aperture are part of the entropy-source boundary.

## Scripts Added

- `scripts/extract_restart_payload_with_header.py`
  - Strictly strips the 8-byte restart header.
  - Rejects incomplete captures unless `--diagnostic-trim-complete-rows` is explicitly used.
- `scripts/make_restart_passband_strict_queue_20260525.py`
  - Builds the strict 125008-byte queue from the old preopen queue.
- `scripts/postprocess_restart_passband_strict_20260525.ps1`
  - Extracts payloads, expands MSB/LSB bit-symbol datasets, runs `ea_restart`, and profiles packed-column bias.
- `scripts/summarize_restart_passband_strict_20260525.py`
  - Produces the paper-facing passband summary table after strict postprocessing.

## Next Action

Use this result in the paper as the sampler-side passband migration experiment. The `sampler_island_local w10` repeat02/repeat03 repeats have already been completed and should be described as a near-threshold passband-edge point, not a deterministic MSB-only failure. The next useful repeat is not another identical single-board `w10` run; it is either a second board, or targeted repeats of `sample_ro_local w5/w11` and `sampler_island_local w5/w11`.
