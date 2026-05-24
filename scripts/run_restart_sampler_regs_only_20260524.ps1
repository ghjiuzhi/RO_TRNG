param(
    [string]$QueueCsv = "data\experiments\fast_mode\restart_sampler_regs_only_queue_20260524.csv",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$MingwRoot = "D:\Toolsapp\MinGW",
    [string]$HwServerUrl = "localhost:3122",
    [string]$BoardId = "z7020_b01",
    [string]$HardwareRoot = "data\hardware\20260511_fpga1_board1",
    [string]$ArtifactRoot = "data\experiments\paper_artifacts_20260524",
    [string]$LogDir = "data\experiments\restart_sampler_regs_only_logs_20260524",
    [switch]$RecordXadc,
    [string]$XadcCsv = "data\hardware\20260511_fpga1_board1\metadata\xadc_readings.csv",
    [switch]$ContinueOnError
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Value)

    $candidate = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    $candidate = Join-Path $repoRoot $Value
    if (Test-Path $candidate) {
        return (Resolve-Path $candidate).Path
    }
    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Value)
}

function Require-FloatField {
    param(
        [object]$Row,
        [string]$Name
    )
    $text = [string]$Row.$Name
    if ($text.Trim() -eq "") {
        throw "Queue row '$($Row.placement) warmup=$($Row.warmup_bytes)' is missing required field $Name."
    }
    return [double]::Parse($text, [System.Globalization.CultureInfo]::InvariantCulture)
}

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$queuePath = Resolve-RepoPath $QueueCsv
if (-not (Test-Path $queuePath)) {
    throw "Queue CSV not found: $QueueCsv"
}

$hardwareRootAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($HardwareRoot)
$artifactRootAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ArtifactRoot)
$logDirAbs = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($LogDir)
$restartDir = Join-Path $hardwareRootAbs "restart"
New-Item -ItemType Directory -Force -Path $restartDir, $artifactRootAbs, $logDirAbs | Out-Null

$rows = Import-Csv -Path $queuePath | Where-Object { [string]$_.enabled -eq "1" }
if (@($rows).Count -eq 0) {
    throw "Queue has no enabled rows: $QueueCsv"
}

$summary = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
    $placement = ([string]$row.placement).Trim()
    $warmup = [int]$row.warmup_bytes
    $repeatTag = ([string]$row.repeat_tag).Trim()
    $bit = ([string]$row.bitstream).Trim()
    $initialEntropyMsb = Require-FloatField -Row $row -Name "initial_entropy_msb"
    $initialEntropyLsb = Require-FloatField -Row $row -Name "initial_entropy_lsb"
    $columnXCutoffText = ([string]$row.column_x_cutoff).Trim()
    $columnXCutoff = if ($columnXCutoffText -eq "") { 0 } else { [int]$columnXCutoffText }

    $bitAbs = Resolve-RepoPath $bit
    if (-not (Test-Path $bitAbs)) {
        throw "Bitstream not found for placement=$placement warmup=$warmup`: $bit"
    }

    $run = "${placement}_restart_auto_formal_bits_1000x125_warmup${warmup}_header_delay60s_${repeatTag}_20260524"
    $packed = Join-Path $restartDir "$run.bin"
    $meta = Join-Path $restartDir "$run.metadata.json"
    $msb = Join-Path $restartDir "${run}_bps1_msb.bin"
    $lsb = Join-Path $restartDir "${run}_bps1_lsb.bin"
    $msbMeta = Join-Path $restartDir "${run}_bps1_msb.metadata.json"
    $lsbMeta = Join-Path $restartDir "${run}_bps1_lsb.metadata.json"
    $columnDir = Join-Path $artifactRootAbs "restart_column_bias_${placement}_formal_bits_warmup${warmup}_${repeatTag}"
    $eaMsbRun = "${placement}_warmup${warmup}_${repeatTag}_msb_20260524"
    $eaLsbRun = "${placement}_warmup${warmup}_${repeatTag}_lsb_20260524"
    $eaMsbDir = Join-Path $restartDir "ea_restart_${placement}_warmup${warmup}_${repeatTag}_msb_20260524"
    $eaLsbDir = Join-Path $restartDir "ea_restart_${placement}_warmup${warmup}_${repeatTag}_lsb_20260524"

    Write-Host "=== placement=$placement warmup=$warmup repeat=$repeatTag ==="
    $status = "completed"
    $errorMessage = ""
    try {
        $captureArgs = @(
            "-ExecutionPolicy", "Bypass",
            "-File", "scripts\capture_90b_restart_dataset.ps1",
            "-Bitstream", $bit,
            "-OutFile", $packed,
            "-Port", $Port,
            "-Baud", "$Baud",
            "-RestartCount", "1000",
            "-SymbolsPerRestart", "125",
            "-BitsPerSymbol", "8",
            "-WarmupSymbols", "0",
            "-HeaderBytes", "8",
            "-SettleMs", "500",
            "-ReadTimeoutMs", "1000",
            "-ReadBufferBytes", "190544",
            "-IdleTimeoutSec", "90",
            "-RestartMethod", "auto_stream_once",
            "-Run", $run,
            "-MetadataFile", $meta,
            "-HwServerUrl", $HwServerUrl,
            "-VivadoBat", $VivadoBat,
            "-BoardId", $BoardId
        )
        if ($RecordXadc) {
            $captureArgs += "-RecordXadc"
            if ($XadcCsv -ne "") {
                $captureArgs += @("-XadcCsv", $XadcCsv)
            }
        }

        powershell @captureArgs *>&1 | Tee-Object -FilePath (Join-Path $logDirAbs "$run.capture.log")
        if ($LASTEXITCODE -ne 0) {
            throw "capture_90b_restart_dataset.ps1 failed with exit code $LASTEXITCODE"
        }
        if (-not (Test-Path $packed)) {
            throw "Packed restart capture was not created: $packed"
        }
        $packedItem = Get-Item -LiteralPath $packed
        if ($packedItem.Length -ne 125000) {
            throw "Packed restart capture has unexpected size $($packedItem.Length), expected 125000 bytes: $packed"
        }

        python scripts\convert_restart_bytes_to_bits.py $packed --output $msb --restart-count 1000 --symbols-per-restart 125 --bit-order msb --metadata $msbMeta
        if ($LASTEXITCODE -ne 0) { throw "MSB bit-symbol conversion failed for $run" }
        python scripts\convert_restart_bytes_to_bits.py $packed --output $lsb --restart-count 1000 --symbols-per-restart 125 --bit-order lsb --metadata $lsbMeta
        if ($LASTEXITCODE -ne 0) { throw "LSB bit-symbol conversion failed for $run" }
        python scripts\analyze_restart_matrix_columns.py --input $packed --restart-count 1000 --bytes-per-restart 125 --x-cutoff $columnXCutoff --label "${placement}_formal_bits_warmup${warmup}_${repeatTag}" --out-dir $columnDir
        if ($LASTEXITCODE -ne 0) { throw "Column-bias analysis failed for $run" }

        powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 -InputFile $msb -InitialEntropy $initialEntropyMsb -BitsPerSymbol 1 -ResultDir $eaMsbDir -Run $eaMsbRun -MingwRoot $MingwRoot
        if ($LASTEXITCODE -ne 0) { throw "ea_restart MSB runner failed for $run" }
        powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 -InputFile $lsb -InitialEntropy $initialEntropyLsb -BitsPerSymbol 1 -ResultDir $eaLsbDir -Run $eaLsbRun -MingwRoot $MingwRoot
        if ($LASTEXITCODE -ne 0) { throw "ea_restart LSB runner failed for $run" }
    } catch {
        $status = "failed"
        $errorMessage = $_.Exception.Message
        Write-Warning "Restart sampler regs-only row failed: $errorMessage"
        if (-not $ContinueOnError) {
            throw
        }
    }

    $packedSha = ""
    if (Test-Path $packed) {
        $packedSha = (Get-FileHash -Path $packed -Algorithm SHA256).Hash
    }
    $summary.Add([ordered]@{
        placement = $placement
        warmup_bytes = $warmup
        repeat_tag = $repeatTag
        status = $status
        error = $errorMessage
        run = $run
        packed = $packed
        packed_sha256 = $packedSha
        bitstream = $bit
        bitstream_sha256 = (Get-FileHash -Path $bitAbs -Algorithm SHA256).Hash
        initial_entropy_msb = $initialEntropyMsb
        initial_entropy_lsb = $initialEntropyLsb
        column_dir = $columnDir
        ea_msb_dir = $eaMsbDir
        ea_lsb_dir = $eaLsbDir
    }) | Out-Null
}

$summaryPath = Join-Path $logDirAbs "restart_sampler_regs_only_queue_summary_20260524.json"
$summary | ConvertTo-Json -Depth 6 | Set-Content -Path $summaryPath -Encoding UTF8
Write-Host "Wrote $summaryPath"
