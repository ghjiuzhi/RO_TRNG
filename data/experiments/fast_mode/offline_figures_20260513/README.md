# Fast Mode Offline Figures Index

Generated from existing CSV analysis files only. No hardware, Vivado, COM, JTAG, or hw_server access is used.

## Key Outputs

- `table_trng_formal_fast_metrics.csv/md`: monobit, runs, adjacent, bit/byte min-entropy table.
- `table_trng_repeat_by_placement.csv/md`: formal/repeat placement aggregate table.
- `table_ro_freq_closest_beats.csv/md`: closest all-on data/data beat pairs.
- `table_ro_freq_pulling_summary.csv/md`: all-on vs single-on pulling summary.
- `table_tdc_diff_phase_metrics.csv/md`: TDC diff_std, phase_r, entropy, used-bin metrics.
- `figure_data_tdc_code_density.csv`: code-density rows for TDC figures.

## Quick Reading

- TRNG bit min-entropy spans `0.593606` (random1) to `0.999909` (random3).
- RO_FREQ closest `random1` all-on data/data pair is `data4/data5` with delta `0.466195 MHz`.
- RO_FREQ closest `random3` all-on data/data pair is `data3/data7` with delta `0.673396 MHz`.
- RO_FREQ `random1` sample pulling is `3466.91 ppm`.
- RO_FREQ `random3` sample pulling is `-824.556 ppm`.
- TDC `tdc_near_run02` has diff_std `1927.59 ps` and phase_r `0.00327627`.
- TDC `tdc_far_run01` has diff_std `1915.29 ps` and phase_r `0.00230247`.
