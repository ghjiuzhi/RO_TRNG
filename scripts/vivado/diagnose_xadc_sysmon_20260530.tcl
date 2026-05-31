# Diagnose Vivado hardware sysmon/XADC visibility.
#
# Usage:
#   vivado -mode batch -source scripts/vivado/diagnose_xadc_sysmon_20260530.tcl \
#     -tclargs <out.csv> ?hw_server_url?

set out_file ""
set hw_url "localhost:3122"

if {$argc >= 1} {
    set out_file [lindex $argv 0]
}
if {$argc >= 2} {
    set hw_url [lindex $argv 1]
}

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
    if {[catch {set props [list_property $obj]}]} {
        set props {}
    }
    if {[llength $props] > 0 && [lsearch -exact $props $prop] < 0} {
        return ""
    }
    if {[catch {set v [get_property $prop $obj]}]} {
        return ""
    }
    return $v
}

proc object_name {obj} {
    if {$obj eq ""} {
        return ""
    }
    if {[catch {set v [get_property NAME $obj]}]} {
        return "$obj"
    }
    return $v
}

set timestamp [clock format [clock seconds] -format "%Y-%m-%d %H:%M:%S"]
set status "ok"
set error ""

open_hw_manager
if {[catch {connect_hw_server -url $hw_url} msg]} {
    puts "connect_hw_server warning: $msg"
}
if {[catch {open_hw_target} msg]} {
    set status "open_target_failed"
    set error $msg
    puts "open_hw_target warning: $msg"
}

set devices [get_hw_devices -quiet]
puts "Detected hardware devices:"
foreach d $devices {
    puts [format "  device=%s name=%s part=%s" $d [safe_prop $d NAME] [safe_prop $d PART]]
}

set selected_device ""
foreach d $devices {
    set d_name [string tolower [safe_prop $d NAME]]
    set d_part [string tolower [safe_prop $d PART]]
    if {[string match "arm_dap*" $d_name]} {
        continue
    }
    if {[string match "xc7z*" $d_name] || [string match "xc7z*" $d_part]} {
        set selected_device $d
        break
    }
}
if {$selected_device eq "" && [llength $devices] > 0} {
    set selected_device [lindex $devices 0]
}
if {$selected_device ne ""} {
    catch {current_hw_device $selected_device}
    catch {refresh_hw_device -update_hw_probes false $selected_device}
}

set sysmons [get_hw_sysmons -quiet]
puts "Detected sysmons: $sysmons"

set fh ""
if {$out_file ne ""} {
    set exists [file exists $out_file]
    set fh [open $out_file a]
    if {!$exists} {
        csv_row $fh {timestamp hw_url status error selected_device selected_device_name selected_device_part sysmon_index sysmon sysmon_name temperature_c vccint_v vccaux_v vccbram_v vpvn_v raw_temperature raw_vccint raw_vccaux raw_vccbram}
    }
}

if {[llength $sysmons] == 0} {
    set status "no_sysmon"
    set error "get_hw_sysmons returned no objects"
    if {$fh ne ""} {
        csv_row $fh [list $timestamp $hw_url $status $error $selected_device [safe_prop $selected_device NAME] [safe_prop $selected_device PART] "" "" "" "" "" "" "" "" "" "" "" ""]
    }
} else {
    set idx 0
    foreach s $sysmons {
        set row_status $status
        set row_error $error
        if {[catch {refresh_hw_sysmon $s} msg]} {
            set row_status "refresh_failed"
            set row_error $msg
        }
        set temp [safe_prop $s TEMPERATURE]
        set vccint [safe_prop $s VCCINT]
        set vccaux [safe_prop $s VCCAUX]
        set vccbram [safe_prop $s VCCBRAM]
        set vpvn [safe_prop $s VPVN]
        puts [format "sysmon(%d)=%s temp=%s vccint=%s vccaux=%s vccbram=%s vpvn=%s status=%s error=%s" $idx $s $temp $vccint $vccaux $vccbram $vpvn $row_status $row_error]
        puts "sysmon($idx) properties: [join [lsort [list_property $s]] { }]"
        if {$fh ne ""} {
            csv_row $fh [list \
                $timestamp \
                $hw_url \
                $row_status \
                $row_error \
                $selected_device \
                [safe_prop $selected_device NAME] \
                [safe_prop $selected_device PART] \
                $idx \
                $s \
                [object_name $s] \
                $temp \
                $vccint \
                $vccaux \
                $vccbram \
                $vpvn \
                [safe_prop $s RAW_TEMPERATURE] \
                [safe_prop $s RAW_VCCINT] \
                [safe_prop $s RAW_VCCAUX] \
                [safe_prop $s RAW_VCCBRAM] \
            ]
        }
        incr idx
    }
}

if {$fh ne ""} {
    close $fh
    puts "Wrote $out_file"
}

catch {close_hw_target}
catch {disconnect_hw_server}
