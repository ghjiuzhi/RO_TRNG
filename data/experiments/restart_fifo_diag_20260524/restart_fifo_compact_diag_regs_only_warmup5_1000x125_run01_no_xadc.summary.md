# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.bin`
- input SHA256: `70B8335811743DB6853119D4A256E8B89E33AE0C450547A1F7810300E6CFD77D`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 5, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.send_packed.bin`
- send packed SHA256: `2332C65BE052DD36110FDB2EF50BF6FE708540A87DE247CCC09E998E05B8B98B`
- matrix: `1000 x 125` bytes
- overall p1: `0.498316000`
- row ones mean/std/min/max: `498.316000000` / `15.940330737` / `449` / `547`
- worst bit: byte `26`, bit `1`, p1 `0.549000000`, x `549`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc --out-dir data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.column_analysis
```
