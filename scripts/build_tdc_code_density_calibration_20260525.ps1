param(
    [ValidateSet("smoke", "formal")]
    [string]$Mode = "smoke",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [string]$Root = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

function New-Run {
    param(
        [string]$Name,
        [int]$CalAStages,
        [int]$CalBStages,
        [int]$SampleDiv = 5000
    )
    return @{
        Name = $Name
        CalAStages = $CalAStages
        CalBStages = $CalBStages
        SampleDiv = $SampleDiv
    }
}

if (-not (Test-Path -LiteralPath $VivadoBat)) {
    throw "Vivado bat not found: $VivadoBat"
}

$runs = @()
if ($Mode -eq "smoke") {
    $runs += (New-Run -Name "tdc_code_density_cal_a7_b11_smoke_20260525" -CalAStages 7 -CalBStages 11)
} else {
    $runs += (New-Run -Name "tdc_code_density_cal_a7_b11_formal_20260525" -CalAStages 7 -CalBStages 11)
    $runs += (New-Run -Name "tdc_code_density_cal_a11_b7_formal_20260525" -CalAStages 11 -CalBStages 7)
}

Push-Location $Root
try {
    $extraXdc = "data\experiments\xdc_tdc_code_density\tdc_code_density_no_extra.xdc"
    if (-not (Test-Path -LiteralPath $extraXdc)) {
        throw "Placeholder XDC not found: $extraXdc"
    }

    foreach ($run in $runs) {
        $outDir = Join-Path $Root ("data\vivado_runs\fpga1_tdc_code_density_cal\" + $run.Name)
        $generic = "{CAL_A_STAGES=$($run.CalAStages) CAL_B_STAGES=$($run.CalBStages) SAMPLE_DIV=$($run.SampleDiv)}"

        Write-Host "Building $($run.Name)"
        Write-Host "  Out dir:  $outDir"
        Write-Host "  Generic:  $generic"
        & $VivadoBat -mode batch `
            -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl `
            -tclargs $extraXdc $outDir RO_TDC_code_density_cal_sysclk_top $generic
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado build failed for $($run.Name) with exit code $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
}
