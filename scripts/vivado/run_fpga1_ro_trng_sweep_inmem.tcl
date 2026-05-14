if {$argc < 2} {
    puts "Usage: vivado -mode batch -source scripts/vivado/run_fpga1_ro_trng_sweep_inmem.tcl -tclargs <placement_xdc> <outdir> ?seed?"
    exit 1
}

set origin_dir [file normalize [file join [file dirname [info script]] ../..]]
set placement_xdc [file normalize [lindex $argv 0]]
set outdir [file normalize [lindex $argv 1]]
set seed 1
if {$argc >= 3} {
    set seed [lindex $argv 2]
}

set part xc7z020clg400-2
file mkdir $outdir

create_project -in_memory -part $part
set_property target_language Verilog [current_project]

read_verilog [list \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl LUT6_and2_1.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl LUT6_nand2_1.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl LUT6_not1.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl LUT6_buf1.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl entropy_source.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl uart_tx.v] \
    [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 imports rtl RO_TRNG_top.v] \
]

read_ip [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 ip clk_wiz_0 clk_wiz_0.xci]
read_ip [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 ip fifo_generator_0 fifo_generator_0.xci]
read_ip [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs sources_1 ip proc_sys_reset_0 proc_sys_reset_0.xci]

synth_design -top RO_TRNG_top -part $part

read_xdc [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs constrs_1 new pin.xdc]
read_xdc [file join $origin_dir fpga1 xc7z020clg400 xc7z020clg400.srcs constrs_1 imports new timing.xdc]
read_xdc $placement_xdc

opt_design
place_design
phys_opt_design
route_design

report_io -file [file join $outdir io.rpt]
report_utilization -file [file join $outdir utilization.rpt]
report_timing_summary -max_paths 20 -report_unconstrained -file [file join $outdir timing_summary.rpt]
report_route_status -file [file join $outdir route_status.rpt]
report_drc -file [file join $outdir drc.rpt]
report_methodology -file [file join $outdir methodology.rpt]
report_clock_utilization -file [file join $outdir clock_utilization.rpt]
write_checkpoint -force [file join $outdir RO_TRNG_top_routed.dcp]
write_bitstream -force [file join $outdir RO_TRNG_top.bit]

set manifest [open [file join $outdir manifest.txt] w]
puts $manifest "top=RO_TRNG_top"
puts $manifest "part=$part"
puts $manifest "placement_xdc=$placement_xdc"
puts $manifest "seed=$seed"
puts $manifest "vivado_version=[version -short]"
puts $manifest "rtl_source=fpga1 imported single-ended sys_clk sources"
close $manifest

puts "RO_TRNG sweep build complete: $outdir"
