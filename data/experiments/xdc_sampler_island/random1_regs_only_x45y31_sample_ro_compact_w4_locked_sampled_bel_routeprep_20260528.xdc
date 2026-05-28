################################################################
# Sample-RO compact W4 placement plus sampled-register BEL locks.
# The sampled-register BEL lock file is generated from the compact W4
# routed DCP before running the partial route-lock probe.
################################################################

source [file normalize "data/experiments/xdc_sampler_island/random1_regs_only_x45y31_sample_ro_compact_w4_locked.xdc"]
source [file normalize "data/experiments/route_lock_20260528/compact_w4_sampled_reg_bel_lock_20260528.xdc"]
