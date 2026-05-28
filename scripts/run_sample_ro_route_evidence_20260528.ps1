param(
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$OutDir = "data\experiments\sample_ro_route_diff_20260528",
    [string[]]$CaseEntry = @(),
    [string]$CaseList = "",
    [string[]]$Pairs = @(),
    [string]$PairsList = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

if (-not (Test-Path $VivadoBat)) {
    throw "Vivado not found: $VivadoBat"
}

$outAbs = Join-Path $repoRoot $OutDir
New-Item -ItemType Directory -Force $outAbs | Out-Null

$cases = [System.Collections.Generic.List[object]]::new()
$caseEntries = @()
if ($CaseList -ne "") {
    $caseEntries += ($CaseList -split "[;\r\n]+")
}
$caseEntries += $CaseEntry
if ($caseEntries.Count -gt 0) {
    foreach ($entry in $caseEntries) {
        if ($entry -eq "") { continue }
        if ($entry -notmatch "^([^=]+)=(.+)$") {
            throw "Invalid -Case entry '$entry'. Use label=path\to\routed.dcp"
        }
        $cases.Add([pscustomobject]@{
            Label = $Matches[1]
            Dcp = $Matches[2]
        }) | Out-Null
    }
} else {
    $cases.Add([pscustomobject]@{
        Label = "compact_w4_baseline"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_random1_regs_only_warmup4_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "compact_w5_baseline"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_random1_regs_only_warmup5_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "compact_w11_baseline"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_random1_regs_only_warmup11_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "forward_w4_formal_sample"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_random1_regs_only_sample_ro_formal_locked_warmup4_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "forward_w5_formal_sample"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "forward_w11_formal_sample"
        Dcp = "data\vivado_runs\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125\checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "formal_w4_baseline"
        Dcp = "data\vivado_runs\restart_auto_random1_regs_only_formal_bits_1000x125_warmup4_header_delay60s\checkpoints\RO_TRNG_restart_auto_top_routed.dcp"
    }) | Out-Null
    $cases.Add([pscustomobject]@{
        Label = "reverse_w4_compact_sample"
        Dcp = "data\vivado_runs\restart_auto_random1_regs_only_sample_ro_compact_locked_warmup4_1000x125_20260525\checkpoints\RO_TRNG_restart_auto_top_routed.dcp"
    }) | Out-Null
}

foreach ($caseItem in $cases) {
    $dcpRel = $caseItem.Dcp
    $label = $caseItem.Label
    $dcpAbs = Join-Path $repoRoot $dcpRel
    if (-not (Test-Path $dcpAbs)) {
        Write-Warning "Skipping missing DCP for ${label}: $dcpAbs"
        continue
    }
    $log = Join-Path $outAbs "$label.vivado.log"
    $errLog = Join-Path $outAbs "$label.vivado.err.log"
    Write-Host "=== extracting sample-RO routed evidence: $label ==="
    $args = @(
        "-mode", "batch",
        "-source", "scripts\vivado\extract_sample_ro_route_evidence_20260528.tcl",
        "-tclargs", $dcpAbs, $outAbs, $label
    )
    $proc = Start-Process -FilePath $VivadoBat `
        -ArgumentList $args `
        -WorkingDirectory $repoRoot `
        -RedirectStandardOutput $log `
        -RedirectStandardError $errLog `
        -WindowStyle Hidden `
        -Wait `
        -PassThru
    $expected = @(
        (Join-Path $outAbs "${label}_cells.csv"),
        (Join-Path $outAbs "${label}_nets.csv"),
        (Join-Path $outAbs "${label}_pips.csv"),
        (Join-Path $outAbs "${label}_net_delays.csv"),
        (Join-Path $outAbs "${label}_neighborhood_cells.csv"),
        (Join-Path $outAbs "${label}_summary.txt")
    )
    $missing = @($expected | Where-Object { -not (Test-Path $_) })
    $hasTclError = Select-String -LiteralPath $log -Pattern "can't |invalid command|while executing|ERROR:" -Quiet
    if ($missing.Count -gt 0 -or $hasTclError) {
        throw "Vivado extraction failed for $label with exit code $($proc.ExitCode). Missing: $($missing -join ', '). See $log and $errLog"
    }
    if ($proc.ExitCode -ne 0) {
        Write-Warning "Vivado returned exit code $($proc.ExitCode) for $label, but all expected extraction files were generated."
    }
}

$pairEntries = @()
if ($PairsList -ne "") {
    $pairEntries += ($PairsList -split "[;\r\n]+")
}
$pairEntries += $Pairs

$summaryArgs = @("scripts\summarize_sample_ro_route_evidence_20260528.py", "--out-dir", $outAbs)
if ($pairEntries.Count -gt 0) {
    $summaryArgs += "--pairs"
    $summaryArgs += $pairEntries
}
python @summaryArgs
if ($LASTEXITCODE -ne 0) {
    throw "Route evidence summarizer failed with exit code $LASTEXITCODE"
}

Write-Host "Wrote routed evidence to $outAbs"
