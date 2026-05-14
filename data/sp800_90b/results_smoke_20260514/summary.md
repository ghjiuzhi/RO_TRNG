# SP800-90B Smoke Summary

- estimator: NIST SP800-90B EntropyAssessment `ea_non_iid`
- sample window: first 1,000,000 symbols per prepared input
- interpretation: smoke screening only; not a full validation campaign

| dataset | mode | bits/symbol | H_original | status |
| --- | --- | ---: | ---: | --- |
| checker_run01 | bit-symbols-lsb | 1 | 0.865884 | ok |
| compact_run01 | bit-symbols-lsb | 1 | 0.834591 | ok |
| cross_region_run02 | bit-symbols-lsb | 1 | 0.861193 | ok |
| far_run01 | bit-symbols-lsb | 1 | 0.847848 | ok |
| original_fpga1_run01_10mib | bit-symbols-lsb | 1 | 0.821566 | ok |
| random1_run01 | bit-symbols-lsb | 1 | 0.383737 | ok |
| random2_run01 | bit-symbols-lsb | 1 | 0.824495 | ok |
| random3_run01 | bit-symbols-lsb | 1 | 0.828444 | ok |
| row_run01 | bit-symbols-lsb | 1 | 0.770955 | ok |
| same_column_run01 | bit-symbols-lsb | 1 | 0.834502 | ok |
| sparse_run01 | bit-symbols-lsb | 1 | 0.742313 | ok |
| checker_run01 | bit-symbols-msb | 1 | 0.863144 | ok |
| compact_run01 | bit-symbols-msb | 1 | 0.872029 | ok |
| cross_region_run02 | bit-symbols-msb | 1 | 0.818336 | ok |
| far_run01 | bit-symbols-msb | 1 | 0.820724 | ok |
| original_fpga1_run01_10mib | bit-symbols-msb | 1 | 0.834723 | ok |
| random1_run01 | bit-symbols-msb | 1 | 0.385385 | ok |
| random2_run01 | bit-symbols-msb | 1 | 0.863906 | ok |
| random3_run01 | bit-symbols-msb | 1 | 0.869064 | ok |
| row_run01 | bit-symbols-msb | 1 | 0.783063 | ok |
| same_column_run01 | bit-symbols-msb | 1 | 0.834068 | ok |
| sparse_run01 | bit-symbols-msb | 1 | 0.734432 | ok |

Notes:

- `H_original` is reported in bits per output symbol by the EntropyAssessment tool.
- The bit-symbol mode expands each captured byte into eight binary symbols before running the non-IID estimator.
- These smoke results are suitable for layout comparison and triage, not for claiming SP800-90B compliance.
