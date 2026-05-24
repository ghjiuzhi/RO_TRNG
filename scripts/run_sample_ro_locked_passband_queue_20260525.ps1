param(
    [string[]]$Warmups = @("4", "5", "11"),
    [string]$WarmupList = "",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 125,
    [int]$HoldCycles = 200000,
    [int]$SettleCycles = 200000,
    [UInt64]$StartDelayCycles = 12000000000,
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$Xdc = "data\experiments\xdc_sampler_island\random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc",
    [string]$BoardId = "z7020_b01",
    [switch]$Rebuild,
    [switch]$RecordXadc,
    [ValidateSet("before_after", "after_only")]
    [string]$XadcMode = "after_only"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$runRoot = Join-Path $repoRoot "data\experiments\restart_fifo_diag_20260525"
$captureRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\restart_fifo_diag"
$metadataDir = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\metadata"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"
$logDir = Join-Path $runRoot "sample_ro_locked_logs"
$summaryCsv = Join-Path $runRoot "sample_ro_locked_passband_queue_summary_20260525.csv"

New-Item -ItemType Directory -Force $runRoot, $captureRoot, $metadataDir, $logDir | Out-Null

$warmupText = if ($WarmupList -ne "") { $WarmupList } else { ($Warmups -join ",") }
$parsedWarmups = @()
foreach ($token in ($warmupText -split "[,\s;]+")) {
    if ($token -eq "") {
        continue
    }
    if ($token -notmatch "^\d+$") {
        throw "Invalid warmup token '$token' in '$warmupText'. Use -WarmupList '4,5,11'."
    }
    $value = [int]$token
    if ($value -lt 0 -or $value -gt 255) {
        throw "Warmup value $value is outside the intended diagnostic range 0..255. Parsed from '$warmupText'."
    }
    $parsedWarmups += $value
}
if ($parsedWarmups.Count -eq 0) {
    throw "No warmup values parsed. Use -WarmupList '4,5,11'."
}
Write-Host "Parsed warmups: $($parsedWarmups -join ', ')"

$captureBytes = 16 + ($RestartCount * $RowBytes)
$summaryRows = @()

foreach ($warmup in $parsedWarmups) {
    $label = "restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup${warmup}_${RestartCount}x${RowBytes}"
    $runId = "${label}_run02_20260525"
    if ($warmup -ne 4) {
        $runId = "${label}_run01_20260525"
    }

    $buildDir = Join-Path $repoRoot "data\vivado_runs\${label}"
    $bitstream = Join-Path $buildDir "RO_TRNG_restart_fifo_compact_diag_top.bit"
    $capture = Join-Path $captureRoot "${runId}.bin"
    $buildLog = Join-Path $logDir "${label}_build.log"
    $buildErr = Join-Path $logDir "${label}_build_stderr.log"
    $captureLog = Join-Path $logDir "${runId}_capture.log"
    $analysisLog = Join-Path $logDir "${runId}_analysis.log"
    $columnLog = Join-Path $logDir "${runId}_columns.log"

    Write-Host "==== $runId ===="
    Write-Host "Goal: sample-RO formal-locked compact diagnostic, warmup=$warmup"
    Write-Host "Expected bytes: $captureBytes"

    if ($Rebuild -or -not (Test-Path $bitstream)) {
        Write-Host "Building bitstream: $bitstream"
        $buildArgs = @(
            "-mode", "batch",
            "-source", "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl",
            "-tclargs", $Xdc, $buildDir, $RestartCount, $RowBytes,
            $HoldCycles, $SettleCycles, $warmup, $StartDelayCycles, 1,
            "RO_TRNG_restart_fifo_compact_diag_top"
        )
        $buildProc = Start-Process -FilePath $VivadoBat `
            -ArgumentList $buildArgs `
            -WorkingDirectory $repoRoot `
            -RedirectStandardOutput $buildLog `
            -RedirectStandardError $buildErr `
            -WindowStyle Hidden `
            -Wait `
            -PassThru
        if ($buildProc.ExitCode -ne 0) {
            throw "Vivado build failed for $runId with exit code $($buildProc.ExitCode). See $buildLog and $buildErr"
        }
    } else {
        Write-Host "Using existing bitstream: $bitstream"
    }

    $captureArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", "scripts\program_and_capture_uart.ps1",
        "-VivadoBat", $VivadoBat,
        "-Bitstream", $bitstream,
        "-Port", $Port,
        "-Baud", $Baud,
        "-Kind", "restart",
        "-Run", $runId,
        "-Bytes", [string]$captureBytes,
        "-OutFile", $capture,
        "-MetadataDir", $metadataDir,
        "-IdleTimeoutSec", "300",
        "-BoardId", $BoardId
    )
    if ($RecordXadc) {
        $captureArgs += @("-RecordXadc", "-XadcMode", $XadcMode, "-XadcCsv", $xadcCsv)
    }

    Write-Host "Programming and capturing: $capture"
    $captureProc = Start-Process -FilePath "powershell" `
        -ArgumentList $captureArgs `
        -WorkingDirectory $repoRoot `
        -RedirectStandardOutput $captureLog `
        -RedirectStandardError (Join-Path $logDir "${runId}_capture_stderr.log") `
        -WindowStyle Hidden `
        -Wait `
        -PassThru
    if ($captureProc.ExitCode -ne 0) {
        throw "Capture failed for $runId with exit code $($captureProc.ExitCode). See $captureLog"
    }

    Write-Host "Analyzing compact capture"
    python "scripts\analyze_restart_fifo_compact_diag.py" `
        --input $capture `
        --out-dir $runRoot `
        --label $runId `
        *>&1 | Tee-Object -FilePath $analysisLog
    if ($LASTEXITCODE -ne 0) {
        throw "Compact analysis failed for $runId with exit code $LASTEXITCODE"
    }

    $packed = Join-Path $runRoot "${runId}.send_packed.bin"
    python "scripts\analyze_restart_matrix_columns.py" `
        --input $packed `
        --restart-count $RestartCount `
        --bytes-per-restart $RowBytes `
        --label $runId `
        --out-dir (Join-Path $runRoot "${runId}.column_analysis") `
        *>&1 | Tee-Object -FilePath $columnLog
    if ($LASTEXITCODE -ne 0) {
        throw "Column analysis failed for $runId with exit code $LASTEXITCODE"
    }

    $summary = Import-Csv (Join-Path $runRoot "${runId}.summary.csv") | Select-Object -First 1
    $summaryRows += [pscustomobject]@{
        run_id = $runId
        warmup = $warmup
        restart_count = $RestartCount
        row_bytes = $RowBytes
        bitstream = $bitstream
        capture = $capture
        capture_sha256 = (Get-FileHash -Path $capture -Algorithm SHA256).Hash
        packed_sha256 = $summary.send_packed_sha256
        overall_p1 = $summary.overall_p1
        row_ones_std = $summary.row_ones_std
        worst_byte_index = $summary.worst_byte_index
        worst_bit_index = $summary.worst_bit_index
        worst_p1 = $summary.worst_p1
        worst_x = $summary.worst_x
        summary_md = (Join-Path $runRoot "${runId}.summary.md")
        column_dir = (Join-Path $runRoot "${runId}.column_analysis")
    }
    $summaryRows | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
}

$summaryRows | Format-Table -AutoSize
Write-Host "Wrote $summaryCsv"
