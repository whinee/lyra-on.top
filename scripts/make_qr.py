#!/usr/bin/env python3
"""
Build-time QR code generator using segno.

Generates static SVG QR code for the Hack & Yap talk slides.
Target URL is read from src/api/config/values/content.yml.
If slides_url is 'TODO(lyra)', falls back to 'https://lyra-on.top#slides'.
Outputs to src/api/static/assets/images/slides-qr.svg.
"""

import sys
from pathlib import Path

import segno
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_PATH = ROOT / "src" / "api" / "config" / "values" / "content.yml"
OUTPUT_PATH = ROOT / "src" / "api" / "static" / "assets" / "images" / "slides-qr.svg"
FALLBACK_URL = "https://lyra-on.top#slides"


def generate_qr() -> Path:
    if not CONTENT_PATH.exists():
        print(f"Error: {CONTENT_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(CONTENT_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    slides_info = data.get("slides", {})
    slides_url = slides_info.get("slides_url", "").strip()

    target_url = slides_url if slides_url and slides_url != "TODO(lyra)" else FALLBACK_URL
    print(f"Generating QR code for target: {target_url}")

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # High-contrast palette: dark base #191a28 on white #ffffff for optimal camera scan
    qr = segno.make_qr(target_url, error="m")
    qr.save(
        OUTPUT_PATH,
        scale=8,
        border=3,
        dark="#191a28",
        light="#ffffff",
        finder_dark="#3b3fa8",  # Blurple accent on finder patterns
    )
    print(f"Saved QR code SVG to {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate_qr()
