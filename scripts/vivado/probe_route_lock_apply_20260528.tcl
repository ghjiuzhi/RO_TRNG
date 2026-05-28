# Probe a generated route-lock Tcl against an existing checkpoint.
#
# This is an offline feasibility check. It opens a checkpoint, sources the
# generated route-lock script, writes a post-apply checkpoint, and exits without
# route_design or bitstream generation.
#
# Usage:
#   vivado -mode batch -source scripts/vivado/probe_route_lock_apply_20260528.tcl \
#     -tclargs <physopt.dcp> <apply_route_lock.tcl> <out_dir> <label>

if {$argc < 4} {
    puts "Usage: vivado -mode batch -source scripts/vivado/probe_route_lock_apply_20260528.tcl -tclargs <physopt.dcp> <apply_route_lock.tcl> <out_dir> <label>"
    exit 1
}

set dcp_file [file normalize [lindex $argv 0]]
set apply_tcl [file normalize [lindex $argv 1]]
set out_dir [file normalize [lindex $argv 2]]
set label [lindex $argv 3]

if {![file exists $dcp_file]} {
    error "Checkpoint not found: $dcp_file"
}
if {![file exists $apply_tcl]} {
    error "Apply Tcl not found: $apply_tcl"
}

file mkdir $out_dir
open_checkpoint $dcp_file

set cell_lock_applied 0
set cell_lock_failed 0
set route_lock_applied 0
set route_lock_failed 0

puts "ROUTE_LOCK_PROBE label=$label"
puts "ROUTE_LOCK_PROBE dcp=$dcp_file"
puts "ROUTE_LOCK_PROBE apply_tcl=$apply_tcl"

if {[catch {source $apply_tcl} msg opts]} {
    puts "ROUTE_LOCK_PROBE_SOURCE_FAILED $msg"
    set fp [open [file join $out_dir "${label}_probe_summary.txt"] w]
    puts $fp "label=$label"
    puts $fp "dcp=$dcp_file"
    puts $fp "apply_tcl=$apply_tcl"
    puts $fp "source_status=failed"
    puts $fp "source_error=$msg"
    puts $fp "cell_lock_applied=$cell_lock_applied"
    puts $fp "cell_lock_failed=$cell_lock_failed"
    puts $fp "route_lock_applied=$route_lock_applied"
    puts $fp "route_lock_failed=$route_lock_failed"
    close $fp
    close_design
    exit 2
}

set fixed_route_nets [get_nets -quiet -hierarchical -filter {IS_ROUTE_FIXED == TRUE}]
set fixed_cells [get_cells -quiet -hierarchical -filter {IS_BEL_FIXED == TRUE || IS_LOC_FIXED == TRUE}]

write_checkpoint -force [file join $out_dir "${label}_post_apply.dcp"]

set fp [open [file join $out_dir "${label}_probe_summary.txt"] w]
puts $fp "label=$label"
puts $fp "dcp=$dcp_file"
puts $fp "apply_tcl=$apply_tcl"
puts $fp "source_status=ok"
puts $fp "cell_lock_applied=$cell_lock_applied"
puts $fp "cell_lock_failed=$cell_lock_failed"
puts $fp "route_lock_applied=$route_lock_applied"
puts $fp "route_lock_failed=$route_lock_failed"
puts $fp "fixed_route_nets=[llength $fixed_route_nets]"
puts $fp "fixed_cells=[llength $fixed_cells]"
close $fp

puts "ROUTE_LOCK_PROBE_SUMMARY cell_applied=$cell_lock_applied cell_failed=$cell_lock_failed route_applied=$route_lock_applied route_failed=$route_lock_failed fixed_route_nets=[llength $fixed_route_nets] fixed_cells=[llength $fixed_cells]"

close_design
exit 0
