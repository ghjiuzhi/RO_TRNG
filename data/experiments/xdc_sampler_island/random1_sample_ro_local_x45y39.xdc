################################################################
# Auto-generated sampler-island TRNG placement constraints
# label=random1_sample_ro_local_x45y39
# matrix_xdc=data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc
# Data RO constraints are copied verbatim from the matrix XDC.
################################################################

################################################################
# Auto-generated RO placement constraints
# pattern=random, x0=36, y0=35, ro_num=8, pitch=8, seed=1
# Assumes entropy_source.RO_STAGES == 2 and RO_TRNG_top instance name u_entropy_source.
################################################################

# RO0 at SLICE_X44Y39
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO1 at SLICE_X52Y42
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO2 at SLICE_X67Y63
set_property LOC SLICE_X67Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X67Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO3 at SLICE_X66Y59
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO4 at SLICE_X49Y41
set_property LOC SLICE_X49Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X49Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO5 at SLICE_X67Y36
set_property LOC SLICE_X67Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X67Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO6 at SLICE_X60Y62
set_property LOC SLICE_X60Y62 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X60Y62 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO7 at SLICE_X36Y63
set_property LOC SLICE_X36Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X36Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# Sample RO constrained near data ROs, origin=SLICE_X45Y39
set_property LOC SLICE_X45Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X45Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X45Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X45Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X47Y39 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
