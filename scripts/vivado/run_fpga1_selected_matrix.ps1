param(
    [string]$Vivado = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$MatrixCsv = "data\experiments\xdc_matrix\matrix_manifest.csv",
    [string]$OutRoot = "data\vivado_runs\fpga1_ro_trng_matrix",
    [string[]]$Names = @(),
    [int[]]$Seeds = @(1)
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $root

$rows = Import-Csv $MatrixCsv
if ($Names.Count -gt 0) {
    $rows = $rows | Where-Object { $Names -contains $_.name }
}

foreach ($row in $rows) {
    foreach ($seed in $Seeds) {
        $xdc = Resolve-Path $row.xdc
        $outDir = Join-Path $OutRoot (Join-Path $row.name "seed_$seed")
        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        Write-Host "Running $($row.name), seed $seed"
        & $Vivado -mode batch -source .\scripts\vivado\run_fpga1_ro_trng_sweep_inmem.tcl -tclargs $xdc $outDir $seed
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado failed for $($row.name), seed $seed with exit code $LASTEXITCODE"
        }
    }
}
