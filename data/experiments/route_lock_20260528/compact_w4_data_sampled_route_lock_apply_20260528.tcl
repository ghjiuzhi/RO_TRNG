# Auto-generated entropy route-lock replay.
# label=compact_w4_data_sampled
# source_dcp=E:/Project/MLDSA/RO_TRNG/data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_warmup4_1000x125/checkpoints/RO_TRNG_restart_fifo_compact_diag_top_routed.dcp
# generated_by=scripts/vivado/export_entropy_route_lock_20260528.tcl
# Apply after phys_opt_design and before route_design.
puts "Applying entropy route lock: compact_w4_data_sampled"

set net_name {u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_A CLBLL_LOGIC_OUTS12 NW2BEG0 EL1BEG_N3 IMUX_L15 CLBLL_LL_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_B  { CLBLL_LL_BMUX CLBLL_LOGIC_OUTS21 IMUX_L7 CLBLL_LL_A1 }  CLBLL_LOGIC_OUTS13 SE2BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { SL1BEG1 WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  WL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SW2BEG0 SE2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_B  { CLBLL_LL_BMUX CLBLL_LOGIC_OUTS21 IMUX_L7 CLBLL_LL_A1 }  CLBLL_LOGIC_OUTS13 SE2BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG1  { SL1BEG1 WL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  WL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SW2BEG0 SE2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_A CLBLL_LOGIC_OUTS12 NW2BEG0 EL1BEG_N3 IMUX_L15 CLBLL_LL_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_C CLBLL_LL_CMUX CLBLL_LOGIC_OUTS22 IMUX40 CLBLL_LL_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_D CLBLL_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX29 CLBLL_LL_C2 }  SS6BEG3 WW4BEG0  { SR1BEG_S0 BYP_ALT1 BYP1 CLBLM_M_AX }  NN2BEG0 SR1BEG_S0  { BYP_ALT1 BYP1 CLBLM_M_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }   { SL1BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }   { SL1BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_D CLBLL_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX29 CLBLL_LL_C2 }  SS6BEG3 WW4BEG0  { SR1BEG_S0 BYP_ALT1 BYP1 CLBLM_M_AX }  NN2BEG0 SR1BEG_S0  { BYP_ALT1 BYP1 CLBLM_M_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }   { SL1BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0  { BYP_ALT1 BYP1 CLBLM_M_AX }   { SL1BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  SS2BEG0 BYP_ALT1 BYP1 CLBLM_M_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_C CLBLL_LL_CMUX CLBLL_LOGIC_OUTS22 IMUX40 CLBLL_LL_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_A CLBLM_LOGIC_OUTS8 NL1BEG_N3 IMUX14 CLBLM_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_B CLBLM_L_BMUX CLBLM_LOGIC_OUTS17  { IMUX6 CLBLM_L_A1 }  SS6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 WW2BEG3  { BYP_ALT0 BYP0 CLBLM_L_AX }  SW2BEG3 ER1BEG_S0  { BYP_ALT0 BYP0 CLBLM_L_AX }  SL1BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }   { SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  SE2BEG0 SW2BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }   { SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  SS2BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }  SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_B CLBLM_L_BMUX CLBLM_LOGIC_OUTS17  { IMUX6 CLBLM_L_A1 }  SS6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 WW2BEG3  { BYP_ALT0 BYP0 CLBLM_L_AX }  SW2BEG3 ER1BEG_S0  { BYP_ALT0 BYP0 CLBLM_L_AX }  SL1BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }   { SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  SE2BEG0 SW2BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }   { SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  SS2BEG0  { BYP_ALT0 BYP0 CLBLM_L_AX }  SL1BEG0 BYP_ALT0 BYP0 CLBLM_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_A CLBLM_LOGIC_OUTS8 NL1BEG_N3 IMUX14 CLBLM_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_C CLBLM_M_CMUX CLBLM_LOGIC_OUTS22 IMUX40 CLBLM_M_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_D CLBLM_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX29 CLBLM_M_C2 }  SS6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3  { WL1BEG2 WL1BEG1 WL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  WW4BEG0  { ER1BEG_S0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SR1BEG_S0 SE2BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }   { SL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SE2BEG0 SW2BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_D CLBLM_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX29 CLBLM_M_C2 }  SS6BEG3 SW6BEG3 SW6BEG3 SW6BEG3 SW6BEG3  { WL1BEG2 WL1BEG1 WL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  WW4BEG0  { ER1BEG_S0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SR1BEG_S0 SE2BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }   { SL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SE2BEG0 SW2BEG0  { BYP_ALT1 BYP_L1 CLBLL_LL_AX }  SL1BEG0 BYP_ALT1 BYP_L1 CLBLL_LL_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_C CLBLM_M_CMUX CLBLM_LOGIC_OUTS22 IMUX40 CLBLM_M_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_A CLBLL_LOGIC_OUTS8 NL1BEG_N3 IMUX_L14 CLBLL_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_B CLBLL_L_BMUX CLBLL_LOGIC_OUTS17  { IMUX_L6 CLBLL_L_A1 }  SS2BEG3 SR1BEG_S0 SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }   { SS2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }   { SL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_B CLBLL_L_BMUX CLBLL_LOGIC_OUTS17  { IMUX_L6 CLBLL_L_A1 }  SS2BEG3 SR1BEG_S0 SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }   { SS2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }   { SL1BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLL_L_AX }  SS2BEG0 BYP_ALT0 BYP_L0 CLBLL_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_A CLBLL_LOGIC_OUTS8 NL1BEG_N3 IMUX_L14 CLBLL_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_C CLBLM_L_CMUX CLBLM_LOGIC_OUTS18 IMUX41 CLBLM_L_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_D CLBLM_LOGIC_OUTS11  { FAN_ALT1 FAN_BOUNCE1 IMUX20 CLBLM_L_C2 }  WW4BEG3 WW4BEG3  { WL1BEG1 NL1BEG1  { NR1BEG1 GFAN0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  BYP_ALT1 BYP_L1 CLBLM_M_AX }  WR1BEG_S0 SR1BEG_S0  { BYP_ALT1 BYP_L1 CLBLM_M_AX }  SS2BEG0  { NR1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }   { BYP_ALT1 BYP_L1 CLBLM_M_AX }  SR1BEG1  { FAN_ALT6 FAN_BOUNCE6 BYP_ALT1 BYP_L1 CLBLM_M_AX }  SE2BEG1  { WL1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  SL1BEG1 WL1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_D CLBLM_LOGIC_OUTS11  { FAN_ALT1 FAN_BOUNCE1 IMUX20 CLBLM_L_C2 }  WW4BEG3 WW4BEG3  { WL1BEG1 NL1BEG1  { NR1BEG1 GFAN0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  BYP_ALT1 BYP_L1 CLBLM_M_AX }  WR1BEG_S0 SR1BEG_S0  { BYP_ALT1 BYP_L1 CLBLM_M_AX }  SS2BEG0  { NR1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }   { BYP_ALT1 BYP_L1 CLBLM_M_AX }  SR1BEG1  { FAN_ALT6 FAN_BOUNCE6 BYP_ALT1 BYP_L1 CLBLM_M_AX }  SE2BEG1  { WL1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  SL1BEG1 WL1BEG0 BYP_ALT1 BYP_L1 CLBLM_M_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_C CLBLM_L_CMUX CLBLM_LOGIC_OUTS18 IMUX41 CLBLM_L_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_A CLBLL_LOGIC_OUTS12 NW2BEG0 EL1BEG_N3 IMUX_L15 CLBLL_LL_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_B CLBLL_LL_BMUX CLBLL_LOGIC_OUTS21  { IMUX_L7 CLBLL_LL_A1 }  SW6BEG3 SS6BEG3 SW6BEG3 SS6BEG3 SS6BEG3 WW2BEG3  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SW2BEG3  { ER1BEG_S0  { NR1BEG0 NR1BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG3 ER1BEG_S0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }   { SS2BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SE2BEG0 SW2BEG0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_B CLBLL_LL_BMUX CLBLL_LOGIC_OUTS21  { IMUX_L7 CLBLL_LL_A1 }  SW6BEG3 SS6BEG3 SW6BEG3 SS6BEG3 SS6BEG3 WW2BEG3  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SW2BEG3  { ER1BEG_S0  { NR1BEG0 NR1BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG3 ER1BEG_S0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }   { SS2BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SE2BEG0 SW2BEG0  { BYP_ALT0 BYP_L0 CLBLM_L_AX }  SL1BEG0 BYP_ALT0 BYP_L0 CLBLM_L_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_A CLBLL_LOGIC_OUTS12 NW2BEG0 EL1BEG_N3 IMUX_L15 CLBLL_LL_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_C CLBLM_M_CMUX CLBLM_LOGIC_OUTS22 IMUX_L40 CLBLM_M_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_D CLBLM_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX_L29 CLBLM_M_C2 }  EE2BEG3 SE6BEG3 SE6BEG3 SE6BEG3 SS6BEG3 SS6BEG3 ER1BEG_S0 SS2BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0 BYP_ALT1 BYP1 CLBLL_LL_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/in0[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_D CLBLM_LOGIC_OUTS15  { FAN_ALT3 FAN_BOUNCE3 IMUX_L29 CLBLM_M_C2 }  EE2BEG3 SE6BEG3 SE6BEG3 SE6BEG3 SS6BEG3 SS6BEG3 ER1BEG_S0 SS2BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0  { BYP_ALT1 BYP1 CLBLL_LL_AX }  SL1BEG0 BYP_ALT1 BYP1 CLBLL_LL_AX }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/out[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_C CLBLM_M_CMUX CLBLM_LOGIC_OUTS22 IMUX_L40 CLBLM_M_D1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX10 CLBLM_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[1]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX0 CLBLM_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[2]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX5 CLBLM_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[3]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX6 CLBLM_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[4]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[5]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[6]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[7]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[8]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[9]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SE2BEG2 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[10]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[11]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[12]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[13]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[14]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[15]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[16]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX25 CLBLM_L_B5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[17]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX16 CLBLM_L_B3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[18]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX13 CLBLM_L_B6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[19]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX14 CLBLM_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[20]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 WL1BEG1 IMUX26 CLBLM_L_B4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[21]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX19 CLBLM_L_B2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[22]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WW2BEG2 WR1BEG_S0 IMUX0 CLBLM_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[23]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW4BEG2 NL1BEG1 IMUX9 CLBLM_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[24]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX3 CLBLM_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[25]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX10 CLBLM_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[26]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX5 CLBLM_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[27]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX6 CLBLM_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[28]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[29]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[30]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[31]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[32]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[33]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SE2BEG2 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[34]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[35]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[36]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[37]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[38]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[39]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WL1BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[40]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 EL1BEG0 IMUX_L1 CLBLL_LL_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[41]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 ER1BEG3 IMUX_L7 CLBLL_LL_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[42]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L2 CLBLL_LL_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[43]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 IMUX_L4 CLBLL_LL_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[44]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 SR1BEG3 IMUX_L8 CLBLL_LL_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[45]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WR1BEG3 WL1BEG1 IMUX_L11 CLBLL_LL_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[46]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 NW2BEG2 WR1BEG3 IMUX_L14 CLBLL_L_B1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[47]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WR1BEG_S0 IMUX_L16 CLBLL_L_B3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[48]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EE2BEG2 IMUX_L13 CLBLL_L_B6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[49]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SR1BEG3 ER1BEG_S0 IMUX_L25 CLBLL_L_B5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[50]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L19 CLBLL_L_B2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[51]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L26 CLBLL_L_B4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[52]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[53]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[54]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 SR1BEG3 WW2BEG3 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[55]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[56]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[57]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 ER1BEG3 SL1BEG3 SR1BEG_S0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[58]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[59]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[60]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[61]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[62]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}

set net_name {u_entropy_source/sampled_data[63]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WL1BEG1 IMUX_L3 CLBLL_L_A2 }  }
    set_property FIXED_ROUTE $fixed_route $n
    catch {set_property IS_ROUTE_FIXED TRUE $n}
    puts "ROUTE_LOCK_APPLIED $net_name"
}
puts "Completed entropy route lock: compact_w4_data_sampled"
