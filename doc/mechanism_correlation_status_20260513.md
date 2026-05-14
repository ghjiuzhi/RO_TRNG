# TRNG placement vs RO frequency mechanism correlation status

Date: 2026-05-13

Scope: offline merge only. This status uses existing TRNG placement statistics and existing `random1/random3` fixed RO-frequency run01 CSV outputs. No Vivado, COM, JTAG, `hw_server`, or new hardware collection was run.

## Generated artifacts

- Script: `scripts/merge_trng_ro_freq_features.py`
- Merged CSV: `data/experiments/correlation/20260513_random1_random3_mechanism_correlation.csv`
- Human-readable summary: `data/experiments/correlation/20260513_random1_random3_mechanism_correlation.md`

The script reads:

- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_summary.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_pairwise_all_on.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/random1_random3_fixed_run01_2mib_pulling.csv`

## Current evidence table

| placement | TRNG abs bias | TRNG bit min-entropy | TRNG byte min-entropy | nearest data-data pair | min delta f MHz | sample shift ppm | data mean abs shift ppm |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| random1 | 0.162684488 | 0.593605945 | 4.80160868 | data4/data5 | 0.466194701 | +3466.912368 | 421.577455 |
| random3 | 0.000031435 | 0.999909299 | 7.98455010 | data3/data7 | 0.673395818 | -824.555525 | 478.085286 |

## What this supports for the paper

The current artifacts can support a compact mechanism-evidence table or paired bar/scatter-style case comparison:

- TRNG quality: `p1`, `abs_bias`, bit min-entropy, adjacent equal ratio, byte min-entropy.
- Close-frequency structure: nearest all-on data-data pair, `abs_delta_f_mhz`, beat period, and count of close pairs under 1 MHz / 3 MHz.
- Enable-dependent frequency shift: sample RO shift in ppm and MHz, plus data RO mean/max absolute shift.
- A combined figure caption can say that random1 and random3 are two matched run01 cases with sharply different TRNG quality and different RO-frequency mechanism signatures.

The safest claim is:

> In the two available matched cases, the biased random1 TRNG output coincides with a very close data-data RO pair and a large positive sample-RO all-on shift, while random3 remains near ideal despite also having a close pair. These observations motivate the close-pair and sample-relation mechanisms, but do not prove causality.

## What must not be over-interpreted

- Do not call the generated table a statistically significant correlation result. There are only two placement cases with matched TRNG and RO-frequency features.
- Do not report Pearson/Spearman coefficients, p-values, or regression significance from `random1/random3` alone.
- Do not claim that a close data-data pair is sufficient to explain TRNG failure. random3 has a close pair (`data3/data7`, 0.673 MHz) while its TRNG metrics are near ideal.
- Do not claim that stronger data RO pulling explains random1. The run01 data RO mean absolute shift is slightly larger for random3 than random1.
- Do not claim causal proof from fundamental frequency counters. The current files do not include phase locking, lag correlation, TDC phase histograms, or sampled XOR timing relationships.

## Next data needed for real correlation

To turn this into a statistical correlation figure, add more placements with the same merged feature columns:

- More placement families beyond random1/random3, especially cases already present in TRNG placement summaries.
- Repeated RO-frequency runs per placement to measure run-to-run stability of nearest pairs and sample shift.
- Sample-placement variants that keep data RO placement mostly fixed while moving the sample RO relation.
- TDC pair validation for anchor pairs such as random1 `data4/data5`, random1 `data0/data1`, and random3 `data3/data7`.

Once there are enough matched placements, the same script can be extended to emit Pearson/Spearman correlations with confidence intervals and an explicit sample count.
