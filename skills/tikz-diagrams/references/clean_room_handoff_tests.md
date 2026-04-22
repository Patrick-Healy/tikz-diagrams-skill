# Clean-Room Handoff Tests

Use these tests to verify the TikZ skill in a fresh agent session without relying on prior conversation context.

## Test 1: Single-Diagram Visual QA

Task prompt:

```text
Use $tikz-diagrams to create one standalone TikZ diagram for a business/economics teaching slide explaining parallel trends in difference-in-differences.

Requirements:
- choose `teaching` mode unless there is a reason not to
- use the provided local example corpus as the quality baseline, if one is available
- compile to PDF and render to PNG
- run static safety checks
- run rendered visual QA with `--visual-check --visual-mode teaching`
- visually inspect the PNG after the automatic checks
- save outputs under `outputs/tikz_skill_cleanroom_single_test`
- create a short QA note
- final response links only the `.tex`, `.pdf`, `.png`, visual QA JSON, and QA note
```

Expected behavior:

- The diagram should use an axis/curve or timeline-style econometrics template.
- Explainer boxes are allowed, but must not enter the protected title band or cover the key effect comparison.
- The visual QA report should be `pass`, or any `warn` status should be documented and manually inspected.

## Test 2: Batch With QA-Badged Contact Sheet

Task prompt:

```text
Use $tikz-diagrams to create a batch of three standalone TikZ diagrams for teaching econometrics:
1. RDD threshold
2. IV/LATE compliance types
3. Event-study coefficients

Use the provided local example corpus as the quality baseline, if one is available. Compile and render all three, run static checks, run rendered visual QA, make a QA-badged contact sheet with `--show-qa`, visually inspect it, fix severe issues, and save outputs under `outputs/tikz_skill_cleanroom_batch_test`.

Final response should link the three final `.tex` files, three `.png` files, three visual QA JSON files, the contact sheet, and a short QA note.
```

Expected behavior:

- The contact sheet should show QA status badges.
- Any title-band collision or text-overlap failure must be fixed before finalizing.
- The QA note should include a complexity review for each figure: `keep`, `simplify`, `split`, or `reject`.
- Caption-style prose should be kept outside the rendered images.

## Test 3: Iterative Series Extension

Run the included clean-room fixture:

```bash
python3 "$SKILL_DIR/scripts/render_tikz_series.py" \
  "$SKILL_DIR/tests/fixtures/series_parallel_trends_manifest.json"
```

Portable form:

```bash
python3 "$SKILL_DIR/scripts/render_tikz_series.py" \
  "$SKILL_DIR/tests/fixtures/series_parallel_trends_manifest.json"
```

Expected behavior:

- Three cumulative variants are produced:
  1. `teaching_explainer`
  2. `research_direct_labels`
  3. `compact_no_note`
- Each step passes static safety checks.
- Each step compiles, renders, and runs visual QA in its requested mode.
- The output folder contains a QA-badged `series_contact_sheet.png` and `series_qa_note.md`.

Use this pattern when a researcher wants to iterate over one diagram with fine-grained control. The source keeps stable geometry; the manifest changes only named placeholders or previously rendered annotation blocks.

## Test 4: Researcher Composite Prompt Critique

Task prompt:

```text
Use $tikz-diagrams to create a researcher-style figure for a marketing analytics paper that asks for both a mediation DAG and effect estimates. Use the provided local example corpus as the quality baseline, if one is available. Apply the figure grammar budget and no-rendered-captions rule. Save versioned renders and a QA note with `complexity_review`.
```

Expected behavior:

- The skill should prefer two paired figures, not one crowded hybrid, unless the user explicitly insists on a composite.
- The DAG figure should use causal-graph grammar only.
- The estimates figure should use coefficient-plot grammar only.
- Caption or interpretation text should be recorded in the QA note rather than rendered in the images.
- The QA note should mark the original composite idea as `split`.

## Test 5: Critique Iteration Output Hygiene

Task prompt:

```text
Use $tikz-diagrams to critique and revise a finance feedback-loop figure. Render the initial attempt, inspect it, simplify redundant labels if needed, and save versioned PNGs/contact sheets for each inspected round.
```

Expected behavior:

- Do not overwrite the inspected PNG during critique rounds.
- Use filenames such as `liquidity_spiral_v01.png`, `liquidity_spiral_v02.png`, and `contact_sheet_v02.png`.
- If a decorative central `feedback loop` label duplicates the arrows, remove it and mark the complexity review as `simplify`.

## Series Manifest Pattern

Minimal manifest shape:

```json
{
  "series_name": "my_diagram_series",
  "source": "/absolute/path/to/template.tex",
  "output_dir": "/absolute/path/to/output",
  "visual_mode": "teaching",
  "cumulative": true,
  "strict_replacements": true,
  "steps": [
    {
      "name": "teaching_explainer",
      "mode": "teaching",
      "replacements": {
        "__ANNOTATION_BLOCK__": "\\node[explainer] at (1,1) {Key idea};"
      }
    },
    {
      "name": "research_direct_labels",
      "mode": "research",
      "replacements": {
        "\\node[explainer] at (1,1) {Key idea};": "\\node[researchlabel] at (1,1) {label};"
      }
    }
  ]
}
```

Use `cumulative: true` when each step should update the previous source. Use `cumulative: false` when each variant should start from the original template.
