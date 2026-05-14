################################################################
# Auto-generated RO placement constraints
# pattern=random, x0=36, y0=35, ro_num=8, pitch=8, seed=2
# Assumes entropy_source.RO_STAGES == 2 and RO_TRNG_top instance name u_entropy_source.
################################################################

# RO0 at SLICE_X39Y40
set_property LOC SLICE_X39Y40 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X39Y40 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO1 at SLICE_X41Y58
set_property LOC SLICE_X41Y58 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X41Y58 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[1].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO2 at SLICE_X46Y54
set_property LOC SLICE_X46Y54 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X46Y54 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[2].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO3 at SLICE_X52Y48
set_property LOC SLICE_X52Y48 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X52Y48 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[3].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO4 at SLICE_X38Y45
set_property LOC SLICE_X38Y45 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X38Y45 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[4].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO5 at SLICE_X63Y60
set_property LOC SLICE_X63Y60 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X63Y60 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[5].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO6 at SLICE_X59Y63
set_property LOC SLICE_X59Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X59Y63 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[6].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# RO7 at SLICE_X53Y37
set_property LOC SLICE_X53Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X53Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[7].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
