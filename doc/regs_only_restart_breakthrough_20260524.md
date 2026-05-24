# regs-only Restart Breakthrough 20260524

## What Ran

- Variant: `random1_sampler_regs_only_x45y31`
- Hardware: `z7020_b01`
- UART: `COM3`, `115200`
- Bitstreams:
  - `data/vivado_runs/restart_auto_random1_regs_only_formal_bits_1000x125_warmup0_header_delay60s/RO_TRNG_restart_auto_top.bit`
  - `data/vivado_runs/restart_auto_random1_regs_only_formal_bits_1000x125_warmup12_header_delay60s/RO_TRNG_restart_auto_top.bit`
- Dataset format: `1000 x 125` packed restart bytes, expanded to `1000 x 1000` bit symbols for `ea_restart`
- Repeats: `run01`, `run02`
- XADC: all associated restart summary rows show valid readings; VCCINT stayed about `1.000 V`

## Result

`regs-only` nearly fixes the 20MiB continuous stream and exposes a non-monotonic SP800-90B restart warmup passband.

| warmup | repeats | status | X_cutoff | X_max range | overall p1 range |
| ---: | ---: | --- | ---: | ---: | ---: |
| 0 | 2 | failed | 572 | 756-802 | 0.498425-0.499146 |
| 4 | 2 | failed | 572 | 733-751 | 0.407103-0.407970 |
| 5 | 2 | passed | 572 | 560-561 | 0.497894-0.498602 |
| 6 | 2 | passed | 572 | 551-554 | 0.496280-0.497339 |
| 8 | 2 | passed | 572 | 566-566 | 0.482728-0.484294 |
| 10 | 2 | passed | 572 | 554-565 | 0.499174-0.500018 |
| 11 | 2 | failed | 572 | 688-701 | 0.558805-0.559210 |
| 12 | 2 | failed | 572 | 601-609 | 0.452171-0.453785 |
| 16 | 1 | failed | 572 | 586-586 | 0.466933 |

## Interpretation

This is a strong mechanism result:

1. `regs-only` continuous stream is near ideal, so sampling registers/routing are causal for steady-state bias.
2. `regs-only` restart still fails, so continuous-stream quality is not enough to certify startup robustness.
3. The restart-safe region is not monotonic. Warmup `5/6/8/10` passes, while adjacent warmups `4` and `11` fail across repeats.
4. The failure mode changes with warmup: warmup0 is dominated by fixed-column hotspots; warmup4/11/12 are dominated by global p1 shifts or mixed global/column effects.
5. A reset-enable TDC re-analysis at warmup-window starts `4/5/10/11/12` did not show an analogous H(diff) jump, so the passband is probably not a simple two-RO raw-bin phase-diffusion threshold.

The best paper-level claim is:

> Sampling-register/routing placement is sufficient to repair steady-state continuous bias, proving that the sampler path is part of the entropy-source boundary. SP800-90B restart experiments reveal a narrow non-monotonic startup passband, and pairwise TDC does not reproduce the pass/fail boundary. Therefore restart robustness is controlled by the real sampling path and early output-position behavior, not only by pairwise RO locking or by waiting longer.

## Sampler Snapshot Diagnostics

Additional sampler-path diagnostics were implemented after the restart passband result.

First, a continuous post-start sampler snapshot captured 1024 consecutive frames after one startup. This showed only weak sampled-bit bias and did not reproduce the formal restart pass/fail boundary:

| formal warmup reference | snapshot type | rand p1 range | key interpretation |
| --- | --- | ---: | --- |
| warmup 4/5/10/11 | continuous after one start | 0.440430-0.506836 | continuous sampler state does not explain restart passband by itself |

Second, a restart-aligned sampler snapshot repeated mini-restarts and captured the same early sampler/output position across runs. This exposed strong startup-position determinism. A smoke run at raw warmup 4 showed `rand p1=0.921875` and fixed sampled/stage bits, proving that the diagnostic sees the hidden startup structure.

The byte-aligned restart snapshot then matched formal `WARMUP_BYTES=N` to raw snapshot warmup `8N`, because the restart FIFO writes 1 bit and reads 8-bit UART bytes. Summary:

| formal warmup bytes | snapshot warmup bits | restart reference | rand p1 | stage_xor H | fixed sampled bits | heavy sampled bits |
| ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 4 | 32 | failed/global-low | 0.470703 | 7.301296 | 15 | 42 |
| 5 | 40 | passed | 0.485352 | 6.642463 | 12 | 43 |
| 10 | 80 | passed | 0.465820 | 7.785172 | 0 | 17 |
| 11 | 88 | failed/global-high | 0.490234 | 7.758783 | 0 | 4 |

This refines the claim. The sampler path is highly structured at restart-aligned positions, but a single captured output bit is not sufficient to explain all formal restart outcomes. In particular, formal warmup 11 fails globally while the single byte-aligned snapshot bit is close to balanced. The next diagnostic must therefore capture a complete post-warmup byte, not just one bit position, so that the eight output positions used by the formal restart byte stream can be compared against the restart column-bias table.

## Key Artifacts

- `data/experiments/sampler_regs_only_20260524/random1_sampler_regs_only_restart_summary_20260524.md`
- `data/experiments/sampler_regs_only_20260524/random1_sampler_regs_only_restart_mode_summary_20260524.md`
- `data/experiments/sampler_snapshot_20260524/restart_aligned_sampler_snapshot_summary_cap1024_20260524.md`
- `data/experiments/sampler_snapshot_20260524/restart_aligned_bits_sampler_snapshot_summary_cap1024_20260524.md`
- `rtl/tdc/RO_TRNG_sampler_snapshot_top.v`
- `rtl/tdc/RO_TRNG_restart_aligned_snapshot_top.v`
- `data/experiments/tdc_reset_enable_warmup_edges_20260524/tdc_reset_enable_warmup_edges_interpretation.md`
- `data/experiments/restart_summary_20260524/restart_result_summary_20260524.md`
- `data/experiments/mechanism_correlation_20260524/mechanism_correlation_master_table_20260524.md`
- `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup0_run01/`
- `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup0_run02/`
- `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup12_run01/`
- `data/experiments/paper_artifacts_20260524/restart_column_bias_random1_sampler_regs_only_formal_bits_warmup12_run02/`

## Next Experiments

The next hardware experiment should not be another broad continuous-stream repeat or another isolated two-RO TDC repeat. It should directly target the true sampling path:

- a restart-position diagnostic top that emits early sampled bytes plus row/position markers for warmup `4/5/10/11`;
- a sampler-register diagnostic top that exposes selected `sampled_data` lanes or per-stage XOR groups around the 64 sampling registers;
- if time allows, compare regs-only against full sampler-island under the same passband protocol.
