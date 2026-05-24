# Fast Mode Status 20260523

## Hardware Status

- Current COM3/JTAG capture task: none.
- `hw_server` may remain resident.
- Last hardware queue: `restart_sampler_island_20260523`, completed with diagnostic failures and no valid formal restart dataset.

## Completed Today

### Sampler-Island 20MiB Confirmation

- Bitstream: `data/vivado_runs/fpga1_sampler_island/random1_sampler_island_local_x45y39_regs_x45y31/seed_1/RO_TRNG_top.bit`
- Output: `data/hardware/20260511_fpga1_board1/trng/random1_sampler_island_local_x45y39_regs_x45y31_program_20mib_20260523.bin`
- Bytes: `20 MiB`
- SHA256: `C42E39A9BC46909105678F20EE918D054C82564FA344FA2F8E1A761D0E0D95E4`
- XADC: `46.0 C -> 46.3 C`, `VCCINT=1.000 V`, `VCCAUX=1.796 V -> 1.794 V`
- `p1=0.5000507474`
- bit min-entropy: `0.9998535814`
- runs p-value: `0.6489840131`
- adjacent-equal ratio: `0.4999824375`
- byte min-entropy: `7.9855784492`

Window stability:

- 1MiB window `p1` range: `0.499794` to `0.500288`
- 5MiB window `p1` range: `0.499994` to `0.500106`
- 5MiB window bit min-entropy minimum: `0.999695`

Interpretation:

This confirms the earlier 5MiB programmed sampler-island result at 20MiB scale. Holding the `random1` data-RO placement fixed, sampler-side placement changes the source from strongly biased to near ideal. This is now the strongest causal mechanism evidence in the project.

### TDC Mechanism Preparation

Added a hypothesis-driven TDC plan:

- `doc/tdc_sampler_mechanism_experiment_plan_20260523.md`

Generated sampler-data TDC XDCs:

- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_baseline_sample_x36y35_ro4.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random1_local_sample_x45y39_ro4.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random3_sample_x36y35_ro0.xdc`
- `data/experiments/xdc_tdc_sampler_data/tdc_sampler_data_random3_sample_x36y35_ro3.xdc`

Added supporting scripts/queues:

- `scripts/generate_tdc_sampler_data_xdc.py`
- `scripts/build_tdc_sampler_data_bitstreams.ps1`
- `data/experiments/fast_mode/hardware_queue_tdc_sampler_data_20260523.csv`
- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl` now supports synth generics as tclarg 4.

## Updated Tables

- `data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv`
- `data/experiments/mechanism_hypothesis_20260523/mechanism_hypothesis_evidence_by_placement.csv`
- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.csv`
- `data/experiments/tdc_sampler_data_20260523/tdc_sampler_data_summary.md`
- `data/experiments/xadc_summary/xadc_capture_summary_20260523.csv`
- `data/experiments/xadc_summary/xadc_capture_summary_20260523.md`

### Sampler-Data TDC Queue

Completed six 2MiB sampler-data TDC captures:

| family | sampler | data_ro | phase_r range | nominal diff_std_ps range | interpretation |
| --- | --- | --- | ---: | ---: | --- |
| `random1` | baseline/local | 0, 4 | `-0.00247` to `0.00149` | `1977.16` to `1980.75` | no strong sampler-data locking split |
| `random3` | good reference | 0, 3 | `-0.00141` to `0.00224` | `1971.94` to `1978.30` | similar weak-correlation behavior |

Interpretation:

The sampler-data TDC line is now a useful negative control. It does not support a simple explanation where `random1` is bad because the sample RO hard-locks or strongly correlates with a selected data RO. This strengthens the more precise mechanism claim: the sampler side matters, but the decisive effect is likely in the sampling-register/routing/metastability aperture path rather than persistent pairwise RO phase locking. Raw TDC bins should be used only for relative/categorical comparisons until code-density calibration is added.

## Next Hardware Priority

1. Do not add more same-style sampler-data TDC repeats unless a new metric or design variant gives a falsifiable distinction.
2. Before formal sampler-island restart capture, build a small restart debug-header smoke variant. The first 2026-05-23 formal attempt produced 0-byte or partial files, so repeating the same 1000x125 queue is not useful yet.
3. If the restart debug-header smoke succeeds, rerun sampler-island restart warmup0/warmup12. If it fails, inspect restart FSM/header generation under the sampler-island constraints.
4. If time allows, build a routing/register ablation: hold sample RO fixed while moving only sampling registers or changing their local constraints.
5. Add code-density calibration only if the paper needs calibrated timing language; otherwise keep TDC as raw-bin negative-control evidence.

Decision goal:

- The next discriminating test should separate sample-RO placement from sampling-register/routing placement.
- Avoid spending board time on blind repeats that do not separate these mechanisms.

### Restart Sampler-Island Diagnostic Attempt

Prepared and built:

- `scripts/build_restart_sampler_island_20260523.ps1`
- `data/experiments/fast_mode/hardware_queue_restart_sampler_island_20260523.csv`
- `doc/restart_sampler_island_experiment_plan_20260523.md`

Capture outcome:

| variant | warmup | expected bytes | captured bytes | status |
| --- | ---: | ---: | ---: | --- |
| `sample_ro_local` | 0 | 125000 | 0 | no UART bytes |
| `sample_ro_local` | 12 | 125000 | 0 | no UART bytes |
| `sampler_island_local` | 0 | 125000 | 36529 | partial stream, then timeout |
| `sampler_island_local` | 12 | 125000 | 0 | no UART bytes |

These outputs are not valid SP800-90B restart inputs. The useful conclusion is engineering/mechanistic: restart auto-stream behavior is sensitive to sampler-side placement constraints, and the register-local variant differs from sample-RO-only. The next run should be a reduced debug-header smoke test, not another blind formal repeat.
