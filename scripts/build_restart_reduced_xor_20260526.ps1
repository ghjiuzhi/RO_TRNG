param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$VariantsCsv = "sampler_island_local",
    [string]$WarmupsCsv = "10",
    [string]$ModesCsv = "data_ro",
    [string]$IndexesCsv = "2",
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
    sampler_island_local = "data\experiments\xdc_sampler_island\random1_sampler_island_local_x45y39_regs_x45y31.xdc"
    sample_ro_local = "data\experiments\xdc_sampler_island\random1_sample_ro_local_x45y39.xdc"
    regs_only = "data\experiments\xdc_sampler_island\random1_sampler_regs_only_x45y31.xdc"
}

$modeMap = @{
    all64 = 0
    data_ro = 1
    line = 2
    except_data_ro = 3
}

$variants = $VariantsCsv.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$modes = $ModesCsv.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
$indexes = $IndexesCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$flow = "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl"
$top = "RO_TRNG_restart_reduced_xor_top"

foreach ($variant in $variants) {
    if (-not $variantMap.ContainsKey($variant)) {
        throw "Unknown variant '$variant'. Known variants: $($variantMap.Keys -join ', ')"
    }
    $xdc = $variantMap[$variant]
    if (-not (Test-Path $xdc)) {
        throw "Variant XDC not found: $xdc"
    }

    foreach ($warmup in $warmups) {
        foreach ($mode in $modes) {
            if (-not $modeMap.ContainsKey($mode)) {
                throw "Unknown mode '$mode'. Known modes: $($modeMap.Keys -join ', ')"
            }
            $modeId = $modeMap[$mode]

            foreach ($index in $indexes) {
                $outDir = "data\vivado_runs\restart_reduced_xor_random1_${variant}_formal_bits_1000x125_warmup${warmup}_${mode}${index}_header_delay60s"
                $bit = Join-Path $outDir "$top.bit"
                if (Test-Path $bit) {
                    Write-Host "SKIP existing $variant warmup=$warmup mode=$mode index=${index}: $bit"
                    continue
                }

                New-Item -ItemType Directory -Force -Path $outDir | Out-Null
                Write-Host "BUILD reduced-xor variant=$variant warmup=$warmup mode=$mode index=$index"
                & $VivadoBat -mode batch -source $flow -tclargs `
                    $xdc `
                    $outDir `
                    $RestartCount `
                    $RowBytes `
                    $HoldCycles `
                    $SettleCycles `
                    $warmup `
                    $StartDelayCycles `
                    $DebugHeader `
                    $top `
                    $modeId `
                    $index
                if ($LASTEXITCODE -ne 0) {
                    throw "Vivado reduced-xor build failed for variant=$variant warmup=$warmup mode=$mode index=$index with exit code $LASTEXITCODE"
                }
                if (-not (Test-Path $bit)) {
                    throw "Vivado reported success but bitstream was not found: $bit"
                }
                Write-Host "DONE reduced-xor variant=$variant warmup=$warmup mode=$mode index=$index -> $bit"
            }
        }
    }
}
