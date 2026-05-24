param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

$runs = @(
    @{ Name = "tdc_sampler_data_random1_baseline_sample_x36y35_ro0"; Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro0.xdc"; PairId = 101; FamilyId = 1 },
    @{ Name = "tdc_sampler_data_random1_local_sample_x45y39_ro0";    Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro0.xdc";    PairId = 102; FamilyId = 1 },
    @{ Name = "tdc_sampler_data_random1_baseline_sample_x36y35_ro4"; Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_baseline_sample_x36y35_ro4.xdc"; PairId = 103; FamilyId = 1 },
    @{ Name = "tdc_sampler_data_random1_local_sample_x45y39_ro4";    Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random1_local_sample_x45y39_ro4.xdc";    PairId = 104; FamilyId = 1 },
    @{ Name = "tdc_sampler_data_random3_sample_x36y35_ro0";          Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro0.xdc";          PairId = 301; FamilyId = 3 },
    @{ Name = "tdc_sampler_data_random3_sample_x36y35_ro3";          Xdc = "data\experiments\xdc_tdc_sampler_data\tdc_sampler_data_random3_sample_x36y35_ro3.xdc";          PairId = 303; FamilyId = 3 }
)

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}

Push-Location $Root
try {
    foreach ($run in $runs) {
        $xdc = Resolve-Path $run.Xdc
        $outDir = Join-Path $Root ("data\vivado_runs\fpga1_tdc_sampler_data\" + $run.Name)
        $generic = "{RO_A_STAGES=9 RO_B_STAGES=2 PAIR_ID=$($run.PairId) FAMILY_ID=$($run.FamilyId)}"
        Write-Host "Building $($run.Name)"
        Write-Host "  XDC:      $xdc"
        Write-Host "  Out dir:  $outDir"
        Write-Host "  Generic:  $generic"
        & $VivadoBat -mode batch `
            -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
            -tclargs $xdc $outDir RO_TDC_pair_sysclk_top $generic
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado build failed for $($run.Name) with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}
