param(
    [string[]]$Variants = @("compact", "formal_sample"),
    [string]$VariantList = "",
    [int[]]$Warmups = @(4),
    [string]$WarmupList = "",
    [string]$DirectiveTag = "alt1",
    [string]$PlaceDirective = "Explore",
    [string]$PhysOptDirective = "Explore",
    [string]$RouteDirective = "Explore",
    [int]$RestartCount = 1000,
    [int]$RowBytes = 125,
    [int]$HoldCycles = 200000,
    [int]$SettleCycles = 200000,
    [UInt64]$StartDelayCycles = 12000000000,
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$BoardId = "z7020_b01",
    [switch]$RecordXadc,
    [switch]$BuildOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-BinaryMinEntropy {
    param([double]$P1)
    $pmax = [Math]::Max($P1, 1.0 - $P1)
    return -1.0 * ([Math]::Log($pmax) / [Math]::Log(2.0))
}

$repoRoot = (Resolve-Path (Join-Path (Split-Path -Parent $PSCommandPath) "..")).Path
Set-Location $repoRoot

$variantXdc = @{
    compact = "data\experiments\xdc_sampler_island\random1_sampler_regs_only_x45y31.xdc"
    formal_sample = "data\experiments\xdc_sampler_island\random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc"
}
$variantCase = @{
    compact = "compact_baseline"
    formal_sample = "forward_fail"
}

$variantText = if ($VariantList -ne "") { $VariantList } else { ($Variants -join ",") }
$parsedVariants = @()
foreach ($token in ($variantText -split "[,\s;]+")) {
    if ($token -eq "") { continue }
    if (-not $variantXdc.ContainsKey($token)) {
        throw "Invalid variant '$token'. Valid variants: $($variantXdc.Keys -join ', ')"
    }
    $parsedVariants += $token
}
if ($parsedVariants.Count -eq 0) {
    throw "No variants parsed"
}

$warmupText = if ($WarmupList -ne "") { $WarmupList } else { ($Warmups -join ",") }
$parsedWarmups = @()
foreach ($token in ($warmupText -split "[,\s;]+")) {
    if ($token -eq "") { continue }
    if ($token -notmatch "^\d+$") {
        throw "Invalid warmup token '$token'"
    }
    $parsedWarmups += [int]$token
}
if ($parsedWarmups.Count -eq 0) {
    throw "No warmups parsed"
}

$hardwareRoot = Join-Path $repoRoot "data\hardware\20260511_fpga1_board1"
$captureRoot = Join-Path $hardwareRoot "restart_fifo_diag"
$metadataDir = Join-Path $hardwareRoot "metadata"
$artifactRoot = Join-Path $repoRoot "data\experiments\sample_ro_directive_variance_20260528"
$logDir = Join-Path $artifactRoot "logs"
$summaryCsv = Join-Path $artifactRoot "sample_ro_directive_variance_20260528.csv"
$xadcCsv = Join-Path $metadataDir "xadc_readings.csv"
$headerBytes = 16
$captureBytes = $headerBytes + ($RestartCount * $RowBytes)

New-Item -ItemType Directory -Force $captureRoot, $metadataDir, $artifactRoot, $logDir | Out-Null

$rows = @()
if (Test-Path $summaryCsv) {
    $rows += Import-Csv $summaryCsv
}

foreach ($variant in $parsedVariants) {
    foreach ($warmup in $parsedWarmups) {
        $caseName = $variantCase[$variant]
        $label = "restart_fifo_compact_diag_${variant}_warmup${warmup}_${RestartCount}x${RowBytes}_${DirectiveTag}"
        $buildDir = Join-Path $repoRoot "data\vivado_runs\sample_ro_directive_variance_20260528\$label"
        $bitstream = Join-Path $buildDir "RO_TRNG_restart_fifo_compact_diag_top.bit"
        $run = "${label}_run01_20260528"
        $capture = Join-Path $captureRoot "$run.bin"
        $columnDir = Join-Path $artifactRoot "$run.column_analysis"

        Write-Host "=== directive variance build/capture ==="
        Write-Host "Variant:    $variant"
        Write-Host "Warmup:     $warmup"
        Write-Host "Directives: place=$PlaceDirective phys_opt=$PhysOptDirective route=$RouteDirective"
        Write-Host "Build dir:  $buildDir"
        Write-Host "Run:        $run"

        $buildArgs = @(
            "-mode", "batch",
            "-source", "scripts\vivado\run_fpga1_ro_trng_restart_auto_inmem.tcl",
            "-tclargs", $variantXdc[$variant], $buildDir, $RestartCount, $RowBytes,
            $HoldCycles, $SettleCycles, $warmup, $StartDelayCycles, 1,
            "RO_TRNG_restart_fifo_compact_diag_top", 0, 0,
            $PlaceDirective, $PhysOptDirective, $RouteDirective
        )
        $buildProc = Start-Process -FilePath $VivadoBat `
            -ArgumentList $buildArgs `
            -WorkingDirectory $repoRoot `
            -RedirectStandardOutput (Join-Path $logDir "$label.build.log") `
            -RedirectStandardError (Join-Path $logDir "$label.build.err.log") `
            -WindowStyle Hidden `
            -Wait `
            -PassThru
        if ($buildProc.ExitCode -ne 0 -or -not (Test-Path $bitstream)) {
            throw "Vivado build failed for $label with exit code $($buildProc.ExitCode)"
        }

        if ($BuildOnly) {
            $row = [pscustomobject]@{
                run = $run
                case = $caseName
                variant = $variant
                warmup = $warmup
                directive_tag = $DirectiveTag
                place_directive = $PlaceDirective
                phys_opt_directive = $PhysOptDirective
                route_directive = $RouteDirective
                build_dir = $buildDir
                bitstream = $bitstream
                bitstream_sha256 = (Get-FileHash -Path $bitstream -Algorithm SHA256).Hash
                routed_dcp = (Join-Path $buildDir "checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp")
                capture = ""
                capture_sha256 = ""
                overall_p1 = ""
                overall_min_entropy = ""
                row_ones_std = ""
                worst_byte_index = ""
                worst_bit_index = ""
                worst_x = ""
                worst_p1 = ""
                xadc_after_status = "build_only"
                xadc_after_temperature_c = ""
            }
            $rows += $row
            $rows | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
            $row | Format-List
            continue
        }

        $captureArgs = @(
            "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", "scripts\program_and_capture_uart.ps1",
            "-VivadoBat", $VivadoBat,
            "-Bitstream", $bitstream,
            "-Port", $Port,
            "-Baud", "$Baud",
            "-Kind", "restart",
            "-Run", $run,
            "-Bytes", "$captureBytes",
            "-OutFile", $capture,
            "-MetadataDir", $metadataDir,
            "-IdleTimeoutSec", "300",
            "-BoardId", $BoardId
        )
        if ($RecordXadc) {
            $captureArgs += @("-RecordXadc", "-XadcMode", "after_only", "-XadcCsv", $xadcCsv)
        }

        powershell @captureArgs *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.capture.log")
        if ($LASTEXITCODE -ne 0) {
            throw "Capture failed for $run"
        }

        python scripts\analyze_restart_fifo_compact_diag.py `
            --input $capture `
            --out-dir $artifactRoot `
            --label $run `
            *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.analysis.log")
        if ($LASTEXITCODE -ne 0) {
            throw "Compact analysis failed for $run"
        }

        $packed = Join-Path $artifactRoot "$run.send_packed.bin"
        python scripts\analyze_restart_matrix_columns.py `
            --input $packed `
            --restart-count $RestartCount `
            --bytes-per-restart $RowBytes `
            --label $run `
            --out-dir $columnDir `
            *>&1 | Tee-Object -FilePath (Join-Path $logDir "$run.columns.log")
        if ($LASTEXITCODE -ne 0) {
            throw "Column analysis failed for $run"
        }

        $summary = Import-Csv (Join-Path $artifactRoot "$run.summary.csv") | Select-Object -First 1
        $captureMetaPath = Join-Path $metadataDir "$run.json"
        $captureMeta = if (Test-Path $captureMetaPath) { Get-Content $captureMetaPath -Raw | ConvertFrom-Json } else { $null }
        $overallP1 = [double]::Parse($summary.overall_p1, [System.Globalization.CultureInfo]::InvariantCulture)

        $row = [pscustomobject]@{
            run = $run
            case = $caseName
            variant = $variant
            warmup = $warmup
            directive_tag = $DirectiveTag
            place_directive = $PlaceDirective
            phys_opt_directive = $PhysOptDirective
            route_directive = $RouteDirective
            build_dir = $buildDir
            bitstream = $bitstream
            bitstream_sha256 = (Get-FileHash -Path $bitstream -Algorithm SHA256).Hash
            routed_dcp = (Join-Path $buildDir "checkpoints\RO_TRNG_restart_fifo_compact_diag_top_routed.dcp")
            capture = $capture
            capture_sha256 = (Get-FileHash -Path $capture -Algorithm SHA256).Hash
            overall_p1 = $summary.overall_p1
            overall_min_entropy = "{0:F9}" -f (Get-BinaryMinEntropy -P1 $overallP1)
            row_ones_std = $summary.row_ones_std
            worst_byte_index = $summary.worst_byte_index
            worst_bit_index = $summary.worst_bit_index
            worst_x = $summary.worst_x
            worst_p1 = $summary.worst_p1
            xadc_after_status = if ($null -ne $captureMeta) { $captureMeta.xadc_after.status } else { "" }
            xadc_after_temperature_c = if ($null -ne $captureMeta) { $captureMeta.xadc_after.temperature_c } else { "" }
        }
        $rows += $row
        $rows | Export-Csv -Path $summaryCsv -NoTypeInformation -Encoding UTF8
        $row | Format-List
    }
}

Write-Host "Wrote $summaryCsv"
