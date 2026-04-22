# TikZ Diagrams Agent Skill

Portable agent skill for creating, rendering, visually checking, iterating, and animating TikZ/PGF diagrams.

The canonical skill lives at:

```text
skills/tikz-diagrams/SKILL.md
```

Install the entire `skills/tikz-diagrams/` folder, not only `SKILL.md`. The folder contains the scripts, references, fixtures, and reusable templates that make the workflow deterministic.

## What It Does

- Creates standalone TikZ diagrams for teaching, research, and compact layouts.
- Compiles LaTeX to PDF and renders PNG previews.
- Runs static TikZ safety checks.
- Runs rendered visual QA for title-band collisions, overlap, clipping, and crowding.
- Builds contact sheets for batches and iteration rounds.
- Creates inspectable frame previews, GIFs, and contact sheets for `animate.sty` animations.

## Dependencies

The skill can be read by any agent as plain Markdown. Rendering workflows need local tools:

- Python 3.10+
- Python packages: `Pillow`, `PyMuPDF`
- TeX distribution: TeX Live or MiKTeX with `xelatex`
- Poppler command-line tools with `pdftoppm`
- `ffmpeg` for GIF/MP4 animation previews
- ImageMagick with the `magick` command for animation contact sheets

Agents should ask before installing missing dependencies. The permission request should name the package manager/source, list packages, and explain what check or render step needs them.

Common macOS setup:

```bash
brew install --cask mactex
brew install poppler ffmpeg imagemagick
python3 -m pip install Pillow PyMuPDF
```

Common Ubuntu setup:

```bash
sudo apt-get update
sudo apt-get install -y texlive-xetex texlive-latex-extra poppler-utils ffmpeg imagemagick python3-pip
python3 -m pip install Pillow PyMuPDF
```

Common Windows setup:

```powershell
winget install MiKTeX.MiKTeX
winget install Python.Python.3.12
winget install Gyan.FFmpeg
winget install ImageMagick.ImageMagick
python -m pip install Pillow PyMuPDF
```

Poppler on Windows is easiest through MSYS2, Chocolatey, or a trusted Poppler build. Verify `pdftoppm` is on `PATH`.

## Install for AI Tools

Replace `REPO_URL` with the final GitHub URL.

### Codex

Codex supports skills as folders with `SKILL.md`. The OpenAI skills catalog documents installing from a GitHub directory URL with `$skill-installer`.

```text
$skill-installer install REPO_URL/tree/main/skills/tikz-diagrams
```

Manual install:

```bash
mkdir -p ~/.codex/skills
git clone REPO_URL /tmp/tikz-diagrams-skill
rsync -a /tmp/tikz-diagrams-skill/skills/tikz-diagrams/ ~/.codex/skills/tikz-diagrams/
```

Restart Codex after installing.

After installation, the user's global skill should contain:

```text
~/.codex/skills/tikz-diagrams/
├── SKILL.md
├── references/
├── scripts/
├── templates/
└── tests/
```

### Claude Code

Claude Code skills live in `~/.claude/skills/<skill-name>/SKILL.md` for personal installs or `.claude/skills/<skill-name>/SKILL.md` for project installs.

```bash
mkdir -p ~/.claude/skills
git clone REPO_URL /tmp/tikz-diagrams-skill
rsync -a /tmp/tikz-diagrams-skill/skills/tikz-diagrams/ ~/.claude/skills/tikz-diagrams/
```

Development symlink:

```bash
ln -s "$PWD/skills/tikz-diagrams" ~/.claude/skills/tikz-diagrams
```

### Gemini CLI

Gemini CLI supports extensions with `gemini-extension.json` and a context file. This repository includes both.

```bash
gemini extensions install REPO_URL
```

Local development:

```bash
git clone REPO_URL
cd tikz-diagrams-skill
gemini extensions link .
```

### Cursor

Cursor supports project rules in `.cursor/rules` and simple root-level `AGENTS.md` instructions.

For a project:

```bash
git clone REPO_URL /tmp/tikz-diagrams-skill
cp /tmp/tikz-diagrams-skill/AGENTS.md /path/to/project/AGENTS.md
mkdir -p /path/to/project/.cursor/rules
cp /tmp/tikz-diagrams-skill/.cursor/rules/tikz-diagrams.mdc /path/to/project/.cursor/rules/
```

Then ask Cursor to read `skills/tikz-diagrams/SKILL.md` from this repository or copy the skill folder into the target project.

### VS Code and GitHub Copilot

VS Code and GitHub Copilot support repository custom instructions in `.github/copilot-instructions.md` and path-scoped `.github/instructions/*.instructions.md` files.

```bash
git clone REPO_URL /tmp/tikz-diagrams-skill
mkdir -p /path/to/project/.github/instructions
cp /tmp/tikz-diagrams-skill/.github/copilot-instructions.md /path/to/project/.github/copilot-instructions.md
cp /tmp/tikz-diagrams-skill/.github/instructions/tikz-diagrams.instructions.md /path/to/project/.github/instructions/
```

### Visual Studio with Copilot

Use the same GitHub Copilot repository instructions:

```bash
mkdir -p /path/to/project/.github/instructions
cp .github/copilot-instructions.md /path/to/project/.github/copilot-instructions.md
cp .github/instructions/tikz-diagrams.instructions.md /path/to/project/.github/instructions/
```

### Antigravity

Antigravity guidance is less standardized publicly than Codex, Claude Code, Gemini CLI, Cursor, and Copilot. The most portable approach is to use `AGENTS.md` and/or `GEMINI.md` at the project root, then tell the agent to read the skill folder.

```bash
git clone REPO_URL /tmp/tikz-diagrams-skill
cp /tmp/tikz-diagrams-skill/AGENTS.md /path/to/project/AGENTS.md
cp /tmp/tikz-diagrams-skill/GEMINI.md /path/to/project/GEMINI.md
```

## Sources Checked for Install Guidance

- Claude Code skills: https://code.claude.com/docs/en/skills
- OpenAI skills catalog: https://github.com/openai/skills
- Gemini CLI extensions: https://google-gemini.github.io/gemini-cli/docs/extensions/
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- GitHub Copilot repository instructions: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- Cursor rules: https://docs.cursor.com/context/rules-for-ai

## Quick Test

```bash
export SKILL_DIR="$PWD/skills/tikz-diagrams"
python3 "$SKILL_DIR/scripts/check_tikz_safety.py" "$SKILL_DIR/templates/standalone.tex"
```

For a real diagram, create a standalone `.tex`, then run:

```bash
python3 "$SKILL_DIR/scripts/compile_render.py" path/to/diagram.tex --visual-check --visual-mode teaching
```
