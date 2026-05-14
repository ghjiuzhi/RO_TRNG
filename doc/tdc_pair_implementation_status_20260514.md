# Pair-specific TDC implementation status

Date: 2026-05-14

Scope: offline engineering preparation only. No hardware programming, no
COM/JTAG/hw_server access, and no Vivado run was performed.

## Added files

- `scripts/generate_tdc_ro_pair_from_matrix_xdc.py`
  - Reads a matrix RO placement XDC such as
    `data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc`.
  - Extracts two selected `u_entropy_source/RO_NUM_LOOP[i]` 2-stage RO
    placements.
  - Emits equivalent LOC/BEL constraints for TDC instances `u_ro_a` and
    `u_ro_b`.
  - Keeps comments with source XDC, family, pair id, pair indexes, stage count,
    and whether BEL constraints were copied.
- `rtl/tdc/RO_TDC_pair_sysclk_top.v`
  - Draft top with the same ports as `RO_TDC_sysclk_top`:
    `sys_clk`, `por_n_i`, `UART_TX_o`.
  - Reuses the existing clocking, reset, two `tdc_lane` instances,
    `tdc_uart_packetizer`, and `uart_tx`.
  - Preserves the constrained RO instance names `u_ro_a` and `u_ro_b`.
  - Defaults `RO_A_STAGES=2` and `RO_B_STAGES=2` to match the random1/random3
    data RO matrix.
- `scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl`
  - Still defaults to `RO_TDC_sysclk_top`.
  - Accepts an optional third Tcl argument for the top name, so a build-only
    session can target `RO_TDC_pair_sysclk_top` without editing the script.

## Generated first-round XDCs

The first offline XDC set has been generated under
`data/experiments/xdc_tdc_pairs/`:

- `tdc_pair_random1_ro4_ro5.xdc`
- `tdc_pair_random1_ro0_ro1.xdc`
- `tdc_pair_random1_ro2_ro4.xdc`
- `tdc_pair_random3_ro3_ro7.xdc`
- `tdc_pair_random3_ro3_ro5.xdc`
- `tdc_pair_random3_ro0_ro6.xdc`

## Example XDC generation

Generate the first priority pair manually with:

```powershell
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py `
  --matrix-xdc data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc `
  --pair 4,5 `
  --family random1 `
  --pair-id random1_ro4_ro5 `
  --out data\experiments\xdc_tdc_pairs\tdc_pair_random1_ro4_ro5.xdc
```

Recommended first offline XDC set from the validation plan:

```powershell
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc --pair 4,5 --family random1 --pair-id random1_ro4_ro5 --out data\experiments\xdc_tdc_pairs\tdc_pair_random1_ro4_ro5.xdc
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc --pair 0,1 --family random1 --pair-id random1_ro0_ro1 --out data\experiments\xdc_tdc_pairs\tdc_pair_random1_ro0_ro1.xdc
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc --pair 2,4 --family random1 --pair-id random1_ro2_ro4 --out data\experiments\xdc_tdc_pairs\tdc_pair_random1_ro2_ro4.xdc
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed3_x36y35.xdc --pair 3,7 --family random3 --pair-id random3_ro3_ro7 --out data\experiments\xdc_tdc_pairs\tdc_pair_random3_ro3_ro7.xdc
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed3_x36y35.xdc --pair 3,5 --family random3 --pair-id random3_ro3_ro5 --out data\experiments\xdc_tdc_pairs\tdc_pair_random3_ro3_ro5.xdc
python scripts\generate_tdc_ro_pair_from_matrix_xdc.py --matrix-xdc data\experiments\xdc_matrix\ro_random_seed3_x36y35.xdc --pair 0,6 --family random3 --pair-id random3_ro0_ro6 --out data\experiments\xdc_tdc_pairs\tdc_pair_random3_ro0_ro6.xdc
```

Review each generated file before build. It should constrain only `u_ro_a` and
`u_ro_b`, not `u_entropy_source`.

## Next build step

In a build-authorized session only, pass one generated pair XDC as the extra XDC
argument, choose a pair-specific output directory, and pass
`RO_TDC_pair_sysclk_top` as the third Tcl argument.

Example command shape:

```powershell
vivado -mode batch -source scripts\vivado\run_fpga1_tdc_sysclk_inmem.tcl -tclargs `
  data\experiments\xdc_tdc_pairs\tdc_pair_random1_ro4_ro5.xdc `
  data\vivado_runs\fpga1_tdc_pairs\random1_ro4_ro5 `
  RO_TDC_pair_sysclk_top
```

The build step must remain build-only: do not open hardware manager, do not
program a bitstream, and do not capture UART data in that session.

## Later capture and analysis

In a separate hardware-authorized session:

1. Program the selected pair bitstream only after build reports and generated
   XDC have been reviewed.
2. Capture UART binary data using the existing capture procedure.
3. Run `scripts/analyze_tdc_uart.py` on each capture.
4. Join TDC metrics with the RO_FREQ random1/random3 summary and TRNG family
   rows as described in `doc/tdc_pair_validation_plan_20260513.md`.

## Open risks

- The draft top has not been synthesized in this offline pass.
- The current build Tcl still defaults to `RO_TDC_sysclk_top`; the third Tcl
  argument must be supplied before the pair top is actually built.
- The generator assumes 2-stage matrix ROs using `RO_AND` plus
  `RO_STAGE_LOOP[0]`, matching the current random1/random3 XDC files.
- Copying BELs exactly preserves the original matrix intent, but final legality
  still must be checked by Vivado during build.
