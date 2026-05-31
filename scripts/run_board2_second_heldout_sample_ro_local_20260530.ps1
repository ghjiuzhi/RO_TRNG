param(
    [string]$Port = "COM3",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b02",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$OutRoot = "data\hardware\20260529_fpga1_board2\restart_reduced_xor_second_heldout_sampler_20260530",
    [ValidateSet("All", "BuildOnly", "FullMapOnly", "AnchorRepeatsOnly")]
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
$warmup = 10
$dateTag = "20260530"
$rawDir = Join-Path $OutRoot "raw"
$metadataDir = Join-Path $OutRoot "metadata"
$logDir = Join-Path $OutRoot "logs"
$summaryDir = Join-Path $OutRoot "summary"
$xadcCsv = Join-Path $OutRoot "xadc_readings.csv"
$pvtManifest = Join-Path $summaryDir "second_heldout_sample_ro_local_pvt_manifest_20260530.csv"
$captureManifest = Join-Path $summaryDir "second_heldout_sample_ro_local_capture_manifest_20260530.csv"

New-Item -ItemType Directory -Force $rawDir, $metadataDir, $logDir, $summaryDir | Out-Null

function New-Condition {
    param(
        [string]$Kind,
        [string]$Mode,
        [int]$Index
    )

    $variantName = if ($Kind -eq "all640") { "all640" } else { "$Kind$Index" }
    $bitKind = if ($Kind -eq "all640") { "all640" } else { "$Kind$Index" }
    return [pscustomobject]@{
        kind = $Kind
        mode = $Mode
        index = $Index
        variant = $variantName
        bitstream = "data\vivado_runs\restart_reduced_xor_random1_${variant}_formal_bits_1000x125_warmup${warmup}_${bitKind}_header_delay60s\RO_TRNG_restart_reduced_xor_top.bit"
    }
}

function Get-FullMapConditions {
    $items = @()
    $items += New-Condition -Kind "all640" -Mode "all64" -Index 0
    foreach ($i in 0..7) {
        $items += New-Condition -Kind "data_ro" -Mode "data_ro" -Index $i
    }
    foreach ($i in 0..7) {
        $items += New-Condition -Kind "except_data_ro" -Mode "except_data_ro" -Index $i
    }
    return $items
}

function Ensure-Bitstream {
    param([pscustomobject]$Item)

    if (Test-Path $Item.bitstream) {
        Write-Host "BITSTREAM exists $($Item.variant)"
        return
    }

    Write-Host "BUILD second-heldout bitstream $($Item.variant)"
    powershell -ExecutionPolicy Bypass -File scripts\build_restart_reduced_xor_20260526.ps1 `
        -VivadoBat $VivadoBat `
        -VariantsCsv $variant `
        -WarmupsCsv "$warmup" `
        -ModesCsv $Item.mode `
        -IndexesCsv "$($Item.index)" `
        -RestartCount 1000 `
        -RowBytes 125 `
        -DebugHeader 1

    if ($LASTEXITCODE -ne 0) {
        throw "Build failed for $($Item.variant) with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path $Item.bitstream)) {
        throw "Build reported success but bitstream is missing: $($Item.bitstream)"
    }
}

function Read-LastXadcRow {
    $empty = [ordered]@{
        status = ""
        timestamp = ""
        temperature_c = ""
        vccint_v = ""
        vccaux_v = ""
        vccbram_v = ""
        vpvn_v = ""
        source_file = $xadcCsv
        error = ""
    }
    if (-not (Test-Path $xadcCsv)) {
        $empty["status"] = "missing"
        $empty["error"] = "xadc csv not found"
        return $empty
    }
    try {
        $rows = Import-Csv $xadcCsv
        if ($rows.Count -lt 1) {
            $empty["status"] = "missing"
            $empty["error"] = "xadc csv empty"
            return $empty
        }
        $row = $rows[-1]
        return [ordered]@{
            status = "ok"
            timestamp = $row.timestamp
            temperature_c = $row.TEMPERATURE
            vccint_v = $row.VCCINT
            vccaux_v = $row.VCCAUX
            vccbram_v = $row.VCCBRAM
            vpvn_v = $row.VPVN
            source_file = $xadcCsv
            error = ""
        }
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
    }

    $manifestExists = Test-Path $pvtManifest
    $line = [pscustomobject]@{
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
        source_file = $row.source_file
        error = $row.error
    }
    $line | Export-Csv -Path $pvtManifest -Append -NoTypeInformation -Encoding UTF8
    if (-not $manifestExists) {
        Write-Host "Created PVT manifest: $pvtManifest"
    }
    return $row
}

function Test-CompletedCapture {
    param(
        [string]$OutFile,
        [string]$MetaFile
    )

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
    $meta | Add-Member -Force -NotePropertyName warmup -NotePropertyValue $warmup
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
        warmup = $warmup
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
    param(
        [pscustomobject]$Item,
        [string]$RunId
    )

    Ensure-Bitstream -Item $Item

    $runName = "restart_reduced_xor_random1_${context}_warmup${warmup}_$($Item.variant)_${RunId}_1000x125_strict_${dateTag}"
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
    python scripts\make_board2_second_heldout_sample_ro_local_20260530.py
    if ($LASTEXITCODE -ne 0) {
        throw "Second held-out summary failed with exit code $LASTEXITCODE"
    }
}

function Get-AnchorConditions {
    $summary = Join-Path $summaryDir "board2_second_heldout_sample_ro_local_w10_reduced_xor_full_map.csv"
    if (-not (Test-Path $summary)) {
        Invoke-Summary
    }
    $rows = Import-Csv $summary
    $dataRows = @($rows | Where-Object { $_.kind -eq "data_ro" })
    if ($dataRows.Count -lt 1) {
        throw "Cannot select anchors; no data_ro rows in $summary"
    }
    $low = $dataRows | Sort-Object {[double]$_.p1} | Select-Object -First 1
    $high = $dataRows | Sort-Object {[double]$_.p1} -Descending | Select-Object -First 1
    $anchors = @()
    $anchors += New-Condition -Kind "all640" -Mode "all64" -Index 0
    $anchors += New-Condition -Kind "data_ro" -Mode "data_ro" -Index ([int]$low.index)
    if ($high.index -ne $low.index) {
        $anchors += New-Condition -Kind "data_ro" -Mode "data_ro" -Index ([int]$high.index)
    }
    Write-Host "Anchor repeat conditions: all640, strongest_low=data_ro$($low.index), strongest_high=data_ro$($high.index)"
    return $anchors
}

$fullMap = Get-FullMapConditions

if ($Phase -in @("All", "BuildOnly")) {
    foreach ($item in $fullMap) {
        Ensure-Bitstream -Item $item
    }
}

if ($Phase -in @("All", "FullMapOnly")) {
    foreach ($item in $fullMap) {
        [void](Capture-One -Item $item -RunId "run01")
    }
    Invoke-Summary
}

if ($Phase -in @("All", "AnchorRepeatsOnly")) {
    $anchors = Get-AnchorConditions
    foreach ($runId in @("run02", "run03")) {
        foreach ($item in $anchors) {
            [void](Capture-One -Item $item -RunId $runId)
        }
    }
    Invoke-Summary
}

Write-Host "Second held-out sample_ro_local queue complete. Summary root: $summaryDir"
