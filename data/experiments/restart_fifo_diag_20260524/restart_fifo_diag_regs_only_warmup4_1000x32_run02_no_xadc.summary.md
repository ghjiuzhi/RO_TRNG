# Restart FIFO Diagnostic Send Matrix: restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc

- input frames: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.frames.csv`
- packed bin: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.send_packed.bin`
- SHA256: `7FCCC9D47D304E06ACF76A0E913DBD9CC6AA202079DFC3CDD81BDC135E2A24F0`
- matrix: `1000 x 32` packed bytes
- overall p1: `0.392917969`
- row ones mean/std/min/max: `100.587000000` / `8.177434255` / `71` / `127`
- worst bit position: byte `0`, bit `6`, p1 `0.193000000`, x `807`
- issues: total `0`, missing `0`, duplicate `0`, out-of-range `0`

## Most Biased Byte Positions

| byte_index | p1 | abs_bias | ones | zeros |
|---:|---:|---:|---:|---:|
| 0 | 0.346750000 | 0.153250000 | 2774 | 5226 |
| 29 | 0.375375000 | 0.124625000 | 3003 | 4997 |
| 4 | 0.381250000 | 0.118750000 | 3050 | 4950 |
| 7 | 0.382375000 | 0.117625000 | 3059 | 4941 |
| 30 | 0.382500000 | 0.117500000 | 3060 | 4940 |
| 24 | 0.384000000 | 0.116000000 | 3072 | 4928 |
| 22 | 0.385125000 | 0.114875000 | 3081 | 4919 |
| 9 | 0.385375000 | 0.114625000 | 3083 | 4917 |

## Most Biased Bit Positions

| byte_index | bit_index | p1 | x | msb_col | lsb_col |
|---:|---:|---:|---:|---:|---:|
| 0 | 6 | 0.193000000 | 807 | 1 | 6 |
| 0 | 4 | 0.197000000 | 803 | 3 | 4 |
| 3 | 0 | 0.280000000 | 720 | 31 | 24 |
| 5 | 7 | 0.284000000 | 716 | 40 | 47 |
| 4 | 1 | 0.289000000 | 711 | 38 | 33 |
| 1 | 7 | 0.309000000 | 691 | 8 | 15 |
| 7 | 2 | 0.327000000 | 673 | 61 | 58 |
| 0 | 7 | 0.334000000 | 666 | 0 | 7 |

## Compatible Column Analysis

The packed bin is row-major and can be passed directly to `scripts/analyze_restart_matrix_columns.py`:

```powershell
python scripts\analyze_restart_matrix_columns.py --input E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.send_packed.bin --restart-count 1000 --bytes-per-restart 32 --out-dir E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.column_analysis --label restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc
```
