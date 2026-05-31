param(
    [string]$Port = "COM3",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b02",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$OutRoot = "data\hardware\20260529_fpga1_board2\restart_reduced_xor_second_heldout_sampler_20260530",
    [string]$WarmupsCsv = "0,4,5,8,9,10,11,12,13,16",
    [string]$RunIdsCsv = "run01",
    [ValidateSet("All", "BuildOnly", "CaptureOnly", "SummaryOnly", "SanityRun04")]
    [string]$Phase = "All",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$context = "second_heldout_sample_ro_local"
$variant = "sample_ro_local"
$dateTag = "20260530"
$rawDir = Join-Path $OutRoot "raw"
$metadataDir = Join-Path $OutRoot "metadata"
$logDir = Join-Path $OutRoot "logs"
$summaryDir = Join-Path $OutRoot "summary"
$xadcCsv = Join-Path $OutRoot "xadc_readings.csv"
$pvtManifest = Join-Path $summaryDir "second_heldout_sample_ro_local_pvt_manifest_20260530.csv"
$captureManifest = Join-Path $summaryDir "second_heldout_sample_ro_local_capture_manifest_20260530.csv"

New-Item -ItemType Directory -Force $rawDir, $metadataDir, $logDir, $summaryDir | Out-Null

function Split-CsvInt {
    param([string]$Text)
    return @($Text.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" } | ForEach-Object { [int]$_ })
}

function Split-CsvText {
    param([string]$Text)
    return @($Text.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
}

function Test-PvtPhysicalValidity {
    param([object]$Row)
    try {
        $temp = [double]$Row.temperature_c
        $vccint = [double]$Row.vccint_v
        $vccaux = [double]$Row.vccaux_v
        $vccbram = [double]$Row.vccbram_v
    } catch {
        return "invalid_non_numeric"
    }
    if ([math]::Abs($temp + 273.1) -lt 0.01 -or [math]::Abs($temp + 273.15) -lt 0.01) {
        return "invalid_sentinel_temperature"
    }
    if ($temp -lt -40 -or $temp -gt 125) {
        return "invalid_temperature_range"
    }
    if ($vccint -lt 0.80 -or $vccint -gt 1.20 -or $vccaux -lt 1.50 -or $vccaux -gt 2.00 -or $vccbram -lt 0.80 -or $vccbram -gt 1.20) {
        return "invalid_voltage_range"
    }
    return "valid"
}

function New-Condition {
    param(
        [int]$Warmup,
        [string]$Kind,
        [string]$Mode,
        [int]$Index
    )

    $variantName = if ($Kind -eq "all640") { "all640" } else { "$Kind$Index" }
    $bitKind = if ($Kind -eq "all640") { "all640" } else { "$Kind$Index" }
    return [pscustomobject]@{
        warmup = $Warmup
        kind = $Kind
        mode = $Mode
        index = $Index
        variant = $variantName
        bitstream = "data\vivado_runs\restart_reduced_xor_random1_${variant}_formal_bits_1000x125_warmup${Warmup}_${bitKind}_header_delay60s\RO_TRNG_restart_reduced_xor_top.bit"
    }
}

function Get-AnchorConditions {
    param([int[]]$Warmups)
    $items = @()
    foreach ($warmup in $Warmups) {
        $items += New-Condition -Warmup $warmup -Kind "all640" -Mode "all64" -Index 0
        $items += New-Condition -Warmup $warmup -Kind "data_ro" -Mode "data_ro" -Index 0
        $items += New-Condition -Warmup $warmup -Kind "data_ro" -Mode "data_ro" -Index 4
    }
    return $items
}

function Ensure-Bitstream {
    param([pscustomobject]$Item)
    if (Test-Path $Item.bitstream) {
        Write-Host "BITSTREAM exists w$($Item.warmup) $($Item.variant)"
        return
    }

    Write-Host "BUILD warmup-aperture bitstream w$($Item.warmup) $($Item.variant)"
    powershell -ExecutionPolicy Bypass -File scripts\build_restart_reduced_xor_20260526.ps1 `
        -VivadoBat $VivadoBat `
        -VariantsCsv $variant `
        -WarmupsCsv "$($Item.warmup)" `
        -ModesCsv $Item.mode `
        -IndexesCsv "$($Item.index)" `
        -RestartCount 1000 `
        -RowBytes 125 `
        -DebugHeader 1
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed for w$($Item.warmup) $($Item.variant) with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path $Item.bitstream)) {
        throw "Build reported success but bitstream is missing: $($Item.bitstream)"
    }
}

function Read-LastXadcRow {
    $empty = [ordered]@{
        status = "missing"
        timestamp = ""
        temperature_c = ""
        vccint_v = ""
        vccaux_v = ""
        vccbram_v = ""
        vpvn_v = ""
        source_file = $xadcCsv
        physical_validity = "invalid_missing"
        error = "xadc csv not found"
    }
    if (-not (Test-Path $xadcCsv)) {
        return $empty
    }
    try {
        $rows = Import-Csv $xadcCsv
        if ($rows.Count -lt 1) {
            $empty["error"] = "xadc csv empty"
            return $empty
        }
        $row = $rows[-1]
        $out = [ordered]@{
            status = "ok"
            timestamp = $row.timestamp
            temperature_c = $row.TEMPERATURE
            vccint_v = $row.VCCINT
            vccaux_v = $row.VCCAUX
            vccbram_v = $row.VCCBRAM
            vpvn_v = if ($row.PSObject.Properties.Name -contains "VPVN") { $row.VPVN } else { "" }
            source_file = $xadcCsv
            physical_validity = ""
            error = ""
        }
        $out["physical_validity"] = Test-PvtPhysicalValidity -Row $out
        return $out
    } catch {
        $empty["status"] = "parse_failed"
        $empty["error"] = $_.Exception.Message
        return $empty
    }
}

function Read-XadcStamped {
    param(
        [string]$CaptureId,
        [string]$Moment
    )

    $status = "ok"
    $err = ""
    try {
        powershell -ExecutionPolicy Bypass -File scripts\read_xadc.ps1 `
            -OutCsv $xadcCsv `
            -HwServerUrl $HwServerUrl `
            -VivadoBat $VivadoBat | Out-Host
    } catch {
        $status = "failed"
        $err = $_.Exception.Message
        Write-Warning "XADC $Moment failed for ${CaptureId}: $err"
    }
    $row = Read-LastXadcRow
    if ($status -ne "ok") {
        $row["status"] = $status
        $row["error"] = $err
        $row["physical_validity"] = "invalid_read_failed"
    }

    [pscustomobject]@{
        capture_id = $CaptureId
        context = $context
        moment = $Moment
        xadc_status = $row.status
        xadc_timestamp = $row.timestamp
        temperature_c = $row.temperature_c
        vccint_v = $row.vccint_v
        vccaux_v = $row.vccaux_v
        vccbram_v = $row.vccbram_v
        vpvn_v = $row.vpvn_v
        physical_validity = $row.physical_validity
        source_file = $row.source_file
        error = $row.error
    } | Export-Csv -Path $pvtManifest -Append -NoTypeInformation -Encoding UTF8
    return $row
}

function Test-CompletedCapture {
    param([string]$OutFile, [string]$MetaFile)
    if (-not (Test-Path $OutFile) -or -not (Test-Path $MetaFile)) {
        return $false
    }
    try {
        $meta = Get-Content $MetaFile -Raw | ConvertFrom-Json
        return ([int64]$meta.output_bytes -eq 125008) -and ([string]$meta.first_16_bytes_hex).StartsWith("A55A03E8007D01D0")
    } catch {
        return $false
    }
}

function Update-CaptureMetadata {
    param(
        [string]$MetaFile,
        [object]$XadcBefore,
        [object]$XadcAfter,
        [pscustomobject]$Item,
        [string]$RunId
    )
    $meta = Get-Content $MetaFile -Raw | ConvertFrom-Json
    $meta | Add-Member -Force -NotePropertyName context -NotePropertyValue $context
    $meta | Add-Member -Force -NotePropertyName warmup -NotePropertyValue $Item.warmup
    $meta | Add-Member -Force -NotePropertyName kind -NotePropertyValue $Item.kind
    $meta | Add-Member -Force -NotePropertyName index -NotePropertyValue $(if ($Item.kind -eq "all640") { "all" } else { "$($Item.index)" })
    $meta | Add-Member -Force -NotePropertyName run_id -NotePropertyValue $RunId
    $meta | Add-Member -Force -NotePropertyName xadc_csv -NotePropertyValue $xadcCsv
    $meta | Add-Member -Force -NotePropertyName xadc_before -NotePropertyValue $XadcBefore
    $meta | Add-Member -Force -NotePropertyName xadc_after -NotePropertyValue $XadcAfter
    $meta | ConvertTo-Json -Depth 8 | Set-Content -Path $MetaFile -Encoding UTF8
}

function Add-CaptureManifestRow {
    param(
        [string]$RunName,
        [pscustomobject]$Item,
        [string]$RunId,
        [string]$Status,
        [string]$OutFile,
        [string]$MetaFile,
        [string]$ErrorMessage
    )
    [pscustomobject]@{
        run = $RunName
        run_id = $RunId
        context = $context
        warmup = $Item.warmup
        kind = $Item.kind
        index = $(if ($Item.kind -eq "all640") { "all" } else { "$($Item.index)" })
        status = $Status
        output_file = $OutFile
        metadata_file = $MetaFile
        bitstream = $Item.bitstream
        error = $ErrorMessage
    } | Export-Csv -Path $captureManifest -Append -NoTypeInformation -Encoding UTF8
}

function Capture-One {
    param([pscustomobject]$Item, [string]$RunId)
    Ensure-Bitstream -Item $Item

    $runName = "restart_reduced_xor_random1_${context}_warmup$($Item.warmup)_$($Item.variant)_${RunId}_1000x125_strict_${dateTag}"
    $outFile = Join-Path $rawDir "$runName.bin"
    $metaFile = Join-Path $metadataDir "$runName.json"
    $logFile = Join-Path $logDir "$runName.capture.log"

    if (-not $Force -and (Test-CompletedCapture -OutFile $outFile -MetaFile $metaFile)) {
        Write-Host "SKIP completed $runName"
        Add-CaptureManifestRow -RunName $runName -Item $Item -RunId $RunId -Status "skipped_completed" -OutFile $outFile -MetaFile $metaFile -ErrorMessage ""
        return $true
    }

    $lastError = ""
    foreach ($attempt in 1..2) {
        try {
            Write-Host "=== CAPTURE $runName attempt $attempt ==="
            $xadcBefore = Read-XadcStamped -CaptureId $runName -Moment "before"
            powershell -ExecutionPolicy Bypass -File scripts\program_and_capture_uart_sync_header.ps1 `
                -Bitstream $Item.bitstream `
                -Port $Port `
                -OutFile $outFile `
                -Run $runName `
                -Bytes 125008 `
                -HeaderHex A55A `
                -MetadataDir $metadataDir `
                -HwServerUrl $HwServerUrl `
                -BoardId $BoardId `
                -VivadoBat $VivadoBat `
                -IdleTimeoutSec 160 `
                *>&1 | Tee-Object -FilePath $logFile
            if ($LASTEXITCODE -ne 0) {
                throw "Capture subprocess failed with exit code $LASTEXITCODE"
            }
            $xadcAfter = Read-XadcStamped -CaptureId $runName -Moment "after"
            Update-CaptureMetadata -MetaFile $metaFile -XadcBefore $xadcBefore -XadcAfter $xadcAfter -Item $Item -RunId $RunId
            Add-CaptureManifestRow -RunName $runName -Item $Item -RunId $RunId -Status "ok" -OutFile $outFile -MetaFile $metaFile -ErrorMessage ""
            return $true
        } catch {
            $lastError = $_.Exception.Message
            Write-Warning "Capture failed for $runName attempt ${attempt}: $lastError"
            if ($attempt -lt 2) {
                Start-Sleep -Seconds 5
            }
        }
    }
    Add-CaptureManifestRow -RunName $runName -Item $Item -RunId $RunId -Status "missing_after_retry" -OutFile $outFile -MetaFile $metaFile -ErrorMessage $lastError
    return $false
}

function Invoke-Summary {
    python scripts\summarize_second_heldout_warmup_aperture_sweep_20260530.py `
        --run-dir $OutRoot `
        --warmups $WarmupsCsv `
        --run-ids $RunIdsCsv
    if ($LASTEXITCODE -ne 0) {
        throw "Warmup/aperture summarizer failed with exit code $LASTEXITCODE"
    }
}

$warmups = Split-CsvInt -Text $WarmupsCsv
$runIds = Split-CsvText -Text $RunIdsCsv
if ($Phase -eq "SanityRun04") {
    $warmups = @(10)
    $runIds = @("run04")
}
$items = Get-AnchorConditions -Warmups $warmups

if ($Phase -in @("All", "BuildOnly", "SanityRun04")) {
    foreach ($item in $items) {
        Ensure-Bitstream -Item $item
    }
}

if ($Phase -in @("All", "CaptureOnly", "SanityRun04")) {
    foreach ($runId in $runIds) {
        foreach ($item in $items) {
            [void](Capture-One -Item $item -RunId $runId)
        }
    }
}

if ($Phase -in @("All", "SummaryOnly", "SanityRun04")) {
    Invoke-Summary
}

Write-Host "Second held-out warmup/aperture queue complete. Summary output: data\experiments\second_heldout_warmup_aperture_sweep_20260530"
