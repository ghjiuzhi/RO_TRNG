# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.bin`
- input SHA256: `6564D472A495F2344D79E99C3DB758163ABD656F81677977EC33031EF1A4E9AF`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 11, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.send_packed.bin`
- send packed SHA256: `592761B2FCC4ACCE5AF191A4EEC1906B1CADFB07FE1412D31406A59C89046B6F`
- matrix: `1000 x 125` bytes
- overall p1: `0.498148000`
- row ones mean/std/min/max: `498.148000000` / `15.991625809` / `444` / `548`
- worst bit: byte `90`, bit `6`, p1 `0.452000000`, x `548`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc --out-dir data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.column_analysis
```
