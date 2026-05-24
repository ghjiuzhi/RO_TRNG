set_property PACKAGE_PIN N16 [get_ports por_n_i]
set_property IOSTANDARD LVCMOS33 [get_ports por_n_i]
set_property PULLUP true [get_ports por_n_i]

set_property PACKAGE_PIN J15 [get_ports UART_TX_o]
set_property IOSTANDARD LVCMOS33 [get_ports UART_TX_o]

set_property PACKAGE_PIN U18 [get_ports sys_clk]
set_property IOSTANDARD LVCMOS33 [get_ports sys_clk]
create_clock -name sys_clk -period 20.000 [get_ports sys_clk]

set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP*.RO_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP*.RO_NAND.u_LUT6_nand2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/in0[0]}]

set_false_path -to [get_pins -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP*/SAMPLE_DATA_BIT_LOOP*/sampled_data_reg*/D}]
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *snapshot_mem_reg*/D}]
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *stage_xor_mem_reg*/D}]
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *rand_bit_mem_reg*/D}]
