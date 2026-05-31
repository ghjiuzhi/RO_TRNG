param(
    [string]$SourceRoot = "E:\Project\MLDSA\RO_TRNG",
    [string]$ExportRoot = "E:\Project\MLDSA\RO_TRNG_github_export",
    [string]$SnapshotTag = "20260525",
    [ValidateSet("Default", "Tvlsi")]
    [string]$Profile = "Default",
    [double]$MaxFileMiB = 5.0,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$SourceRoot = (Resolve-Path $SourceRoot).Path
if (-not (Test-Path $ExportRoot)) {
    throw "ExportRoot does not exist: $ExportRoot"
}
$ExportRoot = (Resolve-Path $ExportRoot).Path

$defaultIncludeRoots = @(
    "README.md",
    "doc",
    "paper/RO_TRNG_entropy_boundary",
    "rtl",
    "scripts",
    "sim/SP800-90B_EntropyAssessment",
    "third_party/libdivsufsort",
    "fpga1/xc7z020clg400/lab_xdc",
    "data/experiments",
    "data/sp800_90b",
    "data/hardware/20260511_fpga1_board1/metadata",
    "data/hardware/20260511_fpga1_board1/restart",
    "data/hardware/20260511_fpga1_board1/restart_fifo_diag",
    "data/hardware/20260511_fpga1_board1/tdc",
    "data/hardware/20260511_fpga1_board1/tdc_pairs",
    "data/hardware/20260511_fpga1_board1/trng"
)

$tvlsiIncludeRoots = @(
    "paper/RO_TRNG_tvlsi_sampler_aperture",
    "scripts/update_github_export_snapshot.ps1",
    "scripts/build_tvlsi_mechanism_validation_20260531.py",
    "scripts/summarize_pvt_xadc_manifest_20260530.py",
    "scripts/summarize_second_heldout_warmup_aperture_sweep_20260530.py",
    "scripts/tvlsi_build_sampler_aperture_model_20260530.py",
    "scripts/run_board2_second_heldout_warmup_aperture_sweep_20260530.ps1",
    "scripts/run_board2_second_heldout_sample_ro_local_20260530.ps1",
    "scripts/diagnose_xadc_sysmon_20260530.ps1",
    "scripts/vivado/diagnose_xadc_sysmon_20260530.tcl",
    "data/experiments/tvlsi_mechanism_validation_20260531",
    "data/experiments/second_heldout_warmup_aperture_sweep_20260530",
    "data/experiments/tvlsi_sampler_aperture_model_20260530",
    "data/experiments/second_heldout_sampler_route_diff_20260530",
    "data/experiments/xadc_summary/board2_bitstream_xadc_compare_20260531.csv",
    "data/experiments/xadc_summary/pvt_xadc_manifest_validation_20260530.csv",
    "data/experiments/xadc_summary/pvt_xadc_manifest_validation_20260531.csv",
    "data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary"
)

$includeRoots = if ($Profile -eq "Tvlsi") {
    $tvlsiIncludeRoots
} else {
    $defaultIncludeRoots
}

$excludeExt = @(
    ".bin", ".bit", ".dcp", ".jou", ".log", ".pb", ".rpx", ".wdb",
    ".wcfg", ".str", ".vdi", ".zip", ".pdf", ".exe", ".o", ".obj",
    ".a", ".tmp", ".docx", ".aux", ".bbl", ".blg", ".fdb_latexmk",
    ".fls", ".png"
)

$excludeDir = @(
    ".git", ".Xil", "__pycache__", "xsim.dir"
)

$excludeDirPatterns = @(
    ".runs", ".cache", ".gen", ".hw", ".ip_user_files", ".sim"
)

$excludeNamePatterns = @(
    "*.tdc_packets.csv",
    "*.sha256.txt",
    "*.bits.bin.metadata.json",
    "*.payload.bin.metadata.json",
    "*.payload.metadata.json"
)

function Convert-ToRelativePath([string]$Base, [string]$Path) {
    $baseUri = [System.Uri]((Join-Path $Base ".") + [System.IO.Path]::DirectorySeparatorChar)
    $pathUri = [System.Uri]$Path
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($pathUri).ToString()).Replace("/", "\")
}

function Test-ExcludedFile([System.IO.FileInfo]$File) {
    if ($File.Length -gt ($MaxFileMiB * 1MB)) {
        return $true
    }
    if ($excludeExt -contains $File.Extension.ToLowerInvariant()) {
        return $true
    }
    foreach ($pattern in $excludeNamePatterns) {
        if ($File.Name -like $pattern) {
            return $true
        }
    }
    $relative = Convert-ToRelativePath $SourceRoot $File.FullName
    $segments = $relative -split "[\\/]+"
    foreach ($segment in $segments) {
        if ($excludeDir -contains $segment) {
            return $true
        }
        foreach ($pattern in $excludeDirPatterns) {
            if ($segment -like "*$pattern") {
                return $true
            }
        }
    }
    return $false
}

$copied = New-Object System.Collections.Generic.List[object]
$skipped = New-Object System.Collections.Generic.List[object]

foreach ($root in $includeRoots) {
    $src = Join-Path $SourceRoot $root
    if (-not (Test-Path $src)) {
        $skipped.Add([pscustomobject]@{ Path = $root; Reason = "missing include root"; Size = 0 }) | Out-Null
        continue
    }

    $item = Get-Item $src
    $files = if ($item.PSIsContainer) {
        Get-ChildItem -LiteralPath $item.FullName -Recurse -File -Force
    } else {
        @($item)
    }

    foreach ($file in $files) {
        $relative = Convert-ToRelativePath $SourceRoot $file.FullName
        if (Test-ExcludedFile $file) {
            $reason = if ($file.Length -gt ($MaxFileMiB * 1MB)) { "excluded: larger than $MaxFileMiB MiB" } else { "excluded" }
            $skipped.Add([pscustomobject]@{ Path = $relative; Reason = $reason; Size = $file.Length }) | Out-Null
            continue
        }

        $dest = Join-Path $ExportRoot $relative
        $destDir = Split-Path -Parent $dest
        if (-not $DryRun) {
            New-Item -ItemType Directory -Force -Path $destDir | Out-Null
            Copy-Item -LiteralPath $file.FullName -Destination $dest -Force
        }
        $copied.Add([pscustomobject]@{
            Path = $relative
            Size = $file.Length
            LastWriteTime = $file.LastWriteTime.ToString("s")
            SHA256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
        }) | Out-Null
    }
}

$manifestDir = Join-Path $ExportRoot "data/experiments/export_snapshot_$SnapshotTag"
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $manifestDir | Out-Null
}

$manifestCsv = Join-Path $manifestDir "included_files.csv"
$skippedCsv = Join-Path $manifestDir "skipped_files.csv"
$summaryMd = Join-Path $manifestDir "README.md"

if (-not $DryRun) {
    $copied | Sort-Object Path | Export-Csv -NoTypeInformation -Encoding UTF8 $manifestCsv
    $skipped | Sort-Object Path | Export-Csv -NoTypeInformation -Encoding UTF8 $skippedCsv

    $totalBytes = ($copied | Measure-Object Size -Sum).Sum
    $summary = @()
    $summary += "# RO_TRNG export snapshot $SnapshotTag"
    $summary += ""
    $summary += "Generated from: ``$SourceRoot``"
    $summary += ""
    $summary += "Export root: ``$ExportRoot``"
    $summary += ""
    $summary += "Profile: ``$Profile``"
    $summary += ""
    $summary += "Included files: $($copied.Count)"
    $summary += ""
    $summary += "Included size: $([math]::Round($totalBytes / 1MB, 3)) MiB"
    $summary += ""
    $summary += "Skipped files: $($skipped.Count)"
    $summary += ""
    $summary += "This snapshot is intended for GitHub/source review. Raw UART captures, bitstreams, Vivado generated products, binaries, PDFs, and packet-level dumps are intentionally excluded. Reproducibility is preserved through scripts, RTL, XDC, metadata, analysis summaries, and SHA256 manifests."
    $summary += ""
    $summary += "Key post-2026-05-15 evidence to inspect:"
    $summary += ""
    if ($Profile -eq "Tvlsi") {
        $summary += "- ``paper/RO_TRNG_tvlsi_sampler_aperture/``"
        $summary += "- ``data/experiments/tvlsi_mechanism_validation_20260531/``"
        $summary += "- ``data/experiments/second_heldout_warmup_aperture_sweep_20260530/``"
        $summary += "- ``data/experiments/xadc_summary/board2_bitstream_xadc_compare_20260531.csv``"
        $summary += "- ``data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/``"
    } else {
        $summary += "- ``doc/restart_fifo_diag_mechanism_update_20260524.md``"
        $summary += "- ``doc/restart_fifo_diag_queue_status_20260524.md``"
        $summary += "- ``doc/regs_only_restart_breakthrough_20260524.md``"
        $summary += "- ``doc/random1_sampler_island_ablation_20260523.md``"
        $summary += "- ``data/experiments/restart_fifo_diag_20260524/``"
        $summary += "- ``data/experiments/xdc_sampler_island/``"
    }
    $summary += ""
    $summary += "Manifests:"
    $summary += ""
    $summary += "- ``included_files.csv``"
    $summary += "- ``skipped_files.csv``"
    $summary | Set-Content -Encoding UTF8 $summaryMd
}

[pscustomobject]@{
    SourceRoot = $SourceRoot
    ExportRoot = $ExportRoot
    SnapshotTag = $SnapshotTag
    Profile = $Profile
    DryRun = [bool]$DryRun
    MaxFileMiB = $MaxFileMiB
    IncludedFiles = $copied.Count
    SkippedFiles = $skipped.Count
    IncludedMiB = [math]::Round((($copied | Measure-Object Size -Sum).Sum) / 1MB, 3)
    ManifestDir = $manifestDir
}
