param(
    [int[]]$Warmups = @(4, 5, 10, 11),
    [int]$RestartCount = 1000,
    [int]$RowBytes = 32,
    [int]$HoldCycles = 200000,
    [int]$SettleCycles = 200000,
    [UInt64]$StartDelayCycles = 12000000000,
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$Xdc = "data\experiments\xdc_sampler_island\random1_sampler_regs_only_x45y31.xdc",
    [string]$BoardId = "z7020_b01"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$runRoot = Join-Path $repoRoot "data\experiments\restart_fifo_diag_20260524"
$captureRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\restart_fifo_diag"
$metadataDir = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\metadata"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"
$logDir = Join-Path $runRoot "queue_logs"

New-Item -ItemType Directory -Force $runRoot, $captureRoot, $metadataDir, $logDir | Out-Null

$preWarmupBytes = 4
$framesPerRun = $RestartCount * ($RowBytes + $preWarmupBytes)
$captureBytes = 16 + ($framesPerRun * 16)
$bytesArg = [string]$captureBytes

$summaryRows = @()

foreach ($warmup in $Warmups) {
    $label = "regs_only_warmup${warmup}_${RestartCount}x${RowBytes}"
    $buildDir = Join-Path $repoRoot "data\vivado_runs\restart_fifo_diag_random1_${label}"
    $bitstream = Join-Path $buildDir "RO_TRNG_restart_fifo_diag_top.bit"
    $capture = Join-Path $captureRoot "restart_fifo_diag_${label}_run01.bin"
    $analysisLabel = "restart_fifo_diag_${label}_run01"
    $buildLog = Join-Path $logDir "${label}_build.log"
    $captureLog = Join-Path $logDir "${label}_capture.log"
    $analysisLog = Join-Path $logDir "${label}_analysis.log"

    Write-Host "==== $label ===="
    Write-Host "Expected diagnostic bytes: $captureBytes"

    if (-not (Test-Path $bitstream)) {
        Write-Host "Building $bitstream"
        $buildErr = Join-Path $logDir "${label}_build_stderr.log"
        $buildArgs = @(
            "-mode", "batch",
            "-source", "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl",
            "-tclargs", $Xdc, $buildDir, $RestartCount, $RowBytes,
            $HoldCycles, $SettleCycles, $warmup, $StartDelayCycles, 1,
            "RO_TRNG_restart_fifo_diag_top"
        )
        $buildProc = Start-Process -FilePath $VivadoBat `
            -ArgumentList $buildArgs `
            -WorkingDirectory $repoRoot `
            -RedirectStandardOutput $buildLog `
            -RedirectStandardError $buildErr `
            -WindowStyle Hidden `
            -Wait `
            -PassThru
        if (Test-Path $buildErr) {
            Get-Content $buildErr | Add-Content $buildLog
        }
        if ($buildProc.ExitCode -ne 0) {
            throw "Vivado build failed for $label with exit code $($buildProc.ExitCode)"
        }
    } else {
        Write-Host "Bitstream already exists: $bitstream"
    }

    Write-Host "Programming and capturing $label"
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\program_and_capture_uart.ps1" `
        -Bitstream $bitstream `
        -Port $Port `
        -Baud $Baud `
        -Kind raw `
        -Run $analysisLabel `
        -Bytes $bytesArg `
        -OutFile $capture `
        -MetadataDir $metadataDir `
        -IdleTimeoutSec 300 `
        -RecordXadc `
        -XadcCsv $xadcCsv `
        -BoardId $BoardId `
        *>&1 | Tee-Object -FilePath $captureLog
    if ($LASTEXITCODE -ne 0) {
        throw "Capture failed for $label with exit code $LASTEXITCODE"
    }

    Write-Host "Decoding diagnostic frames for $label"
    python "scripts\analyze_restart_fifo_diag.py" `
        --input $capture `
        --out-dir $runRoot `
        --label $analysisLabel `
        *>&1 | Tee-Object -FilePath $analysisLog
    if ($LASTEXITCODE -ne 0) {
        throw "Diagnostic decode failed for $label with exit code $LASTEXITCODE"
    }

    Write-Host "Summarizing send-phase matrix for $label"
    python "scripts\summarize_restart_fifo_diag_matrix.py" `
        --input (Join-Path $runRoot "${analysisLabel}.frames.csv") `
        --out-dir $runRoot `
        --label $analysisLabel `
        *>&1 | Tee-Object -FilePath (Join-Path $logDir "${label}_matrix.log")
    if ($LASTEXITCODE -ne 0) {
        throw "Diagnostic matrix summary failed for $label with exit code $LASTEXITCODE"
    }

    Write-Host "Running column analysis for $label"
    python "scripts\analyze_restart_matrix_columns.py" `
        --input (Join-Path $runRoot "${analysisLabel}.send_packed.bin") `
        --restart-count $RestartCount `
        --bytes-per-restart $RowBytes `
        --label $analysisLabel `
        --out-dir (Join-Path $runRoot "${analysisLabel}.column_analysis") `
        *>&1 | Tee-Object -FilePath (Join-Path $logDir "${label}_columns.log")
    if ($LASTEXITCODE -ne 0) {
        throw "Diagnostic column analysis failed for $label with exit code $LASTEXITCODE"
    }

    $hash = (Get-FileHash -Path $capture -Algorithm SHA256).Hash
    $summaryRows += [pscustomobject]@{
        label = $label
        warmup = $warmup
        restart_count = $RestartCount
        row_bytes = $RowBytes
        expected_bytes = $captureBytes
        capture = $capture
        sha256 = $hash
        frames_csv = (Join-Path $runRoot "${analysisLabel}.frames.csv")
        summary_md = (Join-Path $runRoot "${analysisLabel}.summary.md")
        send_packed_bin = (Join-Path $runRoot "${analysisLabel}.send_packed.bin")
        matrix_summary_md = (Join-Path $runRoot "${analysisLabel}.matrix_summary.md")
        column_summary_json = (Join-Path $runRoot "${analysisLabel}.column_analysis\summary.json")
    }
    $summaryRows | Export-Csv -Path (Join-Path $runRoot "restart_fifo_diag_queue_summary_20260524.csv") -NoTypeInformation -Encoding UTF8
}

$summaryRows | Format-Table -AutoSize
Write-Host "Wrote queue summary: $(Join-Path $runRoot 'restart_fifo_diag_queue_summary_20260524.csv')"
