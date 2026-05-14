# In-memory Vivado flow for a minimal UART TX self-test on fpga1.
# It verifies that sys_clk -> clk_wiz -> UART_TX_o(J15) -> USB-UART works.
# Run with:
#   vivado -mode batch -source scripts/vivado/run_fpga1_uart_selftest_inmem.tcl

set origin_dir [file normalize [file join [file dirname [info script]] ../..]]
set part_name xc7z020clg400-2
set top_name uart_selftest_sysclk_top

set fpga1_src_dir [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1]
set fpga1_ip_dir  [file join $fpga1_src_dir ip]
set fpga1_rtl_dir [file join $fpga1_src_dir imports rtl]
set debug_rtl_dir [file join $origin_dir rtl debug]
set xdc_dir       [file join $origin_dir fpga1 xc7z020clg400 lab_xdc]
set out_dir       [file join $origin_dir data vivado_runs fpga1_uart_selftest]

set ip_work_dir    [file join $out_dir ip_src]
set report_dir     [file join $out_dir reports]
set checkpoint_dir [file join $out_dir checkpoints]

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
cd $out_dir

set clk_xci [file join $fpga1_ip_dir clk_wiz_0 clk_wiz_0.xci]
set src_ip_dir [file dirname $clk_xci]
set dst_ip_dir [file join $ip_work_dir [file tail $src_ip_dir]]
copy_tree_contents $src_ip_dir $dst_ip_dir
set isolated_clk_xci [file join $dst_ip_dir [file tail $clk_xci]]

create_project fpga1_uart_selftest -in_memory -part $part_name
set_property target_language Verilog [current_project]
set_property simulator_language Mixed [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property ip_output_repo [file join $out_dir ip_user_files] [current_project]

read_verilog [list \
    [file join $fpga1_rtl_dir uart_tx.v] \
    [file join $debug_rtl_dir uart_selftest_sysclk_top.v] \
]
read_ip $isolated_clk_xci
generate_target all [get_ips]
synth_ip -force [get_ips]

read_xdc [file join $xdc_dir uart_selftest_pin.xdc]

update_compile_order -fileset sources_1

synth_design -top $top_name -part $part_name -flatten_hierarchy rebuilt
write_checkpoint -force [file join $checkpoint_dir ${top_name}_synth.dcp]
report_utilization -file [file join $report_dir synth_utilization.rpt]
report_timing_summary -file [file join $report_dir synth_timing_summary.rpt] -max_paths 20 -report_unconstrained

opt_design
place_design
phys_opt_design
route_design

write_checkpoint -force [file join $checkpoint_dir ${top_name}_routed.dcp]
report_route_status -file [file join $report_dir route_status.rpt]
report_drc -file [file join $report_dir routed_drc.rpt]
report_timing_summary -file [file join $report_dir routed_timing_summary.rpt] -max_paths 20 -report_unconstrained
write_bitstream -force [file join $out_dir ${top_name}.bit]

puts "FPGA1 UART self-test run completed."
puts "Output bitstream: [file join $out_dir ${top_name}.bit]"
