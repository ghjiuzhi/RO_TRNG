# GitHub export snapshot plan 2026-05-25

## Why this is needed

The working directory `E:\Project\MLDSA\RO_TRNG` is not an independent Git repository. Its Git root is `E:\Project\MLDSA`, whose `origin` remote points to `https://github.com/ghjiuzhi/MLDSA.git`.

The publishable RO_TRNG repository is the separate export repository:

```text
E:\Project\MLDSA\RO_TRNG_github_export
origin = https://github.com/ghjiuzhi/RO_TRNG.git
```

Therefore, the safe workflow is:

1. Curate RO_TRNG-only files into `RO_TRNG_github_export`.
2. Exclude raw captures, bitstreams, checkpoints, Vivado generated directories, executables, PDFs, and large packet dumps.
3. Preserve reproducibility through RTL, scripts, constraints, metadata, analysis summaries, and SHA256 manifests.
4. Commit locally in the export repository.
5. Push only when explicitly requested.

## What is included

- `doc/`: plans, status reports, result interpretations, paper drafts, handoff notes.
- `rtl/`: original and added Verilog tops for TDC, restart, FIFO diagnostic, and sampler-side experiments.
- `scripts/`: capture, programming, analysis, SP800-90B, plotting, and export scripts.
- `fpga1/xc7z020clg400/lab_xdc/`: board/lab constraints.
- `data/experiments/`: XDC matrices, compact derived tables, summaries, figures, and routed diff outputs.
- `data/sp800_90b/`: manifests and compact 90B outputs.
- `data/hardware/20260511_fpga1_board1/metadata`: capture metadata and XADC summaries.
- `data/hardware/.../analysis*`: compact CSV/MD/JSON analysis outputs under restart/TDC/TRNG directories.

## What is excluded

- Raw UART captures: `*.bin`
- Bitstreams/checkpoints: `*.bit`, `*.dcp`
- Vivado generated products: `.Xil`, `.runs`, `.cache`, `.gen`, `.hw`, `.ip_user_files`, `.sim`
- Large packet dumps: `*.tdc_packets.csv`
- Any single file larger than 5 MiB by default.
- Build products: `*.exe`, `*.o`, `*.obj`, `*.a`
- PDFs and zip archives.

## Current scientific delta since the GitHub version

The GitHub repository was last pushed on 2026-05-15. The local work after that adds the most important mechanism evidence:

- `random1_sampler_regs_only_x45y31` continuous stream is near ideal, showing that sampler-side placement can repair steady-state output.
- Restart formal tests show warmup-dependent pass/fail behavior.
- Pair-TDC evidence weakens the simple hard-locking explanation.
- FIFO/compact diagnostics separate readout/control effects from sampler-side physical effects.
- The sample-RO locked compact diagnostic restores warmup4 failure, providing causal evidence that the sample RO physical implementation is part of the entropy-source boundary.

## Command

From `E:\Project\MLDSA\RO_TRNG`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\update_github_export_snapshot.ps1 -SnapshotTag 20260525 -MaxFileMiB 5
```

Then inspect and commit in:

```powershell
cd E:\Project\MLDSA\RO_TRNG_github_export
git status --short
git diff --stat
git add .
git commit -m "Update RO_TRNG mechanism evidence snapshot"
```

Do not push until requested.
