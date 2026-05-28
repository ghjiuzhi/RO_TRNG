# Auto-generated entropy route-lock replay.
# label=compact_w4_sampled_regs_and_data
# mode=sampled_data
# source_dcp=E:/Project/MLDSA/RO_TRNG/data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_warmup4_1000x125/checkpoints/RO_TRNG_restart_fifo_compact_diag_top_routed.dcp
# generated_by=scripts/vivado/export_entropy_route_lock_20260528.tcl
# Apply after phys_opt_design and before route_design.
set route_lock_applied 0
set route_lock_failed 0
set cell_lock_applied 0
set cell_lock_failed 0
puts "Applying entropy route lock: compact_w4_sampled_regs_and_data"

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[0]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[1]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y31 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[2]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[3]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[4]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[5]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y31 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[6]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[7]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y31 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[8]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[9]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y32 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[10]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[11]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[12]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[13]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y32 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[14]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[15]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y32 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[16]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[17]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y33 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[18]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[19]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[20]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[21]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y33 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[22]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[23]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y33 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[24]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[25]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y34 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[26]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[27]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[28]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[29]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y34 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[30]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[31]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y34 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[32]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[33]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y35 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[34]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[35]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[36]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[37]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y35 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[38]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[39]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y35 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[40]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[41]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y36 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[42]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[43]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[44]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[45]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y36 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[46]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[47]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y36 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[48]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[49]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y37 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[50]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[51]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[52]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[53]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y37 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[54]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[55]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y37 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg[56]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X45Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg[57]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X46Y38 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg[58]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X47Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg[59]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X48Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg[60]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X49Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg[61]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X50Y38 $c
    if {[catch {set_property BEL SLICEM.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg[62]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X51Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set cell_name {u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg[63]}
set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]
if {[llength $c] != 1} {
    incr cell_lock_failed
    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"
} else {
    set_property LOC SLICE_X52Y38 $c
    if {[catch {set_property BEL SLICEL.A5FF $c} msg]} {
        incr cell_lock_failed
        puts "CELL_LOCK_FAILED $cell_name $msg"
    } else {
        incr cell_lock_applied
        puts "CELL_LOCK_APPLIED $cell_name"
    }
}

set net_name {u_entropy_source/sampled_data[0]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX10 CLBLM_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[1]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX0 CLBLM_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[2]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX5 CLBLM_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[3]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX6 CLBLM_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[4]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[5]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[6]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[7]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[8]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[9]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SE2BEG2 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[10]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[11]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[12]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[13]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[14]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[15]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[16]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX25 CLBLM_L_B5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[17]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX16 CLBLM_L_B3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[18]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX13 CLBLM_L_B6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[19]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX14 CLBLM_L_B1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[20]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 WL1BEG1 IMUX26 CLBLM_L_B4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[21]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX19 CLBLM_L_B2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[22]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WW2BEG2 WR1BEG_S0 IMUX0 CLBLM_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[23]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW4BEG2 NL1BEG1 IMUX9 CLBLM_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[24]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 IMUX3 CLBLM_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[25]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX10 CLBLM_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[26]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 IMUX5 CLBLM_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[27]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WR1BEG3 IMUX6 CLBLM_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[28]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[29]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[30]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[31]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[32]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[33]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SE2BEG2 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[34]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[35]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[36]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[37]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[38]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[39]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WL1BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[40]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 EL1BEG0 IMUX_L1 CLBLL_LL_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[41]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 ER1BEG3 IMUX_L7 CLBLL_LL_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[42]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L2 CLBLL_LL_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[43]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 IMUX_L4 CLBLL_LL_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[44]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 SR1BEG3 IMUX_L8 CLBLL_LL_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[45]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WR1BEG3 WL1BEG1 IMUX_L11 CLBLL_LL_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[46]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 NW2BEG2 WR1BEG3 IMUX_L14 CLBLL_L_B1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[47]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WR1BEG_S0 IMUX_L16 CLBLL_L_B3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[48]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EE2BEG2 IMUX_L13 CLBLL_L_B6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[49]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 SR1BEG3 ER1BEG_S0 IMUX_L25 CLBLL_L_B5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[50]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L19 CLBLL_L_B2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[51]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L26 CLBLL_L_B4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[52]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[53]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[54]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 SR1BEG3 WW2BEG3 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[55]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WL1BEG1 WW2BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[56]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 EL1BEG1 SE2BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[57]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 ER1BEG3 SL1BEG3 SR1BEG_S0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[58]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 EL1BEG1 IMUX_L10 CLBLL_L_A4 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[59]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 FAN_ALT7 FAN_BOUNCE7 IMUX_L0 CLBLL_L_A3 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[60]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_L_AMUX CLBLL_LOGIC_OUTS16 IMUX_L5 CLBLL_L_A6 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[61]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_M_AMUX CLBLM_LOGIC_OUTS20 WW2BEG2 IMUX_L6 CLBLL_L_A1 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[62]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLM_L_AMUX CLBLM_LOGIC_OUTS16 WL1BEG1 WL1BEG0 IMUX_L9 CLBLL_L_A5 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}

set net_name {u_entropy_source/sampled_data[63]}
set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]
if {[llength $n] != 1} {
    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"
} else {
    set fixed_route { { CLBLL_LL_AMUX CLBLL_LOGIC_OUTS20 WW2BEG2 WL1BEG1 IMUX_L3 CLBLL_L_A2 }  }
    if {[catch {set_property FIXED_ROUTE $fixed_route $n} msg]} {
        incr route_lock_failed
        puts "ROUTE_LOCK_FAILED $net_name $msg"
    } else {
        catch {set_property IS_ROUTE_FIXED TRUE $n}
        incr route_lock_applied
        puts "ROUTE_LOCK_APPLIED $net_name"
    }
}
puts "Completed entropy route lock: compact_w4_sampled_regs_and_data"
puts "CELL_LOCK_SUMMARY applied=$cell_lock_applied failed=$cell_lock_failed"
puts "ROUTE_LOCK_SUMMARY applied=$route_lock_applied failed=$route_lock_failed"
