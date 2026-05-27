param(
    [string]$Bitstream = "data\vivado_runs\restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_20260525\RO_TRNG_restart_auto_top.bit",
    [string]$Run = "restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_run02_20260525",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b01",
    [switch]$RecordXadc
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$restartCount = 1000
$rowBytes = 125
$hardwareRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1"
$restartDir = Join-Path $hardwareRoot "restart"
$metadataDir = Join-Path $hardwareRoot "metadata"
$artifactRoot = Join-Path $repoRoot "data\experiments\restart_fifo_diag_20260525"
$logDir = Join-Path $artifactRoot "sample_ro_reverse_logs"
$outFile = Join-Path $restartDir "$Run.bin"
$metadataFile = Join-Path $restartDir "$Run.metadata.json"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"
$summaryCsv = Join-Path $artifactRoot "sample_ro_reverse_repair_repeat_summary_20260525.csv"
$profilePrefix = $Run
$columnDir = Join-Path $artifactRoot "$Run.column_analysis"

New-Item -ItemType Directory -Force $restartDir, $metadataDir, $artifactRoot, $logDir | Out-Null

$bitAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Bitstream)
if (-not (Test-Path $bitAbs)) {
    $candidate = Join-Path $repoRoot $Bitstream
    if (Test-Path $candidate) {
        $bitAbs = (Resolve-Path $candidate).Path
    } else {
        throw "Bitstream not found: $Bitstream"
    }
}

Write-Host "=== sample-RO reverse repair repeat ==="
Write-Host "Run:       $Run"
Write-Host "Bitstream: $bitAbs"
Write-Host "Output:    $outFile"
Write-Host "Matrix:    ${restartCount} x ${rowBytes} bytes"

$captureArgs = @(
    "-ExecutionPolicy", "Bypass",
    "-File", "scripts\capture_90b_restart_dataset.ps1",
    "-Bitstream", $Bitstream,
    "-OutFile", $outFile,
    "-Port", $Port,
    "-Baud", "$Baud",
    "-RestartCount", "$restartCount",
    "-SymbolsPerRestart", "$rowBytes",
    "-BitsPerSymbol", "8",
    "-WarmupSymbols", "0",
    "-HeaderBytes", "8",
    "-SettleMs", "500",
    "-ReadTimeoutMs", "1000",
    "-ReadBufferBytes", "190544",
    "-IdleTimeoutSec", "90",
    "-RestartMethod", "auto_stream_once",
    "-Run", $Run,
    "-MetadataFile", $metadataFile,
    "-HwServerUrl", $HwServerUrl,
    "-VivadoBat", $VivadoBat,
    "-BoardId", $BoardId
)
if ($RecordXadc) {
    $captureArgs += @("-RecordXadc", "-XadcMode", "after_only", "-XadcCsv", $xadcCsv)
}

powershell @captureArgs *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.capture.log")
if ($LASTEXITCODE -ne 0) {
    throw "capture_90b_restart_dataset.ps1 failed with exit code $LASTEXITCODE"
}

$item = Get-Item -LiteralPath $outFile
$expectedBytes = $restartCount * $rowBytes
if ($item.Length -ne $expectedBytes) {
    throw "Unexpected packed body size for ${Run}: expected $expectedBytes, got $($item.Length)"
}

python scripts\summarize_restart_formal_output_profile.py `
    --input $outFile `
    --restart-count $restartCount `
    --row-bytes $rowBytes `
    --out-dir $artifactRoot `
    --prefix $profilePrefix `
    *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.profile.log")
if ($LASTEXITCODE -ne 0) {
    throw "summarize_restart_formal_output_profile.py failed with exit code $LASTEXITCODE"
}

python scripts\analyze_restart_matrix_columns.py `
    --input $outFile `
    --restart-count $restartCount `
    --bytes-per-restart $rowBytes `
    --label $Run `
    --out-dir $columnDir `
    *>&1 | Tee-Object -FilePath (Join-Path $logDir "$Run.columns.log")
if ($LASTEXITCODE -ne 0) {
    throw "analyze_restart_matrix_columns.py failed with exit code $LASTEXITCODE"
}

$profileSummary = Import-Csv (Join-Path $artifactRoot "${profilePrefix}_summary.csv") | Select-Object -First 1
$columnSummaryJson = Get-Content (Join-Path $columnDir "summary.json") -Raw | ConvertFrom-Json
$metadata = Get-Content $metadataFile -Raw | ConvertFrom-Json

$row = [pscustomobject]@{
    run = $Run
    status = "completed"
    capture = $outFile
    capture_bytes = $item.Length
    capture_sha256 = (Get-FileHash -Path $outFile -Algorithm SHA256).Hash
    bitstream = $Bitstream
    bitstream_sha256 = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
    header_bytes = $metadata.header_bytes
    header_hex = $metadata.header_hex
    xadc_mode = $metadata.xadc_mode
    xadc_after_status = $metadata.xadc_after.status
    xadc_after_temperature_c = $metadata.xadc_after.temperature_c
    overall_p1 = $profileSummary.overall_p1
    overall_min_entropy = $profileSummary.overall_min_entropy
    row_ones_std = $profileSummary.row_ones_std
    worst_byte_index = $profileSummary.worst_byte_index
    worst_bit_index = $profileSummary.worst_bit_index
    worst_x = $profileSummary.worst_x
    worst_p1 = $profileSummary.worst_p1
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
