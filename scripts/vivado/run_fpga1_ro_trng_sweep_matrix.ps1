param(
    [string]$Vivado = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [int[]]$Seeds = @(1, 2, 3)
)

$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$Tcl = Join-Path $Root "scripts\vivado\run_fpga1_ro_trng_sweep_inmem.tcl"
$XdcDir = Join-Path $Root "data\experiments\xdc_examples"
$BuildRoot = Join-Path $Root "data\vivado_runs\fpga1_ro_trng_sweep"

$Xdcs = Get-ChildItem -Path $XdcDir -Filter "*.xdc" | Sort-Object Name
if ($Xdcs.Count -eq 0) {
    throw "No placement XDC files found in $XdcDir"
}

foreach ($xdc in $Xdcs) {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($xdc.Name)
    foreach ($seed in $Seeds) {
        $out = Join-Path $BuildRoot "$name\seed_$seed"
        New-Item -ItemType Directory -Force -Path $out | Out-Null
        & $Vivado -mode batch -source $Tcl -tclargs $xdc.FullName $out $seed
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado failed for $($xdc.Name), seed $seed"
        }
    }
}
