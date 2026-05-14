################################################################
# Auto-generated pair-specific TDC RO placement constraints
# source_matrix_xdc=data/experiments/xdc_matrix/ro_random_seed1_x36y35.xdc
# family=random1
# pair_id=random1_ro0_ro1
# pair=(0,1); u_ro_a=RO0; u_ro_b=RO1
# ro_stages=2; expected top=RO_TDC_pair_sysclk_top
# copy_bel=yes
################################################################

# u_ro_a <= source RO0
#   stage0: loc=SLICE_X44Y39, bel=A6LUT
#   stage1: loc=SLICE_X44Y39, bel=B6LUT
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X44Y39 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]

# u_ro_b <= source RO1
#   stage0: loc=SLICE_X52Y42, bel=C6LUT
#   stage1: loc=SLICE_X52Y42, bel=D6LUT
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X52Y42 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
