# Sampler-Island Warmup10 Repeat02 Status 2026-05-26

## Purpose

Repeat the single-board `random1_sampler_island_local warmup10` strict restart run because the first strict run was a boundary case:

```text
repeat01: MSB failed with X_max=610 > cutoff 605,
          LSB passed with X_max=610 < cutoff 632.
```

This repeat tests whether the MSB/LSB split is stable or whether warmup10 is simply close to the restart cutoff boundary.

## Hardware Capture

Queue:

```text
data/experiments/fast_mode/hardware_queue_restart_sampler_island_w10_repeat02_20260526.csv
```

Capture:

```text
data/hardware/20260511_fpga1_board1/restart/restart_random1_sampler_island_local_warmup10_1000x125_strict_repeat02_20260526.bin
```

Result:

- bytes: `125008`
- header: `A55A03E8007D01D0`
- SHA256: `A1ADD4ABA6C9A111DAEFC84D677B6F6F62C6E90C201512F2FA8FFE0A53D1E199`
- XADC after: `46.3 C`, `VCCINT=1.000 V`, `VCCAUX=1.797 V`, `VCCBRAM=1.000 V`

## Repeat02 Analysis

Payload:

```text
data/experiments/restart_sampler_island_w10_repeat02_20260526/payloads/island_w10_repeat02.payload.bin
```

Profile:

| run | packed p1 | min-H | worst byte.bit | worst x | worst p1 |
| --- | ---: | ---: | --- | ---: | ---: |
| island w10 repeat02 | 0.458774 | 0.885697 | 4.4 | 599 | 0.401 |

SP800-90B restart:

| run | order | status | H_I | X_cutoff | X_max | min(Hr,Hc,Hi) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| island w10 repeat01 | MSB | fail | 0.902345 | 605 | 610 | - |
| island w10 repeat01 | LSB | pass | 0.828444 | 632 | 610 | 0.686477 |
| island w10 repeat02 | MSB | pass | 0.902345 | 605 | 599 | 0.706772 |
| island w10 repeat02 | LSB | pass | 0.828444 | 632 | 599 | 0.701080 |

## Interpretation

The original MSB/LSB split is not stable as a deterministic bit-order failure. Instead, `sampler_island_local warmup10` is a near-threshold passband-edge point:

- repeat01: `X_max=610`, slightly above the MSB cutoff `605`, below the LSB cutoff `632`;
- repeat02: `X_max=599`, below both cutoffs.

This is still mechanism-positive. It shows that sampler-island warmup10 lives close to the restart sanity boundary, while warmup4/5/11 are more clearly inside the pass region in the first strict matrix. The paper should describe warmup10 as a boundary/passband-edge window, not as a reproducible MSB-only failure.

## Paper Wording

Use:

```text
The sampler-island warmup10 point lies at the edge of the restart passband. In the first strict run it produced an MSB/LSB split because X_max=610 exceeded the MSB cutoff of 605 but remained below the LSB cutoff of 632; a targeted repeat moved X_max to 599 and passed both orders. This indicates a near-threshold startup window rather than a deterministic bit-order defect.
```

Avoid:

```text
warmup10 always fails in MSB but passes in LSB.
```
