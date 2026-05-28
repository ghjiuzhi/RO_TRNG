# Extract LOC/BEL assignments for exact counterfactual TDC RO cells.
# Usage:
#   vivado -mode batch -source scripts/vivado/extract_tdc_counterfactual_locbel_20260528.tcl \
#     -tclargs <routed.dcp> <out.csv> <label>

if {$argc < 3} {
    error "Usage: extract_tdc_counterfactual_locbel_20260528.tcl <routed.dcp> <out.csv> <label>"
}

set dcp_file [file normalize [lindex $argv 0]]
set out_file [file normalize [lindex $argv 1]]
set label [lindex $argv 2]

open_checkpoint $dcp_file

file mkdir [file dirname $out_file]
set fh [open $out_file w]
puts $fh "label,role,cell,loc,bel"

set patterns [list \
    [list sample_ro "*u_ro_a/RO_NAND.u_LUT6_nand2_1/u_LUT6"] \
    [list sample_ro "*u_ro_a/RO_STAGE_LOOP[*].u_LUT6_not1/u_LUT6"] \
    [list data_ro0 "*u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6"] \
    [list data_ro0 "*u_ro_b/RO_STAGE_LOOP[*].u_LUT6_not1/u_LUT6"] \
]

foreach item $patterns {
    set role [lindex $item 0]
    set pattern [lindex $item 1]
    foreach cell [lsort [get_cells -hierarchical -filter "NAME =~ $pattern"]] {
        set loc [get_property LOC $cell]
        set bel [get_property BEL $cell]
        puts $fh "$label,$role,$cell,$loc,$bel"
    }
}

close $fh
close_design
puts "Wrote $out_file"
