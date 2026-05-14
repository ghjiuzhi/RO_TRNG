# Fast Mode Results Summary 20260514

This is an offline post-analysis summary. It reads existing CSV/bin-derived analysis outputs only; it does not access hardware, Vivado, COM, JTAG, or hw_server.

## Evidence labels

- `statistical_comparison`: repeated-run or placement-matrix aggregates where the table reports mean/std or a repeated observation set.
- `case_comparison`: single-run baseline/case observations, including the original fpga1 baseline and the RO_FREQ 5MiB case. These should not be written as population statistics.

## One-command rerun

```powershell
python scripts\analyze_fast_mode_results.py
```

The fast hardware queue also calls this script during post-analysis after its existing RO_FREQ/TRNG refresh steps.

## Statistical comparisons

- RO_FREQ `run01_run02_run03_repeat` `random1` `closest_abs_delta_f_mhz_mean` = 0.594853203 MHz (n=3; std=0.111430425).
- RO_FREQ `run01_run02_run03_repeat` `random1` `sample_shift_ppm_vs_single_mean` = 345.30715 ppm (n=3; std=2722.7504).
- RO_FREQ `run01_run02_run03_repeat` `random3` `closest_abs_delta_f_mhz_mean` = 0.654329889 MHz (n=3; std=0.0188688461).
- RO_FREQ `run01_run02_run03_repeat` `random3` `sample_shift_ppm_vs_single_mean` = -51.0050737 ppm (n=3; std=677.249376).
- TDC `near_far_repeat_runs` `far` `diff_std_ps_mean` = 1918.04285 ps (n=2; std=3.88619997).
- TDC `near_far_repeat_runs` `far` `phase_pearson_r_mean` = -0.000450586268  (n=2; std=0.00389340702).
- TDC `near_far_repeat_runs` `far` `seq_gaps_mean` = 21.5  (n=2; std=30.4055916).
- TDC `near_far_repeat_runs` `near` `diff_std_ps_mean` = 1736.94713 ps (n=3; std=331.265498).
- TDC `near_far_repeat_runs` `near` `phase_pearson_r_mean` = 0.00170171163  (n=3; std=0.00164183139).
- TDC `near_far_repeat_runs` `near` `seq_gaps_mean` = 682.666667  (n=3; std=1182.41335).
- TRNG `placement_matrix_formal_10mib` `all_non_original_placements` `abs_bias_mean` = 0.0242304766  (n=10; std=0.0502363689; min=random3:3.14354897e-05; max=random1:0.162684488).
- TRNG `placement_matrix_formal_10mib` `all_non_original_placements` `bit_min_entropy_mean` = 0.936974344  (n=10; std=0.12563009; min=random1:0.593605945; max=random3:0.999909299).
- TRNG `placement_matrix_formal_10mib` `all_non_original_placements` `byte_min_entropy_mean` = 7.46673069  (n=10; std=0.979313239; min=random1:4.80160868; max=random3:7.9845501).
- TRNG `placement_matrix_formal_10mib` `all_non_original_placements` `runs_p_mean` = 0.131708449  (n=10; std=0.228633796; min=far:0; max=cross_region:0.719841022).

## Case comparisons

- RO_FREQ `closest_all_on_data_data_beat` `random1` `run01_5mib` `closest_abs_delta_f_mhz` = 0.459446433 MHz.
- RO_FREQ `closest_all_on_data_data_beat` `random3` `run01_5mib` `closest_abs_delta_f_mhz` = 0.50420572 MHz.
- RO_FREQ `sample_all_on_vs_single_on_pulling` `random1` `run01_5mib` `sample_shift_ppm_vs_single` = 4067.32825 ppm.
- RO_FREQ `sample_all_on_vs_single_on_pulling` `random3` `run01_5mib` `sample_shift_ppm_vs_single` = 1112.71136 ppm.
- TRNG `original_fpga1_baseline` `original_fpga1` `original_fpga1_repeat02_5mib` `abs_bias` = 0.000216960907 .
- TRNG `original_fpga1_baseline` `original_fpga1` `original_fpga1_repeat02_5mib` `bit_min_entropy` = 0.999374119 .
- TRNG `original_fpga1_baseline` `original_fpga1` `original_fpga1_run01_10mib` `abs_bias` = 3.58939171e-05 .
- TRNG `original_fpga1_baseline` `original_fpga1` `original_fpga1_run01_10mib` `bit_min_entropy` = 0.9998964357649321 .

## Original fpga1 baseline

- `original_fpga1_repeat02_5mib` bit min-entropy = 0.999374119 (case comparison).
- `original_fpga1_run01_10mib` bit min-entropy = 0.9998964357649321 (case comparison).

## Output files

- `data/experiments/fast_mode/fast_mode_results_20260514.csv`
- `data/experiments/fast_mode/fast_mode_results_20260514.md`
