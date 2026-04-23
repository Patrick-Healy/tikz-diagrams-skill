# TikZ Style Guidelines

Apply these defaults unless the user gives a style reference or project-specific convention.

## Typography

- Use readable labels at the intended output size.
- Use short node labels, ideally one to four words.
- Use `align=center` for multi-line node labels.
- Use explicit `text width` for nodes that may wrap.
- Put paragraphs in captions, slide notes, or surrounding text, not inside diagram nodes.
- Do not render caption-style prose, interpretation paragraphs, or teaching notes inside standalone images by default. Keep those in the QA note, surrounding document, speaker notes, or the calling agent's response.

## Presentation Modes

- **Teaching mode** is for lecture slides, tutorials, and student-facing handouts. Explainer boxes are allowed, but the title band, legends, axes, and key plotted comparison must stay clear. Teaching notes should sit outside the main plot or flow.
- **Research mode** is for seminars, papers, and professional research presentations. Prefer direct labels, legends, axis labels, concise callouts, and captions outside the plot. Avoid large explainer boxes unless the user explicitly asks for a teaching-style version.
- **Compact mode** is for multi-panel figures and constrained layouts. Use direct labels only, omit teaching notes, and avoid framed explanation boxes.

When producing variants, keep the same geometry and semantics where possible so users can switch between teaching and research versions without reinterpreting the figure.

## Layout

- Give every diagram a clear reading order.
- Use one primary figure grammar unless a multi-panel design clearly reduces cognitive load.
- Keep notes outside the main flow.
- Use stable node dimensions when generating variants.
- Leave visible whitespace between nodes, arrows, labels, and callouts.
- Reserve a protected title band. No callout, event marker, legend, arrow, or plot label may touch or enter it.
- Keep effect labels, estimate labels, coefficient labels, and other direct labels out of plotted strokes. If a label is inside the plotting region, verify that its rendered text box does not cover curves, brackets, axes, shaded-region boundaries, or the key comparison.
- Do not let labels determine the entire geometry unless the diagram is tiny.
- Prefer separate small multiples over a single overloaded diagram.
- Split figures that combine incompatible grammars, such as a DAG plus coefficient plot, unless the user explicitly wants a composite and the layout remains readable.

## Arrows

- Arrows should encode semantics: causality, sequence, transformation, diagnostic relation, feedback, or dependency.
- Avoid arrows crossing labels or nodes.
- Do not let arrows, braces, brackets, or event lines pass through callout text.
- Use dashed arrows for optional, diagnostic, uncertain, or counterfactual links.
- Use separate positioned nodes for labels when inline edge labels become crowded.
- Avoid redundant arrow labels. Do not label a branch with the same text as its terminal node, or add `feedback loop` text when the arrows already form the loop.

## Color

- Use color semantically:
  - blue or dark neutral for default structure
  - teal or green for positive, stable, source, or accepted states
  - red for risk, failure, warning, or burden
  - gold for emphasis, pressure, field, or transition
- Keep palettes restrained. Avoid rainbow diagrams.
- Ensure diagrams remain understandable if printed in grayscale.

## Slide Fit

- For Beamer slides, prefer landscape diagrams and short labels.
- Keep the title outside the dense graph area.
- Do not place key text below the visible baseline.
- Avoid tiny matrix labels.
- Use a 16:9 wrapper when slide-fit risk matters.

## Batch Review

- Always make a contact sheet for multi-diagram batches.
- Inspect contact sheets for repeated layout problems.
- Patch shared templates or generators when the same issue appears repeatedly.
- During critique rounds, use versioned PNG and contact-sheet filenames so the inspected image cannot be confused with a stale cached render.
- When showing updates to a user, prefer the versioned local file just rendered. Overwritten PNG/GIF filenames and GitHub README images may be cached by browsers or chat clients.
- Record a complexity outcome for each figure: `keep`, `simplify`, `split`, or `reject`.
