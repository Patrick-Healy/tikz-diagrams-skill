# Diagram Patterns

Choose templates by communication job, not decoration.

Use a figure grammar budget: one diagram should usually have one primary visual grammar. If a prompt asks for two grammars, such as DAG plus coefficient estimates or mechanism plus diagnostics, prefer paired figures or clearly separated panels. Split when the combined figure needs two legends, two reading orders, or dense explanatory labels.

## Flow / Process

Use for sequential processes, research pipelines, teaching modules, data workflows, operations processes, and reproducibility chains.

Metadata tags: `flow`, `process`, `workflow`, `pipeline`, `sequence`, `teaching`.

## DAG / Causal Graph

Use for causal assumptions, treatment/outcome relationships, confounding, mediation, selection, and collider bias.

Metadata tags: `dag`, `causal`, `identification`, `assumptions`, `econometrics`.

Avoid combining a DAG with coefficient estimates in the same panel. Use a paired coefficient plot unless the shared layout is simple and the DAG remains visually dominant.

## Axis / Curve

Use for supply-demand, forecast paths, frontiers, thresholds, response functions, distributions, and comparative statics.

Metadata tags: `curve`, `axis`, `economics`, `finance`, `forecast`, `threshold`.

### Delayed Adjustment Path / J-Curve

Use when an intervention, shock, or treatment has a near-term response that differs from the eventual response: deterioration before recovery, muted response before catch-up, overshoot before settling, or adoption friction before acceleration.

Metadata tags: `delayed-adjustment`, `j-curve`, `time-path`, `shock`, `recovery`, `response`.

Recommended structure:

- horizontal time axis with a clearly marked intervention, shock, launch, policy change, or treatment date
- vertical outcome axis named for the relevant measure, not a generic "value"
- baseline or pre-shock reference line when the reversal is the message
- path with three readable phases: initial state, short-run adjustment/friction, longer-run recovery or new steady state
- at most two direct phase labels inside the plot; move interpretation prose outside the rendered image

Use this pattern for static figures or smooth reveal animations. Animate the path only when timing, lag, reversal, or accumulated adjustment is the teaching point. Do not combine the path with a full mechanism diagram, causal graph, regression table, or diagnostic panel unless the layout is deliberately split.

## Matrix / Grid

Use for payoff tables, robustness checks, risk matrices, specification grids, retention heatmaps, confusion matrices, and checklists.

Metadata tags: `matrix`, `grid`, `table`, `robustness`, `risk`, `diagnostic`.

For robustness grids, keep cell labels short and put interpretation in the caption or QA note. If row or column labels become paragraph-like, split the grid or use a table outside TikZ.

## Quadrant Map

Use for stakeholder maps, strategy matrices, segmentation, prioritization, and risk classification.

Metadata tags: `quadrant`, `strategy`, `segmentation`, `prioritization`.

## Tree / Branch

Use for decision trees, game trees, concept checks, churn rules, and uncertainty paths.

Metadata tags: `tree`, `branch`, `decision`, `game`, `classification`.

Avoid branch labels that repeat terminal node text. If a terminal node already says `Fight` or `Accommodate`, omit the same branch label unless it disambiguates a payoff path.

## Stack / Comparison

Use for components, decompositions, before/after comparisons, balance sheets, and side-by-side logic.

Metadata tags: `stack`, `comparison`, `decomposition`, `balance-sheet`.

## Feedback / Convergence Loop

Use for iterative estimation, model monitoring, learning loops, policy cycles, and diagnostics.

Metadata tags: `loop`, `feedback`, `convergence`, `monitoring`, `diagnostics`.

Let the arrows express feedback. Avoid central decorative loop labels unless they encode an additional state or mechanism not already shown by the cycle.

## Field / Pressure

Use when an invisible force or pressure should become visible: tax incidence, incentives, liquidity pressure, constraints, congestion, or bargaining power.

Metadata tags: `field`, `pressure`, `wedge`, `incentives`, `elasticity`.

## Threshold / Phase Transition

Use for nonlinear regime changes, tipping points, crisis cliffs, adoption thresholds, and margin-call dynamics.

Metadata tags: `threshold`, `phase-transition`, `regime`, `crisis`, `nonlinear`.

## Ensemble / Aggregation

Use for model voting, committees, ensemble forecasts, decision support, and aggregation over uncertain signals.

Metadata tags: `ensemble`, `aggregation`, `vote`, `model`, `decision-support`.
