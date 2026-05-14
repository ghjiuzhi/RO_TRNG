# SP800-90B/NIST Evidence Integration Plan

Date: 2026-05-14

Scope: offline evidence planning only. Do not touch hardware, Vivado, COM/JTAG, or `hw_server` while following this plan.

## 1. Repository status

- SP800-90B EntropyAssessment is already present at `sim/SP800-90B_EntropyAssessment`.
- The local 90B tree includes `README.md`, `cpp/Makefile`, and sample files in `bin/`.
- NIST SP800-22 STS is also present at `sim/sts-2.1.2`, but STS pass/fail evidence is not a substitute for SP800-90B entropy-source estimation.
- No internet download is required for the 90B route. If binaries are not built on a given machine, build them from the existing local source only.

## 2. Raw files to test first

Primary sequential datasets, complete 10 MiB TRNG captures:

| Role | Raw file | Bytes | 90B use |
| --- | --- | ---: | --- |
| Baseline | `data/hardware/20260511_fpga1_board1/trng/original_fpga1_run01_10mib.bin` | 10485760 | Baseline source comparison |
| Random1 | `data/hardware/20260511_fpga1_board1/trng/random1_run01.bin` | 10485760 | Main proposed placement |
| Random2 | `data/hardware/20260511_fpga1_board1/trng/random2_run01.bin` | 10485760 | Placement contrast |
| Random3 | `data/hardware/20260511_fpga1_board1/trng/random3_run01.bin` | 10485760 | Main proposed placement / best candidate check |
| Compact | `data/hardware/20260511_fpga1_board1/trng/compact_run01.bin` | 10485760 | Dense layout contrast |
| Sparse | `data/hardware/20260511_fpga1_board1/trng/sparse_run01.bin` | 10485760 | Sparse layout contrast |
| Row | `data/hardware/20260511_fpga1_board1/trng/row_run01.bin` | 10485760 | Same-row structure contrast |
| Same column | `data/hardware/20260511_fpga1_board1/trng/same_column_run01.bin` | 10485760 | Same-column structure contrast |
| Checker | `data/hardware/20260511_fpga1_board1/trng/checker_run01.bin` | 10485760 | Alternating placement contrast |
| Far | `data/hardware/20260511_fpga1_board1/trng/far_run01.bin` | 10485760 | Physical separation contrast |
| Cross region | `data/hardware/20260511_fpga1_board1/trng/cross_region_run02.bin` | 10485760 | Cross-region placement contrast |

Repeat datasets for stability and paper tables:

| Role | Raw file pattern | Bytes each | 90B use |
| --- | --- | ---: | --- |
| Repeat run | `data/hardware/20260511_fpga1_board1/trng/*_repeat02_5mib.bin` | 5242880 | Secondary reproducibility check |
| Smoke run | `data/hardware/20260511_fpga1_board1/trng/*_smoke01.bin` | 1048576 | Only quick sanity checks; not headline evidence |

Do not use partial or zero-byte captures as headline 90B evidence:

| Raw file | Reason |
| --- | --- |
| `random1_run02_partial_timeout_8692840.bin` | Partial timeout capture; useful only as an auxiliary robustness check |
| `cross_region_run01.bin` | Short partial capture compared with formal 10 MiB run |
| `original_fpga1_smoke01.bin` | Zero bytes |
| `original_fpga1_program_capture01.bin` | 1024 bytes, too small for meaningful 90B evidence |

TDC and RO-frequency captures should be handled separately from the TRNG output stream. They can support mechanism analysis, code-density plots, and correlation arguments, but should not be mixed into the main entropy-source sequential dataset unless the paper explicitly defines them as the assessed noise-source symbol stream.

## 3. Input format preparation

The EntropyAssessment programs expect each symbol to occupy one byte. For a binary source, use `bits_per_symbol=1` and store each bit as byte value `0x00` or `0x01`. For byte-level assessment, use `bits_per_symbol=8` and keep the raw byte stream.

Local helper script:

```powershell
python scripts\prepare_90b_inputs.py `
  --out-dir data\sp800_90b\inputs_20260514 `
  --max-bytes 1000000
```

Recommended explicit conversion for the main formal files:

```powershell
python scripts\prepare_90b_inputs.py `
  data\hardware\20260511_fpga1_board1\trng\random1_run01.bin `
  data\hardware\20260511_fpga1_board1\trng\random3_run01.bin `
  --mode bit-symbols-msb `
  --mode byte-symbols `
  --max-bytes 1000000 `
  --out-dir data\sp800_90b\inputs_20260514
```

The script writes `manifest.csv` and `manifest.json` with source path, source SHA-256, offset, read length, representation, output path, output length, and output SHA-256. This is the audit trail to cite in paper artifacts.

Bit order note: `bit-symbols-msb` matches the bit order used by the current Python bit-statistics script. Keep it as the default unless the UART packet format is documented as LSB-first; if that is later confirmed, run `--mode bit-symbols-lsb` as a sensitivity check and report both.

## 4. Command templates

Build local 90B tools only from the checked-in source:

```powershell
cd sim\SP800-90B_EntropyAssessment\cpp
make iid
make non_iid
make restart
make conditioning
```

Linux/WSL style commands from the 90B `cpp` directory:

```bash
./ea_non_iid -i -a ../../../data/sp800_90b/inputs_20260514/random3_run01_bps1_msb.bin 1 > ../../../data/sp800_90b/results_20260514/random3_run01_bps1_msb.non_iid.txt
./ea_iid     -i -a ../../../data/sp800_90b/inputs_20260514/random3_run01_bps1_msb.bin 1 > ../../../data/sp800_90b/results_20260514/random3_run01_bps1_msb.iid.txt
./ea_non_iid -i -a ../../../data/sp800_90b/inputs_20260514/random3_run01_bps8.bin 8 > ../../../data/sp800_90b/results_20260514/random3_run01_bps8.non_iid.txt
```

PowerShell template if native executables are built:

```powershell
New-Item -ItemType Directory -Force data\sp800_90b\results_20260514 | Out-Null
sim\SP800-90B_EntropyAssessment\cpp\ea_non_iid.exe -i -a data\sp800_90b\inputs_20260514\random3_run01_bps1_msb.bin 1 *> data\sp800_90b\results_20260514\random3_run01_bps1_msb.non_iid.txt
sim\SP800-90B_EntropyAssessment\cpp\ea_iid.exe     -i -a data\sp800_90b\inputs_20260514\random3_run01_bps1_msb.bin 1 *> data\sp800_90b\results_20260514\random3_run01_bps1_msb.iid.txt
```

For high-level paper evidence, use `ea_non_iid` as the conservative headline estimate. Use `ea_iid` only as a diagnostic and only claim IID if the IID tests pass and the design/measurement story justifies IID. RO-TRNG sources usually need the non-IID route.

Restart testing requires a row dataset as described by SP800-90B Section 3.1.4.1. The existing sequential `.bin` files are not restart datasets. A future collection should capture independent restarts, typically 1000 restarts by 1000 symbols, and write one byte per symbol in row-major order:

```bash
./ea_restart -n restart_rows_random3_bps1.bin 1 <H_I_from_non_iid>
```

Conditioning assessment template, if the RTL/paper defines a conditioning stage:

```bash
./ea_conditioning <n_in> <n_out> <narrowest_width> <h_in>
```

If the TRNG output is raw and unconditioned, state that no conditioning reduction is claimed.

## 5. Output table structure

Create one machine-readable summary table after running the tools:

| Column | Meaning |
| --- | --- |
| `dataset_id` | Stable name, e.g. `random3_run01_bps1_msb` |
| `source_file` | Original raw capture path |
| `source_sha256` | SHA-256 of original raw capture |
| `prepared_file` | 90B input file path |
| `prepared_sha256` | SHA-256 of prepared file |
| `placement` | `original`, `random1`, `random3`, etc. |
| `sample_role` | `formal`, `repeat`, `smoke`, `partial`, or `restart` |
| `bytes_raw` | Source bytes used |
| `symbols` | Number of one-byte symbols in prepared file |
| `bits_per_symbol` | `1` or `8` |
| `bit_order` | `msb`, `lsb`, or `byte` |
| `tool` | `ea_non_iid`, `ea_iid`, `ea_restart`, or `ea_conditioning` |
| `tool_version_path` | Local tool path, preferably with git commit if available |
| `command` | Exact command line used |
| `iid_result` | pass/fail/NA |
| `h_original` | Initial min-entropy per symbol from 90B output |
| `h_bitstring` | Bitstring entropy result when reported |
| `h_submitter` | Claimed entropy used for restart/conditioning, if any |
| `restart_pass` | pass/fail/NA |
| `conditioning_h_out` | Final entropy after conditioning, if applicable |
| `result_file` | Saved stdout/stderr text path |
| `notes` | Any exclusion, warning, or interpretation note |

Paper-facing tables should report the conservative non-IID min-entropy per bit for the main raw bitstream, plus repeat-run variability. Keep byte-symbol results as auxiliary, because byte-level min-entropy can obscure bitstream assumptions.

## 6. Current script metrics that cannot replace SP800-90B

The following existing metrics are useful screening and visualization evidence, but they are not SP800-90B entropy-source validation:

| Existing script/metric | Why it helps | Why it cannot replace 90B |
| --- | --- | --- |
| `scripts/analyze_trng_dataset.py` `p1`, `monobit_p`, `runs_p` | Fast bias and simple run checks | Only a small subset of statistical behavior; no SP800-90B estimator suite |
| `bit_min_entropy` from one-symbol frequency | Gives a quick most-common-bit bound | Ignores dependencies, Markov behavior, compression estimates, collision estimates, and restart tests |
| `shannon_entropy_byte` | Measures average byte distribution spread | Shannon entropy is not min-entropy and is not the 90B assessed value |
| `min_entropy_byte` | Quick most-common-byte bound | Byte-symbol MCV alone is not the full non-IID assessment |
| `scripts/summarize_trng_repeats.py` means/stds | Good reproducibility table across placements | Aggregates pre-90B metrics and cannot prove source entropy |
| NIST STS in `sim/sts-2.1.2` | Randomness test suite for output streams | SP800-22 pass/fail does not estimate source min-entropy and does not satisfy SP800-90B |
| TDC code-density / RO-frequency analysis | Supports physical mechanism and placement argument | Mechanism evidence is complementary; it is not a 90B sequential/restart assessment of the entropy source |
| SHA-256 metadata | Ensures traceability and reproducibility | Integrity evidence only; no entropy estimate |

## 7. Evidence route for a high-level paper

1. Prepare inputs from all complete 10 MiB formal captures using `bit-symbols-msb` and `byte-symbols`.
2. Run `ea_non_iid` on the 1-bit symbol inputs and report the conservative assessed min-entropy.
3. Run `ea_iid` as a diagnostic. Do not claim IID unless both tool output and source model justify it.
4. Repeat `ea_non_iid` on the 5 MiB repeat captures for placements used in the main claims.
5. Add a restart dataset collection to the future hardware protocol. Existing sequential captures do not satisfy restart-test format.
6. If a conditioning function is claimed, run `ea_conditioning` and report the final entropy after reduction.
7. Keep STS, monobit/runs, TDC, RO-frequency, and placement-correlation results as supporting evidence around the 90B core.

## 8. Immediate no-hardware next actions

- Run `python scripts/prepare_90b_inputs.py --max-bytes 1000000` to generate a small first-pass 90B input set.
- Build/check local EntropyAssessment binaries only if the machine already has the required compiler/libraries.
- Run one short `ea_non_iid` job on a prepared 1-bit symbol file to validate plumbing before launching the full matrix.
- Add future restart collection to the lab protocol, but do not attempt restart claims from the current sequential files.
