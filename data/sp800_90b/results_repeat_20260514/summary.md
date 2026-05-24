# SP800-90B Smoke Summary

- estimator: NIST SP800-90B EntropyAssessment `ea_non_iid` plus selected `ea_iid` diagnostics
- sample window: first 1,000,000 symbols per prepared input
- interpretation: smoke screening only; not a full validation campaign

| dataset | tool | mode | bits/symbol | H_original | IID chi-square | IID LRS | status |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| random1_repeat03 | ea_non_iid | bit-symbols-lsb | 1 | 0.390783 | NA | NA | ok |
| random3_repeat03 | ea_non_iid | bit-symbols-lsb | 1 | 0.894588 | NA | NA | ok |
| random1_repeat03 | ea_non_iid | bit-symbols-msb | 1 | 0.390399 | NA | NA | ok |
| random3_repeat03 | ea_non_iid | bit-symbols-msb | 1 | 0.856158 | NA | NA | ok |

Notes:

- `H_original` is reported in bits per output symbol by the EntropyAssessment tool.
- The bit-symbol mode expands each captured byte into eight binary symbols before running the non-IID estimator.
- IID rows are diagnostic only; the headline entropy claim should use the conservative non-IID rows unless IID is fully justified.
- These smoke results are suitable for layout comparison and triage, not for claiming SP800-90B compliance.
