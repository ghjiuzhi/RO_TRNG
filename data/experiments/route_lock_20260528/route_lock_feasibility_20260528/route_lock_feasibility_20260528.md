# Route-Lock Feasibility Gate 20260528

This is an offline gate for partial route-lock attempts. A build should not be programmed unless the gate says READY_FOR_HARDWARE. The current threshold is applied_ratio >= 0.88, zero route/cell failures, clean route status, and a bitstream.

| run | selected_nets | route_lock_applied | route_lock_failed | route_lock_skipped | applied_ratio | has_bitstream | hardware_gate | gate_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| restart_fifo_compact_diag_scompact_w4_data_sampled_fixed_route_1000x125 | 96 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | no_bitstream |
| restart_fifo_compact_diag_scompact_w4_sampled_bel_routes_fixed_1000x125 | 64 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | no_bitstream |
| restart_fifo_compact_diag_scompact_w4_sampled_bel_routes_fixed_v2_1000x125 | 64 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | no_bitstream |
| restart_fifo_compact_diag_scompact_w4_sampled_data_fixed_route_1000x125 | 64 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | no_bitstream |
| restart_fifo_compact_diag_scompact_w4_sampled_regs_data_fixed_route_1000x125 | 64 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | no_bitstream |
| sampled_regs_data_on_existing_physopt | 64 | 0 | 0 | 0 | 0.000000 | False | DO_NOT_PROGRAM | probe_source_failed |
| sampled_routes_only_on_existing_physopt | 64 | 17 | 47 | 0 | 0.265625 | False | DO_NOT_PROGRAM | insufficient_route_lock_coverage |
