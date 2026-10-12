#!/usr/bin/env python3
"""
scripts/freeze.py - Static export generator for lyra-on.top.

Enumerates all active routes and collection slugs honoring the Auto-Hide rule,
renders via FastAPI TestClient into dist/, copies static assets, builds sitemap.xml
and _redirects, and verifies output for Cloudflare Pages deployment.
"""

import shutil
import sys
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from main import app  # noqa: E402
from scripts.make_qr import generate_qr  # noqa: E402
from src.api.config.content_loader import load_all_content  # noqa: E402

DIST_DIR = REPO_ROOT / "dist"
STATIC_SRC = REPO_ROOT / "src" / "api" / "static"
STATIC_DEST = DIST_DIR / "static"


def _collect_content_routes(catalog) -> list[tuple[str, str]]:
    routes: list[tuple[str, str]] = []
    if catalog.has_projects:
        routes.append(("/projects", "projects/index.html"))
        routes.extend([
            (f"/projects/{p.slug}", f"projects/{p.slug}/index.html")
            for p in catalog.public_projects
            if p.body
        ])
    if catalog.has_talks:
        routes.append(("/talks", "talks/index.html"))
    return routes


def _collect_writing_routes(catalog) -> list[tuple[str, str]]:
    routes: list[tuple[str, str]] = []
    if catalog.has_writing:
        routes.append(("/writing", "writing/index.html"))
    if catalog.has_poems:
        routes.append(("/writing/poems", "writing/poems/index.html"))
        routes.extend([
            (f"/writing/poems/{p.slug}", f"writing/poems/{p.slug}/index.html")
            for p in catalog.public_poems
        ])
    if catalog.has_song_analysis:
        routes.append(("/writing/song-analysis", "writing/song-analysis/index.html"))
        routes.extend([
            (f"/writing/song-analysis/{s.slug}", f"writing/song-analysis/{s.slug}/index.html")
            for s in catalog.public_song_analysis
        ])
    if catalog.has_blog:
        routes.extend([
            ("/blog", "blog/index.html"),
            ("/blog/rss.xml", "blog/rss.xml"),
            ("/blog/rss.xml", "rss.xml"),
        ])
        routes.extend([
            (f"/blog/{b.slug}", f"blog/{b.slug}/index.html")
            for b in catalog.public_blog
        ])
    return routes


def get_routes_to_freeze() -> list[tuple[str, str]]:
    """Determine all active routes based on Auto-Hide rule and content catalog."""
    catalog = load_all_content()
    routes: list[tuple[str, str]] = [
        ("/", "index.html"),
        ("/404.html", "404.html"),
        ("/resume", "resume/index.html"),
        ("/cv", "cv/index.html"),
        ("/contacts", "contacts/index.html"),
    ]
    routes.extend(_collect_content_routes(catalog))
    routes.extend(_collect_writing_routes(catalog))
    return routes


def render_routes(client: TestClient, routes: list[tuple[str, str]]) -> bool:
    for route, dest_filename in routes:
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


def generate_sitemap(routes: list[tuple[str, str]]) -> None:
    """Generate dist/sitemap.xml for all frozen public pages."""
    catalog = load_all_content()
    base_url = catalog.site.url.rstrip("/")
    today = date.today().isoformat()

    url_entries = []
    for route, dest in routes:
        if dest.endswith(".html") and dest != "404.html":
            page_url = base_url if route == "/" else f"{base_url}{route}"
            url_entries.append(f"""  <url>
    <loc>{page_url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
  </url>""")

    body = "\n".join(url_entries)
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>"""

    (DIST_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"  Generated sitemap.xml with {len(url_entries)} URLs")


def generate_redirects() -> None:
    """Generate dist/_redirects for Cloudflare Pages rewrites and redirects."""
    redirects = """# Cloudflare Pages _redirects
/cv  /resume  301
/slides  https://lyra-on.top/#slides  302
"""
    (DIST_DIR / "_redirects").write_text(redirects, encoding="utf-8")
    print("  Generated dist/_redirects")


def copy_static_assets() -> bool:
    print(f"  Copying static assets from {STATIC_SRC} -> {STATIC_DEST}...")
    if not STATIC_SRC.exists():
        print(f"Error: Static directory not found: {STATIC_SRC}", file=sys.stderr)
        return False
    shutil.copytree(STATIC_SRC, STATIC_DEST, dirs_exist_ok=True)
    if (STATIC_SRC / "robots.txt").exists():
        shutil.copy2(STATIC_SRC / "robots.txt", DIST_DIR / "robots.txt")
    return True


def verify_dist() -> bool:
    required_files = [
        DIST_DIR / "index.html",
        DIST_DIR / "404.html",
        DIST_DIR / "resume" / "index.html",
        DIST_DIR / "contacts" / "index.html",
        DIST_DIR / "sitemap.xml",
        DIST_DIR / "_redirects",
    ]
    for rf in required_files:
        if not rf.exists() or rf.stat().st_size == 0:
            print(f"Error: {rf.relative_to(REPO_ROOT)} is missing or empty!", file=sys.stderr)
            return False
    return True


def main() -> int:
    print(f"Freezing site into {DIST_DIR}...")
    generate_qr()
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    client = TestClient(app)
    routes = get_routes_to_freeze()
    print(f"Discovered {len(routes)} active route(s) honoring auto-hide rules:")

    if not render_routes(client, routes):
        return 1
    if not copy_static_assets():
        return 1

    generate_sitemap(routes)
    generate_redirects()

    if not verify_dist():
        return 1

    total_size = sum(f.stat().st_size for f in DIST_DIR.rglob("*") if f.is_file())
    print(f"\nStatic freeze successful! Total size: {total_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
