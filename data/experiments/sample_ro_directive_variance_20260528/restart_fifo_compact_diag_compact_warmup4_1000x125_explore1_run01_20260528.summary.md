# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.bin`
- input SHA256: `6F70F6BE63CC3A8D8EB02E38FE1A11FB5AD1BD373FA64C8C363A3DAE98BE7ABB`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.send_packed.bin`
- send packed SHA256: `C25ECF9DC893BF145FC774046D7C265321904D8A318C04D61C16412ACAADCBD7`
- matrix: `1000 x 125` bytes
- overall p1: `0.496761000`
- row ones mean/std/min/max: `496.761000000` / `15.475331305` / `442` / `542`
- worst bit: byte `3`, bit `3`, p1 `0.440000000`, x `560`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528 --out-dir data\experiments\sample_ro_directive_variance_20260528\restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.column_analysis
```
