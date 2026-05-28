if {$argc < 2} {
    puts "Usage: vivado -mode batch -source scripts/vivado/probe_net_delay_command_20260528.tcl -tclargs <routed.dcp> <out.txt>"
    exit 1
}

set dcp [file normalize [lindex $argv 0]]
set out [file normalize [lindex $argv 1]]

open_checkpoint $dcp
set fp [open $out w]

set sample_cells {}
foreach c [get_cells -hierarchical -quiet -filter {NAME =~ *u_entropy_source*}] {
    set cname [get_property NAME $c]
    if {([string first "u_entropy_source/RO_SAMPLE_NAND." $cname] >= 0 ||
         [string first "u_entropy_source/RO_SAMPLE_LOOP" $cname] >= 0) &&
        [string match "*/u_LUT6" $cname]} {
        lappend sample_cells $c
    }
}

puts $fp "sample_cells=[llength $sample_cells]"
set probe_net ""
foreach c $sample_cells {
    set pins [get_pins -quiet -of_objects $c -filter {REF_PIN_NAME == O}]
    foreach p $pins {
        set nets [get_nets -quiet -of_objects $p]
        if {[llength $nets] > 0} {
            set probe_net [lindex $nets 0]
            break
        }
    }
    if {$probe_net ne ""} {
        break
    }
}

if {$probe_net ne ""} {
    puts $fp "probe_net=[get_property NAME $probe_net]"
    puts $fp "net_properties=[list_property $probe_net]"
    if {[catch {set nd [get_net_delays -of_objects $probe_net]} err]} {
        puts $fp "get_net_delays_error=$err"
    } else {
        puts $fp "net_delays_count=[llength $nd]"
        foreach d $nd {
            puts $fp "net_delay_object=[get_property NAME $d]"
            puts $fp "net_delay_properties=[list_property $d]"
            foreach prop [list FAST_MAX FAST_MIN SLOW_MAX SLOW_MIN DELAY INCREMENTAL_DELAY] {
                if {![catch {set v [get_property $prop $d]}]} {
                    puts $fp "$prop=$v"
                }
            }
        }
    }
}

close $fp
close_design
exit
