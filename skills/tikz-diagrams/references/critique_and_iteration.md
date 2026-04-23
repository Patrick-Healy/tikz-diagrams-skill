# Critique and Iteration

Use this reference when a task involves design critique, researcher-style revision, noisy figures, composite diagrams, or figure batteries. Visual QA can detect overlap and title-band failures, but it cannot decide whether a figure should exist in its current form.

## Critique Gate

After rendered visual QA and PNG inspection, record one outcome:

- `keep`: the figure is clear enough after ordinary checks.
- `simplify`: remove redundant labels, callouts, notes, decorative marks, or secondary encodings.
- `split`: the figure combines incompatible visual grammars or asks the reader to parse too much at once.
- `reject`: the figure is misleading, semantically wrong, or not useful even if technically valid.

Ask these questions:

- Is there one primary figure grammar?
- Can the main message be understood after a brief glance?
- Are labels explaining the plot, or compensating for an overloaded plot?
- Do direct labels, effect labels, or math labels sit on top of plotted lines, brackets, axes, or shaded boundaries?
- Does every annotation add information not already expressed by nodes, arrows, axes, or direct labels?
- Would two simpler figures communicate better than one composite figure?

For model-dependent plots, do not let `keep` mean "looks plausible." Run `references/math_logic_checks.md` as a separate gate whenever curves, intersections, brackets, thresholds, estimates, payoffs, or comparative statics carry mathematical meaning.

## Figure Grammar Budget

A single figure should usually use one primary grammar:

- DAG
- coefficient plot
- quadrant
- timeline
- game tree
- flow/process
- matrix/grid
- axis/curve
- feedback loop

Split or simplify by default when the prompt asks for multiple unrelated figure grammars, two reading orders, or two legends. See `Overcrowding Examples` below for common warning signs.

Multi-panel layouts are appropriate when panels share a common axis, timeline, sequence, or visual grammar. If panels use different grammars, keep them visually separated and avoid cross-panel arrows unless they are essential.

## Overcrowding Examples

The rule is general: split or simplify when one figure asks the reader to use multiple unrelated grammars or read two stories at once.

Examples:

- state transfer plus effect estimates
- funnel plus causal attribution
- mechanism diagram plus diagnostics
- distribution animation plus regression table
- DAG plus coefficient plot

Do not treat these examples as banned combinations. They are warning signs. A multi-panel figure can still work when panels share a common axis, sequence, or clear reading order.

## No Rendered Captions

Do not render caption-style prose inside standalone images by default. Keep the image limited to:

- title
- axis labels
- panel labels
- direct labels
- short legends
- short semantic marks such as `target`, `avoid`, `policy`, or `cutoff`

Put caption text, interpretation, teaching notes, caveats, and methodological explanation in:

- QA notes
- Beamer speaker notes
- markdown handoff files
- the calling agent's response

## Redundancy Rules

- Do not label a branch with the same text as the terminal node.
- Do not add `feedback loop` text when the arrows already form a loop.
- Do not label every arrow in a DAG unless the label changes interpretation.
- Do not add a callout that restates the title.
- Prefer one meaningful label over many tiny labels.

## Iteration Output Hygiene

Viewer caches can show stale images when PNGs are overwritten in place. During critique or multi-round review:

1. Render versioned images such as `figure_v01.png`, `figure_v02.png`, and `figure_v03.png`.
2. Render versioned contact sheets such as `contact_sheet_v01.png` and `contact_sheet_v02.png`.
3. Link or inspect the versioned file that was actually reviewed.
4. Copy the accepted image to the canonical final filename only after the review is complete.

When a user says an image still looks stale or unchanged, assume cache confusion is possible until disproven. Show the freshly rendered local versioned artifact, compare file modification times or checksums if needed, and avoid using a GitHub README-rendered image as the only evidence of the current state.

## Fine-Grained Text-On-Geometry Gate

Ordinary rendered visual QA catches text-text overlap, title-band collisions, and edge clipping. It can miss a label sitting on a plotted line because the line is vector geometry, not text.

Use the targeted text-over-plot gate when a figure has effect labels, coefficient labels, estimate labels, math notation, or callouts inside a plotted region:

```bash
python3 "$SKILL_DIR/scripts/check_tikz_visual.py" path/to/diagram.pdf --mode research --text-plot-overlap
```

What worked best in testing:

- Use PDF text extraction for exact text boxes; OCR text recognition is too noisy for math labels such as `\hat\tau_{DiD}`.
- Map those text boxes to rendered PNG pixels.
- Inspect the pixels inside each targeted label box for plot-colored strokes that are not the label's own text color or a light backing box.
- Use a targeted regex for labels such as `tau`, `DiD`, `effect`, `estimate`, `coef`, `gap`, or `jump`; do not run the gate indiscriminately on every axis tick or direct label.

If the gate fails, move the label to whitespace, shorten it, add a visible backing box, or connect it to the bracket/curve with a small leader. Rerender and rerun the same gate.

## Repair, Simplify, Redesign

Use the right response for the critique:

- `repair`: fix a concrete defect such as overlap, clipping, compilation failure, or title-band collision.
- `simplify`: remove clutter, redundant labels, decorative marks, or in-image prose.
- `redesign`: change the structure, split the figure, or choose a different diagram family.

When the user says a figure is noisy, overloaded, or confusing, prefer `simplify` or `redesign` over a minor coordinate repair.

## Department Fit Checks

- Economics: does the figure express incentives, equilibrium, tradeoff, or strategic choice?
- Econometrics and Business Statistics: does it distinguish assumptions, identification, estimation, diagnostics, and sample selection?
- Finance: does it clarify risk, return, balance-sheet pressure, time, or feedback?
- Marketing and Analytics: does it clarify one primary job, such as state transfer, funnel movement, segmentation, causal attribution, or estimates? If several are requested, split or externalize the extras.
- Management and Operations: does it clarify sequence, capacity, queueing, timing, bottlenecks, or risk?

## QA Note Fields

For critique batteries, include:

```text
complexity_review: keep | simplify | split | reject
reason:
caption_text:
render_version:
contact_sheet_version:
```
