create_clock -name sys_clk -period 20.000 [get_ports sys_clk]

set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_ro_a/RO_NAND.u_LUT6_nand2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_ro_b/RO_NAND.u_LUT6_nand2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_ro_a/RO_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS true [get_nets -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/in0[0]}]

# The RO/CARRY outputs are asynchronous events sampled by the TDC registers.
# Keep STA focused on the synchronous post-sampler processing path.
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *u_tdc_a/u_sampler/thermo_raw_o_reg*/D}]
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *u_tdc_b/u_sampler/thermo_raw_o_reg*/D}]
set_false_path -through [get_cells -hierarchical -filter {REF_NAME == CARRY4}]
