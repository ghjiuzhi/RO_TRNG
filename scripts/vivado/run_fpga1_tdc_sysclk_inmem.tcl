# In-memory Vivado flow for the fpga1 Navigator V2 single-ended sys_clk TDC build.
# Run with:
#   vivado -mode batch -source scripts/vivado/run_fpga1_tdc_sysclk_inmem.tcl
# Optional tclargs:
#   1: extra placement XDC
#   2: output directory
#   3: top module name, default RO_TDC_sysclk_top

set origin_dir [file normalize [file join [file dirname [info script]] ../..]]
set part_name xc7z020clg400-2
set top_name RO_TDC_sysclk_top
set extra_xdc ""

set fpga1_src_dir [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1]
set fpga1_rtl_dir [file join $fpga1_src_dir imports rtl]
set fpga1_ip_dir  [file join $fpga1_src_dir ip]
set tdc_rtl_dir   [file join $origin_dir rtl tdc]
set xdc_dir       [file join $origin_dir fpga1 xc7z020clg400 lab_xdc]

set out_dir        [file join $origin_dir data vivado_runs fpga1_tdc_sysclk_inmem]
if {$argc >= 1} {
    set extra_xdc [file normalize [lindex $argv 0]]
}
if {$argc >= 2} {
    set out_dir [file normalize [lindex $argv 1]]
}
if {$argc >= 3} {
    set top_name [lindex $argv 2]
}
set ip_work_dir    [file join $out_dir ip_src]
set report_dir     [file join $out_dir reports]
set checkpoint_dir [file join $out_dir checkpoints]

proc require_nonempty {label paths} {
    if {[llength $paths] == 0} {
        error "No files found for $label"
    }
    foreach f $paths {
        if {![file exists $f]} {
            error "Missing $label file: $f"
        }
    }
    return [lsort $paths]
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

file mkdir $out_dir
file mkdir $ip_work_dir
file mkdir $report_dir
file mkdir $checkpoint_dir

# Keep Vivado-generated transient files under this isolated run tree.
cd $out_dir

set fpga1_rtl_files [require_nonempty "fpga1 imported RTL" \
    [glob -nocomplain -types f -directory $fpga1_rtl_dir *.v]]
set tdc_rtl_files [require_nonempty "TDC RTL" \
    [glob -nocomplain -types f -directory $tdc_rtl_dir *.v]]
set fpga1_ip_files [require_nonempty "fpga1 imported IP" [list \
    [file join $fpga1_ip_dir clk_wiz_0 clk_wiz_0.xci] \
    [file join $fpga1_ip_dir proc_sys_reset_0 proc_sys_reset_0.xci] \
]]
set xdc_files [require_nonempty "TDC sys_clk XDC" \
    [glob -nocomplain -types f -directory $xdc_dir tdc_sysclk_*.xdc]]

set isolated_ip_files [list]
foreach xci $fpga1_ip_files {
    set src_ip_dir [file dirname $xci]
    set dst_ip_dir [file join $ip_work_dir [file tail $src_ip_dir]]
    copy_tree_contents $src_ip_dir $dst_ip_dir
    lappend isolated_ip_files [file join $dst_ip_dir [file tail $xci]]
}
set isolated_ip_files [lsort $isolated_ip_files]

create_project fpga1_tdc_sysclk_inmem -in_memory -part $part_name
set_property target_language Verilog [current_project]
set_property simulator_language Mixed [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property ip_output_repo [file join $out_dir ip_user_files] [current_project]

puts "Reading fpga1 imported RTL:"
foreach f $fpga1_rtl_files {
    puts "  $f"
}
read_verilog $fpga1_rtl_files

puts "Reading TDC RTL:"
foreach f $tdc_rtl_files {
    puts "  $f"
}
read_verilog $tdc_rtl_files

puts "Reading isolated fpga1 IP XCI copies:"
foreach f $isolated_ip_files {
    puts "  $f"
}
read_ip $isolated_ip_files
generate_target all [get_ips]
synth_ip -force [get_ips]

puts "Reading TDC sys_clk XDC:"
foreach f $xdc_files {
    puts "  $f"
}
read_xdc $xdc_files
if {$extra_xdc ne ""} {
    if {![file exists $extra_xdc]} {
        error "Missing extra TDC placement XDC: $extra_xdc"
    }
    puts "Reading extra TDC placement XDC: $extra_xdc"
    read_xdc $extra_xdc
}

update_compile_order -fileset sources_1

synth_design -top $top_name -part $part_name -flatten_hierarchy rebuilt
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

puts "FPGA1 TDC sys_clk in-memory run completed."
puts "Output directory: $out_dir"
