param(
    [string[]]$Warmups = @("4", "5", "11"),
    [string]$WarmupList = "",
    [string]$RunSuffix = "run02_20260528",
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

$warmupText = if ($WarmupList -ne "") { $WarmupList } else { ($Warmups -join ",") }
$parsedWarmups = @()
foreach ($token in ($warmupText -split "[,\s;]+")) {
    if ($token -eq "") { continue }
    if ($token -notmatch "^\d+$") {
        throw "Invalid warmup token '$token'"
    }
    $parsedWarmups += [int]$token
}
if ($parsedWarmups.Count -eq 0) {
    throw "No warmups parsed"
}

$hardwareRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1"
$captureRoot = Join-Path $hardwareRoot "restart_fifo_diag"
$metadataDir = Join-Path $hardwareRoot "metadata"
$artifactRoot = Join-Path $repoRoot "data\experiments\restart_fifo_diag_20260528"
$logDir = Join-Path $artifactRoot "compact_baseline_repeat_logs"
$summaryCsv = Join-Path $artifactRoot "compact_baseline_repeat_summary_20260528.csv"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"

New-Item -ItemType Directory -Force $captureRoot, $metadataDir, $artifactRoot, $logDir | Out-Null

$rows = @()
if (Test-Path $summaryCsv) {
    $rows += Import-Csv $summaryCsv
}

foreach ($warmup in $parsedWarmups) {
    $label = "restart_fifo_compact_diag_random1_regs_only_warmup${warmup}_${restartCount}x${rowBytes}"
    $run = "restart_fifo_compact_diag_regs_only_warmup${warmup}_${restartCount}x${rowBytes}_${RunSuffix}"
    $bitstream = "data\vivado_runs\$label\RO_TRNG_restart_fifo_compact_diag_top.bit"
    $bitAbs = Join-Path $repoRoot $bitstream
    if (-not (Test-Path $bitAbs)) {
        throw "Bitstream not found: $bitstream"
    }

    $outFile = Join-Path $captureRoot "$run.bin"
    $columnDir = Join-Path $artifactRoot "$run.column_analysis"

    Write-Host "=== compact baseline repeat ==="
    Write-Host "Run:       $run"
    Write-Host "Warmup:    $warmup"
    Write-Host "Bitstream: $bitstream"
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
        "-Run", $run,
        "-Bytes", "$captureBytes",
        "-OutFile", $outFile,
        "-MetadataDir", $metadataDir,
        "-IdleTimeoutSec", "300",
        "-BoardId", $BoardId
    )
    if ($RecordXadc) {
        $captureArgs += @("-RecordXadc", "-XadcMode", "after_only", "-XadcCsv", $xadcCsv)
    }

    powershell @captureArgs *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.capture.log")
    if ($LASTEXITCODE -ne 0) {
        throw "program_and_capture_uart.ps1 failed for $run with exit code $LASTEXITCODE"
    }

    $item = Get-Item -LiteralPath $outFile
    if ($item.Length -ne $captureBytes) {
        throw "Unexpected size for ${run}: expected $captureBytes, got $($item.Length)"
    }

    python scripts\analyze_restart_fifo_compact_diag.py `
        --input $outFile `
        --out-dir $artifactRoot `
        --label $run `
        *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.analysis.log")
    if ($LASTEXITCODE -ne 0) {
        throw "analyze_restart_fifo_compact_diag.py failed for $run"
    }

    $packed = Join-Path $artifactRoot "$run.send_packed.bin"
    python scripts\analyze_restart_matrix_columns.py `
        --input $packed `
        --restart-count $restartCount `
        --bytes-per-restart $rowBytes `
        --label $run `
        --out-dir $columnDir `
        *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.columns.log")
    if ($LASTEXITCODE -ne 0) {
        throw "analyze_restart_matrix_columns.py failed for $run"
    }

    $analysisSummary = Import-Csv (Join-Path $artifactRoot "$run.summary.csv") | Select-Object -First 1
    $overallP1 = [double]::Parse($analysisSummary.overall_p1, [System.Globalization.CultureInfo]::InvariantCulture)
    $captureMetaPath = Join-Path $metadataDir "$run.json"
    $captureMeta = if (Test-Path $captureMetaPath) { Get-Content $captureMetaPath -Raw | ConvertFrom-Json } else { $null }

    $rows += [pscustomobject]@{
        run = $run
        status = "completed"
        warmup = $warmup
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
    $rows | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
}

$rows | Format-Table run,warmup,overall_p1,overall_min_entropy,worst_x,worst_p1 -AutoSize
Write-Host "Wrote $summaryCsv"
