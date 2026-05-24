# Restart Column Bias: restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.send_packed.bin`
- SHA256: `8665D8BF5157A8303EDBDA6F72D81252612EFBB3BD1D635EBCEED42481981430`
- matrix: `1000 x 32` packed bytes
- expanded columns: `256` bit positions per restart
- overall p1: `0.285109375`
- worst raw position: byte `0`, bit `3`, ones `101`, zeros `899`, x `899`
- MSB expanded column: `4`
- LSB expanded column: `3`

The CSV files preserve the raw byte/bit mapping so the same physical bit position can be compared across MSB-first and LSB-first SP800-90B input conversions.
