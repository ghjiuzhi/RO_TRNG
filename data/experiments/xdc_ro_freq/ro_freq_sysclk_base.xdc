set_property PACKAGE_PIN N16 [get_ports por_n_i]
set_property IOSTANDARD LVCMOS33 [get_ports por_n_i]
set_property PULLUP true [get_ports por_n_i]

set_property PACKAGE_PIN J15 [get_ports UART_TX_o]
set_property IOSTANDARD LVCMOS33 [get_ports UART_TX_o]

set_property PACKAGE_PIN U18 [get_ports sys_clk]
set_property IOSTANDARD LVCMOS33 [get_ports sys_clk]
create_clock -name sys_clk -period 20.000 [get_ports sys_clk]

set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[*].RO_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/in0[0]}]

# The measured RO clocks are asynchronous to sys_clk and are intentionally muxed
# into a debug counter. Do not use this probe top for timing closure evidence.
set_false_path -through [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/*}]
