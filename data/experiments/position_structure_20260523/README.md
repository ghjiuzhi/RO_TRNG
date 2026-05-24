# TRNG Position Structure Analysis 20260523

Offline analysis of existing 20 MiB placement captures under `data/hardware/20260511_fpga1_board1/trng`. No hardware or Vivado flow was started.

## Outputs

- `position_structure_summary.csv`: one row per capture with scalar metrics and expanded bit/byte-position fields.
- `README.md`: this summary.

## Metric Notes

- `p1`: fraction of one bits over the whole bitstream, MSB-first within each byte.
- `bit_min_entropy`: `-log2(max(p1, 1-p1))`, the binary most-common-value estimate.
- `adjacent_equal`: fraction of adjacent bit pairs that are `00` or `11`.
- `lag1_phi`: phi/Pearson correlation from adjacent-bit 2x2 counts.
- `bitpos0..7`: byte-internal bit positions, where 0 is the MSB and 7 is the LSB.
- `bytepos_mod16/mod32`: one-bit fraction grouped by byte index modulo 16 or 32.

## Core Findings

- Captures analyzed: 10, total bytes: 209715200.
- Mean p1: 0.476054211259; largest absolute whole-stream bias: random1_repeat03 (0.16138318181).
- Lowest binary min-entropy: random1_repeat03 (0.596441734915 bits/bit).
- Strongest lag-1 magnitude: same_column_repeat03_20mib (0.0127211372898); adjacent_equal = 0.506360581555.
- Largest byte-position mod32 max bias: random1_repeat03 (0.161852264404 at slot 1).

## Per-Capture Overview

| capture_id | placement | bytes | p1 | bit_min_entropy | adjacent_equal | lag1_phi | bytepos_mod16_max_abs_bias | bytepos_mod32_max_abs_bias | longest_zero_run | longest_one_run |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checker_repeat03_20mib | checker | 20971520 | 0.499891072512 | 0.999685735936 | 0.500038537383 | 7.70273120796e-05 | 0.000426578521729 | 0.000556755065918 | 25 | 25 |
| compact_repeat03_20mib | compact | 20971520 | 0.499989509583 | 0.999969731371 | 0.49997420609 | -5.15882605787e-05 | 0.000359535217285 | 0.000461196899414 | 28 | 27 |
| cross_region_repeat03_20mib | cross_region | 20971520 | 0.500040173531 | 0.99988408835 | 0.49990709722 | -0.000185812018074 | 0.000295543670654 | 0.000559616088867 | 26 | 25 |
| far_repeat03_20mib | far | 20971520 | 0.491668611765 | 0.976158778417 | 0.500706014041 | 0.00113469480715 | 0.00858459472656 | 0.0087474822998 | 25 | 25 |
| random1_repeat03 | random1 | 20971520 | 0.33861681819 | 0.596441734915 | 0.555965105033 | 0.00865359908018 | 0.161725997925 | 0.161852264404 | 43 | 17 |
| random2_repeat03_20mib | random2 | 20971520 | 0.490493577719 | 0.972827763344 | 0.501216486104 | 0.00207223303252 | 0.0100215911865 | 0.010231590271 | 26 | 26 |
| random3_repeat03 | random3 | 20971520 | 0.499915069342 | 0.999754962731 | 0.500077232719 | 0.00015443658742 | 0.000358009338379 | 0.000551223754883 | 29 | 26 |
| row_repeat03_20mib | row | 20971520 | 0.476642209291 | 0.934130520503 | 0.503794005536 | 0.00541748833013 | 0.0236385345459 | 0.0238162994385 | 31 | 24 |
| same_column_repeat03_20mib | same_column | 20971520 | 0.499919140339 | 0.999766707199 | 0.506360581555 | 0.0127211372898 | 0.0003830909729 | 0.000673675537109 | 29 | 29 |
| sparse_repeat03_20mib | sparse | 20971520 | 0.463365930319 | 0.897989443942 | 0.506530579964 | 0.00773446077348 | 0.0368098258972 | 0.0370010375977 | 30 | 22 |

## Byte-Internal Bit-Position Bias

| capture_id | bitpos0_bias | bitpos1_bias | bitpos2_bias | bitpos3_bias | bitpos4_bias | bitpos5_bias | bitpos6_bias | bitpos7_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| checker_repeat03_20mib | 7.49588012695e-05 | -0.000131416320801 | -8.34465026855e-06 | -0.000142192840576 | -0.00025954246521 | -0.000120162963867 | -0.000107669830322 | -0.000177049636841 |
| compact_repeat03_20mib | -0.000206518173218 | 0.000146961212158 | -5.69820404053e-05 | -6.55651092529e-05 | 3.80992889404e-05 | 3.31401824951e-05 | 1.6736984253e-05 | 1.02043151855e-05 |
| cross_region_repeat03_20mib | -2.09331512451e-05 | 0.000246906280518 | 9.83238220215e-05 | -7.83443450928e-05 | 5.34534454346e-05 | 6.13689422607e-05 | -4.1151046753e-05 | 1.76429748533e-06 |
| far_repeat03_20mib | -0.00835180282593 | -0.00831084251404 | -0.00829887390137 | -0.00842523574829 | -0.00828409194946 | -0.00823855400085 | -0.00821709632874 | -0.00852460861206 |
| random1_repeat03 | -0.161302375793 | -0.161418008804 | -0.161526727676 | -0.161430025101 | -0.161224603653 | -0.161428165436 | -0.161261510849 | -0.16147403717 |
| random2_repeat03_20mib | -0.0093273639679 | -0.00975589752197 | -0.00948920249939 | -0.00955891609192 | -0.00951538085937 | -0.00953245162964 | -0.0093683719635 | -0.00950379371643 |
| random3_repeat03 | -0.000105571746826 | -0.000245189666748 | -5.41210174561e-05 | -9.84668731689e-05 | -1.20162963867e-05 | -3.69548797607e-05 | -1.14440917969e-05 | -0.00011568069458 |
| row_repeat03_20mib | -0.0232860565186 | -0.0233518123627 | -0.0232769012451 | -0.0233877658844 | -0.0233248710632 | -0.0234105587006 | -0.0234871387482 | -0.0233372211456 |
| same_column_repeat03_20mib | -7.64846801758e-05 | -9.6845626831e-05 | -0.000114583969116 | -4.92572784424e-05 | -0.000130319595337 | -3.80516052246e-05 | -0.000141620635986 | 2.86102294966e-07 |
| sparse_repeat03_20mib | -0.0366805553436 | -0.0366754055023 | -0.0365099906921 | -0.036542224884 | -0.036612701416 | -0.0367304325104 | -0.0366487503052 | -0.0366724967957 |
