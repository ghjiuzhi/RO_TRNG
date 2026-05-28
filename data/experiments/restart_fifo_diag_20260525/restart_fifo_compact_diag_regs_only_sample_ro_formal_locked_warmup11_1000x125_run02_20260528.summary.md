# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528.bin`
- input SHA256: `22242E327A1320FE5D458FD995A097994D22CFAE4042F52F62C1BF71663ED0B2`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 11, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528.send_packed.bin`
- send packed SHA256: `C82F1E8C13FFFDA7194BEEFDA3317E39A3E6636521920E7385EAB967F911CEE3`
- matrix: `1000 x 125` bytes
- overall p1: `0.461135000`
- row ones mean/std/min/max: `461.135000000` / `15.397752271` / `414` / `510`
- worst bit: byte `26`, bit `0`, p1 `0.412000000`, x `588`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run02_20260528.column_analysis
```
