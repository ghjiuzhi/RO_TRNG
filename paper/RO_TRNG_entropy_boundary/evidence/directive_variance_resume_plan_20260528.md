# Directive-Variance Resume Plan 20260528

Purpose: prepare and execute a route-variance control for the sampler-side counterfactual. This is not called a Vivado seed experiment because the current Vivado 2023.2 non-project flow does not expose a true placement/routing seed. The control uses explicit implementation directives and records them in each build manifest.

## Offline Preparation Already Completed

- Added directive parameters to `scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl`.
- Added `scripts/run_sample_ro_directive_variance_20260528.ps1`.
- Built two W4 `Explore/Explore/Explore` bitstreams in build-only mode:
  - compact baseline: `data/vivado_runs/sample_ro_directive_variance_20260528/restart_fifo_compact_diag_compact_warmup4_1000x125_explore1/RO_TRNG_restart_fifo_compact_diag_top.bit`
  - forward fail: `data/vivado_runs/sample_ro_directive_variance_20260528/restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1/RO_TRNG_restart_fifo_compact_diag_top.bit`
- Generated routed locality audit for the two directive builds:
  - `data/experiments/sample_ro_directive_variance_route_diff_20260528/sample_ro_route_evidence_summary_20260528.md`

## Current Offline Locality Result

The W4 directive-controlled pair keeps the same useful locality pattern as the main Table VII forward audit:

| Pair | data-RO cells changed | sampled registers changed | sample-RO cells changed | data-RO net routes changed | sample-RO net routes changed | sampled-data net routes changed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| compact_w4_explore1 vs forward_w4_explore1 | 0/16 LOC, 0/16 BEL | 0/64 LOC, 0/64 BEL | 2/9 LOC, 3/9 BEL | 34/64 | 18/36 | 9/64 |

This remains bounded locality evidence, not sample-RO-only proof. Its value is that an independently implemented directive-controlled pair is ready for hardware capture.

## Hardware Result

Hardware capture was completed after starting `hw_server` on `localhost:3122`.

| Variant | Run | Overall p1 | Min-H | Worst byte.bit | Worst x | XADC after |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| compact baseline, W4, Explore | `restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528` | 0.496761000 | 0.990684362 | 3.3 | 560 | 44.3 C |
| forward fail, W4, Explore | `restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528` | 0.375294000 | 0.678750709 | 2.2 | 796 | 44.9 C |

Result summary:

- `paper/RO_TRNG_entropy_boundary/evidence/directive_variance_result_20260528.md`
- `data/experiments/sample_ro_directive_variance_20260528/sample_ro_directive_variance_20260528.csv`

## Commands Used

```powershell
powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart.ps1 `
  -VivadoBat "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  -Bitstream "data\vivado_runs\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1\RO_TRNG_restart_fifo_compact_diag_top.bit" `
  -Port COM3 -Baud 115200 -Kind restart `
  -Run "restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528" `
  -Bytes 125016 `
  -OutFile "data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.bin" `
  -MetadataDir "data\hardware\20260511_fpga1_board1\metadata" `
  -IdleTimeoutSec 300 -BoardId z7020_b01 `
  -RecordXadc -XadcMode after_only `
  -XadcCsv "data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv"
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart.ps1 `
  -VivadoBat "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat" `
  -Bitstream "data\vivado_runs\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1\RO_TRNG_restart_fifo_compact_diag_top.bit" `
  -Port COM3 -Baud 115200 -Kind restart `
  -Run "restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528" `
  -Bytes 125016 `
  -OutFile "data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.bin" `
  -MetadataDir "data\hardware\20260511_fpga1_board1\metadata" `
  -IdleTimeoutSec 300 -BoardId z7020_b01 `
  -RecordXadc -XadcMode after_only `
  -XadcCsv "data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv"
```

```powershell
python scripts\analyze_restart_fifo_compact_diag.py `
  --input data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.bin `
  --out-dir data\experiments\sample_ro_directive_variance_20260528 `
  --label restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528

python scripts\analyze_restart_fifo_compact_diag.py `
  --input data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.bin `
  --out-dir data\experiments\sample_ro_directive_variance_20260528 `
  --label restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528
```

## Interpretation

- The strongest expected result occurred: compact directive build remains near balanced while formal-sample directive build remains biased. This supports that the sampler-side counterfactual is not merely one default implementation accident.
- The route audit still reports route residuals, so this strengthens sampler-side/local routed-context evidence without proving sample-RO-only causality.
- Do not describe this as a seed-controlled experiment. Describe it as a directive-controlled route-variance control.
