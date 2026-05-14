param(
    [string]$Port = "COM3",

    [int]$Baud = 115200,

    [string]$Day = "20260511_fpga1_board1",

    [string]$Bytes = "1MiB",

    [string]$Suffix = "smoke01",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$trngDir = Join-Path $repoRoot "data\hardware\$Day\trng"
$metadataDir = Join-Path $repoRoot "data\hardware\$Day\metadata"
$logDir = Join-Path $repoRoot "data\hardware\$Day\logs"
New-Item -ItemType Directory -Force $trngDir, $metadataDir, $logDir | Out-Null

$items = @(
    [pscustomobject]@{ Id = "checker"; Bitstream = "data\vivado_runs\fpga1_ro_trng_sweep\ro_checker_pitch3_x44y43\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "same_column"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\same_column_pitch3_x44y35\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "row"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\row_pitch3_x38y43\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "cross_region"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\cross_region_x36y25\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "random1"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "random2"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed2_x36y35\seed_1\RO_TRNG_top.bit" },
    [pscustomobject]@{ Id = "random3"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit" }
)

foreach ($item in $items) {
    $bitAbs = Join-Path $repoRoot $item.Bitstream
    if (-not (Test-Path $bitAbs)) {
        throw "Missing bitstream for $($item.Id): $bitAbs"
    }

    $runId = "$($item.Id)_$Suffix"
    $outFile = Join-Path $trngDir "$runId.bin"
    if ((Test-Path $outFile) -and (-not $Force)) {
        Write-Host "Skipping existing capture: $outFile"
        continue
    }

    Write-Host ""
    Write-Host "=== Capturing $runId ($Bytes) ==="
    & (Join-Path $repoRoot "scripts\program_and_capture_uart.ps1") `
        -Bitstream $item.Bitstream `
        -Port $Port `
        -Baud $Baud `
        -Kind trng `
        -Run $runId `
        -Bytes $Bytes `
        -OutFile $outFile `
        -MetadataDir $metadataDir `
        -HwServerUrl $HwServerUrl `
        -VivadoBat $VivadoBat `
        -Analyze
    if ($LASTEXITCODE -ne 0) {
        throw "Capture failed for $runId with exit code $LASTEXITCODE"
    }
}

& python (Join-Path $repoRoot "scripts\audit_hardware_runs.py") (Join-Path $repoRoot "data\hardware\$Day")
if ($LASTEXITCODE -ne 0) {
    throw "Hardware run audit failed with exit code $LASTEXITCODE"
}
