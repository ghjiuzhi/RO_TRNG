param(
    [string]$PlacementsCsv = "same_column,sparse,compact,checker",
    [string]$WarmupsCsv = "0,12",
    [string]$OutCsv = "data\experiments\fast_mode\restart_placement_bitstream_status_20260515.csv",
    [string]$OutMarkdown = "doc\restart_placement_bitstream_status_20260515.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$placements = $PlacementsCsv.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$rows = @()

foreach ($placement in $placements) {
    foreach ($warmup in $warmups) {
        $run = "restart_auto_${placement}_formal_bits_1000x125_warmup${warmup}_header_delay60s"
        $dir = Join-Path "data\vivado_runs" $run
        $bit = Join-Path $dir "RO_TRNG_restart_auto_top.bit"
        $manifest = Join-Path $dir "manifest.txt"
        $bitExists = Test-Path $bit
        $manifestExists = Test-Path $manifest
        $bitSize = 0
        $bitSha256 = ""
        $lastWrite = ""
        if ($bitExists) {
            $item = Get-Item $bit
            $bitSize = $item.Length
            $lastWrite = $item.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
            $bitSha256 = (Get-FileHash -Path $bit -Algorithm SHA256).Hash
        }
        $rows += [pscustomobject]@{
            placement = $placement
            warmup_bytes = $warmup
            run = $run
            bitstream = $bit
            bit_exists = $bitExists
            bit_size = $bitSize
            bit_sha256 = $bitSha256
            manifest_exists = $manifestExists
            last_write = $lastWrite
        }
    }
}

$outCsvPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutCsv)
$outCsvDir = Split-Path -Parent $outCsvPath
if (-not (Test-Path $outCsvDir)) {
    New-Item -ItemType Directory -Force -Path $outCsvDir | Out-Null
}
$rows | Export-Csv -Path $outCsvPath -NoTypeInformation -Encoding UTF8

$outMdPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutMarkdown)
$outMdDir = Split-Path -Parent $outMdPath
if (-not (Test-Path $outMdDir)) {
    New-Item -ItemType Directory -Force -Path $outMdDir | Out-Null
}

$ready = @($rows | Where-Object { $_.bit_exists -and $_.manifest_exists }).Count
$total = @($rows).Count
$lines = @()
$lines += "# Restart Placement Bitstream Status"
$lines += ""
$lines += "- Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$lines += "- Ready: $ready / $total"
$lines += ""
$lines += "| placement | warmup_bytes | bit_exists | manifest_exists | bit_size | bitstream |"
$lines += "| --- | ---: | --- | --- | ---: | --- |"
foreach ($row in $rows) {
    $lines += "| $($row.placement) | $($row.warmup_bytes) | $($row.bit_exists) | $($row.manifest_exists) | $($row.bit_size) | ``$($row.bitstream)`` |"
}
$lines | Set-Content -Path $outMdPath -Encoding UTF8

Write-Host "Wrote $outCsvPath"
Write-Host "Wrote $outMdPath"
Write-Host "Ready $ready / $total"
