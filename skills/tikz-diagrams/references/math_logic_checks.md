# Math and Diagram Logic Checks

Use this reference when a figure contains equations, curves, equilibria, estimands, thresholds, payoffs, geometry-dependent arrows, or model-implied comparative statics. Visual QA can catch overlap and clipping; it cannot prove that a curve, bracket, crossing, payoff, or animation step says the right thing.

## Planning Gate

Before drawing, write down the figure's model logic:

- Variables, axes, units, and sign conventions.
- Equations, inequalities, identities, payoff definitions, estimands, or source data that determine the geometry.
- Which elements are exact and which are schematic.
- Expected monotonicity, concavity, convexity, slopes, intercepts, asymptotes, orderings, and feasible regions.
- Equilibrium, crossing, tangency, threshold, or cutoff conditions.
- Comparative statics: what shifts, what moves along a curve, what must increase, decrease, stay fixed, or change order.
- Animation invariants: what changes frame by frame, what must remain fixed, and when labels or markers become true.

If the math cannot be specified, treat the output as a schematic teaching sketch. Do not add exact-looking guide lines, estimates, brackets, or numeric labels unless they are generated from stated values.

## Critical Visual Check

Inspect rendered images and animation frames for logic as well as layout:

- Do labels attach to the correct curve, region, point, or branch?
- Do intersections, brackets, guide lines, arrows, and shaded areas measure the stated object?
- Are shifts separated from movements along a curve?
- Are pre/post, treated/control, threshold/region, sender/receiver, and before/after labels in the right states?
- Does a final effect bracket correspond to the intended difference rather than convenient spacing?
- Are all frame labels true at the moment they appear?
- Would a knowledgeable reader infer a stronger numerical or causal claim than the figure supports?

## Common Economics and Research Checks

- **AD-AS / supply-demand**: Define which curves are fixed and which shift. Equilibria should lie at curve intersections. Output, price, or quantity guide lines should be generated from those intersections when exact claims are made.
- **Multiplier or comparative statics**: State the baseline, shock, rounds or shifts, and final effect. If the multiplier size is shown by a bracket, compute it from the plotted coordinates or call the figure schematic.
- **J-curve / delayed adjustment**: Keep the event date, baseline, trough, recovery, and final direction consistent. Avoid implying a measured recovery path when only the qualitative pattern is known.
- **Threshold / corridor trajectories**: Region labels must match inequalities. Failure, exit, or crossing markers should appear only after the path crosses the relevant boundary.
- **Distributions and parameter sweeps**: Density curves should remain normalized when treated as exact. Mean, variance, skew, or tail changes must match the parameter movement shown.
- **Game trees**: Chance probabilities should sum to one at each information set. Information sets must connect nodes that are indistinguishable to the player. Payoff tuples, player order, and branch labels must be consistent across frames.
- **DiD / event studies / RDD**: Axes, treatment timing, cutoff, pre-period patterns, coefficient timing, and estimand labels must correspond to the identification story.
- **Mediation / DAGs / causal graphs**: Directed edges should match the causal claim. Do not combine paths, estimates, and diagnostics into one figure unless the shared layout makes the logic clearer.

## QA Note Fields

For model-dependent figures, include:

```text
math_logic_review: exact | schematic | needs_source | failed
model_or_equations:
curve_or_geometry_constraints:
checked_invariants:
schematic_limits:
remaining_risks:
```

Use `exact` only when the plotted geometry is generated from stated equations, coordinates, data, or source values. Use `schematic` when the figure is a qualitative teaching diagram. Use `needs_source` when the user-provided source is not enough to verify the logic. Use `failed` when the rendered figure contradicts the expected math or model logic and must be patched before release.
