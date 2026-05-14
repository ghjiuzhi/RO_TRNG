# 2026-05-11 FPGA1 Hardware Results - Live Notes

## Current validated setup

- Board: fpga1, xc7z020clg400, UART on COM3.
- Vivado: `C:\Programs\Xilinx2023\Vivado\2023.2`.
- Hardware server: use `localhost:3122`, because `3121` is occupied on this machine.
- PL UART pin is J15. Earlier no-byte captures were caused by the board UART path still being connected to PS, not PL.

## Important data-validity rule

Use `data/hardware/20260511_fpga1_board1/hardware_run_audit.csv` as the inclusion table.

The early `tdc_near_run01` capture must not be used in paper figures because it has bad packet framing:

- file size: 2 MiB
- decoded packets: 2049
- sequence gaps: 2048

The valid TDC comparison currently starts from `tdc_near_run02` and `tdc_far_run01`.

## TDC result snapshot

| run | packets | seq_gaps | diff_std_ps | phase_pearson_r | initial reading |
| --- | ---: | ---: | ---: | ---: | --- |
| tdc_near_run02 | 262143 | 0 | 1927.586 | 0.003276 | valid near baseline |
| tdc_far_run01 | 262132 | 43 | 1915.295 | 0.002302 | valid far baseline |

Initial interpretation: the current near/far TDC pair does not show strong phase locking or strong coupling. This is not a negative result; it means the first measurable placement effect is currently stronger in TRNG bias/throughput than in the simple two-lane TDC correlation metric. Repeat runs are required.

## TRNG result snapshot

| run | bytes | role | throughput KiB/s | p1 | bit min-entropy | initial reading |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| compact_smoke01 | 1048576 | smoke | 5.690 | 0.500126 | 0.999638 | very good smoke result |
| compact_run01 | 10485760 | formal | 5.077 | 0.499948 | 0.999850 | very good formal result |
| sparse_smoke01 | 1048576 | smoke | 11.040 | 0.463956 | 0.899577 | strong bias |
| sparse_run01 | 10485760 | formal | 5.305 | 0.464350 | 0.900637 | bias confirmed at 10 MiB |
| far_smoke01 | 1048576 | smoke | 4.811 | 0.491601 | 0.975968 | moderate bias |
| far_run01 | 10485760 | formal | 7.643 | 0.491508 | 0.975703 | moderate bias confirmed at 10 MiB |
| random1_smoke01 | 1048576 | smoke | 11.220 | 0.338280 | 0.595707 | severe bias |
| random1_run01 | 10485760 | formal | 11.245 | 0.337316 | 0.593606 | severe bias confirmed at 10 MiB |
| random3_smoke01 | 1048576 | smoke | 11.219 | 0.500068 | 0.999803 | very good smoke result |
| random3_run01 | 10485760 | formal | 11.246 | 0.499969 | 0.999909 | best formal result so far |

Initial paper hypothesis:

RO placement has a significant and non-monotonic effect on raw entropy quality. The data so far does not support the simple story that "more spread is always better." Random placement is especially revealing: `random1` is the worst result so far, while `random3` is the best formal 10 MiB result so far. This means the paper should quantify actual physical placement and routing features, not only use coarse labels such as compact/sparse/far/random.

Current 10 MiB ranking by bit min-entropy:

| run | p1 | bit min-entropy | reading |
| --- | ---: | ---: | --- |
| random1_run01 | 0.337316 | 0.593606 | severe failure |
| sparse_run01 | 0.464350 | 0.900637 | strong bias |
| far_run01 | 0.491508 | 0.975703 | moderate bias |
| compact_run01 | 0.499948 | 0.999850 | very good |
| random3_run01 | 0.499969 | 0.999909 | best so far |

## Literature/standard anchor

- NIST SP 800-90B defines the expected framing for entropy source validation: noise source, min-entropy estimation, health testing, and connection to SP 800-90A/90C random bit generators. Source: https://csrc.nist.gov/pubs/sp/800/90/b/final
- Saarinen, "On Entropy and Bit Patterns of Ring Oscillator Jitter", emphasizes entropy justification from RO thermal jitter/phase noise, autocorrelation, and bit pattern distributions. Source: https://arxiv.org/abs/2102.02196
- Recent RO-TRNG FPGA papers commonly report throughput, jitter/statistical tests, and NIST 800-90B/800-22 validation. Example: https://www.mdpi.com/2227-7390/11/4/1049

## Automation added

- `scripts/audit_hardware_runs.py`
  - scans metadata and analysis outputs
  - computes or verifies data SHA256 and bitstream SHA256 when possible
  - marks invalid TDC packet framing
  - emits `hardware_run_audit.csv` and `hardware_run_audit.md`
- `scripts/capture_uart.ps1`
  - future captures will record bitstream SHA256 and throughput in metadata
- `scripts/fpga1_capture_required_bits.ps1`
  - default hw_server URL is now `localhost:3122`
  - automatically runs the audit script after a batch completes

## Immediate next experiment order

1. Repeat the key 10 MiB cases in interleaved order: `random1`, `random3`, `compact`, `sparse`, `far`.
2. Promote `row` and `random2` to 10 MiB because their smoke results show moderate bias.
3. Promote one or two good smoke cases, such as `checker` or `cross_region`, to 10 MiB as additional positive controls.
4. Repeat TDC near/far at least 3 times each, then add TDC placements that correspond more closely to `random1` and `random3`.

## Current caution

Do not overclaim yet. The strongest current claim is:

"On this FPGA1 board and current RTL, RO placement measurably changes raw TRNG bias, min-entropy, and output throughput. The strongest current evidence is the contrast between `random1_run01` and `random3_run01`: both are random-placement variants, but one has severe bias while the other is close to ideal."

The stronger claim:

"This is caused by RO coupling/locking observed through TDC phase correlation"

is not established yet. It requires more TDC placements, repeats, and correlation analysis.
