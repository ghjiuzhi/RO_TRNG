param(
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$Placement = "random3",
    [string]$RepeatTag = "repeat02",
    [string]$WarmupsCsv = "10,11,12",
    [double]$InitialEntropyMsb = 0.902345,
    [double]$InitialEntropyLsb = 0.828444,
    [int]$ColumnXCutoff = 605,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$MingwRoot = "D:\Toolsapp\MinGW",
    [string]$HwServerUrl = "localhost:3122",
    [switch]$RecordXadc,
    [string]$XadcCsv = "",
    [string]$BoardId = "z7020_b01"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
Set-Location $repoRoot

$restartDir = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1\restart"
$artifactRoot = Join-Path $repoRoot "data\experiments\paper_artifacts_20260515"
$logDir = Join-Path $repoRoot "data\experiments\restart_warmup_repeat_logs_20260515"
New-Item -ItemType Directory -Force -Path $restartDir, $artifactRoot, $logDir | Out-Null

$warmups = $WarmupsCsv.Split(",") | ForEach-Object { [int]$_.Trim() }
$summary = New-Object System.Collections.Generic.List[object]

foreach ($warmup in $warmups) {
    $run = "${Placement}_restart_auto_formal_bits_1000x125_warmup${warmup}_header_delay60s_${RepeatTag}_20260515"
    $bit = "data\vivado_runs\restart_auto_${Placement}_formal_bits_1000x125_warmup${warmup}_header_delay60s\RO_TRNG_restart_auto_top.bit"
    $packed = "data\hardware\20260511_fpga1_board1\restart\$run.bin"
    $meta = "data\hardware\20260511_fpga1_board1\restart\$run.metadata.json"
    $msb = "data\hardware\20260511_fpga1_board1\restart\${run}_bps1_msb.bin"
    $lsb = "data\hardware\20260511_fpga1_board1\restart\${run}_bps1_lsb.bin"
    $msbMeta = "data\hardware\20260511_fpga1_board1\restart\${run}_bps1_msb.metadata.json"
    $lsbMeta = "data\hardware\20260511_fpga1_board1\restart\${run}_bps1_lsb.metadata.json"
    $columnDir = "data\experiments\paper_artifacts_20260515\restart_column_bias_${Placement}_formal_bits_warmup${warmup}_${RepeatTag}"
    $eaMsbDir = "data\hardware\20260511_fpga1_board1\restart\ea_restart_${Placement}_warmup${warmup}_${RepeatTag}_msb_20260515"
    $eaLsbDir = "data\hardware\20260511_fpga1_board1\restart\ea_restart_${Placement}_warmup${warmup}_${RepeatTag}_lsb_20260515"
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

    Write-Host "=== warmup=$warmup run=$run ==="

    try {
        powershell @captureArgs

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
    } catch {
        $summary.Add([ordered]@{
            warmup = $warmup
            run = $run
            status = "capture_failed"
            error = $_.Exception.Message
            packed = $packed
        }) | Out-Null
        Write-Warning "Skipping post-processing for $run because capture failed: $($_.Exception.Message)"
        continue
    }

    python scripts\convert_restart_bytes_to_bits.py $packed --output $msb --restart-count 1000 --symbols-per-restart 125 --bit-order msb --metadata $msbMeta
    python scripts\convert_restart_bytes_to_bits.py $packed --output $lsb --restart-count 1000 --symbols-per-restart 125 --bit-order lsb --metadata $lsbMeta
    python scripts\analyze_restart_matrix_columns.py --input $packed --restart-count 1000 --bytes-per-restart 125 --x-cutoff $ColumnXCutoff --label "${Placement}_formal_bits_warmup${warmup}_${RepeatTag}" --out-dir $columnDir

    powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 -InputFile $msb -InitialEntropy $InitialEntropyMsb -BitsPerSymbol 1 -ResultDir $eaMsbDir -Run "${Placement}_warmup${warmup}_${RepeatTag}_msb_20260515" -MingwRoot $MingwRoot
    powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 -InputFile $lsb -InitialEntropy $InitialEntropyLsb -BitsPerSymbol 1 -ResultDir $eaLsbDir -Run "${Placement}_warmup${warmup}_${RepeatTag}_lsb_20260515" -MingwRoot $MingwRoot

    $packedHash = (Get-FileHash -Path $packed -Algorithm SHA256).Hash
    $summary.Add([ordered]@{
        warmup = $warmup
        run = $run
        status = "completed"
        packed = (Resolve-Path $packed).Path
        packed_sha256 = $packedHash
        column_summary = (Resolve-Path (Join-Path $columnDir "summary.json")).Path
        ea_msb_stdout = (Resolve-Path (Join-Path $eaMsbDir "${Placement}_warmup${warmup}_${RepeatTag}_msb_20260515.ea_restart.stdout.txt")).Path
        ea_lsb_stdout = (Resolve-Path (Join-Path $eaLsbDir "${Placement}_warmup${warmup}_${RepeatTag}_lsb_20260515.ea_restart.stdout.txt")).Path
    }) | Out-Null
}

$summaryPath = Join-Path $logDir "restart_warmup_${Placement}_${RepeatTag}_summary.json"
$summary | ConvertTo-Json -Depth 5 | Set-Content -Path $summaryPath -Encoding UTF8
Write-Host "Wrote $summaryPath"
