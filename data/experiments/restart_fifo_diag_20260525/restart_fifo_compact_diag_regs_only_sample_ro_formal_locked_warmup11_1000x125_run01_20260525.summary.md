# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.bin`
- input SHA256: `714C29CB96098DF231C0D0FEAEB8C49CEFFC745A1E73AFE1F66D03381C8FB37C`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 11, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.send_packed.bin`
- send packed SHA256: `3663963D27F6C5F4682E7E45278CE6D710E2E8A4B39E80A09C24E455FAA08AC7`
- matrix: `1000 x 125` bytes
- overall p1: `0.464819000`
- row ones mean/std/min/max: `464.819000000` / `16.116830923` / `415` / `512`
- worst bit: byte `18`, bit `4`, p1 `0.424000000`, x `576`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525.column_analysis
```
