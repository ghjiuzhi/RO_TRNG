param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$VariantsCsv = "sample_ro_local,sampler_island_local",
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

$variantMap = @{
    sample_ro_local = "data\experiments\xdc_sampler_island\random1_sample_ro_local_x45y39.xdc"
    sampler_island_local = "data\experiments\xdc_sampler_island\random1_sampler_island_local_x45y39_regs_x45y31.xdc"
    regs_only = "data\experiments\xdc_sampler_island\random1_sampler_regs_only_x45y31.xdc"
}

$variants = $VariantsCsv.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$flow = "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl"

foreach ($variant in $variants) {
    if (-not $variantMap.ContainsKey($variant)) {
        throw "Unknown variant '$variant'. Known variants: $($variantMap.Keys -join ', ')"
    }
    $xdc = $variantMap[$variant]
    if (-not (Test-Path $xdc)) {
        throw "Variant XDC not found: $xdc"
    }

    foreach ($warmup in $warmups) {
        $outDir = "data\vivado_runs\restart_auto_random1_${variant}_formal_bits_1000x125_warmup${warmup}_header_delay60s"
        $bit = Join-Path $outDir "RO_TRNG_restart_auto_top.bit"
        if (Test-Path $bit) {
            Write-Host "SKIP existing $variant warmup=${warmup}: $bit"
            continue
        }

        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        Write-Host "BUILD restart variant=$variant warmup=$warmup"
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
            throw "Vivado restart build failed for variant=$variant warmup=$warmup with exit code $LASTEXITCODE"
        }
        if (-not (Test-Path $bit)) {
            throw "Vivado reported success but bitstream was not found: $bit"
        }
        Write-Host "DONE restart variant=$variant warmup=$warmup -> $bit"
    }
}
