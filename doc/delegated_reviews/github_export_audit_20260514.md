# GitHub Export Audit 2026-05-14

## Executive Summary

`E:\Project\MLDSA\RO_TRNG_github_export` 是给 GPT/Claude/合作者看的 curated repo，不是完整 Vivado 工作目录。当前策略正确：上传脚本、RTL、约束、文档、结果表、metadata、SHA256；不要上传 raw `.bin`、`.bit`、`.dcp`、Vivado `.runs/.cache`、90B `.exe` 和大日志。

## Inputs Read

- `E:\Project\MLDSA\RO_TRNG_github_export\.gitignore`
- `doc/fast_mode_master_status_20260514.md`
- `doc/sp800_90b_restart_execution_status_20260514.md`
- `data/experiments/paper_artifacts_20260514/claims_vs_evidence.md`
- GitHub export git status during 2026-05-14 updates

## Findings

1. Export is suitable for external model review.

   It contains the evidence map, paper artifacts, status docs, restart scripts, SP800-90B scripts, and delegated reviews.

2. Raw data is intentionally excluded.

   `.gitignore` excludes `*.bin`, `*.bit`, `*.dcp`, `*.exe`, Vivado generated directories, and large logs. This prevents accidental upload of large or generated artifacts.

3. Restart pilot metadata is included without raw captures.

   The export contains `.metadata.json` and `.sha256.txt` for restart smoke/pilot, but not the raw `.bin` files. This is the right compromise for traceability.

4. The export repo is cleaner than the monorepo root.

   The main workspace has unrelated dirty Vivado/PQC files and large generated outputs. Do not use root `git status` as the publication/export status.

## Recommended Actions

- P0: Continue using `E:\Project\MLDSA\RO_TRNG_github_export` as the public review package.
- P0: Keep pushing status docs after each completed hardware milestone.
- P0: Do not relax `.gitignore` for `.bin`, `.bit`, `.dcp`, `.exe`, or Vivado generated directories.
- P1: Add a short top-level README section explaining that raw captures are available locally by SHA256 but omitted from GitHub.
- P1: Add a manifest of key local raw files and hashes for reproducibility without uploading large binaries.
- P2: If reviewers need raw data, publish a separate archive or release asset with selected compressed datasets and checksums.

## Snippets For README

```text
This repository is a curated analysis/export package. Large raw captures, generated bitstreams, Vivado implementation directories, and compiled NIST tools are intentionally excluded. Metadata and SHA256 files are provided so local raw datasets can be matched to the reported analyses.
```

## Open Questions

- Should selected small `.csv` intermediate files be included for full figure regeneration?
- Should a separate release asset contain the final formal datasets once the paper result set is frozen?
