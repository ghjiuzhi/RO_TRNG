param(
    [string[]]$Ports = @("COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9"),
    [int]$Baud = 115200,
    [int]$Seconds = 5
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$expandedPorts = @()
foreach ($entry in $Ports) {
    $expandedPorts += ($entry -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
}
$expandedPorts = $expandedPorts | Select-Object -Unique

foreach ($portName in $expandedPorts) {
    $serial = $null
    $bytes = 0
    $first = New-Object System.Collections.Generic.List[byte]
    try {
        $serial = [System.IO.Ports.SerialPort]::new(
            $portName,
            $Baud,
            [System.IO.Ports.Parity]::None,
            8,
            [System.IO.Ports.StopBits]::One
        )
        $serial.Handshake = [System.IO.Ports.Handshake]::None
        $serial.ReadTimeout = 200
        $serial.WriteTimeout = 200
        $serial.Open()
        Start-Sleep -Milliseconds 100
        $serial.DiscardInBuffer()

        $deadline = (Get-Date).AddSeconds($Seconds)
        $buffer = New-Object byte[] 4096
        while ((Get-Date) -lt $deadline) {
            try {
                $n = $serial.Read($buffer, 0, $buffer.Length)
                if ($n -gt 0) {
                    $bytes += $n
                    for ($i = 0; $i -lt $n -and $first.Count -lt 16; $i++) {
                        $first.Add($buffer[$i])
                    }
                }
            } catch [TimeoutException] {
            }
        }
        $hex = ($first | ForEach-Object { "{0:X2}" -f $_ }) -join " "
        [pscustomobject]@{
            Port = $portName
            Opened = $true
            BytesInSeconds = $bytes
            FirstBytesHex = $hex
            Error = ""
        }
    } catch {
        [pscustomobject]@{
            Port = $portName
            Opened = $false
            BytesInSeconds = 0
            FirstBytesHex = ""
            Error = $_.Exception.Message
        }
    } finally {
        if ($serial -ne $null -and $serial.IsOpen) {
            $serial.Close()
        }
    }
}
