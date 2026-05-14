################################################################
# Auto-generated RO placement constraints
# pattern=sparse, x0=36, y0=35, ro_num=8, pitch=6, seed=1
# Assumes entropy_source.RO_STAGES == 2 and RO_TRNG_top instance name u_entropy_source.
################################################################

# RO0 at SLICE_X36Y35
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO1 at SLICE_X42Y35
set_property LOC SLICE_X42Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X42Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO2 at SLICE_X48Y35
set_property LOC SLICE_X48Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X48Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO3 at SLICE_X54Y35
set_property LOC SLICE_X54Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X54Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO4 at SLICE_X36Y41
set_property LOC SLICE_X36Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X36Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO5 at SLICE_X42Y41
set_property LOC SLICE_X42Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X42Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO6 at SLICE_X48Y41
set_property LOC SLICE_X48Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X48Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO7 at SLICE_X54Y41
set_property LOC SLICE_X54Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X54Y41 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
