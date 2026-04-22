# Repository Instructions

This repository packages the `tikz-diagrams` agent skill. When a user asks for TikZ, PGF, LaTeX diagrams, rendered visual QA, contact sheets, or TikZ/animate.sty animations, read `skills/tikz-diagrams/SKILL.md` and follow that workflow.

## Checks

- Validate skill metadata by confirming `skills/tikz-diagrams/SKILL.md` has YAML frontmatter with `name` and `description`.
- Run static checks on generated TikZ sources with `python3 skills/tikz-diagrams/scripts/check_tikz_safety.py <file.tex>`.
- Compile/render diagrams with `python3 skills/tikz-diagrams/scripts/compile_render.py <file.tex> --visual-check --visual-mode teaching`.
- For animations, render a frame deck and preview with `python3 skills/tikz-diagrams/scripts/render_animation_preview.py <frames.pdf>`.

## Safety

- Do not commit user output folders, build products, secrets, logs, or local absolute paths.
- Ask before installing missing dependencies. Name the package manager/source and why the dependency is needed.
- Keep the skill itself agent-facing and concise. Put human-facing installation notes in `README.md`.

