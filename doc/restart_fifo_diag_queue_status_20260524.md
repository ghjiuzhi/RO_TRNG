# Restart FIFO Diagnostic Queue Status - 2026-05-24

## Current goal

Use the formal restart FIFO/readout path itself to explain why
`random1_sampler_regs_only_x45y31` has a non-monotonic restart warmup passband.

The key comparison is:

- warmup4: formal restart fail, global low-one bias
- warmup5: formal restart pass, near-balanced output
- warmup10: formal restart pass, near-balanced output
- warmup11: formal restart fail, global high-one bias

The new diagnostic top records FIFO output byte events before UART replay, so it
keeps the official entropy source and FIFO byte-packing path while making the
internal row/event/byte structure visible.

## Why this matters

Earlier evidence already weakens simple RO-RO hard locking:

- pair-TDC correlations are near zero and show no strong-lock windows.
- moving only sampler registers/routing makes the continuous stream nearly
  ideal.
- however, the same sampler-regs-only design still has restart failures.

Therefore the current mechanism target is narrower:

> placement changes the sampler-side physical implementation, but restart
> failures may be amplified by the official FIFO byte-packing / warmup discard /
> fixed output-position path.

## Current queue

Script:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_restart_fifo_diag_regs_only_queue_20260524.ps1
```

Matrix:

| placement | warmup | restart_count | row_bytes | expected bytes |
| --- | ---: | ---: | ---: | ---: |
| random1_sampler_regs_only_x45y31 | 4 | 1000 | 32 | 576016 |
| random1_sampler_regs_only_x45y31 | 5 | 1000 | 32 | 576016 |
| random1_sampler_regs_only_x45y31 | 10 | 1000 | 32 | 576016 |
| random1_sampler_regs_only_x45y31 | 11 | 1000 | 32 | 576016 |

Logs:

- `data/experiments/restart_fifo_diag_20260524/fifo_diag_queue_stdout.log`
- `data/experiments/restart_fifo_diag_20260524/fifo_diag_queue_stderr.log`
- `data/experiments/restart_fifo_diag_20260524/queue_logs/`

Outputs:

- captures: `data/hardware/20260511_fpga1_board1/restart_fifo_diag/`
- decoded frames: `data/experiments/restart_fifo_diag_20260524/*.frames.csv`
- summaries: `data/experiments/restart_fifo_diag_20260524/*.summary.md`

## First smoke result

The earlier `32 x 16, warmup4` smoke capture was valid. The initial all-zero
interpretation was caused by a byte-order mismatch in
`scripts/analyze_restart_fifo_diag.py`; after fixing the decoder, the same
capture shows:

- warmup frames: 128
- send frames: 512
- rows observed: 32
- event indexes: warmup 0..3, send 0..15

This proves the diagnostic UART/BRAM/header path is working and the current
queue is a meaningful next experiment.

## Slow-warmup diagnostic result

The first `1000 x 32` diagnostic implementation was captured successfully after
removing the pre-capture XADC read from the critical UART timing path.

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.bin`
- capture size: `576016` bytes
- capture SHA256:
  `7BB74291FCDF2FC3B2832BEFB64BBBD16BDF687C6CB360EDFD8E1B01EFEBB63B`
- send matrix:
  `data/experiments/restart_fifo_diag_20260524/restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc.send_packed.bin`
- matrix size: `1000 x 32` bytes
- warmup4 send-matrix p1: `0.392917969`
- row ones mean/std/min/max:
  `100.587000000 / 8.177434255 / 71 / 127`
- worst bit: byte `0`, bit `6`, p1 `0.193000000`, x `807`

The matching slow-warmup warmup5 diagnostic also produced a strong low-one
bias:

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc.bin`
- send-matrix p1: `0.285109375`
- worst bit: byte `0`, bit `3`, p1 `0.101000000`, x `899`

This result initially looked surprising because formal warmup5 passes. The
important correction is that the first diagnostic top did not preserve formal
warmup timing: it throttled warmup reads with `UART_BYTE_CYCLES`, while
`RO_TRNG_restart_auto_top` discards warmup bytes immediately whenever the FIFO is
non-empty. That slow warmup changes how long the RO and FIFO path remain active
before send-phase capture and is therefore a diagnostic perturbation.

Interpretation: the slow-warmup diagnostic is useful as an engineering check,
but not a faithful formal-restart mechanism measurement. A v3 diagnostic top now
uses fast warmup discard like the formal design and should replace the slow
diagnostic for paper claims.

The first `warmup4` attempt with inline `-RecordXadc` produced a partial file
(`522352 / 576016` bytes) that began with a diagnostic frame instead of the
`FDIA` header. This confirmed that pre-capture XADC can make the PC open COM3
too late for the 60-second debug start delay. For the remaining FIFO diagnostic
runs, capture should avoid inline pre-capture XADC; read XADC before/after as a
separate measurement or rebuild with a longer start delay.

## Faithful warmup v3 plan

RTL change:

- `rtl/restart/RO_TRNG_restart_fifo_diag_top.v`
- header version changed from `0x02` to `0x03`
- `ST_WARMUP` now reads FIFO bytes as soon as available, matching
  `RO_TRNG_restart_auto_top`, instead of waiting for `UART_BYTE_CYCLES`

Immediate v3 matrix:

| placement | warmup | restart_count | row_bytes | purpose |
| --- | ---: | ---: | ---: | --- |
| random1_sampler_regs_only_x45y31 | 4 | 1000 | 32 | formal fail / low-bias reference |
| random1_sampler_regs_only_x45y31 | 5 | 1000 | 32 | formal pass edge |

If v3 warmup4 is low-biased and v3 warmup5 is near-balanced, then the FIFO
diagnostic directly reproduces the formal pass/fail transition. If both are
near formal behavior only in the full 125-byte data but not the first 32 bytes,
then the mechanism is a byte-window effect in the formal readout sequence.

## Updated v3 findings

The faithful v3 16-byte-frame diagnostic was built and captured for
`warmup4, 1000 x 32`:

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc.bin`
- p1: `0.499285156`
- worst x: `551`

This means the first 32 send bytes are near ideal when warmup timing matches the
formal auto-stream. The earlier low-bias result was caused by diagnostic
warmup-throttling perturbation.

The faithful v3 16-byte-frame `1000 x 125` build was attempted but could not fit
on XC7Z020:

- required `152` RAMB36/FIFO cells
- available `140`

Therefore a compact diagnostic top was added:

- `rtl/restart/RO_TRNG_restart_fifo_compact_diag_top.v`
- output format: 16-byte `FDIC` header followed directly by row-major send bytes
- same formal hold/settle/warmup/FIFO/UART path, but no diagnostic BRAM frames

Compact `warmup4, 1000 x 125` was captured:

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc.bin`
- capture SHA256:
  `EFB2ADE99B65534889C1625D69CA03742D8228A7EEDB2AF7F6FBB84035E05AEB`
- packed p1: `0.498297000`
- row ones std: `15.119086976`
- worst x: `555`

Interpretation: the entropy-source/FIFO real-time send path is near ideal for
the same placement, warmup, restart count, and row length where the formal
auto-stream restart file had p1 near `0.407`. This pushes the likely mechanism
away from raw RO/FIFO byte generation and toward the auto-stream capture/replay
implementation, run-to-run state, or storage/readout scheduling. It is also a
strong guard against over-claiming that TDC or raw FIFO phase alone explains the
formal restart failure.

Compact `warmup5, 1000 x 125` has now also been captured:

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc.bin`
- capture size: `125016` bytes
- capture SHA256:
  `70B8335811743DB6853119D4A256E8B89E33AE0C450547A1F7810300E6CFD77D`
- packed p1: `0.498316000`
- worst x: `549`
- column worst: byte `26`, bit `1`, x `549`, p1 `0.549`

Compact comparison:

| diagnostic | warmup | matrix | packed p1 | worst x | interpretation |
| --- | ---: | --- | ---: | ---: | --- |
| compact FIFO diag | 4 | `1000 x 125` | `0.498297000` | `555` | near ideal |
| compact FIFO diag | 5 | `1000 x 125` | `0.498316000` | `549` | near ideal |

Interpretation update: compact w4 and w5 are both near ideal, so the formal
restart w4 fail / w5 pass transition did not reproduce in the compact
real-time FIFO diagnostic path. This points the mechanism toward formal
auto-stream behavior, bitstream-specific behavior, readout scheduling, or exact
constraint differences, rather than a simple imbalance in raw FIFO byte
generation.

Capture notes from this run:

- `program_and_capture_uart.ps1 -VivadoBat` should receive `vivado.bat`, not
  `settings64.bat`.
- For bitstreams with `60s START_DELAY`, use `-IdleTimeoutSec 90` or longer so
  the host capture does not time out before the delayed UART stream begins.

## Interpretation plan

If warmup4 and warmup11 diagnostic send bytes reproduce the formal low/high
global bias while warmup5 and warmup10 remain balanced, then the formal restart
failure is already present at the FIFO byte-output boundary.

If diagnostic send bytes are balanced for all warmups, but formal 1000x125
restart still fails, then the mechanism is downstream of this diagnostic window:
longer row length, later byte positions, or the full UART/readout scheduling.

If the bias only appears in fixed byte/event positions, this supports a
windowed output-position mechanism rather than a simple RO locking story.

## Formal auto retest and routed-diff update

To check whether the earlier formal `warmup4` failure was a stale-bitstream or
capture artifact, a same-night retest bitstream was rebuilt from
`RO_TRNG_restart_auto_top` with the same placement XDC and parameters:

- placement:
  `data/experiments/xdc_sampler_island/random1_sampler_regs_only_x45y31.xdc`
- top: `RO_TRNG_restart_auto_top`
- restart matrix: `1000 x 125`
- warmup bytes: `4`
- start delay: `12000000000`
- capture:
  `data/hardware/20260511_fpga1_board1/restart/random1_sampler_regs_only_restart_auto_formal_1000x125_warmup4_retest01_20260524.bin`
- capture size: `125008` bytes
- capture SHA256:
  `AC3D7D6D9A9531B86947EB69495CD27C62EFE554C6FF052F2D2D254146AFCBC2`
- header: `A55A03E8007D01D0`
- packed data SHA256:
  `E65394FB07B954C4A6021C1CBEA9602D83400DB35A26EA00DB5A281205793A58`
- packed p1: `0.406735000`
- row ones std: `17.174713244`
- worst position: byte `0`, bit `2`, p1 `0.297000000`, x `703`

This confirms that the formal auto `warmup4` low-bias result is reproducible in
a freshly rebuilt same-night bitstream. The contrast with compact diagnostics is
therefore strong:

| design | warmup | matrix | packed p1 | row ones std | worst x | result |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| formal auto retest | 4 | `1000 x 125` | `0.406735000` | `17.174713244` | `703` | low-bias fail |
| compact FIFO diag | 4 | `1000 x 125` | `0.498297000` | `15.119086976` | `555` | near ideal |
| compact FIFO diag | 5 | `1000 x 125` | `0.498316000` | `15.940330737` | `549` | near ideal |

A routed checkpoint comparison was also generated:

- formal cell dump:
  `data/experiments/restart_fifo_diag_20260524/formal_auto_w4_retest_routed_cells.csv`
- compact cell dump:
  `data/experiments/restart_fifo_diag_20260524/compact_w4_routed_cells.csv`
- diff summary:
  `data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.md`
- diff CSV:
  `data/experiments/restart_fifo_diag_20260524/auto_vs_compact_w4_routed_cell_diff_20260524.csv`

The common named-cell diff found `682 / 886` common cells with LOC or BEL
changes. The data RO and sampled-data registers stayed fixed, but surrounding
logic changed heavily:

| group | common cells | LOC changed | BEL changed |
| --- | ---: | ---: | ---: |
| entropy_source.data_ro | 48 | 0 | 0 |
| entropy_source.sampled_data_regs | 64 | 0 | 0 |
| entropy_source.sample_ro | 27 | 2 | 3 |
| fifo_generator | 241 | 195 | 151 |
| top_fsm_counters | 236 | 234 | 159 |
| uart_tx | 249 | 247 | 227 |

Interpretation update: the compact diagnostic is useful, but it is not a
non-invasive probe. Changing the top-level protocol/header and surrounding
logic leaves the explicitly constrained data RO and sampled-data registers in
place, yet substantially changes FIFO, UART, control FSM, and part of the
sample-RO implementation. The current mechanism should therefore be stated more
carefully: the reproducible formal restart failure is an implementation-state
effect of the complete entropy-source/readout boundary, not a simple imbalance
of the core RO/FIFO byte generator alone.
## Compact warmup11 and sample-RO locked causal test

Compact `warmup11, 1000 x 125` was built and captured to test whether the
compact top can reproduce the formal `warmup11` high-bias failure:

- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc.bin`
- capture SHA256:
  `6564D472A495F2344D79E99C3DB758163ABD656F81677977EC33031EF1A4E9AF`
- packed SHA256:
  `592761B2FCC4ACCE5AF191A4EEC1906B1CADFB07FE1412D31406A59C89046B6F`
- packed p1: `0.498148000`
- row ones std: `15.991625809`
- worst position: byte `90`, bit `6`, p1 `0.452000000`, x `548`

This means compact `warmup11` is also near ideal. The compact diagnostic masks
both formal `warmup4` low-bias and formal `warmup11` high-bias failures.

A sharper causal test was then run. A new XDC copied
`random1_sampler_regs_only_x45y31.xdc` and additionally locked the sample RO
LUTs to the routed LOC/BEL observed in the formal auto w4 retest:

- XDC:
  `data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_formal_auto_w4_locked.xdc`
- bitstream:
  `data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_sample_ro_formal_locked_warmup4_1000x125/RO_TRNG_restart_fifo_compact_diag_top.bit`
- capture:
  `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc.bin`
- capture SHA256:
  `1A79DC13BE9FC2596F4FB60255D50C96E5BE5D3A5EEE83A3B24A35FD3DC26428`
- packed p1: `0.376796000`
- worst position: byte `0`, bit `5`, p1 `0.195000000`, x `805`

This is the strongest mechanism result so far:

| design | sample RO | warmup | packed p1 | worst x | interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| formal auto retest | formal routed | 4 | `0.406735000` | `703` | low-bias fail |
| compact FIFO diag | compact routed | 4 | `0.498297000` | `555` | near ideal |
| compact FIFO diag | compact routed | 11 | `0.498148000` | `548` | near ideal |
| compact FIFO diag | formal-routed sample RO locked | 4 | `0.376796000` | `805` | low-bias fail restored |

Interpretation update: the compact top originally masked formal restart
failures because the sample-RO implementation changed. When the compact design
keeps the compact readout/control path but locks the sample RO back to the
formal auto physical implementation, the warmup4 low-bias failure returns.
Therefore the decisive boundary is sampler-side physical implementation, not
only FIFO/UART/readout scheduling. This directly supports the paper claim that
the sampler RO and its local placement/routing must be treated as part of the
physical entropy source boundary.
