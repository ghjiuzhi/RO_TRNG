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

    [int]$HeaderBytes = 0,

    [int]$SettleMs = 500,

    [int]$ReadTimeoutMs = 1000,

    [int]$ReadBufferBytes = 0,

    [int]$IdleTimeoutSec = 30,

    [int]$MaxRetriesPerRestart = 2,

    [ValidateSet("program_bitstream", "auto_stream_once")]
    [string]$RestartMethod = "program_bitstream",

    [string]$Run = "",

    [string]$MetadataFile = "",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",

    [switch]$RecordXadc,

    [string]$XadcCsv = "",

    [string]$BoardId = "z7020_b01"
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

function Open-CaptureSerial {
    param(
        [string]$PortName,
        [int]$BaudRate,
        [int]$TimeoutMs,
        [int]$InputBufferBytes = 0
    )

    $serial = [System.IO.Ports.SerialPort]::new(
        $PortName,
        $BaudRate,
        [System.IO.Ports.Parity]::None,
        8,
        [System.IO.Ports.StopBits]::One
    )
    if ($InputBufferBytes -gt 0) {
        try {
            $serial.ReadBufferSize = $InputBufferBytes
        } catch {
            Write-Warning "Could not set serial ReadBufferSize=${InputBufferBytes}: $($_.Exception.Message)"
        }
    }
    $serial.Handshake = [System.IO.Ports.Handshake]::None
    $serial.ReadTimeout = $TimeoutMs
    $serial.WriteTimeout = $TimeoutMs
    $serial.DtrEnable = $false
    $serial.RtsEnable = $false
    return $serial
}

function Get-ExpectedRestartHeaderHex {
    param(
        [int]$RestartCountValue,
        [int]$SymbolsPerRestartValue
    )

    if ($RestartCountValue -lt 0 -or $RestartCountValue -gt 65535) {
        return ""
    }
    if ($SymbolsPerRestartValue -lt 0 -or $SymbolsPerRestartValue -gt 65535) {
        return ""
    }

    $header = [byte[]]@(
        0xA5,
        0x5A,
        (($RestartCountValue -shr 8) -band 0xFF),
        ($RestartCountValue -band 0xFF),
        (($SymbolsPerRestartValue -shr 8) -band 0xFF),
        ($SymbolsPerRestartValue -band 0xFF),
        0x01,
        0xD0
    )
    return [System.BitConverter]::ToString($header).Replace("-", "")
}

function Read-LastXadcCsvRow {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return $null
    }
    try {
        $rows = Import-Csv -Path $Path
        if ($rows.Count -eq 0) {
            return $null
        }
        return $rows[-1]
    } catch {
        Write-Warning "Could not parse XADC CSV ${Path}: $($_.Exception.Message)"
        return $null
    }
}

function Get-CsvField {
    param(
        [object]$Row,
        [string]$Name
    )

    if ($null -eq $Row) {
        return ""
    }
    $prop = $Row.PSObject.Properties[$Name]
    if ($null -eq $prop) {
        return ""
    }
    return [string]$prop.Value
}

function Invoke-XadcSnapshot {
    param(
        [string]$Phase,
        [string]$CsvPath
    )

    $result = [ordered]@{
        phase = $Phase
        status = "not_requested"
        csv = $CsvPath
        timestamp = ""
        temperature_c = ""
        vccint_v = ""
        vccaux_v = ""
        vccbram_v = ""
        vpvn_v = ""
        error = ""
    }

    if (-not $RecordXadc) {
        return $result
    }

    try {
        Write-Host "Reading XADC snapshot ($Phase)..."
        & (Join-Path $repoRoot "scripts\read_xadc.ps1") `
            -OutCsv $CsvPath `
            -HwServerUrl $HwServerUrl `
            -VivadoBat $VivadoBat |
            ForEach-Object { Write-Host $_ }
        if ($LASTEXITCODE -ne 0) {
            throw "read_xadc.ps1 exited with $LASTEXITCODE"
        }
        $row = Read-LastXadcCsvRow -Path $CsvPath
        if ($null -ne $row) {
            $result["timestamp"] = Get-CsvField -Row $row -Name "timestamp"
            $result["temperature_c"] = Get-CsvField -Row $row -Name "TEMPERATURE"
            $result["vccint_v"] = Get-CsvField -Row $row -Name "VCCINT"
            $result["vccaux_v"] = Get-CsvField -Row $row -Name "VCCAUX"
            $result["vccbram_v"] = Get-CsvField -Row $row -Name "VCCBRAM"
            $result["vpvn_v"] = Get-CsvField -Row $row -Name "VPVN"
        }
        $result["status"] = "ok"
    } catch {
        $result["status"] = "failed"
        $result["error"] = $_.Exception.Message
        Write-Warning "XADC snapshot failed ($Phase): $($_.Exception.Message)"
    }
    return $result
}

if ($RestartCount -le 0) { throw "RestartCount must be positive." }
if ($SymbolsPerRestart -le 0) { throw "SymbolsPerRestart must be positive." }
if ($BitsPerSymbol -lt 1 -or $BitsPerSymbol -gt 8) { throw "BitsPerSymbol must be between 1 and 8." }
if ($WarmupSymbols -lt 0) { throw "WarmupSymbols must be non-negative." }
if ($HeaderBytes -lt 0) { throw "HeaderBytes must be non-negative." }

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

if ($XadcCsv -eq "") {
    $XadcCsv = Join-Path $metadataDir "xadc_readings.csv"
}
$xadcCsvPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($XadcCsv)
$xadcDir = Split-Path -Parent $xadcCsvPath
if (-not (Test-Path $xadcDir)) {
    New-Item -ItemType Directory -Force $xadcDir | Out-Null
}

$tmpPath = "$outPath.tmp"
$hashPath = "$outPath.sha256.txt"
$rowBytesToRead = $WarmupSymbols + $SymbolsPerRestart
$expectedBytes = [int64]$RestartCount * [int64]$SymbolsPerRestart
$autoReadBufferBytes = $ReadBufferBytes
if ($autoReadBufferBytes -le 0) {
    $autoReadBufferBytes = [int][Math]::Min([int64]::MaxValue, [Math]::Max(4096, $expectedBytes + $HeaderBytes + 65536))
}
$bitHash = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
$scriptHash = (Get-FileHash -Path $PSCommandPath -Algorithm SHA256).Hash
$programTcl = Join-Path $repoRoot "scripts\vivado\program_bitstream.tcl"

if (Test-Path $tmpPath) { Remove-Item -LiteralPath $tmpPath -Force }
if (Test-Path $outPath) { Remove-Item -LiteralPath $outPath -Force }

$startTime = Get-Date
$xadcBefore = Invoke-XadcSnapshot -Phase "before_restart_capture" -CsvPath $xadcCsvPath
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
Write-Host "  Header bytes:        $HeaderBytes"
if ($RestartMethod -eq "auto_stream_once") {
    Write-Host "  Read buffer bytes:   $autoReadBufferBytes"
}
Write-Host "  Output:              $outPath"

$fs = [System.IO.File]::Open($tmpPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
$headerHex = ""
try {
    if ($RestartMethod -eq "auto_stream_once") {
        $serial = Open-CaptureSerial -PortName $Port -BaudRate $Baud -TimeoutMs $ReadTimeoutMs -InputBufferBytes $autoReadBufferBytes
        try {
            $captureStart = Get-Date
            $serial.Open()
            Start-Sleep -Milliseconds 200
            $serial.DiscardInBuffer()

            Write-Host "Programming restart auto-stream bitstream once..."
            & $VivadoBat -mode batch -source $programTcl -tclargs $bitAbs $HwServerUrl | Out-Host
            if ($LASTEXITCODE -ne 0) {
                throw "Vivado programming failed with exit code $LASTEXITCODE"
            }

            # The previous bitstream may emit UART bytes while Vivado is starting/programming.
            # Clear the PC-side buffer after programming so debug-header reads are from the new design.
            $serial.DiscardInBuffer()
            Start-Sleep -Milliseconds 100

            if ($SettleMs -gt 0) {
                Start-Sleep -Milliseconds $SettleMs
            }

            if ($HeaderBytes -gt 0) {
                $headerBytesRaw = Read-SerialBytes -Serial $serial -Count $HeaderBytes -IdleSeconds $IdleTimeoutSec
                $headerHex = [System.BitConverter]::ToString($headerBytesRaw).Replace("-", "")
                Write-Host "  Header: $headerHex"
                if ($HeaderBytes -eq 8) {
                    $expectedHeaderHex = Get-ExpectedRestartHeaderHex -RestartCountValue $RestartCount -SymbolsPerRestartValue $SymbolsPerRestart
                    if ($expectedHeaderHex -ne "" -and $headerHex -ne $expectedHeaderHex) {
                        throw "Restart debug header mismatch: expected $expectedHeaderHex, got $headerHex. This usually means stale UART bytes, wrong bitstream generics, or HeaderBytes does not match DEBUG_HEADER."
                    }
                }
            }

            $allBytes = Read-SerialBytes -Serial $serial -Count $expectedBytes -IdleSeconds $IdleTimeoutSec
            $fs.Write($allBytes, 0, $allBytes.Length)
            $fs.Flush()
            $captureEnd = Get-Date
            $totalDuration = ($captureEnd - $captureStart).TotalSeconds
            for ($restartIndex = 0; $restartIndex -lt $RestartCount; $restartIndex++) {
                $rowRecords.Add([ordered]@{
                    restart_index = $restartIndex
                    attempts = 1
                    bytes_read = $SymbolsPerRestart
                    bytes_written = $SymbolsPerRestart
                    start_time = $captureStart.ToString("yyyy-MM-dd HH:mm:ss")
                    end_time = $captureEnd.ToString("yyyy-MM-dd HH:mm:ss")
                    duration_seconds = [Math]::Round($totalDuration / $RestartCount, 3)
                    source = "auto_stream_partitioned"
                }) | Out-Null
            }
        } finally {
            if ($serial -ne $null -and $serial.IsOpen) {
                $serial.Close()
            }
        }
    }
    else {
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

                    $serial = Open-CaptureSerial -PortName $Port -BaudRate $Baud -TimeoutMs $ReadTimeoutMs
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
$xadcAfter = Invoke-XadcSnapshot -Phase "after_restart_capture" -CsvPath $xadcCsvPath
$hash = (Get-FileHash -Path $outPath -Algorithm SHA256).Hash
"$hash  $outPath" | Set-Content -Path $hashPath -Encoding ASCII

$isFormal90BRestartSize = ($RestartCount -eq 1000 -and $SymbolsPerRestart -eq 1000)
$metadata = [ordered]@{
    dataset_type = "SP800-90B restart dataset"
    capture_id = $Run
    board_id = $BoardId
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
    header_bytes = $HeaderBytes
    header_hex = $headerHex
    settle_ms = $SettleMs
    uart_port = $Port
    baud = $Baud
    uart_format = "8N1, no parity, no flow control"
    read_timeout_ms = $ReadTimeoutMs
    read_buffer_bytes = if ($RestartMethod -eq "auto_stream_once") { $autoReadBufferBytes } else { "" }
    idle_timeout_sec = $IdleTimeoutSec
    max_retries_per_restart = $MaxRetriesPerRestart
    retry_total = $retryTotal
    formal_90b_restart_size = $isFormal90BRestartSize
    start_time = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
    end_time = $endTime.ToString("yyyy-MM-dd HH:mm:ss")
    duration_seconds = [Math]::Round(($endTime - $startTime).TotalSeconds, 3)
    xadc_csv = $xadcCsvPath
    xadc_before = $xadcBefore
    xadc_after = $xadcAfter
    capture_script = $PSCommandPath
    capture_script_sha256 = $scriptHash
    row_records = $rowRecords
    notes = if ($isFormal90BRestartSize) { "1000x1000 row-major restart matrix." } else { "Pilot/smoke restart matrix; do not report as formal SP800-90B restart result." }
    capture_path_semantics = if ($RestartMethod -eq "auto_stream_once") { "Program once, then stream row-major restart matrix over UART." } else { "Reprogram FPGA before each restart row." }
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
