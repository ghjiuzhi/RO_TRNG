# TVLSI Checkpoint 20260530

Purpose: freeze the current Experiment 1-5 evidence state for the TVLSI sampler-aperture line without touching the TIM manuscript, pushing to GitHub, or changing the MLDSA remote.

## Checkpoint Status

This checkpoint covers the first closed loop:

1. Board2 held-out sampler W10 full reduced-XOR map.
2. Board2 counterfactual balanced repeats.
3. Held-out per-bitstream route/PIP/net-delay audit.
4. Offline prediction-vs-observed and route/result correlation tables.
5. Implementation utilization/timing/power/status metrics.

Current acceptance snapshot:

| Item | Status | Evidence |
|---|---|---|
| Held-out full reduced-XOR map | 17 rows; complete | `data/hardware/20260529_fpga1_board2/restart_reduced_xor_heldout_sampler_20260530/summary/board2_heldout_sampler_w10_reduced_xor_full_map.csv` |
| Board2 counterfactual repeats | 7 target conditions; all `n=3`; no missing rows | `data/hardware/20260529_fpga1_board2/restart_counterfactual/summary/board2_sampler_counterfactual_repeats_aggregate_20260530.csv`; `board2_sampler_counterfactual_repeats_missing_20260530.csv` |
| Held-out route audit | 17/17 route extraction rows; 16/16 all640-to-subset comparisons | `data/experiments/heldout_sampler_route_diff_20260530/heldout_per_bitstream_route_audit_20260530.csv` |
| Implementation metrics | 34 rows for original plus held-out report sets | `data/experiments/tvlsi_sampler_aperture_model_20260530/implementation_metrics_20260530.csv` |
| Prediction table | 22 rows; residuals and mismatches retained | `data/experiments/tvlsi_sampler_aperture_model_20260530/prediction_vs_observed.csv` |
| Input source status | 12 tracked inputs; no optional missing input | `data/experiments/tvlsi_sampler_aperture_model_20260530/input_source_status.csv` |

Key numerical anchors:

- Held-out all640 W10: `p1=0.500718`, `abs_bias=0.000718`, `min-H=0.997930`.
- Independent XOR approximation from eight held-out data-RO contributors: predicted `p1=0.499996685`, residual `+0.000721315`.
- Strongest held-out low contributor: `data_ro5`, `p1=0.273096`.
- Strongest held-out high contributor: `data_ro3`, `p1=0.658159`.
- Board2 counterfactual repeats:
  - compact baseline w4/w5/w11: `n=3`, complete.
  - forward Srestart w4/w5/w11: `n=3`, complete.
  - reverse Scompact w4: `n=3`, complete.
- Held-out route audit: data-RO LOC/BEL stayed fixed in all held-out all640-to-subset comparisons; sample-RO/context route features vary and should be treated as implementation variables.

## Scoped Inventory to Preserve

Recommended checkpoint include set:

- TVLSI paper workspace:
  - `paper/RO_TRNG_tvlsi_sampler_aperture/`
- TVLSI model and capture scripts:
  - `scripts/make_board2_heldout_sampler_w10_reduced_xor_full_map_20260530.py`
  - `scripts/run_board2_counterfactual_repeats_20260530.ps1`
  - `scripts/summarize_board2_counterfactual_repeats_20260530.py`
  - `scripts/summarize_heldout_route_and_impl_metrics_20260530.py`
  - `scripts/tvlsi_build_sampler_aperture_model_20260530.py`
  - `scripts/program_and_capture_uart_sync_header.ps1`
  - `scripts/vivado/route_checkpoint_to_bitstream_20260530.tcl`
- Board2 held-out and repeat summaries:
  - `data/hardware/20260529_fpga1_board2/restart_reduced_xor_heldout_sampler_20260530/summary/`
  - `data/hardware/20260529_fpga1_board2/restart_counterfactual/summary/`
  - `data/hardware/20260529_fpga1_board2/metadata/` only if the export remains metadata-only and excludes raw payloads.
- TVLSI experiment outputs:
  - `data/experiments/heldout_sampler_route_diff_20260530/`
  - `data/experiments/tvlsi_sampler_aperture_model_20260530/`

The existing evidence files already cite the key local evidence paths:

- `paper/RO_TRNG_tvlsi_sampler_aperture/evidence/claim_evidence_table.md`
- `paper/RO_TRNG_tvlsi_sampler_aperture/evidence/evidence_gap.md`
- `paper/RO_TRNG_tvlsi_sampler_aperture/evidence/figure_table_plan.md`

## Explicit Exclude List

Do not include in this checkpoint:

- TIM manuscript or TIM PDF changes under `paper/RO_TRNG_entropy_boundary/`.
- Raw captures and hardware binaries: `*.bin`, `*.bit`, `*.dcp`, packet dumps, and SHA256 sidecars unless a future archival snapshot explicitly wants them.
- Vivado transient products: `*.jou`, `*.log`, `.Xil/`, `.runs/`, `.cache/`, `.gen/`, `.hw/`, `.ip_user_files/`, `.sim/`.
- Generated manuscript build products: `*.aux`, `*.bbl`, `*.blg`, `*.fdb_latexmk`, `*.fls`, PDFs.
- Unrelated MLDSA/PQC files outside the RO_TRNG export scope.
- Any push or remote change from the working repository.

## GitHub Export Flow Review

Reviewed export repository:

- Export root: `E:\Project\MLDSA\RO_TRNG_github_export`
- Remote: `https://github.com/ghjiuzhi/RO_TRNG.git`
- Branch state at review time: `main...origin/main`
- Recent head: `532f27b Add 20260529 board2 experiment export snapshot`

Reviewed source-side export script:

- `scripts/update_github_export_snapshot.ps1`
- Dry run command used:
  - `powershell -ExecutionPolicy Bypass -File scripts\update_github_export_snapshot.ps1 -SnapshotTag 20260530_tvlsi_checkpoint -DryRun`
- Dry run result:
  - included files: `3011`
  - skipped files: `2276`
  - included size: `235.692 MiB`

Important export caveat:

- The current include roots cover `data/experiments` and scripts, but the reviewed script does not yet explicitly include `paper/RO_TRNG_tvlsi_sampler_aperture/` or the Board2 hardware summary roots under `data/hardware/20260529_fpga1_board2/`.
- Therefore, a TVLSI checkpoint export should first update the export include roots or perform a targeted manual copy into the export repository. Otherwise the GitHub snapshot can miss the TVLSI paper workspace and Board2 summary CSV/MD evidence.

Recommended export update before an actual push:

- Add `paper/RO_TRNG_tvlsi_sampler_aperture` to the include roots.
- Add summary-only Board2 roots:
  - `data/hardware/20260529_fpga1_board2/restart_reduced_xor_heldout_sampler_20260530/summary`
  - `data/hardware/20260529_fpga1_board2/restart_counterfactual/summary`
- Keep the existing binary/log/PDF exclusions.
- Run the export script once with `-DryRun`, inspect included/skipped manifests, then run without `-DryRun` only when the include set is correct.
- Commit and push from `E:\Project\MLDSA\RO_TRNG_github_export`, not from the MLDSA working repository.

Suggested future export commit message:

```text
Add TVLSI sampler-aperture evidence checkpoint
```

## Current Limits

- This checkpoint is an evidence freeze, not a calibrated physical proof.
- The current prediction table is useful because it preserves mismatches; it should not be described as a trained transfer model.
- The route audit supports sampler/context sensitivity, but it is not a fully isolated causal proof because non-sampler logic may also move.
- The next high-value step is the second held-out sampler/context experiment with frozen prediction outputs and PVT-linked manifesting.
