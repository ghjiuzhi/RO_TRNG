param(
    [int]$Warmup = 5,
    [string]$Run = "",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$BoardId = "z7020_b01",
    [switch]$RecordXadc
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-BinaryMinEntropy {
    param([double]$P1)
    $pmax = [Math]::Max($P1, 1.0 - $P1)
    return -1.0 * ([Math]::Log($pmax) / [Math]::Log(2.0))
}

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$restartCount = 1000
$rowBytes = 125
$headerBytes = 16
$captureBytes = $headerBytes + ($restartCount * $rowBytes)
$label = "restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup${Warmup}_${restartCount}x${rowBytes}"
if ($Run -eq "") {
    $Run = "${label}_run02_20260525"
}

$bitstream = "data\vivado_runs\${label}\RO_TRNG_restart_fifo_compact_diag_top.bit"
$bitAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($bitstream)
if (-not (Test-Path $bitAbs)) {
    $candidate = Join-Path $repoRoot $bitstream
    if (Test-Path $candidate) {
        $bitAbs = (Resolve-Path $candidate).Path
    } else {
        throw "Bitstream not found: $bitstream"
    }
}

$hardwareRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1"
$captureRoot = Join-Path $hardwareRoot "restart_fifo_diag"
$metadataDir = Join-Path $hardwareRoot "metadata"
$artifactRoot = Join-Path $repoRoot "data\experiments\restart_fifo_diag_20260525"
$logDir = Join-Path $artifactRoot "sample_ro_locked_logs"
$outFile = Join-Path $captureRoot "$Run.bin"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"
$summaryCsv = Join-Path $artifactRoot "sample_ro_forward_fail_repeat_summary_20260525.csv"
$columnDir = Join-Path $artifactRoot "$Run.column_analysis"

New-Item -ItemType Directory -Force $captureRoot, $metadataDir, $artifactRoot, $logDir | Out-Null

Write-Host "=== sample-RO forward fail repeat ==="
Write-Host "Run:       $Run"
Write-Host "Warmup:    $Warmup"
Write-Host "Bitstream: $bitAbs"
Write-Host "Output:    $outFile"
Write-Host "Bytes:     $captureBytes"

$captureArgs = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", "scripts\program_and_capture_uart.ps1",
    "-VivadoBat", $VivadoBat,
    "-Bitstream", $bitstream,
    "-Port", $Port,
    "-Baud", "$Baud",
    "-Kind", "restart",
    "-Run", $Run,
    "-Bytes", "$captureBytes",
    "-OutFile", $outFile,
    "-MetadataDir", $metadataDir,
    "-IdleTimeoutSec", "300",
    "-BoardId", $BoardId
)
if ($RecordXadc) {
    $captureArgs += @("-RecordXadc", "-XadcMode", "after_only", "-XadcCsv", $xadcCsv)
}

powershell @captureArgs *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.capture.log")
if ($LASTEXITCODE -ne 0) {
    throw "program_and_capture_uart.ps1 failed with exit code $LASTEXITCODE"
}

$item = Get-Item -LiteralPath $outFile
if ($item.Length -ne $captureBytes) {
    throw "Unexpected compact diagnostic size for ${Run}: expected $captureBytes, got $($item.Length)"
}

python scripts\analyze_restart_fifo_compact_diag.py `
    --input $outFile `
    --out-dir $artifactRoot `
    --label $Run `
    *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.analysis.log")
if ($LASTEXITCODE -ne 0) {
    throw "analyze_restart_fifo_compact_diag.py failed with exit code $LASTEXITCODE"
}

$packed = Join-Path $artifactRoot "$Run.send_packed.bin"
python scripts\analyze_restart_matrix_columns.py `
    --input $packed `
    --restart-count $restartCount `
    --bytes-per-restart $rowBytes `
    --label $Run `
    --out-dir $columnDir `
    *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.columns.log")
if ($LASTEXITCODE -ne 0) {
    throw "analyze_restart_matrix_columns.py failed with exit code $LASTEXITCODE"
}

$analysisSummary = Import-Csv (Join-Path $artifactRoot "$Run.summary.csv") | Select-Object -First 1
$captureMetaPath = Join-Path $metadataDir "$Run.json"
$captureMeta = if (Test-Path $captureMetaPath) { Get-Content $captureMetaPath -Raw | ConvertFrom-Json } else { $null }
$overallP1 = [double]::Parse($analysisSummary.overall_p1, [System.Globalization.CultureInfo]::InvariantCulture)

$row = [pscustomobject]@{
    run = $Run
    status = "completed"
    warmup = $Warmup
    capture = $outFile
    capture_bytes = $item.Length
    capture_sha256 = (Get-FileHash -Path $outFile -Algorithm SHA256).Hash
    packed_body = $packed
    packed_sha256 = $analysisSummary.send_packed_sha256
    bitstream = $bitstream
    bitstream_sha256 = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
    header_bytes = $headerBytes
    xadc_mode = if ($RecordXadc) { "after_only" } else { "not_requested" }
    xadc_after_status = if ($null -ne $captureMeta) { $captureMeta.xadc_after.status } else { "" }
    xadc_after_temperature_c = if ($null -ne $captureMeta) { $captureMeta.xadc_after.temperature_c } else { "" }
    overall_p1 = $analysisSummary.overall_p1
    overall_min_entropy = "{0:F9}" -f (Get-BinaryMinEntropy -P1 $overallP1)
    row_ones_std = $analysisSummary.row_ones_std
    worst_byte_index = $analysisSummary.worst_byte_index
    worst_bit_index = $analysisSummary.worst_bit_index
    worst_x = $analysisSummary.worst_x
    worst_p1 = $analysisSummary.worst_p1
    column_summary_json = (Join-Path $columnDir "summary.json")
}

$rows = @()
if (Test-Path $summaryCsv) {
    $rows += Import-Csv $summaryCsv
}
$rows += $row
$rows | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8

$row | Format-List
Write-Host "Wrote $summaryCsv"
