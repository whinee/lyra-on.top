#!/usr/bin/env python3
"""
scripts/freeze.py - Static export generator for lyra-on.top.

Renders FastAPI public routes through TestClient into dist/,
copies static assets, and validates output for Cloudflare Pages deployment.
"""

import shutil
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from main import app  # noqa: E402
from scripts.make_qr import generate_qr  # noqa: E402

DIST_DIR = REPO_ROOT / "dist"
STATIC_SRC = REPO_ROOT / "src" / "api" / "static"
STATIC_DEST = DIST_DIR / "static"

ROUTES_TO_FREEZE = [
    ("/", "index.html"),
    ("/404.html", "404.html"),
]


def render_routes(client: TestClient) -> bool:
    for route, dest_filename in ROUTES_TO_FREEZE:
        print(f"  Rendering route: {route} -> {dest_filename}")
        response = client.get(route)
        if route == "/404.html" and response.status_code == 404:
            pass
        elif response.status_code != 200:
            print(f"Error: Route {route} returned status {response.status_code}", file=sys.stderr)
            return False

        dest_path = DIST_DIR / dest_filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(response.content)
        print(f"    Wrote {dest_path.stat().st_size} bytes to {dest_filename}")
    return True


def copy_static_assets() -> bool:
    print(f"  Copying static assets from {STATIC_SRC} -> {STATIC_DEST}...")
    if not STATIC_SRC.exists():
        print(f"Error: Static directory not found: {STATIC_SRC}", file=sys.stderr)
        return False
    shutil.copytree(STATIC_SRC, STATIC_DEST, dirs_exist_ok=True)
    if (STATIC_SRC / "robots.txt").exists():
        shutil.copy2(STATIC_SRC / "robots.txt", DIST_DIR / "robots.txt")
    if (STATIC_SRC / "sitemap.xml").exists():
        shutil.copy2(STATIC_SRC / "sitemap.xml", DIST_DIR / "sitemap.xml")
    return True


def verify_dist() -> bool:
    index_file = DIST_DIR / "index.html"
    not_found_file = DIST_DIR / "404.html"
    if not index_file.exists() or index_file.stat().st_size == 0:
        print("Error: dist/index.html is missing or empty!", file=sys.stderr)
        return False
    if not not_found_file.exists() or not_found_file.stat().st_size == 0:
        print("Error: dist/404.html is missing or empty!", file=sys.stderr)
        return False
    return True


def main() -> int:
    print(f"Freezing site into {DIST_DIR}...")
    generate_qr()
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    client = TestClient(app)
    if not render_routes(client) or not copy_static_assets() or not verify_dist():
        return 1

    total_size = sum(f.stat().st_size for f in DIST_DIR.rglob("*") if f.is_file())
    print(f"Static freeze successful! Total size: {total_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
