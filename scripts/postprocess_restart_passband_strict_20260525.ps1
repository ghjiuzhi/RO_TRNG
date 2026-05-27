param(
    [string]$SummaryCsv = "data\experiments\restart_sampler_island_passband_strict_20260525\restart_preopen_queue_summary_20260525.csv",
    [string]$OutRoot = "data\experiments\restart_sampler_island_passband_strict_20260525",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 125,
    [double]$InitialEntropyMsb = 0.902345,
    [double]$InitialEntropyLsb = 0.828444,
    [string]$MingwRoot = "D:\Toolsapp\MinGW",
    [switch]$SkipEaRestart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

function Resolve-RepoPath {
    param([string]$Value)
    if ([System.IO.Path]::IsPathRooted($Value)) {
        return $Value
    }
    return (Join-Path $repoRoot $Value)
}

$summaryPath = Resolve-RepoPath $SummaryCsv
if (-not (Test-Path $summaryPath)) {
    throw "Summary CSV not found: $SummaryCsv"
}

$outRootAbs = Resolve-RepoPath $OutRoot
$payloadDir = Join-Path $outRootAbs "payloads"
$bitsDir = Join-Path $outRootAbs "bit_symbols"
$profileDir = Join-Path $outRootAbs "profile"
$restartDir = Join-Path $outRootAbs "ea_restart"
New-Item -ItemType Directory -Force $payloadDir, $bitsDir, $profileDir, $restartDir | Out-Null

$payloads = New-Object System.Collections.Generic.List[string]
$manifest = New-Object System.Collections.Generic.List[object]
$rows = @(Import-Csv -Path $summaryPath | Where-Object { $_.status -eq "completed" })
if ($rows.Count -eq 0) {
    throw "No completed rows in $SummaryCsv"
}

foreach ($row in $rows) {
    $capture = Resolve-RepoPath ([string]$row.capture)
    if (-not (Test-Path $capture)) {
        throw "Capture not found: $capture"
    }
    $label = [System.IO.Path]::GetFileNameWithoutExtension($capture)
    $variantShort = if ($label -like "*sampler_island_local*") { "island" } elseif ($label -like "*sample_ro_local*") { "sro" } else { "unk" }
    $warmupShort = if ($label -match "warmup(\d+)") { "w$($Matches[1])" } else { "wNA" }
    $payload = Join-Path $payloadDir "$label.payload.bin"
    python scripts\extract_restart_payload_with_header.py `
        $capture `
        --output $payload `
        --restart-count $RestartCount `
        --row-bytes $RowBytes | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "extract_restart_payload_with_header.py failed for $label"
    }
    $payloads.Add($payload) | Out-Null

    foreach ($order in @("msb", "lsb")) {
        $bits = Join-Path $bitsDir "$label.$order.bits.bin"
        python scripts\convert_restart_bytes_to_bits.py `
            $payload `
            --output $bits `
            --restart-count $RestartCount `
            --symbols-per-restart $RowBytes `
            --bit-order $order | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "convert_restart_bytes_to_bits.py failed for $label $order"
        }

        if (-not $SkipEaRestart) {
            $h = if ($order -eq "msb") { $InitialEntropyMsb } else { $InitialEntropyLsb }
            $run = "$variantShort`_$warmupShort`_$order"
            $runDir = Join-Path $restartDir $run
            powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 `
                -InputFile $bits `
                -InitialEntropy $h `
                -BitsPerSymbol 1 `
                -ResultDir $runDir `
                -Run $run `
                -MingwRoot $MingwRoot | Out-Host
            if ($LASTEXITCODE -ne 0) {
                throw "run_90b_restart.ps1 failed for $run"
            }
            $manifest.Add([pscustomobject]@{
                label = $label
                variant_short = $variantShort
                warmup_short = $warmupShort
                bit_order = $order
                ea_run = $run
                ea_result_dir = $runDir
                bit_symbols = $bits
                initial_entropy = $h
            }) | Out-Null
        }
    }
}

$manifestCsv = Join-Path $outRootAbs "ea_restart_manifest_20260525.csv"
$manifest | Export-Csv -Path $manifestCsv -NoTypeInformation -Encoding UTF8

python scripts\summarize_restart_formal_output_profile.py `
    @($payloads.ToArray()) `
    --restart-count $RestartCount `
    --row-bytes $RowBytes `
    --out-dir $profileDir `
    --prefix restart_sampler_island_passband_strict_20260525 | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "summarize_restart_formal_output_profile.py failed"
}

Write-Host "Postprocess complete:"
Write-Host "  payloads: $payloadDir"
Write-Host "  bit symbols: $bitsDir"
Write-Host "  profile: $profileDir"
Write-Host "  ea_restart: $restartDir"
Write-Host "  manifest: $manifestCsv"
