# Restart Warmup Repeat02 Status - 2026-05-15

## Current Hardware State

- `warmup10/11/12 repeat02` hardware queue completed.
- No Vivado/program/capture/ea_restart hardware job is running after queue completion.
- Outputs are summarized in `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition_with_repeats.csv`.

## Key Result

The repeated boundary sweep confirms the first-pass transition: `warmup10` still fails, while `warmup11` and `warmup12` pass under the current board, placement, and auto-stream restart protocol.

| warmup | repeat | overall p1 | over cutoff | worst X | MSB | LSB |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 10 | repeat02 | 0.415849000 | 89 | 633 | failed (Xmax=633) | failed (Xmax=633) |
| 10 | run01 | 0.415017000 | 106 | 650 | failed (Xmax=650) | failed (Xmax=650) |
| 11 | repeat02 | 0.469261000 | 0 | 588 | passed (Xmax=588) | passed (Xmax=588) |
| 11 | run01 | 0.469088000 | 0 | 583 | passed (Xmax=583) | passed (Xmax=583) |
| 12 | repeat02 | 0.499506000 | 0 | 549 | passed (Xmax=556) | passed (Xmax=556) |
| 12 | run01 | 0.499478000 | 0 | 562 | passed (Xmax=562) | passed (Xmax=562) |

## Paper Interpretation

- The boundary is no longer based on a single run: two observations now show `warmup10` failing and `warmup11/12` passing.
- The safe wording is: under this board/placement/protocol, the observed pass boundary lies at `10 < WARMUP_BYTES <= 11`.
- This is still not a universal SP800-90B certification or cross-PVT threshold; it is strong mechanism evidence for a restart transient window.