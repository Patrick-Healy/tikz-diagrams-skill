# TikZ Gotchas

## Edge Labels

Avoid unpositioned inline edge labels in dense diagrams:

```latex
\draw (a) -- node {label} (b);
```

Prefer:

```latex
\draw (a) -- node[above] {label} (b);
```

Or use a separately positioned `\node`.

## Long Node Text

Long labels cause wrapping and collision. Use short labels and move explanation outside the diagram.

Use:

```latex
\node[box, text width=1.6cm, align=center] {Short label};
```

## Bounding Box Clipping

Standalone diagrams can clip labels, arrowheads, braces, or annotations near the edge. Increase standalone border or add an explicit bounding box.

## Dense Matrices

Matrix labels often collide with first-column cells. Reserve left gutter space and set cell text widths.

## Dashed Frames

Dashed frames often cut through nodes or crowd labels. Prefer a small label or background band unless the frame has enough margin.

## Curves and Callouts

Callout boxes can cover curves. This is acceptable only if the label is more important than the covered segment. Avoid covering intersections or thresholds.

## Title-Band Collisions

Standalone TikZ output can compile even when callout boxes overlap the title. Reserve a protected title band and keep event labels, legends, arrows, and callouts below it.

## Connector Intrusion

Arrows, brackets, braces, and vertical event lines can pass through text while still compiling cleanly. Keep connector endpoints outside text boxes and route them around labels.

## Teaching vs Research Callouts

Teaching diagrams may use explainer boxes, but research figures should usually use direct labels and captions outside the plot. If a diagram feels crowded, first try switching to research or compact mode before shrinking text.

## Slide Fit

A diagram can compile while being unusable on a slide. Render it and inspect at normal slide size.

The static checker is not enough for slide readiness. Run rendered visual QA to catch text overlap, title-band collisions, and clipped labels.

## Batch Generation

Do not trust a generated batch without a contact sheet. Repeated layout problems usually mean the shared template needs patching.
