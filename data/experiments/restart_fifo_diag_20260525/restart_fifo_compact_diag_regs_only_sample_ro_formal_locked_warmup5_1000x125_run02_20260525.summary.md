# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525.bin`
- input SHA256: `8A980D32DDADDBA678C4B5A64B715A3C53291605D0F3C94E67772068A9C69DDC`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 5, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525.send_packed.bin`
- send packed SHA256: `7E45D2883DD8624A93CF10394AD7D0DA4420A0C67BD76B4290DC2BDF5820115C`
- matrix: `1000 x 125` bytes
- overall p1: `0.373541000`
- row ones mean/std/min/max: `373.541000000` / `16.146278797` / `324` / `434`
- worst bit: byte `1`, bit `2`, p1 `0.208000000`, x `792`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525.column_analysis
```
