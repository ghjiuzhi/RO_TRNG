# random1/random3 RO frequency and beat-frequency experiment

Date: 2026-05-13

Scope: prepare build and analysis material for mechanism validation only. This
document does not report hardware results, does not claim any measured RO
frequency, and does not require COM/JTAG/Vivado hardware access.

## Goal

The existing random1/random3 TRNG results show a placement-controlled contrast:

- random1: stable strong bias around `p1 ~= 0.337`.
- random3: stable near-ideal output around `p1 ~= 0.500`.

This experiment tests whether that contrast is associated with:

1. per-RO frequency distribution differences;
2. low beat-frequency pairs among data ROs;
3. low beat-frequency relations between each data RO and the sample RO;
4. frequency shift between `all-on` and `single-on` modes, used as a pulling or
   coupling proxy.

The experiment is not intended to prove locking by itself. It produces evidence
for the chain:

`placement -> RO frequency / beat / pulling metrics -> observed entropy quality`

## Probe design

New debug RTL:

- `rtl/debug/ro_freq_entropy_probe.v`
- `rtl/debug/RO_FREQ_trng_probe_top.v`

The probe keeps the TRNG-like oscillator structure:

- 8 data ROs, each `RO_STAGES=2`;
- 1 sample RO, `SAMPLE_STAGES=9`;
- instance name `u_entropy_source` and generate labels compatible with the
  existing matrix placement XDC hierarchy.

The top uses a single selected RO clock into the existing `counter` module. It
automatically cycles through two modes:

| mode id | name | active oscillators |
| ---: | --- | --- |
| 0 | `all_on` | data RO0..RO7 plus sample RO |
| 1 | `single_on` | only the measured data RO, or only sample RO for target 8 |

Targets are:

- `0..7`: data RO index;
- `8`: sample RO.

Each measurement emits a 14-byte UART frame:

| byte | field |
| ---: | --- |
| 0 | `0x52` (`R`) |
| 1 | `0x46` (`F`) |
| 2 | frame version, currently `1` |
| 3 | family id, use `1` for random1 and `3` for random3 |
| 4 | mode id |
| 5 | target index |
| 6 | active data RO mask |
| 7 | sample active flag |
| 8..9 | `WINDOW_CYCLES`, little endian |
| 10 | 8-bit count |
| 11..12 | sequence number, little endian |
| 13 | XOR checksum over bytes 0..12 |

Default `WINDOW_CYCLES=100` at 200 MHz gives a nominal 500 ns counter window.
This follows the existing `jitter_measure` scale and avoids immediate 8-bit
counter overflow for expected RO rates. If counts cluster near 0 or 255, rebuild
with a smaller or larger window.

## XDC material

Base non-hardware constraints:

- `data/experiments/xdc_ro_freq/ro_freq_sysclk_base.xdc`

Generated placement XDCs:

- `data/experiments/xdc_ro_freq/ro_freq_random1_seed1_x36y35_sample_x36y35.xdc`
- `data/experiments/xdc_ro_freq/ro_freq_random3_seed3_x36y35_sample_x36y35.xdc`

Generator:

```powershell
D:\Programs\Anaconda3\python.exe scripts\generate_ro_freq_probe_xdc.py `
  --matrix-xdc data\experiments\xdc_matrix\ro_random_seed1_x36y35.xdc `
  --sample-x 36 --sample-y 35 `
  --out data\experiments\xdc_ro_freq\ro_freq_random1_seed1_x36y35_sample_x36y35.xdc

D:\Programs\Anaconda3\python.exe scripts\generate_ro_freq_probe_xdc.py `
  --matrix-xdc data\experiments\xdc_matrix\ro_random_seed3_x36y35.xdc `
  --sample-x 36 --sample-y 35 `
  --out data\experiments\xdc_ro_freq\ro_freq_random3_seed3_x36y35_sample_x36y35.xdc
```

The data RO LOC/BEL constraints are copied from the random1/random3 matrix XDC.
The sample RO is currently placed at `SLICE_X36Y35` and spills across adjacent
slices for its 9 LUT stages. This is a deliberate fixed reference location, not
a measured optimum.

TODO before final paper use: decide whether the sample RO should instead be
co-located with the actual routed sample RO from `RO_TRNG_top`, if that route is
available and stable across builds.

## Build commands

These are build-only Vivado batch commands. They do not program the board and do
not open hardware manager.

```powershell
vivado -mode batch -source scripts\vivado\run_fpga1_ro_freq_probe_inmem.tcl `
  -tclargs data\experiments\xdc_ro_freq\ro_freq_random1_seed1_x36y35_sample_x36y35.xdc `
  data\vivado_runs\fpga1_ro_freq_probe\random1_seed1_x36y35 1 100

vivado -mode batch -source scripts\vivado\run_fpga1_ro_freq_probe_inmem.tcl `
  -tclargs data\experiments\xdc_ro_freq\ro_freq_random3_seed3_x36y35_sample_x36y35.xdc `
  data\vivado_runs\fpga1_ro_freq_probe\random3_seed3_x36y35 3 100
```

Expected bitstreams:

- `data/vivado_runs/fpga1_ro_freq_probe/random1_seed1_x36y35/RO_FREQ_trng_probe_top.bit`
- `data/vivado_runs/fpga1_ro_freq_probe/random3_seed3_x36y35/RO_FREQ_trng_probe_top.bit`

## Analysis

After the hardware session captures raw UART bytes from the two bitstreams, run:

```powershell
D:\Programs\Anaconda3\python.exe scripts\analyze_ro_frequency_matrix.py `
  data\hardware\<run_dir>\random1_ro_freq.bin `
  data\hardware\<run_dir>\random3_ro_freq.bin `
  --out-dir data\experiments\ro_freq_analysis\<run_id> `
  --prefix random1_random3_ro_freq
```

The script writes:

- `*_measurements.csv`: one row per valid UART frame;
- `*_summary.csv`: per family/mode/target mean frequency and count spread;
- `*_pairwise_all_on.csv`: data-data and data-sample `abs(delta_f)` plus beat
  period ranking;
- `*_pulling.csv`: `all_on - single_on` frequency shift in MHz and ppm.

Primary metrics for the mechanism table:

- minimum data-data `abs_delta_f_mhz` per family;
- minimum data-sample `abs_delta_f_mhz` per family;
- maximum absolute `shift_ppm_vs_single` per family;
- frequency standard deviation across data RO0..RO7 in `all_on`;
- whether random1's suspicious pairs align with the already observed TRNG bias.

## Interpretation guardrails

- A lower random1 beat separation supports the beat-dominated bias hypothesis,
  but does not by itself prove deterministic locking.
- Larger random1 all-on/single-on shift supports pulling/coupling, but must be
  compared against random3 under the same build and capture conditions.
- Similar random1/random3 frequency metrics would be useful too: it would push
  the next mechanism step toward phase relation, sample timing, routing delay, or
  multi-RO XOR interaction rather than simple frequency clustering.

