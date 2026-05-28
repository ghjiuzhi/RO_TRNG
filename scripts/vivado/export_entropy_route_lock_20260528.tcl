# Export a narrow post-physopt FIXED_ROUTE replay script from a routed restart DCP.
#
# This intentionally avoids global/control nets. The default net set is:
#   - data RO local loop nets: RO_NUM_LOOP[*] ... /in0* and /out*
#   - sampled data output nets: u_entropy_source/sampled_data[0..63]
#
# Usage:
#   vivado -mode batch -source scripts/vivado/export_entropy_route_lock_20260528.tcl \
#     -tclargs <source_routed.dcp> <out_apply.tcl> <label> ?mode?
#
# Modes:
#   data_sampled   data RO local loop nets plus sampled_data nets (default)
#   sampled_data   sampled_data nets plus sampled-register LOC/BEL locks
#   sampled_routes sampled_data nets only
#   data_ro        data RO local loop nets only

if {$argc < 3} {
    puts "Usage: vivado -mode batch -source scripts/vivado/export_entropy_route_lock_20260528.tcl -tclargs <source_routed.dcp> <out_apply.tcl> <label> ?mode?"
    exit 1
}

set dcp_file [file normalize [lindex $argv 0]]
set out_file [file normalize [lindex $argv 1]]
set label [lindex $argv 2]
set mode "data_sampled"
if {$argc >= 4} {
    set mode [lindex $argv 3]
}

proc route_lock_should_include_net {net_name mode} {
    if {[string first "<const" $net_name] >= 0} {
        return 0
    }
    set is_data_ro [regexp {u_entropy_source/RO_NUM_LOOP\[[0-9]+\]\..*/(in0|out)} $net_name]
    set is_sampled_data [regexp {u_entropy_source/sampled_data\[[0-9]+\]$} $net_name]
    if {$mode eq "data_sampled" && ($is_data_ro || $is_sampled_data)} {
        return 1
    }
    if {($mode eq "sampled_data" || $mode eq "sampled_routes") && $is_sampled_data} {
        return 1
    }
    if {$mode eq "data_ro" && $is_data_ro} {
        return 1
    }
    return 0
}

proc safe_prop {obj prop} {
    if {$obj eq ""} {
        return ""
    }
    if {[catch {set v [get_property $prop $obj]}]} {
        return ""
    }
    return $v
}

proc emit_route_lock {fp net_name route} {
    puts $fp ""
    puts $fp "set net_name [list $net_name]"
    puts $fp {set n [get_nets -quiet -hierarchical -filter [format {NAME == "%s"} $net_name]]}
    puts $fp "if {\[llength \$n\] != 1} \{"
    puts $fp {    puts "ROUTE_LOCK_SKIP net_not_unique_or_missing $net_name count=[llength $n]"}
    puts $fp "\} else \{"
    puts $fp "    set fixed_route [list $route]"
    puts $fp "    if {\[catch {set_property FIXED_ROUTE \$fixed_route \$n} msg\]} \{"
    puts $fp {        incr route_lock_failed}
    puts $fp {        puts "ROUTE_LOCK_FAILED $net_name $msg"}
    puts $fp "    \} else \{"
    puts $fp {        catch {set_property IS_ROUTE_FIXED TRUE $n}}
    puts $fp {        incr route_lock_applied}
    puts $fp {        puts "ROUTE_LOCK_APPLIED $net_name"}
    puts $fp "    \}"
    puts $fp "\}"
}

file mkdir [file dirname $out_file]
open_checkpoint $dcp_file

set selected_nets {}
foreach n [get_nets -hierarchical -quiet] {
    set net_name [get_property NAME $n]
    if {![route_lock_should_include_net $net_name $mode]} {
        continue
    }
    set route [safe_prop $n ROUTE]
    set status [safe_prop $n ROUTE_STATUS]
    if {$route eq "" || $status ne "ROUTED"} {
        continue
    }
    lappend selected_nets $n
}

set selected_cells {}
if {$mode eq "sampled_data" || $mode eq "data_sampled"} {
    foreach c [get_cells -hierarchical -quiet] {
        set cell_name [get_property NAME $c]
        if {[string first "u_entropy_source/SAMPLE_DATA_LINE_LOOP" $cell_name] >= 0 &&
            [string first "sampled_data_reg" $cell_name] >= 0} {
            lappend selected_cells $c
        }
    }
}

set fp [open $out_file w]
puts $fp "# Auto-generated entropy route-lock replay."
puts $fp "# label=$label"
puts $fp "# mode=$mode"
puts $fp "# source_dcp=$dcp_file"
puts $fp "# generated_by=scripts/vivado/export_entropy_route_lock_20260528.tcl"
puts $fp "# Apply after phys_opt_design and before route_design."
puts $fp "set route_lock_applied 0"
puts $fp "set route_lock_failed 0"
puts $fp "set cell_lock_applied 0"
puts $fp "set cell_lock_failed 0"
puts $fp "puts \"Applying entropy route lock: $label\""

foreach c [lsort -dictionary $selected_cells] {
    set cell_name [get_property NAME $c]
    set loc [safe_prop $c LOC]
    set bel [safe_prop $c BEL]
    puts $fp ""
    puts $fp "set cell_name [list $cell_name]"
    puts $fp {set c [get_cells -quiet -hierarchical -filter [format {NAME == "%s"} $cell_name]]}
    puts $fp "if {\[llength \$c\] != 1} \{"
    puts $fp {    incr cell_lock_failed}
    puts $fp {    puts "CELL_LOCK_FAILED cell_not_unique_or_missing $cell_name count=[llength $c]"}
    puts $fp "\} else \{"
    puts $fp "    set_property LOC [list $loc] \$c"
    puts $fp "    if {\[catch {set_property BEL [list $bel] \$c} msg\]} \{"
    puts $fp {        incr cell_lock_failed}
    puts $fp {        puts "CELL_LOCK_FAILED $cell_name $msg"}
    puts $fp "    \} else \{"
    puts $fp {        incr cell_lock_applied}
    puts $fp {        puts "CELL_LOCK_APPLIED $cell_name"}
    puts $fp "    \}"
    puts $fp "\}"
}

foreach n [lsort -dictionary $selected_nets] {
    emit_route_lock $fp [get_property NAME $n] [safe_prop $n ROUTE]
}

puts $fp "puts \"Completed entropy route lock: $label\""
puts $fp {puts "CELL_LOCK_SUMMARY applied=$cell_lock_applied failed=$cell_lock_failed"}
puts $fp {puts "ROUTE_LOCK_SUMMARY applied=$route_lock_applied failed=$route_lock_failed"}
close $fp

set summary_file "${out_file}.summary.txt"
set sfp [open $summary_file w]
puts $sfp "label=$label"
puts $sfp "mode=$mode"
puts $sfp "source_dcp=$dcp_file"
puts $sfp "out_file=$out_file"
puts $sfp "selected_cells=[llength $selected_cells]"
puts $sfp "selected_nets=[llength $selected_nets]"
close $sfp

close_design
puts "Wrote $out_file"
puts "Wrote $summary_file"
exit
