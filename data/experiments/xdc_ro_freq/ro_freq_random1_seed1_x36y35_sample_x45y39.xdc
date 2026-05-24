################################################################
# Auto-generated RO frequency probe placement constraints
# matrix_xdc=data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc
# Data RO constraints are copied from the matrix XDC. The probe RTL
# intentionally keeps instance name u_entropy_source and generate labels
# compatible with RO_TRNG_top entropy_source placement constraints.
################################################################

# Data RO coordinates copied from source:
# RO0: SLICE_X44Y39
# RO1: SLICE_X52Y42
# RO2: SLICE_X67Y63
# RO3: SLICE_X66Y59
# RO4: SLICE_X49Y41
# RO5: SLICE_X67Y36
# RO6: SLICE_X60Y62
# RO7: SLICE_X36Y63

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

# sample RO at SLICE_X45Y39, stages=9
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
