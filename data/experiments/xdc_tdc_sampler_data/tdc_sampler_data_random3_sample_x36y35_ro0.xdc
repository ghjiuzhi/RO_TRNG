################################################################
# Auto-generated sampler-data TDC placement constraints
# label=tdc_sampler_data_random3_sample_x36y35_ro0
# family=random3
# source_matrix_xdc=data/experiments/xdc_matrix/ro_random_seed3_x36y35.xdc
# u_ro_a=sample_ro_x36y35; u_ro_b=data_ro0
# expected top=RO_TDC_pair_sysclk_top
# required synth generics: {RO_A_STAGES=9 RO_B_STAGES=2}
################################################################

# u_ro_a <= sample RO island at SLICE_X36Y35, expected RO_STAGES=9
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X36Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X37Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X38Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[7].u_LUT6_not1/u_LUT6}]

# u_ro_b <= data RO0, expected RO_STAGES=2
set_property LOC SLICE_X51Y43 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X51Y43 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
