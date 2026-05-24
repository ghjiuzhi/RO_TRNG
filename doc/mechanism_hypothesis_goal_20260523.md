# Mechanism Hypothesis Goal 20260523

- workspace: `E:\Project\MLDSA\RO_TRNG`
- board: `z7020_b01`
- status: hypothesis-driven offline screening before the next hardware queue

## Self-Defined Goal

The next goal is not to collect more repeated data blindly. The goal is to identify the most defensible physical/statistical mechanism behind placement-dependent RO-TRNG degradation, then run only the hardware experiments that can separate competing explanations.

Working question:

> Why can some placements produce near-full continuous bit min-entropy while other placements on the same FPGA, same RTL family, same UART path, and similar environment produce strong bias or serial dependence?

## Current Best Reading

The simple explanation "nearby ROs lock together" is now too weak as the main paper claim. The latest TDC pair campaign tested 12 pair-specific captures and 192 windows; `strong_lock_windows=0`, with the maximum small-lag absolute phase correlation about `0.0318`. This is valuable negative evidence.

The better paper direction is:

> Placement changes the sampling relationship between the sampler RO and the data-RO ensemble. The observable consequences are continuous-stream bias, short-range bit dependence, and restart/startup fixed-position bias. Pairwise RO locking may exist locally or intermittently, but it is not the dominant mechanism in the tested random1/random3 data-data pairs.

## Hypotheses To Rank

### H1. Sampler-Coupling / Sampler-Pulling Hypothesis

Claim:

The sampler RO is not a neutral observer. Placement can change how much the always-on data RO set pulls the sampler frequency and phase, and this changes which regions of the data-RO phase ensemble are sampled.

Why it is promising:

- Existing RO frequency data show a much larger sample RO shift in `random1` than in `random3`.
- `random1` is badly biased in continuous TRNG, while TDC data-data pairs do not show strong locking.
- This explains why data-data TDC can look clean while output bits are poor: the missing measurement is data-sampler interaction.

Predictions:

- Bad placements should show larger sampler all-on shift, or smaller/structured data-sampler beat separation, than good placements.
- TDC between sampler and selected data ROs should show stronger drift/structure than data-data pairs.
- Moving only the sampler RO while holding data RO placement similar should change TRNG quality more than moving one data RO.

Current evidence:

- Supports: `random1` has poor TRNG entropy and larger sampler shift than `random3`.
- Missing: RO_FREQ/TDC coverage for sampler-data pairs and for compact/sparse/same_column/checker.

Next hardware if this survives offline screening:

- Build sampler-data TDC probes for `random1` and `random3`.
- Build RO_FREQ probes for `compact`, `sparse`, `same_column`, and `checker`.

### H2. Local Correlation / Adjacency Structure Hypothesis

Claim:

Some placements do not mainly create monobit bias; instead they create short-range dependence, visible in adjacent-bit equality and lag autocorrelation.

Why it is promising:

- `same_column` has near-full bit min-entropy but elevated adjacent-equal ratio, making it a useful "bias good, dependence bad" counterexample.
- `random1`, `sparse`, and `row` show both bias and dependence.
- This gives the paper a richer statistical story than a single p1/min-entropy table.

Predictions:

- Bad placements should separate into at least two classes:
  - bias-dominated: large `|p1-0.5|`
  - dependence-dominated: high lag-1 or adjacent-equal index with small monobit bias
- Continuous-stream bit-position metrics should explain some restart fixed-column behavior.

Current evidence:

- Supports: placement summary already shows `same_column` as a special high-Hmin/high-adjacent-equal case.
- Missing: per-bit-position and lag-spectrum analysis over the 20MiB repeat files.

Next action:

- Offline analysis first. No hardware is needed yet.

### H3. Startup/Restart Transient Fixed-Column Hypothesis

Claim:

The initial samples after enable/reset contain deterministic phase memory. Warmup removes this transient, but the required warmup depends on placement.

Why it is promising:

- `random3` continuous stream is good, but restart around warmup10 fails and warmup11/12 pass.
- `compact`, `checker`, `same_column`, and `sparse` warmup0 fail while warmup12 passes.
- This is exactly the kind of mechanism reviewers care about: long-run non-IID quality does not guarantee restart robustness.

Predictions:

- Worst restart columns should move or weaken as warmup increases.
- Warmup boundary should be reproducible on repeat runs but not necessarily at the same exact column.
- Placements with stronger initial fixed-column bias should have worse early-row column statistics even if continuous TRNG is good.

Current evidence:

- Strong support from restart summary.
- Missing: a compact table linking warmup, worst column, continuous bit-position bias, and XADC.

Next action:

- Offline join of restart summary with continuous position-structure features.
- Optional hardware later: finer warmup sweep around the transition for `random3` and one placement contrast.

### H4. Global Frequency Ensemble / Beat Diversity Hypothesis

Claim:

Placement quality depends on the diversity of beat frequencies among the data ROs and between data ROs and the sampler, not only the closest pair.

Why it is promising:

- `random1` and `random3` have similar-looking closest data-data gaps, yet very different TRNG quality.
- Pair TDC no-lock suggests the ensemble/sampler relation matters more than a single pair.

Predictions:

- Good placements should have better distribution of data-sampler beat periods or less coherent grouping.
- Bad placements may have clusters of data ROs whose sampled XOR/parity has a stable bias.

Current evidence:

- Partial support from RO_FREQ random1/random3 only.
- Missing broad RO_FREQ matrix across placements.

Next hardware:

- RO_FREQ probes for all important placements before more TDC.

### H5. TDC Calibration / Measurement Caveat Hypothesis

Claim:

TDC is still useful, but raw TDC bin values should not be treated as linear time until code-density calibrated.

Why it matters:

- This protects the paper from overclaiming.
- Current TDC evidence is strongest as relative phase/correlation evidence, not calibrated ps-level metrology.

Next action:

- Keep TDC features as categorical/windowed phase indicators.
- Add dedicated code-density calibration only after the main mechanism path is clearer.

## Decision Rule

Do not start a long hardware queue until the offline analysis answers these:

1. Does continuous TRNG position/lag structure separate `random1`, `sparse`, `same_column`, `compact`, and `random3` into meaningful classes?
2. Does restart worst-column behavior align with any continuous bit-position or lag feature?
3. Are the remaining missing mechanism fields mostly sampler/data RO frequency and TDC measurements?

If yes, the next hardware priority is not more data-data TDC. It is:

1. sampler-data TDC for `random1` and `random3`;
2. RO_FREQ for `compact`, `sparse`, `same_column`, and `checker`;
3. then targeted restart warmup boundary repeats only if needed.

## Tentative Paper Claim

The likely high-level claim is:

> FPGA RO-TRNG entropy is placement-sensitive not merely because nearby oscillators lock, but because placement changes the sampler-data phase ensemble. This produces distinct failure modes: continuous monobit bias, short-range dependence, and restart fixed-column bias. TDC pair experiments provide negative evidence against persistent two-RO locking in the tested pairs, while restart and continuous-position analyses expose the sampler/startup mechanisms that matter for entropy-source validation.

## 2026-05-23 Update: Sampler-Island Ablation

The first causal ablation supports H1. Keeping the `random1` data RO placement fixed but moving only the sample RO to `SLICE_X45Y39` changed the programmed 20MiB TRNG result from the baseline `p1=0.337669`, bit min-entropy `0.594377`, adjacent-equal `0.556683` to `p1=0.484799`, bit min-entropy `0.956792`, adjacent-equal `0.501911`. Moving the 64 sampling registers in addition to the sample RO produced a near-ideal programmed 20MiB result (`p1=0.500051`, bit min-entropy `0.999854`, adjacent-equal `0.499982`).

The matching RO_FREQ control also moved in the expected direction: same-session baseline `sample_x36y35` had sample all-on shift `+3855.97 ppm`, while local `sample_x45y39` had `-466.04 ppm`. This makes sampler placement and sample-RO pulling the strongest current mechanism candidate.

Important data-quality note: two early 5MiB sampler-local rows were captured without programming the corresponding bitstream in the same command. They are now marked invalid/ambiguous and should not be used for causal claims.

The sample-only effect is large but incomplete, while the sampler-island result suggests that sampling register/routing placement can remove the remaining bias. The claim should be causal but bounded: sampler-side placement is a major control knob for `random1` bias, and the sampler path should be treated as part of the entropy source rather than as a passive readout.
