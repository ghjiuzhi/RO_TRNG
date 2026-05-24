param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$VariantsCsv = "regs_only",
    [int[]]$Seeds = @(1)
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
$flow = "scripts\vivado\run_fpga1_ro_trng_sweep_inmem.tcl"

foreach ($variant in $variants) {
    if (-not $variantMap.ContainsKey($variant)) {
        throw "Unknown variant '$variant'. Known variants: $($variantMap.Keys -join ', ')"
    }
    $xdc = $variantMap[$variant]
    if (-not (Test-Path $xdc)) {
        throw "Variant XDC not found: $xdc"
    }
    foreach ($seed in $Seeds) {
        $outDir = "data\vivado_runs\fpga1_sampler_island\$variant\seed_$seed"
        $bit = Join-Path $outDir "RO_TRNG_top.bit"
        if (Test-Path $bit) {
            Write-Host "SKIP existing $variant seed=${seed}: $bit"
            continue
        }
        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        Write-Host "BUILD sampler ablation variant=$variant seed=$seed"
        & $VivadoBat -mode batch -source $flow -tclargs $xdc $outDir $seed
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado sampler-ablation build failed for variant=$variant seed=$seed with exit code $LASTEXITCODE"
        }
        if (-not (Test-Path $bit)) {
            throw "Vivado reported success but bitstream was not found: $bit"
        }
        Write-Host "DONE sampler ablation variant=$variant seed=$seed -> $bit"
    }
}
