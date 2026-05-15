# Offline Data Consistency Audit - 2026-05-15

Scope: offline-only consistency audit for `random3` warmup10/11/12 `repeat02`. No hardware, Vivado programming, COM3, or JTAG command was intentionally launched during this audit.

## Files Read

Key status documents:

- `doc/fast_mode_master_status_20260514.md`
- `doc/restart_warmup_repeat02_status_20260515.md`
- `doc/sp800_90b_restart_execution_status_20260514.md`

Key tables and logs:

- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.csv`
- `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition_with_repeats.csv`
- `data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.csv`
- `data/experiments/restart_warmup_repeat_logs_20260515/restart_warmup_repeat02_summary.json`
- `data/experiments/restart_warmup_repeat_logs_20260515/warmup_repeat02_stdout.log`
- `data/experiments/restart_warmup_repeat_logs_20260515/warmup_repeat02_stderr.log`

Key repeat02 analysis metadata:

- `data/experiments/paper_artifacts_20260515/restart_column_bias_random3_formal_bits_warmup10_repeat02/summary.json`
- `data/experiments/paper_artifacts_20260515/restart_column_bias_random3_formal_bits_warmup11_repeat02/summary.json`
- `data/experiments/paper_artifacts_20260515/restart_column_bias_random3_formal_bits_warmup12_repeat02/summary.json`
- `data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_repeat02_20260515*.metadata.json`
- `data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_repeat02_20260515*.metadata.json`
- `data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_repeat02_20260515*.metadata.json`
- `data/hardware/20260511_fpga1_board1/restart/ea_restart_random3_warmup10_repeat02_*_20260515/*.txt` and `*.metadata.json`
- `data/hardware/20260511_fpga1_board1/restart/ea_restart_random3_warmup11_repeat02_*_20260515/*.txt` and `*.metadata.json`
- `data/hardware/20260511_fpga1_board1/restart/ea_restart_random3_warmup12_repeat02_*_20260515/*.txt` and `*.metadata.json`

Note: there is no project-root `metadata` directory. The relevant metadata files are under `data/hardware/20260511_fpga1_board1/restart/` and `data/sp800_90b/restart_results_20260515/`.

## Consistency Summary

The repeat02 headline is internally consistent across the current repeat table, repeat summary JSON, column-bias summaries, ea_restart stdout files, metadata, file sizes, and recomputed SHA256 values:

- `warmup10 repeat02` failed for both MSB and LSB.
- `warmup11 repeat02` passed for both MSB and LSB.
- `warmup12 repeat02` passed for both MSB and LSB.
- The observed repeated boundary remains `10 < WARMUP_BYTES <= 11` for this board, placement, and auto-stream restart protocol.

## Repeat02 Checked Values

| warmup | packed bytes | packed SHA256 | overall p1 | over cutoff | worst byte.bit | worst X | MSB result | LSB result |
| ---: | ---: | --- | ---: | ---: | --- | ---: | --- | --- |
| 10 | 125000 | `743E2A6536BFFAADDBFEE8F45FFE8DE4D14734504118CAFB3D3DAB7A2A1C7CAD` | 0.415849000 | 89 | 6.0 | 633 | failed, `H_I=0.902345`, `X_cutoff=605`, `X_max=633` | failed, `H_I=0.828444`, `X_cutoff=632`, `X_max=633` |
| 11 | 125000 | `806E52B1C50539152C6AE5450E7CD47E961DFC4B9E0197788F722711386A0BB6` | 0.469261000 | 0 | 68.3 | 588 | passed, `H_I=0.902345`, `X_cutoff=605`, `X_max=588`, min 0.765014 | passed, `H_I=0.828444`, `X_cutoff=632`, `X_max=588`, min 0.746636 |
| 12 | 125000 | `2137FD20C71F1245E2568E4AFE4F86FA126B04536E4E63588CE1257D2E0BA134` | 0.499506000 | 0 | 118.1 | 549 | passed, `H_I=0.902345`, `X_cutoff=605`, `X_max=556`, min 0.813237 | passed, `H_I=0.828444`, `X_cutoff=632`, `X_max=556`, min 0.828444 |

The `worst X` in the column-bias table is the worst packed byte/bit column from the offline column analysis. For warmup12 repeat02, ea_restart reports `X_max=556`, while the packed-position column summary reports worst packed `x=549`. This is not necessarily a contradiction: the ea_restart row/column sanity maximum can come from either row or expanded-column statistics, while the column-bias summary reports packed byte/bit positions only.

## File Size and SHA256 Check

Recomputed hashes match the table/log/metadata values:

| file kind | warmup10 | warmup11 | warmup12 |
| --- | --- | --- | --- |
| packed `.bin` size | 125000 | 125000 | 125000 |
| packed SHA256 | `743E2A6536BFFAADDBFEE8F45FFE8DE4D14734504118CAFB3D3DAB7A2A1C7CAD` | `806E52B1C50539152C6AE5450E7CD47E961DFC4B9E0197788F722711386A0BB6` | `2137FD20C71F1245E2568E4AFE4F86FA126B04536E4E63588CE1257D2E0BA134` |
| MSB bps1 size | 1000000 | 1000000 | 1000000 |
| MSB bps1 SHA256 | `81497E66D2D25D6FA4AECF64237BC671FFD2EC720FB86BD2EC5CCABA2F52AFFA` | `C7C030EBBB907A497F07D1470FFEDBCADEB7E45FA8F576D5C67DCCFF01A2AEEC` | `19BC177436E6C47B63440E6B068A3591C3393D0867F9C39434E0A825D12D9528` |
| LSB bps1 size | 1000000 | 1000000 | 1000000 |
| LSB bps1 SHA256 | `379F505566F2E03897A2CC717693FE0027E152CFA98E37C39E1B801CD864E402` | `5EAFC5C39A22D656FC7DCC31980E85BAB76B278DCD8266A881E102F7762A7A8E` | `C3302B0F6B851845337F587918D1682B22527E3762E3942C224AAB6E6F79EF20` |

## Issues and Caveats

1. `table_restart_warmup_transition.csv` appears to be an older first-pass table and has stale LSB `X_cutoff=605` values for warmup8/10/11/12/16. The current repeated table and ea_restart stdout use LSB `X_cutoff=632`, which is consistent with `H_I=0.828444`. Use `table_restart_warmup_transition_with_repeats.csv` for repeat02 reporting.

2. `doc/restart_warmup_repeat02_status_20260515.md` says warmup12 repeat02 has `worst X=549` but `passed (Xmax=556)`. This is consistent only if `worst X` means packed column-bias worst position and `Xmax` means ea_restart maximum. The document would be clearer if it labels these as separate quantities.

3. `doc/sp800_90b_restart_execution_status_20260514.md` is readable but displayed with mojibake in this environment. The ASCII paths, hashes, `H_I`, `X_cutoff`, and `X_max` values inspected there align with the other files, but the encoding damage makes it a weaker source for manual review than the CSV/JSON/stdout artifacts.

4. The packed capture metadata contains `formal_90b_restart_size: false` and the logs print "This is not 1000x1000" for the packed 1000 x 125 byte files. This is not a data contradiction because the packed files are intentionally expanded to 1000 x 1000 one-byte bit-symbol files before ea_restart. The bps1 metadata/files show 1000000 bytes and `bits_per_symbol=1`.

5. The repeat02 run log includes warmup10 ea_restart failures with exit code `-1`; this is expected for "Restart Sanity Check Failed". The queue continued and produced warmup11/12 pass outputs plus `restart_warmup_repeat02_summary.json`.

## Conclusion

No substantive data contradiction was found for the current repeat02 claim. The evidence chain supports: warmup10 repeat02 failed, warmup11 repeat02 passed, and warmup12 repeat02 passed, with consistent packed and bps1 SHA256/file-size records. The main cleanup need is presentation-level: prefer the repeat-aware CSV, and distinguish packed-column worst `x` from ea_restart `X_max` in prose tables.
