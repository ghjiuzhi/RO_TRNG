param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$PlacementsCsv = "same_column,sparse,compact,checker",
    [string]$WarmupsCsv = "0,12",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 125,
    [int]$HoldCycles = 200000,
    [int]$SettleCycles = 200000,
    [string]$StartDelayCycles = "12000000000",
    [int]$DebugHeader = 1
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$placementMap = @{
    same_column = "data\experiments\xdc_matrix\ro_same_column_pitch3_x44y35.xdc"
    sparse = "data\experiments\xdc_matrix\ro_sparse_pitch6_x36y35.xdc"
    compact = "data\experiments\xdc_matrix\ro_compact_x44y43.xdc"
    checker = "data\experiments\xdc_matrix\ro_checker_pitch3_x44y43.xdc"
}

$placements = $PlacementsCsv.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$flow = "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl"

foreach ($placement in $placements) {
    if (-not $placementMap.ContainsKey($placement)) {
        throw "Unknown placement '$placement'. Known placements: $($placementMap.Keys -join ', ')"
    }
    $xdc = $placementMap[$placement]
    if (-not (Test-Path $xdc)) {
        throw "Placement XDC not found: $xdc"
    }

    foreach ($warmup in $warmups) {
        $outDir = "data\vivado_runs\restart_auto_${placement}_formal_bits_1000x125_warmup${warmup}_header_delay60s"
        $bit = Join-Path $outDir "RO_TRNG_restart_auto_top.bit"
        if (Test-Path $bit) {
            Write-Host "SKIP existing $placement warmup=${warmup}: $bit"
            continue
        }

        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        Write-Host "BUILD restart placement=$placement warmup=$warmup"
        & $VivadoBat -mode batch -source $flow -tclargs `
            $xdc `
            $outDir `
            $RestartCount `
            $RowBytes `
            $HoldCycles `
            $SettleCycles `
            $warmup `
            $StartDelayCycles `
            $DebugHeader
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado restart build failed for placement=$placement warmup=$warmup with exit code $LASTEXITCODE"
        }
        if (-not (Test-Path $bit)) {
            throw "Vivado reported success but bitstream was not found: $bit"
        }
        Write-Host "DONE restart placement=$placement warmup=$warmup -> $bit"
    }
}
