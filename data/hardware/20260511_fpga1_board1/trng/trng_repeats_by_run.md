# TRNG Repeats by Run

Complete formal/repeat captures only.

| run | placement | sample_role | formal_or_repeat | bytes | p1 | abs_bias | bit_min_entropy | monobit_p | runs_p | adjacent_equal_ratio | byte_min_entropy | sha256 | valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checker_run01 | checker | formal | formal | 10485760 | 0.499929237 | 7.07626343e-05 | 0.999795837 | 0.194899475 | 0.149267368 | 0.500078744 | 7.97278511 | 9AD7FB0641A2790C8FFAA9AA35CC2C4626CF9B765A0558588D681C36323DB3A1 | true |
| checker_repeat02_5mib | checker | repeat | repeat | 5242880 | 0.499947119 | 5.28812408e-05 | 0.999847425 | 0.493372771 | 0.239635009 | 0.500090802 | 7.96410121 | 240A92C1D92DD9783CA4D76A2B3544F752A41E2B8BF75E41EC79EF5226580692 | true |
| compact_run01 | compact | formal | formal | 10485760 | 0.499947906 | 5.20944595e-05 | 0.999849695 | 0.339952314 | 0.263603273 | 0.499938983 | 7.97683476 | 465A74CBD8EA45D543DA994FF2C4B4FD147A906B15CDEB460AA8A643BCB74716 | true |
| compact_repeat02_5mib | compact | repeat | repeat | 5242880 | 0.500059223 | 5.9223175e-05 | 0.999829128 | 0.443022427 | 0.0980423787 | 0.499872291 | 7.97347656 | EB601E16DC5E287778BD73AFD7D10DAE7ABA3BFD2A04937BF1117D28641AD917 | true |
| cross_region_run02 | cross_region | formal | formal | 10485760 | 0.49994415 | 5.58495522e-05 | 0.999838861 | 0.306286677 | 0.719841022 | 0.499980432 | 7.98367919 | F21CF761EF2074B8BA0E6E5B3C811FE320CFD26FCF1F8EC76BE4AA4315890215 | true |
| cross_region_repeat02_5mib | cross_region | repeat | repeat | 5242880 | 0.500011396 | 1.13964081e-05 | 0.999967117 | 0.882647301 | 0.561737791 | 0.500044811 | 7.96623289 | 693DD1C7F65C3E7AD5815A7DFC54A4E94A3C88A3B92CAB0B01D275908AA17115 | true |
| far_run01 | far | formal | formal | 10485760 | 0.491507936 | 0.00849206448 | 0.975702835 | 0 | 0 | 0.500726348 | 7.79616262 | 863885F73EEDFDF58444D4705CEED0260F9BAA3D883410D82BA5F4AE95161732 | true |
| far_repeat02_5mib | far | repeat | repeat | 5242880 | 0.491642475 | 0.00835752487 | 0.976084602 | 0 | 0 | 0.500773513 | 7.79024204 | E211FFEEBA215C82C32B3017167FA34CCF2C62676847B7A32979596D7E999EF9 | true |
| original_fpga1_repeat02_5mib | original_fpga1 | repeat | repeat | 5242880 | 0.500216961 | 0.000216960907 | 0.999374119 | 0.00495065355 | 0.64365765 | 0.499964392 | 7.96898809 | E6244C3F8317BF7AB55E5594EE69425CCB2542F7E172835A46BFD9926173A9F0 | true |
| random1_run01 | random1 | formal | formal | 10485760 | 0.337315512 | 0.162684488 | 0.593605945 | 0 | 0 | 0.556739754 | 4.80160868 | 48D17BAA35460C4FE9142D38E7DAAD4EF1FE8538D74186658AEC02D73F99C4E2 | true |
| random1_repeat02_5mib | random1 | repeat | repeat | 5242880 | 0.337669373 | 0.162330627 | 0.594376522 | 0 | 0 | 0.556682719 | 4.80477392 | FAC1A5CFCDA3A82ACEA1D8C3503F4CED49B6070FDCEF9F5C054B03CA92A3A470 | true |
| random2_run01 | random2 | formal | formal | 10485760 | 0.491222239 | 0.00877776146 | 0.974892483 | 0 | 0 | 0.501079673 | 7.77684296 | 98F5AE37C7D727553F1221B78AC1A4301AB81D410C30CDF60D52DB71E641670B | true |
| random2_repeat02_5mib | random2 | repeat | repeat | 5242880 | 0.491030312 | 0.00896968842 | 0.974348355 | 0 | 0 | 0.501148617 | 7.79591799 | BA89FBA3927D03108EFC6CC0506761055F1C3BBADB00083FBF9DF037D8CF0221 | true |
| random3_run01 | random3 | formal | formal | 10485760 | 0.499968565 | 3.14354897e-05 | 0.999909299 | 0.564729298 | 0.18437283 | 0.500072473 | 7.9845501 | 42BA7D7466E4D8F3303EF544585AE322938FD9D83341B7F6A5F58E1439848C7D | true |
| random3_repeat02_5mib | random3 | repeat | repeat | 5242880 | 0.499971128 | 2.88724899e-05 | 0.999916694 | 0.708421881 | 0.0487015454 | 0.499847829 | 7.97396076 | 3DC7AE9DFC0E718F87E2E4F851061F6D1817CDD72C0D3FA0798F3357D536D359 | true |
| row_run01 | row | formal | formal | 10485760 | 0.473579586 | 0.0264204144 | 0.925712657 | 0 | 0 | 0.504303533 | 7.36645981 | 2A3D04A19180AC5EF47351B7CBD608D781A9F2BD302690FDE4D9B2E8A18497AD | true |
| row_repeat02_5mib | row | repeat | repeat | 5242880 | 0.473337555 | 0.0266624451 | 0.925049507 | 0 | 0 | 0.504302442 | 7.34742388 | 317A01D9FF318A68850B7A40F7321606B1818AB6D5CD1096275955611AA805BC | true |
| same_column_run01 | same_column | formal | formal | 10485760 | 0.499930251 | 6.97493553e-05 | 0.99979876 | 0.201369495 | 0 | 0.505979735 | 7.86432277 | C7D7D252A804D8FF652BA76815FA59367ABE02BC7EEC39BFFB00FAA45D14E9E5 | true |
| same_column_repeat02_5mib | same_column | repeat | repeat | 5242880 | 0.499835944 | 0.000164055824 | 0.999526713 | 0.033589607 | 0 | 0.506032288 | 7.86672933 | 1EA95A632173BEE21F6E731B6F992F30E90E3C30356D6E87EDA0F014948E4787 | true |
| sparse_run01 | sparse | formal | formal | 10485760 | 0.464349854 | 0.035650146 | 0.900637067 | 0 | 0 | 0.506596333 | 7.1440609 | 3F7A3B491848262BFF1C3AE8E9A136C2226227B0C1B27DA796227B6F2E2A5791 | true |
| sparse_repeat02_5mib | sparse | repeat | repeat | 5242880 | 0.464140511 | 0.0358594894 | 0.900073341 | 0 | 0 | 0.506506574 | 7.1555296 | DC9AC7B1EC34F7A64EC8530BAC3C59F5D3D3BEA81ECD7D796E21834FF4BE41B5 | true |

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
| random1_ro_freq_fixed_smoke01_512k |  |  | 524288 | metadata kind is not trng |
| random1_ro_freq_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| random1_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| random2_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| random3_ro_freq_fixed_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_run01_5mib |  |  | 5242880 | metadata kind is not trng |
| random3_ro_freq_fixed_run02_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_run03_2mib |  |  | 2097152 | metadata kind is not trng |
| random3_ro_freq_fixed_smoke01_512k |  |  | 524288 | metadata kind is not trng |
| random3_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| row_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| same_column_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| sparse_smoke01 |  |  | 1048576 | not a formal/repeat capture id |
| tdc_far_run01 |  |  | 2097152 | metadata kind is not trng |
| tdc_far_run02_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_near_run01 |  |  | 2097152 | metadata kind is not trng |
| tdc_near_run02 |  |  | 2097152 | metadata kind is not trng |
| tdc_near_run03_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_near_smoke03 |  |  | 1024 | metadata kind is not trng |
| tdc_near_smoke_direct01 |  |  | 1024 | metadata kind is not trng |
| tdc_pair_random1_ro0_ro1_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro2_ro4_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random1_ro4_ro5_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro0_ro6_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro5_run01_2mib |  |  | 2097152 | metadata kind is not trng |
| tdc_pair_random3_ro3_ro7_run01_2mib |  |  | 2097152 | metadata kind is not trng |
