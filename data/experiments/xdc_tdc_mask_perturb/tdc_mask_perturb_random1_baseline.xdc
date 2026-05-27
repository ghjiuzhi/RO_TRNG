################################################################
# Auto-generated TDC mask perturbation placement constraints
# family=random1
# matrix_xdc=data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc
# sample_source=baseline
# expected top=RO_TDC_pair_mask_perturb_top; RO matrix instance u_ro_matrix
################################################################
################################################################
# Auto-generated RO placement constraints
# pattern=random, x0=36, y0=35, ro_num=8, pitch=8, seed=1
# Assumes entropy_source.RO_STAGES == 2 and RO_TDC_pair_mask_perturb_top instance name u_ro_matrix.
################################################################

# RO0 at SLICE_X44Y39
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO1 at SLICE_X52Y42
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO2 at SLICE_X67Y63
set_property LOC SLICE_X67Y63 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X67Y63 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO3 at SLICE_X66Y59
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO4 at SLICE_X49Y41
set_property LOC SLICE_X49Y41 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X49Y41 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO5 at SLICE_X67Y36
set_property LOC SLICE_X67Y36 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X67Y36 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO6 at SLICE_X60Y62
set_property LOC SLICE_X60Y62 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X60Y62 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO7 at SLICE_X36Y63
set_property LOC SLICE_X36Y63 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X36Y63 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]


# Baseline sample RO placement for TDC perturbation control
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X38Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]

# Acknowledge intentional RO combinational loops for bitstream generation.
set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[*].RO_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_NUM_LOOP[*].RO_NAND.u_LUT6_nand2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_AND.u_LUT6_and2_1/in0[0]}]
set_property ALLOW_COMBINATORIAL_LOOPS TRUE [get_nets -hierarchical -filter {NAME =~ *u_ro_matrix/RO_SAMPLE_NAND.u_LUT6_nand2_1/in0[0]}]
