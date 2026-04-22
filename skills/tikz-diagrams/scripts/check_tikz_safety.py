#!/usr/bin/env python3
"""Static safety checks for TikZ diagram sources.

This is intentionally conservative. It catches common authoring hazards before
LaTeX compilation and before visual QA.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


EDGE_NODE_RE = re.compile(r"\\draw\b[^;\n]*--\s*node\s*\{", re.MULTILINE)
LONG_NODE_RE = re.compile(r"\\node(?:\[[^\]]*\])?\s*\{([^{}]{70,})\}")


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    if "\\begin{tikzpicture}" not in text:
        issues.append("missing \\begin{tikzpicture}")

    if EDGE_NODE_RE.search(text):
        issues.append("unpositioned inline edge label: use node[above]/node[below] or a separate label node")

    for match in LONG_NODE_RE.finditer(text):
        snippet = " ".join(match.group(1).split())[:90]
        issues.append(f"long raw node text without explicit wrapping: {snippet!r}")

    if "\\documentclass" not in text and "\\begin{document}" in text:
        issues.append("has document body but no documentclass")

    if re.search(r"\\node\[[^\]]*rotate=90[^\]]*\]", text) and "anchor=" not in text:
        issues.append("rotated node without explicit anchor may collide or clip")

    if text.count("\\begin{tikzpicture}") != text.count("\\end{tikzpicture}"):
        issues.append("mismatched tikzpicture begin/end count")

    return issues


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_tikz_safety.py <file.tex> [more.tex ...]", file=sys.stderr)
        return 2

    files: list[Path] = []
    for arg in argv[1:]:
        p = Path(arg)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.tex")))
        else:
            files.append(p)

    failed = False
    checked = 0
    for path in files:
        if not path.exists():
            print(f"ERROR: {path}: file does not exist")
            failed = True
            continue
        issues = check_file(path)
        checked += 1
        if issues:
            failed = True
            for issue in issues:
                print(f"ERROR: {path}: {issue}")

    if failed:
        print(f"FAILED: {checked} file(s) checked")
        return 1
    print(f"OK: {checked} file(s) pass TikZ safety checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
