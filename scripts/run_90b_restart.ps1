param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile,

    [Parameter(Mandatory = $true)]
    [double]$InitialEntropy,

    [int]$BitsPerSymbol = 8,

    [string]$ResultDir = "",

    [string]$Run = "",

    [string]$MingwRoot = "D:\Toolsapp\MinGW",

    [string]$RepoRoot = "",

    [ValidateSet("non_iid", "iid")]
    [string]$Mode = "non_iid",

    [int]$SimulationCount = 0,

    [switch]$AllowNonStandardSize
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($RepoRoot -eq "") {
    $scriptRoot = Split-Path -Parent $PSCommandPath
    $RepoRoot = (Resolve-Path (Join-Path $scriptRoot "..")).Path
}

if ($BitsPerSymbol -lt 1 -or $BitsPerSymbol -gt 8) {
    throw "BitsPerSymbol must be between 1 and 8."
}

$env:Path = (Join-Path $MingwRoot "bin") + ";" + $env:Path
$exe = Join-Path $RepoRoot "sim\SP800-90B_EntropyAssessment\cpp\ea_restart.exe"
if (-not (Test-Path $exe)) {
    throw "ea_restart.exe not found. Build it first with scripts\build_90b_mingw.ps1"
}

$inputAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($InputFile)
if (-not (Test-Path $inputAbs)) {
    $candidate = Join-Path $RepoRoot $InputFile
    if (Test-Path $candidate) {
        $inputAbs = (Resolve-Path $candidate).Path
    } else {
        throw "Input file not found: $InputFile"
    }
}

$inputSize = (Get-Item -LiteralPath $inputAbs).Length
if ($inputSize -ne 1000000 -and -not $AllowNonStandardSize) {
    throw "ea_restart expects exactly 1000x1000 = 1,000,000 samples for formal use. File has $inputSize bytes. Use -AllowNonStandardSize only for tool-debug experiments."
}

if ($Run -eq "") {
    $Run = [System.IO.Path]::GetFileNameWithoutExtension($inputAbs)
}
if ($ResultDir -eq "") {
    $ResultDir = Join-Path (Split-Path -Parent $inputAbs) "ea_restart_$Run"
}
$resultAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ResultDir)
New-Item -ItemType Directory -Force $resultAbs | Out-Null

$modeFlag = if ($Mode -eq "iid") { "-i" } else { "-n" }
$args = New-Object System.Collections.Generic.List[string]
$args.Add($modeFlag) | Out-Null
if ($SimulationCount -gt 0) {
    $args.Add("-s") | Out-Null
    $args.Add([string]$SimulationCount) | Out-Null
}
$args.Add($inputAbs) | Out-Null
$args.Add([string]$BitsPerSymbol) | Out-Null
$args.Add(([string]::Format([System.Globalization.CultureInfo]::InvariantCulture, "{0:R}", $InitialEntropy))) | Out-Null

$stdout = Join-Path $resultAbs "$Run.ea_restart.stdout.txt"
$stderr = Join-Path $resultAbs "$Run.ea_restart.stderr.txt"
$version = Join-Path $resultAbs "$Run.ea_restart.version.txt"
$metadata = Join-Path $resultAbs "$Run.ea_restart.metadata.json"

& $exe --version 2>&1 | Out-File -FilePath $version -Encoding utf8

Write-Host "Running ea_restart:"
Write-Host "  exe:  $exe"
Write-Host "  args: $($args -join ' ')"
Write-Host "  out:  $stdout"

$startTime = Get-Date
$process = Start-Process -FilePath $exe -ArgumentList $args.ToArray() -NoNewWindow -Wait -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$exitCode = $process.ExitCode
$endTime = Get-Date
$stdoutText = ""
if (Test-Path $stdout) {
    $stdoutText = Get-Content -Path $stdout -Raw
}
$isRestartSanityFailure = $stdoutText -match "Restart Sanity Check Failed"
$isValidationPassed = $stdoutText -match "Validation Test Passed"

$inputHash = (Get-FileHash -Path $inputAbs -Algorithm SHA256).Hash
$meta = [ordered]@{
    tool = "ea_restart"
    mode = $Mode
    exe = $exe
    input_file = $inputAbs
    input_sha256 = $inputHash
    input_bytes = $inputSize
    bits_per_symbol = $BitsPerSymbol
    initial_entropy = $InitialEntropy
    simulation_count = $SimulationCount
    command = "$exe $($args -join ' ')"
    stdout = $stdout
    stderr = $stderr
    version_file = $version
    exit_code = $exitCode
    ea_restart_status = if ($isValidationPassed) { "passed" } elseif ($isRestartSanityFailure) { "failed" } else { "error" }
    start_time = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
    end_time = $endTime.ToString("yyyy-MM-dd HH:mm:ss")
    duration_seconds = [Math]::Round(($endTime - $startTime).TotalSeconds, 3)
}
$meta | ConvertTo-Json -Depth 5 | Set-Content -Path $metadata -Encoding UTF8

if ($exitCode -ne 0 -and -not $isRestartSanityFailure) {
    throw "ea_restart failed with exit code $exitCode. See $stdout and $stderr"
}
if ($isRestartSanityFailure) {
    Write-Warning "ea_restart completed with Restart Sanity Check Failed. This is a statistical result, not a runner error."
}

Write-Host "ea_restart complete."
Write-Host "  stdout:   $stdout"
Write-Host "  stderr:   $stderr"
Write-Host "  metadata: $metadata"
