# SP800-90B Smoke Summary

- estimator: NIST SP800-90B EntropyAssessment `ea_non_iid` plus selected `ea_iid` diagnostics
- sample window: first 1,000,000 symbols per prepared input
- interpretation: smoke screening only; not a full validation campaign

| dataset | tool | mode | bits/symbol | H_original | IID chi-square | IID LRS | status |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| original_fpga1_run01_10mib | ea_iid | bit-symbols-msb | 1 | 0.995802 | pass | fail | iid_failed |
| random1_run01 | ea_iid | bit-symbols-msb | 1 | 0.588813 | fail | fail | iid_failed |
| random3_run01 | ea_iid | bit-symbols-msb | 1 | 0.995676 | pass | fail | iid_failed |
| checker_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.865884 | NA | NA | ok |
| compact_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.834591 | NA | NA | ok |
| cross_region_run02 | ea_non_iid | bit-symbols-lsb | 1 | 0.861193 | NA | NA | ok |
| far_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.847848 | NA | NA | ok |
| original_fpga1_run01_10mib | ea_non_iid | bit-symbols-lsb | 1 | 0.821566 | NA | NA | ok |
| random1_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.383737 | NA | NA | ok |
| random2_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.824495 | NA | NA | ok |
| random3_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.828444 | NA | NA | ok |
| row_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.770955 | NA | NA | ok |
| same_column_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.834502 | NA | NA | ok |
| sparse_run01 | ea_non_iid | bit-symbols-lsb | 1 | 0.742313 | NA | NA | ok |
| checker_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.863144 | NA | NA | ok |
| compact_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.872029 | NA | NA | ok |
| cross_region_run02 | ea_non_iid | bit-symbols-msb | 1 | 0.818336 | NA | NA | ok |
| far_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.820724 | NA | NA | ok |
| original_fpga1_run01_10mib | ea_non_iid | bit-symbols-msb | 1 | 0.834723 | NA | NA | ok |
| random1_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.385385 | NA | NA | ok |
| random2_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.863906 | NA | NA | ok |
| random3_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.869064 | NA | NA | ok |
| row_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.783063 | NA | NA | ok |
| same_column_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.834068 | NA | NA | ok |
| sparse_run01 | ea_non_iid | bit-symbols-msb | 1 | 0.734432 | NA | NA | ok |

Notes:

- `H_original` is reported in bits per output symbol by the EntropyAssessment tool.
- The bit-symbol mode expands each captured byte into eight binary symbols before running the non-IID estimator.
- IID rows are diagnostic only; the headline entropy claim should use the conservative non-IID rows unless IID is fully justified.
- These smoke results are suitable for layout comparison and triage, not for claiming SP800-90B compliance.
