# Restart Column Bias: smoke_run01_fixed_decode

- input: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\smoke_run01_fixed_decode.send_packed.bin`
- SHA256: `52B4CA34924B4970F8193457EF810B39E2EF23D149E86900215FBCF5CED3576E`
- matrix: `32 x 16` packed bytes
- expanded columns: `128` bit positions per restart
- overall p1: `0.377197266`
- worst raw position: byte `3`, bit `4`, ones `5`, zeros `27`, x `27`
- MSB expanded column: `27`
- LSB expanded column: `28`

The CSV files preserve the raw byte/bit mapping so the same physical bit position can be compared across MSB-first and LSB-first SP800-90B input conversions.
