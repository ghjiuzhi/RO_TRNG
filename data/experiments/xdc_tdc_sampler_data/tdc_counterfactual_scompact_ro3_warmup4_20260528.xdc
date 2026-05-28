################################################################
# Exact sampler-side counterfactual TDC placement constraints
# label=tdc_counterfactual_scompact_ro3_warmup4_20260528
# u_ro_a=Scompact sample RO lock from compact FIFO diagnostic W4
# u_ro_b=data_ro3 from random1 matrix
# expected top=RO_TDC_reset_aligned_top or RO_TDC_pair_sysclk_top
# required synth generics: {RO_A_STAGES=9 RO_B_STAGES=2}
################################################################

# u_ro_a <= Scompact sample RO, expected RO_STAGES=9
set_property LOC SLICE_X46Y34 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X46Y32 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X47Y33 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y33 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y34 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y35 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y36 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y37 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X49Y45 [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_a/RO_STAGE_LOOP[7].u_LUT6_not1/u_LUT6}]

# u_ro_b <= data RO3 from random1 matrix, expected RO_STAGES=2
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL C6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property LOC SLICE_X66Y59 [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL D6LUT [get_cells -hierarchical -filter {NAME =~ *u_ro_b/RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
