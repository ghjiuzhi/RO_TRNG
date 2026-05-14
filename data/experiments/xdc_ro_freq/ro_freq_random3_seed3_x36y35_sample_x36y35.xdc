################################################################
# Auto-generated RO frequency probe placement constraints
# matrix_xdc=data/experiments/xdc_matrix/ro_random_seed3_x36y35.xdc
# Data RO constraints are copied from the matrix XDC. The probe RTL
# intentionally keeps instance name u_entropy_source and generate labels
# compatible with RO_TRNG_top entropy_source placement constraints.
################################################################

# Data RO coordinates copied from source:
# RO0: SLICE_X51Y43
# RO1: SLICE_X59Y65
# RO2: SLICE_X40Y35
# RO3: SLICE_X66Y51
# RO4: SLICE_X50Y47
# RO5: SLICE_X66Y65
# RO6: SLICE_X61Y44
# RO7: SLICE_X50Y44

# RO0 at SLICE_X51Y43
set_property LOC SLICE_X51Y43 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X51Y43 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO1 at SLICE_X59Y65
set_property LOC SLICE_X59Y65 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X59Y65 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO2 at SLICE_X40Y35
set_property LOC SLICE_X40Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X40Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO3 at SLICE_X66Y51
set_property LOC SLICE_X66Y51 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X66Y51 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO4 at SLICE_X50Y47
set_property LOC SLICE_X50Y47 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X50Y47 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO5 at SLICE_X66Y65
set_property LOC SLICE_X66Y65 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X66Y65 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO6 at SLICE_X61Y44
set_property LOC SLICE_X61Y44 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X61Y44 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO7 at SLICE_X50Y44
set_property LOC SLICE_X50Y44 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X50Y44 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# sample RO at SLICE_X36Y35, stages=9
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X38Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
