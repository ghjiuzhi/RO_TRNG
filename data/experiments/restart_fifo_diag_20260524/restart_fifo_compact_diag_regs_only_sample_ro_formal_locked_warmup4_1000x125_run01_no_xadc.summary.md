# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.bin`
- input SHA256: `1A79DC13BE9FC2596F4FB60255D50C96E5BE5D3A5EEE83A3B24A35FD3DC26428`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.send_packed.bin`
- send packed SHA256: `6935E4698D4945E629E8361A4F6F9E6BC6750E54C1180B390A839D6F25EA67CE`
- matrix: `1000 x 125` bytes
- overall p1: `0.376796000`
- row ones mean/std/min/max: `376.796000000` / `14.577255709` / `325` / `430`
- worst bit: byte `0`, bit `5`, p1 `0.195000000`, x `805`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc --out-dir data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.column_analysis
```
