# Claims vs Evidence

| claim | evidence_table | key_number | status | caveat |
| --- | --- | --- | --- | --- |
| Placement changes TRNG quality under fast-mode captures | table_placement_trng_repeats.csv/md | formal bit_min_entropy_mean min=0.593606; max abs_bias_mean=0.162684 | supported, with weak placements explicitly visible | fast-mode dataset; not a substitute for full SP800-90B certification |
| Repeat captures are broadly consistent at placement level | table_placement_trng_repeats.csv/md | max formal-repeat bit_min_entropy_mean delta=0.00841786 | supported for available repeats | some placements have repeat-only rows and are excluded from paired delta |
| All-on operation measurably pulls RO frequencies | table_ro_freq_pulling_summary.csv/md | max \|sample_shift_ppm\|=3466.91; max data_mean_abs_ppm=478.085 | supported | summarizes random1/random3 RO_FREQ run only |
| The six monitored TDC RO pairs do not show strong phase locking | table_tdc_pair_dynamics_summary.csv/md | max small-lag \|r\|=0.0317827; strong_lock_windows=0 | negative/null evidence for strong locking | does not rule out coupling under other placements, voltage, temperature, or longer captures |
