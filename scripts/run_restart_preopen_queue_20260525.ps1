param(
    [string]$QueueCsv = "data\experiments\fast_mode\hardware_queue_restart_sampler_island_passband_preopen_20260525.csv",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b01",
    [string]$OutRoot = "data\experiments\restart_sampler_island_passband_preopen_20260525",
    [switch]$RecordXadcAfter,
    [switch]$ContinueOnError
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SizeToBytes {
    param([string]$Value)

    $text = $Value.Trim()
    if ($text -match '^\d+$') {
        return [int64]$text
    }
    if ($text -match '^(\d+)(KiB|MiB|GiB|KB|MB|GB)$') {
        $n = [int64]$Matches[1]
        switch ($Matches[2]) {
            "KiB" { return $n * 1024 }
            "MiB" { return $n * 1024 * 1024 }
            "GiB" { return $n * 1024 * 1024 * 1024 }
            "KB"  { return $n * 1000 }
            "MB"  { return $n * 1000 * 1000 }
            "GB"  { return $n * 1000 * 1000 * 1000 }
        }
    }
    throw "Invalid byte count: $Value"
}

function Resolve-RepoPath {
    param([string]$Value)

    if ([System.IO.Path]::IsPathRooted($Value)) {
        return $Value
    }
    return (Join-Path $repoRoot $Value)
}

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$queuePath = Resolve-RepoPath $QueueCsv
if (-not (Test-Path $queuePath)) {
    throw "Queue CSV not found: $QueueCsv"
}

$outRootAbs = Resolve-RepoPath $OutRoot
$logDir = Join-Path $outRootAbs "logs"
$summaryCsv = Join-Path $outRootAbs "restart_preopen_queue_summary_20260525.csv"
$xadcCsv = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv"
New-Item -ItemType Directory -Force $outRootAbs, $logDir | Out-Null

$rows = @(Import-Csv -Path $queuePath | Where-Object { [string]$_.enabled -eq "1" })
if ($rows.Count -eq 0) {
    throw "No enabled queue rows: $QueueCsv"
}

$summary = New-Object System.Collections.Generic.List[object]
foreach ($row in $rows) {
    $run = ([string]$row.run).Trim()
    $bit = ([string]$row.bitstream).Trim()
    $bytesText = ([string]$row.bytes).Trim()
    $expectedBytes = Convert-SizeToBytes $bytesText
    $outFile = ([string]$row.out_file).Trim()
    $metadataDir = ([string]$row.metadata_dir).Trim()
    $idleTimeout = if (([string]$row.idle_timeout_sec).Trim() -ne "") { [int]$row.idle_timeout_sec } else { 120 }
    $bitAbs = Resolve-RepoPath $bit
    $outAbs = Resolve-RepoPath $outFile
    $status = "completed"
    $errorMessage = ""

    Write-Host "=== $run ==="
    try {
        if (-not (Test-Path $bitAbs)) {
            throw "Bitstream not found: $bit"
        }

        powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart_preopen.ps1 `
            -Bitstream $bit `
            -Port $Port `
            -Baud $Baud `
            -Run $run `
            -Bytes $bytesText `
            -OutFile $outFile `
            -MetadataDir $metadataDir `
            -IdleTimeoutSec $idleTimeout `
            -ReadBufferBytes 1048576 `
            -HwServerUrl $HwServerUrl `
            -VivadoBat $VivadoBat `
            -BoardId $BoardId `
            *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.capture.log")
        if ($LASTEXITCODE -ne 0) {
            throw "program_and_capture_uart_preopen.ps1 failed with exit code $LASTEXITCODE"
        }

        $item = Get-Item -LiteralPath $outAbs
        if ($item.Length -ne $expectedBytes) {
            throw "Capture size mismatch: expected $expectedBytes, got $($item.Length)"
        }

        if ($RecordXadcAfter) {
            powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
                -OutCsv $xadcCsv `
                -HwServerUrl $HwServerUrl `
                -VivadoBat $VivadoBat `
                *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.xadc_after.log")
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "XADC after-capture failed for ${run}: exit $LASTEXITCODE"
            }
        }
    } catch {
        $status = "failed"
        $errorMessage = $_.Exception.Message
        Write-Warning "$run failed: $errorMessage"
        if (-not $ContinueOnError) {
            throw
        }
    }

    $captureSha = ""
    $captureBytes = ""
    $first16 = ""
    $metaPath = Resolve-RepoPath (Join-Path $metadataDir "$run.json")
    if (Test-Path $outAbs) {
        $captureSha = (Get-FileHash -Path $outAbs -Algorithm SHA256).Hash
        $captureBytes = (Get-Item -LiteralPath $outAbs).Length
    }
    if (Test-Path $metaPath) {
        $meta = Get-Content $metaPath -Raw | ConvertFrom-Json
        $first16 = $meta.first_16_bytes_hex
    }
    $summary.Add([pscustomobject]@{
        run = $run
        status = $status
        error = $errorMessage
        priority = $row.priority
        bytes_expected = $expectedBytes
        bytes_captured = $captureBytes
        first_16_bytes_hex = $first16
        capture = $outAbs
        capture_sha256 = $captureSha
        bitstream = $bit
        bitstream_sha256 = if (Test-Path $bitAbs) { (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash } else { "" }
        notes = $row.notes
    }) | Out-Null
    $summary | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
}

$summary | Format-Table -AutoSize
Write-Host "Wrote $summaryCsv"
