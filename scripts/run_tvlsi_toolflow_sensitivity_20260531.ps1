param(
    [string]$Port = "COM3",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b02",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$OutRoot = "data\hardware\20260529_fpga1_board2\restart_toolflow_sensitivity_20260531",
    [ValidateSet("All", "BuildOnly", "CaptureOnly", "RouteOnly", "SummaryOnly", "ListOnly")]
    [string]$Phase = "All",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$dateTag = "20260531"
$warmup = 10
$rawDir = Join-Path $OutRoot "raw"
$metadataDir = Join-Path $OutRoot "metadata"
$logDir = Join-Path $OutRoot "logs"
$summaryDir = Join-Path $OutRoot "summary"
$routeOutDir = "data\experiments\toolflow_sensitivity_matrix_20260531\route_extract"
$summaryOutDir = "data\experiments\toolflow_sensitivity_matrix_20260531"
$xadcCsv = Join-Path $OutRoot "xadc_readings.csv"
$pvtManifest = Join-Path $summaryDir "toolflow_sensitivity_pvt_manifest_20260531.csv"
$captureManifest = Join-Path $summaryDir "toolflow_sensitivity_capture_manifest_20260531.csv"

New-Item -ItemType Directory -Force $rawDir, $metadataDir, $logDir, $summaryDir, $summaryOutDir | Out-Null

$contexts = @(
    [pscustomobject]@{
        context = "heldout_sample_x36y35_regs_x45y31"
        label = "heldout_x36y35"
        variant = "heldout_sample_x36y35_regs_x45y31"
    },
    [pscustomobject]@{
        context = "second_heldout_sample_ro_local"
        label = "sample_ro_local"
        variant = "sample_ro_local"
    }
)

$anchors = @(
    [pscustomobject]@{ anchor = "all640"; kind = "all640"; mode = "all64"; index = 0 },
    [pscustomobject]@{ anchor = "data_ro0"; kind = "data_ro"; mode = "data_ro"; index = 0 },
    [pscustomobject]@{ anchor = "data_ro4"; kind = "data_ro"; mode = "data_ro"; index = 4 }
)

$implementations = @(
    [pscustomobject]@{
        implementation = "original"
        directive_tag = ""
        place_directive = ""
        phys_opt_directive = ""
        route_directive = ""
    },
    [pscustomobject]@{
        implementation = "explore1"
        directive_tag = "explore1"
        place_directive = "Explore"
        phys_opt_directive = "Explore"
        route_directive = "Explore"
    }
)

function New-ConditionMatrix {
    $items = @()
    foreach ($context in $contexts) {
        foreach ($anchor in $anchors) {
            foreach ($impl in $implementations) {
                $suffix = if ($impl.directive_tag -ne "") { "_$($impl.directive_tag)" } else { "" }
                $modeSuffix = "$($anchor.mode)$($anchor.index)"
                $runDir = "data\vivado_runs\restart_reduced_xor_random1_$($context.variant)_formal_bits_1000x125_warmup${warmup}_${modeSuffix}${suffix}_header_delay60s"
                $bitstream = Join-Path $runDir "RO_TRNG_restart_reduced_xor_top.bit"
                $dcp = Join-Path $runDir "checkpoints\RO_TRNG_restart_reduced_xor_top_routed.dcp"
                if ($context.variant -eq "heldout_sample_x36y35_regs_x45y31" -and $anchor.anchor -eq "data_ro0" -and $impl.implementation -eq "original") {
                    $fallbackRunDir = "data\vivado_runs\restart_reduced_xor_random1_$($context.variant)_formal_bits_1000x125_warmup${warmup}_data_ro0_ipreuse_header_delay60s"
                    $fallbackBit = Join-Path $fallbackRunDir "RO_TRNG_restart_reduced_xor_top.bit"
                    if (Test-Path $fallbackBit) {
                        $runDir = $fallbackRunDir
                        $bitstream = $fallbackBit
                        $dcp = Join-Path $runDir "checkpoints\RO_TRNG_restart_reduced_xor_top_routed.dcp"
                    }
                }
                $items += [pscustomobject]@{
                    context = $context.context
                    context_label = $context.label
                    variant = $context.variant
                    anchor = $anchor.anchor
                    kind = $anchor.kind
                    mode = $anchor.mode
                    index = $anchor.index
                    implementation = $impl.implementation
                    directive_tag = $impl.directive_tag
                    place_directive = $impl.place_directive
                    phys_opt_directive = $impl.phys_opt_directive
                    route_directive = $impl.route_directive
                    run_dir = $runDir
                    bitstream = $bitstream
                    dcp = $dcp
                    route_label = "$($context.label)_$($anchor.anchor)_$($impl.implementation)"
                }
            }
        }
    }
    return $items
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
        [string]$Moment,
        [pscustomobject]$Item
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
        context = $Item.context
        anchor = $Item.anchor
        implementation = $Item.implementation
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

function Ensure-Bitstream {
    param([pscustomobject]$Item)
    if (Test-Path $Item.bitstream) {
        Write-Host "BITSTREAM exists $($Item.route_label): $($Item.bitstream)"
        return
    }

    Write-Host "BUILD toolflow sensitivity bitstream $($Item.route_label)"
    $buildArgs = @(
        "-ExecutionPolicy", "Bypass",
        "-File", "scripts\build_restart_reduced_xor_20260526.ps1",
        "-VivadoBat", $VivadoBat,
        "-VariantsCsv", $Item.variant,
        "-WarmupsCsv", "$warmup",
        "-ModesCsv", $Item.mode,
        "-IndexesCsv", "$($Item.index)",
        "-RestartCount", "1000",
        "-RowBytes", "125",
        "-DebugHeader", "1"
    )
    if ($Item.directive_tag -ne "") {
        $buildArgs += @("-DirectiveTag", $Item.directive_tag)
    }
    if ($Item.place_directive -ne "") {
        $buildArgs += @("-PlaceDirective", $Item.place_directive)
    }
    if ($Item.phys_opt_directive -ne "") {
        $buildArgs += @("-PhysOptDirective", $Item.phys_opt_directive)
    }
    if ($Item.route_directive -ne "") {
        $buildArgs += @("-RouteDirective", $Item.route_directive)
    }
    powershell @buildArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed for $($Item.route_label) with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path $Item.bitstream)) {
        throw "Build reported success but bitstream is missing: $($Item.bitstream)"
    }
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
    $meta | Add-Member -Force -NotePropertyName context -NotePropertyValue $Item.context
    $meta | Add-Member -Force -NotePropertyName context_label -NotePropertyValue $Item.context_label
    $meta | Add-Member -Force -NotePropertyName warmup -NotePropertyValue $warmup
    $meta | Add-Member -Force -NotePropertyName anchor -NotePropertyValue $Item.anchor
    $meta | Add-Member -Force -NotePropertyName kind -NotePropertyValue $Item.kind
    $meta | Add-Member -Force -NotePropertyName index -NotePropertyValue $(if ($Item.kind -eq "all640") { "all" } else { "$($Item.index)" })
    $meta | Add-Member -Force -NotePropertyName implementation -NotePropertyValue $Item.implementation
    $meta | Add-Member -Force -NotePropertyName directive_tag -NotePropertyValue $Item.directive_tag
    $meta | Add-Member -Force -NotePropertyName place_directive -NotePropertyValue $Item.place_directive
    $meta | Add-Member -Force -NotePropertyName phys_opt_directive -NotePropertyValue $Item.phys_opt_directive
    $meta | Add-Member -Force -NotePropertyName route_directive -NotePropertyValue $Item.route_directive
    $meta | Add-Member -Force -NotePropertyName route_label -NotePropertyValue $Item.route_label
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
        context = $Item.context
        context_label = $Item.context_label
        anchor = $Item.anchor
        implementation = $Item.implementation
        directive_tag = $Item.directive_tag
        status = $Status
        output_file = $OutFile
        metadata_file = $MetaFile
        bitstream = $Item.bitstream
        dcp = $Item.dcp
        error = $ErrorMessage
    } | Export-Csv -Path $captureManifest -Append -NoTypeInformation -Encoding UTF8
}

function Capture-One {
    param([pscustomobject]$Item, [string]$RunId)
    Ensure-Bitstream -Item $Item

    $runName = "restart_toolflow_random1_$($Item.context)_warmup${warmup}_$($Item.anchor)_$($Item.implementation)_${RunId}_1000x125_strict_${dateTag}"
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
            $xadcBefore = Read-XadcStamped -CaptureId $runName -Moment "before" -Item $Item
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
            $xadcAfter = Read-XadcStamped -CaptureId $runName -Moment "after" -Item $Item
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

function Invoke-RouteExtraction {
    param([object[]]$Items)

    $caseEntries = @()
    $missing = @()
    foreach ($item in $Items) {
        if (Test-Path $item.dcp) {
            $caseEntries += "$($item.route_label)=$($item.dcp)"
        } else {
            $missing += "$($item.route_label)=$($item.dcp)"
        }
    }
    if ($missing.Count -gt 0) {
        Write-Warning "Missing DCPs for route extraction: $($missing -join '; ')"
    }
    if ($caseEntries.Count -eq 0) {
        throw "No routed DCPs available for route extraction."
    }

    $pairEntries = @()
    foreach ($context in $contexts) {
        foreach ($anchor in $anchors) {
            $pairEntries += "$($context.label)_$($anchor.anchor)_original:$($context.label)_$($anchor.anchor)_explore1"
        }
    }

    powershell -ExecutionPolicy Bypass -File scripts\run_sample_ro_route_evidence_20260528.ps1 `
        -VivadoBat $VivadoBat `
        -OutDir $routeOutDir `
        -CaseList ($caseEntries -join ";") `
        -PairsList ($pairEntries -join ";")
    if ($LASTEXITCODE -ne 0) {
        throw "Route extraction failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Summary {
    python scripts\summarize_tvlsi_toolflow_sensitivity_20260531.py `
        --run-dir $OutRoot `
        --route-dir $routeOutDir `
        --out-dir $summaryOutDir
    if ($LASTEXITCODE -ne 0) {
        throw "Toolflow sensitivity summarizer failed with exit code $LASTEXITCODE"
    }
}

$items = New-ConditionMatrix

if ($Phase -eq "ListOnly") {
    $items | Select-Object context, anchor, implementation, bitstream, dcp | Format-Table -AutoSize
    return
}

if ($Phase -in @("All", "BuildOnly")) {
    foreach ($item in $items) {
        Ensure-Bitstream -Item $item
    }
}

if ($Phase -in @("All", "CaptureOnly")) {
    foreach ($item in $items) {
        [void](Capture-One -Item $item -RunId "run01")
    }
}

if ($Phase -in @("All", "RouteOnly")) {
    Invoke-RouteExtraction -Items $items
}

if ($Phase -in @("All", "SummaryOnly")) {
    Invoke-Summary
}

Write-Host "TVLSI toolflow sensitivity queue complete. Summary output: $summaryOutDir"
