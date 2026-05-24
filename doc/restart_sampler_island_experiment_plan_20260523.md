# Restart Sampler-Island Experiment Plan 20260523

## Goal

Test whether the sampler-side placement repair that fixes continuous `random1` TRNG output also fixes SP800-90B restart startup bias.

This is now more valuable than adding more same-style sampler-data TDC repeats, because the completed six-run TDC queue did not show a strong baseline/local phase-correlation split.

## Hypotheses

### H1: Unified Sampler-Path Mechanism

If `sample_ro_local` or `sampler_island_local` improves both continuous TRNG entropy and restart sanity, then the sampler-side physical path controls both steady-state bias and startup fixed-column bias.

Expected result:

- warmup0 improves relative to baseline `random1`
- warmup12 passes with margin
- worst restart columns weaken or move away from the previously fixed byte/bit positions

### H2: Two-Mechanism Split

If sampler-island fixes continuous TRNG but warmup0 restart still fails, then steady-state entropy and restart startup transient are related but not identical.

Expected result:

- continuous 20MiB sampler-island remains near ideal
- warmup0 still fails restart sanity
- warmup12 still passes
- paper should separate "steady-state sampler aperture/routing" from "startup phase-memory transient"

## Prepared Bitstream Build

Script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_restart_sampler_island_20260523.ps1
```

Build targets:

| variant | warmup | output bitstream |
| --- | ---: | --- |
| `sample_ro_local` | 0 | `data\vivado_runs\restart_auto_random1_sample_ro_local_formal_bits_1000x125_warmup0_header_delay60s\RO_TRNG_restart_auto_top.bit` |
| `sample_ro_local` | 12 | `data\vivado_runs\restart_auto_random1_sample_ro_local_formal_bits_1000x125_warmup12_header_delay60s\RO_TRNG_restart_auto_top.bit` |
| `sampler_island_local` | 0 | `data\vivado_runs\restart_auto_random1_sampler_island_local_formal_bits_1000x125_warmup0_header_delay60s\RO_TRNG_restart_auto_top.bit` |
| `sampler_island_local` | 12 | `data\vivado_runs\restart_auto_random1_sampler_island_local_formal_bits_1000x125_warmup12_header_delay60s\RO_TRNG_restart_auto_top.bit` |

## Prepared Capture Queue

Queue:

```text
data\experiments\fast_mode\hardware_queue_restart_sampler_island_20260523.csv
```

Run after all four bitstreams exist:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_restart_sampler_island_20260523.csv `
  -Port COM3 `
  -Baud 115200 `
  -StatusMarkdown doc\restart_sampler_island_capture_status_20260523.md `
  -LogDir data\experiments\fast_mode\restart_sampler_island_logs_20260523 `
  -RecordXadc `
  -XadcCsv data\experiments\xadc_summary\xadc_capture_log_20260523 `
  -ContinueOnError
```

Each capture is `125000` bytes, representing `1000 x 125` bytes that can be expanded to `1000 x 1000` bit symbols for SP800-90B restart analysis.

## Decision Rule

- If both `sample_ro_local` and `sampler_island_local` pass at warmup0, sampler-side relocation suppresses startup phase memory.
- If only `sampler_island_local` passes at warmup0, sampling registers/routing are the decisive restart factor.
- If both fail at warmup0 but pass at warmup12, continuous-stream repair and restart-startup repair are different mechanisms.

## Paper Use

This experiment gives a cleaner high-level paper story than more raw TDC repeats:

- TDC: negative control against simple pairwise locking.
- Continuous TRNG ablation: sampler side can repair steady-state entropy.
- Restart sampler-island ablation: determines whether startup transient shares the same physical cause.

## 2026-05-23 Execution Status

Bitstream build:

- Built all four planned restart bitstreams successfully:
  - `sample_ro_local` warmup0/warmup12
  - `sampler_island_local` warmup0/warmup12

Capture attempt:

| run | expected bytes | captured bytes | status |
| --- | ---: | ---: | --- |
| `restart_random1_sample_ro_local_warmup0_1000x125_20260523` | 125000 | 0 | no UART bytes before timeout |
| `restart_random1_sample_ro_local_warmup12_1000x125_20260523` | 125000 | 0 | no UART bytes before timeout |
| `restart_random1_sampler_island_local_warmup0_1000x125_20260523` | 125000 | 36529 | partial UART stream, then timeout |
| `restart_random1_sampler_island_local_warmup12_1000x125_20260523` | 125000 | 0 | no UART bytes before timeout |

Engineering interpretation:

- These four files are **not valid SP800-90B restart datasets** and must not be used as formal restart inputs.
- The failure is not a generic COM3/JTAG problem: the bitstreams programmed, XADC snapshots worked, and `sampler_island_local warmup0` emitted a partial stream.
- The contrast is still informative as a diagnostic: applying sampler-side XDC variants to the restart auto-stream top changes startup/streaming behavior, and the register-local variant behaves differently from sample-RO-only.
- The partial `sampler_island_local warmup0` stream did not begin with the expected debug header bytes, so the next step should be RTL/header-level debug rather than another blind capture repeat.

Next action:

1. Build a restart debug-header-only smoke variant for `sample_ro_local` and `sampler_island_local`, with a much smaller `RESTART_COUNT` and `ROW_BYTES`.
2. Add or expose an LED/status signal for restart FSM states if possible.
3. Only after header smoke succeeds, rerun `1000 x 125` restart captures.
