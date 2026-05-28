# Extract sampler-side routed implementation evidence from a routed DCP.
#
# Usage:
#   vivado -mode batch -source scripts/vivado/extract_sample_ro_route_evidence_20260528.tcl \
#     -tclargs <routed.dcp> <out_dir> <label>

if {$argc < 3} {
    puts "Usage: vivado -mode batch -source scripts/vivado/extract_sample_ro_route_evidence_20260528.tcl -tclargs <routed.dcp> <out_dir> <label>"
    exit 1
}

set dcp   [file normalize [lindex $argv 0]]
set outdir [file normalize [lindex $argv 1]]
set label [lindex $argv 2]

file mkdir $outdir
open_checkpoint $dcp

proc csv_quote {value} {
    set s "$value"
    regsub -all {"} $s {""} s
    return "\"$s\""
}

proc csv_row {fp values} {
    set quoted {}
    foreach v $values {
        lappend quoted [csv_quote $v]
    }
    puts $fp [join $quoted ","]
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

proc object_names {objs {limit 0}} {
    set names {}
    set i 0
    foreach o $objs {
        if {$limit > 0 && $i >= $limit} {
            break
        }
        lappend names [get_property NAME $o]
        incr i
    }
    return [join $names " "]
}

proc classify_cell {cell_name} {
    if {[string match "*u_entropy_source/RO_SAMPLE_*" $cell_name]} {
        return "sample_ro"
    }
    if {[string match "*u_entropy_source/SAMPLE_DATA_LINE_LOOP*" $cell_name] && [string match "*sampled_data_reg*" $cell_name]} {
        return "sampled_data_regs"
    }
    if {[string match "*u_entropy_source/RO_NUM_LOOP*" $cell_name]} {
        return "data_ro"
    }
    if {[string match "*u_entropy_source*" $cell_name]} {
        return "entropy_source_other"
    }
    return "other"
}

set entropy_cells [get_cells -hierarchical -quiet -filter {NAME =~ *u_entropy_source*}]

set sample_cells {}
set sampled_regs {}
set data_cells {}
foreach c $entropy_cells {
    set cname [get_property NAME $c]
    if {([string first "u_entropy_source/RO_SAMPLE_NAND." $cname] >= 0 ||
         [string first "u_entropy_source/RO_SAMPLE_AND." $cname] >= 0 ||
         [string first "u_entropy_source/RO_SAMPLE_LOOP" $cname] >= 0) &&
        [string match "*/u_LUT6" $cname]} {
        lappend sample_cells $c
    }
    if {[string first "u_entropy_source/SAMPLE_DATA_LINE_LOOP" $cname] >= 0 &&
        [string first "sampled_data_reg" $cname] >= 0} {
        lappend sampled_regs $c
    }
    if {[string first "u_entropy_source/RO_NUM_LOOP" $cname] >= 0 &&
        [string match "*/u_LUT6" $cname]} {
        lappend data_cells $c
    }
}

set summary_fp [open [file join $outdir "${label}_summary.txt"] w]
puts $summary_fp "label=$label"
puts $summary_fp "dcp=$dcp"
puts $summary_fp "sample_cells=[llength $sample_cells]"
puts $summary_fp "sampled_regs=[llength $sampled_regs]"
puts $summary_fp "data_cells=[llength $data_cells]"
puts $summary_fp "entropy_cells=[llength $entropy_cells]"
close $summary_fp

set cell_fp [open [file join $outdir "${label}_cells.csv"] w]
csv_row $cell_fp {label group name ref_name loc bel site tile clock_region is_placed is_bel_fixed is_loc_fixed}
foreach c [concat $sample_cells $sampled_regs $data_cells] {
    set name [get_property NAME $c]
    set loc [safe_prop $c LOC]
    set site [safe_prop $c SITE]
    set tile ""
    if {$site ne ""} {
        set site_obj [get_sites -quiet $site]
        if {[llength $site_obj] > 0} {
            set tile [object_names [get_tiles -quiet -of_objects $site_obj] 1]
        }
    }
    csv_row $cell_fp [list \
        $label \
        [classify_cell $name] \
        $name \
        [safe_prop $c REF_NAME] \
        $loc \
        [safe_prop $c BEL] \
        $site \
        $tile \
        [safe_prop $c CLOCK_REGION] \
        [safe_prop $c IS_PLACED] \
        [safe_prop $c IS_BEL_FIXED] \
        [safe_prop $c IS_LOC_FIXED] \
    ]
}
close $cell_fp

array set net_seen {}
proc remember_nets_for_pin_pattern {var_name cells pin_patterns} {
    upvar $var_name seen
    foreach c $cells {
        foreach pat $pin_patterns {
            set pins [get_pins -quiet -of_objects $c -filter "REF_PIN_NAME =~ $pat"]
            foreach p $pins {
                set nets [get_nets -quiet -of_objects $p]
                foreach n $nets {
                    set nn [get_property NAME $n]
                    set seen($nn) 1
                }
            }
        }
    }
}

remember_nets_for_pin_pattern net_seen $sample_cells {O I0 I1 I2 I3 I4 I5}
remember_nets_for_pin_pattern net_seen $sampled_regs {C D Q}
remember_nets_for_pin_pattern net_seen $data_cells {O I0 I1 I2 I3 I4 I5}

set net_fp [open [file join $outdir "${label}_nets.csv"] w]
csv_row $net_fp {label net group driver_pins load_pins driver_cells load_cells fanout route_status pips_count nodes_count route}

set pip_fp [open [file join $outdir "${label}_pips.csv"] w]
csv_row $pip_fp {label net group pip tile start_wire end_wire is_route_fixed}

set delay_fp [open [file join $outdir "${label}_net_delays.csv"] w]
csv_row $delay_fp {label net group to_pin fast_min fast_max slow_min slow_max estimated}

foreach net_name [lsort [array names net_seen]] {
    set n [get_nets -quiet $net_name]
    if {[llength $n] == 0} {
        continue
    }
    set n [lindex $n 0]
    set pins [get_pins -quiet -of_objects $n]
    set drivers {}
    set loads {}
    foreach p $pins {
        set dir [safe_prop $p DIRECTION]
        if {$dir eq "OUT"} {
            lappend drivers $p
        } else {
            lappend loads $p
        }
    }

    set group "other"
    set nn [get_property NAME $n]
    if {[string match "*ro_sample_chain*" $nn] || [string match "*RO_SAMPLE*" $nn]} {
        set group "sample_ro_net"
    } elseif {[string match "*sampled_data*" $nn]} {
        set group "sampled_data_net"
    } elseif {[string match "*ro_chain*" $nn] || [string match "*RO_NUM_LOOP*" $nn]} {
        set group "data_ro_net"
    }

    set pips [get_pips -quiet -of_objects $n]
    set nodes [get_nodes -quiet -of_objects $n]
    set route [safe_prop $n ROUTE]
    if {[string length $route] > 2000} {
        set route "[string range $route 0 1999]..."
    }
    csv_row $net_fp [list \
        $label \
        $nn \
        $group \
        [object_names $drivers] \
        [object_names $loads 40] \
        [object_names [get_cells -quiet -of_objects $drivers]] \
        [object_names [get_cells -quiet -of_objects $loads] 40] \
        [safe_prop $n FLAT_PIN_COUNT] \
        [safe_prop $n ROUTE_STATUS] \
        [llength $pips] \
        [llength $nodes] \
        $route \
    ]

    foreach pip $pips {
        csv_row $pip_fp [list \
            $label \
            $nn \
            $group \
            [get_property NAME $pip] \
            [object_names [get_tiles -quiet -of_objects $pip] 1] \
            [safe_prop $pip START_WIRE_NAME] \
            [safe_prop $pip END_WIRE_NAME] \
            [safe_prop $pip IS_ROUTE_FIXED] \
        ]
    }

    if {![catch {set net_delays [get_net_delays -quiet -of_objects $n]}]} {
        foreach d $net_delays {
            csv_row $delay_fp [list \
                $label \
                $nn \
                $group \
                [safe_prop $d TO_PIN] \
                [safe_prop $d FAST_MIN] \
                [safe_prop $d FAST_MAX] \
                [safe_prop $d SLOW_MIN] \
                [safe_prop $d SLOW_MAX] \
                [safe_prop $d ESTIMATED] \
            ]
        }
    }
}
close $net_fp
close $pip_fp
close $delay_fp

set neigh_fp [open [file join $outdir "${label}_neighborhood_cells.csv"] w]
csv_row $neigh_fp {label center_sample_site cell name ref_name loc bel manhattan_dx manhattan_dy}
foreach sc $sample_cells {
    set sloc [safe_prop $sc LOC]
    if {![regexp {SLICE_X([0-9]+)Y([0-9]+)} $sloc -> sx sy]} {
        continue
    }
    foreach c $entropy_cells {
        set cloc [safe_prop $c LOC]
        if {![regexp {SLICE_X([0-9]+)Y([0-9]+)} $cloc -> cx cy]} {
            continue
        }
        set dx [expr {abs($cx - $sx)}]
        set dy [expr {abs($cy - $sy)}]
        if {$dx <= 2 && $dy <= 2} {
            csv_row $neigh_fp [list \
                $label \
                $sloc \
                [get_property NAME $sc] \
                [get_property NAME $c] \
                [safe_prop $c REF_NAME] \
                $cloc \
                [safe_prop $c BEL] \
                $dx \
                $dy \
            ]
        }
    }
}
close $neigh_fp

set timing_file [file join $outdir "${label}_sample_to_regs_timing.rpt"]
set sample_out_pins [get_pins -quiet -of_objects $sample_cells -filter {REF_PIN_NAME == O}]
set sampled_clock_pins [get_pins -quiet -of_objects $sampled_regs -filter {REF_PIN_NAME == C}]
if {[llength $sample_out_pins] > 0 && [llength $sampled_clock_pins] > 0} {
    catch {
        report_timing -quiet -from $sample_out_pins -to $sampled_clock_pins -max_paths 50 -delay_type min_max -file $timing_file
    } timing_result
    if {[info exists timing_result] && $timing_result ne ""} {
        set tfp [open "${timing_file}.status.txt" w]
        puts $tfp $timing_result
        close $tfp
    }
}

close_design
exit
