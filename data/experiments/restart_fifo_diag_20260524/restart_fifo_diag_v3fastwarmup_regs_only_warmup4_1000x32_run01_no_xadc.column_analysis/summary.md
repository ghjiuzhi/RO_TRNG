# Restart Column Bias: restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc

- input: `E:\Project\MLDSA\RO_TRNG\data\experiments\restart_fifo_diag_20260524\restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.send_packed.bin`
- SHA256: `BD06ED21EAF164BA6A897E0D0ABFD80A9CDA7362E7E3CF0130AE51AD668319A6`
- matrix: `1000 x 32` packed bytes
- expanded columns: `256` bit positions per restart
- overall p1: `0.499285156`
- worst raw position: byte `17`, bit `4`, ones `449`, zeros `551`, x `551`
- MSB expanded column: `139`
- LSB expanded column: `140`

The CSV files preserve the raw byte/bit mapping so the same physical bit position can be compared across MSB-first and LSB-first SP800-90B input conversions.
