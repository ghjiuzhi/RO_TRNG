param(
    [Parameter(Mandatory = $true)]
    [string]$Port,

    [string]$Day = "",

    [ValidateSet("tdc", "trng", "all")]
    [string]$Set = "all",

    [int]$TdcRuns = 1,

    [int]$TrngRuns = 1,

    [string]$TdcBytes = "2MiB",

    [string]$TrngBytes = "10MiB",

    [int]$Baud = 115200,

    [switch]$ProgramWithVivado,

    [switch]$SkipProgramming,

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [string]$HwServerUrl = "localhost:3122",

    [switch]$Analyze
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path

if ($Day -eq "") {
    $Day = "$(Get-Date -Format yyyyMMdd)_fpga1_board1"
}

$tdcDir = Join-Path $repoRoot "data\hardware\$Day\tdc"
$trngDir = Join-Path $repoRoot "data\hardware\$Day\trng"
$metadataDir = Join-Path $repoRoot "data\hardware\$Day\metadata"
New-Item -ItemType Directory -Force $tdcDir, $trngDir, $metadataDir | Out-Null

$tdcBits = @(
    [pscustomobject]@{
        Id = "tdc_near"
        Kind = "tdc"
        Bitstream = "data\vivado_runs\fpga1_tdc_matrix\tdc_ro_near_x36y35\RO_TDC_sysclk_top.bit"
        Bytes = $TdcBytes
    },
    [pscustomobject]@{
        Id = "tdc_far"
        Kind = "tdc"
        Bitstream = "data\vivado_runs\fpga1_tdc_matrix\tdc_ro_far_x24y25\RO_TDC_sysclk_top.bit"
        Bytes = $TdcBytes
    }
)

$trngBits = @(
    [pscustomobject]@{ Id = "compact"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_sweep\ro_compact_x44y43\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "checker"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_sweep\ro_checker_pitch3_x44y43\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "same_column"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\same_column_pitch3_x44y35\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "row"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\row_pitch3_x38y43\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "sparse"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\sparse_pitch6_x36y35\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "cross_region"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\cross_region_x36y25\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "far"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\far_x20y25\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "random1"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed1_x36y35\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "random2"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed2_x36y35\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes },
    [pscustomobject]@{ Id = "random3"; Kind = "trng"; Bitstream = "data\vivado_runs\fpga1_ro_trng_matrix\random_seed3_x36y35\seed_1\RO_TRNG_top.bit"; Bytes = $TrngBytes }
)

$items = @()
if ($Set -in @("tdc", "all")) {
    $items += $tdcBits
}
if ($Set -in @("trng", "all")) {
    $items += $trngBits
}

function Program-Bitstream {
    param([string]$Bitstream)

    $bitAbs = (Resolve-Path (Join-Path $repoRoot $Bitstream)).Path
    if ($ProgramWithVivado) {
        & $VivadoBat -mode batch -source (Join-Path $repoRoot "scripts\vivado\program_bitstream.tcl") -tclargs $bitAbs $HwServerUrl
        if ($LASTEXITCODE -ne 0) {
            throw "Vivado programming failed with exit code $LASTEXITCODE"
        }
    } else {
        Write-Host ""
        Write-Host "Please program this bitstream now:"
        Write-Host "  $bitAbs"
        Read-Host "Press Enter after Program Device finishes"
    }
}

foreach ($item in $items) {
    $runs = if ($item.Kind -eq "tdc") { $TdcRuns } else { $TrngRuns }
    if ($SkipProgramming) {
        Write-Host ""
        Write-Host "Skipping programming. Assuming this bitstream is already loaded:"
        Write-Host "  $($item.Bitstream)"
    } else {
        Program-Bitstream -Bitstream $item.Bitstream
    }

    for ($i = 1; $i -le $runs; $i++) {
        $runId = "{0}_run{1:D2}" -f $item.Id, $i
        $outDir = if ($item.Kind -eq "tdc") { $tdcDir } else { $trngDir }
        $outFile = Join-Path $outDir "$runId.bin"

        $captureArgs = @{
            Port = $Port
            Baud = $Baud
            Kind = $item.Kind
            Run = $runId
            Bytes = $item.Bytes
            OutFile = $outFile
            Bitstream = $item.Bitstream
            MetadataDir = $metadataDir
        }
        if ($Analyze) {
            $captureArgs["Analyze"] = $true
        }

        & (Join-Path $repoRoot "scripts\capture_uart.ps1") @captureArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Capture failed for $runId with exit code $LASTEXITCODE"
        }
    }
}

Write-Host ""
Write-Host "Capture plan completed."
Write-Host "Data directory: $(Join-Path $repoRoot "data\hardware\$Day")"

& python (Join-Path $repoRoot "scripts\audit_hardware_runs.py") (Join-Path $repoRoot "data\hardware\$Day")
if ($LASTEXITCODE -ne 0) {
    throw "Hardware run audit failed with exit code $LASTEXITCODE"
}
