# Restart FIFO Diagnostic Send Matrix: restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc

- input frames: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.frames.csv`
- packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.send_packed.bin`
- SHA256: `8665D8BF5157A8303EDBDA6F72D81252612EFBB3BD1D635EBCEED42481981430`
- matrix: `1000 x 32` packed bytes
- overall p1: `0.285109375`
- row ones mean/std/min/max: `72.988000000` / `7.648258364` / `51` / `101`
- worst bit position: byte `0`, bit `3`, p1 `0.101000000`, x `899`
- issues: total `0`, missing `0`, duplicate `0`, out-of-range `0`

## Most Biased Byte Positions

| byte_index | p1 | abs_bias | ones | zeros |
|---:|---:|---:|---:|---:|
| 0 | 0.240625000 | 0.259375000 | 1925 | 6075 |
| 6 | 0.267750000 | 0.232250000 | 2142 | 5858 |
| 3 | 0.267875000 | 0.232125000 | 2143 | 5857 |
| 9 | 0.276250000 | 0.223750000 | 2210 | 5790 |
| 25 | 0.277750000 | 0.222250000 | 2222 | 5778 |
| 17 | 0.277875000 | 0.222125000 | 2223 | 5777 |
| 23 | 0.279125000 | 0.220875000 | 2233 | 5767 |
| 15 | 0.281125000 | 0.218875000 | 2249 | 5751 |

## Most Biased Bit Positions

| byte_index | bit_index | p1 | x | msb_col | lsb_col |
|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 0.101000000 | 899 | 4 | 3 |
| 1 | 7 | 0.118000000 | 882 | 8 | 15 |
| 0 | 6 | 0.130000000 | 870 | 1 | 6 |
| 3 | 6 | 0.147000000 | 853 | 25 | 30 |
| 0 | 5 | 0.176000000 | 824 | 2 | 5 |
| 6 | 7 | 0.181000000 | 819 | 48 | 55 |
| 0 | 2 | 0.182000000 | 818 | 5 | 2 |
| 3 | 3 | 0.202000000 | 798 | 28 | 27 |

## Compatible Column Analysis

The packed bin is row-major and can be passed directly to `scripts/analyze_restart_matrix_columns.py`:

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 32 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.column_analysis --label restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc
```
