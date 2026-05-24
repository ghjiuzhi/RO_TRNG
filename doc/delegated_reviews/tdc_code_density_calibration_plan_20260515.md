# TDC Code-Density Calibration Plan

Date: 2026-05-15

Scope: offline design review only. No hardware, Vivado programming, COM3, JTAG,
or hw_server access was used or required.

Input material reviewed:

- `rtl/tdc/*.v`
- `scripts/analyze_tdc_uart.py`
- `scripts/analyze_tdc_pair_dynamics.py`
- `doc/tdc_pair_validation_plan_20260513.md`
- `doc/tdc_pair_fast_mode_status_20260514.md`

## Executive Recommendation

The existing TDC pair captures can be used for per-run, per-lane code-density
post-processing, and the current scripts already do that. They are sufficient
for the current negative statement: no strong zero-lag or small-lag pair locking
was detected in the six 2 MiB pair captures after code-density phase mapping.

They are not sufficient for a strong paper claim that the TDC has an independent,
validated code-density calibration. The current captures use the RO pair itself
as the phase stimulus, so the histogram mixes TDC bin width, RO phase dynamics,
possible coupling, dead codes, and edge-distribution bias. For a publishable
"calibrated TDC" result, add a dedicated calibration bitstream/mode that drives
each TDC lane with a known asynchronous free-running calibration oscillator or
phase-sweep source, captures much larger histograms, and then reuses the
resulting lookup table for pair runs.

Recommended wording split:

- Current paper result: "TDC codes were mapped to phase using per-run
  code-density normalization; this removes first-order nonuniform bin width
  effects for within-run comparisons but is not an independent TDC calibration."
- Future/stronger result after the extra mode: "A dedicated asynchronous
  code-density calibration was used to estimate per-bin widths for each TDC
  lane; pair measurements were then converted from raw code to calibrated phase
  using the fixed lookup table."

## What the Existing RTL Actually Measures

The TDC lane is a 16-CARRY4 chain:

- `carry4_tdc_chain.v`: `CARRY4_NUM = 16`, `TAP_NUM = 64`.
- `tdc_sampler.v`: samples the 64 carry taps on `clk_200m`.
- `tdc_bubble_correct.v`: applies a local majority-style correction and flags
  bubbles.
- `tdc_encoder.v`: outputs the count of one bits, not a thermometer transition
  index.
- `tdc_lane.v`: registers corrected thermometer state, encoded bin, sample
  valid, bubble, empty, and full flags.

Important consequence: although `BIN_W = 8` and the UART packet carries one
byte per lane, the physical encoded range is effectively `0..64` for the
default 64 taps. Codes above 64 are structurally unreachable unless the RTL
parameters change. Existing analysis commonly uses `bins=256`, which is
conservative for the 8-bit packet field but produces many structural dead bins.
For TDC-quality reporting, show both:

- packet code space: 256 possible byte values;
- physical code space: 65 possible ones-count values, `0..64`, with `0` and
  `64` also serving as empty/full boundary indicators.

The packetizer in `RO_TDC_pair_sysclk_top.v` uses `clk_200m` and
`SAMPLE_DIV = 5000`, so one packet is emitted roughly every 5001 cycles of the
200 MHz clock, subject to UART backpressure. The phase span for code-density
mapping is the 200 MHz sample period:

`Tclk = 5000 ps`

The current pair top instantiates two 2-stage ROs (`RO_A_STAGES = 2`,
`RO_B_STAGES = 2`) and maps their edge snapshots to `bin_a` and `bin_b`.

## Existing Data Status

The completed pair-specific captures are:

| run | packets | seq gaps | diff std ps | phase r |
| --- | ---: | ---: | ---: | ---: |
| `tdc_pair_random1_ro4_ro5_run01_2mib` | 262143 | 124 | 2041.510 | -0.001195 |
| `tdc_pair_random1_ro0_ro1_run01_2mib` | 262142 | 67 | 2042.904 | -0.002491 |
| `tdc_pair_random1_ro2_ro4_run01_2mib` | 262138 | 122 | 2042.290 | -0.002237 |
| `tdc_pair_random3_ro3_ro7_run01_2mib` | 262142 | 120 | 2040.448 | -0.0000368 |
| `tdc_pair_random3_ro3_ro5_run01_2mib` | 262143 | 4 | 2040.263 | -0.0000203 |
| `tdc_pair_random3_ro0_ro6_run01_2mib` | 262143 | 8 | 2041.957 | -0.001465 |

The refreshed dynamic analysis reports 96 windows, zero strong-lock windows,
maximum absolute zero-lag window phase correlation about `0.017`, and maximum
absolute small-lag correlation about `0.032`.

Code-density artifacts visible in the current `.tdc_metrics.csv` files:

- analysis uses `bins=256` and `clock_period_ps=5000`;
- each lane uses only about 57 to 67 bins out of 256;
- each lane therefore reports about 189 to 199 dead bins;
- `peak_abs_inl_lsb` is around 191 to 195 when expressed over the 256-code
  packet space, dominated by structural dead bins;
- `flag_nonzero_ratio` is `1.0` because bit 7 of `flags` is the normal
  `vld_a & vld_b` valid bit, so this field should not be interpreted as an
  error ratio.

This is acceptable for current relative phase mapping, but not a clean TDC
linearity calibration.

## Can the Existing Data Do Code-Density Calibration?

Yes, for limited within-run post-processing:

- The current `scripts/analyze_tdc_uart.py` already builds one histogram per
  lane, converts counts to `width_ps`, computes DNL/INL, and maps each raw code
  to `phase_center_ps`.
- The pair dynamics script also builds full-run code-density phase lookups and
  reuses them across windows.
- This is enough to avoid comparing raw bin standard deviation directly across
  lanes or builds.
- It supports the current negative conclusion that the tested pair data show no
  strong phase correlation after first-order phase normalization.

No, for independent calibration:

- Code-density calibration assumes the input phase is uniformly distributed
  across one sample-clock period.
- In the existing pair captures, the input phase distribution is generated by
  the same ROs under investigation.
- If a pair is frequency-pulled, weakly locked, slowly drifting, or sampled with
  an aliased beat relation, the histogram is no longer only a TDC bin-width
  measurement.
- Per-run calibration can also remove or hide some low-frequency nonuniformity
  that may itself be part of the mechanism under study.
- A single run per pair is not enough to separate stable TDC bin width from
  run-specific RO dynamics, voltage/temperature drift, or placement-dependent
  routing changes.

Therefore, use existing data as "code-density normalized pair measurements",
not as "independently calibrated TDC measurements."

## What to Capture Next

### Required New Bitstream or Mode

Add a dedicated calibration top or selectable mode with these properties:

1. Keep the same TDC lane RTL, CARRY4 count, sampling clock, UART packet format,
   and intended TDC placement policy as the pair measurement bitstreams.
2. Drive one or both `hit_i` inputs from calibration oscillators that are not
   the investigated RO pair.
3. Make the calibration source asynchronous to `clk_200m`, free-running, and
   frequency-offset enough that the sampled phase walks through the whole 5 ns
   period.
4. If possible, support lane modes:
   - lane A calibration source into TDC A, lane B calibration source into TDC B;
   - swapped source/lane mode to distinguish source bias from lane bin width;
   - optional common-source split mode to measure lane-to-lane offset and
     common-mode response.
5. Preserve manifest fields: bitstream path, top, git commit if available,
   lane mode, CARRY4 placement policy, calibration source type/frequency,
   board id, capture size, temperature/voltage note, and SHA-256.

The smallest practical RTL option is a sibling top such as
`RO_TDC_code_density_cal_sysclk_top.v` that reuses `tdc_lane` and
`tdc_uart_packetizer`, but instantiates calibration ROs instead of the
random1/random3 pair ROs. A mode-selectable top is also acceptable if it does
not disturb the measured pair placement or timing.

### Data Volume

For current 65 physical codes, 2 MiB gives about 262k packets, or roughly 4k
samples per physical code if phase coverage is uniform. That is enough for a
smoke-level lookup and obvious dead-code detection.

For a publication-quality calibration, capture more:

- minimum useful calibration: 2 MiB per lane/mode;
- recommended calibration: 8 to 16 MiB per lane/mode;
- repeatability check: at least 3 repeats for one representative build or one
  repeat before and after the pair measurement sequence;
- if keeping the 256-code packet-space report, target at least 1k counts per
  reachable physical code and state that unreachable byte values are structural
  dead codes.

At 8 MiB, each lane has about 1,048,576 packets. Over 65 physical codes, the
ideal count is about 16k per physical code, giving roughly 0.8% Poisson relative
uncertainty for well-populated bins. At 16 MiB, it is about 0.6%. This is a much
cleaner basis for DNL/INL tables than the current pair captures.

### Pair Data to Keep or Add

Keep the six existing pair captures as the first mechanism screen. Do not
discard them. They already show no strong pair locking under the tested
condition.

If extra hardware time is available after calibration, collect:

- one repeat of the strongest random1 suspect pair: `random1 RO4/RO5`;
- one repeat of a good-family low-beat control: `random3 RO3/RO7`;
- one far/spatial control in each family, if not already represented by the
  selected pair list;
- data-RO versus sample-RO TDC mode, because the status note says random1
  degradation coincides more strongly with close RO frequencies and abnormal
  sample-RO pulling than with observed data/data zero-lag locking.

## Counts to Bin Width and ps Mapping

For each lane and each calibration run:

1. Decode frames:
   `0xA5, seq[15:0], coarse_lsb[15:0], bin_a, bin_b, flags`.
2. Filter or stratify frames:
   - require sequence continuity for the main calibration table;
   - require valid bit set;
   - report bubble, empty, and full rates separately;
   - do not treat `flags != 0` as an error, because valid frames set bit 7.
3. Choose code space:
   - for packet compatibility: `N = 256`;
   - for physical TDC reporting: `N = TAP_NUM + 1 = 65`.
4. Build counts `C[k]` for each code `k`.
5. Let `Ctot = sum_k C[k]`, `Tclk_ps = 5000`.
6. Estimate bin width:
   `width_ps[k] = C[k] / Ctot * Tclk_ps`.
7. Ideal width:
   `ideal_width_ps = Tclk_ps / N`.
8. DNL:
   `DNL[k] = C[k] / (Ctot / N) - 1`.
9. INL:
   `INL[k] = sum_{i=0..k} DNL[i]`.
10. Phase lower edge:
    `edge_ps[0] = 0`,
    `edge_ps[k+1] = edge_ps[k] + width_ps[k]`.
11. Phase center lookup:
    `phase_center_ps[k] = edge_ps[k] + 0.5 * width_ps[k]`.
12. Convert samples:
    `phase_a_ps[n] = LUT_A[bin_a[n]]`,
    `phase_b_ps[n] = LUT_B[bin_b[n]]`.
13. For differences, use a circular or modulo-aware phase difference when the
    statistic is about phase separation:
    `diff_ps = wrap_to_pm_half_period(phase_a_ps - phase_b_ps, Tclk_ps)`.
    The current script uses direct subtraction, which is fine for continuity
    with existing tables but should be marked as non-circular.

For current pair-capture post-processing, build `LUT_A` and `LUT_B` from the
same run and describe it as per-run normalization. For dedicated calibration,
build `LUT_A` and `LUT_B` from calibration captures and apply the fixed LUTs to
the pair captures.

## Script and Reporting Adjustments

No RTL change is required to document the current result. For future analysis,
update or wrap the scripts to make the calibration status explicit:

- add `--physical-bins 65` or equivalent reporting mode;
- keep `--bins 256` only for packet-space compatibility;
- add `valid_ratio`, `bubble_ratio`, `empty_ratio`, and `full_ratio` instead of
  relying on `flag_nonzero_ratio`;
- write whether the LUT source is `same-run`, `dedicated-calibration`, or
  `external-fixed`;
- optionally add circular phase-difference statistics alongside the existing
  direct `phase_a - phase_b` metrics;
- save one calibration manifest per LUT file.

## Paper Wording

### If Only the Existing Data Are Used

Use conservative wording:

> The UART TDC records were converted from raw code to phase using per-lane
> code-density normalization over each run. This compensates first-order
> nonuniformity of the sampled code distribution for within-run comparisons.
> Because the same RO pair provides both the measurement stimulus and the
> histogram used for normalization, these results should be interpreted as
> code-density-normalized TDC observations rather than an independently
> calibrated TDC transfer function.

For the result:

> Across the six pair-specific 2 MiB captures, the code-density-normalized TDC
> phase correlations remained near zero and no window exceeded the conservative
> small-lag locking screen. Thus, the tested data/data RO pairs did not show a
> strong TDC-level phase-locking signature under this setup.

Avoid:

- "fully calibrated TDC";
- "absolute ps-accurate bin widths";
- "pair coupling ruled out";
- "locking cannot occur".

### After Dedicated Calibration Is Captured

Then stronger wording is defensible:

> A dedicated asynchronous code-density calibration was performed for each TDC
> lane using the same carry-chain sampling path and 200 MHz sampling clock as
> the pair measurements. Per-bin widths were estimated from the calibration
> histograms and used to construct fixed lane-specific code-to-phase lookup
> tables. Pair captures were then analyzed in calibrated phase units using
> these lookup tables, with dead bins, DNL, INL, and flag rates reported for
> each calibration run.

Even then, keep mechanism language cautious:

> The calibrated pair measurements constrain the simple phase-locking
> hypothesis, but they do not exclude coupling mechanisms that appear only under
> different supply, placement, temperature, multi-RO activity, or data/sample
> interaction conditions.

## Bottom Line

Use the existing data now as code-density-normalized evidence for a null
data/data locking result. Do not present it as an independent TDC calibration.
The next bitstream should be a dedicated asynchronous code-density calibration
mode with unchanged TDC lanes and packet format, captured at 8 to 16 MiB per
lane/mode plus at least one repeat. The counts-to-ps mapping is straightforward,
but the credibility comes from separating the calibration stimulus from the RO
pairs being studied.
