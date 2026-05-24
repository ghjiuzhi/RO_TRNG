proc dump_cells {dcp out_csv} {
  open_checkpoint $dcp
  set fp [open $out_csv w]
  puts $fp "name,ref_name,loc,bel"
  foreach c [lsort [get_cells -hierarchical]] {
    set n [get_property NAME $c]
    if {[string match "*u_entropy_source*" $n] || [string match "*u_fifo_generator_0*" $n] || [string match "*u_uart_tx*" $n] || [string match "*state*" $n] || [string match "*send_count*" $n] || [string match "*row_index*" $n] || [string match "*warmup_count*" $n] || [string match "*header_index*" $n]} {
      set ref [get_property REF_NAME $c]
      set loc [get_property LOC $c]
      set bel [get_property BEL $c]
      regsub -all {,} $n {;} n2
      puts $fp "$n2,$ref,$loc,$bel"
    }
  }
  close $fp
  close_design
}
dump_cells {data/vivado_runs/restart_auto_retest_random1_regs_only_warmup4_1000x125_20260524/checkpoints/RO_TRNG_restart_auto_top_routed.dcp} {data/experiments/restart_fifo_diag_20260524/formal_auto_w4_retest_routed_cells.csv}
dump_cells {data/vivado_runs/restart_fifo_compact_diag_random1_regs_only_warmup4_1000x125/checkpoints/RO_TRNG_restart_fifo_compact_diag_top_routed.dcp} {data/experiments/restart_fifo_diag_20260524/compact_w4_routed_cells.csv}
exit
