param(
    [string]$MingwRoot = "D:\Toolsapp\MinGW",
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$env:Path = (Join-Path $MingwRoot "bin") + ";" + $env:Path
$cppDir = Join-Path $RepoRoot "sim\SP800-90B_EntropyAssessment\cpp"
$divDir = Join-Path $RepoRoot "third_party\libdivsufsort"
$buildDir = Join-Path $cppDir "build_mingw"
New-Item -ItemType Directory -Force $buildDir | Out-Null

$gcc = Join-Path $MingwRoot "bin\gcc.exe"
$gxx = Join-Path $MingwRoot "bin\g++.exe"
if (-not (Test-Path $gcc)) { throw "gcc.exe not found under $MingwRoot\bin" }
if (-not (Test-Path $gxx)) { throw "g++.exe not found under $MingwRoot\bin" }

$includeArgs = @(
    "-I$cppDir\compat",
    "-I$cppDir",
    "-I$divDir\include",
    "-I$MingwRoot\include"
)

$cSources = @("divsufsort.c", "sssort.c", "trsort.c", "utils.c")
$objects = New-Object System.Collections.Generic.List[string]
foreach ($src in $cSources) {
    $in = Join-Path $divDir "lib\$src"
    $out = Join-Path $buildDir ($src -replace "\.c$", "_32.o")
    & $gcc -O2 -DHAVE_CONFIG_H=1 @includeArgs -c $in -o $out
    if ($LASTEXITCODE -ne 0) { throw "Failed compiling $src 32-bit suffix-array object" }
    $objects.Add($out)
}
foreach ($src in $cSources) {
    $in = Join-Path $divDir "lib\$src"
    $out = Join-Path $buildDir ($src -replace "\.c$", "_64.o")
    & $gcc -O2 -DHAVE_CONFIG_H=1 -DBUILD_DIVSUFSORT64 @includeArgs -c $in -o $out
    if ($LASTEXITCODE -ne 0) { throw "Failed compiling $src 64-bit suffix-array object" }
    $objects.Add($out)
}

$exe = Join-Path $cppDir "ea_non_iid.exe"
& $gxx -std=c++11 -fopenmp -O2 -ffloat-store @includeArgs `
    (Join-Path $cppDir "non_iid_main.cpp") `
    @($objects.ToArray()) `
    -L"$MingwRoot\lib" -lbz2 -ladvapi32 -o $exe
if ($LASTEXITCODE -ne 0) { throw "Failed linking ea_non_iid.exe" }

Write-Host "Built $exe"
