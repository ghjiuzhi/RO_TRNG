# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528.bin`
- input SHA256: `47B9D2394177A4624553FFA437C36B2274A5EA74564EF93744DE92E789C5F09B`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528.send_packed.bin`
- send packed SHA256: `FBDDD7C686BF2E3650D4375E1990D9820058493DE18A9082639E83B219A2E9F5`
- matrix: `1000 x 125` bytes
- overall p1: `0.499008000`
- row ones mean/std/min/max: `499.008000000` / `15.995747435` / `438` / `543`
- worst bit: byte `3`, bit `5`, p1 `0.438000000`, x `562`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run02_20260528.column_analysis
```
