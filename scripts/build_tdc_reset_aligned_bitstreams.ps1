param(
    [ValidateSet("smoke", "matrix", "clean32k_p0", "clean32k_remaining", "clean32k", "w10_boundary", "all")]
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
        [int]$WarmupPackets,
        [int]$CapturePackets,
        [int]$SampleDiv = 5000,
        [int64]$StartDelayCycles = 200000,
        [int64]$RoEnableDelayCycles = 200000
    )

    return @{
        Name = $Name
        Xdc = $Xdc
        PairId = $PairId
        FamilyId = $FamilyId
        WarmupPackets = $WarmupPackets
        CapturePackets = $CapturePackets
        SampleDiv = $SampleDiv
        StartDelayCycles = $StartDelayCycles
        RoEnableDelayCycles = $RoEnableDelayCycles
    }
}

$smokeRuns = @(
    (New-Run `
        -Name "tdc_reset_random1_baseline_ro0_smoke_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 1101 -FamilyId 1 -WarmupPackets 0 -CapturePackets 64 -SampleDiv 1000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_smoke_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1102 -FamilyId 1 -WarmupPackets 12 -CapturePackets 64 -SampleDiv 1000 -StartDelayCycles 16000000000)
)

$matrixRuns = @(
    (New-Run `
        -Name "tdc_reset_random1_baseline_ro0_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 1201 -FamilyId 1 -WarmupPackets 0 -CapturePackets 65536),
    (New-Run `
        -Name "tdc_reset_random1_baseline_ro0_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 1202 -FamilyId 1 -WarmupPackets 12 -CapturePackets 65536),
    (New-Run `
        -Name "tdc_reset_random3_goodref_ro0_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc" `
        -PairId 1301 -FamilyId 3 -WarmupPackets 0 -CapturePackets 65536),
    (New-Run `
        -Name "tdc_reset_random3_goodref_ro0_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc" `
        -PairId 1302 -FamilyId 3 -WarmupPackets 12 -CapturePackets 65536),
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1401 -FamilyId 1 -WarmupPackets 0 -CapturePackets 65536),
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1402 -FamilyId 1 -WarmupPackets 12 -CapturePackets 65536)
)

$clean32kRuns = @(
    (New-Run `
        -Name "tdc_reset_random1_baseline_ro0_clean32k_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 1501 -FamilyId 1 -WarmupPackets 0 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random1_baseline_ro0_clean32k_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc" `
        -PairId 1502 -FamilyId 1 -WarmupPackets 12 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random3_goodref_ro0_clean32k_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc" `
        -PairId 1503 -FamilyId 3 -WarmupPackets 0 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random3_goodref_ro0_clean32k_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc" `
        -PairId 1504 -FamilyId 3 -WarmupPackets 12 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_clean32k_warmup0" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1505 -FamilyId 1 -WarmupPackets 0 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000),
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_clean32k_warmup12" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1506 -FamilyId 1 -WarmupPackets 12 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000)
)

$w10BoundaryRuns = @(
    (New-Run `
        -Name "tdc_reset_random1_sampler_local_ro0_clean32k_warmup10" `
        -Xdc "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc" `
        -PairId 1510 -FamilyId 1 -WarmupPackets 10 -CapturePackets 32768 -SampleDiv 5000 -StartDelayCycles 16000000000)
)

if ($Mode -eq "smoke") {
    $runs = $smokeRuns
} elseif ($Mode -eq "matrix") {
    $runs = $matrixRuns
} elseif ($Mode -eq "clean32k_p0") {
    $runs = @($clean32kRuns[0])
} elseif ($Mode -eq "clean32k_remaining") {
    $runs = @($clean32kRuns[1..($clean32kRuns.Count - 1)])
} elseif ($Mode -eq "clean32k") {
    $runs = $clean32kRuns
} elseif ($Mode -eq "w10_boundary") {
    $runs = $w10BoundaryRuns
} else {
    $runs = @($smokeRuns + $matrixRuns + $clean32kRuns + $w10BoundaryRuns)
}

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}

Push-Location $Root
try {
    foreach ($run in $runs) {
        $xdc = Resolve-Path $run.Xdc
        $outDir = Join-Path $Root ("data\vivado_runs\fpga1_tdc_reset_aligned\" + $run.Name)
        $generic = "{RO_A_STAGES=9 RO_B_STAGES=2 PAIR_ID=$($run.PairId) FAMILY_ID=$($run.FamilyId) WARMUP_PACKETS=$($run.WarmupPackets) CAPTURE_PACKETS=$($run.CapturePackets) SAMPLE_DIV=$($run.SampleDiv) START_DELAY_CYCLES=$($run.StartDelayCycles) RO_ENABLE_DELAY_CYCLES=$($run.RoEnableDelayCycles)}"

        Write-Host "Building $($run.Name)"
        Write-Host "  XDC:      $xdc"
        Write-Host "  Out dir:  $outDir"
        Write-Host "  Generic:  $generic"
        & $VivadoBat -mode batch `
            -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
            -tclargs $xdc $outDir RO_TDC_reset_aligned_top $generic
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado build failed for $($run.Name) with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}
