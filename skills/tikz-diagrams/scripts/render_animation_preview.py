#!/usr/bin/env python3
"""Render an animation frame-deck PDF into PNG frames, GIF, and contact sheet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        if proc.stdout:
            print(proc.stdout[-4000:])
        if proc.stderr:
            print(proc.stderr[-4000:], file=sys.stderr)
        raise SystemExit(proc.returncode)


def natural_key(path: Path) -> list[int | str]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p for p in parts]


def pick_key_frames(frames: list[Path], requested: list[int] | None) -> list[Path]:
    if requested:
        picked = []
        for n in requested:
            idx = n - 1
            if idx < 0 or idx >= len(frames):
                raise SystemExit(f"ERROR: key frame {n} is outside 1..{len(frames)}")
            picked.append(frames[idx])
        return picked
    if len(frames) <= 4:
        return frames
    idxs = [0, len(frames) // 3, (2 * len(frames)) // 3, len(frames) - 1]
    return [frames[i] for i in dict.fromkeys(idxs)]


def ffmpeg_input_pattern(frames: list[Path]) -> Path:
    match = re.match(r"^(.*-)(\d+)(\.png)$", frames[0].name)
    if not match:
        raise SystemExit(f"ERROR: cannot infer ffmpeg pattern from {frames[0].name}")
    prefix, digits, suffix = match.groups()
    width = len(digits)
    spec = f"%0{width}d" if width > 1 else "%d"
    return frames[0].parent / f"{prefix}{spec}{suffix}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Frame-deck PDF; each page is one animation frame")
    parser.add_argument("--output-dir", help="Output directory; defaults beside PDF")
    parser.add_argument("--stem", help="Output file stem; defaults to PDF stem without _frames suffix")
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--scale-width", type=int, default=960)
    parser.add_argument("--key-frames", help="Comma-separated 1-based frame numbers for contact sheet")
    parser.add_argument("--tile", default="2x2", help="ImageMagick montage tile layout")
    args = parser.parse_args(argv[1:])

    pdf = Path(args.pdf).resolve()
    if not pdf.exists():
        print(f"ERROR: PDF not found: {pdf}", file=sys.stderr)
        return 2

    out_dir = Path(args.output_dir).resolve() if args.output_dir else pdf.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or re.sub(r"_frames(_v\d+)?$", r"_preview\1", pdf.stem)
    frames_dir = out_dir / f"{stem}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    prefix = frames_dir / "frame"
    for old in frames_dir.glob("frame-*.png"):
        old.unlink()
    run(["pdftoppm", "-png", "-r", str(args.dpi), str(pdf), str(prefix)], out_dir)
    frames = sorted(frames_dir.glob("frame-*.png"), key=natural_key)
    if not frames:
        print(f"ERROR: no frames rendered into {frames_dir}", file=sys.stderr)
        return 1
    frame_pattern = ffmpeg_input_pattern(frames)

    palette = out_dir / f"{stem}_palette.png"
    gif = out_dir / f"{stem}.gif"
    contact = out_dir / f"{stem}_contact.png"
    manifest = out_dir / f"{stem}_manifest.json"

    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(args.fps),
            "-i",
            str(frame_pattern),
            "-vf",
            f"scale={args.scale_width}:-1:flags=lanczos,palettegen",
            str(palette),
        ],
        out_dir,
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(args.fps),
            "-i",
            str(frame_pattern),
            "-i",
            str(palette),
            "-lavfi",
            f"scale={args.scale_width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
            str(gif),
        ],
        out_dir,
    )

    key_frames = None
    if args.key_frames:
        key_frames = [int(p.strip()) for p in args.key_frames.split(",") if p.strip()]
    contact_frames = pick_key_frames(frames, key_frames)
    run(
        [
            "magick",
            "montage",
            *[str(p) for p in contact_frames],
            "-tile",
            args.tile,
            "-geometry",
            "+16+16",
            "-background",
            "white",
            str(contact),
        ],
        out_dir,
    )

    data = {
        "pdf": str(pdf),
        "frames_dir": str(frames_dir),
        "ffmpeg_input_pattern": str(frame_pattern),
        "frame_count": len(frames),
        "frames": [p.name for p in frames],
        "gif": str(gif),
        "contact_sheet": str(contact),
        "contact_frames": [p.name for p in contact_frames],
    }
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"OK: rendered {len(frames)} frames")
    print(f"GIF: {gif}")
    print(f"CONTACT: {contact}")
    print(f"MANIFEST: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
