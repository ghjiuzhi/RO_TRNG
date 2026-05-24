param(
    [string]$WarmupsCsv = "4,5,10,11",
    [string]$VariantsCsv = "regs_only",
    [int]$CaptureSnapshots = 1024,
    [string]$TopName = "RO_TRNG_sampler_snapshot_top",
    [string]$OutPrefix = "sampler_snapshot",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$Root = (Resolve-Path ".").Path,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$variantMap = @{
    "regs_only" = @{
        Xdc = "data\experiments\xdc_sampler_island\random1_sampler_regs_only_x45y31.xdc"
        VariantId = 16
    }
    "baseline" = @{
        Xdc = "data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc"
        VariantId = 17
    }
    "sampler_island" = @{
        Xdc = "data\experiments\xdc_sampler_island\random1_sampler_island_local_x45y39_regs_x45y31.xdc"
        VariantId = 18
    }
}

$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$variants = $VariantsCsv.Split(",") | ForEach-Object { $_.Trim() }
$baseXdc = Join-Path $Root "fpga1\xc7z020clg400\lab_xdc\sampler_snapshot_sysclk.xdc"

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}
if (-not (Test-Path -LiteralPath $baseXdc)) {
    throw "Base sampler snapshot XDC not found: $baseXdc"
}

Push-Location $Root
try {
    foreach ($variant in $variants) {
        if (-not $variantMap.ContainsKey($variant)) {
            throw "Unknown variant '$variant'. Known: $($variantMap.Keys -join ', ')"
        }
        $info = $variantMap[$variant]
        $xdc = Resolve-Path $info.Xdc
        foreach ($warmup in $warmups) {
            $name = "${OutPrefix}_random1_${variant}_warmup${warmup}_cap${CaptureSnapshots}"
            $outDir = Join-Path $Root ("data\vivado_runs\sampler_snapshot\" + $name)
            $bit = Join-Path $outDir "$TopName.bit"
            if ((Test-Path -LiteralPath $bit) -and -not $Force) {
                Write-Host "SKIP existing ${name}: $bit"
                continue
            }
            $variantId = [int]$info.VariantId + $warmup
            $generic = "{RO_NUM=8 RO_STAGES=2 SAMPLE_STAGES=9 WARMUP_SNAPSHOTS=$warmup CAPTURE_SNAPSHOTS=$CaptureSnapshots START_DELAY_CYCLES=16000000000 VARIANT_ID=$variantId}"
            Write-Host "BUILD $name"
            Write-Host "  XDC:     $xdc"
            Write-Host "  BaseXDC: $baseXdc"
            Write-Host "  Out:     $outDir"
            Write-Host "  Generic: $generic"
            & $VivadoBat -mode batch `
                -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
                -tclargs $xdc $outDir $TopName $generic $baseXdc
            if ($LASTEXITCODE -ne 0) {
                throw "Vivado build failed for $name with exit code $LASTEXITCODE"
            }
            Write-Host "DONE $name -> $bit"
        }
    }
}
finally {
    Pop-Location
}
