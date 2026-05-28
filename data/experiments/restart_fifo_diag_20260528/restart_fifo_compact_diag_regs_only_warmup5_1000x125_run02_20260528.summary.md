# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528.bin`
- input SHA256: `F2D4C3EB9AE679F0E62CFBD85C2793E3830AC61E155B04A70B5315CA4E50AC19`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 5, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528.send_packed.bin`
- send packed SHA256: `011546D3D2B724F6ECA984698908230A58FAE3D6241D8C570385D3265A413D43`
- matrix: `1000 x 125` bytes
- overall p1: `0.499276000`
- row ones mean/std/min/max: `499.276000000` / `15.834261082` / `451` / `561`
- worst bit: byte `95`, bit `6`, p1 `0.452000000`, x `548`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260528\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run02_20260528.column_analysis
```
