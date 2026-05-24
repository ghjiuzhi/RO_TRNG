# In-memory Vivado flow for a restart-capable auto-stream RO-TRNG bitstream.
# The programmed design auto-generates a row-major restart dataset after reset:
# one bitstream download, then UART emits RESTART_COUNT * ROW_BYTES raw bytes.
#
# Usage:
#   vivado -mode batch -source scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl \
#     -tclargs <placement_xdc> <out_dir> ?restart_count? ?row_bytes? ?hold_cycles? ?settle_cycles? ?warmup_bytes? ?start_delay_cycles? ?debug_header? ?top_name?

if {$argc < 2} {
    puts "Usage: vivado -mode batch -source scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl -tclargs <placement_xdc> <out_dir> ?restart_count? ?row_bytes? ?hold_cycles? ?settle_cycles? ?warmup_bytes? ?start_delay_cycles? ?debug_header? ?top_name?"
    exit 1
}

set origin_dir [file normalize [file join [file dirname [info script]] ../..]]
set part_name xc7z020clg400-2
set top_name RO_TRNG_restart_auto_top
set placement_xdc [file normalize [lindex $argv 0]]
set out_dir [file normalize [lindex $argv 1]]
set restart_count 1000
set row_bytes 1000
set hold_cycles 200000
set settle_cycles 200000
set warmup_bytes 0
set start_delay_cycles 0
set debug_header 0

if {$argc >= 3} {
    set restart_count [lindex $argv 2]
}
if {$argc >= 4} {
    set row_bytes [lindex $argv 3]
}
if {$argc >= 5} {
    set hold_cycles [lindex $argv 4]
}
if {$argc >= 6} {
    set settle_cycles [lindex $argv 5]
}
if {$argc >= 7} {
    set warmup_bytes [lindex $argv 6]
}
if {$argc >= 8} {
    set start_delay_cycles [lindex $argv 7]
}
if {$argc >= 9} {
    set debug_header [lindex $argv 8]
}
if {$argc >= 10} {
    set top_name [lindex $argv 9]
}

set fpga1_src_dir [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1]
set fpga1_ip_dir  [file join $fpga1_src_dir ip]
set rtl_dir       [file join $origin_dir rtl]
set restart_rtl_dir [file join $rtl_dir restart]
set base_xdc      [file join $origin_dir data experiments xdc_restart restart_sysclk_base.xdc]
set ip_work_dir    [file join $out_dir ip_src]
set report_dir     [file join $out_dir reports]
set checkpoint_dir [file join $out_dir checkpoints]
set shared_generated_ip_dir [file join $origin_dir data vivado_runs xc7z020clg400.gen sources_1 ip]
set fallback_generated_ip_dir [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.gen sources_1 ip]

proc require_file {label path} {
    if {![file exists $path]} {
        error "Missing $label: $path"
    }
    return $path
}

proc copy_tree_contents {src_dir dst_dir} {
    file mkdir $dst_dir
    foreach item [glob -nocomplain -directory $src_dir *] {
        set dst [file join $dst_dir [file tail $item]]
        if {[file isdirectory $item]} {
            copy_tree_contents $item $dst
        } else {
            file copy -force $item $dst
        }
    }
}

proc seed_ip_dcp_if_missing {ip_name shared_ip_dir fallback_ip_dir} {
    set expected_dcp [file join $shared_ip_dir $ip_name ${ip_name}.dcp]
    set fallback_dcp [file join $fallback_ip_dir $ip_name ${ip_name}.dcp]
    if {![file exists $expected_dcp] && [file exists $fallback_dcp]} {
        file mkdir [file dirname $expected_dcp]
        file copy -force $fallback_dcp $expected_dcp
        puts "Seeded missing IP DCP from fpga1 generated output: $expected_dcp"
    }
    return [file exists $expected_dcp]
}

require_file "placement XDC" $placement_xdc
require_file "base XDC" $base_xdc

file mkdir $out_dir
file mkdir $ip_work_dir
file mkdir $report_dir
file mkdir $checkpoint_dir
cd $out_dir

set restart_rtl_files [lsort [glob -nocomplain -types f -directory $restart_rtl_dir *.v]]
if {[llength $restart_rtl_files] == 0} {
    error "No restart RTL files found in $restart_rtl_dir"
}

set rtl_files [concat [list \
    [require_file "LUT6_and2_1" [file join $rtl_dir LUT6_and2_1.v]] \
    [require_file "LUT6_nand2_1" [file join $rtl_dir LUT6_nand2_1.v]] \
    [require_file "LUT6_not1" [file join $rtl_dir LUT6_not1.v]] \
    [require_file "entropy_source" [file join $rtl_dir entropy_source.v]] \
    [require_file "uart_tx" [file join $rtl_dir uart_tx.v]] \
] $restart_rtl_files]

set fpga1_ip_files [list \
    [require_file "clk_wiz_0 XCI" [file join $fpga1_ip_dir clk_wiz_0 clk_wiz_0.xci]] \
    [require_file "proc_sys_reset_0 XCI" [file join $fpga1_ip_dir proc_sys_reset_0 proc_sys_reset_0.xci]] \
    [require_file "fifo_generator_0 XCI" [file join $fpga1_ip_dir fifo_generator_0 fifo_generator_0.xci]] \
]

set isolated_ip_files [list]
foreach xci $fpga1_ip_files {
    set src_ip_dir [file dirname $xci]
    set dst_ip_dir [file join $ip_work_dir [file tail $src_ip_dir]]
    copy_tree_contents $src_ip_dir $dst_ip_dir
    lappend isolated_ip_files [file join $dst_ip_dir [file tail $xci]]
}

create_project fpga1_ro_trng_restart_auto_inmem -in_memory -part $part_name
set_property target_language Verilog [current_project]
set_property simulator_language Mixed [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property ip_output_repo [file join $out_dir ip_user_files] [current_project]

puts "Reading restart auto-stream RTL:"
foreach f $rtl_files {
    puts "  $f"
}
read_verilog $rtl_files

puts "Reading isolated IP XCI copies:"
foreach f $isolated_ip_files {
    puts "  $f"
}
read_ip $isolated_ip_files
generate_target all [get_ips]
set ips_to_synth [list]
foreach ip_name [list clk_wiz_0 proc_sys_reset_0 fifo_generator_0] {
    if {[seed_ip_dcp_if_missing $ip_name $shared_generated_ip_dir $fallback_generated_ip_dir]} {
        puts "Using available IP DCP: [file join $shared_generated_ip_dir $ip_name ${ip_name}.dcp]"
    } else {
        lappend ips_to_synth [get_ips $ip_name]
    }
}
if {[llength $ips_to_synth] > 0} {
    synth_ip -force $ips_to_synth
    foreach ip_name [list clk_wiz_0 proc_sys_reset_0 fifo_generator_0] {
        seed_ip_dcp_if_missing $ip_name $shared_generated_ip_dir $fallback_generated_ip_dir
    }
}

read_xdc $base_xdc
read_xdc $placement_xdc
update_compile_order -fileset sources_1

set synth_generics [list \
    RESTART_COUNT=$restart_count \
    ROW_BYTES=$row_bytes \
    HOLD_CYCLES=$hold_cycles \
    SETTLE_CYCLES=$settle_cycles \
    START_DELAY_CYCLES=$start_delay_cycles \
    DEBUG_HEADER=$debug_header \
    WARMUP_BYTES=$warmup_bytes \
]
puts "Synth generics: $synth_generics"
synth_design -top $top_name -part $part_name -flatten_hierarchy rebuilt -generic $synth_generics
write_checkpoint -force [file join $checkpoint_dir ${top_name}_synth.dcp]
report_utilization -file [file join $report_dir synth_utilization.rpt]
report_timing_summary -file [file join $report_dir synth_timing_summary.rpt] \
    -max_paths 20 -report_unconstrained

opt_design
write_checkpoint -force [file join $checkpoint_dir ${top_name}_opt.dcp]
report_drc -file [file join $report_dir opt_drc.rpt]

place_design
write_checkpoint -force [file join $checkpoint_dir ${top_name}_placed.dcp]
report_utilization -file [file join $report_dir placed_utilization.rpt]
report_timing_summary -file [file join $report_dir placed_timing_summary.rpt] \
    -max_paths 20 -report_unconstrained

phys_opt_design
write_checkpoint -force [file join $checkpoint_dir ${top_name}_physopt.dcp]

route_design
write_checkpoint -force [file join $checkpoint_dir ${top_name}_routed.dcp]
report_route_status -file [file join $report_dir route_status.rpt]
report_drc -file [file join $report_dir routed_drc.rpt]
report_utilization -file [file join $report_dir routed_utilization.rpt]
report_timing_summary -file [file join $report_dir routed_timing_summary.rpt] \
    -max_paths 20 -report_unconstrained
report_power -file [file join $report_dir routed_power.rpt]

write_bitstream -force [file join $out_dir ${top_name}.bit]

set manifest [open [file join $out_dir manifest.txt] w]
puts $manifest "top=$top_name"
puts $manifest "part=$part_name"
puts $manifest "placement_xdc=$placement_xdc"
puts $manifest "restart_count=$restart_count"
puts $manifest "row_bytes=$row_bytes"
puts $manifest "hold_cycles=$hold_cycles"
puts $manifest "settle_cycles=$settle_cycles"
puts $manifest "warmup_bytes=$warmup_bytes"
puts $manifest "start_delay_cycles=$start_delay_cycles"
puts $manifest "debug_header=$debug_header"
puts $manifest "vivado_version=[version -short]"
puts $manifest "note=build-only flow; one programming event, then UART emits a row-major restart dataset"
close $manifest

puts "Restart auto-stream build completed."
puts "Output bitstream: [file join $out_dir ${top_name}.bit]"
