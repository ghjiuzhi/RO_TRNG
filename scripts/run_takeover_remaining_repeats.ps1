param(
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$Bytes = "5MiB",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BaseDir = "data\hardware\20260511_fpga1_board1",
    [int]$WaitVivadoPid = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$logDir = Join-Path $BaseDir "logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$logPath = Join-Path $logDir ("takeover_remaining_repeats_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss"))

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    $line | Tee-Object -FilePath $logPath -Append
}

if ($WaitVivadoPid -ne 0) {
    $p = Get-Process -Id $WaitVivadoPid -ErrorAction SilentlyContinue
    if ($p) {
        Write-Log "Waiting for existing Vivado PID $WaitVivadoPid before hardware programming."
        Wait-Process -Id $WaitVivadoPid
    }
}

$runs = @(
    @{
        Run = "random2_repeat02_5mib"
        Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed2_x36y35\seed_1\RO_TRNG_top.bit"
    },
    @{
        Run = "checker_repeat02_5mib"
        Bitstream = "data\vivado_runs\fpga1_ro_trng_sweep\ro_checker_pitch3_x44y43\seed_1\RO_TRNG_top.bit"
    },
    @{
        Run = "cross_region_repeat02_5mib"
        Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\cross_region_x36y25\seed_1\RO_TRNG_top.bit"
    },
    @{
        Run = "same_column_repeat02_5mib"
        Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\same_column_pitch3_x44y35\seed_1\RO_TRNG_top.bit"
    }
)

foreach ($item in $runs) {
    $run = $item.Run
    $metadataPath = Join-Path (Join-Path $BaseDir "metadata") "$run.json"
    if (Test-Path $metadataPath) {
        Write-Log "Skipping $run because metadata already exists: $metadataPath"
        continue
    }

    $outFile = Join-Path (Join-Path $BaseDir "trng") "$run.bin"
    Write-Log "Starting $run"
    & .\scripts\program_and_capture_uart.ps1 `
        -Bitstream $item.Bitstream `
        -Port $Port `
        -Baud $Baud `
        -Kind trng `
        -Bytes $Bytes `
        -Run $run `
        -MetadataDir (Join-Path $BaseDir "metadata") `
        -OutFile $outFile `
        -HwServerUrl $HwServerUrl `
        -Analyze *>&1 | Tee-Object -FilePath $logPath -Append

    if ($LASTEXITCODE -ne 0) {
        throw "Capture failed for $run with exit code $LASTEXITCODE"
    }
    Write-Log "Completed $run"
}

Write-Log "All takeover repeat captures completed."
