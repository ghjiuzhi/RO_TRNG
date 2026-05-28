# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.bin`
- input SHA256: `1C97A78710D12E6F477DBE61B3E3AF19ED05609BB94079B36638360FFB5AF5BE`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.send_packed.bin`
- send packed SHA256: `B37351202A54E4E0921C95DE68FFAB2147FB42B3A54DECC3A63728C191B12CCD`
- matrix: `1000 x 125` bytes
- overall p1: `0.375294000`
- row ones mean/std/min/max: `375.294000000` / `15.459998836` / `328` / `424`
- worst bit: byte `2`, bit `2`, p1 `0.204000000`, x `796`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528 --out-dir data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.column_analysis
```
