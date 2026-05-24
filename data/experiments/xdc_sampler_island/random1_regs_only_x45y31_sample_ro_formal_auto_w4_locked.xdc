################################################################
# Auto-generated sampler-island TRNG placement constraints
# label=random1_sampler_regs_only_x45y31
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

# Sample RO intentionally left unconstrained/baseline for regs-only ablation.

# Sampling registers constrained as an 8x8 local island, origin=SLICE_X45Y31
# sampled_data[0] line=0 bit=0
set_property LOC SLICE_X45Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[1] line=0 bit=1
set_property LOC SLICE_X46Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[2] line=0 bit=2
set_property LOC SLICE_X47Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[3] line=0 bit=3
set_property LOC SLICE_X48Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[4] line=0 bit=4
set_property LOC SLICE_X49Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[5] line=0 bit=5
set_property LOC SLICE_X50Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[6] line=0 bit=6
set_property LOC SLICE_X51Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[7] line=0 bit=7
set_property LOC SLICE_X52Y31 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[0].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[8] line=1 bit=0
set_property LOC SLICE_X45Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[9] line=1 bit=1
set_property LOC SLICE_X46Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[10] line=1 bit=2
set_property LOC SLICE_X47Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[11] line=1 bit=3
set_property LOC SLICE_X48Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[12] line=1 bit=4
set_property LOC SLICE_X49Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[13] line=1 bit=5
set_property LOC SLICE_X50Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[14] line=1 bit=6
set_property LOC SLICE_X51Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[15] line=1 bit=7
set_property LOC SLICE_X52Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[1].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[16] line=2 bit=0
set_property LOC SLICE_X45Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[17] line=2 bit=1
set_property LOC SLICE_X46Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[18] line=2 bit=2
set_property LOC SLICE_X47Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[19] line=2 bit=3
set_property LOC SLICE_X48Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[20] line=2 bit=4
set_property LOC SLICE_X49Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[21] line=2 bit=5
set_property LOC SLICE_X50Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[22] line=2 bit=6
set_property LOC SLICE_X51Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[23] line=2 bit=7
set_property LOC SLICE_X52Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[2].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[24] line=3 bit=0
set_property LOC SLICE_X45Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[25] line=3 bit=1
set_property LOC SLICE_X46Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[26] line=3 bit=2
set_property LOC SLICE_X47Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[27] line=3 bit=3
set_property LOC SLICE_X48Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[28] line=3 bit=4
set_property LOC SLICE_X49Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[29] line=3 bit=5
set_property LOC SLICE_X50Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[30] line=3 bit=6
set_property LOC SLICE_X51Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[31] line=3 bit=7
set_property LOC SLICE_X52Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[3].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[32] line=4 bit=0
set_property LOC SLICE_X45Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[33] line=4 bit=1
set_property LOC SLICE_X46Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[34] line=4 bit=2
set_property LOC SLICE_X47Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[35] line=4 bit=3
set_property LOC SLICE_X48Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[36] line=4 bit=4
set_property LOC SLICE_X49Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[37] line=4 bit=5
set_property LOC SLICE_X50Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[38] line=4 bit=6
set_property LOC SLICE_X51Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[39] line=4 bit=7
set_property LOC SLICE_X52Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[4].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[40] line=5 bit=0
set_property LOC SLICE_X45Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[41] line=5 bit=1
set_property LOC SLICE_X46Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[42] line=5 bit=2
set_property LOC SLICE_X47Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[43] line=5 bit=3
set_property LOC SLICE_X48Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[44] line=5 bit=4
set_property LOC SLICE_X49Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[45] line=5 bit=5
set_property LOC SLICE_X50Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[46] line=5 bit=6
set_property LOC SLICE_X51Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[47] line=5 bit=7
set_property LOC SLICE_X52Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[5].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[48] line=6 bit=0
set_property LOC SLICE_X45Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[49] line=6 bit=1
set_property LOC SLICE_X46Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[50] line=6 bit=2
set_property LOC SLICE_X47Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[51] line=6 bit=3
set_property LOC SLICE_X48Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[52] line=6 bit=4
set_property LOC SLICE_X49Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[53] line=6 bit=5
set_property LOC SLICE_X50Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[54] line=6 bit=6
set_property LOC SLICE_X51Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[55] line=6 bit=7
set_property LOC SLICE_X52Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[6].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]
# sampled_data[56] line=7 bit=0
set_property LOC SLICE_X45Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[0].sampled_data_reg*}]
# sampled_data[57] line=7 bit=1
set_property LOC SLICE_X46Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[1].sampled_data_reg*}]
# sampled_data[58] line=7 bit=2
set_property LOC SLICE_X47Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[2].sampled_data_reg*}]
# sampled_data[59] line=7 bit=3
set_property LOC SLICE_X48Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[3].sampled_data_reg*}]
# sampled_data[60] line=7 bit=4
set_property LOC SLICE_X49Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[4].sampled_data_reg*}]
# sampled_data[61] line=7 bit=5
set_property LOC SLICE_X50Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[5].sampled_data_reg*}]
# sampled_data[62] line=7 bit=6
set_property LOC SLICE_X51Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[6].sampled_data_reg*}]
# sampled_data[63] line=7 bit=7
set_property LOC SLICE_X52Y38 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/SAMPLE_DATA_LINE_LOOP[7].SAMPLE_DATA_BIT_LOOP[7].sampled_data_reg*}]

################################################################
# Extra constraints: lock sample RO to formal auto w4 retest routed LOC/BEL.
# Purpose: test whether compact diagnostic masks formal restart bias because
# sample-RO physical implementation changed, or because surrounding
# FIFO/UART/FSM/readout implementation changed.
################################################################
set_property LOC SLICE_X47Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property LOC SLICE_X46Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[2].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[3].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y35 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[4].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y36 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[5].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X46Y37 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[6].u_LUT6_not1/u_LUT6}]
set_property LOC SLICE_X49Y45 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
