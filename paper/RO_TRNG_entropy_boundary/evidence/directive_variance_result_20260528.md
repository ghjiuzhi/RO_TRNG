# Directive-Controlled Route-Variance Result 20260528

Purpose: test whether the sampler-side forward counterfactual survives an independent Vivado implementation directive. This is not a seed-controlled experiment. The current Vivado 2023.2 non-project flow used here records implementation directives, not a true placement/routing seed.

## Build Scope

- RTL/top: compact diagnostic restart top.
- Warmup: 4 bytes.
- Implementation directives: place `Explore`, phys_opt `Explore`, route `Explore`.
- Variants:
  - compact baseline: compact sample-RO lock (`Scompact`)
  - forward fail: restart-oriented sample-RO lock (`Srestart`)

## Hardware Captures

| Variant | Run | Capture | SHA256 | XADC after |
| --- | --- | --- | --- | ---: |
| compact baseline | `restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528` | `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.bin` | `6F70F6BE63CC3A8D8EB02E38FE1A11FB5AD1BD373FA64C8C363A3DAE98BE7ABB` | 44.3 C |
| forward fail | `restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528` | `data/hardware/20260511_fpga1_board1/restart_fifo_diag/restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.bin` | `1C97A78710D12E6F477DBE61B3E3AF19ED05609BB94079B36638360FFB5AF5BE` | 44.9 C |

## Restart Analysis

| Variant | Overall p1 | Min-H | Row ones std | Worst byte.bit | Worst x | Worst p1 |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| compact baseline, W4, Explore | 0.496761000 | 0.990684362 | 15.475331305 | 3.3 | 560 | 0.440000000 |
| forward fail, W4, Explore | 0.375294000 | 0.678750709 | 15.459998836 | 2.2 | 796 | 0.204000000 |

Analysis outputs:

- `data/experiments/sample_ro_directive_variance_20260528/restart_fifo_compact_diag_compact_warmup4_1000x125_explore1_run01_20260528.summary.md`
- `data/experiments/sample_ro_directive_variance_20260528/restart_fifo_compact_diag_formal_sample_warmup4_1000x125_explore1_run01_20260528.summary.md`
- `data/experiments/sample_ro_directive_variance_20260528/sample_ro_directive_variance_20260528.csv`

## Routed Locality Audit

Source:

- `data/experiments/sample_ro_directive_variance_route_diff_20260528/sample_ro_route_evidence_summary_20260528.md`

| Pair | data-RO cells changed | sampled registers changed | sample-RO cells changed | data-RO net routes changed | sample-RO net routes changed | sampled-data net routes changed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| compact_w4_explore1 vs forward_w4_explore1 | 0/16 LOC, 0/16 BEL | 0/64 LOC, 0/64 BEL | 2/9 LOC, 3/9 BEL | 34/64 | 18/36 | 9/64 |

## Interpretation

The strongest outcome occurred: under an independent `Explore/Explore/Explore` implementation directive, the compact baseline remains near balanced while the restart-oriented sample-RO lock remains strongly biased. This supports that the sampler-side counterfactual is not merely one default implementation accident.

The interpretation remains bounded. The directive-controlled pair reproduces the useful cell-locality pattern, but data-RO, sample-RO, and sampled-data routes still change. Therefore this strengthens the claim that sampler-side physical implementation and local routed context shape restart behavior; it still does not prove sample-RO-only causality.
