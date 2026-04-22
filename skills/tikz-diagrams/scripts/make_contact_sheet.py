#!/usr/bin/env python3
"""Create a contact sheet from rendered PNG diagrams."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def qa_badge(path: Path) -> tuple[str, tuple[int, int, int]]:
    report = path.with_name(f"{path.stem}-visual-qa.json")
    if not report.exists():
        return "QA: not run", (102, 112, 133)
    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except Exception:
        return "QA: unreadable", (169, 76, 76)
    status = data.get("status", "unknown")
    if status == "pass":
        return "QA: pass", (40, 124, 114)
    if status == "warn":
        return "QA: warn", (183, 131, 47)
    return "QA: fail", (169, 76, 76)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Directory containing PNGs, or one or more PNGs")
    parser.add_argument("extra", nargs="*", help="Additional PNG files")
    parser.add_argument("--output", required=True, help="Output contact sheet PNG")
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--thumb-width", type=int, default=380)
    parser.add_argument("--thumb-height", type=int, default=280)
    parser.add_argument("--show-qa", action="store_true", help="Show visual QA badge from sibling *-visual-qa.json files")
    args = parser.parse_args()

    paths: list[Path] = []
    first = Path(args.input)
    if first.is_dir():
        paths.extend(sorted(p for p in first.rglob("*.png") if "contact-sheet" not in p.name))
    else:
        paths.append(first)
    paths.extend(Path(p) for p in args.extra)

    paths = [p for p in paths if p.exists()]
    if not paths:
        raise SystemExit("no PNG files found")

    font = ImageFont.load_default()
    tile_w = args.thumb_width
    tile_h = args.thumb_height + 42
    cols = max(1, args.cols)
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows * tile_h), (245, 247, 250))

    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        im.thumbnail((args.thumb_width - 24, args.thumb_height - 20), Image.LANCZOS)
        tile = Image.new("RGB", (tile_w, tile_h), "white")
        tile.paste(im, ((tile_w - im.width) // 2, 10))
        label = path.stem[:52]
        draw = ImageDraw.Draw(tile)
        draw.text((12, args.thumb_height + 10), label, fill=(35, 49, 66), font=font)
        if args.show_qa:
            badge, color = qa_badge(path)
            draw.text((12, args.thumb_height + 26), badge, fill=color, font=font)
        sheet.paste(tile, ((i % cols) * tile_w, (i // cols) * tile_h))

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
