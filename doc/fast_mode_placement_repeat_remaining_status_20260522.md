# Fast Mode Hardware Status

- updated: 2026-05-22 23:45:00
- phase: done
- message: Queue finished. All 20MiB TRNG placement repeat files are complete; metadata/analysis were recovered after fixing the post-capture XADC handling issue.
- port: COM3
- baud: 115200

| priority | run | kind | bytes | status | output |
| --- | --- | --- | ---: | --- | --- |
| P0 | same_column_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\same_column_repeat03_20mib.bin` |
| P0 | sparse_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\sparse_repeat03_20mib.bin` |
| P0 | far_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\far_repeat03_20mib.bin` |
| P0 | compact_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\compact_repeat03_20mib.bin` |
| P0 | checker_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\checker_repeat03_20mib.bin` |
| P1 | random2_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\random2_repeat03_20mib.bin` |
| P1 | row_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\row_repeat03_20mib.bin` |
| P1 | cross_region_repeat03_20mib | trng | 20MiB | complete + analyzed | `data\hardware\20260511_fpga1_board1\trng\cross_region_repeat03_20mib.bin` |

## Post-Processing Note

The original queue captured full-size files and SHA256 sidecars, but the post-capture XADC block returned Vivado stdout together with the result object, which caused a `temperature_c` property error before metadata and TRNG analysis were written. This has been fixed in `scripts\capture_uart.ps1`, and existing completed captures were recovered with `scripts\recover_completed_trng_captures.py`.
