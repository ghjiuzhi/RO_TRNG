set out_file ""
set hw_url "localhost:3122"

if {$argc >= 1} {
    set out_file [lindex $argv 0]
}
if {$argc >= 2} {
    set hw_url [lindex $argv 1]
}

open_hw_manager
if {[catch {connect_hw_server -url $hw_url} msg]} {
    puts "connect_hw_server warning: $msg"
}
if {[catch {open_hw_target} msg]} {
    puts "open_hw_target warning: $msg"
}

set sysmons [get_hw_sysmons]
if {[llength $sysmons] == 0} {
    puts "No hw_sysmon object found."
    exit 2
}

set sysmon [lindex $sysmons 0]
refresh_hw_sysmon $sysmon

set keys {TEMPERATURE VCCINT VCCAUX VCCBRAM VPVN}
set values {}
foreach key $keys {
    set value ""
    catch {set value [get_property $key $sysmon]}
    lappend values $value
}

set timestamp [clock format [clock seconds] -format "%Y-%m-%d %H:%M:%S"]
set line "$timestamp,[join $values ,]"
set header "timestamp,[join $keys ,]"

puts $header
puts $line

if {$out_file ne ""} {
    set exists [file exists $out_file]
    set fh [open $out_file a]
    if {!$exists} {
        puts $fh $header
    }
    puts $fh $line
    close $fh
    puts "Wrote $out_file"
}

catch {close_hw_target}
catch {disconnect_hw_server}
