param(
    [ValidateSet("smoke", "p0", "p1", "matrix", "all")]
    [string]$Mode = "smoke",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

function New-Run {
    param(
        [string]$Name,
        [string]$Xdc,
        [int]$RoA,
        [int]$RoB,
        [int]$PerturbMode,
        [string]$PerturbMask,
        [int]$SampleEnable,
        [int]$PairId,
        [int]$FamilyId,
        [int64]$StartDelayCycles = 2000000000,
        [int]$SampleDiv = 5000
    )

    return @{
        Name = $Name
        Xdc = $Xdc
        RoA = $RoA
        RoB = $RoB
        PerturbMode = $PerturbMode
        PerturbMask = $PerturbMask
        SampleEnable = $SampleEnable
        PairId = $PairId
        FamilyId = $FamilyId
        StartDelayCycles = $StartDelayCycles
        SampleDiv = $SampleDiv
    }
}

# PERTURB_MODE:
#   0 = only the measured A/B pair is enabled
#   1 = all 8 data ROs are enabled
#   2 = measured pair plus PERTURB_MASK
#   3 = measured pair plus sample RO enabled
$smokeRuns = @(
    (New-Run `
        -Name "tdc_mask_random1_ro0_ro1_pair_only_smoke" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_baseline.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 0 -PerturbMask "8'h00" -SampleEnable 0 `
        -PairId 3101 -FamilyId 1 -SampleDiv 1000)
)

$p0Runs = @(
    (New-Run `
        -Name "tdc_mask_random1_ro0_ro1_pair_only" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_baseline.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 0 -PerturbMask "8'h00" -SampleEnable 0 `
        -PairId 3201 -FamilyId 1),
    (New-Run `
        -Name "tdc_mask_random1_ro0_ro1_all_data_on" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_baseline.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 1 -PerturbMask "8'hFF" -SampleEnable 0 `
        -PairId 3202 -FamilyId 1),
    (New-Run `
        -Name "tdc_mask_random1_ro0_ro1_pair_plus_sample" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_baseline.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 3 -PerturbMask "8'h00" -SampleEnable 1 `
        -PairId 3203 -FamilyId 1),
    (New-Run `
        -Name "tdc_mask_random3_ro0_ro6_pair_only" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
        -RoA 0 -RoB 6 -PerturbMode 0 -PerturbMask "8'h00" -SampleEnable 0 `
        -PairId 3301 -FamilyId 3),
    (New-Run `
        -Name "tdc_mask_random3_ro0_ro6_all_data_on" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
        -RoA 0 -RoB 6 -PerturbMode 1 -PerturbMask "8'hFF" -SampleEnable 0 `
        -PairId 3302 -FamilyId 3),
    (New-Run `
        -Name "tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_local_x45y39.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 3 -PerturbMask "8'h00" -SampleEnable 1 `
        -PairId 3401 -FamilyId 1)
)

$matrixRuns = @(
    $p0Runs +
    @(
        (New-Run `
            -Name "tdc_mask_random1_ro0_ro1_neighbors_on" `
            -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_baseline.xdc" `
            -RoA 0 -RoB 1 -PerturbMode 2 -PerturbMask "8'h3C" -SampleEnable 0 `
            -PairId 3204 -FamilyId 1),
        (New-Run `
            -Name "tdc_mask_random3_ro0_ro6_neighbors_on" `
            -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
            -RoA 0 -RoB 6 -PerturbMode 2 -PerturbMask "8'h3E" -SampleEnable 0 `
            -PairId 3303 -FamilyId 3),
        (New-Run `
            -Name "tdc_mask_random3_ro0_ro6_pair_plus_sample" `
            -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
            -RoA 0 -RoB 6 -PerturbMode 3 -PerturbMask "8'h00" -SampleEnable 1 `
            -PairId 3304 -FamilyId 3),
        (New-Run `
            -Name "tdc_mask_random1_local_sample_ro0_ro1_pair_only" `
            -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_local_x45y39.xdc" `
            -RoA 0 -RoB 1 -PerturbMode 0 -PerturbMask "8'h00" -SampleEnable 0 `
            -PairId 3402 -FamilyId 1)
    )
)

$p1Runs = @(
    (New-Run `
        -Name "tdc_mask_random3_ro0_ro6_all_data_on_repeat02" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
        -RoA 0 -RoB 6 -PerturbMode 1 -PerturbMask "8'hFF" -SampleEnable 0 `
        -PairId 3312 -FamilyId 3),
    (New-Run `
        -Name "tdc_mask_random3_ro0_ro6_neighbors_on" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
        -RoA 0 -RoB 6 -PerturbMode 2 -PerturbMask "8'h3E" -SampleEnable 0 `
        -PairId 3303 -FamilyId 3),
    (New-Run `
        -Name "tdc_mask_random3_ro0_ro6_pair_plus_sample" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random3_baseline.xdc" `
        -RoA 0 -RoB 6 -PerturbMode 3 -PerturbMask "8'h00" -SampleEnable 1 `
        -PairId 3304 -FamilyId 3),
    (New-Run `
        -Name "tdc_mask_random1_local_sample_ro0_ro1_pair_only" `
        -Xdc "data\experiments\xdc_tdc_mask_perturb\tdc_mask_perturb_random1_local_x45y39.xdc" `
        -RoA 0 -RoB 1 -PerturbMode 0 -PerturbMask "8'h00" -SampleEnable 0 `
        -PairId 3402 -FamilyId 1)
)

if ($Mode -eq "smoke") {
    $runs = $smokeRuns
} elseif ($Mode -eq "p0") {
    $runs = $p0Runs
} elseif ($Mode -eq "p1") {
    $runs = $p1Runs
} elseif ($Mode -eq "matrix") {
    $runs = $matrixRuns
} else {
    $runs = @($smokeRuns + $matrixRuns)
}

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}

Push-Location $Root
try {
    foreach ($run in $runs) {
        $xdc = Resolve-Path $run.Xdc
        $outDir = Join-Path $Root ("data\vivado_runs\fpga1_tdc_mask_perturb\" + $run.Name)
        $generic = "{RO_A_INDEX=$($run.RoA) RO_B_INDEX=$($run.RoB) PERTURB_MODE=$($run.PerturbMode) PERTURB_MASK=$($run.PerturbMask) SAMPLE_ENABLE=$($run.SampleEnable) PAIR_ID=$($run.PairId) FAMILY_ID=$($run.FamilyId) START_DELAY_CYCLES=$($run.StartDelayCycles) SAMPLE_DIV=$($run.SampleDiv)}"

        Write-Host "Building $($run.Name)"
        Write-Host "  XDC:      $xdc"
        Write-Host "  Out dir:  $outDir"
        Write-Host "  Generic:  $generic"
        & $VivadoBat -mode batch `
            -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
            -tclargs $xdc $outDir RO_TDC_pair_mask_perturb_top $generic
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado build failed for $($run.Name) with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}
