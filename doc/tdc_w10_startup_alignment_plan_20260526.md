# TDC w10 Startup Alignment Plan 2026-05-26

## Goal

Use reset/header-aligned TDC to test whether the `sampler_island_local warmup10` restart boundary is visible as a sample/data RO phase-diffusion anomaly.

The immediate hardware run is:

```text
tdc_reset_random1_sampler_local_ro0_clean32k_warmup10
```

This observes:

```text
lane A = local sample RO at x45y39
lane B = random1 data RO0 at x44y39
warmup packets = 10
capture packets = 32768
sample divider = 5000
```

## Scope Boundary

This TDC top observes the sample RO and one data RO directly. It does not instantiate the full restart sampler-island register array. Therefore:

- a positive TDC anomaly at `w10` would support a sample/data phase-diffusion explanation;
- a negative TDC result would not kill the mechanism. It would instead push the explanation toward sampling registers, local routing, output packing, or aperture effects that are present in the restart top but absent from this two-lane TDC top.

## Reproduction

Build:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_reset_aligned_bitstreams.ps1 -Mode w10_boundary
```

Capture:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_tdc_reset_aligned_preopen_queue_20260525.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_w10_boundary_20260526.csv `
  -OutRoot data\experiments\tdc_reset_aligned_w10_boundary_20260526 `
  -RecordXadcAfter
```

Compare against existing clean32k controls:

```text
data/experiments/tdc_reset_aligned_clean32k_all_20260525/
```
