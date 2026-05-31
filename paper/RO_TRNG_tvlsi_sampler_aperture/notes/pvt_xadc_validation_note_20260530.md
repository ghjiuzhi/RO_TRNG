# PVT/XADC Validation Note 2026-05-30

## Scope

This note is bounded to PVT/XADC diagnosis for the second held-out
`sample_ro_local` hardware run. It does not change the TIM manuscript, capture
payloads, bitstreams, or hardware scripts.

## Inputs Inspected

- PVT manifest:
  `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/second_heldout_sample_ro_local_pvt_manifest_20260530.csv`
- Capture manifest:
  `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/summary/second_heldout_sample_ro_local_capture_manifest_20260530.csv`
- XADC source CSVs:
  `data/hardware/20260529_fpga1_board2/restart_reduced_xor_second_heldout_sampler_20260530/xadc_readings.csv`
  and `data/hardware/20260529_fpga1_board2/xadc_readings.csv`
- Capture-side XADC readers:
  `scripts/read_xadc.ps1`,
  `scripts/vivado/read_xadc.tcl`, and
  `scripts/run_board2_second_heldout_sample_ro_local_20260530.ps1`
- Historical valid Board1 comparison:
  `data/hardware/20260511_fpga1_board1/xadc_readings.csv`
- Offline physical-validity summaries:
  `data/experiments/xadc_summary/pvt_xadc_manifest_validation_20260530.csv`
  and `data/experiments/xadc_summary/pvt_xadc_manifest_validation_20260531.csv`
- Board2 bitstream XADC comparison:
  `data/experiments/xadc_summary/board2_bitstream_xadc_compare_20260531.csv`

## Finding

The second held-out PVT manifest contains 58 rows across 23 capture IDs. All 58
rows have `xadc_status=ok`, but every row reports:

```text
temperature_c = -273.1
vccint_v      = 0.000
vccaux_v      = 0.000
vccbram_v     = 0.000
```

These values are not usable physical PVT evidence. Treat them as invalid XADC
readings even though the CSV parse path marked them `ok`.

After the subsequent warmup/aperture captures, the same manifest contains 112
PVT rows across 50 capture IDs. The refreshed offline validity summary reports:

```text
Rows scanned: 112
Captures scanned: 50
Row validity: invalid=112
Capture validity: invalid_pair=50
```

Thus the current conclusion did not improve with additional captures: every
Board2 pre/post XADC row in this manifest remains physically invalid.

The same sentinel pattern appears in the underlying second-heldout XADC CSV
from `2026-05-30 12:26:35` through `2026-05-30 15:11:34`, and in the Board2
top-level XADC CSV row from `2026-05-29 12:55:04`. The per-capture JSON metadata
also echoes the sentinel values in `xadc_before` and `xadc_after`.

By contrast, the historical Board1 XADC CSV contains plausible values such as:

```text
2026-05-11 23:28:54,47.4,1.000,1.797,1.000,
```

That contrast points to a Board2/XADC readout path problem or uninitialized
SysMon property read, not to a real die temperature or rail condition.

## Board1-Style Bitstream Check

To test whether the failure was caused by the current reduced-XOR bitstream, a
direct comparison was run on Board2:

1. Program the current Board2 second-heldout reduced-XOR `all640` bitstream.
2. Read XADC.
3. Program a historical Board1 TRNG bitstream on Board2.
4. Read XADC.
5. Restore the current Board2 second-heldout reduced-XOR `all640` bitstream.
6. Read XADC.

The resulting CSV,
`data/experiments/xadc_summary/board2_bitstream_xadc_compare_20260531.csv`,
has three rows. All three rows still report:

```text
TEMPERATURE = -273.1
VCCINT      = 0.000
VCCAUX      = 0.000
VCCBRAM     = 0.000
```

This means the Board2 problem is not explained by the current reduced-XOR
bitstream alone. The more likely boundary is the Board2 hardware target,
hw_server/SYSMON readout path, or board-specific state. It is still reasonable
to analyze valid UART payload captures, but the Board2 PVT values must not be
used as temperature or voltage evidence.

## Manifest/Cardinality Notes

- PVT manifest rows: 58.
- Distinct capture IDs in PVT manifest: 23.
- Moment counts: 30 `before`, 28 `after`.
- Capture IDs with duplicate PVT rows are present for several failed/retried
  `except_data_ro*` captures. This is expected from retry behavior, but it means
  analysis should group by `(capture_id, moment)` carefully.
- Capture manifest rows: 57.
- Capture manifest statuses: 28 `ok`, 17 `missing_after_retry`, 12
  `skipped_completed`.

## Schema Diagnosis

The current PVT schema separates capture moment (`before`/`after`) and parse
status (`xadc_status`), but it does not encode physical validity. The capture
driver's `Read-LastXadcRow` function reports `status="ok"` when `Import-Csv`
succeeds, without checking whether the XADC values are plausible.

Recommended downstream interpretation:

| Field | Meaning |
|---|---|
| `xadc_status` | Transport/parse status from the capture path. |
| `pvt_row_validity` | Offline physical validity of the row. |
| `pvt_invalid_reason` | Reason a parsed row is not usable PVT evidence. |
| `pvt_capture_status` | Capture-level PVT status after pairing valid `before` and `after` rows. |

Recommended validity rules for this run:

- Require `xadc_status=ok`.
- Require numeric `temperature_c`, `vccint_v`, `vccaux_v`, and `vccbram_v`.
- Treat `temperature_c` near `-273.1` or `-273.15` as a sentinel failure.
- Use generous physical bounds before accepting a row:
  `temperature_c=-40..125`, `vccint_v=0.80..1.20`,
  `vccaux_v=1.50..2.00`, and `vccbram_v=0.80..1.20`.
- Do not require `vpvn_v`; it is optional/blank in the existing schema.

## Non-Hardware Checker

Added an offline checker:

```powershell
python scripts\summarize_pvt_xadc_manifest_20260530.py `
  --out-csv data\experiments\xadc_summary\pvt_xadc_manifest_validation_20260530.csv
```

Expected result on the initial manifests:

```text
Manifests scanned: 1
Rows scanned: 58
Captures scanned: 23
Row validity: invalid=58
Capture validity: invalid_pair=23
```

The generated CSV is a derived diagnostic layer only. It leaves the original
PVT manifest and metadata untouched.

The refreshed warmup/aperture run should be summarized with:

```powershell
python scripts\summarize_pvt_xadc_manifest_20260530.py `
  --manifest data\hardware\20260529_fpga1_board2\restart_reduced_xor_second_heldout_sampler_20260530\summary\second_heldout_sample_ro_local_pvt_manifest_20260530.csv `
  --out-csv data\experiments\xadc_summary\pvt_xadc_manifest_validation_20260531.csv
```

The current refreshed result is `invalid=112` rows and `invalid_pair=50`
captures.

## Actionable Conclusion

For TVLSI second-heldout analysis, do not use the current Board2 XADC readings
as valid PVT covariates or guards. Mark the PVT evidence for these captures as
invalid/failed at the physical-validity layer while preserving the raw manifest
for auditability. Capture outputs may still be analyzed as hardware captures,
but any claim that relies on measured Board2 die temperature or rail stability
needs a fresh validated XADC path or an explicitly stated missing-PVT caveat.
