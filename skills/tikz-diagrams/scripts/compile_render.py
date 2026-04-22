#!/usr/bin/env python3
"""Compile a standalone TikZ/LaTeX file and render it to PNG."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stdout[-4000:])
        print(proc.stderr[-4000:], file=sys.stderr)
        raise SystemExit(proc.returncode)


def png_nonblank(path: Path) -> bool:
    try:
        from PIL import Image
    except Exception:
        return path.exists() and path.stat().st_size > 1000

    if not path.exists() or path.stat().st_size < 1000:
        return False
    im = Image.open(path).convert("L")
    extrema = im.getextrema()
    return extrema != (255, 255)


def run_visual_check(pdf: Path, mode: str, report: Path | None) -> int:
    script = Path(__file__).resolve().parent / "check_tikz_visual.py"
    cmd = [sys.executable, str(script), str(pdf), "--mode", mode]
    if report is not None:
        cmd.extend(["--report", str(report)])
    proc = subprocess.run(cmd, cwd=pdf.parent, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        filtered = []
        ignored_screen_warning = False
        for line in proc.stderr.splitlines():
            if "cannot create appearance stream for Screen annotations" in line:
                ignored_screen_warning = True
                continue
            filtered.append(line)
        if filtered:
            print("\n".join(filtered), file=sys.stderr)
        if ignored_screen_warning:
            print("NOTE: ignored MuPDF Screen-annotation appearance warning from animate.sty PDF.", file=sys.stderr)
    return proc.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", help="Path to .tex file")
    parser.add_argument("--engine", default="xelatex", help="LaTeX engine, default xelatex")
    parser.add_argument("--dpi", type=int, default=180, help="PNG render DPI")
    parser.add_argument("--visual-check", action="store_true", help="Run rendered visual QA after PNG creation")
    parser.add_argument("--visual-mode", choices=["teaching", "research", "compact"], default="teaching")
    parser.add_argument("--visual-report", help="Optional JSON report path; defaults to <stem>-visual-qa.json when visual checking")
    args = parser.parse_args(argv[1:])

    tex = Path(args.tex).resolve()
    if not tex.exists():
        print(f"ERROR: {tex} does not exist", file=sys.stderr)
        return 2

    cwd = tex.parent
    stem = tex.stem
    run([args.engine, "-interaction=nonstopmode", "-halt-on-error", tex.name], cwd)

    pdf = cwd / f"{stem}.pdf"
    if not pdf.exists():
        print(f"ERROR: expected PDF not found: {pdf}", file=sys.stderr)
        return 1

    out_prefix = cwd / stem
    run(["pdftoppm", "-png", "-r", str(args.dpi), "-singlefile", str(pdf), str(out_prefix)], cwd)

    png = cwd / f"{stem}.png"
    if not png_nonblank(png):
        print(f"ERROR: rendered PNG appears blank or missing: {png}", file=sys.stderr)
        return 1

    if args.visual_check:
        report = Path(args.visual_report).resolve() if args.visual_report else cwd / f"{stem}-visual-qa.json"
        rc = run_visual_check(pdf, args.visual_mode, report)
        if rc != 0:
            return rc

    print(f"OK: {tex}")
    print(f"PDF: {pdf}")
    print(f"PNG: {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
