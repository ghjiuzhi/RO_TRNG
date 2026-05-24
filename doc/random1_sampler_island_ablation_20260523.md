# random1 Sampler-Island Ablation 20260523

- goal: test whether `random1` degradation is driven by the sample RO / sampler relationship rather than by simple data-data RO locking
- board: `z7020_b01`
- UART: `COM3`, `115200`
- XADC during new captures: about `45.9 C` to `46.4 C`, `VCCINT=1.000 V`, `VCCAUX=1.796-1.797 V`

## Why This Experiment

The 12 pair-specific TDC captures did not show strong data-data RO locking. That weakens the simple "bad placement means two ROs lock" story. The next stronger hypothesis is that the sample RO is an active part of the entropy source: moving the sample RO changes the sampled phase ensemble and therefore changes output bias.

This experiment keeps the `random1` data RO placement and changes the sampler side:

1. `random1_baseline`: original `random1` data placement and original sample position.
2. `random1_sample_ro_local_x45y39`: same data ROs, only the sample RO is moved near the data-RO region.
3. `random1_sampler_island_local_x45y39_regs_x45y31`: same as 2, plus the 64 sampling registers are constrained into a local island.

## Main Result

| experiment | bytes | p1 | bit min-entropy | adjacent equal | sample shift |
| --- | ---: | ---: | ---: | ---: | ---: |
| `random1_baseline_5mib` | 5MiB | 0.337669 | 0.594377 | 0.556683 | +3855.97 ppm |
| `random1_sample_ro_local_x45y39_20mib_programmed` | 20MiB | 0.484799 | 0.956792 | 0.501911 | -466.04 ppm |
| `random1_sampler_island_local_x45y39_regs_x45y31_20mib_programmed` | 20MiB | 0.500051 | 0.999854 | 0.499982 | -466.04 ppm |
| `random3_good_reference_5mib` | 5MiB | 0.499971 | 0.999917 | 0.499848 | reference |

The result supports the sample-RO coupling / sampling-relationship hypothesis:

- Moving only the sample RO improves `random1` substantially: `p1` moves from about `0.338` to `0.485`, and bit min-entropy rises from about `0.594` to `0.957`.
- Moving the sampling registers as well improves the same fixed-data placement further: the programmed 20MiB confirmation is near ideal (`p1=0.500051`, bit min-entropy `0.999854`).
- The RO_FREQ control agrees with the TRNG change: the same-session baseline sample RO has strong positive all-on shift (`+3855.97 ppm`), while the local sample RO has weak negative shift (`-466.04 ppm`).

Important data-quality note: the early 5MiB captures named without `program` were collected with `capture_uart.ps1`, which does not program the bitstream first. They are useful as debugging history only and should not be used for causal claims. The causal rows above use `program_and_capture_uart.ps1`, or the explicitly programmed 20MiB sample-only capture metadata.

## Interpretation

This is currently the strongest mechanism evidence in the project. It says that `random1` was not bad only because of data-data RO locking. Instead, changing the sample RO location alone changes both the measured sampler pulling and the observed output bias; additionally constraining the sampling registers locally removes the residual bias in the 20MiB confirmation.

The sample-only effect does not fully recover `random1` to the `random3` quality level, so the paper should not claim the sample RO explains everything. The sampler-island result suggests the sampling register/routing side may be the missing part. A better claim is:

> Sample-RO placement is a causal control knob for placement-dependent bias. It explains a large part of the random1 degradation, while residual bias likely comes from the data-RO ensemble and routing/beat structure.

After the programmed sampler-island result, this can be sharpened to:

> The sampler path is a physical part of the entropy source, not only a readout path. Holding the data-RO placement fixed, changing the sampler-side placement moves the output from a biased source to a near-ideal continuous stream.

## Stability Check

The 20MiB sampler-island confirmation is stable across windows:

- 1MiB windows: `p1` ranges from `0.499794` to `0.500288`.
- 5MiB windows: `p1` ranges from `0.499994` to `0.500106`.
- 5MiB window bit min-entropy stays above `0.999695`.
- 5MiB adjacent-equal ratio stays close to `0.5` (`0.499903` to `0.500049`).

XADC for the 20MiB run: `46.0 C -> 46.3 C`, `VCCINT=1.000 V`, `VCCAUX=1.796 V -> 1.794 V`.

## 20260524 regs-only Update

A stricter ablation was added after this document was first written: `random1_sampler_regs_only_x45y31`.
This variant keeps the sample RO at the baseline site and constrains only the 64 sampling registers/routing island.
It nearly fixes the 20MiB continuous stream:

- `p1=0.499809736`
- bit min-entropy `0.999451119`
- adjacent-equal ratio `0.501785037`
- XADC `47.4 C -> 47.4 C`, `VCCINT=1.000 V`

The same variant was then tested with SP800-90B restart auto-stream datasets at `1000 x 125` packed bytes, expanded to `1000 x 1000` bit symbols.
Both `warmup0` and `warmup12` failed restart sanity across two repeats:

| variant | warmup | repeats | result | key observation |
| --- | ---: | ---: | --- | --- |
| `random1_sampler_regs_only_x45y31` | 0 | 2 | failed | overall p1 near 0.499, but fixed early-column hotspots with `X_max=756` and `802` over cutoff `572` |
| `random1_sampler_regs_only_x45y31` | 12 | 2 | failed | worst-column strength drops to `609` and `601`, but global p1 shifts low to about `0.452-0.454` |

This sharpens the interpretation. Sampling-register/routing placement is sufficient to repair steady-state continuous bias, proving that sampler-side physical implementation is part of the entropy-source boundary. However, restart startup behavior is a separate requirement: the source can look near ideal in a long continuous stream while still failing fixed-position restart sanity.

The paper should therefore use a layered mechanism claim:

> The sampler path controls steady-state placement-dependent bias, while reset/startup transients control restart robustness. Continuous non-IID quality alone does not imply SP800-90B restart robustness.

## Files

- Summary table: `data/experiments/sampler_island_20260523/random1_sampler_island_ablation_summary.csv`
- Sample RO local XDC: `data/experiments/xdc_sampler_island/random1_sample_ro_local_x45y39.xdc`
- Sampler island XDC: `data/experiments/xdc_sampler_island/random1_sampler_island_local_x45y39_regs_x45y31.xdc`
- Sample RO local bitstream: `data/vivado_runs/fpga1_sampler_island/random1_sample_ro_local_x45y39/seed_1/RO_TRNG_top.bit`
- Sampler island bitstream: `data/vivado_runs/fpga1_sampler_island/random1_sampler_island_local_x45y39_regs_x45y31/seed_1/RO_TRNG_top.bit`
- RO_FREQ sample local bitstream: `data/vivado_runs/fpga1_ro_freq_probe_fixed/random1_seed1_x36y35_sample_x45y39_w100/RO_FREQ_trng_probe_top.bit`

## Next Step

The 20MiB sampler-island and regs-only confirmations should become main paper figures. The next useful hardware step is a targeted startup/restart investigation, not another broad continuous-stream repeat: compare restart traces and reset-aligned TDC around the first few byte/bit positions that become hotspots in regs-only warmup0 and warmup12.
