param(
    [string]$Port = "COM3",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b02",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$OutRoot = "data\hardware\20260529_fpga1_board2\restart_reduced_xor_crossboard",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$rawDir = Join-Path $OutRoot "raw"
$metadataDir = Join-Path $OutRoot "metadata"
$logDir = Join-Path $OutRoot "logs"
New-Item -ItemType Directory -Force $rawDir, $metadataDir, $logDir | Out-Null

$items = @()
foreach ($warmup in @(5, 11)) {
    foreach ($kind in @("all640", "data_ro0", "except_data_ro0", "data_ro3", "except_data_ro3")) {
        $items += [pscustomobject]@{
            warmup = $warmup
            kind = $kind
            run = "restart_reduced_xor_w${warmup}_${kind}_board2_sync"
            bitstream = "data\vivado_runs\restart_reduced_xor_random1_sampler_island_local_formal_bits_1000x125_warmup${warmup}_${kind}_header_delay60s\RO_TRNG_restart_reduced_xor_top.bit"
        }
    }
}

foreach ($item in $items) {
    $outFile = Join-Path $rawDir "$($item.run).bin"
    $metaFile = Join-Path $metadataDir "$($item.run).json"
    if (-not $Force -and (Test-Path $outFile) -and (Test-Path $metaFile)) {
        try {
            $meta = Get-Content $metaFile -Raw | ConvertFrom-Json
            if ([int64]$meta.output_bytes -eq 125008 -and ([string]$meta.first_16_bytes_hex).StartsWith("A55A03E8007D01D0")) {
                Write-Host "SKIP completed $($item.run)"
                continue
            }
        } catch {
            Write-Warning "Existing metadata is not parseable; recapturing $($item.run)"
        }
    }

    if (-not (Test-Path $item.bitstream)) {
        throw "Missing bitstream for $($item.run): $($item.bitstream)"
    }

    Write-Host "=== CAPTURE $($item.run) ==="
    powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart_sync_header.ps1 `
        -Bitstream $item.bitstream `
        -Port $Port `
        -OutFile $outFile `
        -Run $item.run `
        -Bytes 125008 `
        -HeaderHex A55A `
        -MetadataDir $metadataDir `
        -HwServerUrl $HwServerUrl `
        -BoardId $BoardId `
        -VivadoBat $VivadoBat `
        -IdleTimeoutSec 140 `
        *>&1 | Tee-Object -FilePath (Join-Path $logDir "$($item.run).capture.log")
    if ($LASTEXITCODE -ne 0) {
        throw "Capture failed: $($item.run)"
    }
}

Write-Host "Board2 reduced-XOR warmup-neighbor queue complete."
