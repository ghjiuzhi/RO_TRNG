# Second Held-Out Route/PVT Guard 2026-05-30

## Purpose

Guard note for the second held-out sampler/context hardware run. This note is intentionally limited to planning/checklist material: it inventories available bitstreams/DCPs, defines route-audit and PVT-manifest expectations, and proposes the queue order for the main hardware thread. It does not modify capture scripts or TIM material.

## Current Availability

Repository root: `E:/Project/MLDSA/RO_TRNG`

| Context | XDC / entry point | Reduced-XOR W10 bitstream+DCP coverage | Status | Use |
|---|---|---:|---|---|
| `heldout_sample_x36y35_regs_x45y31` | `data/experiments/xdc_sampler_island/random1_sampler_island_sample_x36y35_regs_x45y31_heldout_20260530.xdc` | 17/17 | ready, already used as first held-out | Do not rerun as "second" context; use as prior/training context. |
| `sampler_island_local` | `data/experiments/xdc_sampler_island/random1_sampler_island_local_x45y39_regs_x45y31.xdc` | 17/17 | ready, original Board1/Board2 sampler-island context | Baseline/original comparison only. |
| `sample_ro_local` | `data/experiments/xdc_sampler_island/random1_sample_ro_local_x45y39.xdc`; build entry already in `scripts/build_restart_reduced_xor_20260526.ps1` | 0/17 | build needed | Recommended second held-out context if the goal is sampler/context perturbation with the same random1 data-RO matrix. |
| `regs_only` | `data/experiments/xdc_sampler_island/random1_sampler_regs_only_x45y31.xdc`; build entry already in `scripts/build_restart_reduced_xor_20260526.ps1` | 0/17 | build needed | Useful fallback/ablation, but sample RO is intentionally unconstrained, so route variation may be harder to interpret. |
| `compact_locked_candidate` | `data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_compact_w4_locked.xdc` | 0/17 | XDC exists, no reduced-XOR build entry confirmed | Useful later as counterfactual aperture-lock test, not first choice for frozen prediction. |

Important existing route evidence:

- First held-out per-bitstream audit is complete: `data/experiments/heldout_sampler_route_diff_20260530/heldout_per_bitstream_route_audit_20260530.csv`.
- First held-out `data_ro0` uses the successful `data_ro0_ipreuse` run directory; empty original/retry directories should not be counted as valid route evidence.
- Existing summary reports first held-out data-RO LOC/BEL stable versus held-out all640 across all 16 subset comparisons.

## Recommended Second Context

Use `sample_ro_local` as the next hardware context.

Rationale:

- It is already supported by the generic reduced-XOR build script via `-VariantsCsv sample_ro_local`.
- It keeps the random1 data-RO matrix constraints copied from `ro_random_seed1_x36y35.xdc`.
- It locks the sample RO near `SLICE_X45Y39`, which is the original local sample-RO context and differs from the first held-out `SLICE_X36Y35` sample context.
- It is scientifically useful as a frozen-prediction context: first held-out `sample_x36y35` can serve as the prior/context used for model fitting, while `sample_ro_local` provides a second context for testing transfer.

Caveat:

- `sample_ro_local` constrains the data ROs and sample RO, but not the sampled-data register island in the same explicit way as `sampler_island_local` and first held-out. The route audit must therefore report sampled-data LOC/BEL stability rather than assume it.

## Build/Capture Entry Point

A second-heldout driver already exists and was not modified here:

`scripts/run_board2_second_heldout_sample_ro_local_20260530.ps1`

The script defines:

- context: `second_heldout_sample_ro_local`
- variant: `sample_ro_local`
- warmup: `10`
- output root: `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530`
- expected capture length: `125008`
- sync header: `A55A`
- PVT manifest: `summary/second_heldout_sample_ro_local_pvt_manifest_20260530.csv`
- capture manifest: `summary/second_heldout_sample_ro_local_capture_manifest_20260530.csv`

Recommended first command for main thread:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_board2_second_heldout_sample_ro_local_20260530.ps1 -Phase BuildOnly
```

Only after all 17 bitstreams exist should the hardware capture phase start.

## Missing/Available List For `sample_ro_local`

Currently missing reduced-XOR W10 bitstream+DCP pairs:

```text
all640
data_ro0
data_ro1
data_ro2
data_ro3
data_ro4
data_ro5
data_ro6
data_ro7
except_data_ro0
except_data_ro1
except_data_ro2
except_data_ro3
except_data_ro4
except_data_ro5
except_data_ro6
except_data_ro7
```

Required bitstream pattern after build:

```text
data/vivado_runs/restart_reduced_xor_random1_sample_ro_local_formal_bits_1000x125_warmup10_<suffix>_header_delay60s/RO_TRNG_restart_reduced_xor_top.bit
```

Required DCP pattern after build:

```text
data/vivado_runs/restart_reduced_xor_random1_sample_ro_local_formal_bits_1000x125_warmup10_<suffix>_header_delay60s/checkpoints/RO_TRNG_restart_reduced_xor_top_routed.dcp
```

## Route Audit Checklist

For every available second-heldout routed DCP, extract the same feature families as the first held-out audit:

| Feature family | Required fields |
|---|---|
| Cell placement | `label`, `cohort`, `mode`, `index`, `group`, `cell_name`, `LOC`, `BEL` |
| LOC/BEL stability | common cell count and LOC/BEL change count versus second-heldout `all640`, separately for `sample_ro`, `sampled_data_regs`, and `data_ro` |
| Net routes | net name, group, route string or normalized PIP route, common net count, changed route count versus second-heldout `all640` |
| PIPs | PIP count by `sample_ro_net`, `sampled_data_net`, and `data_ro_net` |
| Net delay | per-group arc count, slow max mean ps, slow max max ps for `sample_ro`, `sampled_data`, and `data_ro` nets |
| Neighborhood | count and optional rows of cells in the local sample/sampled-data neighborhood |
| Implementation metrics | LUT/FF/BRAM/DSP, WNS/TNS/WHS/THS/WPWS/TPWS, routed power, junction temperature, route status, DRC violation/error/warning counts |

Minimum route-audit success criterion:

- `17/17` DCPs extracted if build succeeds.
- `16/16` pairwise comparisons against `second_heldout_all640`.
- No implicit isolation claim: if sampled-data, FIFO/control, or UART features move, report them rather than hiding them.

## PVT Manifest Schema

Use one row per capture and moment (`before`, `after`). Required columns:

| Column | Meaning |
|---|---|
| `capture_id` | Full run/capture label. |
| `context` | `second_heldout_sample_ro_local`. |
| `moment` | `before` or `after`. |
| `xadc_status` | `ok`, `missing`, `failed`, or `parse_failed`. |
| `xadc_timestamp` | Timestamp returned by Vivado/XADC. |
| `temperature_c` | XADC die temperature if valid. |
| `vccint_v` | XADC VCCINT if valid. |
| `vccaux_v` | XADC VCCAUX if valid. |
| `vccbram_v` | XADC VCCBRAM if valid. |
| `vpvn_v` | XADC VP/VN if available. |
| `source_file` | Path to the XADC CSV/log source. |
| `error` | Empty on success; otherwise the read/parse error. |

Recommended derived capture-level fields for the analysis summary:

| Derived field | Rule |
|---|---|
| `temperature_delta_c` | `after.temperature_c - before.temperature_c` when both are valid. |
| `vccint_delta_v` | `after.vccint_v - before.vccint_v` when both are valid. |
| `pvt_status` | `ok` only when both before/after rows are valid; otherwise `partial_or_failed` or `missing`. |

Known caveat:

- `data/hardware/20260529_fpga1_board2/xadc_readings.csv` currently contains an invalid-looking row with `TEMPERATURE=-273.1` and zero rails. Treat that row as failed/missing PVT evidence, not as a physical board condition.

## Suggested Hardware Queue For Main Thread

### Phase 0: Build/readiness

1. Run `BuildOnly` for `sample_ro_local`.
2. Confirm 17 bitstreams and 17 routed DCPs exist.
3. If a build fails, retry once for the failed suffix only.
4. If retry still fails, write the missing suffix to the capture manifest and continue with available suffixes only if at least `all640` and four contributors are available. For the full TVLSI target, rebuild until all 17 are available.

### Phase 1: Full map capture

Capture once each:

```text
all640
data_ro0
data_ro1
data_ro2
data_ro3
data_ro4
data_ro5
data_ro6
data_ro7
except_data_ro0
except_data_ro1
except_data_ro2
except_data_ro3
except_data_ro4
except_data_ro5
except_data_ro6
except_data_ro7
```

For each capture:

- read XADC before
- program/capture `125008` bytes with header `A55A`
- read XADC after
- write metadata JSON and sha256
- append PVT manifest rows
- validate output bytes and first bytes immediately

### Phase 2: Anchor repeats

After the full map summary identifies second-context strongest low/high contributors, run `run01..run03` for:

```text
all640
strongest_low_data_ro_or_except_ro
strongest_high_data_ro_or_except_ro
```

If the main thread needs anchors before the full summary exists, use first-heldout anchors as provisional:

```text
all640
data_ro5
data_ro3
```

Reason: first held-out W10 found `data_ro5` as strongest low and `data_ro3` as strongest high.

### Phase 3: Route audit and metrics

After build completion and before/after capture analysis:

- run a second-heldout route audit against `second_heldout_all640`;
- produce a per-bitstream audit CSV mirroring `heldout_per_bitstream_route_audit_20260530.csv`;
- produce implementation metrics rows mirroring `implementation_metrics_20260530.csv`;
- feed the new route/PVT/result tables into the TVLSI frozen-prediction model.

## Stop/Failure Rules

- Single condition capture failure: retry once.
- Repeated capture failure: mark that condition as missing and continue.
- XADC failure: do not stop capture; mark PVT as `partial_or_failed`.
- Build failure for `all640`: stop hardware capture, because no route/capture baseline exists.
- Build failure for one subset: continue only if the main thread explicitly accepts a partial map; otherwise finish missing bitstreams first.
