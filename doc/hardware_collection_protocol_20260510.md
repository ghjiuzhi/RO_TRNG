# RO_TRNG Hardware Collection Protocol - 2026-05-10

This protocol is the hardware-side runbook for the Zynq-7020 Navigator V2
layout/TDC experiment. It only defines acquisition, naming, metadata, and
calibration records. Do not change RTL while following this document.

## Scope

- Board/project: `fpga1/xc7z020clg400`, part `xc7z020clg400-2`.
- Clock assumption: single-ended `sys_clk` through the fpga1 clock wizard.
- UART: board UART TX from FPGA pin `J15`, 115200 baud unless the bitstream
  manifest says otherwise.
- Primary outputs:
  - TDC code-density calibration captures.
  - TDC layout characterization captures.
  - RO_TRNG raw byte streams.
  - Per-capture metadata sidecar files.

## Bitstreams Under Test

Use already generated bitstreams first. Do not overwrite the manual baseline
bitstream in the Vivado project directory.

| ID | Purpose | Bitstream | Layout |
| --- | --- | --- | --- |
| `trng_baseline_manual` | Existing reproduced TRNG baseline | `fpga1/xc7z020clg400/xc7z020clg400.runs/impl_1/RO_TRNG_top.bit` | Current manual fpga1 placement |
| `trng_compact_x44y43_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_sweep/ro_compact_x44y43/seed_1/RO_TRNG_top.bit` | Compact |
| `trng_checker_p3_x44y43_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_sweep/ro_checker_pitch3_x44y43/seed_1/RO_TRNG_top.bit` | Checker, pitch 3 |
| `trng_same_col_p3_x44y35_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/same_column_pitch3_x44y35/seed_1/RO_TRNG_top.bit` | Same column, pitch 3 |
| `trng_row_p3_x38y43_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/row_pitch3_x38y43/seed_1/RO_TRNG_top.bit` | Same row, pitch 3 |
| `trng_sparse_p6_x36y35_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/sparse_pitch6_x36y35/seed_1/RO_TRNG_top.bit` | Sparse grid, pitch 6 |
| `trng_cross_region_x36y25_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/cross_region_x36y25/seed_1/RO_TRNG_top.bit` | Two vertical bands |
| `trng_far_x20y25_s01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/far_x20y25/seed_1/RO_TRNG_top.bit` | Far spread |
| `trng_random_x36y35_r01` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed1_x36y35/seed_1/RO_TRNG_top.bit` | Random placement seed 1 |
| `trng_random_x36y35_r02` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed2_x36y35/seed_1/RO_TRNG_top.bit` | Random placement seed 2 |
| `trng_random_x36y35_r03` | Layout sweep raw stream | `data/vivado_runs/fpga1_ro_trng_matrix/random_seed3_x36y35/seed_1/RO_TRNG_top.bit` | Random placement seed 3 |
| `tdc_sysclk_inmem` | TDC diagnostic and code-density capture | `data/vivado_runs/fpga1_tdc_sysclk_inmem/RO_TDC_sysclk_top.bit` | Current TDC diagnostic placement |
| `tdc_ro_near_x36y35` | TDC near-pair coupling diagnostic | `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_near_x36y35/RO_TDC_sysclk_top.bit` | Near RO pair |
| `tdc_ro_far_x24y25` | TDC far-pair coupling diagnostic | `data/vivado_runs/fpga1_tdc_matrix/tdc_ro_far_x24y25/RO_TDC_sysclk_top.bit` | Far RO pair |

A capture without an entry here is not paper-quality evidence. If a bitstream is
rebuilt, add a new row or update the SHA256 sidecar rather than silently
overwriting a prior capture record.

## Required Collection Matrix

Collect in this order so environmental drift is visible in the metadata.

| Phase | Bitstream ID | Capture type | Repeats | Minimum per repeat | Required record |
| --- | --- | --- | ---: | ---: | --- |
| P0 | `tdc_sysclk_inmem` | TDC code-density calibration, idle board | 3 | 200000 valid packets | `.bin`, `.tdc_packets.csv`, `.json` |
| P1 | `trng_baseline_manual` | RO_TRNG raw UART stream | 5 | 10 MiB raw bytes | `.bin`, `.json`, hash |
| P2 | `trng_compact_x44y43_s01` | RO_TRNG raw UART stream | 5 | 10 MiB raw bytes | `.bin`, `.json`, hash |
| P3 | `trng_checker_p3_x44y43_s01` | RO_TRNG raw UART stream | 5 | 10 MiB raw bytes | `.bin`, `.json`, hash |
| P4 | `tdc_sysclk_inmem` | TDC layout/health capture after TRNG runs | 3 | 200000 valid packets | `.bin`, `.tdc_packets.csv`, `.json` |

For each future layout, use the same rule:

- RO_TRNG raw stream: 5 repeats, at least 10 MiB per repeat.
- TDC capture: 3 repeats, at least 200000 valid packets per repeat.
- If temperature or voltage is intentionally swept, repeat the full layout set
  at every temperature/voltage point.

Recommended environmental setpoints:

| Setpoint ID | Temperature | Voltage | Use |
| --- | --- | --- | --- |
| `room_nom` | ambient lab, recorded in Celsius | nominal board supply | mandatory baseline |
| `warm_nom` | heated or enclosed board if available | nominal board supply | optional stress |
| `room_lowv` | ambient lab | lowest stable board/FPGA rail setting available | optional voltage sensitivity |
| `room_highv` | ambient lab | highest safe board/FPGA rail setting available | optional voltage sensitivity |

If the bench cannot control temperature or voltage, still record measured values
and mark the setpoint as `room_nom_uncontrolled`.

## File Naming

Store captures under:

```text
data/hardware/YYYYMMDD_<board_id>/
```

Use this filename pattern:

```text
YYYYMMDD_HHMMSS_<board_id>_<phase>_<mode>_<layout>_<seed>_<tempC>_<volt>_capNN.<ext>
```

Fields:

| Field | Example | Meaning |
| --- | --- | --- |
| `board_id` | `navv2_z7020_b01` | Physical board identifier on the lab label |
| `phase` | `P2` | Matrix phase above |
| `mode` | `trngraw`, `tdccal`, `tdcdiag` | Capture content |
| `layout` | `compact_x44y43`, `checker_p3_x44y43` | Placement/layout ID |
| `seed` | `s01`, `manual`, `na` | Vivado seed or manual/unknown |
| `tempC` | `25p4C` | Measured board or chamber temperature |
| `volt` | `nom`, `vccint0p99` | Voltage setting or measured key rail |
| `capNN` | `cap01` | Repeat number for the same condition |

Example:

```text
data/hardware/20260510_navv2_z7020_b01/20260510_153022_navv2_z7020_b01_P2_trngraw_compact_x44y43_s01_25p4C_nom_cap01.bin
data/hardware/20260510_navv2_z7020_b01/20260510_153022_navv2_z7020_b01_P2_trngraw_compact_x44y43_s01_25p4C_nom_cap01.json
```

## UART Capture Commands

Replace `COM7` and output paths with the actual machine values. Record the exact
command in the metadata sidecar.

Capture a fixed byte count for RO_TRNG raw streams:

```powershell
$portName = 'COM7'
$baud = 115200
$bytesToRead = 10MB
$out = 'data/hardware/20260510_navv2_z7020_b01/20260510_153022_navv2_z7020_b01_P2_trngraw_compact_x44y43_s01_25p4C_nom_cap01.bin'
$port = [System.IO.Ports.SerialPort]::new($portName, $baud, 'None', 8, 'One')
$port.ReadTimeout = 10000
$port.Open()
$fs = [System.IO.File]::Open($out, [System.IO.FileMode]::CreateNew)
$buf = New-Object byte[] 4096
$total = 0
try {
  while ($total -lt $bytesToRead) {
    $need = [Math]::Min($buf.Length, $bytesToRead - $total)
    $n = $port.Read($buf, 0, $need)
    if ($n -gt 0) {
      $fs.Write($buf, 0, $n)
      $total += $n
    }
  }
}
finally {
  $fs.Close()
  $port.Close()
}
Get-FileHash $out -Algorithm SHA256
```

Capture TDC packets by byte count. For 200000 packets, read at least
`200000 * 8 = 1600000` bytes:

```powershell
$portName = 'COM7'
$baud = 115200
$bytesToRead = 1600000
$out = 'data/hardware/20260510_navv2_z7020_b01/20260510_145200_navv2_z7020_b01_P0_tdccal_tdc_sysclk_na_25p2C_nom_cap01.bin'
$port = [System.IO.Ports.SerialPort]::new($portName, $baud, 'None', 8, 'One')
$port.ReadTimeout = 10000
$port.Open()
$fs = [System.IO.File]::Open($out, [System.IO.FileMode]::CreateNew)
$buf = New-Object byte[] 4096
$total = 0
try {
  while ($total -lt $bytesToRead) {
    $need = [Math]::Min($buf.Length, $bytesToRead - $total)
    $n = $port.Read($buf, 0, $need)
    if ($n -gt 0) {
      $fs.Write($buf, 0, $n)
      $total += $n
    }
  }
}
finally {
  $fs.Close()
  $port.Close()
}
Get-FileHash $out -Algorithm SHA256
python .\scripts\analyze_tdc_uart.py $out
```

Expected TDC frame format:

```text
0xA5 seq_lo seq_hi coarse_lo coarse_hi bin_a bin_b flags
```

After every TDC capture, check:

- `packets` reported by `scripts/analyze_tdc_uart.py` is at least 200000.
- Packet sync loss is not visually obvious from the decoded CSV length versus
  raw size. The approximate ratio should be `raw_bytes / 8`.
- Flag bits for `bubble`, `full`, and `empty` are recorded in the CSV and noted
  in the metadata summary if frequent.

## Metadata Sidecar Template

Create one JSON file per capture with the same base name as the `.bin`.

```json
{
  "project": "RO_TRNG",
  "capture_id": "20260510_153022_navv2_z7020_b01_P2_trngraw_compact_x44y43_s01_25p4C_nom_cap01",
  "operator": "",
  "date_local": "2026-05-10",
  "timezone": "Asia/Shanghai",
  "board": {
    "board_id": "navv2_z7020_b01",
    "board_model": "Zynq-7020 Navigator V2",
    "fpga_part": "xc7z020clg400-2",
    "serial_or_label": "",
    "power_source": ""
  },
  "bitstream": {
    "id": "trng_compact_x44y43_s01",
    "path": "data/vivado_runs/fpga1_ro_trng_sweep/ro_compact_x44y43/seed_1/RO_TRNG_top.bit",
    "sha256": "",
    "vivado_version": "2023.2",
    "seed": 1,
    "layout": "compact_x44y43",
    "xdc": "",
    "ro_num": "",
    "ro_stages": "",
    "sample_stages": ""
  },
  "uart": {
    "port": "COM7",
    "baud": 115200,
    "data_bits": 8,
    "parity": "None",
    "stop_bits": 1,
    "flow_control": "None",
    "capture_command": ""
  },
  "environment": {
    "setpoint_id": "room_nom",
    "ambient_temp_c": "",
    "board_temp_c": "",
    "chamber_temp_c": "",
    "vccint_v": "",
    "vccaux_v": "",
    "vccio_v": "",
    "supply_current_a": "",
    "measurement_instrument": "",
    "notes": ""
  },
  "data": {
    "mode": "trngraw",
    "raw_path": "",
    "raw_bytes": "",
    "raw_sha256": "",
    "repeat_index": 1,
    "target_repeats": 5
  },
  "tdc": {
    "is_tdc_capture": false,
    "packets_target": null,
    "packets_decoded": null,
    "code_density_csv": null,
    "bin_width_ps_csv": null,
    "valid_flag_summary": null
  },
  "analysis": {
    "quick_script": "python .\\scripts\\analyze_trng_dataset.py <dir> --glob <file> --out-dir <out>",
    "sp800_90b_command": "",
    "nist_sts_command": "",
    "result_paths": []
  }
}
```

## Temperature And Voltage Log

Keep a session-level CSV in the same directory as the captures:

```text
timestamp_local,board_id,phase,capture_id,setpoint_id,ambient_temp_c,board_temp_c,chamber_temp_c,vccint_v,vccaux_v,vccio_v,supply_current_a,instrument,notes
2026-05-10T15:30:22+08:00,navv2_z7020_b01,P2,20260510_153022_navv2_z7020_b01_P2_trngraw_compact_x44y43_s01_25p4C_nom_cap01,room_nom,25.4,,,,,,,,
```

Minimum logging rule:

- Record temperature and voltage before programming each bitstream.
- Record again immediately before each capture starts.
- Record again after each capture finishes if the capture lasts more than 5
  minutes.
- If only one thermometer is available, state whether it measures ambient air,
  heatsink/FPGA package, or chamber air.

## TDC Code-Density Calibration Record

For this experiment, code-density calibration means collecting a large TDC fine
code histogram under the most random available phase relationship and converting
the histogram into per-code bin widths. The current diagnostic UART exposes
`bin_a`, `bin_b`, `flags`, and coarse LSBs; keep both the raw packet stream and
decoded CSV.

Procedure:

1. Program `tdc_sysclk_inmem`.
2. Let the board sit powered for at least 2 minutes at the target environment.
3. Capture P0 `tdccal` repeat 1 to 3, each with at least 200000 decoded packets.
4. Decode each capture:

```powershell
python .\scripts\analyze_tdc_uart.py .\data\hardware\<session>\<capture>.bin --out .\data\hardware\<session>\<capture>.tdc_packets.csv
```

5. Build histograms for `bin_a`, `bin_b`, and `diff = bin_a - bin_b` from the
   decoded CSV.
6. For each lane, record:
   - total decoded packets,
   - count per fine code,
   - missing codes,
   - bubble/full/empty flag rates,
   - estimated bin width fraction `count[code] / total`,
   - estimated bin width in ps if the reference period is known.
7. Save calibration outputs next to the raw capture:

```text
<capture>.tdc_packets.csv
<capture>.tdc_histogram.csv
<capture>.tdc_bin_width.csv
<capture>.tdc_calibration_summary.md
```

Use this CSV schema for histograms:

```text
capture_id,lane,code,count,total,probability,bin_width_ps,missing_code
```

If the TDC input phase is not known to be uniformly distributed, mark the record
as `relative_code_density_only` in the summary. It can still compare stability
between layouts, but should not be used as an absolute delay calibration claim.

## RO_TRNG Raw Stream Record

For every RO_TRNG capture:

1. Program the target `RO_TRNG_top.bit`.
2. Reset the board once after programming.
3. Discard the first 1 to 2 seconds of UART output if using a GUI serial tool.
   If using the PowerShell command above, note whether discard was performed.
4. Capture at least 10 MiB raw bytes.
5. Save the raw `.bin` without text conversion, timestamps, or line endings.
6. Compute SHA256:

```powershell
Get-FileHash .\data\hardware\<session>\<capture>.bin -Algorithm SHA256
```

7. Run the quick repository analyzer:

```powershell
python .\scripts\analyze_trng_dataset.py .\data\hardware\<session> --glob <capture>.bin --out-dir .\data\hardware\<session>\analysis_<capture>
```

8. Record formal SP800-90B and NIST STS commands/results when they are run.

Raw streams must never be edited after capture. If a stream is truncated,
contains serial-tool headers, or has a wrong setting, keep it only under a
`rejected/` subdirectory with a metadata note and repeat the capture.

## Acceptance Checklist

Before a session is considered complete:

- Every `.bin` has a same-base-name `.json`.
- Every `.bin` has a SHA256 in its JSON sidecar.
- Every TDC `.bin` has a decoded `.tdc_packets.csv`.
- Every required matrix cell has the required repeat count.
- Temperature/voltage CSV has entries before and after captures as required.
- `capture_command` is filled for every capture, including COM port and baud.
- Any rejected capture is preserved separately and explained.
- No RTL file was modified as part of data acquisition.
