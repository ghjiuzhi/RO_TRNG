# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528.bin`
- input SHA256: `1EEEF2FA9D4B89A2CD95645EC2AFF08D11207E2A8DDEE60643BF41ACA21DACED`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 4, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528.send_packed.bin`
- send packed SHA256: `8AEF145052A04159E00A2ACCF97484BD3025F14DE7AD3E3A1B71797043FFB675`
- matrix: `1000 x 125` bytes
- overall p1: `0.378757000`
- row ones mean/std/min/max: `378.757000000` / `16.246351929` / `326` / `432`
- worst bit: byte `2`, bit `0`, p1 `0.248000000`, x `752`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run03_20260528.column_analysis
```
