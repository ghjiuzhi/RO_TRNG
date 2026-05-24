param(
    [Parameter(Mandatory = $true)]
    [string]$Bitstream,

    [Parameter(Mandatory = $true)]
    [string]$Port,

    [Parameter(Mandatory = $true)]
    [string]$OutFile,

    [ValidateSet("raw", "tdc", "trng", "restart")]
    [string]$Kind = "raw",

    [string]$Run = "",

    [string]$Bytes = "1KiB",

    [int]$Baud = 115200,

    [string]$MetadataDir = "",

    [int]$IdleTimeoutSec = 30,

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [switch]$RecordXadc,

    [string]$XadcCsv = "",

    [string]$BoardId = "z7020_b01",

    [switch]$Analyze
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$bitAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Bitstream)

if (-not (Test-Path $bitAbs)) {
    $candidate = Join-Path $repoRoot $Bitstream
    if (Test-Path $candidate) {
        $bitAbs = (Resolve-Path $candidate).Path
    } else {
        throw "Bitstream not found: $Bitstream"
    }
}

Write-Host "Programming bitstream first:"
Write-Host "  $bitAbs"
& $VivadoBat -mode batch -source (Join-Path $repoRoot "scripts\vivado\program_bitstream.tcl") -tclargs $bitAbs $HwServerUrl
if ($LASTEXITCODE -ne 0) {
    throw "Vivado programming failed with exit code $LASTEXITCODE"
}

Write-Host "Waiting 2 seconds after programming..."
Start-Sleep -Seconds 2

$captureArgs = @{
    Port = $Port
    Baud = $Baud
    Kind = $Kind
    Bytes = $Bytes
    OutFile = $OutFile
    Bitstream = $Bitstream
    BoardId = $BoardId
    IdleTimeoutSec = $IdleTimeoutSec
}
if ($Run -ne "") {
    $captureArgs["Run"] = $Run
}
if ($MetadataDir -ne "") {
    $captureArgs["MetadataDir"] = $MetadataDir
}
if ($Analyze) {
    $captureArgs["Analyze"] = $true
}
if ($RecordXadc) {
    $captureArgs["RecordXadc"] = $true
    $captureArgs["HwServerUrl"] = $HwServerUrl
    $captureArgs["VivadoBat"] = $VivadoBat
}
if ($XadcCsv -ne "") {
    $captureArgs["XadcCsv"] = $XadcCsv
}

& (Join-Path $repoRoot "scripts\capture_uart.ps1") @captureArgs
if ($LASTEXITCODE -ne 0) {
    throw "Capture failed with exit code $LASTEXITCODE"
}
