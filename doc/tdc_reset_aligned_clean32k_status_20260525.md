# TDC reset-aligned clean32k status 20260525

## Goal

Build a clean reset-aligned TDC capture path for the mechanism paper. The
previous 32k matrix produced useful raw `0xA5` packet streams, but those files
start at a packet boundary rather than at the 16-byte `TDCR` header. That means
they are useful as startup/diffusion comparisons, but should be described
cautiously in the paper.

The clean32k path keeps the same TDC RTL and packet format, but rebuilds the
matrix with `START_DELAY_CYCLES=16000000000` so that the serial port is already
open long before the FPGA emits the `TDCR` header.

## Current Diagnosis

- Smoke reset-aligned bitstreams used an 80 s post-configuration delay and
  captured the `TDCR` header correctly.
- Matrix bitstreams used `START_DELAY_CYCLES=200000`, only about 1 ms at
  200 MHz. `program_hw_devices` returns much later than that, so the matrix
  header and early bytes are emitted before the PC-side read loop begins.
- Therefore the missing `TDCR` header in the 32k matrix is a capture timing
  artifact, not physical TDC evidence.

## First Clean Point

Enabled queue row:

| run | warmup | placement | expected bytes | purpose |
| --- | ---: | --- | ---: | --- |
| `tdc_reset_random1_baseline_ro0_clean32k_warmup0` | 0 | random1 baseline | 262160 | prove clean `TDCR` + 32768 packet capture |

The remaining five rows are present in
`data/experiments/fast_mode/hardware_queue_tdc_reset_aligned_clean32k_20260525.csv`
but disabled until this first point passes.

## First Clean Point Result

`tdc_reset_random1_baseline_ro0_clean32k_warmup0_preopen_20260525` completed on
real hardware.

- file:
  `data/hardware/20260511_fpga1_board1/tdc_reset_aligned/tdc_reset_random1_baseline_ro0_clean32k_warmup0._preopen_20260525.bin`
- bytes: `262160`
- SHA256: `2A41FA5EB26E0671C72C3CCA21F5465FA59AF8044F098D9767F5304F35C4A3A9`
- first 16 bytes: `5444435201DD05010000000080881352`
- decoded header:
  `TDCR`, version `1`, pair id `1501`, family id `1`, warmup packets `0`,
  capture packets `32768`, sample divider `5000`, trailer `0x52`
- XADC after: `47.0 C`, `VCCINT=1.000 V`, `VCCAUX=1.796 V`,
  `VCCBRAM=1.000 V`

This confirms that the clean32k method gives a defensible reset/header-aligned
TDC capture. The next step is the remaining five clean32k rows.

## Remaining Clean32k Matrix Result

The remaining five clean32k bitstreams were built and captured on real
hardware. Together with the first clean point, the full six-point matrix is now
available as `TDCR`-aligned data.

| run | bytes | first16 | XADC after | status |
| --- | ---: | --- | --- | --- |
| `random1_baseline_warmup0` | `262160` | `5444435201DD05010000000080881352` | `47.0 C`, `VCCINT=1.000 V` | complete |
| `random1_baseline_warmup12` | `262160` | `5444435201DE0501000C000080881352` | `47.1 C`, `VCCINT=1.000 V` | complete |
| `random3_goodref_warmup0` | `262160` | `5444435201DF05030000000080881352` | `47.4 C`, `VCCINT=1.000 V` | complete |
| `random3_goodref_warmup12` | `262160` | `5444435201E00503000C000080881352` | `47.1 C`, `VCCINT=1.000 V` | complete |
| `random1_sampler_local_warmup0` | `262160` | `5444435201E105010000000080881352` | `47.2 C`, `VCCINT=1.000 V` | complete |
| `random1_sampler_local_warmup12` | `262160` | `5444435201E20501000C000080881352` | `46.8 C`, `VCCINT=1.000 V` | complete |

Unified analysis artifacts:

```text
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.summary.csv
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.summary.md
data/experiments/tdc_reset_aligned_clean32k_all_20260525/tdc_reset_aligned_clean32k_all_20260525.windows.csv
```

Mechanism evidence table:

```text
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.csv
data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md
```

Key clean32k TDC readings at `warmup_start=0`:

| label | H(diff) | early H(diff) | transition H(diff) | same ratio | longest run | autocorr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `random1_baseline_warmup0` | `6.75886` | `6.53655` | `13.1434` | `0.009949` | `3` | `-0.00828` |
| `random1_baseline_warmup12` | `6.66619` | `6.44347` | `12.9741` | `0.011658` | `3` | `0.000004` |
| `random3_goodref_warmup0` | `6.61583` | `6.43642` | `12.8973` | `0.013153` | `3` | `-0.00922` |
| `random3_goodref_warmup12` | `6.60778` | `6.46444` | `12.8768` | `0.012940` | `3` | `-0.00613` |
| `random1_sampler_local_warmup0` | `6.65464` | `6.43888` | `12.9439` | `0.013031` | `3` | `-0.00083` |
| `random1_sampler_local_warmup12` | `6.73356` | `6.50239` | `13.0993` | `0.010651` | `3` | `0.00186` |

Interpretation:

- The full clean matrix gives negative/control evidence against simple pairwise
  RO hard locking: same-bin residence is about 1%, longest same-differential-bin
  run is only 3, and small-lag autocorrelation is close to zero.
- `random1_sampler_local_warmup12` has the highest H(diff) and transition
  H(diff) in this matrix. This is weak positive evidence that sampler-local
  placement can improve startup phase diffusion, but it is not strong enough by
  itself to explain the much larger restart/TRNG changes.
- Combined with the sample-RO bidirectional counterfactual loop, the paper
  should write TDC as a mechanism constraint: it rules out hard-locking as the
  dominant explanation and pushes the main causal boundary toward the sampler RO,
  sampling registers, local routing, and sampling aperture.

## Commands

Build first clean point:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_reset_aligned_bitstreams.ps1 -Mode clean32k_p0
```

Capture first clean point:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_tdc_reset_aligned_preopen_queue_20260525.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_clean32k_20260525.csv `
  -OutRoot data\experiments\tdc_reset_aligned_clean32k_20260525 `
  -RecordXadcAfter `
  -ContinueOnError
```

Build remaining clean32k points:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_tdc_reset_aligned_bitstreams.ps1 -Mode clean32k_remaining
```

Capture remaining clean32k points:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_tdc_reset_aligned_preopen_queue_20260525.ps1 `
  -QueueCsv data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_clean32k_remaining_20260525.csv `
  -OutRoot data\experiments\tdc_reset_aligned_clean32k_remaining_20260525 `
  -RecordXadcAfter `
  -ContinueOnError
```

## Interpretation Rule

If the first 16 bytes are `54444352...52`, the capture is cleanly
reset/header-aligned and can replace the earlier raw-packet 32k point for the
same run. If it still starts with `A5`, the next fix should be command-gated
start or a much longer post-program delay, not another blind repeat.
