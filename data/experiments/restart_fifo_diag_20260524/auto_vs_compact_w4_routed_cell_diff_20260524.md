# Auto vs Compact W4 Routed Cell Diff - 2026-05-24

- formal cells dumped: `896`
- compact cells dumped: `902`
- common named cells: `886`
- common cells with LOC/BEL change: `682`
- diff CSV: `data\experiments\restart_fifo_diag_20260524\auto_vs_compact_w4_routed_cell_diff_20260524.csv`

| group | common cells | LOC changed | BEL changed |
| --- | ---: | ---: | ---: |
| entropy_source.data_ro | 48 | 0 | 0 |
| entropy_source.other | 17 | 0 | 0 |
| entropy_source.sample_ro | 27 | 2 | 3 |
| entropy_source.sampled_data_regs | 64 | 0 | 0 |
| fifo_generator | 241 | 195 | 151 |
| other | 4 | 1 | 1 |
| top_fsm_counters | 236 | 234 | 159 |
| uart_tx | 249 | 247 | 227 |

## Examples

| name | formal loc | compact loc | formal bel | compact bel |
| --- | --- | --- | --- | --- |
| `FSM_sequential_state_reg[0]` | `SLICE_X45Y40` | `SLICE_X43Y44` | `SLICEL.CFF` | `SLICEL.DFF` |
| `FSM_sequential_state_reg[1]` | `SLICE_X45Y41` | `SLICE_X42Y44` | `SLICEL.DFF` | `SLICEM.AFF` |
| `FSM_sequential_state_reg[2]` | `SLICE_X47Y41` | `SLICE_X43Y43` | `SLICEL.BFF` | `SLICEL.AFF` |
| `header_index_reg[0]` | `SLICE_X39Y36` | `SLICE_X35Y43` | `SLICEL.AFF` | `SLICEL.AFF` |
| `header_index_reg[1]` | `SLICE_X39Y36` | `SLICE_X35Y43` | `SLICEL.BFF` | `SLICEL.A5FF` |
| `header_index_reg[2]` | `SLICE_X39Y36` | `SLICE_X36Y43` | `SLICEL.A5FF` | `SLICEM.AFF` |
| `row_index[0]_i_1` | `SLICE_X37Y40` | `SLICE_X46Y39` | `SLICEL.A6LUT` | `SLICEM.A6LUT` |
| `row_index[10]_i_1` | `SLICE_X43Y42` | `SLICE_X44Y41` | `SLICEL.A6LUT` | `SLICEL.A6LUT` |
| `row_index[11]_i_1` | `SLICE_X43Y42` | `SLICE_X46Y41` | `SLICEL.B6LUT` | `SLICEM.A6LUT` |
| `row_index[12]_i_1` | `SLICE_X43Y42` | `SLICE_X46Y41` | `SLICEL.B5LUT` | `SLICEM.A5LUT` |
| `row_index[13]_i_1` | `SLICE_X43Y42` | `SLICE_X44Y41` | `SLICEL.A5LUT` | `SLICEL.A5LUT` |
| `row_index[14]_i_1` | `SLICE_X42Y43` | `SLICE_X44Y42` | `SLICEM.A6LUT` | `SLICEL.A6LUT` |
| `row_index[15]_i_1` | `SLICE_X42Y43` | `SLICE_X43Y42` | `SLICEM.B6LUT` | `SLICEL.A6LUT` |
| `row_index[16]_i_1` | `SLICE_X42Y43` | `SLICE_X43Y42` | `SLICEM.B5LUT` | `SLICEL.A5LUT` |
| `row_index[17]_i_1` | `SLICE_X42Y43` | `SLICE_X44Y42` | `SLICEM.A5LUT` | `SLICEL.A5LUT` |
| `row_index[18]_i_1` | `SLICE_X43Y44` | `SLICE_X44Y43` | `SLICEL.A6LUT` | `SLICEL.A6LUT` |
| `row_index[19]_i_1` | `SLICE_X44Y44` | `SLICE_X44Y43` | `SLICEL.A6LUT` | `SLICEL.B6LUT` |
| `row_index[1]_i_1` | `SLICE_X37Y40` | `SLICE_X46Y39` | `SLICEL.A5LUT` | `SLICEM.A5LUT` |
| `row_index[20]_i_1` | `SLICE_X44Y44` | `SLICE_X44Y43` | `SLICEL.A5LUT` | `SLICEL.B5LUT` |
| `row_index[21]_i_1` | `SLICE_X43Y44` | `SLICE_X44Y43` | `SLICEL.A5LUT` | `SLICEL.A5LUT` |
| `row_index[22]_i_1` | `SLICE_X43Y44` | `SLICE_X46Y43` | `SLICEL.B6LUT` | `SLICEM.C6LUT` |
| `row_index[23]_i_1` | `SLICE_X43Y43` | `SLICE_X43Y43` | `SLICEL.C5LUT` | `SLICEL.B5LUT` |
| `row_index[24]_i_1` | `SLICE_X38Y46` | `SLICE_X46Y43` | `SLICEM.A6LUT` | `SLICEM.A6LUT` |
| `row_index[25]_i_1` | `SLICE_X37Y46` | `SLICE_X46Y43` | `SLICEL.A6LUT` | `SLICEM.B6LUT` |
| `row_index[26]_i_1` | `SLICE_X38Y46` | `SLICE_X46Y44` | `SLICEM.B6LUT` | `SLICEM.A6LUT` |
| `row_index[27]_i_1` | `SLICE_X43Y46` | `SLICE_X44Y44` | `SLICEL.A6LUT` | `SLICEL.A6LUT` |
| `row_index[28]_i_1` | `SLICE_X43Y46` | `SLICE_X44Y44` | `SLICEL.B6LUT` | `SLICEL.C6LUT` |
| `row_index[29]_i_1` | `SLICE_X38Y46` | `SLICE_X46Y44` | `SLICEM.C6LUT` | `SLICEM.B6LUT` |
| `row_index[2]_i_1` | `SLICE_X37Y40` | `SLICE_X46Y39` | `SLICEL.B6LUT` | `SLICEM.B6LUT` |
| `row_index[30]_i_1` | `SLICE_X43Y45` | `SLICE_X44Y45` | `SLICEL.A6LUT` | `SLICEL.A6LUT` |
