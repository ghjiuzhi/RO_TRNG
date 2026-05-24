param(
    [string]$FramesGlob = "data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup*_1000x32_run01.frames.csv",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 32,
    [string]$OutDir = "data\experiments\restart_fifo_diag_20260524"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$outDirAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutDir)
New-Item -ItemType Directory -Force $outDirAbs | Out-Null

$frames = @(Get-ChildItem -Path $FramesGlob -File -ErrorAction SilentlyContinue | Sort-Object Name)
if ($frames.Count -eq 0) {
    Write-Host "No frames files matched: $FramesGlob"
    exit 0
}

$rows = @()
foreach ($file in $frames) {
    $label = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    if ($label.EndsWith(".frames")) {
        $label = $label.Substring(0, $label.Length - ".frames".Length)
    }

    Write-Host "Postprocessing $label"
    python "scripts\summarize_restart_fifo_diag_matrix.py" `
        --input $file.FullName `
        --out-dir $outDirAbs `
        --label $label
    if ($LASTEXITCODE -ne 0) {
        throw "Matrix summary failed for $label"
    }

    $packed = Join-Path $outDirAbs "${label}.send_packed.bin"
    $columnDir = Join-Path $outDirAbs "${label}.column_analysis"
    python "scripts\analyze_restart_matrix_columns.py" `
        --input $packed `
        --restart-count $RestartCount `
        --bytes-per-restart $RowBytes `
        --label $label `
        --out-dir $columnDir
    if ($LASTEXITCODE -ne 0) {
        throw "Column analysis failed for $label"
    }

    $summaryCsv = Join-Path $outDirAbs "${label}.summary.csv"
    $summary = Import-Csv $summaryCsv | Select-Object -First 1
    $rows += $summary
}

$merged = Join-Path $outDirAbs "restart_fifo_diag_matrix_summary_20260524.csv"
$rows | Export-Csv -Path $merged -NoTypeInformation -Encoding UTF8

$md = Join-Path $outDirAbs "restart_fifo_diag_matrix_summary_20260524.md"
$lines = @(
    "# Restart FIFO Diagnostic Matrix Summary - 2026-05-24",
    "",
    "| label | restart_count | bytes_per_restart | overall_p1 | row_ones_mean | row_ones_std | row_ones_min | row_ones_max | worst_byte_index | worst_bit_index | worst_p1 | worst_x |",
    "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
)
foreach ($row in $rows) {
    $lines += "| $($row.label) | $($row.restart_count) | $($row.bytes_per_restart) | $($row.overall_p1) | $($row.row_ones_mean) | $($row.row_ones_std) | $($row.row_ones_min) | $($row.row_ones_max) | $($row.worst_byte_index) | $($row.worst_bit_index) | $($row.worst_p1) | $($row.worst_x) |"
}
$lines | Set-Content -Path $md -Encoding UTF8

Write-Host "Wrote $merged"
Write-Host "Wrote $md"
