# Restart-Capable RTL Plan 2026-05-14

## Goal

Build a separate restart-capable TRNG top so formal SP800-90B restart collection does not depend on reprogramming the FPGA for every row.

This should be a new experimental bitstream, not a silent mutation of the already-used baseline `RO_TRNG_top`.

## Current Constraints

- `rtl/RO_TRNG_top.v` always drives `entropy_source.en = 1'b1`.
- `fifo_generator_0` is instantiated without any explicit reset/clear control at the top level.
- `uart_tx` already has `rst_n`, so the TX side is restart-friendly.
- `uart_rx.v` already exists and can be reused for a command-triggered restart path.
- `entropy_source.v` already supports an `en` input, which is the key hook for a real entropy-source restart.

## Practical Architecture

New top suggestion:

- `rtl/RO_TRNG_restart_top.v`

Suggested behavior:

1. Idle state:
   RO enabled, FIFO writing disabled, UART TX idle.

2. Host sends one-byte restart command over UART RX.

3. Control FSM asserts an internal restart sequence:
   - disable RO (`ro_en = 0`)
   - hold restart for fixed `RESTART_HOLD_CYCLES`
   - clear internal byte packer state
   - clear sample-valid counters
   - reset/flush data path state

4. Release phase:
   - enable RO (`ro_en = 1`)
   - wait `SETTLE_CYCLES`
   - optionally discard `WARMUP_BITS`

5. Capture phase:
   - pack raw bits into UART bytes
   - emit exactly `N` bytes for one restart row
   - return to idle and wait for next restart command

## Why This Is Better

This changes restart cost from "launch Vivado and reconnect JTAG every row" to "send one byte over UART every row".

That would turn a projected `70-96` hour formal `1000x1000` run into something much closer to a serial-throughput-limited acquisition.

## Minimum Design Blocks

1. `uart_rx`
   Use existing `rtl/uart_rx.v`.

2. Restart FSM
   New small control block inside the new top or a helper module.

3. RO gate
   Drive `entropy_source.en` from FSM-controlled `ro_en`.

4. Bit-to-byte packer
   Current top relies on asynchronous FIFO width conversion. For restart control, a direct byte packer in the 200 MHz domain will be easier to reason about in the paper.

5. Optional FIFO simplification
   For restart experiments only, replacing the asynchronous FIFO path with a simpler controlled byte path may be cleaner than trying to prove FIFO reset semantics.

## Recommended First Implementation

Phase 1:

- New restart top.
- Use `entropy_source` directly.
- Synchronize `rand_clk` into `clk_200m` only through a simple bit-capture / handshake design if feasible.
- Use existing `uart_tx`.
- Add `uart_rx` command `0x52` (`'R'`) to trigger one restart-and-capture transaction.

Phase 2:

- Add exact byte-count framing for one row.
- Update capture script to use `-RestartMethod uart_command`.

## Script Impact

The next script upgrade would be:

- extend `scripts/capture_90b_restart_dataset.ps1`
- add restart mode `uart_command`
- per row:
  - open serial
  - send command byte
  - read exact row payload
  - append to row-major file

This would remove Vivado from the per-row loop.

## Risks

- Crossing from RO-derived clocking into a controlled restart FSM must be designed carefully.
- If we keep the current FIFO path, proving reset semantics is harder.
- If we simplify the datapath too much, we must clearly separate this restart bitstream from the original baseline bitstream in the paper.

## Recommended Scope

Do not rewrite the whole source.

Do this as a separate restart-only experimental top so:

- existing published/collected data stays untouched
- restart methodology becomes auditable
- risk is localized

