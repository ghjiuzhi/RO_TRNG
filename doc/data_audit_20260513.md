# RO_TRNG data audit 2026-05-13

Scope:

- Metadata: `data/hardware/20260511_fpga1_board1/metadata/*.json`
- TRNG binaries: `data/hardware/20260511_fpga1_board1/trng/*.bin`
- Analysis summaries: `data/hardware/20260511_fpga1_board1/trng/analysis_*/trng_summary.csv`
- Repeat tables: `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_run.md`, `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`

No hardware collection, COM port, JTAG, hw_server, or Vivado action was performed. I reran:

```powershell
python scripts\summarize_trng_repeats.py
```

The script regenerated the repeat CSV/Markdown tables and reported `Included 19 captures; excluded 16 captures.`

## Executive summary

- Complete valid formal/repeat TRNG captures: 19.
- Complete formal coverage: 10/10 placements.
- Complete repeat coverage: 9/10 placements.
- Missing complete repeats: `same_column`.
- Metadata-analysis-bin consistency for the 19 valid captures: OK. For each valid capture, metadata `bytes_requested == bytes_captured`, bin size matches, analysis summary bytes match, and metadata SHA256 matches the binary.
- Important audit caveat: `summarize_trng_repeats.py` starts from metadata, so bin-only partial files are not shown in its excluded table. This audit lists them separately below.

## Complete valid formal/repeat runs

These are the runs currently valid for formal/repeat tables.

| placement | formal run | formal bytes | repeat run | repeat bytes | coverage |
| --- | --- | ---: | --- | ---: | --- |
| checker | `checker_run01` | 10485760 | `checker_repeat02_5mib` | 5242880 | formal + repeat complete |
| compact | `compact_run01` | 10485760 | `compact_repeat02_5mib` | 5242880 | formal + repeat complete |
| cross_region | `cross_region_run02` | 10485760 | `cross_region_repeat02_5mib` | 5242880 | formal + repeat complete |
| far | `far_run01` | 10485760 | `far_repeat02_5mib` | 5242880 | formal + repeat complete |
| random1 | `random1_run01` | 10485760 | `random1_repeat02_5mib` | 5242880 | formal + repeat complete |
| random2 | `random2_run01` | 10485760 | `random2_repeat02_5mib` | 5242880 | formal + repeat complete |
| random3 | `random3_run01` | 10485760 | `random3_repeat02_5mib` | 5242880 | formal + repeat complete |
| row | `row_run01` | 10485760 | `row_repeat02_5mib` | 5242880 | formal + repeat complete |
| same_column | `same_column_run01` | 10485760 |  |  | formal only; repeat missing |
| sparse | `sparse_run01` | 10485760 | `sparse_repeat02_5mib` | 5242880 | formal + repeat complete |

## Latest repeat result summary

Latest complete valid repeat is `cross_region_repeat02_5mib`, ended `2026-05-13 20:59:52`, 5 MiB, p1 `0.500011396`, bit min-entropy `0.999967117`, monobit p `0.882647301`, runs p `0.561737791`.

| repeat run | end time | bytes | p1 | bit min-entropy | monobit p | runs p | byte min-entropy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cross_region_repeat02_5mib` | 2026-05-13 20:59:52 | 5242880 | 0.500011396 | 0.999967117 | 0.882647301 | 0.561737791 | 7.96623289 |
| `checker_repeat02_5mib` | 2026-05-13 20:40:47 | 5242880 | 0.499947119 | 0.999847425 | 0.493372771 | 0.239635009 | 7.96410121 |
| `random2_repeat02_5mib` | 2026-05-13 20:23:47 | 5242880 | 0.491030312 | 0.974348355 | 0 | 0 | 7.79591799 |
| `row_repeat02_5mib` | 2026-05-13 15:42:10 | 5242880 | 0.473337555 | 0.925049507 | 0 | 0 | 7.34742388 |
| `far_repeat02_5mib` | 2026-05-13 15:28:25 | 5242880 | 0.491642475 | 0.976084602 | 0 | 0 | 7.79024204 |
| `sparse_repeat02_5mib` | 2026-05-13 14:04:08 | 5242880 | 0.464140511 | 0.900073341 | 0 | 0 | 7.15552960 |
| `compact_repeat02_5mib` | 2026-05-13 13:55:29 | 5242880 | 0.500059223 | 0.999829128 | 0.443022427 | 0.098042379 | 7.97347656 |
| `random3_repeat02_5mib` | 2026-05-13 13:46:25 | 5242880 | 0.499971128 | 0.999916694 | 0.708421881 | 0.048701545 | 7.97396076 |
| `random1_repeat02_5mib` | 2026-05-13 13:37:01 | 5242880 | 0.337669373 | 0.594376522 | 0 | 0 | 4.80477392 |

## Partial and excluded files

### Bin-only partial or orphan TRNG files

These files are not represented by metadata and are not included by `summarize_trng_repeats.py`.

| file | observed bytes | reason |
| --- | ---: | --- |
| `cross_region_run01.bin` | 1697816 | missing metadata; missing analysis summary; partial, below 10485760-byte formal target |
| `random1_run02_partial_timeout_8692840.bin` | 8692840 | missing metadata; missing analysis summary; filename indicates timeout partial; below 10485760-byte formal target |
| `original_fpga1_smoke01.bin` | 0 | missing metadata; missing analysis summary; empty smoke/orphan file |

### Metadata-backed excluded captures

These are excluded by the repeat summary script and should stay out of formal/repeat tables.

| capture | bytes | reason |
| --- | ---: | --- |
| `checker_smoke01` | 1048576 | smoke, not formal/repeat |
| `compact_smoke01` | 1048576 | smoke, not formal/repeat |
| `cross_region_smoke01` | 1048576 | smoke, not formal/repeat |
| `far_smoke01` | 1048576 | smoke, not formal/repeat |
| `original_fpga1_program_capture01` | 1024 | program/smoke style capture, not formal/repeat |
| `random1_smoke01` | 1048576 | smoke, not formal/repeat |
| `random2_smoke01` | 1048576 | smoke, not formal/repeat |
| `random3_smoke01` | 1048576 | smoke, not formal/repeat |
| `row_smoke01` | 1048576 | smoke, not formal/repeat |
| `same_column_smoke01` | 1048576 | smoke, not formal/repeat |
| `sparse_smoke01` | 1048576 | smoke, not formal/repeat |
| `tdc_far_run01` | 2097152 | metadata kind is not `trng` |
| `tdc_near_run01` | 2097152 | metadata kind is not `trng` |
| `tdc_near_run02` | 2097152 | metadata kind is not `trng` |
| `tdc_near_smoke03` | 1024 | metadata kind is not `trng` |
| `tdc_near_smoke_direct01` | 1024 | metadata kind is not `trng` |

## Metadata and analysis matching

Counts observed:

| item | count |
| --- | ---: |
| metadata JSON files | 35 |
| TRNG `.bin` files | 33 |
| `trng_summary.csv` rows/files by capture id | 30 |
| valid formal/repeat captures | 19 |
| metadata-backed exclusions | 16 |
| bin-only partial/orphan files | 3 |
| analysis rows with neither metadata nor bin | 0 |
| SHA256 mismatches among metadata-backed TRNG files | 0 |

Valid-run matching checks:

- `metadata.capture_id` matches the analysis row capture id.
- `metadata.output_file` points to an existing TRNG binary for valid formal/repeat runs.
- `metadata.bytes_requested` equals `metadata.bytes_captured`.
- binary file size equals metadata `bytes_captured`.
- analysis `bytes` equals binary file size.
- metadata SHA256 equals recomputed SHA256 of the binary.

No mismatch was found for the 19 valid formal/repeat runs.

## Missing collection for complete matrix

Required to reach 10/10 formal + repeat coverage:

| placement | missing item | target |
| --- | --- | --- |
| `same_column` | complete repeat capture with metadata and analysis | 5242880 bytes |

No additional formal 10 MiB capture is required for the current placement matrix: all 10 placements already have one complete formal run.
