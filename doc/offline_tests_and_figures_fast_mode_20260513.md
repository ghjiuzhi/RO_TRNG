# Fast Mode Offline Tests and Figures

Date: 2026-05-13

Scope: offline analysis only. Do not program hardware, do not run Vivado, do
not access COM/JTAG/hw_server. This note prepares the fast-mode standard tests,
paper table/figure data, and handoff commands from existing CSV analysis files.

## Inputs Read

- `scripts/analyze_trng_dataset.py`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.md`
- `data/hardware/20260511_fpga1_board1/trng/trng_formal_all_10mib_ranked.csv`
- `data/hardware/20260511_fpga1_board1/trng/trng_repeats_by_placement.csv`
- `data/experiments/ro_freq_analysis/20260513_random1_random3_fixed_run01_2mib/*_{summary,pairwise_all_on,pulling}.csv`
- `data/hardware/20260511_fpga1_board1/tdc/tdc_near_far_compare.csv`
- `data/hardware/20260511_fpga1_board1/tdc/analysis_tdc_*/*.tdc_{metrics,bins}.csv`

## Existing TRNG Test Coverage

`scripts/analyze_trng_dataset.py` is already suitable for the fast offline
standard-test layer. It uses only the Python standard library and computes:

- monobit: `p1`, `zeros`, `ones`, `monobit_z`, `monobit_p`
- runs: total `runs`, approximate `runs_p`
- adjacent correlation proxy: `adjacent_equal_ratio`
- min-entropy: bit-level `bit_min_entropy` and byte-level `min_entropy_byte`
- byte Shannon entropy: `shannon_entropy_byte`
- longest runs: `longest_zero_run`, `longest_one_run`

Recommended offline commands when raw captures are present:

```powershell
python scripts\analyze_trng_dataset.py `
  data\hardware\20260511_fpga1_board1\trng `
  --glob *.DAT `
  --out-dir data\hardware\20260511_fpga1_board1\trng\analysis_refresh_fast_20260513
```

For paper tables in fast mode, prefer the already consolidated CSVs instead of
re-reading raw binaries unless a capture was newly completed:

- `trng_formal_all_10mib_ranked.csv` for the main 10MiB formal result table.
- `trng_repeats_by_placement.csv/md` for formal-vs-repeat reproducibility.

Key current readings:

- `random1` is the strongest negative example: `p1=0.337315512`,
  `bit_min_entropy=0.593605945`, `adjacent_equal_ratio=0.556739754`.
- `random3` is the best current formal sample by bit min-entropy:
  `p1=0.499968565`, `bit_min_entropy=0.999909299`,
  `adjacent_equal_ratio=0.500072473`.
- `same_column` has near-ideal balance but abnormal runs/adjacent behavior:
  report `runs_p` and adjacent metrics, not only `p1`.

## Added Figure/Table Script

New script:

```text
scripts/make_fast_mode_figures.py
```

It reads existing CSVs and writes paper-ready CSV/Markdown tables plus simple
SVG previews. It does not use pandas, matplotlib, Vivado, COM, JTAG, or
hw_server.

Default command:

```powershell
python scripts\make_fast_mode_figures.py
```

Default output directory:

```text
data/experiments/fast_mode/offline_figures_20260513
```

Useful options:

```powershell
python scripts\make_fast_mode_figures.py `
  --out-dir data\experiments\fast_mode\offline_figures_20260513 `
  --top-n-beats 4
```

## Generated Outputs

The script was run once successfully in offline mode and generated:

- `README.md`
- `table_trng_formal_fast_metrics.csv/md`
- `table_trng_repeat_by_placement.csv/md`
- `table_ro_freq_closest_beats.csv/md`
- `table_ro_freq_pulling_summary.csv/md`
- `table_tdc_diff_phase_metrics.csv/md`
- `figure_data_ro_freq_summary_all_on.csv`
- `figure_data_tdc_code_density.csv`
- `fig_trng_bit_min_entropy.svg`
- `fig_trng_abs_bias.svg`
- `fig_trng_adjacent_deviation.svg`
- `fig_ro_freq_closest_beats.svg`
- `fig_ro_freq_sample_pulling_ppm.svg`
- `fig_tdc_diff_std_ps.svg`
- `fig_tdc_phase_pearson_r.svg`
- `fig_tdc_code_density_tdc_near_run02.svg`
- `fig_tdc_code_density_tdc_far_run01.svg`

## RO_FREQ Figure Logic

Inputs:

- `*_summary.csv`: per-family/per-target frequency mean/std in all-on and
  single-on modes.
- `*_pairwise_all_on.csv`: all-on pairwise frequency deltas and beat periods.
- `*_pulling.csv`: `all_on_freq_mhz - single_on_freq_mhz` per target.

Generated table priorities:

- closest all-on data/data beats, sorted by `abs_delta_f_mhz`
- pulling summary, including data RO shift range/mean and sample shift ppm

Current run01 readings:

| family | closest all-on data/data pair | delta MHz | beat period ns | sample pulling ppm |
| --- | --- | ---: | ---: | ---: |
| random1 | data4/data5 | 0.466195 | 2145.03 | +3466.91 |
| random3 | data3/data7 | 0.673396 | 1485.01 | -824.56 |

Interpretation boundary: closest beat and pulling are mechanism evidence, not
causal proof. `random3` also has a close data/data pair, so "close pair exists"
alone cannot explain the `random1` TRNG bias.

## TDC Figure Logic

Inputs:

- `tdc_near_far_compare.csv`
- `analysis_tdc_*/*.tdc_metrics.csv`
- `analysis_tdc_*/*.tdc_bins.csv`

Generated table priorities:

- `diff_std_ps`
- `bin_pearson_r` and `phase_pearson_r`
- lane code entropy/min-entropy
- used/dead bins
- code-density figure data: bin, count, probability, width, DNL, INL,
  phase center

Current baseline readings:

| run | packets | seq gaps | diff_std_ps | phase_r | used bins A/B |
| --- | ---: | ---: | ---: | ---: | --- |
| tdc_near_run02 | 262143 | 0 | 1927.59 | 0.003276 | 63/63 |
| tdc_far_run01 | 262132 | 43 | 1915.29 | 0.002302 | 73/73 |

Interpretation boundary: these are near/far TDC baseline runs. They validate
the offline metric path and code-density reporting, but they are not the
pair-specific random1/random3 TDC mechanism result.

## Fast-Mode Paper Figure Set

Recommended minimum set:

1. Table: TRNG formal 10MiB metrics with `p1`, monobit/runs p-values,
   adjacent-equal ratio, bit min-entropy, byte min-entropy.
2. Figure: bit min-entropy by placement.
3. Figure: absolute bit bias by placement.
4. Figure: adjacent-equal deviation from 0.5 by placement.
5. Table/Figure: RO_FREQ closest all-on data/data beat pairs.
6. Table/Figure: RO_FREQ all-on vs single-on pulling, especially sample shift.
7. Table/Figure: TDC baseline `diff_std_ps` and `phase_pearson_r`.
8. Figure data: TDC code-density probability/DNL/INL from `figure_data_tdc_code_density.csv`.

## Standard-Test Next Layer

For a formal standards appendix, keep the current lightweight tests separate
from full standard suites:

- Current fast-mode layer: monobit, runs, adjacent-equal proxy, bit/byte
  min-entropy from `analyze_trng_dataset.py`.
- Optional offline-only standards layer: NIST STS and SP800-90B entropy
  assessment on selected raw captures. Run only against local files, never as
  part of a hardware queue.
- Report raw-source tests and post-processed-output tests separately.

Suggested sample selection for full offline standards runs:

- `random1_run01`: strongest failure case.
- `random3_run01`: strongest high-quality random-placement contrast.
- `same_column_run01`: balanced but adjacent/runs-suspicious case.
- `compact_run01` or `cross_region_run02`: high-quality structured layout.
- matching 5MiB repeat files where available, reported as repeat support rather
  than replacing 10MiB formal results.

## Reproducibility Notes

- The new figure script is deterministic for a fixed set of CSV inputs.
- Outputs are derived data; regenerate after any new hardware queue row is
  analyzed into CSV.
- Do not mix incomplete/partial captures into the formal 10MiB table.
- Do not claim TDC causality until random1/random3 pair-specific TDC data is
  collected and joined with RO_FREQ/TRNG features.
