set dcp [lindex $argv 0]
set out [lindex $argv 1]

open_checkpoint $dcp
set fp [open $out w]

proc dump_props {fp label obj} {
    puts $fp "## $label"
    puts $fp "OBJECT=[get_property NAME $obj]"
    foreach p [lsort [list_property $obj]] {
        set v [get_property $p $obj]
        if {[string length $v] > 240} {
            set v "[string range $v 0 239]..."
        }
        regsub -all {\r|\n} $v { } v
        puts $fp "$p=$v"
    }
    puts $fp ""
}

set sample_cells [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_*/*/u_LUT6}]
set sampled_regs [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP*.sampled_data_reg*}]
puts $fp "sample_cells=[llength $sample_cells]"
puts $fp "sampled_regs=[llength $sampled_regs]"

if {[llength $sample_cells] > 0} {
    set c [lindex $sample_cells 0]
    dump_props $fp "CELL" $c
    set pins [get_pins -of_objects $c]
    if {[llength $pins] > 0} {
        set pin [lindex $pins 0]
        dump_props $fp "PIN" $pin
        set nets [get_nets -of_objects $pin]
        if {[llength $nets] > 0} {
            set net [lindex $nets 0]
            dump_props $fp "NET" $net
            set pips [get_pips -quiet -of_objects $net]
            puts $fp "PIPS=[llength $pips]"
            if {[llength $pips] > 0} {
                dump_props $fp "PIP" [lindex $pips 0]
            }
        }
    }
}

if {[llength $sampled_regs] > 0} {
    set r [lindex $sampled_regs 0]
    dump_props $fp "SAMPLED_REG" $r
}

close $fp
close_design
exit
