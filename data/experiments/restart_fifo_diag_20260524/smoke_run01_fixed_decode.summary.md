# Restart FIFO Diagnostic Send Matrix: smoke_run01_fixed_decode

- input frames: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\smoke_run01_fixed_decode.frames.csv`
- packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\smoke_run01_fixed_decode.send_packed.bin`
- SHA256: `52B4CA34924B4970F8193457EF810B39E2EF23D149E86900215FBCF5CED3576E`
- matrix: `32 x 16` packed bytes
- overall p1: `0.377197266`
- row ones mean/std/min/max: `48.281250000` / `5.449967746` / `38` / `62`
- worst bit position: byte `3`, bit `4`, p1 `0.156250000`, x `27`
- issues: total `0`, missing `0`, duplicate `0`, out-of-range `0`

## Most Biased Byte Positions

| byte_index | p1 | abs_bias | ones | zeros |
|---:|---:|---:|---:|---:|
| 2 | 0.343750000 | 0.156250000 | 88 | 168 |
| 14 | 0.343750000 | 0.156250000 | 88 | 168 |
| 4 | 0.355468750 | 0.144531250 | 91 | 165 |
| 1 | 0.359375000 | 0.140625000 | 92 | 164 |
| 3 | 0.359375000 | 0.140625000 | 92 | 164 |
| 13 | 0.359375000 | 0.140625000 | 92 | 164 |
| 6 | 0.363281250 | 0.136718750 | 93 | 163 |
| 15 | 0.367187500 | 0.132812500 | 94 | 162 |

## Most Biased Bit Positions

| byte_index | bit_index | p1 | x | msb_col | lsb_col |
|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 0.156250000 | 27 | 27 | 28 |
| 1 | 1 | 0.187500000 | 26 | 14 | 9 |
| 2 | 3 | 0.187500000 | 26 | 20 | 19 |
| 12 | 0 | 0.187500000 | 26 | 103 | 96 |
| 6 | 7 | 0.218750000 | 25 | 48 | 55 |
| 10 | 5 | 0.218750000 | 25 | 82 | 85 |
| 13 | 1 | 0.218750000 | 25 | 110 | 105 |
| 1 | 0 | 0.250000000 | 24 | 15 | 8 |

## Compatible Column Analysis

The packed bin is row-major and can be passed directly to `scripts/analyze_restart_matrix_columns.py`:

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\smoke_run01_fixed_decode.send_packed.bin --restart-count 32 --bytes-per-restart 16 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\smoke_run01_fixed_decode.column_analysis --label smoke_run01_fixed_decode
```
