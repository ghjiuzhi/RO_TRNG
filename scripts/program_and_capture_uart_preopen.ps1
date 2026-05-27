param(
    [Parameter(Mandatory = $true)]
    [string]$Bitstream,

    [Parameter(Mandatory = $true)]
    [string]$Port,

    [Parameter(Mandatory = $true)]
    [string]$OutFile,

    [string]$Run = "",

    [string]$Bytes = "1KiB",

    [int]$Baud = 115200,

    [int]$IdleTimeoutSec = 30,

    [int]$ReadTimeoutMs = 1000,

    [int]$ReadBufferBytes = 1048576,

    [string]$MetadataDir = "",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [string]$BoardId = "z7020_b01"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SizeToBytes {
    param([string]$Value)

    $text = $Value.Trim()
    if ($text -match '^\d+$') {
        return [int64]$text
    }
    if ($text -match '^(\d+)(KiB|MiB|GiB|KB|MB|GB)$') {
        $n = [int64]$Matches[1]
        switch ($Matches[2]) {
            "KiB" { return $n * 1024 }
            "MiB" { return $n * 1024 * 1024 }
            "GiB" { return $n * 1024 * 1024 * 1024 }
            "KB"  { return $n * 1000 }
            "MB"  { return $n * 1000 * 1000 }
            "GB"  { return $n * 1000 * 1000 * 1000 }
        }
    }
    throw "Invalid byte count: $Value"
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
                throw "No UART bytes received for $IdleSeconds seconds while pre-open capture was active. Captured $captured / $Count bytes."
            }
        }
    }
    return $buffer
}

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$bitAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Bitstream)
if (-not (Test-Path $bitAbs)) {
    $candidate = Join-Path $repoRoot $Bitstream
    if (Test-Path $candidate) {
        $bitAbs = (Resolve-Path $candidate).Path
    } else {
        throw "Bitstream not found: $Bitstream"
    }
}

$byteCount = Convert-SizeToBytes $Bytes
if ($byteCount -le 0 -or $byteCount -gt [int64][int]::MaxValue) {
    throw "Bytes must be between 1 and $([int]::MaxValue): $Bytes"
}

$outPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutFile)
$outDir = Split-Path -Parent $outPath
New-Item -ItemType Directory -Force $outDir | Out-Null
if ($Run -eq "") {
    $Run = [System.IO.Path]::GetFileNameWithoutExtension($outPath)
}
if ($MetadataDir -eq "") {
    $MetadataDir = $outDir
}
$metadataPath = Join-Path ($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($MetadataDir)) "$Run.json"
New-Item -ItemType Directory -Force (Split-Path -Parent $metadataPath) | Out-Null

if (Test-Path $outPath) {
    Remove-Item -LiteralPath $outPath -Force
}
$tmpPath = "$outPath.tmp"
if (Test-Path $tmpPath) {
    Remove-Item -LiteralPath $tmpPath -Force
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
if ($ReadBufferBytes -gt 0) {
    try {
        $serial.ReadBufferSize = $ReadBufferBytes
    } catch {
        Write-Warning "Could not set serial ReadBufferSize=${ReadBufferBytes}: $($_.Exception.Message)"
    }
}

$start = Get-Date
$headerHex = ""
try {
    Write-Host "Opening $Port before programming, $Baud baud, 8N1, no flow control..."
    $serial.Open()
    Start-Sleep -Milliseconds 200
    $serial.DiscardInBuffer()

    Write-Host "Programming bitstream while serial capture is already armed:"
    Write-Host "  $bitAbs"
    & $VivadoBat -mode batch -source (Join-Path $repoRoot "scripts\vivado\program_bitstream.tcl") -tclargs $bitAbs $HwServerUrl | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Vivado programming failed with exit code $LASTEXITCODE"
    }

    Write-Host "Reading $byteCount bytes from already-open serial port..."
    $data = Read-SerialBytes -Serial $serial -Count ([int]$byteCount) -IdleSeconds $IdleTimeoutSec
    [System.IO.File]::WriteAllBytes($tmpPath, $data)
    Move-Item -LiteralPath $tmpPath -Destination $outPath -Force
    $headerLen = [Math]::Min(16, $data.Length)
    $headerBytes = New-Object byte[] $headerLen
    [Array]::Copy($data, 0, $headerBytes, 0, $headerLen)
    $headerHex = [System.BitConverter]::ToString($headerBytes).Replace("-", "")
} finally {
    if ($serial -ne $null -and $serial.IsOpen) {
        $serial.Close()
    }
}

$end = Get-Date
$hash = (Get-FileHash -Path $outPath -Algorithm SHA256).Hash
"$hash  $outPath" | Set-Content -Path "$outPath.sha256.txt" -Encoding ASCII

$metadata = [ordered]@{
    capture_id = $Run
    board_id = $BoardId
    capture_method = "preopen_serial_then_program"
    bitstream = $Bitstream
    bitstream_resolved = $bitAbs
    bitstream_sha256 = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
    output_file = $outPath
    output_sha256 = $hash
    output_bytes = (Get-Item -LiteralPath $outPath).Length
    first_16_bytes_hex = $headerHex
    uart_port = $Port
    baud = $Baud
    read_timeout_ms = $ReadTimeoutMs
    idle_timeout_sec = $IdleTimeoutSec
    read_buffer_bytes = $ReadBufferBytes
    start_time = $start.ToString("yyyy-MM-dd HH:mm:ss")
    end_time = $end.ToString("yyyy-MM-dd HH:mm:ss")
    duration_seconds = [Math]::Round(($end - $start).TotalSeconds, 3)
    capture_script = $PSCommandPath
}
$metadata | ConvertTo-Json -Depth 5 | Set-Content -Path $metadataPath -Encoding UTF8

Write-Host "Pre-open capture complete."
Write-Host "  File:   $outPath"
Write-Host "  Bytes:  $((Get-Item -LiteralPath $outPath).Length)"
Write-Host "  SHA256: $hash"
Write-Host "  First16:$headerHex"
Write-Host "  Meta:   $metadataPath"
