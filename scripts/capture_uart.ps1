param(
    [Parameter(Mandatory = $true)]
    [string]$Port,

    [int]$Baud = 115200,

    [Parameter(Mandatory = $true)]
    [string]$OutFile,

    [string]$Bytes = "10MiB",

    [ValidateSet("raw", "tdc", "trng", "restart")]
    [string]$Kind = "raw",

    [string]$Run = "",

    [string]$Bitstream = "",

    [string]$MetadataDir = "",

    [switch]$Analyze,

    [int]$ClockPeriodPs = 5000,

    [int]$TdcBins = 256,

    [string]$Python = "python",

    [int]$ReadTimeoutMs = 1000,

    [int]$IdleTimeoutSec = 30,

    [switch]$RecordXadc,

    [ValidateSet("before_after", "after_only")]
    [string]$XadcMode = "before_after",

    [string]$XadcCsv = "",

    [string]$HwServerUrl = "localhost:3122",

    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat"
    ,
    [string]$BoardId = "z7020_b01"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SizeToBytes {
    param([string]$Value)

    $text = $Value.Trim()
    if ($text -match '^(?<num>\d+)(?<unit>\s*(B|K|KB|KiB|M|MB|MiB|G|GB|GiB)?)$') {
        [int64]$num = [int64]$Matches['num']
        $unit = $Matches['unit'].Trim().ToLowerInvariant()
        switch ($unit) {
            { $_ -in @('', 'b') } { return $num }
            { $_ -in @('k', 'kb') } { return $num * 1000 }
            'kib' { return $num * 1024 }
            { $_ -in @('m', 'mb') } { return $num * 1000 * 1000 }
            'mib' { return $num * 1024 * 1024 }
            { $_ -in @('g', 'gb') } { return $num * 1000 * 1000 * 1000 }
            'gib' { return $num * 1024 * 1024 * 1024 }
        }
    }

    throw "Invalid size '$Value'. Examples: 2097152, 2MiB, 10MiB, 10MB."
}

function Get-RepoRoot {
    $scriptDir = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptDir "..")).Path
}

function Read-LastXadcCsvRow {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return $null
    }
    try {
        $rows = @(Import-Csv -Path $Path)
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

$targetBytes = Convert-SizeToBytes $Bytes
$repoRoot = Get-RepoRoot
$outPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutFile)
$outDir = Split-Path -Parent $outPath
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force $outDir | Out-Null
}

if ($Run -eq "") {
    $Run = [System.IO.Path]::GetFileNameWithoutExtension($outPath)
}

if ($MetadataDir -eq "") {
    $MetadataDir = Join-Path (Split-Path -Parent $outDir) "metadata"
}
$metadataPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath(
    (Join-Path $MetadataDir "$Run.json")
)
if (-not (Test-Path $MetadataDir)) {
    New-Item -ItemType Directory -Force $MetadataDir | Out-Null
}

if ($XadcCsv -eq "") {
    $XadcCsv = Join-Path $MetadataDir "xadc_readings.csv"
}
$xadcCsvPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($XadcCsv)
$xadcDir = Split-Path -Parent $xadcCsvPath
if (-not (Test-Path $xadcDir)) {
    New-Item -ItemType Directory -Force $xadcDir | Out-Null
}

$startTime = Get-Date
$xadcBefore = [ordered]@{
    phase = "before_capture"
    status = "skipped"
    csv = $xadcCsvPath
    timestamp = ""
    temperature_c = ""
    vccint_v = ""
    vccaux_v = ""
    vccbram_v = ""
    vpvn_v = ""
    error = ""
}
if ($XadcMode -eq "before_after") {
    $xadcBefore = Invoke-XadcSnapshot -Phase "before_capture" -CsvPath $xadcCsvPath
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

Write-Host "Serial config:"
Write-Host "  DTR:       $($serial.DtrEnable)"
Write-Host "  RTS:       $($serial.RtsEnable)"
Write-Host "  Handshake: $($serial.Handshake)"

$fs = $null
$captured = [int64]0
$lastByteTime = Get-Date

try {
    Write-Host "Opening $Port at $Baud baud, 8N1, no flow control..."
    $serial.Open()
    Start-Sleep -Milliseconds 200
    $serial.DiscardInBuffer()

    $fs = [System.IO.File]::Open($outPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
    $bufferSize = 8192
    $buffer = New-Object byte[] $bufferSize

    Write-Host "Capturing $targetBytes bytes to $outPath"
    while ($captured -lt $targetBytes) {
        $remaining = $targetBytes - $captured
        $want = [int][Math]::Min($buffer.Length, $remaining)
        try {
            $n = $serial.Read($buffer, 0, $want)
            if ($n -gt 0) {
                $fs.Write($buffer, 0, $n)
                $captured += $n
                $lastByteTime = Get-Date
                $percent = [Math]::Min(100, [Math]::Round(($captured * 100.0) / $targetBytes, 2))
                Write-Progress -Activity "UART capture $Run" -Status "$captured / $targetBytes bytes" -PercentComplete $percent
            }
        } catch [TimeoutException] {
            $idle = ((Get-Date) - $lastByteTime).TotalSeconds
            if ($idle -ge $IdleTimeoutSec) {
                throw "No UART bytes received for $IdleTimeoutSec seconds. Check bitstream, UART pin, COM port, baud rate, and reset."
            }
        }
    }
    Write-Progress -Activity "UART capture $Run" -Completed
} finally {
    if ($fs -ne $null) {
        $fs.Flush()
        $fs.Close()
    }
    if ($serial.IsOpen) {
        try {
            $serial.Close()
        } catch {
            Write-Warning "Serial close failed after capture loop: $($_.Exception.Message)"
        }
    }
}

$endTime = Get-Date
$xadcAfter = Invoke-XadcSnapshot -Phase "after_capture" -CsvPath $xadcCsvPath
$hash = Get-FileHash -Path $outPath -Algorithm SHA256
$hashPath = "$outPath.sha256.txt"
"$($hash.Hash)  $outPath" | Set-Content -Path $hashPath -Encoding ASCII
$durationSeconds = [Math]::Round(($endTime - $startTime).TotalSeconds, 3)
$throughputBytesPerSec = 0.0
if ($durationSeconds -gt 0) {
    $throughputBytesPerSec = [Math]::Round($captured / $durationSeconds, 3)
}

$bitAbs = ""
$bitSha256 = ""
if ($Bitstream -ne "") {
    try {
        $bitAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Bitstream)
        if (-not (Test-Path $bitAbs)) {
            $candidate = Join-Path $repoRoot $Bitstream
            if (Test-Path $candidate) {
                $bitAbs = (Resolve-Path $candidate).Path
            }
        }
        if (Test-Path $bitAbs) {
            $bitSha256 = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
        }
    } catch {
        $bitAbs = ""
        $bitSha256 = ""
    }
}

$metadata = [ordered]@{
    capture_id = $Run
    board_id = $BoardId
    kind = $Kind
    output_file = $outPath
    bitstream = $Bitstream
    bitstream_resolved = $bitAbs
    bitstream_sha256 = $bitSha256
    uart_port = $Port
    baud = $Baud
    uart_format = "8N1, no parity, no flow control"
    bytes_requested = $targetBytes
    bytes_captured = $captured
    sha256 = $hash.Hash
    start_time = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
    end_time = $endTime.ToString("yyyy-MM-dd HH:mm:ss")
    duration_seconds = $durationSeconds
    throughput_bytes_per_second = $throughputBytesPerSec
    room_temperature_c = ""
    fpga_temperature_c = $xadcAfter.temperature_c
    voltage_condition = "nominal_board_power"
    xadc_csv = $xadcCsvPath
    xadc_before = $xadcBefore
    xadc_after = $xadcAfter
    notes = ""
}
$metadata | ConvertTo-Json -Depth 5 | Set-Content -Path $metadataPath -Encoding UTF8

Write-Host "Capture complete."
Write-Host "  File:     $outPath"
Write-Host "  Bytes:    $captured"
Write-Host "  SHA256:   $($hash.Hash)"
Write-Host "  Metadata: $metadataPath"

if ($Analyze) {
    if ($Kind -eq "tdc") {
        $analysisDir = Join-Path $outDir "analysis_$Run"
        & $Python (Join-Path $repoRoot "scripts\analyze_tdc_uart.py") `
            $outPath `
            --format raw `
            --clock-period-ps $ClockPeriodPs `
            --bins $TdcBins `
            --run $Run `
            --out-dir $analysisDir
        if ($LASTEXITCODE -ne 0) {
            throw "TDC analysis failed with exit code $LASTEXITCODE"
        }
        Write-Host "  Analysis: $analysisDir"
    } elseif ($Kind -eq "trng") {
        $analysisDir = Join-Path $outDir "analysis_$Run"
        & $Python (Join-Path $repoRoot "scripts\analyze_trng_dataset.py") `
            $outPath `
            --out-dir $analysisDir
        if ($LASTEXITCODE -ne 0) {
            throw "TRNG analysis failed with exit code $LASTEXITCODE"
        }
        Write-Host "  Analysis: $analysisDir"
    } else {
        Write-Host "Analyze was requested, but Kind=$Kind. Skipping analysis."
    }
}
