set origin_dir [file normalize [file join [file dirname [info script]] ../..]]
set src_project [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.xpr]
set lab_root [file join $origin_dir data vivado_runs fpga1_tdc_sysclk]
set lab_project_dir [file join $lab_root project]
set report_dir [file join $lab_root reports]
file mkdir $lab_root
file mkdir $report_dir

open_project $src_project
save_project_as fpga1_tdc_sysclk $lab_project_dir -force
close_project

open_project [file join $lab_project_dir fpga1_tdc_sysclk.xpr]

set tdc_files [list \
    [file join $origin_dir rtl tdc carry4_tdc_chain.v] \
    [file join $origin_dir rtl tdc tdc_sampler.v] \
    [file join $origin_dir rtl tdc tdc_bubble_correct.v] \
    [file join $origin_dir rtl tdc tdc_encoder.v] \
    [file join $origin_dir rtl tdc tdc_lane.v] \
    [file join $origin_dir rtl tdc tdc_uart_packetizer.v] \
    [file join $origin_dir rtl tdc RO_TDC_sysclk_top.v] \
]
foreach f $tdc_files {
    if {[lsearch -exact [get_files -quiet $f] $f] < 0} {
        add_files -fileset sources_1 $f
    }
}

set constr_name constrs_tdc_sysclk
if {[llength [get_filesets -quiet $constr_name]] == 0} {
    create_fileset -constrset $constr_name
}
add_files -fileset $constr_name -quiet [file join $origin_dir fpga1 xc7z020clg400 lab_xdc tdc_sysclk_pin.xdc]
add_files -fileset $constr_name -quiet [file join $origin_dir fpga1 xc7z020clg400 lab_xdc tdc_sysclk_timing.xdc]
set_property target_constrs_file [file join $origin_dir fpga1 xc7z020clg400 lab_xdc tdc_sysclk_pin.xdc] [get_filesets $constr_name]
current_fileset -constrset [get_filesets $constr_name]

set_property top RO_TDC_sysclk_top [current_fileset]
update_compile_order -fileset sources_1

set synth_run synth_tdc_sysclk
set impl_run impl_tdc_sysclk
if {[llength [get_runs -quiet $synth_run]] == 0} {
    create_run $synth_run -flow {Vivado Synthesis 2023} -strategy {Vivado Synthesis Defaults} -constrset $constr_name
}
set_property top RO_TDC_sysclk_top [get_runs $synth_run]
if {[llength [get_runs -quiet $impl_run]] == 0} {
    create_run $impl_run -parent_run $synth_run -flow {Vivado Implementation 2023} -strategy {Vivado Implementation Defaults} -constrset $constr_name
}

reset_run $synth_run
launch_runs $synth_run -jobs 4
wait_on_run $synth_run
open_run $synth_run
report_utilization -file [file join $report_dir synth_utilization.rpt]
report_timing_summary -file [file join $report_dir synth_timing_summary.rpt] -max_paths 20 -report_unconstrained
close_design

reset_run $impl_run
launch_runs $impl_run -to_step write_bitstream -jobs 4
wait_on_run $impl_run
open_run $impl_run
report_utilization -file [file join $report_dir implemented_utilization.rpt]
report_timing_summary -file [file join $report_dir implemented_timing_summary.rpt] -max_paths 20 -report_unconstrained
report_drc -file [file join $report_dir implemented_drc.rpt]
report_route_status -file [file join $report_dir route_status.rpt]
write_checkpoint -force [file join $lab_root RO_TDC_sysclk_top_routed.dcp]
write_bitstream -force [file join $lab_root RO_TDC_sysclk_top.bit]

puts "FPGA1 TDC sysclk run completed."
puts "Output directory: $lab_root"
