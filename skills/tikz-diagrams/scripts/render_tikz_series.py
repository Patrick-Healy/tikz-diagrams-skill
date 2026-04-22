#!/usr/bin/env python3
"""Render a controlled series of TikZ diagram variants from a JSON manifest.

The manifest applies small text replacements step by step. By default each step
starts from the previous step's source, which supports researcher-style
iteration: keep the geometry stable, change one control, render, QA, repeat.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CHECK_SAFETY = SCRIPT_DIR / "check_tikz_safety.py"
COMPILE_RENDER = SCRIPT_DIR / "compile_render.py"
CONTACT_SHEET = SCRIPT_DIR / "make_contact_sheet.py"


def run(cmd: list[str], cwd: Path, allow_fail: bool = False) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")
    if proc.returncode != 0 and not allow_fail:
        raise SystemExit(proc.returncode)
    return proc


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "source" not in data:
        raise SystemExit("manifest must include 'source'")
    if "steps" not in data or not isinstance(data["steps"], list) or not data["steps"]:
        raise SystemExit("manifest must include a non-empty 'steps' list")
    return data


def resolve_manifest_path(value: str | Path, manifest_dir: Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return (manifest_dir / path).resolve()


def apply_replacements(text: str, replacements: dict[str, str], *, strict: bool) -> str:
    for old, new in replacements.items():
        if strict and old not in text:
            raise SystemExit(f"replacement key not found in source: {old!r}")
        text = text.replace(old, str(new))
    return text


def write_qa_note(output_dir: Path, manifest: dict, records: list[dict], contact_sheet: Path | None) -> Path:
    note = output_dir / "series_qa_note.md"
    lines = [
        "# TikZ Series QA Note",
        "",
        f"Series: `{manifest.get('series_name', output_dir.name)}`",
        f"Source: `{manifest['source']}`",
        f"Default visual mode: `{manifest.get('visual_mode', 'teaching')}`",
        f"Cumulative steps: `{manifest.get('cumulative', True)}`",
        "",
        "## Steps",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"- `{record['name']}`: mode `{record['mode']}`, status `{record['status']}`",
                f"  - TeX: `{record['tex']}`",
                f"  - PNG: `{record['png']}`",
                f"  - Visual QA: `{record['visual_report']}`",
            ]
        )
    if contact_sheet is not None:
        lines.extend(["", f"Contact sheet: `{contact_sheet}`"])
    lines.append("")
    note.write_text("\n".join(lines), encoding="utf-8")
    return note


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="JSON manifest describing the variant series")
    parser.add_argument("--keep-going", action="store_true", help="Continue after visual QA failures")
    parser.add_argument("--no-contact-sheet", action="store_true")
    args = parser.parse_args(argv[1:])

    manifest_path = Path(args.manifest).resolve()
    manifest = load_manifest(manifest_path)
    manifest_dir = manifest_path.parent
    source = resolve_manifest_path(manifest["source"], manifest_dir)
    if not source.exists():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        return 2

    output_dir = resolve_manifest_path(manifest.get("output_dir", f"{source.stem}_series"), manifest_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_text = source.read_text(encoding="utf-8")
    current_text = base_text
    default_mode = manifest.get("visual_mode", "teaching")
    strict = bool(manifest.get("strict_replacements", True))
    cumulative = bool(manifest.get("cumulative", True))
    records: list[dict] = []
    any_failed = False

    for idx, step in enumerate(manifest["steps"], start=1):
        name = step.get("name", f"step_{idx:02d}")
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name).strip("_")
        if not safe_name:
            safe_name = f"step_{idx:02d}"
        mode = step.get("visual_mode", step.get("mode", default_mode))
        replacements = step.get("replacements", {})
        if not isinstance(replacements, dict):
            raise SystemExit(f"step {name!r} replacements must be an object")

        start_text = current_text if cumulative else base_text
        next_text = apply_replacements(start_text, replacements, strict=strict)
        tex = output_dir / f"{idx:02d}_{safe_name}.tex"
        tex.write_text(next_text, encoding="utf-8")
        current_text = next_text

        run([sys.executable, str(CHECK_SAFETY), str(tex)], output_dir)
        visual_report = output_dir / f"{tex.stem}-visual-qa.json"
        proc = run(
            [
                sys.executable,
                str(COMPILE_RENDER),
                str(tex),
                "--visual-check",
                "--visual-mode",
                mode,
                "--visual-report",
                str(visual_report),
            ],
            output_dir,
            allow_fail=args.keep_going,
        )
        status = "pass"
        if visual_report.exists():
            try:
                status = json.loads(visual_report.read_text(encoding="utf-8")).get("status", "unknown")
            except Exception:
                status = "unknown"
        if proc.returncode != 0:
            any_failed = True
            status = "fail"

        records.append(
            {
                "name": name,
                "mode": mode,
                "status": status,
                "tex": str(tex),
                "png": str(tex.with_suffix(".png")),
                "visual_report": str(visual_report),
            }
        )

    contact_sheet: Path | None = None
    if not args.no_contact_sheet:
        contact_sheet = output_dir / "series_contact_sheet.png"
        pngs = [record["png"] for record in records if Path(record["png"]).exists()]
        if pngs:
            run(
                [sys.executable, str(CONTACT_SHEET), pngs[0], *pngs[1:], "--output", str(contact_sheet), "--show-qa"],
                output_dir,
                allow_fail=args.keep_going,
            )

    note = write_qa_note(output_dir, manifest, records, contact_sheet)
    shutil.copy2(manifest_path, output_dir / manifest_path.name)
    print(f"QA note: {note}")
    return 1 if any_failed and not args.keep_going else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
