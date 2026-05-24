param(
    [ValidateSet("smoke", "matrix", "ro4", "random3_ro3", "all")]
    [string]$Mode = "smoke",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

function New-Run {
    param(
        [string]$Name,
        [string]$Xdc,
        [int]$PairId,
        [int]$FamilyId,
        [int64]$StartDelayCycles,
        [int]$SampleDiv = 5000
    )

    return @{
        Name = $Name
        Xdc = $Xdc
        PairId = $PairId
        FamilyId = $FamilyId
        StartDelayCycles = $StartDelayCycles
        SampleDiv = $SampleDiv
    }
}

# START_DELAY_CYCLES is in the 200 MHz clock domain. The capture wrapper waits
# about 2 seconds after programming before opening COM3, but Vivado shutdown and
# Windows serial open timing vary. 2,000,000,000 cycles is about 10 seconds and
# keeps the enable edge inside a short capture with comfortable margin.
$smokeRuns = @(
    (New-Run `
        -Name "tdc_reset_enable_random1_baseline_ro0_smoke" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 2101 -FamilyId 1 -StartDelayCycles 2000000000 -SampleDiv 1000)
)

$matrixRuns = @(
    (New-Run `
        -Name "tdc_reset_enable_random1_baseline_ro0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 2201 -FamilyId 1 -StartDelayCycles 2000000000),
    (New-Run `
        -Name "tdc_reset_enable_random3_goodref_ro0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc" `
        -PairId 2301 -FamilyId 3 -StartDelayCycles 2000000000),
    (New-Run `
        -Name "tdc_reset_enable_random1_sampler_local_ro0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 2401 -FamilyId 1 -StartDelayCycles 2000000000)
)

$ro4Runs = @(
    (New-Run `
        -Name "tdc_reset_enable_random1_baseline_ro4" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro4.xdc" `
        -PairId 2204 -FamilyId 1 -StartDelayCycles 2000000000),
    (New-Run `
        -Name "tdc_reset_enable_random1_sampler_local_ro4" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro4.xdc" `
        -PairId 2404 -FamilyId 1 -StartDelayCycles 2000000000)
)

$random3Ro3Runs = @(
    (New-Run `
        -Name "tdc_reset_enable_random3_goodref_ro3" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro3.xdc" `
        -PairId 2303 -FamilyId 3 -StartDelayCycles 2000000000)
)

if ($Mode -eq "smoke") {
    $runs = $smokeRuns
} elseif ($Mode -eq "matrix") {
    $runs = $matrixRuns
} elseif ($Mode -eq "ro4") {
    $runs = $ro4Runs
} elseif ($Mode -eq "random3_ro3") {
    $runs = $random3Ro3Runs
} else {
    $runs = @($smokeRuns + $matrixRuns + $ro4Runs + $random3Ro3Runs)
}

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}

Push-Location $Root
try {
    foreach ($run in $runs) {
        $xdc = Resolve-Path $run.Xdc
        $outDir = Join-Path $Root ("data\vivado_runs\fpga1_tdc_reset_enable\" + $run.Name)
        $generic = "{RO_A_STAGES=9 RO_B_STAGES=2 PAIR_ID=$($run.PairId) FAMILY_ID=$($run.FamilyId) START_DELAY_CYCLES=$($run.StartDelayCycles) SAMPLE_DIV=$($run.SampleDiv)}"

        Write-Host "Building $($run.Name)"
        Write-Host "  XDC:      $xdc"
        Write-Host "  Out dir:  $outDir"
        Write-Host "  Generic:  $generic"
        & $VivadoBat -mode batch `
            -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
            -tclargs $xdc $outDir RO_TDC_pair_reset_enable_top $generic
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado build failed for $($run.Name) with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}
