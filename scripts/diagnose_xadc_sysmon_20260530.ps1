param(
    [string]$OutCsv = "data\experiments\tvlsi_sampler_aperture_model_20260530\xadc_sysmon_diagnosis_20260530.csv",
    [string]$HwServerUrl = "localhost:3122",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

if (-not (Test-Path $VivadoBat)) {
    throw "Vivado not found: $VivadoBat"
}

$outAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutCsv)
$outDir = Split-Path -Parent $outAbs
New-Item -ItemType Directory -Force $outDir | Out-Null

& $VivadoBat -mode batch -source (Join-Path $repoRoot "scripts\vivado\diagnose_xadc_sysmon_20260530.tcl") -tclargs $outAbs $HwServerUrl
if ($LASTEXITCODE -ne 0) {
    throw "Vivado XADC sysmon diagnosis failed with exit code $LASTEXITCODE"
}

Write-Host "Wrote $outAbs"
