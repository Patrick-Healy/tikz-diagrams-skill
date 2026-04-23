#!/usr/bin/env python3
"""Rendered visual QA checks for TikZ PDF/PNG artifacts.

The checker is intentionally conservative. It is not a replacement for human
inspection, but it catches common slide-killing problems that static TikZ checks
cannot see: title-band collisions, overlapping text boxes, clipped labels, and
annotation-heavy teaching diagrams with crowded callouts.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


MODE_LIMITS = {
    "teaching": {
        "edge_margin": 3.0,
        "title_margin": 4.0,
        "overlap_tol": 1.2,
        "max_top_band_boxes": 4,
        "min_text_gap": 1.0,
    },
    "research": {
        "edge_margin": 4.0,
        "title_margin": 6.0,
        "overlap_tol": 0.8,
        "max_top_band_boxes": 2,
        "min_text_gap": 1.5,
    },
    "compact": {
        "edge_margin": 2.0,
        "title_margin": 3.0,
        "overlap_tol": 0.5,
        "max_top_band_boxes": 1,
        "min_text_gap": 0.7,
    },
}

TITLE_RE = re.compile(r"^[A-Z0-9][A-Za-z0-9 /:&,\-()]+$")
CALLOUT_RE = re.compile(
    r"\b(effect|jump|cutoff|starts|policy|trend|parallel|diagnostic|lags?|leads?|risk|assumption|message)\b",
    re.IGNORECASE,
)


@dataclass
class Box:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    colors: list[int] | None = None

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def area(self) -> float:
        return max(0.0, self.width) * max(0.0, self.height)

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2.0

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2.0

    def inflate(self, margin: float) -> "Box":
        return Box(self.text, self.x0 - margin, self.y0 - margin, self.x1 + margin, self.y1 + margin, self.colors)


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    boxes: list[str]


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def intersect(a: Box, b: Box) -> tuple[float, float, float]:
    ix = max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0))
    iy = max(0.0, min(a.y1, b.y1) - max(a.y0, b.y0))
    area = ix * iy
    return ix, iy, area


def close_gap(a: Box, b: Box) -> float:
    dx = max(0.0, max(a.x0, b.x0) - min(a.x1, b.x1))
    dy = max(0.0, max(a.y0, b.y0) - min(a.y1, b.y1))
    return math.hypot(dx, dy)


def text_boxes_from_pdf(pdf: Path) -> tuple[float, float, list[Box]]:
    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"ERROR: PyMuPDF is required for visual checks: {exc}") from exc
    try:
        fitz.TOOLS.mupdf_display_errors(False)
    except Exception:
        pass

    doc = fitz.open(pdf)
    if len(doc) < 1:
        raise SystemExit(f"ERROR: {pdf} has no pages")
    page = doc[0]
    page_rect = page.rect
    boxes: list[Box] = []
    data = page.get_text("dict")

    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if normalize_text(s.get("text", ""))]
            if not spans:
                continue
            text = normalize_text("".join(s.get("text", "") for s in spans))
            x0 = min(float(s["bbox"][0]) for s in spans)
            y0 = min(float(s["bbox"][1]) for s in spans)
            x1 = max(float(s["bbox"][2]) for s in spans)
            y1 = max(float(s["bbox"][3]) for s in spans)
            colors = sorted({int(s.get("color", 0)) for s in spans})
            boxes.append(Box(text=text, x0=x0, y0=y0, x1=x1, y1=y1, colors=colors))

    boxes.sort(key=lambda b: (b.y0, b.x0))
    return float(page_rect.width), float(page_rect.height), boxes


def int_to_rgb(color: int) -> tuple[int, int, int]:
    return ((color >> 16) & 255, (color >> 8) & 255, color & 255)


DEFAULT_PLOT_LABEL_RE = re.compile(
    r"(τ|tau|DiD|\bATT\b|\bATE\b|effect|estimate|coef|coefficient|gap|jump|bracket)",
    re.IGNORECASE,
)


def text_box_plot_pixels(
    pdf: Path,
    boxes: list[Box],
    dpi: int = 180,
    label_re: re.Pattern[str] = DEFAULT_PLOT_LABEL_RE,
) -> list[tuple[Box, int, int]]:
    """Find non-text, non-background pixels inside text boxes.

    This is a deliberately conservative fine-grained gate for direct labels on
    plots. It catches labels placed over curve/bracket/axis strokes, a failure
    mode that PDF text-box overlap checks miss because the colliding geometry is
    not text. The heuristic ignores pixels matching the text's own span color and
    near-white/light-gray antialiasing from the label background.
    """
    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"ERROR: PyMuPDF is required for visual checks: {exc}") from exc
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"ERROR: Pillow is required for text/plot overlap checks: {exc}") from exc

    doc = fitz.open(pdf)
    page = doc[0]
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    try:
        import numpy as np
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"ERROR: numpy is required for text/plot overlap checks: {exc}") from exc

    results: list[tuple[Box, int, int]] = []
    for box in boxes:
        if len(box.text.strip()) <= 1:
            continue
        if not label_re.search(box.text):
            continue
        pad = 1.5
        x0 = max(0, int((box.x0 - pad) * zoom))
        y0 = max(0, int((box.y0 - pad) * zoom))
        x1 = min(image.width, int((box.x1 + pad) * zoom))
        y1 = min(image.height, int((box.y1 + pad) * zoom))
        if x1 <= x0 or y1 <= y0:
            continue

        arr = np.array(image.crop((x0, y0, x1, y1))).astype(np.int16)
        red = arr[:, :, 0]
        green = arr[:, :, 1]
        blue = arr[:, :, 2]

        near_white = (red > 215) & (green > 215) & (blue > 215)
        light_gray = (abs(red - green) < 10) & (abs(green - blue) < 10) & (red > 155)
        allowed = near_white | light_gray

        for color in box.colors or []:
            tr, tg, tb = int_to_rgb(color)
            # Allow antialiased pixels close to the text color.
            dist = abs(red - tr) + abs(green - tg) + abs(blue - tb)
            allowed |= dist < 95

        # For the fine-grained gate, focus on plotted strokes from common
        # semantic palettes. Do not count red pixels by default because many
        # effect labels are themselves red; red-on-red bracket checks are better
        # handled by moving the label outside the bracket or giving it a
        # background.
        colored_or_dark = (
            ((blue > 90) & (blue > red + 18) & (blue > green))
            | ((green > 70) & (green > red + 15) & (blue > 40) & (blue < 200))
            | ((red < 85) & (green < 95) & (blue < 115))
        )
        bad = colored_or_dark & ~allowed
        bad_count = int(bad.sum())
        total = int(arr.shape[0] * arr.shape[1])
        if bad_count >= 8 and bad_count / max(total, 1) > 0.002:
            results.append((box, bad_count, total))

    return results


def likely_title(boxes: list[Box], page_width: float, page_height: float) -> Box | None:
    top_candidates = [
        b
        for b in boxes
        if b.y0 < page_height * 0.22
        and b.width > page_width * 0.22
        and len(b.text) >= 8
        and TITLE_RE.match(b.text)
    ]
    if not top_candidates:
        top_candidates = [b for b in boxes if b.y0 < page_height * 0.2 and len(b.text) >= 8]
    if not top_candidates:
        return None
    return max(top_candidates, key=lambda b: (b.height, b.width))


def check_visual(
    pdf: Path,
    mode: str,
    text_plot_overlap: bool = False,
    plot_label_regex: str | None = None,
) -> dict:
    limits = MODE_LIMITS[mode]
    page_width, page_height, boxes = text_boxes_from_pdf(pdf)
    issues: list[Issue] = []

    edge = limits["edge_margin"]
    for b in boxes:
        if b.x0 < edge or b.y0 < edge or page_width - b.x1 < edge or page_height - b.y1 < edge:
            issues.append(
                Issue(
                    severity="warn",
                    code="near_edge",
                    message=f"Text is close to the page edge: {b.text!r}",
                    boxes=[b.text],
                )
            )

    title = likely_title(boxes, page_width, page_height)
    if title is not None:
        protected = Box(
            "title protected band",
            0,
            max(0.0, title.y0 - limits["title_margin"]),
            page_width,
            min(page_height, title.y1 + limits["title_margin"]),
        )
        for b in boxes:
            if b is title:
                continue
            _, _, area = intersect(protected, b)
            if area > 0:
                issues.append(
                    Issue(
                        severity="error",
                        code="title_band_collision",
                        message=f"Text enters protected title band near {title.text!r}: {b.text!r}",
                        boxes=[title.text, b.text],
                    )
                )

    overlap_tol = limits["overlap_tol"]
    min_gap = limits["min_text_gap"]
    for i, a in enumerate(boxes):
        if len(a.text) <= 1:
            continue
        for b in boxes[i + 1 :]:
            if len(b.text) <= 1:
                continue
            ix, iy, area = intersect(a.inflate(0.2), b.inflate(0.2))
            if area > overlap_tol and ix > 0.6 and iy > 0.6:
                issues.append(
                    Issue(
                        severity="error",
                        code="text_overlap",
                        message=f"Text boxes overlap: {a.text!r} and {b.text!r}",
                        boxes=[a.text, b.text],
                    )
                )
            elif close_gap(a, b) < min_gap and abs(a.cy - b.cy) < max(a.height, b.height) * 0.75:
                issues.append(
                    Issue(
                        severity="warn",
                        code="text_crowding",
                        message=f"Text boxes are very close: {a.text!r} and {b.text!r}",
                        boxes=[a.text, b.text],
                    )
                )

    top_band = page_height * 0.27
    top_callouts = [
        b for b in boxes if b.y0 < top_band and b is not title and CALLOUT_RE.search(b.text) and len(b.text) > 4
    ]
    if len(top_callouts) > limits["max_top_band_boxes"]:
        issues.append(
            Issue(
                severity="warn",
                code="crowded_top_annotations",
                message=f"{len(top_callouts)} annotation-like text boxes appear in the top band",
                boxes=[b.text for b in top_callouts],
            )
        )

    if text_plot_overlap:
        label_re = re.compile(plot_label_regex, re.IGNORECASE) if plot_label_regex else DEFAULT_PLOT_LABEL_RE
        for box, bad_count, total in text_box_plot_pixels(pdf, boxes, label_re=label_re):
            issues.append(
                Issue(
                    severity="error",
                    code="text_plot_overlap",
                    message=f"Targeted text box appears to cover plotted geometry: {box.text!r} ({bad_count}/{total} plot-colored pixels inside text box)",
                    boxes=[box.text],
                )
            )

    report = {
        "pdf": str(pdf),
        "mode": mode,
        "text_plot_overlap_check": text_plot_overlap,
        "plot_label_regex": plot_label_regex or DEFAULT_PLOT_LABEL_RE.pattern if text_plot_overlap else None,
        "page": {"width": page_width, "height": page_height},
        "text_box_count": len(boxes),
        "title": asdict(title) if title else None,
        "issues": [asdict(issue) for issue in issues],
        "status": "fail" if any(i.severity == "error" for i in issues) else "warn" if issues else "pass",
    }
    return report


def print_report(report: dict) -> None:
    status = report["status"].upper()
    print(f"{status}: {report['pdf']} ({report['mode']} mode)")
    for issue in report["issues"]:
        print(f"{issue['severity'].upper()}: {issue['code']}: {issue['message']}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Rendered PDF to inspect")
    parser.add_argument("--mode", choices=sorted(MODE_LIMITS), default="teaching")
    parser.add_argument("--report", help="Optional JSON report path")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument(
        "--text-plot-overlap",
        action="store_true",
        help="Run targeted text-box-vs-rendered-geometry check for effect/estimate/callout labels",
    )
    parser.add_argument(
        "--plot-label-regex",
        help="Regex for labels to include in --text-plot-overlap; defaults to effect/estimate terms",
    )
    args = parser.parse_args(argv[1:])

    pdf = Path(args.pdf).resolve()
    if not pdf.exists():
        print(f"ERROR: PDF not found: {pdf}", file=sys.stderr)
        return 2

    report = check_visual(pdf, args.mode, args.text_plot_overlap, args.plot_label_regex)
    print_report(report)

    if args.report:
        out = Path(args.report).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if report["status"] == "fail" or (args.warnings_as_errors and report["status"] == "warn"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
