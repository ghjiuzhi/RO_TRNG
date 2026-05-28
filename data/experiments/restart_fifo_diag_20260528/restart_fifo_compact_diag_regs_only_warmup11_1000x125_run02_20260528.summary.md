# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528.bin`
- input SHA256: `4114C65E67CB43A374A1E2BADA68DC2ED290553C4AC29BE34479E54516212940`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 11, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528.send_packed.bin`
- send packed SHA256: `4A656CDC7E29B1A0BF7DF73ADB8BAEF61101CA9584B025AAAD0FB69D39FBF23C`
- matrix: `1000 x 125` bytes
- overall p1: `0.498425000`
- row ones mean/std/min/max: `498.425000000` / `15.492720065` / `447` / `556`
- worst bit: byte `24`, bit `7`, p1 `0.456000000`, x `544`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run02_20260528.column_analysis
```
