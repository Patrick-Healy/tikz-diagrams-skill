# Copilot Instructions

When the task involves TikZ, PGF, LaTeX diagrams, rendered visual QA, contact sheets, or animations, use the workflow in `skills/tikz-diagrams/SKILL.md`.

Prefer the bundled scripts over ad hoc rendering:

- `skills/tikz-diagrams/scripts/check_tikz_safety.py`
- `skills/tikz-diagrams/scripts/compile_render.py`
- `skills/tikz-diagrams/scripts/check_tikz_visual.py`
- `skills/tikz-diagrams/scripts/make_contact_sheet.py`
- `skills/tikz-diagrams/scripts/render_animation_preview.py`
- `skills/tikz-diagrams/scripts/render_tikz_series.py`

Do not commit generated PDFs, PNGs, GIFs, frame folders, logs, or user-specific absolute paths unless they are deliberate presentation assets.

