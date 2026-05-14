param(
    [string]$MingwRoot = "D:\Toolsapp\MinGW",
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$InputDir = "data\sp800_90b\inputs_smoke_20260514",
    [string]$ResultDir = "data\sp800_90b\results_smoke_20260514",
    [string[]]$Modes = @("bps1_msb"),
    [int]$LimitSymbols = 1000000,
    [switch]$Overwrite
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$env:Path = (Join-Path $MingwRoot "bin") + ";" + $env:Path
$exe = Join-Path $RepoRoot "sim\SP800-90B_EntropyAssessment\cpp\ea_non_iid.exe"
if (-not (Test-Path $exe)) {
    throw "ea_non_iid.exe not found. Build it first with scripts\build_90b_mingw.ps1"
}

$inputRoot = Join-Path $RepoRoot $InputDir
$outputRoot = Join-Path $RepoRoot $ResultDir
New-Item -ItemType Directory -Force $outputRoot | Out-Null

foreach ($mode in $Modes) {
    $bitsPerSymbol = if ($mode -eq "bps8") { 8 } elseif ($mode -eq "bps1_msb" -or $mode -eq "bps1_lsb") { 1 } else { throw "Unknown mode $mode" }
    $pattern = "*_${mode}.bin"
    $inputs = Get-ChildItem -Path $inputRoot -Filter $pattern | Sort-Object Name
    if ($inputs.Count -eq 0) {
        Write-Warning "No inputs matched $pattern under $inputRoot"
        continue
    }

    foreach ($input in $inputs) {
        $stem = [System.IO.Path]::GetFileNameWithoutExtension($input.Name)
        $log = Join-Path $outputRoot ("{0}_non_iid_{1}m.log" -f $stem, [Math]::Floor($LimitSymbols / 1000000))
        if ((Test-Path $log) -and -not $Overwrite) {
            Write-Host "Skipping existing $log"
            continue
        }

        Write-Host "Running SP800-90B non-IID: $($input.Name), bps=$bitsPerSymbol, limit=$LimitSymbols"
        & $exe -l "0,$LimitSymbols" $input.FullName $bitsPerSymbol 2>&1 | Out-File -FilePath $log -Encoding utf8
        if ($LASTEXITCODE -ne 0) {
            throw "ea_non_iid failed for $($input.FullName) with exit code $LASTEXITCODE. See $log"
        }
    }
}
