# Program the first connected FPGA device with a bitstream.
# Run with:
#   vivado -mode batch -source scripts/vivado/program_bitstream.tcl -tclargs path/to/file.bit
#   vivado -mode batch -source scripts/vivado/program_bitstream.tcl -tclargs path/to/file.bit localhost:3122

if {$argc < 1} {
    error "Usage: program_bitstream.tcl <bitstream.bit> ?hw_server_url?"
}

set bit_file [file normalize [lindex $argv 0]]
if {![file exists $bit_file]} {
    error "Bitstream not found: $bit_file"
}
set hw_url "localhost:3121"
if {$argc >= 2} {
    set hw_url [lindex $argv 1]
}

open_hw_manager
puts "Connecting to hw_server at $hw_url"
connect_hw_server -url $hw_url
open_hw_target

set devices [get_hw_devices]
if {[llength $devices] == 0} {
    error "No hardware device found. Check USB-JTAG connection and board power."
}

puts "Detected hardware devices:"
foreach d $devices {
    puts "  $d"
}

set dev ""
foreach d $devices {
    set d_name [string tolower [get_property NAME $d]]
    set d_part ""
    catch {set d_part [string tolower [get_property PART $d]]}

    # Zynq JTAG chains commonly expose arm_dap_0 before the FPGA fabric device.
    # arm_dap_0 is useful for PS debug, but it cannot accept a PL bitstream.
    if {[string match "arm_dap*" $d_name]} {
        continue
    }
    if {[string match "xc7z*" $d_name] || [string match "xc7z*" $d_part]} {
        set dev $d
        break
    }
}

if {$dev eq ""} {
    foreach d $devices {
        set d_name [string tolower [get_property NAME $d]]
        if {![string match "arm_dap*" $d_name]} {
            set dev $d
            break
        }
    }
}

if {$dev eq ""} {
    error "No programmable FPGA fabric device found. Detected only: $devices"
}

current_hw_device $dev
refresh_hw_device -update_hw_probes false $dev
set_property PROGRAM.FILE $bit_file $dev

puts "Programming device $dev with $bit_file"
program_hw_devices $dev
refresh_hw_device $dev
puts "Programming completed."

close_hw_target
disconnect_hw_server
