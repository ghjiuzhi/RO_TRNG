param(
    [string]$QueueCsv = "data\experiments\fast_mode\hardware_queue_restart_reduced_xor_smoke_20260526.csv",
    [string]$OutRoot = "data\experiments\restart_reduced_xor_strict_20260526",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 125,
    [switch]$RunEaRestart,
    [double]$InitialEntropyMsb = 1.0,
    [double]$InitialEntropyLsb = 1.0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

function Resolve-RepoPath {
    param([string]$Value)
    if ([System.IO.Path]::IsPathRooted($Value)) {
        return $Value
    }
    return (Join-Path $repoRoot $Value)
}

$queuePath = Resolve-RepoPath $QueueCsv
if (-not (Test-Path $queuePath)) {
    throw "Queue CSV not found: $QueueCsv"
}

$outRootAbs = Resolve-RepoPath $OutRoot
$payloadDir = Join-Path $outRootAbs "payloads"
$bitDir = Join-Path $outRootAbs "bit_symbols"
$profileDir = Join-Path $outRootAbs "profile"
$eaDir = Join-Path $outRootAbs "ea_restart"
New-Item -ItemType Directory -Force $payloadDir, $bitDir, $profileDir, $eaDir | Out-Null

$rows = @(Import-Csv -Path $queuePath | Where-Object { [string]$_.enabled -eq "1" })
if ($rows.Count -eq 0) {
    throw "No enabled queue rows: $QueueCsv"
}

$manifest = New-Object System.Collections.Generic.List[object]
$payloads = New-Object System.Collections.Generic.List[string]

foreach ($row in $rows) {
    $run = ([string]$row.run).Trim()
    $capture = Resolve-RepoPath ([string]$row.out_file).Trim()
    if (-not (Test-Path $capture)) {
        Write-Warning "Skip missing capture for ${run}: $capture"
        continue
    }

    $payload = Join-Path $payloadDir "$run.payload.bin"
    python scripts\extract_restart_payload_with_header.py `
        $capture `
        --output $payload `
        --restart-count $RestartCount `
        --row-bytes $RowBytes
    if ($LASTEXITCODE -ne 0) {
        throw "extract_restart_payload_with_header.py failed for $run"
    }
    $payloads.Add($payload) | Out-Null

    foreach ($order in @("msb", "lsb")) {
        $bits = Join-Path $bitDir "$run.$order.bits.bin"
        python scripts\convert_restart_bytes_to_bits.py `
            $payload `
            --output $bits `
            --restart-count $RestartCount `
            --symbols-per-restart $RowBytes `
            --bit-order $order
        if ($LASTEXITCODE -ne 0) {
            throw "convert_restart_bytes_to_bits.py failed for $run $order"
        }

        $eaStatus = "not_run"
        if ($RunEaRestart) {
            $initialEntropy = if ($order -eq "msb") { $InitialEntropyMsb } else { $InitialEntropyLsb }
            $runEa = "${run}_${order}"
            $resultDir = Join-Path $eaDir $runEa
            powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 `
                -InputFile $bits `
                -InitialEntropy $initialEntropy `
                -BitsPerSymbol 1 `
                -ResultDir $resultDir `
                -Run $runEa
            if ($LASTEXITCODE -ne 0) {
                throw "run_90b_restart.ps1 failed for $run $order"
            }
            $metaPath = Join-Path $resultDir "$runEa.ea_restart.metadata.json"
            if (Test-Path $metaPath) {
                $eaStatus = (Get-Content $metaPath -Raw | ConvertFrom-Json).ea_restart_status
            }
        }

        $manifest.Add([pscustomobject]@{
            run = $run
            order = $order
            capture = $capture
            capture_sha256 = (Get-FileHash -Path $capture -Algorithm SHA256).Hash
            payload = $payload
            payload_sha256 = (Get-FileHash -Path $payload -Algorithm SHA256).Hash
            bit_symbols = $bits
            bit_symbols_sha256 = (Get-FileHash -Path $bits -Algorithm SHA256).Hash
            ea_restart_status = $eaStatus
            notes = $row.notes
        }) | Out-Null
    }
}

if ($payloads.Count -gt 0) {
    $profileArgs = New-Object System.Collections.Generic.List[string]
    foreach ($payloadPath in $payloads) {
        $profileArgs.Add("--input") | Out-Null
        $profileArgs.Add($payloadPath) | Out-Null
    }
    $profileArgs.Add("--restart-count") | Out-Null
    $profileArgs.Add([string]$RestartCount) | Out-Null
    $profileArgs.Add("--row-bytes") | Out-Null
    $profileArgs.Add([string]$RowBytes) | Out-Null
    $profileArgs.Add("--out-dir") | Out-Null
    $profileArgs.Add($profileDir) | Out-Null
    $profileArgs.Add("--prefix") | Out-Null
    $profileArgs.Add("restart_reduced_xor_strict_20260526") | Out-Null

    python scripts\summarize_restart_formal_output_profile.py `
        @($profileArgs.ToArray())
    if ($LASTEXITCODE -ne 0) {
        throw "summarize_restart_formal_output_profile.py failed"
    }
}

$manifestPath = Join-Path $outRootAbs "restart_reduced_xor_manifest_20260526.csv"
$manifest | Export-Csv -Path $manifestPath -NoTypeInformation -Encoding UTF8
Write-Host "Wrote $manifestPath"
