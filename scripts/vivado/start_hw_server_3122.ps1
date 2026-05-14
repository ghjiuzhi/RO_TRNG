param(
    [int]$Port = 3122,
    [string]$VivadoRoot = "C:\Programs\Xilinx2023\Vivado\2023.2",
    [string]$LogFile = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$hwServer = Join-Path $VivadoRoot "bin\hw_server.bat"
if (-not (Test-Path $hwServer)) {
    throw "hw_server.bat not found: $hwServer"
}

if ($LogFile -eq "") {
    $repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..\..")).Path
    $logDir = Join-Path $repoRoot "data\hardware\hw_server_logs"
    New-Item -ItemType Directory -Force $logDir | Out-Null
    $LogFile = Join-Path $logDir ("hw_server_{0}.log" -f $Port)
}

$existing = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Port $Port is already listening:"
    $existing | Select-Object LocalAddress,LocalPort,State,OwningProcess | Format-Table -AutoSize
    return
}

$args = @("-s", "tcp::$Port", "-L", $LogFile)
Write-Host "Starting hw_server on tcp::$Port"
Write-Host "Log: $LogFile"
Start-Process -FilePath $hwServer -ArgumentList $args -WindowStyle Hidden

Start-Sleep -Seconds 2
$started = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if (-not $started) {
    throw "hw_server did not start on port $Port. Check log: $LogFile"
}

Write-Host "hw_server is listening on localhost:$Port"
