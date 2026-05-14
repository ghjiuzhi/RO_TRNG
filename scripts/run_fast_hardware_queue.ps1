param(
    [string]$QueueCsv = "data\experiments\fast_mode\hardware_queue_20260513.csv",
    [string]$Port = "COM3",
    [int]$Baud = 115200,
    [string]$HwServerUrl = "localhost:3122",
    [string]$VivadoBat = "C:\Programs\Xilinx2023\Vivado\2023.2\bin\vivado.bat",
    [string]$Python = "python",
    [string]$StatusMarkdown = "doc\fast_mode_hardware_status_20260513.md",
    [string]$LogDir = "data\experiments\fast_mode\logs",
    [switch]$ContinueOnError
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SizeToBytes {
    param([string]$Value)
    $text = $Value.Trim()
    if ($text -match '^(?<num>\d+)(?<unit>\s*(B|K|KB|KiB|M|MB|MiB|G|GB|GiB)?)$') {
        [int64]$num = [int64]$Matches['num']
        $unit = $Matches['unit'].Trim().ToLowerInvariant()
        switch ($unit) {
            { $_ -in @('', 'b') } { return $num }
            { $_ -in @('k', 'kb') } { return $num * 1000 }
            'kib' { return $num * 1024 }
            { $_ -in @('m', 'mb') } { return $num * 1000 * 1000 }
            'mib' { return $num * 1024 * 1024 }
            { $_ -in @('g', 'gb') } { return $num * 1000 * 1000 * 1000 }
            'gib' { return $num * 1024 * 1024 * 1024 }
        }
    }
    throw "Invalid size '$Value'."
}

function Resolve-RepoPath {
    param([string]$PathText)
    if ([System.IO.Path]::IsPathRooted($PathText)) {
        return $PathText
    }
    return (Join-Path $script:RepoRoot $PathText)
}

function Test-CaptureComplete {
    param($Item)
    $targetBytes = Convert-SizeToBytes $Item.bytes
    $outPath = Resolve-RepoPath $Item.out_file
    $metadataPath = Resolve-RepoPath (Join-Path $Item.metadata_dir "$($Item.run).json")
    if (-not (Test-Path $outPath) -or -not (Test-Path $metadataPath)) {
        return $false
    }
    $file = Get-Item $outPath
    if ($file.Length -ne $targetBytes) {
        return $false
    }
    try {
        $meta = Get-Content $metadataPath -Raw | ConvertFrom-Json
        return ([int64]$meta.bytes_captured -eq $targetBytes)
    } catch {
        return $false
    }
}

function Write-Status {
    param([array]$Rows, [string]$Phase, [string]$Message)
    $path = Resolve-RepoPath $StatusMarkdown
    $dir = Split-Path -Parent $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force $dir | Out-Null
    }
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Fast Mode Hardware Status")
    $lines.Add("")
    $lines.Add("- updated: $now")
    $lines.Add("- phase: $Phase")
    $lines.Add("- message: $Message")
    $lines.Add("- port: $Port")
    $lines.Add("- baud: $Baud")
    $lines.Add("")
    $lines.Add("| priority | run | kind | bytes | status | output |")
    $lines.Add("| --- | --- | --- | ---: | --- | --- |")
    foreach ($row in $Rows) {
        if ([string]$row.enabled -ne "1") { continue }
        $status = if (Test-CaptureComplete $row) { "complete" } else { "pending" }
        $outPath = Resolve-RepoPath $row.out_file
        $size = ""
        if (Test-Path $outPath) {
            $size = (Get-Item $outPath).Length
        }
        if ($size -ne "") {
            $status = "$status ($size bytes)"
        }
        $outputFile = $row.out_file
        $lines.Add("| $($row.priority) | $($row.run) | $($row.kind) | $($row.bytes) | $status | ``$outputFile`` |")
    }
    Set-Content -Path $path -Value $lines -Encoding UTF8
}

function Run-Analysis {
    param([array]$Rows)
    $roGroups = $Rows | Where-Object { [string]$_.enabled -eq "1" -and $_.kind -eq "raw" -and $_.analyze_group -like "ro_freq*" } | Group-Object analyze_group
    foreach ($group in $roGroups) {
        $files = @()
        foreach ($row in $group.Group) {
            if (Test-CaptureComplete $row) {
                $files += (Resolve-RepoPath $row.out_file)
            }
        }
        if ($files.Count -eq 0) { continue }
        $outDir = Resolve-RepoPath (Join-Path "data\experiments\ro_freq_analysis" ("20260513_" + $group.Name))
        New-Item -ItemType Directory -Force $outDir | Out-Null
        & $Python (Resolve-RepoPath "scripts\analyze_ro_frequency_matrix.py") @files `
            --family-map "1=random1,3=random3" `
            --out-dir $outDir `
            --prefix $group.Name
        if ($LASTEXITCODE -ne 0) {
            throw "RO_FREQ analysis failed for group $($group.Name)"
        }
    }

    & $Python (Resolve-RepoPath "scripts\summarize_trng_repeats.py")
    if ($LASTEXITCODE -ne 0) {
        throw "TRNG repeat summary refresh failed"
    }

    & $Python (Resolve-RepoPath "scripts\analyze_fast_mode_results.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Fast-mode aggregate analysis failed"
    }
}

$scriptDir = Split-Path -Parent $PSCommandPath
$script:RepoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$queuePath = Resolve-RepoPath $QueueCsv
$logPath = Resolve-RepoPath $LogDir
New-Item -ItemType Directory -Force $logPath | Out-Null

$rows = Import-Csv $queuePath
Write-Status -Rows $rows -Phase "starting" -Message "Queue loaded."

foreach ($row in $rows) {
    if ([string]$row.enabled -ne "1") { continue }

    if (Test-CaptureComplete $row) {
        Write-Host "SKIP complete: $($row.run)"
        Write-Status -Rows $rows -Phase "skip" -Message "Already complete: $($row.run)"
        continue
    }

    $runLog = Join-Path $logPath "$($row.run).log"
    Write-Host "RUN $($row.priority): $($row.run)"
    Write-Status -Rows $rows -Phase "capturing" -Message "Running $($row.run)"

    $args = @(
        "-ExecutionPolicy", "Bypass",
        "-File", (Resolve-RepoPath "scripts\program_and_capture_uart.ps1"),
        "-Bitstream", $row.bitstream,
        "-Port", $Port,
        "-Baud", "$Baud",
        "-Kind", $row.kind,
        "-Run", $row.run,
        "-Bytes", $row.bytes,
        "-OutFile", $row.out_file,
        "-MetadataDir", $row.metadata_dir,
        "-HwServerUrl", $HwServerUrl,
        "-VivadoBat", $VivadoBat
    )
    if ($row.kind -eq "tdc" -or $row.kind -eq "trng") {
        $args += "-Analyze"
    }

    try {
        & powershell @args *>&1 | Tee-Object -FilePath $runLog
        if ($LASTEXITCODE -ne 0) {
            throw "Capture command exited with $LASTEXITCODE"
        }
        Write-Status -Rows $rows -Phase "captured" -Message "Completed $($row.run)"
    } catch {
        Write-Status -Rows $rows -Phase "error" -Message "Failed $($row.run): $($_.Exception.Message)"
        if (-not $ContinueOnError) {
            throw
        }
        Write-Warning "Continuing after failed run $($row.run): $($_.Exception.Message)"
    }
}

Write-Status -Rows $rows -Phase "analysis" -Message "Running post-capture analysis."
Run-Analysis -Rows $rows
Write-Status -Rows $rows -Phase "done" -Message "Queue finished and post-analysis completed."
