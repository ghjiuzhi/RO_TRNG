# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.bin`
- input SHA256: `A34F4E7C6CD61C8EA9EE9C1C95DCDDEACBCA37ABC0F849093D5904B034B26033`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.send_packed.bin`
- send packed SHA256: `588BBEB1FD9D59E93C84468056BF77335F6E46EE129DBB50BA4E0E08AADC8F96`
- matrix: `1000 x 125` bytes
- overall p1: `0.376651000`
- row ones mean/std/min/max: `376.651000000` / `15.575596265` / `326` / `430`
- worst bit: byte `0`, bit `5`, p1 `0.116000000`, x `884`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525.column_analysis
```
