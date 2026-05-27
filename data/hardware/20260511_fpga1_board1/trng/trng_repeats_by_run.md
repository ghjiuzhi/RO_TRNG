# TRNG Repeats by Run

Complete formal/repeat captures only.

| run | placement | sample_role | formal_or_repeat | bytes | p1 | abs_bias | bit_min_entropy | monobit_p | runs_p | adjacent_equal_ratio | byte_min_entropy | sha256 | valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checker_run01 | checker | formal | formal | 10485760 | 0.499929237 | 7.07626343e-05 | 0.999795837 | 0.194899475 | 0.149267368 | 0.500078744 | 7.97278511 | 9AD7FB0641A2790C8FFAA9AA35CC2C4626CF9B765A0558588D681C36323DB3A1 | true |
| checker_repeat02_5mib | checker | repeat | repeat | 5242880 | 0.499947119 | 5.28812408e-05 | 0.999847425 | 0.493372771 | 0.239635009 | 0.500090802 | 7.96410121 | 240A92C1D92DD9783CA4D76A2B3544F752A41E2B8BF75E41EC79EF5226580692 | true |
| checker_repeat03_20mib | checker | repeat | repeat | 20971520 | 0.499891073 | 0.000108927488 | 0.999685736 | 0.00477537838 | 0.318457063 | 0.500038537 | 7.98496832 | 8036BA5E92E81577C8D80BF5369E7F80CF9F2BBC0D5ABC638C906E83E4D861F2 | true |
| compact_run01 | compact | formal | formal | 10485760 | 0.499947906 | 5.20944595e-05 | 0.999849695 | 0.339952314 | 0.263603273 | 0.499938983 | 7.97683476 | 465A74CBD8EA45D543DA994FF2C4B4FD147A906B15CDEB460AA8A643BCB74716 | true |
| compact_repeat02_5mib | compact | repeat | repeat | 5242880 | 0.500059223 | 5.9223175e-05 | 0.999829128 | 0.443022427 | 0.0980423787 | 0.499872291 | 7.97347656 | EB601E16DC5E287778BD73AFD7D10DAE7ABA3BFD2A04937BF1117D28641AD917 | true |
| compact_repeat03_20mib | compact | repeat | repeat | 20971520 | 0.49998951 | 1.04904175e-05 | 0.999969731 | 0.78580792 | 0.503952382 | 0.499974206 | 7.98679948 | F86DE00FB040877D86BE9AA8B5EBCB854C1736E64077A2C009F295344C803807 | true |
| cross_region_run02 | cross_region | formal | formal | 10485760 | 0.49994415 | 5.58495522e-05 | 0.999838861 | 0.306286677 | 0.719841022 | 0.499980432 | 7.98367919 | F21CF761EF2074B8BA0E6E5B3C811FE320CFD26FCF1F8EC76BE4AA4315890215 | true |
| cross_region_repeat02_5mib | cross_region | repeat | repeat | 5242880 | 0.500011396 | 1.13964081e-05 | 0.999967117 | 0.882647301 | 0.561737791 | 0.500044811 | 7.96623289 | 693DD1C7F65C3E7AD5815A7DFC54A4E94A3C88A3B92CAB0B01D275908AA17115 | true |
| cross_region_repeat03_20mib | cross_region | repeat | repeat | 20971520 | 0.500040174 | 4.01735306e-05 | 0.999884088 | 0.29800992 | 0.0160911071 | 0.499907097 | 7.98868537 | C79235898C34814AD5752858DAE0BD8874E5CC7B76E378140B5B37F7C87770C6 | true |
| far_run01 | far | formal | formal | 10485760 | 0.491507936 | 0.00849206448 | 0.975702835 | 0 | 0 | 0.500726348 | 7.79616262 | 863885F73EEDFDF58444D4705CEED0260F9BAA3D883410D82BA5F4AE95161732 | true |
| far_repeat02_5mib | far | repeat | repeat | 5242880 | 0.491642475 | 0.00835752487 | 0.976084602 | 0 | 0 | 0.500773513 | 7.79024204 | E211FFEEBA215C82C32B3017167FA34CCF2C62676847B7A32979596D7E999EF9 | true |
| far_repeat03_20mib | far | repeat | repeat | 20971520 | 0.491668612 | 0.00833138824 | 0.976158778 | 0 | 0 | 0.500706014 | 7.8060281 | B95B393BBA5A901E401378374190BC8141B5B0EAC595BB544110287891B8515E | true |
| original_fpga1_repeat02_5mib | original_fpga1 | repeat | repeat | 5242880 | 0.500216961 | 0.000216960907 | 0.999374119 | 0.00495065355 | 0.64365765 | 0.499964392 | 7.96898809 | E6244C3F8317BF7AB55E5594EE69425CCB2542F7E172835A46BFD9926173A9F0 | true |
| random1_run01 | random1 | formal | formal | 10485760 | 0.337315512 | 0.162684488 | 0.593605945 | 0 | 0 | 0.556739754 | 4.80160868 | 48D17BAA35460C4FE9142D38E7DAAD4EF1FE8538D74186658AEC02D73F99C4E2 | true |
| random1_repeat02_5mib | random1 | repeat | repeat | 5242880 | 0.337669373 | 0.162330627 | 0.594376522 | 0 | 0 | 0.556682719 | 4.80477392 | FAC1A5CFCDA3A82ACEA1D8C3503F4CED49B6070FDCEF9F5C054B03CA92A3A470 | true |
| random1_repeat03 | random1 | repeat | repeat | 20971520 | 0.338616818 | 0.161383182 | 0.596441735 | 0 | 0 | 0.555965105 | 4.8233827 | 0D02918F7803A7885F611E15566CDE14D531B2ADE0525231065884F7D0583BD2 | true |
| random2_run01 | random2 | formal | formal | 10485760 | 0.491222239 | 0.00877776146 | 0.974892483 | 0 | 0 | 0.501079673 | 7.77684296 | 98F5AE37C7D727553F1221B78AC1A4301AB81D410C30CDF60D52DB71E641670B | true |
| random2_repeat02_5mib | random2 | repeat | repeat | 5242880 | 0.491030312 | 0.00896968842 | 0.974348355 | 0 | 0 | 0.501148617 | 7.79591799 | BA89FBA3927D03108EFC6CC0506761055F1C3BBADB00083FBF9DF037D8CF0221 | true |
| random2_repeat03_20mib | random2 | repeat | repeat | 20971520 | 0.490493578 | 0.00950642228 | 0.972827763 | 0 | 0 | 0.501216486 | 7.77221862 | 201A5C9B48CAEE65A68B813F8C3ED1417D30691D264F304B0B4ED5C7FF6D5AB7 | true |
| random3_run01 | random3 | formal | formal | 10485760 | 0.499968565 | 3.14354897e-05 | 0.999909299 | 0.564729298 | 0.18437283 | 0.500072473 | 7.9845501 | 42BA7D7466E4D8F3303EF544585AE322938FD9D83341B7F6A5F58E1439848C7D | true |
| random3_repeat02_5mib | random3 | repeat | repeat | 5242880 | 0.499971128 | 2.88724899e-05 | 0.999916694 | 0.708421881 | 0.0487015454 | 0.499847829 | 7.97396076 | 3DC7AE9DFC0E718F87E2E4F851061F6D1817CDD72C0D3FA0798F3357D536D359 | true |
| random3_repeat03 | random3 | repeat | repeat | 20971520 | 0.499915069 | 8.49306583e-05 | 0.999754963 | 0.0277954843 | 0.0454687485 | 0.500077233 | 7.98505547 | 25BB10AEB89CF743993498DEEA9606DF2EFF30CA40884710C3672CA9850A7DB4 | true |
| row_run01 | row | formal | formal | 10485760 | 0.473579586 | 0.0264204144 | 0.925712657 | 0 | 0 | 0.504303533 | 7.36645981 | 2A3D04A19180AC5EF47351B7CBD608D781A9F2BD302690FDE4D9B2E8A18497AD | true |
| row_repeat02_5mib | row | repeat | repeat | 5242880 | 0.473337555 | 0.0266624451 | 0.925049507 | 0 | 0 | 0.504302442 | 7.34742388 | 317A01D9FF318A68850B7A40F7321606B1818AB6D5CD1096275955611AA805BC | true |
| row_repeat03_20mib | row | repeat | repeat | 20971520 | 0.476642209 | 0.0233577907 | 0.934130521 | 0 | 0 | 0.503794006 | 7.41843455 | 7422E7EAF71267F8195433FA4DD1B3350B6C647D3BAD7493B758C37FD3B96290 | true |
| same_column_run01 | same_column | formal | formal | 10485760 | 0.499930251 | 6.97493553e-05 | 0.99979876 | 0.201369495 | 0 | 0.505979735 | 7.86432277 | C7D7D252A804D8FF652BA76815FA59367ABE02BC7EEC39BFFB00FAA45D14E9E5 | true |
| same_column_repeat02_5mib | same_column | repeat | repeat | 5242880 | 0.499835944 | 0.000164055824 | 0.999526713 | 0.033589607 | 0 | 0.506032288 | 7.86672933 | 1EA95A632173BEE21F6E731B6F992F30E90E3C30356D6E87EDA0F014948E4787 | true |
| same_column_repeat03_20mib | same_column | repeat | repeat | 20971520 | 0.49991914 | 8.08596611e-05 | 0.999766707 | 0.0361976574 | 0 | 0.506360582 | 7.86265659 | 4D4F4B8ACFC90CA5329BC710FFAF4CF9CC5A12F247FAFB4D4F102F89978E083A | true |
| sparse_run01 | sparse | formal | formal | 10485760 | 0.464349854 | 0.035650146 | 0.900637067 | 0 | 0 | 0.506596333 | 7.1440609 | 3F7A3B491848262BFF1C3AE8E9A136C2226227B0C1B27DA796227B6F2E2A5791 | true |
| sparse_repeat02_5mib | sparse | repeat | repeat | 5242880 | 0.464140511 | 0.0358594894 | 0.900073341 | 0 | 0 | 0.506506574 | 7.1555296 | DC9AC7B1EC34F7A64EC8530BAC3C59F5D3D3BEA81ECD7D796E21834FF4BE41B5 | true |
| sparse_repeat03_20mib | sparse | repeat | repeat | 20971520 | 0.46336593 | 0.0366340697 | 0.897989444 | 0 | 0 | 0.50653058 | 7.1220545 | D8901B892ED4B24AA36F323F50FDFD5E08F4D9EA4C6B677DE9E6526F273F3EA0 | true |

## Excluded captures

| run | placement | sample_role | bytes | reason |
| --- | --- | --- | --- | --- |
| checker_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| compact_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| cross_region_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| far_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| original_fpga1_program_capture01 |  |  | 1024 | not a formal/repeat capture id |
| original_fpga1_run01_10mib |  |  | 10485760 | not a formal/repeat capture id |
| random1_ro_freq_fixed_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| random1_ro_freq_fixed_run01_5mib |  |  | 5242880 | metadata kind is not trng |
| random1_ro_freq_fixed_run02_2mib |  |  | 2097152 | metadata kind is not trng |
| random1_ro_freq_fixed_run03_2mib |  |  | 2097152 | metadata kind is not trng |
| random1_ro_freq_fixed_run04_5mib |  |  | 5242880 | metadata kind is not trng |
| random1_ro_freq_fixed_smoke01_512k |  |  | 524288 | metadata kind is not trng |
| random1_ro_freq_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| random1_sample_ro_local_x45y39_20mib_20260523 |  |  | 20971520 | not a formal/repeat capture id |
| random1_sample_ro_local_x45y39_5mib_20260523 |  |  | 5242880 | not a formal/repeat capture id |
| random1_sampler_island_local_x45y39_regs_x45y31_5mib_20260523 |  |  | 5242880 | not a formal/repeat capture id |
| random1_sampler_island_local_x45y39_regs_x45y31_program_20mib_20260523 |  |  | 20971520 | not a formal/repeat capture id |
| random1_sampler_island_local_x45y39_regs_x45y31_program_5mib_20260523 |  |  | 5242880 | not a formal/repeat capture id |
| random1_sampler_regs_only_restart_auto_formal_1000x125_warmup4_retest01_20260524 |  |  | 125008 | metadata kind is not trng |
| random1_sampler_regs_only_x45y31_20mib_20260524 |  |  | 20971520 | not a formal/repeat capture id |
| random1_sampler_regs_only_x45y31_smoke_5mib_20260524 |  |  | 5242880 | not a formal/repeat capture id |
| random1_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| random2_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| random3_ro_freq_fixed_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_run01_5mib |  |  | 5242880 | metadata kind is not trng |
| random3_ro_freq_fixed_run02_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_run03_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_run04_5mib |  |  | 5242880 | metadata kind is not trng |
| random3_ro_freq_fixed_smoke01_512k |  |  | 524288 | metadata kind is not trng |
| random3_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| restart_aligned_snapshot_bits_regs_only_warmup32_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_bits_regs_only_warmup40_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_bits_regs_only_warmup80_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_bits_regs_only_warmup88_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_regs_only_warmup10_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_regs_only_warmup11_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_regs_only_warmup4_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_aligned_snapshot_regs_only_warmup4_cap64_smoke01 |  |  | 1040 | metadata kind is not trng |
| restart_aligned_snapshot_regs_only_warmup5_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup32_cap1024_fixed_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup32_cap1024_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup32_cap64_smoke01 |  |  | 8208 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup40_cap1024_fixed_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup40_cap1024_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup80_cap1024_fixed_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup80_cap1024_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup88_cap1024_fixed_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup88_cap1024_run01 |  |  | 131088 | metadata kind is not trng |
| restart_byte_snapshot_bits_regs_only_warmup88_cap1024_run02 |  |  | 131088 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup11_1000x125_run01_20260525 |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_oldbit_repeat03_no_xadc_20260525 |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup4_1000x125_run01_no_xadc |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run01_20260525 |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_sample_ro_formal_locked_warmup5_1000x125_run02_20260525 |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_warmup11_1000x125_run01_no_xadc |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_warmup4_1000x125_run01_no_xadc |  |  | 125016 | metadata kind is not trng |
| restart_fifo_compact_diag_regs_only_warmup5_1000x125_run01_no_xadc |  |  | 125016 | metadata kind is not trng |
| restart_fifo_diag_regs_only_warmup4_1000x32_run02_no_xadc |  |  | 576016 | metadata kind is not trng |
| restart_fifo_diag_regs_only_warmup4_smoke_32x16_run01 |  |  | 10256 | metadata kind is not trng |
| restart_fifo_diag_regs_only_warmup5_1000x32_run01_no_xadc |  |  | 576016 | metadata kind is not trng |
| restart_fifo_diag_v3fastwarmup_regs_only_warmup4_1000x32_run01_no_xadc |  |  | 576016 | metadata kind is not trng |
| ro_freq_random1_sample_x36y35_w100_baseline_2mib_20260523 |  |  | 2097152 | metadata kind is not trng |
| ro_freq_random1_sample_x45y39_2mib_20260523 |  |  | 2097152 | metadata kind is not trng |
| ro_freq_random1_sample_x45y39_2mib_program_20260523 |  |  | 2097152 | metadata kind is not trng |
| ro_freq_random1_sample_x45y39_w100_2mib_20260523 |  |  | 2097152 | metadata kind is not trng |
| row_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| same_column_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| sampler_snapshot_regs_only_warmup10_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup10_cap64_run01 |  |  | 1040 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup11_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup11_cap64_run01 |  |  | 1040 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup4_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup4_cap64_smoke01 |  |  | 1040 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup5_cap1024_run01 |  |  | 16400 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup5_cap64_bram_regress01 |  |  | 1040 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup5_cap64_run01 |  |  | 1040 | metadata kind is not trng |
| sampler_snapshot_regs_only_warmup5_cap64_xpm_regress01 |  |  | 1040 | metadata kind is not trng |
| sparse_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| tdc_code_density_cal_a11_b7_formal_8mib_20260525 |  |  | 8388608 | metadata kind is not trng |
| tdc_code_density_cal_a7_b11_formal_8mib_20260525 |  |  | 8388608 | metadata kind is not trng |
| tdc_code_density_cal_a7_b11_smoke_2mib_20260525 |  |  | 2097152 | metadata kind is not trng |
| tdc_far_run01 |  |  | 2097152 | metadata kind is not trng |
| tdc_far_run02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_mask_random1_local_sample_ro0_ro1_pair_only |  |  |  | metadata kind is not trng |
| tdc_mask_random1_local_sample_ro0_ro1_pair_plus_sample |  |  |  | metadata kind is not trng |
| tdc_mask_random1_ro0_ro1_all_data_on |  |  |  | metadata kind is not trng |
| tdc_mask_random1_ro0_ro1_pair_only |  |  |  | metadata kind is not trng |
| tdc_mask_random1_ro0_ro1_pair_only_smoke_20260525 |  |  |  | metadata kind is not trng |
| tdc_mask_random1_ro0_ro1_pair_plus_sample |  |  |  | metadata kind is not trng |
| tdc_mask_random3_ro0_ro6_all_data_on |  |  |  | metadata kind is not trng |
| tdc_mask_random3_ro0_ro6_all_data_on_repeat02 |  |  |  | metadata kind is not trng |
| tdc_mask_random3_ro0_ro6_neighbors_on |  |  |  | metadata kind is not trng |
| tdc_mask_random3_ro0_ro6_pair_only |  |  |  | metadata kind is not trng |
| tdc_mask_random3_ro0_ro6_pair_plus_sample |  |  |  | metadata kind is not trng |
| tdc_near_run01 |  |  | 2097152 | metadata kind is not trng |
| tdc_near_run02 |  |  | 2097152 | metadata kind is not trng |
| tdc_near_run03_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_near_smoke03 |  |  | 1024 | metadata kind is not trng |
| tdc_near_smoke_direct01 |  |  | 1024 | metadata kind is not trng |
| tdc_pair_random1_ro0_ro1_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro0_ro1_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro2_ro4_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro2_ro4_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro4_ro5_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro4_ro5_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro0_ro6_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro0_ro6_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro5_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro5_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro7_repeat02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro7_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro0 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro0_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro0_smoke_delay10s_no_xadc |  |  | 262144 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro0_smoke_delay3s_no_xadc |  |  | 65536 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro0_smoke_no_xadc |  |  | 65536 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro4 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_baseline_ro4_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_sampler_local_ro0 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_sampler_local_ro0_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_sampler_local_ro4 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random1_sampler_local_ro4_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random3_goodref_ro0 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random3_goodref_ro0_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random3_goodref_ro3 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_enable_random3_goodref_ro3_repeat02 |  |  | 2097152 | metadata kind is not trng |
| tdc_reset_random1_baseline_ro0_clean32k_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_baseline_ro0_clean32k_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_baseline_ro0_smoke_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_baseline_ro0_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_baseline_ro0_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_sampler_local_ro0_clean32k_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_sampler_local_ro0_smoke_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_sampler_local_ro0_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random1_sampler_local_ro0_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random3_goodref_ro0_clean32k_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random3_goodref_ro0_clean32k_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random3_goodref_ro0_warmup0_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_reset_random3_goodref_ro0_warmup12_preopen_20260525 |  |  |  | metadata kind is not trng |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro0_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_sampler_data_random1_baseline_sample_x36y35_ro4_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_sampler_data_random1_local_sample_x45y39_ro0_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_sampler_data_random1_local_sample_x45y39_ro4_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_sampler_data_random3_sample_x36y35_ro0_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_sampler_data_random3_sample_x36y35_ro3_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_uart_header_debug_repeat8_no_xadc |  |  | 128 | metadata kind is not trng |
