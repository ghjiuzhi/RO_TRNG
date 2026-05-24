# Multi-Board Validation and Naming Plan - 2026-05-15

## Purpose

This document defines the offline plan for extending the current single-board RO-TRNG evidence chain to cross-board validation. It is a design and naming review only. It does not authorize hardware access, Vivado programming, COM3 capture, JTAG operations, or any new board run while hardware is paused.

The current strongest evidence is still single-board:

- Placement changes raw TRNG quality strongly on the current Zynq-7020 board.
- `random1` is the stable bad placement and `random3` is the stable good placement for continuous fast-mode data.
- Pair-specific TDC runs are useful mechanism evidence, but did not show conservative strong pair-level phase locking in the six measured pairs.
- Restart warmup is the clearest transient-window result: on the current board, `random3` warmup10 fails while warmup11/12 pass, and repeat02 reproduces the same boundary.

Multi-board validation should answer a narrower question: which observations are robust across boards, and which are board-specific manifestations of the same layout-sensitive mechanism?

## Board Identity Standard

Every hardware artifact must carry a stable `board_id`. The identifier should describe the physical board, not the placement, bitstream, host PC, COM port, or run date.

Recommended format:

```text
board_id = z7020_bNN
```

Examples:

- `z7020_b01`: current board, historically appearing in paths as `fpga1_board1`.
- `z7020_b02`: second physical board of the same FPGA/package/board family.
- `z7020_b03`: third physical board.

If board vendor/revision differs, extend the prefix rather than overloading the number:

```text
z7020_clg400_b01
z7020_clg400_b02
```

Minimum board manifest fields:

| field | required | note |
| --- | --- | --- |
| `board_id` | yes | Stable physical-board ID. |
| `fpga_part` | yes | Example: `xc7z020clg400`. |
| `board_model` | yes | Development board name or lab shorthand. |
| `board_revision` | if known | Silkscreen or vendor revision. |
| `serial_or_asset_tag` | if available | Keep private if needed, but record in lab notebook. |
| `host_id` | yes | Capture PC or workstation ID. |
| `uart_port` | yes | Example: `COM3`; do not treat as identity. |
| `jtag_adapter_id` | if available | Useful for debugging, not for grouping results. |
| `ambient_condition` | yes | At least room/bench condition; temperature/voltage if measured. |
| `operator` | yes | Initials are enough. |

Recommended path convention:

```text
data/hardware/YYYYMMDD_<board_id>/<experiment_family>/<run_name>.bin
```

Examples:

```text
data/hardware/20260516_z7020_b02/fast_mode/random3_run01_10mib_20260516.bin
data/hardware/20260516_z7020_b02/restart/random3_restart_auto_formal_bits_1000x125_warmup11_run01_20260516.bin
```

Do not reuse `fpga1_board1` for new boards. Preserve old paths as historical artifacts, but map them in summaries to `board_id=z7020_b01`.

## Run Naming Standard

Use names that make the comparison factors explicit:

```text
<placement>_<mode>_<protocol>_<size>_<warmup_or_probe>_<run_id>_<date>
```

For continuous fast-mode TRNG:

```text
random3_fast_trng_10mib_run01_20260516.bin
random1_fast_trng_20mib_repeat03_20260516.bin
```

For RO frequency:

```text
random3_ro_freq_fixed_5mib_run01_20260516.bin
```

For TDC pair:

```text
random3_tdc_pair_ro3_ro7_run01_20260516.bin
```

For restart auto-stream:

```text
random3_restart_auto_bits_1000x125_warmup11_run01_20260516.bin
```

Metadata must record:

- `board_id`
- `placement_id`
- `xdc_path`
- `rtl_top`
- `bitstream_path`
- `bitstream_sha256`
- `vivado_version`
- `vivado_seed`
- `git_commit_or_export_id`
- `capture_script`
- `capture_script_sha256` or Git hash
- `protocol_parameters`
- `raw_output_sha256`
- `derived_input_sha256` for MSB/LSB expanded SP800-90B inputs

## Same Bitstream vs Rebuild Per Board

Use two tiers because they answer different questions.

### Tier A: Same Bitstream Across Boards

Use the exact same `.bit` file on every compatible board when possible.

Purpose:

- Isolate chip-to-chip and board-to-board variation under identical implemented placement/routing.
- Avoid confusing board variation with implementation drift.
- Support the paper phrase "the same implemented design was evaluated on multiple physical boards."

Requirements:

- Same FPGA part/package/speed-grade compatibility.
- Same board clock/reset/UART wiring.
- Same `.bit` SHA256 recorded for all boards.
- Same capture scripts and protocol parameters.

Primary use:

- Cross-board replication of headline placements: `random1`, `random3`, and `original`/baseline.
- Cross-board restart warmup boundary check for `random3`.
- Cross-board TDC sanity for one or two already-important pairs.

### Tier B: Rebuild Per Board

Rebuild only when a board is not bitstream-compatible, or when board-specific constraints are unavoidable.

Purpose:

- Validate that the methodology survives normal implementation reproducibility constraints.
- Separate "physical board variation" from "Vivado implementation variation."

Requirements:

- Record XDC, seed, Vivado version, reports, and bitstream hash.
- Keep placement geometry identical at the logical `placement_id` level.
- Prefer fixed Vivado seed first; only sweep seeds if the experiment is explicitly about implementation variation.

Paper treatment:

- Same-bitstream results support stronger cross-board comparability.
- Rebuild-per-board results support methodology robustness, but must be reported as a separate factor.
- Do not pool same-bitstream and rebuild-per-board results without a factor label.

Recommended order:

1. Run Tier A same-bitstream validation on all compatible boards.
2. Only then add Tier B rebuild validation if reviewers are likely to ask whether the result depends on one routed implementation.

## Board-Level Required and Optional Captures

The minimum multi-board plan should be small enough to finish, but strong enough to answer reviewer attacks.

### Per-Board P0 Required

Run these on every additional compatible board.

| item | placements | size/protocol | purpose |
| --- | --- | --- | --- |
| Continuous TRNG formal | `random1`, `random3`, `original` if available | 10 MiB each | Replicate good/bad placement gap and baseline. |
| Continuous repeat | `random1`, `random3` | 5 MiB or 20 MiB, one repeat each | Check run-to-run stability without exploding queue length. |
| RO_FREQ fixed probe | `random1`, `random3` | same fixed protocol as current evidence | Link entropy gap to frequency/beat features. |
| Restart warmup boundary | `random3` | `1000 x 125` packed bytes, warmup10/11/12 | Test whether the observed boundary is board-specific or broadly reproducible. |
| Environment snapshot | all runs | before/after if possible | Record temperature/voltage context; do not overclaim if coarse. |

If time is limited, prioritize `random1/random3` continuous 10 MiB and `random3` warmup10/11/12 restart. That pair directly attacks the two main claims: placement gap and restart transient window.

### Per-Board P1 Recommended

| item | placements/pairs | size/protocol | purpose |
| --- | --- | --- | --- |
| Restart contrast | `random1` warmup0/8/11/12 | same as current plan | Show that pass/fail depends on cutoff and raw column bias, not only placement label. |
| TDC pair replication | `random1_ro4_ro5`, `random3_ro3_ro7` | same pair-specific protocol | Check whether no-strong-lock negative result is stable. |
| More placements | `compact`, `checker`, `sparse`, `row` | 5 or 10 MiB | Test whether ordering beyond random1/random3 generalizes. |
| Bit-order 90B inputs | MSB and LSB | derived from same raw captures | Keep bit-order sensitivity visible. |

### Per-Board P2 Optional

| item | purpose |
| --- | --- |
| Full placement matrix | Broad cross-board ranking, useful if time is abundant. |
| Temperature/voltage sweep | PVT boundary; valuable but should not block base multi-board validation. |
| Aggressor/toggler experiment | Stronger mechanism evidence, but separate from current placement/restart story. |
| Vivado seed sweep | Distinguish placement geometry from implementation variation. |

## Statistical Comparison Policy

Do not compare only pass/fail labels. Use a fixed set of metrics so board-to-board effects are visible even when tools classify both runs the same way.

### Continuous TRNG Metrics

For each `(board_id, placement_id, bitstream_id, run_id)` report:

- file size and SHA256
- `p1`
- fast bit min-entropy
- byte entropy
- adjacent-bit or short-lag correlation if available
- SP800-90B non-IID smoke `H_original` for MSB and LSB if generated
- IID route status only as a diagnostic; current evidence says non-IID should be the main route

Comparison views:

- Within-board contrast: `random3 - random1` for entropy metrics, and absolute difference for `p1 - 0.5`.
- Across-board distribution: median, min, max, and board count for each placement.
- Effect consistency: count boards where `random3` remains better than `random1` under the same metric.

Avoid claiming that a placement is universally best unless it wins across all tested boards and protocols.

### Restart Metrics

For each restart dataset report:

- packed raw SHA256
- MSB and LSB expanded SHA256
- `H_I` source and value
- `X_cutoff`
- `X_max`
- pass/fail
- `H_r`, `H_c`, and final min if available
- column diagnostic: worst raw byte/bit position, ones, zeros, `p1`, and number of positions over cutoff
- warmup bytes

Comparison views:

- Per board: warmup transition curve for `WARMUP_BYTES=10,11,12`.
- Across boards: first passing warmup among the tested values.
- Boundary robustness: whether `warmup10` fails and `warmup11/12` pass on each board.

Do not use `ea_restart` pass/fail alone as evidence that early fixed-position bias is absent. The random1 case already shows that a wider cutoff can pass while raw column bias remains visible.

### TDC and RO_FREQ Metrics

For each board/pair:

- RO frequency summary per oscillator
- pair frequency separation
- small-lag correlation summary
- strong-lock window count under the existing conservative criterion
- mean and max relevant TDC spread/correlation features

Comparison views:

- Mechanism consistency, not certification.
- Whether bad placements show repeatable frequency closeness, phase coverage issues, or correlation structures.
- Whether pair-specific TDC continues to show no conservative strong-lock windows.

Do not treat TDC bin width as an absolute calibrated time unless calibration is added.

## Minimum Tables for Paper/Appendix

Recommended cross-board tables:

1. Board manifest table:
   `board_id`, FPGA part, board model/revision, environment summary, compatible with same bitstream yes/no.

2. Bitstream manifest table:
   `bitstream_id`, placement, mode, top, XDC, Vivado seed/version, SHA256, same-bitstream group.

3. Continuous TRNG cross-board table:
   one row per board and placement, with `p1`, fast min-entropy, non-IID smoke entropy, and SHA256.

4. Restart warmup cross-board table:
   one row per board, placement, warmup, bit order, with `X_cutoff`, `X_max`, pass/fail, worst column, and SHA256.

5. Mechanism table:
   selected RO_FREQ/TDC features for `random1` and `random3`, tied to the entropy and restart outcomes.

## Paper Wording Boundaries

Use this language if only the current board is available:

- "On one Zynq-7020 board under room-temperature/default-voltage conditions, placement produced a large and repeatable raw entropy gap."
- "The observed restart warmup boundary is a board-, placement-, and protocol-specific result, reproduced on the same board across two runs."
- "The results motivate multi-board and PVT validation, which remains future work."

Use this language after two or more compatible boards complete Tier A same-bitstream validation:

- "Using the same implemented bitstream on multiple compatible Zynq-7020 boards, we observed the same direction of placement-dependent entropy change between `random1` and `random3`."
- "The restart transient-window effect was evaluated across boards using the same auto-stream protocol; the reported warmup threshold is the observed range for the tested boards, not a universal device constant."

Use this language only after rebuild-per-board validation is also done:

- "The placement-aware methodology remained effective when the design was rebuilt for additional boards, although implementation seed and routing remain explicit experimental factors."

Avoid these claims:

- "This proves the placement rule generalizes to all FPGAs."
- "This is a full SP800-90B certification."
- "Near RO placement necessarily causes strong injection locking."
- "The TDC bins are calibrated absolute time measurements."
- "Warmup11 is a universal threshold."
- "A restart pass means no fixed-position bias exists."

## Recommended Execution Sequence When Hardware Returns

1. Assign and record `board_id` for every physical board before programming anything.
2. Confirm part/package/board compatibility for Tier A same-bitstream reuse.
3. For each additional board, collect P0 continuous TRNG data for `random1`, `random3`, and baseline.
4. Run RO_FREQ fixed probes for `random1/random3`.
5. Run `random3` restart warmup10/11/12 with the same auto-stream protocol.
6. Generate MSB/LSB derived inputs and restart column diagnostics immediately after each capture.
7. Only after P0 completes on at least one additional board, decide whether P1 random1 restart contrast or TDC pair replication is higher value.

This sequence keeps the first cross-board result focused: same design, same protocol, new physical board, same headline comparisons.

## Final Recommendation

For the paper, treat multi-board validation as a replication layer, not as a new exploratory matrix. The first additional board should receive a narrow, same-bitstream P0 queue centered on `random1`, `random3`, and `random3` warmup10/11/12. Rebuild-per-board experiments are valuable, but they should be labeled as a second factor and not mixed with same-bitstream board replication.

