param(
    [string]$BaseDir = "data\hardware\20260511_fpga1_board1",
    [string]$Run = "",
    [string]$Kind = "trng",
    [string]$Bytes = "5MiB"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SizeToBytes {
    param([string]$Value)

    $text = $Value.Trim()
    if ($text -match '^(?<num>\d+)(?<unit>\s*(B|K|KB|KiB|M|MB|MiB|G|GB|GiB)?)$') {
        [int64]$num = [int64]$Matches["num"]
        $unit = $Matches["unit"].Trim().ToLowerInvariant()
        switch ($unit) {
            { $_ -in @("", "b") } { return $num }
            { $_ -in @("k", "kb") } { return $num * 1000 }
            "kib" { return $num * 1024 }
            { $_ -in @("m", "mb") } { return $num * 1000 * 1000 }
            "mib" { return $num * 1024 * 1024 }
            { $_ -in @("g", "gb") } { return $num * 1000 * 1000 * 1000 }
            "gib" { return $num * 1024 * 1024 * 1024 }
        }
    }
    throw "Invalid size '$Value'. Examples: 1KiB, 5MiB, 10MiB."
}

function Format-Percent {
    param([double]$Value)
    return ("{0:N2}%" -f $Value)
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$targetBytes = Convert-SizeToBytes $Bytes
$dataDir = Join-Path $BaseDir $Kind
$metadataDir = Join-Path $BaseDir "metadata"

if ($Run -ne "") {
    $files = @(Get-Item (Join-Path $dataDir "$Run.bin") -ErrorAction SilentlyContinue)
} else {
    $files = @(Get-ChildItem $dataDir -Filter "*.bin" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 12)
}

$now = Get-Date
Write-Host "Capture status at $($now.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
Write-Host "BaseDir: $BaseDir"
Write-Host "Kind:    $Kind"
Write-Host ""

$hw = Get-Process hw_server -ErrorAction SilentlyContinue
if ($hw) {
    Write-Host "hw_server: running (pid $($hw.Id -join ', '))"
} else {
    Write-Host "hw_server: not running"
}

$vivado = Get-Process vivado -ErrorAction SilentlyContinue
if ($vivado) {
    Write-Host "vivado:    running (pid $($vivado.Id -join ', '))"
} else {
    Write-Host "vivado:    not running"
}

Write-Host ""
Write-Host "Recent captures:"

foreach ($file in $files) {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $metaPath = Join-Path $metadataDir "$name.json"
    $shaPath = "$($file.FullName).sha256.txt"
    $analysisDir = Join-Path $file.DirectoryName "analysis_$name"
    $pct = if ($targetBytes -gt 0) { [double]$file.Length * 100.0 / [double]$targetBytes } else { 0.0 }
    $age = [int](($now - $file.LastWriteTime).TotalSeconds)

    [PSCustomObject]@{
        Run = $name
        Bytes = $file.Length
        Target = $targetBytes
        Percent = Format-Percent $pct
        LastWrite = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        AgeSec = $age
        Metadata = Test-Path $metaPath
        Sha256 = Test-Path $shaPath
        Analysis = Test-Path $analysisDir
    }
}
