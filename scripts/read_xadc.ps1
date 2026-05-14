param(
    [string]$OutCsv = "",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path

if ($OutCsv -eq "") {
    $OutCsv = Join-Path $repoRoot "data\hardware\xadc_readings.csv"
}

$outAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutCsv)
$outDir = Split-Path -Parent $outAbs
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force $outDir | Out-Null
}

& $VivadoBat -mode batch -source (Join-Path $repoRoot "scripts\vivado\read_xadc.tcl") -tclargs $outAbs $HwServerUrl
if ($LASTEXITCODE -ne 0) {
    throw "Vivado XADC read failed with exit code $LASTEXITCODE"
}
