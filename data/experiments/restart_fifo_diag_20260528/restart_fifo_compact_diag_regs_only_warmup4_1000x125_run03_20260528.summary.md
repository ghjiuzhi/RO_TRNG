# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528.bin`
- input SHA256: `C405A876413EE8188E3A9E20558F36DB9C3563B3A2171D25AE9E9AF749C5F78A`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528.send_packed.bin`
- send packed SHA256: `39B4335587125E89BEDDC7B980CC5BDAA422103DD7F278AF420178B5600831AF`
- matrix: `1000 x 125` bytes
- overall p1: `0.499131000`
- row ones mean/std/min/max: `499.131000000` / `15.342354415` / `452` / `554`
- worst bit: byte `84`, bit `0`, p1 `0.556000000`, x `556`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run03_20260528.column_analysis
```
