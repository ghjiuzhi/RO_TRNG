# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.bin`
- input SHA256: `AF82E88A362F51624C88ACB63A23B7574A4245062E894A3DA1D47E962199BB85`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 5, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.send_packed.bin`
- send packed SHA256: `ABF3BF6B847CCE468C01592EAC575BFABD67D1E26451FE595D6EE71A40BBB4B7`
- matrix: `1000 x 125` bytes
- overall p1: `0.373430000`
- row ones mean/std/min/max: `373.430000000` / `15.638257576` / `328` / `425`
- worst bit: byte `2`, bit `2`, p1 `0.243000000`, x `757`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525.column_analysis
```
