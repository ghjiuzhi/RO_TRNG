# Compact Restart FIFO Diagnostic: restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528

- input: `E:\Project\MLDSA\RO_TRNG\data\hardware\20260511_fpga1_board1\restart_fifo_diag\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528.bin`
- input SHA256: `64ED91314037BD8EB6CE53B230C539D42BE2C0ABB1120E315286E93AFE13761B`
- header: `{'version': 1, 'restart_count': 1000, 'row_bytes': 125, 'warmup_bytes': 5, 'total_bytes': 125000, 'marker': 170}`
- send packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528.send_packed.bin`
- send packed SHA256: `096EA004DA54EC2AA7972E5905C412DC66A54AC63A3709D1897114E7C2893D14`
- matrix: `1000 x 125` bytes
- overall p1: `0.371751000`
- row ones mean/std/min/max: `371.751000000` / `15.668088556` / `325` / `426`
- worst bit: byte `2`, bit `5`, p1 `0.255000000`, x `745`

## Column Analysis Command

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528.send_packed.bin --restart-count 1000 --bytes-per-restart 125 --label restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260525\restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run03_20260528.column_analysis
```
