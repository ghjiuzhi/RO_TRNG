# random1 regs-only Restart Failure-Mode Analysis 20260524

This is an offline synthesis of the SP800-90B restart warmup sweep and per-column bias diagnostics.
It separates fixed-column hotspots from global p1 shifts and passband behavior.

## Key Result

The restart pass/fail boundary is not mirrored by pairwise reset-enable TDC warmup-edge entropy.
Instead, the restart data itself shows a windowed output-position effect: warmups 5/6/8/10 form a restart-safe passband, while adjacent warmups fail through either fixed-column hotspots or global p1 shifts.

| warmup | status | mode | X_max | p1 mean | top positions |
| ---: | --- | --- | ---: | ---: | --- |
| 0 | failed | fixed_column_hotspot | 756-802 | 0.498785 | 1.6x2;1.7x2;0.0x2;1.4x1;1.2x1 |
| 4 | failed | global_bias | 733-751 | 0.407536 | 0.2x1;0.3x1;0.6x1;2.6x1;1.6x1;1.3x1 |
| 5 | passed | passband | 560-561 | 0.498248 | 111.2x1;47.0x1;100.2x1;15.5x1;104.4x1;121.0x1 |
| 6 | passed | passband | 551-554 | 0.496810 | 24.4x1;123.5x1;2.1x1;18.4x1;108.7x1;98.0x1 |
| 8 | passed | passband | 566-566 | 0.483511 | 0.3x1;40.6x1;114.4x1;91.3x1;83.0x1;16.2x1 |
| 10 | passed | passband | 554-565 | 0.499596 | 115.3x1;16.7x1;42.2x1;4.4x1;14.1x1;102.5x1 |
| 11 | failed | global_bias | 688-701 | 0.559007 | 81.4x1;90.2x1;96.5x1;41.1x1;57.2x1;86.4x1 |
| 12 | failed | global_bias | 601-609 | 0.452978 | 2.7x1;3.5x1;75.6x1;1.6x1;6.1x1;23.4x1 |
| 16 | failed | moderate_column_or_mixed_bias | 586-586 | 0.466933 | 60.3x1;92.0x1;52.7x1;67.3x1 |

## Interpretation

- Warmup0 fails mainly as fixed-column hotspot behavior: overall p1 is near 0.5, but X_max is extreme.
- Warmup4 and warmup11/12/16 fail mainly through global p1 shifts or mixed global/column effects.
- Warmup5/6/8/10 pass with X_max below cutoff, showing that the safe startup region is a passband rather than a monotonic delay effect.
- Existing pairwise TDC does not show a 4->5 or 10->11 entropy jump, so the passband is probably not a simple two-RO phase-diffusion threshold visible in raw TDC bins.
- The stronger mechanism is sampler-path/output-position dependent: sampling-register placement can repair steady-state stream quality, while restart robustness depends on which early sampled positions are emitted after reset.

## Next Hardware Target

The next meaningful hardware design should instrument the true TRNG sampling path rather than another isolated two-RO TDC pair. Two good options:

1. A restart-position diagnostic top that emits early sampled bytes plus row/position markers for warmup 4/5/10/11.
2. A sampler-register diagnostic top that exposes selected sampled_data lanes or per-stage XOR groups around the 64 sampling registers.

Both are better aligned with the current evidence than broad repeat captures.

- CSV: `data\experiments\sampler_regs_only_20260524\random1_sampler_regs_only_restart_mode_summary_20260524.csv`
