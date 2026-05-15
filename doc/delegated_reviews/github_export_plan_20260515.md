# GitHub / GPT / Claude Export Plan 2026-05-15

Scope: `E:\Project\MLDSA\RO_TRNG`

Purpose: prepare a curated external-analysis package for GitHub, GPT, Claude, and human reviewers. This is not a Vivado working-copy mirror. It should preserve source, scripts, constraints, documentation, and small derived evidence while excluding raw captures, implementation products, logs, and machine-generated build trees.

## Recommended Upload Categories

Upload these categories by default:

1. RTL source
   - `rtl/*.v`
   - `rtl/debug/*.v`
   - `rtl/restart/*.v`
   - `rtl/tdc/*.v`
   - Rationale: small, human-reviewable, central to design analysis.

2. Analysis and orchestration scripts
   - `scripts/*.py`
   - `scripts/*.ps1` when they are analysis, conversion, summarization, queue generation, capture wrappers, or reproducibility helpers.
   - `scripts/vivado/*.tcl` and other small Tcl scripts that document reproducible Vivado project/build steps.
   - Rationale: lets external reviewers inspect analysis flow and regenerate summaries from local or separately shared data.

3. Hand-authored constraints and IP descriptors
   - `fpga/RO_TRNG.srcs/constrs_*/new/*.xdc`
   - `fpga/RO_TRNG.srcs/sources_1/ip/*/*.xci`
   - `fpga1/xc7z020clg400/lab_xdc/*.xdc`
   - `fpga1/xc7z020clg400/xc7z020clg400.srcs/constrs_1/**/*.xdc`
   - `fpga1/xc7z020clg400/xc7z020clg400.srcs/sources_1/ip/*/*.xci`
   - `data/experiments/xdc_examples/*.xdc`
   - `data/experiments/xdc_matrix/*.xdc`
   - `data/experiments/xdc_restart/*.xdc`
   - `data/experiments/xdc_ro_freq/*.xdc`
   - `data/experiments/xdc_tdc/*.xdc`
   - `data/experiments/xdc_tdc_pairs/*.xdc`
   - Rationale: placement and clocking constraints are part of the experiment definition. Prefer authored/generated experiment XDC over copied files buried in `.runs` or `.gen`.

4. Project descriptors, selectively
   - `fpga/RO_TRNG.xpr`
   - `fpga1/xc7z020clg400/xc7z020clg400.xpr`
   - Include only if reviewers need Vivado project context. They may contain absolute/local paths, so inspect before public release.

5. Documentation and review notes
   - `doc/*.md`
   - `doc/delegated_reviews/*.md`
   - Small PDFs only when they are authored project references and legally shareable. Avoid literature PDFs and private thesis/manuscript files unless explicitly cleared.
   - Rationale: status, claims/evidence mapping, runbooks, and paper notes are the most useful context for external model review.

6. Small derived result artifacts
   - `data/experiments/**/*.md`
   - `data/experiments/**/*.csv`
   - `data/experiments/**/*.json`
   - `data/experiments/**/*.svg`
   - `data/experiments/**/*.png`
   - `data/sp800_90b/**/summary.md`
   - `data/sp800_90b/**/summary.csv`
   - `data/sp800_90b/**/manifest.csv`
   - `data/sp800_90b/**/manifest.json`
   - `data/sp800_90b/restart_results_*/**/*.metadata.json`
   - `data/sp800_90b/restart_results_*/**/*.version.txt`
   - Rationale: these are compact summaries, tables, figures, manifests, and metadata that support claims without uploading raw entropy streams.

7. Testbenches and tiny simulation helpers
   - `sim/*_tb.v`
   - `sim/set_timestamp.tcl`
   - `sim/timestamp.txt`
   - Rationale: useful for source-level review. Do not include large `.DAT`, compiled STS objects/executables, or xsim build outputs.

8. Third-party source, only when license-compatible and needed
   - `third_party/libdivsufsort/README.md`
   - `third_party/libdivsufsort/LICENSE`
   - Source files needed to rebuild SP800-90B support, if the export is intended to be self-contained.
   - Rationale: source is acceptable if license is preserved; compiled objects and executables are not.

## Recommended Exclusion Categories

Exclude these categories by default:

1. Raw entropy and hardware capture data
   - `*.bin`
   - `*.DAT`
   - Large raw `.txt` capture files
   - `data/hardware/**`
   - `data/sp800_90b/inputs_*/**`
   - Full restart input matrices or byte streams.
   - Reason: large, hardware-specific, not suitable for normal GitHub review. Share separately by archive/release asset only if needed, with SHA256.

2. Vivado implementation products
   - `*.bit`
   - `*.dcp`
   - `*.hwdef`
   - `*.vdi`
   - `*.vds`
   - `*.wdf`
   - `*.rpx`
   - `*.pb`
   - `*.str`
   - `.Xil/`
   - `*.runs/`
   - `*.cache/`
   - `*.gen/`
   - `*.hw/`
   - `*.ip_user_files/`
   - `*.sim/`
   - `xsim.dir/`
   - Reason: generated, bulky, machine/local-state dependent. Keep only concise reports if manually selected.

3. Logs, journals, and local process outputs
   - `*.jou`
   - `*.log`
   - `*.backup.jou`
   - `*.backup.log`
   - `xvlog.log`
   - `xvlog.pb`
   - `runme.log`
   - Automation stdout/stderr logs.
   - Reason: noisy, local, and often very large.

4. Compiled binaries and caches
   - `*.exe`
   - `*.o`
   - `*.obj`
   - `*.a`
   - `__pycache__/`
   - `*.pyc`
   - Reason: rebuildable and platform-specific.

5. Large generated reports unless specifically curated
   - `*.rpt`
   - `*.rpx`
   - Full Vivado report directories under `data/vivado_runs/**`
   - Exception: a small selected report can be copied into a curated `reports/` or `data/experiments/...` folder if it directly supports a claim.

6. Private or legally ambiguous documents
   - `论文/**`
   - Literature PDFs or private drafts not intended for public sharing.
   - Reason: copyright/privacy risk.

7. Archives of generated working trees
   - `*.zip`
   - Example: `fpga1.zip`
   - Reason: opaque, large, and likely to reintroduce excluded artifacts.

## Suggested Export Staging Layout

Continue using `E:\Project\MLDSA\RO_TRNG_github_export` as the curated package instead of publishing the full workspace. Recommended top-level layout:

```text
RO_TRNG_github_export/
  README.md
  rtl/
  scripts/
  fpga1/
    xc7z020clg400/
      lab_xdc/
      xc7z020clg400.srcs/constrs_1/
      xc7z020clg400.srcs/sources_1/ip/
  sim/
    *_tb.v
  doc/
  data/
    experiments/
    sp800_90b/
      summaries, manifests, metadata only
  third_party/
    source and licenses only
```

The export package should explain that raw captures and bitstreams are omitted intentionally, and that metadata/SHA256/manifests identify local or separately archived datasets.

## Suggested `.gitignore` Rules For Export Package

Use deny-by-default for dangerous/generated extensions, then selectively include curated summaries:

```gitignore
# Raw captures and generated FPGA artifacts
*.bin
*.bit
*.dcp
*.jou
*.log
*.pb
*.rpx
*.wdb
*.wcfg
*.str
*.vdi
*.zip
*.exe
*.o
*.obj
*.a
*.DAT

# Vivado / xsim generated directories
.Xil/
*.runs/
*.cache/
*.gen/
*.hw/
*.ip_user_files/
*.sim/
xsim.dir/

# Python/build caches
__pycache__/
*.pyc

# Large derived packet dumps
*.tdc_packets.csv

# Local automation logs
data/experiments/fast_mode/*stdout.log
data/experiments/fast_mode/*stderr.log
data/experiments/fast_mode/logs/
data/experiments/fast_mode/short_queue_logs/

# Private / copyright-risk material
论文/
```

If the main workspace itself gets a root `.gitignore`, keep the same exclusions there, but do not rely on the root repo as the publication boundary. The export staging directory remains the safer release artifact.

## Practical Upload Checklist

Before upload or external sharing:

1. Refresh the staged export from curated source folders only.
2. Confirm `git status --short` inside `E:\Project\MLDSA\RO_TRNG_github_export`, not the monorepo parent.
3. Search for excluded artifacts before sharing:
   - `*.bin`, `*.bit`, `*.dcp`, `*.jou`, `*.log`, `*.DAT`, `*.exe`, `*.pyc`, `*.zip`
   - `.Xil`, `.runs`, `.cache`, `.gen`, `.hw`, `.ip_user_files`, `.sim`, `xsim.dir`
4. Confirm large CSV files are intentional. Keep summary/table CSVs; exclude packet dumps and raw captures.
5. Confirm public/legal status of PDFs and files under `论文/`.
6. Include a README note: raw data is available locally or separately by SHA256, but not committed.

## Bottom Line

Recommended upload: `rtl`, selected `scripts`, authored/generated experiment `xdc`, selected `xci` and `xpr`, `doc/*.md`, delegated review notes, small `data/experiments` tables/figures/metadata, SP800-90B summaries/manifests/metadata, small testbenches, and license-preserved third-party source.

Recommended exclusion: raw hardware data, `.bin`, `.DAT`, bitstreams, checkpoints, Vivado runs/cache/gen/hw/ip_user_files/sim trees, logs/journals, compiled binaries, Python caches, large packet dumps, archives, and private/copyright-risk documents.
