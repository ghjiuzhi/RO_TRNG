param(
    [string]$QueueCsv = "data\experiments\fast_mode\hardware_queue_tdc_reset_aligned_matrix_20260523.csv",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b01",
    [string]$OutRoot = "data\experiments\tdc_reset_aligned_preopen_20260525",
    [switch]$RecordXadcAfter,
    [switch]$ContinueOnError
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Value)

    $candidate = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    $candidate = Join-Path $repoRoot $Value
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
}

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$queuePath = Resolve-RepoPath $QueueCsv
if (-not (Test-Path $queuePath)) {
    throw "Queue CSV not found: $QueueCsv"
}

$outRootAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutRoot)
$logDir = Join-Path $outRootAbs "logs"
$summaryCsv = Join-Path $outRootAbs "tdc_reset_aligned_preopen_queue_summary_20260525.csv"
$xadcCsv = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv"
New-Item -ItemType Directory -Force $outRootAbs, $logDir | Out-Null

$rows = Import-Csv -Path $queuePath | Where-Object { [string]$_.enabled -eq "1" }
if (@($rows).Count -eq 0) {
    throw "No enabled queue rows: $QueueCsv"
}

$summary = New-Object System.Collections.Generic.List[object]
$capturedInputs = New-Object System.Collections.Generic.List[string]
$capturedLabels = New-Object System.Collections.Generic.List[string]

foreach ($row in $rows) {
    $run = ([string]$row.run).Trim()
    $bit = ([string]$row.bitstream).Trim()
    $bytes = ([string]$row.bytes).Trim()
    $outFile = ([string]$row.out_file).Trim()
    $metadataDir = ([string]$row.metadata_dir).Trim()
    $idleTimeout = if (([string]$row.idle_timeout_sec).Trim() -ne "") { [int]$row.idle_timeout_sec } else { 90 }
    $runId = "${run}_preopen_20260525"
    $outFilePreopen = [System.IO.Path]::ChangeExtension($outFile, $null) + "_preopen_20260525.bin"
    $bitAbs = Resolve-RepoPath $bit
    $status = "completed"
    $errorMessage = ""

    Write-Host "=== $runId ==="
    Write-Host "Bitstream: $bitAbs"
    Write-Host "Out:       $outFilePreopen"
    try {
        if (-not (Test-Path $bitAbs)) {
            throw "Bitstream not found: $bit"
        }

        powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart_preopen.ps1 `
            -Bitstream $bit `
            -Port $Port `
            -Baud $Baud `
            -Run $runId `
            -Bytes $bytes `
            -OutFile $outFilePreopen `
            -MetadataDir $metadataDir `
            -IdleTimeoutSec $idleTimeout `
            -ReadBufferBytes 1048576 `
            -HwServerUrl $HwServerUrl `
            -VivadoBat $VivadoBat `
            -BoardId $BoardId `
            *>&1 | Tee-Object -FilePath (Join-Path $logDir "$runId.capture.log")
        if ($LASTEXITCODE -ne 0) {
            throw "program_and_capture_uart_preopen.ps1 failed with exit code $LASTEXITCODE"
        }

        $item = Get-Item -LiteralPath $outFilePreopen
        if ($item.Length -ne [int64]$bytes) {
            throw "Capture size mismatch: expected $bytes, got $($item.Length)"
        }

        if ($RecordXadcAfter) {
            powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
                -OutCsv $xadcCsv `
                -HwServerUrl $HwServerUrl `
                -VivadoBat $VivadoBat `
                *>&1 | Tee-Object -FilePath (Join-Path $logDir "$runId.xadc_after.log")
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "XADC after-capture failed for ${runId}: exit $LASTEXITCODE"
            }
        }

        $capturedInputs.Add($outFilePreopen) | Out-Null
        $capturedLabels.Add($runId) | Out-Null
    } catch {
        $status = "failed"
        $errorMessage = $_.Exception.Message
        Write-Warning "$runId failed: $errorMessage"
        if (-not $ContinueOnError) {
            throw
        }
    }

    $captureSha = ""
    $captureBytes = ""
    $first16 = ""
    $metaPath = Join-Path (Resolve-RepoPath $metadataDir) "$runId.json"
    if (Test-Path $outFilePreopen) {
        $captureSha = (Get-FileHash -Path $outFilePreopen -Algorithm SHA256).Hash
        $captureBytes = (Get-Item -LiteralPath $outFilePreopen).Length
    }
    if (Test-Path $metaPath) {
        $meta = Get-Content $metaPath -Raw | ConvertFrom-Json
        $first16 = $meta.first_16_bytes_hex
    }
    $summary.Add([pscustomobject]@{
        run = $runId
        status = $status
        error = $errorMessage
        priority = $row.priority
        bytes_expected = $bytes
        bytes_captured = $captureBytes
        first_16_bytes_hex = $first16
        capture = $outFilePreopen
        capture_sha256 = $captureSha
        bitstream = $bit
        bitstream_sha256 = if (Test-Path $bitAbs) { (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash } else { "" }
        notes = $row.notes
    }) | Out-Null
    $summary | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
}

if ($capturedInputs.Count -gt 0) {
    $analysisArgs = @(
        "scripts\analyze_tdc_startup_diffusion.py",
        "--out-dir", $outRootAbs,
        "--prefix", "tdc_reset_aligned_matrix_preopen_20260525",
        "--early-packets", "512",
        "--window-packets", "4096",
        "--warmup-starts", "0,12,64,256,1024,4096"
    )
    for ($i = 0; $i -lt $capturedInputs.Count; $i++) {
        $analysisArgs += @("--input", $capturedInputs[$i], "--label", $capturedLabels[$i])
    }
    python @analysisArgs *>&1 | Tee-Object -FilePath (Join-Path $logDir "tdc_reset_aligned_matrix_preopen_20260525.analysis.log")
    if ($LASTEXITCODE -ne 0) {
        throw "analyze_tdc_startup_diffusion.py failed with exit code $LASTEXITCODE"
    }
}

$summary | Format-Table -AutoSize
Write-Host "Wrote $summaryCsv"
