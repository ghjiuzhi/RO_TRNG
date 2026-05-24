param(
    [string]$OutMarkdown = "doc\next_hardware_readiness_20260515.md",
    [string]$OutCsv = "data\experiments\fast_mode\next_hardware_readiness_20260515.csv",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$MingwRoot = "D:\Toolsapp\MinGW"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

function Add-Check {
    param(
        [string]$Category,
        [string]$Name,
        [bool]$Ok,
        [string]$Path = "",
        [string]$Note = ""
    )
    [pscustomobject]@{
        category = $Category
        name = $Name
        ok = $Ok
        path = $Path
        note = $Note
    }
}

function Test-RepoPath {
    param([string]$Path)
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return Test-Path $Path
    }
    return Test-Path (Join-Path $repoRoot $Path)
}

$checks = New-Object System.Collections.Generic.List[object]

$requiredFiles = @(
    "scripts\run_restart_placement_queue.ps1",
    "scripts\run_restart_warmup_repeat_queue.ps1",
    "scripts\run_fast_hardware_queue.ps1",
    "scripts\capture_90b_restart_dataset.ps1",
    "scripts\capture_uart.ps1",
    "scripts\read_xadc.ps1",
    "scripts\summarize_restart_results.py",
    "scripts\summarize_xadc_metadata.py",
    "scripts\convert_restart_bytes_to_bits.py",
    "scripts\analyze_restart_matrix_columns.py",
    "data\experiments\fast_mode\restart_placement_queue_20260515.csv",
    "data\experiments\fast_mode\hardware_queue_placement_repeat_20260515.csv"
)
foreach ($file in $requiredFiles) {
    $checks.Add((Add-Check "file" $file (Test-RepoPath $file) $file "")) | Out-Null
}

$restartQueue = "data\experiments\fast_mode\restart_placement_queue_20260515.csv"
if (Test-RepoPath $restartQueue) {
    $rows = Import-Csv (Join-Path $repoRoot $restartQueue)
    foreach ($row in $rows | Where-Object { [string]$_.enabled -eq "1" }) {
        $bit = [string]$row.bitstream
        $name = "restart_queue:$($row.placement):warmup$($row.warmup_bytes)"
        $entropyOk = ([string]$row.initial_entropy_msb).Trim() -ne "" -and ([string]$row.initial_entropy_lsb).Trim() -ne ""
        $checks.Add((Add-Check "restart_queue" $name (Test-RepoPath $bit) $bit "bitstream")) | Out-Null
        $checks.Add((Add-Check "restart_queue" "${name}:initial_entropy" $entropyOk "" "MSB/LSB H_I fields")) | Out-Null
    }
}

$placementQueue = "data\experiments\fast_mode\hardware_queue_placement_repeat_20260515.csv"
if (Test-RepoPath $placementQueue) {
    $rows = Import-Csv (Join-Path $repoRoot $placementQueue)
    foreach ($row in $rows | Where-Object { [string]$_.enabled -eq "1" }) {
        $bit = [string]$row.bitstream
        $name = "placement_repeat:$($row.run)"
        $checks.Add((Add-Check "placement_repeat_queue" $name (Test-RepoPath $bit) $bit "bitstream")) | Out-Null
    }
}

$restartStatusCsv = "data\experiments\fast_mode\restart_placement_bitstream_status_20260515.csv"
if (Test-RepoPath $restartStatusCsv) {
    $rows = Import-Csv (Join-Path $repoRoot $restartStatusCsv)
    foreach ($row in $rows) {
        $ok = ([string]$row.bit_exists -eq "True" -and [string]$row.manifest_exists -eq "True")
        $checks.Add((Add-Check "restart_bitstream_status" "$($row.placement):warmup$($row.warmup_bytes)" $ok $row.bitstream "bit+manifest")) | Out-Null
    }
}

$eaExe = Join-Path $repoRoot "sim\SP800-90B_EntropyAssessment\cpp\ea_restart.exe"
$checks.Add((Add-Check "tool" "ea_restart.exe" (Test-Path $eaExe) $eaExe "SP800-90B restart runner")) | Out-Null
$checks.Add((Add-Check "tool" "Vivado batch" (Test-Path $VivadoBat) $VivadoBat "Vivado path")) | Out-Null
$gpp = Join-Path $MingwRoot "bin\g++.exe"
$checks.Add((Add-Check "tool" "MinGW g++" (Test-Path $gpp) $gpp "SP800-90B build toolchain")) | Out-Null

$vivadoProcesses = @(Get-Process -Name vivado -ErrorAction SilentlyContinue)
$checks.Add((Add-Check "process" "no active Vivado build" ($vivadoProcesses.Count -eq 0) "" "avoid colliding with hardware programming")) | Out-Null

$outCsvPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutCsv)
$outCsvDir = Split-Path -Parent $outCsvPath
if (-not (Test-Path $outCsvDir)) {
    New-Item -ItemType Directory -Force -Path $outCsvDir | Out-Null
}
$checks | Export-Csv -Path $outCsvPath -NoTypeInformation -Encoding UTF8

$outMdPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutMarkdown)
$outMdDir = Split-Path -Parent $outMdPath
if (-not (Test-Path $outMdDir)) {
    New-Item -ItemType Directory -Force -Path $outMdDir | Out-Null
}
$failed = @($checks | Where-Object { -not $_.ok })
$lines = @()
$lines += "# Next Hardware Readiness"
$lines += ""
$lines += "- Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$lines += "- Checks: $($checks.Count)"
$lines += "- Failed: $($failed.Count)"
$lines += "- CSV: ``$outCsvPath``"
$lines += ""
$lines += "| category | name | ok | path | note |"
$lines += "| --- | --- | --- | --- | --- |"
foreach ($check in $checks) {
    $lines += "| $($check.category) | $($check.name) | $($check.ok) | ``$($check.path)`` | $($check.note) |"
}
$lines | Set-Content -Path $outMdPath -Encoding UTF8

Write-Host "Wrote $outCsvPath"
Write-Host "Wrote $outMdPath"
Write-Host "Failed checks: $($failed.Count)"
if ($failed.Count -gt 0) {
    $failed | Format-Table -AutoSize
}
