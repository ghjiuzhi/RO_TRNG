# TDC Reset-Enable Status 20260524

## Decision

The reset-aligned TDC experiment has been redirected back onto the original,
already-validated TDC UART path.

The failed finite-header approach is no longer the main path. It emitted finite
bytes too early relative to PC-side serial opening and XADC timing. The working
path now preserves the original continuous `0xA5` packetizer and only adds a
delayed RO enable bit.

## Implemented Working Path

- RTL: `rtl/tdc/RO_TDC_pair_reset_enable_top.v`
- Build script: `scripts/build_tdc_reset_enable_bitstreams.ps1`
- Smoke queue: `data/experiments/fast_mode/hardware_queue_tdc_reset_enable_smoke_20260524.csv`
- Matrix queue: `data/experiments/fast_mode/hardware_queue_tdc_reset_enable_matrix_20260524.csv`
- Analysis: `scripts/analyze_tdc_startup_diffusion.py`

This top is intentionally close to `RO_TDC_pair_sysclk_top`:

- same `tdc_lane`
- same `tdc_uart_packetizer`
- same `uart_tx`
- same 8-byte `A5 seq coarse bin_a bin_b flags` packet format
- only difference: RO enable starts at 0, flips to 1 after a delay, and is
  exported as `flags[0]`

## Smoke Result

Smoke bitstream:

- `data/vivado_runs/fpga1_tdc_reset_enable/tdc_reset_enable_random1_baseline_ro0_smoke/RO_TDC_pair_reset_enable_top.bit`

Successful capture:

- `data/hardware/20260511_fpga1_board1/tdc_reset_enable/tdc_reset_enable_random1_baseline_ro0_smoke_delay10s_no_xadc.bin`
- bytes: `262144`
- SHA256: `B20C1824316B2E66FBEF1271D3E1606AEF3F2D138CCEEC2DBD0D76EDCAD442E6`
- decoded packets: `32767`
- sequence gaps: `0`
- enable edge index: `9537`
- pre-enable packets: `9537`
- post-enable packets: `23230`

The edge is visible in the decoded stream:

```text
9532..9536: flags=152, bin_a=64, bin_b=64, ro_enable=0
9537:       flags=195, bin_a=0,  bin_b=36, ro_enable=1
```

Startup diffusion analysis:

- output dir: `data/experiments/tdc_reset_enable_smoke_20260524_delay10s`
- `H(diff)` after enable: `6.68352277`
- early `H(diff)`: `5.86388142`
- warmup12-equivalent `H(diff)`: `5.86690967`
- transition `H(diff)`: `12.8652098`
- warmup transition `H(diff)`: `6.97293666`
- longest same diff-bin run: `3`

Interpretation:

This smoke validates the experimental instrument, not the final mechanism claim.
It proves that the original continuous TDC UART path can capture a reset-aligned
RO-enable boundary inside the file. The full mechanism comparison requires the
matrix runs.

## Next Matrix

Build:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build_tdc_reset_enable_bitstreams.ps1 -Mode matrix
```

Then run one queue at a time:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_fast_hardware_queue.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_enable_matrix_20260524.csv `
  -Port COM3 `
  -Baud 115200 `
  -StatusMarkdown doc\tdc_reset_enable_matrix_status_20260524.md `
  -LogDir data\experiments\fast_mode\tdc_reset_enable_matrix_logs_20260524 `
  -ContinueOnError
```

Use `-RecordXadc` only after confirming capture timing still leaves the enable
edge inside the file. XADC adds a long and variable delay before COM3 opens.

After capture:

```powershell
python scripts\analyze_tdc_startup_diffusion.py `
  --input data\hardware\20260511_fpga1_board1\tdc_reset_enable\tdc_reset_enable_random1_baseline_ro0_2mib.bin `
  --input data\hardware\20260511_fpga1_board1\tdc_reset_enable\tdc_reset_enable_random3_goodref_ro0_2mib.bin `
  --input data\hardware\20260511_fpga1_board1\tdc_reset_enable\tdc_reset_enable_random1_sampler_local_ro0_2mib.bin `
  --out-dir data\experiments\tdc_reset_enable_matrix_20260524 `
  --label random1_baseline `
  --label random3_goodref `
  --label random1_sampler_local `
  --early-packets 1024 `
  --window-packets 16384 `
  --lag 1
```

## Paper Logic

The reset-enable TDC line tests:

- whether startup bins are more concentrated than later bins
- whether warmup12-equivalent packets diffuse more than warmup0 packets
- whether random1 bad placement differs from random3 good reference
- whether sampler-local repair changes startup diffusion

Possible outcomes:

- If bad placement has lower early/warmup transition entropy or longer
  residence, TDC gives positive phase-diffusion evidence.
- If all TDC startup metrics look similar while TRNG/restart differs, TDC
  strengthens the negative-control claim and pushes the mechanism toward
  sampling-register/routing/aperture behavior.

## Matrix Result 2026-05-24

The three-run minimum matrix completed with the original continuous packetizer
path.

| label | file | bytes | enable edge | post-enable packets |
| --- | --- | ---: | ---: | ---: |
| `random1_baseline` | `data/hardware/20260511_fpga1_board1/tdc_reset_enable/tdc_reset_enable_random1_baseline_ro0_2mib.bin` | `2097152` | `9595` | `252548` |
| `random3_goodref` | `data/hardware/20260511_fpga1_board1/tdc_reset_enable/tdc_reset_enable_random3_goodref_ro0_2mib.bin` | `2097152` | `9582` | `252561` |
| `random1_sampler_local` | `data/hardware/20260511_fpga1_board1/tdc_reset_enable/tdc_reset_enable_random1_sampler_local_ro0_2mib.bin` | `2097152` | `9644` | `252499` |

Analysis output:

- `data/experiments/tdc_reset_enable_matrix_20260524/tdc_startup_diffusion.summary.csv`
- `data/experiments/tdc_reset_enable_matrix_20260524/tdc_startup_diffusion.windows.csv`
- `data/experiments/tdc_reset_enable_matrix_20260524/tdc_startup_diffusion.summary.md`

Key reset-aligned metrics:

| label | H(diff) | early H(diff) | warmup12 H(diff) | transition H(diff) | warmup transition H(diff) | same-diff ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `random1_baseline` | `6.67227` | `6.54038` | `6.54209` | `13.2961` | `9.85683` | `0.0113444` | `4` | `-0.00117893` |
| `random3_goodref` | `6.69450` | `6.58148` | `6.58243` | `13.3466` | `9.89424` | `0.0109954` | `3` | `0.000272926` |
| `random1_sampler_local` | `6.71817` | `6.60532` | `6.60266` | `13.3895` | `9.85561` | `0.0109585` | `3` | `-0.000525189` |

Initial interpretation:

- This is not evidence of strong pairwise locking. Autocorrelation remains close
  to zero and same-bin residence is short in all three runs.
- There is a weak but directionally useful diffusion ordering:
  `random1_sampler_local` has the highest overall and early differential-bin
  entropy, while `random1_baseline` is lowest. `random3_goodref` is between them.
- The differences are modest, so paper wording should be cautious:
  reset-aligned TDC gives boundary/weak-positive evidence for startup diffusion
  differences, but does not by itself prove the sampler-island repair mechanism.
- Combined with the much larger TRNG improvement from sampler-island placement,
  this supports the paper claim that the dominant effect is not simple persistent
  RO-RO hard locking. The stronger mechanism remains sampler-side
  implementation, routing/register placement, and sampling aperture behavior.

Recommended next step:

1. Repeat the reset-enable matrix once more for stability if board time allows.
2. Add a second data RO pair such as RO4 for `random1 baseline/local` only if the
   first repeat shows the same ordering.
3. Keep TDC claims relative/raw-bin only until code-density calibration exists.

## Repeat02 and RO4 Update

The RO0 matrix was repeated once and the ordering was stable:

| placement | repeats | mean H(diff) | mean early H(diff) | mean transition H(diff) |
| --- | ---: | ---: | ---: | ---: |
| `random1_baseline` | 2 | `6.67450` | `6.54875` | `13.3012` |
| `random3_goodref` | 2 | `6.69528` | `6.60829` | `13.3477` |
| `random1_sampler_local` | 2 | `6.71884` | `6.62594` | `13.3904` |

The next discriminating expansion, RO4, was built and captured twice:

| placement | repeats | mean H(diff) | mean early H(diff) | mean transition H(diff) |
| --- | ---: | ---: | ---: | ---: |
| `random1_baseline_ro4` | 2 | `6.60577` | `6.48960` | `13.1661` |
| `random1_sampler_local_ro4` | 2 | `6.70120` | `6.63113` | `13.3578` |

RO4 is the strongest reset-enable TDC evidence so far. Moving the sampler from
the baseline site to the local sampler site raises mean `H(diff)` by about
`0.095` bit and mean early `H(diff)` by about `0.142` bit across two repeats.
At the same time, autocorrelation stays close to zero and longest same-bin runs
remain short. This supports a startup phase-diffusion/sampling-aperture
mechanism and continues to argue against simple persistent pairwise RO hard
locking.

A good-reference `random3` data-RO contrast was then added:

| placement | repeats | mean H(diff) | mean early H(diff) | mean transition H(diff) |
| --- | ---: | ---: | ---: | ---: |
| `random3_goodref` | 2 | `6.69528` | `6.60829` | `13.3477` |
| `random3_goodref_ro3` | 2 | `6.67366` | `6.54893` | `13.3007` |

This result is an important boundary condition. `random3_goodref_ro3` drops
toward the `random1_baseline` startup-diffusion level, so the mechanism should
not be written as a simple family-level statement such as "random3 is good and
random1 is bad." The stronger claim is that startup diffusion is shaped by the
sample RO, the selected data RO, and their physical/routing geometry. The
`random1_sampler_local_ro4` improvement still supports sampler-side control,
but the data-RO/sampler pair relationship must be treated as part of the entropy
source boundary.

Updated outputs:

- `data/experiments/tdc_reset_enable_stability_20260524/tdc_reset_enable_repeat_stability.csv`
- `data/experiments/tdc_reset_enable_stability_20260524/tdc_reset_enable_repeat_stability.md`
- `data/experiments/mechanism_correlation_20260524/mechanism_correlation_master_by_placement.csv`
- `data/experiments/mechanism_correlation_20260524/mechanism_correlation_master_table_20260524.md`
