################################################################
# Counterfactual sample-RO placement constraints
# label=random1_regs_only_x45y31_sample_ro_compact_w4_locked
#
# Purpose:
#   Keep the random1 data-RO placement and the sampler-register island from
#   random1_sampler_regs_only_x45y31.xdc, but explicitly lock the sample RO
#   to the compact FIFO diagnostic w4 routed LOC/BEL.
#
# Mechanism test:
#   If formal auto warmup4 improves when only these sample-RO cells are moved
#   back to the compact routed implementation, this closes the counterfactual
#   loop with the 2026-05-25 sample-RO formal-locked compact failures.
################################################################

source [file normalize "data/experiments/xdc_sampler_island/random1_sampler_regs_only_x45y31.xdc"]

################################################################
# Extra constraints: lock sample RO to compact FIFO diagnostic w4 routed LOC/BEL.
# Source:
#   data/experiments/restart_fifo_diag_20260524/compact_w4_routed_cells.csv
################################################################
set_property LOC SLICE_X46Y34 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL B6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]

set_property LOC SLICE_X46Y32 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[0].u_LUT6_not1/u_LUT6}]

set_property LOC SLICE_X47Y33 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[1].u_LUT6_not1/u_LUT6}]

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
set_property BEL A6LUT [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_LOOP[7].u_LUT6_not1/u_LUT6}]
