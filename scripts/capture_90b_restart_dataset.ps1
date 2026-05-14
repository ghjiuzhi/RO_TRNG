param(
    [Parameter(Mandatory = $true)]
    [string]$Bitstream,

    [Parameter(Mandatory = $true)]
    [string]$OutFile,

    [string]$Port = "COM3",

    [int]$Baud = 115200,

    [int]$RestartCount = 1000,

    [int]$SymbolsPerRestart = 1000,

    [int]$BitsPerSymbol = 8,

    [int]$WarmupSymbols = 0,

    [int]$SettleMs = 500,

    [int]$ReadTimeoutMs = 1000,

    [int]$IdleTimeoutSec = 30,

    [int]$MaxRetriesPerRestart = 2,

    [ValidateSet("program_bitstream")]
    [string]$RestartMethod = "program_bitstream",

    [string]$Run = "",

    [string]$MetadataFile = "",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$PathValue)

    $scriptDir = Split-Path -Parent $PSCommandPath
    $repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
    $candidate = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PathValue)
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    $candidate = Join-Path $repoRoot $PathValue
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PathValue)
}

function Read-SerialBytes {
    param(
        [System.IO.Ports.SerialPort]$Serial,
        [int]$Count,
        [int]$IdleSeconds
    )

    $buffer = New-Object byte[] $Count
    $captured = 0
    $lastByteTime = Get-Date
    while ($captured -lt $Count) {
        try {
            $n = $Serial.Read($buffer, $captured, $Count - $captured)
            if ($n -gt 0) {
                $captured += $n
                $lastByteTime = Get-Date
            }
        } catch [TimeoutException] {
            $idle = ((Get-Date) - $lastByteTime).TotalSeconds
            if ($idle -ge $IdleSeconds) {
                throw "No UART bytes received for $IdleSeconds seconds while reading restart row."
            }
        }
    }
    return $buffer
}

if ($RestartCount -le 0) { throw "RestartCount must be positive." }
if ($SymbolsPerRestart -le 0) { throw "SymbolsPerRestart must be positive." }
if ($BitsPerSymbol -lt 1 -or $BitsPerSymbol -gt 8) { throw "BitsPerSymbol must be between 1 and 8." }
if ($WarmupSymbols -lt 0) { throw "WarmupSymbols must be non-negative." }

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$bitAbs = Resolve-RepoPath $Bitstream
if (-not (Test-Path $bitAbs)) {
    throw "Bitstream not found: $Bitstream"
}

$outPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutFile)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force $outDir | Out-Null
}

if ($Run -eq "") {
    $Run = [System.IO.Path]::GetFileNameWithoutExtension($outPath)
}
if ($MetadataFile -eq "") {
    $MetadataFile = Join-Path $outDir "$Run.metadata.json"
}
$metadataPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($MetadataFile)
$metadataDir = Split-Path -Parent $metadataPath
if (-not (Test-Path $metadataDir)) {
    New-Item -ItemType Directory -Force $metadataDir | Out-Null
}

$tmpPath = "$outPath.tmp"
$hashPath = "$outPath.sha256.txt"
$rowBytesToRead = $WarmupSymbols + $SymbolsPerRestart
$expectedBytes = [int64]$RestartCount * [int64]$SymbolsPerRestart
$bitHash = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
$scriptHash = (Get-FileHash -Path $PSCommandPath -Algorithm SHA256).Hash
$programTcl = Join-Path $repoRoot "scripts\vivado\program_bitstream.tcl"

if (Test-Path $tmpPath) { Remove-Item -LiteralPath $tmpPath -Force }
if (Test-Path $outPath) { Remove-Item -LiteralPath $outPath -Force }

$startTime = Get-Date
$rowRecords = New-Object System.Collections.Generic.List[object]
$retryTotal = 0

Write-Host "SP800-90B restart dataset capture"
Write-Host "  Run:                 $Run"
Write-Host "  Restart method:      $RestartMethod"
Write-Host "  Bitstream:           $bitAbs"
Write-Host "  UART:                $Port @ $Baud, 8N1"
Write-Host "  Matrix:              $RestartCount x $SymbolsPerRestart symbols"
Write-Host "  Bits per symbol:     $BitsPerSymbol"
Write-Host "  Warmup symbols:      $WarmupSymbols"
Write-Host "  Output:              $outPath"

$fs = [System.IO.File]::Open($tmpPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
try {
    for ($restartIndex = 0; $restartIndex -lt $RestartCount; $restartIndex++) {
        $rowOk = $false
        $attempt = 0
        while (-not $rowOk -and $attempt -le $MaxRetriesPerRestart) {
            $attemptStart = Get-Date
            $attempt++
            try {
                Write-Progress -Activity "SP800-90B restart capture $Run" -Status "restart $($restartIndex + 1) / $RestartCount, attempt $attempt" -PercentComplete ([Math]::Round((100.0 * $restartIndex) / $RestartCount, 2))
                Write-Host ("Restart row {0}/{1}, attempt {2}" -f ($restartIndex + 1), $RestartCount, $attempt)

                & $VivadoBat -mode batch -source $programTcl -tclargs $bitAbs $HwServerUrl | Out-Host
                if ($LASTEXITCODE -ne 0) {
                    throw "Vivado programming failed with exit code $LASTEXITCODE"
                }

                if ($SettleMs -gt 0) {
                    Start-Sleep -Milliseconds $SettleMs
                }

                $serial = [System.IO.Ports.SerialPort]::new(
                    $Port,
                    $Baud,
                    [System.IO.Ports.Parity]::None,
                    8,
                    [System.IO.Ports.StopBits]::One
                )
                $serial.Handshake = [System.IO.Ports.Handshake]::None
                $serial.ReadTimeout = $ReadTimeoutMs
                $serial.WriteTimeout = $ReadTimeoutMs
                $serial.DtrEnable = $false
                $serial.RtsEnable = $false

                try {
                    $serial.Open()
                    Start-Sleep -Milliseconds 200
                    $serial.DiscardInBuffer()
                    $rowRaw = Read-SerialBytes -Serial $serial -Count $rowBytesToRead -IdleSeconds $IdleTimeoutSec
                } finally {
                    if ($serial -ne $null -and $serial.IsOpen) {
                        $serial.Close()
                    }
                }

                $fs.Write($rowRaw, $WarmupSymbols, $SymbolsPerRestart)
                $fs.Flush()
                $rowOk = $true
                $attemptEnd = Get-Date
                $rowRecords.Add([ordered]@{
                    restart_index = $restartIndex
                    attempts = $attempt
                    bytes_read = $rowBytesToRead
                    bytes_written = $SymbolsPerRestart
                    start_time = $attemptStart.ToString("yyyy-MM-dd HH:mm:ss")
                    end_time = $attemptEnd.ToString("yyyy-MM-dd HH:mm:ss")
                    duration_seconds = [Math]::Round(($attemptEnd - $attemptStart).TotalSeconds, 3)
                }) | Out-Null
            } catch {
                $retryTotal++
                Write-Warning ("Restart row {0} attempt {1} failed: {2}" -f $restartIndex, $attempt, $_.Exception.Message)
                if ($attempt -gt $MaxRetriesPerRestart) {
                    throw "Restart row $restartIndex failed after $MaxRetriesPerRestart retries."
                }
                Start-Sleep -Seconds 2
            }
        }
    }
} finally {
    Write-Progress -Activity "SP800-90B restart capture $Run" -Completed
    $fs.Flush()
    $fs.Close()
}

$actualSize = (Get-Item -LiteralPath $tmpPath).Length
if ($actualSize -ne $expectedBytes) {
    throw "Restart dataset size mismatch: expected $expectedBytes bytes, got $actualSize bytes at $tmpPath"
}

Move-Item -LiteralPath $tmpPath -Destination $outPath -Force
$endTime = Get-Date
$hash = (Get-FileHash -Path $outPath -Algorithm SHA256).Hash
"$hash  $outPath" | Set-Content -Path $hashPath -Encoding ASCII

$isFormal90BRestartSize = ($RestartCount -eq 1000 -and $SymbolsPerRestart -eq 1000)
$metadata = [ordered]@{
    dataset_type = "SP800-90B restart dataset"
    capture_id = $Run
    output_file = $outPath
    output_sha256 = $hash
    output_bytes = $actualSize
    bitstream = $Bitstream
    bitstream_resolved = $bitAbs
    bitstream_sha256 = $bitHash
    restart_method = $RestartMethod
    restart_count = $RestartCount
    symbols_per_restart = $SymbolsPerRestart
    bits_per_symbol = $BitsPerSymbol
    warmup_symbols_discarded = $WarmupSymbols
    settle_ms = $SettleMs
    uart_port = $Port
    baud = $Baud
    uart_format = "8N1, no parity, no flow control"
    read_timeout_ms = $ReadTimeoutMs
    idle_timeout_sec = $IdleTimeoutSec
    max_retries_per_restart = $MaxRetriesPerRestart
    retry_total = $retryTotal
    formal_90b_restart_size = $isFormal90BRestartSize
    start_time = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
    end_time = $endTime.ToString("yyyy-MM-dd HH:mm:ss")
    duration_seconds = [Math]::Round(($endTime - $startTime).TotalSeconds, 3)
    capture_script = $PSCommandPath
    capture_script_sha256 = $scriptHash
    row_records = $rowRecords
    notes = if ($isFormal90BRestartSize) { "1000x1000 row-major restart matrix." } else { "Pilot/smoke restart matrix; do not report as formal SP800-90B restart result." }
}
$metadata | ConvertTo-Json -Depth 8 | Set-Content -Path $metadataPath -Encoding UTF8

Write-Host "Restart capture complete."
Write-Host "  File:     $outPath"
Write-Host "  Bytes:    $actualSize"
Write-Host "  SHA256:   $hash"
Write-Host "  Metadata: $metadataPath"
if (-not $isFormal90BRestartSize) {
    Write-Warning "This is not 1000x1000. It is a pilot/smoke dataset, not a formal ea_restart dataset."
}
