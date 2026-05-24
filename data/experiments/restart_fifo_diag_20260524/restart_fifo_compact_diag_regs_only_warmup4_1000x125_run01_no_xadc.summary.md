# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.bin`
- input SHA256: `EFB2ADE99B65534889C1625D69CA03742D8228A7EEDB2AF7F6FBB84035E05AEB`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.send_packed.bin`
- send packed SHA256: `018A2D008554AC928D41CED2A0C15C5558BD87522484A93A9476CEFD566E42DC`
- matrix: `1000 x 125` bytes
- overall p1: `0.498297000`
- row ones mean/std/min/max: `498.297000000` / `15.119086976` / `447` / `547`
- worst bit: byte `1`, bit `7`, p1 `0.445000000`, x `555`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc --out-dir data\experiments\restart_fifo_diag_20260524\restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.column_analysis
```
