# RO_TRNG Placement/TDC Mechanism Study

This repository is a curated research package for an FPGA RO-TRNG placement-sensitivity and mechanism-analysis paper.

It contains the Verilog RTL, Vivado/XDC build scripts, UART capture scripts, SP800-90B input/result summaries, TDC analysis scripts, placement experiment metadata, and paper-facing evidence tables. Large raw hardware captures, bitstreams, Vivado generated directories, PDFs, executables, and packet-level dumps are intentionally excluded from the public snapshot.

## Current Research Position

The central claim is not simply that a new RO-TRNG design has high throughput or low resource cost. The current evidence supports a more physical mechanism-oriented result:

> FPGA RO-TRNG quality is strongly placement-sensitive, and the sampler-side implementation should be treated as part of the entropy-source boundary. The observed failures are not well explained by simple pairwise RO hard locking alone.

The strongest evidence chain is:

- Placement changes raw TRNG quality reproducibly on the measured Zynq-7020 board.
- `random1` is a repeatable poor placement; `random3` is a repeatable good continuous-stream placement.
- TDC pair measurements do not support a simple strong-locking explanation under the measured conditions.
- SP800-90B restart tests reveal fixed-position startup bias that is not visible from continuous-stream balance alone.
- Sampler-side and reduced-XOR counterfactual hardware experiments show that the final output can be governed by sampler-vector correlation and XOR cancellation, not only by one bad RO pair.

## SP800-90B Status

The repository now includes formal-size SP800-90B entropy-assessment evidence, not only early smoke tests.

Completed locally and summarized in this snapshot:

- SP800-90B `ea_non_iid` runs on sequential bit-symbol datasets, including 1M smoke runs and 8M full runs for key placements.
- Formal-size restart datasets using `1000 x 1000` bit symbols derived from hardware auto-stream restart captures.
- `ea_restart` results for `random1`, `random3`, repeat runs, and warmup scans.
- Restart column-bias diagnostics that identify fixed-position bias as the reason some formal restart sanity checks fail.

Key restart examples:

- `random3` formal restart, MSB bit-symbol input: `H_I=0.902345`, `X_cutoff=605`, `X_max=685`, restart sanity check failed.
- `random3` formal restart, LSB bit-symbol input: `H_I=0.828444`, `X_cutoff=632`, `X_max=685`, restart sanity check failed.
- `random1` formal restart, MSB bit-symbol input: `H_I=0.389520`, `X_cutoff=821`, `X_max=680`, validation test passed.
- `random1` formal restart, LSB bit-symbol input: `H_I=0.383737`, `X_cutoff=824`, `X_max=680`, validation test passed.
- `random3` warmup scan shows a transition: warmup0/8/10 fail, while warmup11/12/16 pass under the recorded tests.

Important caveat: these are formal-size SP800-90B entropy-assessment runs and restart sanity-check results, not a claim of complete SP800-90B certification. A compliance/certification claim would require a tighter validation package, clearer restart-equivalence argument, broader PVT/multi-board evidence, and final conditioning/component documentation.

Start with:

- `doc/sp800_90b_restart_execution_status_20260514.md`
- `doc/paper_claim_evidence_boundary_20260525.md`
- `doc/paper_draft_cn_v3_20260525.md`
- `data/sp800_90b/results_full8m_20260514/summary.md`
- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.md`
- `data/experiments/mechanism_evidence_chain_20260525/mechanism_evidence_chain_20260525.md`
- `data/experiments/reduced_xor_paper_artifacts_20260527/`

## Key Current Findings

- Placement strongly affects raw RO-TRNG quality on the measured Zynq-7020 board.
- `random1` is a repeatable bad continuous-stream case: 10MiB analysis gives low bit min-entropy and strong bias.
- `random3` is a repeatable good continuous-stream case: 10MiB analysis is close to balanced and high min-entropy.
- `same_column` shows why bit balance alone is insufficient: p1 can be near 0.5 while run/adjacent structure remains abnormal.
- Restart tests reveal that a continuous-stream "good" placement can still fail restart sanity due to fixed-column startup bias.
- Reduced-XOR counterfactuals show strongly biased same-data-RO directions, while excluding certain directions can recover near-balanced outputs.

## Repository Layout

- `doc/` - planning notes, status reports, result interpretation, paper drafts, and limitation documents.
- `rtl/` - original and added Verilog RTL, including restart, TDC, sampler, and reduced-XOR experiment tops.
- `scripts/` - Vivado build scripts, UART capture scripts, SP800-90B input preparation, analysis, plotting, and report generation.
- `fpga1/xc7z020clg400/lab_xdc/` - board/lab XDC constraints.
- `data/experiments/` - placement XDCs, queue CSVs, generated tables/figures, mechanism summaries, and export manifests.
- `data/sp800_90b/` - compact SP800-90B summaries, manifests, and result logs; large binary inputs are excluded.
- `data/hardware/20260511_fpga1_board1/` - metadata and compact analysis outputs; raw UART captures are excluded.
- `sim/SP800-90B_EntropyAssessment/` - lightweight local source subset for the NIST entropy-assessment toolchain.
- `third_party/libdivsufsort/` - dependency source used by the MinGW SP800-90B build route.

## Excluded On Purpose

- Raw capture files: `*.bin`
- Bitstreams and checkpoints: `*.bit`, `*.dcp`
- Vivado generated directories: `.Xil`, `.runs`, `.cache`, `.gen`, `.hw`, `.ip_user_files`, `.sim`
- Large packet-level dumps: `*.tdc_packets.csv`
- Generated executables/objects, PDFs, DOCX reports, and ZIP archives

The raw files remain on the local experiment machine. Their SHA256 hashes, dimensions, headers, metadata, and compact analysis summaries are preserved in the public evidence package where available.

## Useful Offline Commands

Most analysis scripts are offline-only and should not touch COM, JTAG, Vivado, or hardware unless their names clearly indicate capture or programming.

```powershell
python scripts/analyze_fast_mode_results.py
python scripts/summarize_trng_repeats.py
python scripts/summarize_90b_results.py
python scripts/make_restart_mechanism_table.py
python scripts/make_mechanism_evidence_chain_20260525.py
python scripts/make_reduced_xor_paper_artifacts_20260527.py
```

SP800-90B build route:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_90b_mingw.ps1
python scripts/prepare_90b_inputs.py --help
powershell -ExecutionPolicy Bypass -File scripts/run_90b_smoke.ps1 -Modes bps1_msb
python scripts/summarize_90b_results.py
```

Hardware scripts such as `scripts/run_fast_hardware_queue.ps1`, `scripts/program_and_capture_uart.ps1`, and `scripts/capture_uart.ps1` require the FPGA board, COM3/UART, and Vivado setup. Do not run multiple hardware queues in parallel because they contend for COM3, JTAG, and `hw_server`.
