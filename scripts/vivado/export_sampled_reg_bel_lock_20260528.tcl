# Export sampled-data register LOC/BEL constraints from a routed restart DCP.
#
# Usage:
#   vivado -mode batch -source scripts/vivado/export_sampled_reg_bel_lock_20260528.tcl \
#     -tclargs <source_routed.dcp> <out.xdc> <label>

if {$argc < 3} {
    puts "Usage: vivado -mode batch -source scripts/vivado/export_sampled_reg_bel_lock_20260528.tcl -tclargs <source_routed.dcp> <out.xdc> <label>"
    exit 1
}

set dcp_file [file normalize [lindex $argv 0]]
set out_file [file normalize [lindex $argv 1]]
set label [lindex $argv 2]

proc safe_prop {obj prop} {
    if {$obj eq ""} {
        return ""
    }
    if {[catch {set v [get_property $prop $obj]}]} {
        return ""
    }
    return $v
}

file mkdir [file dirname $out_file]
open_checkpoint $dcp_file

set cells {}
foreach c [get_cells -hierarchical -quiet] {
    set cell_name [get_property NAME $c]
    if {[string first "u_entropy_source/SAMPLE_DATA_LINE_LOOP" $cell_name] >= 0 &&
        [string first "sampled_data_reg" $cell_name] >= 0} {
        lappend cells $c
    }
}

set fp [open $out_file w]
puts $fp "################################################################"
puts $fp "# Auto-generated sampled-register BEL lock"
puts $fp "# label=$label"
puts $fp "# source_dcp=$dcp_file"
puts $fp "# generated_by=scripts/vivado/export_sampled_reg_bel_lock_20260528.tcl"
puts $fp "################################################################"

foreach c [lsort -dictionary $cells] {
    set name [get_property NAME $c]
    set loc [safe_prop $c LOC]
    set bel [safe_prop $c BEL]
    puts $fp ""
    puts $fp "set sampled_reg \[get_cells -hierarchical -filter {NAME == \"$name\"}\]"
    puts $fp "if {\[llength \$sampled_reg\] != 1} { error \"sampled_reg selector failed for $name count=\[llength \$sampled_reg\]\" }"
    puts $fp "set_property BEL [list $bel] \$sampled_reg"
    puts $fp "set_property LOC [list $loc] \$sampled_reg"
}
close $fp

set summary_file "${out_file}.summary.txt"
set sfp [open $summary_file w]
puts $sfp "label=$label"
puts $sfp "source_dcp=$dcp_file"
puts $sfp "out_file=$out_file"
puts $sfp "selected_cells=[llength $cells]"
close $sfp

close_design
puts "Wrote $out_file"
puts "Wrote $summary_file"
exit
