# Physical Mechanism Scaffold for the Sampler-Aperture TVLSI Track

Date: 2026-05-30

This note defines a bottom-up mathematical scaffold for the TVLSI track. It is
intended to connect the existing reduced-XOR, repeat, route-audit, and
implementation-metric evidence to a testable physical interpretation. It is not
a calibrated physical jitter model, not a metastability transfer proof, and not a
complete timing-path derivation.

The useful claim is narrower:

> The observed restart bias can be modeled as a contributor-level probability
> produced by the interaction of RO startup phase state, route/sampler aperture,
> and XOR aggregation. Current data can estimate contributor probabilities,
> repeat stability, XOR residuals, and route/aperture proxy features; it cannot
> yet uniquely identify physical jitter variance, metastability constants, or
> coupling coefficients.

## Evidence Boundary

The scaffold is grounded in the current TVLSI evidence files:

- `data/experiments/tvlsi_sampler_aperture_model_20260530/contributor_dataset.csv`
- `data/experiments/tvlsi_sampler_aperture_model_20260530/xor_cancellation_model.csv`
- `data/experiments/tvlsi_sampler_aperture_model_20260530/repeat_stability_summary.csv`
- `data/experiments/tvlsi_sampler_aperture_model_20260530/prediction_vs_observed.csv`
- `data/experiments/tvlsi_sampler_aperture_model_20260530/route_result_correlation.csv`
- `data/experiments/heldout_sampler_route_diff_20260530/heldout_per_bitstream_route_audit_20260530.csv`
- `data/experiments/tvlsi_sampler_aperture_model_20260530/implementation_metrics_20260530.csv`

The existing evidence already supports contributor-level decomposition, XOR
cancellation residuals, same-condition repeat stability for selected settings,
Board1/Board2 sampler counterfactual behavior, and route/PIP/net-delay proxy
features. It does not yet support a calibrated physical proof.

## Three-Layer Model

### Layer 1: RO Startup and Phase State

For contributor RO `i` on board/device `b`, implementation context `r`, and
warmup setting `w`, let the unobserved oscillator phase be:

```text
phi_i(t; b,r,w) =
    phi_i(0; b,r,w)
  + omega_i(b,r) * t
  + eta_i(t; b,r,w)
  + kappa_i(t; b,r,w)
```

where:

- `phi_i(t)` is the instantaneous phase state of contributor `i`.
- `phi_i(0)` is the restart/startup phase offset after reset and warmup setup.
- `omega_i` is the mean angular frequency of contributor `i`.
- `eta_i(t)` is random phase noise or jitter accumulated up to time `t`.
- `kappa_i(t)` is deterministic or stochastic perturbation from coupling,
  supply activity, neighboring logic, and implementation context.
- `b` captures board/device instance differences.
- `r` captures routed implementation and sampler context.
- `w` captures warmup count or restart timing condition.

The current data does not observe `phi_i(t)` directly. It observes binary
samples produced after restart and warmup. Therefore, this layer should be read
as the hidden-state source of measured contributor probabilities, not as a
directly fitted phase-noise model.

The warmup parameter enters through both `phi_i(0; b,r,w)` and the elapsed time
before sampling. Warmup experiments therefore test whether startup phase state is
stable, shifted, or reordered by small changes in `w`.

### Layer 2: Route and Sampler-Aperture Transfer

Let the sampler observe contributor `i` at an effective sampling time:

```text
t_i^sample = t_0(w) + delta_route_i(r) + delta_sampler(r) + epsilon_sample(t)
```

where:

- `delta_route_i(r)` is the routed data/sampler path delay affecting
  contributor `i`.
- `delta_sampler(r)` is the sampler-side aperture shift caused by sample-RO
  placement, sampled register placement, clocking, local routing, and local
  neighborhood.
- `epsilon_sample(t)` is short-term sampler timing noise.

Define the aperture transfer function:

```text
A_i(theta; r) = Pr[observed bit is 1 | phase theta, sampler context r]
```

where `theta = phi_i(t_i^sample)`. In a hard-threshold idealization, `A_i` is a
binary phase-region indicator. In a more realistic metastability-sensitive
interpretation, `A_i` is a smooth transition function around sampling boundaries.
The current evidence does not fit the shape of `A_i`; it only estimates its
aggregate effect through observed probabilities and route/aperture proxies.

The measured contributor one-probability is:

```text
p_i(b,r,w) = E[ A_i(phi_i(t_i^sample; b,r,w); r) ]
```

This expression is the core bridge from route context to observed bias. It says
that a contributor can change measured bias even if its data-RO cells stay fixed,
because the sampler aperture, local route delays, or local sampler neighborhood
can shift the phase region being observed.

This interpretation is consistent with the current route audit:

- Held-out per-bitstream audit covers 17/17 routed reduced-XOR DCPs.
- In all held-out all640-to-subset comparisons, common data-RO cells have 0 LOC
  and 0 BEL changes.
- Sample-RO and sampled-data route features vary across contexts and
  bitstreams.
- Original-vs-heldout all640 audit keeps data-RO cells fixed while moving 9/9
  sample-RO cells and changing 27/36 sample-RO nets.

These facts support route/sampler context as a meaningful implementation
variable. They do not prove that only the sampler changed, because other
control/FIFO/UART routes can also move.

### Layer 3: Observed Contributor Probability and XOR Residual

For a contributor bitstream:

```text
X_i(b,r,w,n) in {0,1}
p_i(b,r,w) = Pr[X_i = 1]
s_i(b,r,w) = p_i(b,r,w) - 0.5
```

where `n` indexes samples within a capture.

For a contributor set `S`, define the aggregate XOR output:

```text
Y_S(n) = xor_{i in S} X_i(n)
```

Under an independence approximation:

```text
Pr[Y_S = 1] =
    (1 - product_{i in S}(1 - 2p_i)) / 2
```

Define the XOR residual:

```text
rho_S(b,r,w) =
    p_observed(Y_S = 1; b,r,w)
  - p_independent(Y_S = 1; {p_i(b,r,w) : i in S})
```

Interpretation:

- `p_i` and `s_i` quantify contributor-level bias.
- The independence approximation quantifies cancellation expected from measured
  individual contributors.
- `rho_S` captures what the simple model does not explain: correlation,
  deterministic startup-position structure, unobserved common-mode effects, or
  sampler-aperture effects not captured by individual `p_i` alone.

This layer is already useful with current data. For example, the current TVLSI
offline report records that Board2 held-out w10 data-RO contributors predict
aggregate `p1 = 0.499996685` under the independence approximation, while the
measured all640 aggregate is `p1 = 0.500718000`. The small but nonzero residual
is evidence to report, not a nuisance to hide.

## Parameter Identifiability Table

| Quantity | Meaning | Current status | Current evidence or required future data |
|---|---|---|---|
| `p_i(b,r,w)` | Contributor one-probability | directly estimable | Reduced-XOR captures and full-map summaries |
| `s_i = p_i - 0.5` | Signed contributor bias | directly estimable | Contributor tables and repeat summaries |
| `Y_S` aggregate `p1` | XOR output one-probability | directly estimable | all640 and subset aggregate captures |
| `rho_S` | Independent-XOR residual | directly estimable when contributors and aggregate are matched | `xor_cancellation_model.csv`, held-out full map |
| Repeat sign stability | Stability of contributor bias direction | directly estimable for repeated settings | Board1 reduced-XOR repeat, Board2 counterfactual repeats |
| Contributor rank stability | Stability of strongest low/high contributors | directly estimable when full maps repeat | Full-map/repeat summaries; stronger after second held-out repeats |
| Route/PIP/net-delay summaries | Implementation proxy for sampler/context perturbation | directly extractable, proxy for mechanism | Held-out route audit and route/result correlation |
| `delta_route_i(r)` | Contributor-specific route delay shift | proxy estimable | Net-delay reports; not a calibrated sampling-time perturbation |
| `delta_sampler(r)` | Sampler aperture/context shift | proxy estimable | Sample-RO LOC/BEL/PIP/net-delay/neighborhood changes |
| Warmup sensitivity | Change in startup phase sampling with `w` | proxy estimable | Warmup neighbor and counterfactual summaries |
| Board/device offset | Board-dependent phase/noise/context shift | proxy estimable | Board1 vs Board2 summaries |
| `omega_i` | Mean oscillator frequency | not identified by current reduced-XOR data | Needs frequency/TDC or calibrated counter measurement |
| `eta_i(t)` variance | Physical jitter/phase-noise variance | not identified | Needs jitter/TDC/phase-noise measurement or calibrated timing sweep |
| `kappa_i(t)` coefficient | Coupling strength from neighboring RO/logic activity | not identified | Needs controlled neighbor/coupling activation sweep |
| Shape of `A_i(theta; r)` | Aperture/metastability transfer curve | not identified | Needs phase sweep, IDELAY/MMCM shift, or equivalent controlled aperture sweep |
| Metastability time constant | Flip-flop transfer parameter near aperture boundary | not identified | Needs metastability S-curve or logistic transfer fitting |
| Voltage/temperature drift coefficient | PVT dependence of phase/aperture | not identified yet | Needs capture-linked XADC/PVT sweep or logged environmental variation |

## Mechanistic Hypotheses

The scaffold leads to testable hypotheses:

1. **Contributor decomposition hypothesis.** Aggregate XOR can appear balanced
   while individual contributors remain strongly biased because XOR cancellation
   operates on signed contributor factors.

2. **Sampler-aperture hypothesis.** Moving or perturbing the sampler/context can
   change `p_i(b,r,w)` even when data-RO cell LOC/BEL remains fixed, because
   `delta_sampler(r)` and route-dependent aperture features shift which phase
   region is sampled.

3. **Warmup/startup-state hypothesis.** Small changes in warmup can change
   `phi_i(0; b,r,w)` or sampling phase alignment, producing stable but different
   contributor signs/ranks.

4. **Residual hypothesis.** Nonzero `rho_S` indicates correlation,
   deterministic startup structure, common-mode perturbation, or aperture effects
   beyond an independent-contributor XOR model.

5. **Board/context boundary hypothesis.** Board1-derived contributor priors
   should only partially transfer to Board2 or to a new sampler context until
   route/aperture and PVT/coupling proxies are included.

These hypotheses are falsifiable. A second held-out sampler/context can disprove
or bound them if contributor signs, ranks, aggregate class, or residual direction
do not transfer under a frozen prediction rule.

## Validation Route

The TVLSI validation route should proceed in layers:

1. **Explain existing evidence.** Use the current five-experiment closure to
   show contributor decomposition, XOR cancellation/residual, repeat stability,
   sampler/route linkage, and implementation sanity.

2. **Freeze a prediction rule.** Before observing the second held-out context,
   define the prediction target and metrics: contributor sign, strongest low/high
   rank, aggregate near-balanced vs biased class, XOR residual direction,
   sign accuracy, rank correlation, class accuracy, mean absolute error, and
   residual direction accuracy.

3. **Run second held-out validation.** Compare frozen predictions against the
   new full map and repeat anchors. Prediction success strengthens the
   sampler-aperture mechanism; failure identifies model boundaries.

4. **Add route/PVT controls.** Join second held-out route audit and capture-linked
   PVT logs so observed differences are not attributed only to contributor
   randomness.

5. **Escalate only after predictive closure.** A calibrated physical model
   requires targeted experiments such as phase sweep, MMCM/IDELAY sampler shift,
   TDC/frequency logging, PVT sweep, and controlled neighbor/coupling activation.

## What Not to Claim Yet

Do not claim:

- physical jitter variance has been measured or fitted;
- metastability transfer has been calibrated;
- route delay has been formally derived into aperture probability;
- coupling coefficients have been identified;
- data-RO placement is the only possible explanation or has been perfectly
  isolated from all control/FIFO/UART routing effects;
- the current simple Board1 prior is a calibrated transfer model.

Safe wording:

- "is consistent with a sampler-aperture interpretation";
- "supports route/context as a measurable implementation variable";
- "exposes residuals beyond an independent-XOR approximation";
- "provides a falsifiable scaffold for held-out prediction";
- "does not yet identify calibrated physical jitter, metastability, or coupling
  parameters."

## Manuscript Use

This scaffold can support a compact TVLSI subsection titled "Mechanistic
Interpretation" or "Stochastic Sampler-Aperture Model." The subsection should:

- introduce the three-layer model;
- report which parameters are directly estimated versus only proxied;
- connect route audit and reduced-XOR results without overclaiming causality;
- frame second held-out prediction as the decisive validation step;
- place calibrated jitter/metastability/coupling models in future work unless
  later experiments make them identifiable.
