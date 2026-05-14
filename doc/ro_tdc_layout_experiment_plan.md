# RO-TRNG Layout/TDC Experiment Plan

## Research Position

Plain inverter/LUT ring-oscillator TRNGs are already a mature topic. A stronger paper should treat the FPGA fabric as a physical noise and coupling medium, then connect:

`layout / routing / neighbor activity -> frequency, jitter, phase diffusion, coupling -> min-entropy and health-test behavior`.

The likely publishable contribution is not manual placement itself. It is a reproducible characterization and design methodology for layout-aware RO entropy sources.

## Baseline Already Present

- RTL TRNG: `rtl/RO_TRNG_top.v`, `rtl/entropy_source.v`
- RO counter measurement: `rtl/jitter_measure.v`, `rtl/CU.v`, `rtl/counter.v`
- Existing Zynq-7020 placement constraints: `fpga1/xc7z020clg400/xc7z020clg400.srcs/constrs_1/new/manual_ro_locbel_round1.xdc`
- Existing data:
  - `data/lutl/RO*.DAT`: per-RO counter dumps
  - `sim/*.DAT` and `sim/sel_ro/*.DAT`: raw TRNG bitstreams from parameter sweeps
- Analysis scripts added:
  - `scripts/analyze_ro_counter.py`
  - `scripts/analyze_trng_dataset.py`
  - `scripts/generate_ro_placement_xdc.py`

## Experiment Matrix

### E0: Baseline Counter Characterization

Goal: reproduce frequency, counter-distribution entropy, and count-derived jitter for current `RO2` to `RO9`.

Run:

```powershell
python scripts/analyze_ro_counter.py data/lutl --windows-ns 250,200,400,450,625,600,675,800 --out data/experiments/e0_lut_ro_counter.csv
```

The window values correspond to the existing script's `window_sizes_lutl = [50,40,80,90,125,120,135,160] * 5 ns`.

### E1: Raw Bitstream Quality for Existing Sweeps

Goal: compare bias, monobit/runs p-values, byte entropy, and bit min-entropy across existing TRNG dumps.

Run:

```powershell
python scripts/analyze_trng_dataset.py sim --glob *.DAT --out-dir data/experiments/e1_sim_top
python scripts/analyze_trng_dataset.py sim/sel_ro --glob *.DAT --out-dir data/experiments/e1_sel_ro
```

Use this as a quick screening layer. NIST SP800-22 and SP800-90B are still needed for paper claims.

### E2: Layout Sweep Without TDC

Goal: isolate whether RO cluster geometry changes output quality before adding TDC.

Generate example constraints:

```powershell
python scripts/generate_ro_placement_xdc.py --pattern compact --x0 44 --y0 43 --out fpga1/xc7z020clg400/xc7z020clg400.srcs/constrs_1/new/ro_compact_x44y43.xdc
python scripts/generate_ro_placement_xdc.py --pattern row --x0 44 --y0 43 --pitch 3 --out fpga1/xc7z020clg400/xc7z020clg400.srcs/constrs_1/new/ro_row_pitch3_x44y43.xdc
python scripts/generate_ro_placement_xdc.py --pattern checker --x0 44 --y0 43 --pitch 3 --out fpga1/xc7z020clg400/xc7z020clg400.srcs/constrs_1/new/ro_checker_pitch3_x44y43.xdc
```

For each bitstream, record:

- XDC file and Vivado seed
- Pblock/SLICE coordinate range
- `RO_NUM`, `RO_STAGES`, `SAMPLE_STAGES`
- UART capture length
- temperature/voltage if available
- SP800-22, SP800-90B IID/non-IID results

### E3: Neighbor-Aggressor Coupling Sweep

Goal: test the coupling hypothesis directly.

Add a controllable neighboring toggler block near, then far from, the RO cluster:

- idle
- low-frequency toggling
- high-frequency toggling
- pseudo-random toggling

Compare frequency drift, jitter collapse, adjacent-bit correlation, SP800-90B min-entropy, and health-test fail rate. This is stronger than only moving RO positions because it probes a mechanism.

### E4: TDC-Assisted Measurement

Goal: turn the experiment from black-box bit testing into physical timing evidence.

Minimum useful TDC:

- CARRY4 delay chain sampled by `clk_200m`
- thermometer-to-binary encoder
- optional bubble correction
- capture RO edge timestamp relative to reference clock
- UART/FIFO output mode for timestamp histograms

Measured features:

- per-edge phase bin distribution
- transition density near sampling boundary
- phase random-walk diffusion over lag
- pairwise phase correlation between ROs
- common-mode collapse under aggressor or injection-like conditions

## Paper Hypotheses

H1: Closely packed ROs have higher common-mode coupling and worse independence than spatially separated or routing-diverse ROs.

H2: High raw throughput can hide poor entropy when deterministic beating dominates; TDC phase histograms expose this earlier than NIST-only testing.

H3: A placement rule that maximizes frequency separation alone is insufficient; the objective must include jitter, pairwise correlation, and health-test stability.

H4: Neighbor activity can emulate part of the injection-locking risk surface, causing measurable entropy degradation even without external EM injection.

## Suggested Contribution Shape

1. A compact TDC measurement core for RO phase/jitter monitoring.
2. A layout/coupling characterization dataset across placement patterns and aggressor modes.
3. A stochastic or semi-empirical entropy model calibrated by TDC measurements.
4. An entropy-aware placement rule or constraint generator.
5. Validation through SP800-90B, NIST STS, and online health-test behavior.

## Important Risks

- UART at 115200 bps limits acquisition speed; use it for characterization, not throughput claims.
- Current scripts provide screening statistics, not formal certification.
- Existing `fpga1` constraints must be checked against the actual board clock pins before rebuilding.
- Carry-chain TDC placement must itself be constrained, otherwise bin widths vary too much for cross-run claims.
