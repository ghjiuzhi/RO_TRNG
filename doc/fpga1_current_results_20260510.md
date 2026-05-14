# FPGA1 RO-TRNG/TDC Current Results - 2026-05-10

## Build Status

Target board/project assumption: fpga1 is the Zynq-7020 Navigator V2 reproduction using a single-ended `sys_clk`.

| Artifact | Path | Status | Timing | DRC |
| --- | --- | --- | --- | --- |
| Compact RO_TRNG placement | `data/vivado_runs/fpga1_ro_trng_sweep/ro_compact_x44y43/seed_1/RO_TRNG_top.bit` | bit generated | WNS 1.518 ns, TNS 0, WHS 0.116 ns | 31 warnings, 0 errors |
| Checker RO_TRNG placement | `data/vivado_runs/fpga1_ro_trng_sweep/ro_checker_pitch3_x44y43/seed_1/RO_TRNG_top.bit` | bit generated | WNS 1.873 ns, TNS 0, WHS 0.106 ns | 31 warnings, 0 errors |
| TDC diagnostic top | `data/vivado_runs/fpga1_tdc_sysclk_inmem/RO_TDC_sysclk_top.bit` | bit generated | WNS 0.276 ns, TNS 0, WHS 0.121 ns | 3 warnings, 0 errors |

The remaining DRC warnings are expected for this class of experiment: allowed RO combinational loops and Zynq PS7-unused warning. The TDC timing violation observed before pipelining was removed by registering the corrected thermometer word before encoding/packetizing.

Additional layout matrix builds completed after the first compact/checker pair:

| Layout | Bitstream | Timing |
| --- | --- | --- |
| Same column, pitch 3 | `data/vivado_runs/fpga1_ro_trng_matrix/same_column_pitch3_x44y35/seed_1/RO_TRNG_top.bit` | WNS 2.038 ns, TNS 0, WHS 0.121 ns |
| Row, pitch 3 | `data/vivado_runs/fpga1_ro_trng_matrix/row_pitch3_x38y43/seed_1/RO_TRNG_top.bit` | WNS 1.852 ns, TNS 0, WHS 0.071 ns |
| Sparse, pitch 6 | `data/vivado_runs/fpga1_ro_trng_matrix/sparse_pitch6_x36y35/seed_1/RO_TRNG_top.bit` | WNS 1.702 ns, TNS 0, WHS 0.103 ns |
| Cross region | `data/vivado_runs/fpga1_ro_trng_matrix/cross_region_x36y25/seed_1/RO_TRNG_top.bit` | WNS 1.614 ns, TNS 0, WHS 0.121 ns |
| Far spread | `data/vivado_runs/fpga1_ro_trng_matrix/far_x20y25/seed_1/RO_TRNG_top.bit` | WNS 1.722 ns, TNS 0, WHS 0.120 ns |
| Random placement seed 1 | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed1_x36y35/seed_1/RO_TRNG_top.bit` | WNS 1.549 ns, TNS 0, WHS 0.121 ns |
| Random placement seed 2 | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed2_x36y35/seed_1/RO_TRNG_top.bit` | WNS 1.476 ns, TNS 0, WHS 0.127 ns |
| Random placement seed 3 | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed3_x36y35/seed_1/RO_TRNG_top.bit` | WNS 1.680 ns, TNS 0, WHS 0.118 ns |

TDC layout diagnostic builds:

| TDC Layout | Bitstream | Timing | DRC |
| --- | --- | --- | --- |
| Near RO pair | `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_near_x36y35/RO_TDC_sysclk_top.bit` | WNS 0.213 ns, TNS 0, WHS 0.129 ns | 3 warnings, 0 errors |
| Far RO pair | `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_far_x24y25/RO_TDC_sysclk_top.bit` | WNS 0.252 ns, TNS 0, WHS 0.121 ns | 3 warnings, 0 errors |

## Implemented Experiment Infrastructure

RTL:

- `rtl/tdc/RO_TDC_sysclk_top.v`: single-ended `sys_clk` TDC diagnostic top for fpga1.
- `rtl/tdc/carry4_tdc_chain.v`: CARRY4 tapped delay line.
- `rtl/tdc/tdc_sampler.v`: system-clock sampler.
- `rtl/tdc/tdc_bubble_correct.v`: simple thermometer bubble correction.
- `rtl/tdc/tdc_encoder.v`: thermometer-to-bin encoder.
- `rtl/tdc/tdc_lane.v`: pipelined TDC lane.
- `rtl/tdc/tdc_uart_packetizer.v`: 8-byte UART packet stream.

Vivado automation:

- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`: in-memory TDC build flow.
- `scripts/vivado/run_fpga1_ro_trng_sweep_inmem.tcl`: in-memory RO_TRNG placement build flow.
- `scripts/vivado/run_fpga1_ro_trng_sweep_matrix.ps1`: placement/seed sweep launcher.
- `scripts/vivado/run_fpga1_selected_matrix.ps1`: selected layout-matrix build launcher.

Analysis:

- `scripts/analyze_ro_counter.py`: frequency and count-jitter summary.
- `scripts/analyze_trng_dataset.py`: raw stream bias, byte entropy, min-entropy, run/autocorrelation summaries.
- `scripts/analyze_tdc_uart.py`: TDC UART packet decoder, code-density calibration, phase/jitter/correlation metrics.
- `scripts/merge_experiment_tables.py`: joins TDC, TRNG, RO counter, and Vivado run metrics into paper tables.
- `scripts/generate_ro_placement_xdc.py`: placement XDC generation.
- `scripts/generate_fpga1_experiment_matrix.py`: first fpga1 placement-matrix generator.
- `scripts/generate_tdc_ro_placement_xdc.py`: near/far TDC RO probe placement generator.

## Existing Data Summary

Counter-derived LUT RO results from `data/lutl` show RO frequencies from 286.873 MHz to 1061.163 MHz and estimated jitter standard deviations from 3.738 ps to 8.431 ps. These are useful as a pre-hardware baseline and as a sanity check for the TDC capture.

Simulation/raw-stream analysis indicates that low-mux or poorly selected configurations can be strongly biased, while larger selector sets are close to ideal byte min-entropy. This supports the paper direction: placement/topology changes should be evaluated through both physical timing observables and entropy-source statistics, not only NIST pass/fail.

## Hardware Collection Order

1. Burn `RO_TDC_sysclk_top.bit`, capture UART at 115200 baud, and decode with `scripts/analyze_tdc_uart.py`.
2. Run TDC code-density calibration and save the sidecar metadata described in `doc/hardware_collection_protocol_20260510.md`.
3. Burn each RO_TRNG matrix bitstream, capture equal-size raw UART streams, and analyze with `scripts/analyze_trng_dataset.py`.
4. Merge TDC/TRNG/Vivado summaries with `scripts/merge_experiment_tables.py`.

## Paper Direction

The feasible high-level claim is not "manual placement" or "using a TDC" alone. The stronger contribution is a layout-aware entropy characterization flow: controlled RO placement, on-chip TDC observables, code-density/bin calibration, raw entropy estimation, and a physical explanation for coupling/locking/phase-difference effects.

Relevant literature confirms the direction:

- NIST SP 800-90B requires entropy-source validation, min-entropy estimation, health testing, and source modeling.
- TROT shows that TDC-based extraction plus a stochastic model can be publishable when platform-specific jitter, TDC nonuniformity, placement, and min-entropy lower bounds are tied together.
- Ring-oscillator TRNGs are vulnerable to coupling/locking effects, including frequency injection, so placement-dependent coupling is a meaningful security-relevant phenomenon to characterize.
