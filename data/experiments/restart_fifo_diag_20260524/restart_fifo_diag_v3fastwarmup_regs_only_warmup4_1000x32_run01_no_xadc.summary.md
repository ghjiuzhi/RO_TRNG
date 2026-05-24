# Restart FIFO Diagnostic Send Matrix: restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc

- input frames: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.frames.csv`
- packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.send_packed.bin`
- SHA256: `BD06ED21EAF164BA6A897E0D0ABFD80A9CDA7362E7E3CF0130AE51AD668319A6`
- matrix: `1000 x 32` packed bytes
- overall p1: `0.499285156`
- row ones mean/std/min/max: `127.817000000` / `7.823778563` / `103` / `151`
- worst bit position: byte `17`, bit `4`, p1 `0.449000000`, x `551`
- issues: total `0`, missing `0`, duplicate `0`, out-of-range `0`

## Most Biased Byte Positions

| byte_index | p1 | abs_bias | ones | zeros |
|---:|---:|---:|---:|---:|
| 2 | 0.488625000 | 0.011375000 | 3909 | 4091 |
| 28 | 0.489000000 | 0.011000000 | 3912 | 4088 |
| 0 | 0.491375000 | 0.008625000 | 3931 | 4069 |
| 25 | 0.507625000 | 0.007625000 | 4061 | 3939 |
| 30 | 0.506750000 | 0.006750000 | 4054 | 3946 |
| 29 | 0.494625000 | 0.005375000 | 3957 | 4043 |
| 3 | 0.505125000 | 0.005125000 | 4041 | 3959 |
| 20 | 0.505125000 | 0.005125000 | 4041 | 3959 |

## Most Biased Bit Positions

| byte_index | bit_index | p1 | x | msb_col | lsb_col |
|---:|---:|---:|---:|---:|---:|
| 17 | 4 | 0.449000000 | 551 | 139 | 140 |
| 28 | 2 | 0.449000000 | 551 | 229 | 226 |
| 13 | 1 | 0.543000000 | 543 | 110 | 105 |
| 17 | 7 | 0.538000000 | 538 | 136 | 143 |
| 21 | 0 | 0.538000000 | 538 | 175 | 168 |
| 15 | 0 | 0.536000000 | 536 | 127 | 120 |
| 6 | 5 | 0.535000000 | 535 | 50 | 53 |
| 9 | 2 | 0.535000000 | 535 | 77 | 74 |

## Compatible Column Analysis

The packed bin is row-major and can be passed directly to `scripts/analyze_restart_matrix_columns.py`:

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 32 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.column_analysis --label restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc
```
