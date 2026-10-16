#!/usr/bin/env python3
"""
scripts/freeze.py - Static export generator for lyra-on.top.

Enumerates all active routes and collection slugs honoring the Auto-Hide rule,
renders via FastAPI TestClient into dist/, copies static assets, builds sitemap.xml,
_redirects, llms.txt, and llms-full.txt, and verifies output for Cloudflare Pages deployment.
"""

import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any

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


def generate_llms_txt(catalog: Any, base_url: str) -> str:
    """Generate llms.txt content following llmstxt.org proposal."""
    llms_txt = f"""# {catalog.site.author_display_name}

> {catalog.site.description}

## Summary
- Author: {catalog.site.author_display_name}
- Tagline: {catalog.site.tagline}
- Site: {base_url}
- Public Email: {catalog.site.email.address}
- GitHub: https://github.com/whinee

## Core Pages
- [{catalog.site.author_display_name} Home]({base_url}/): Main landing page with cyberdeck sidekick WhiskerFrame and hardware stories.
- [Resume / CV]({base_url}/resume/): Technical skills in Python, FastAPI, Linux, embedded systems, and hackathon wins.
- [Contact]({base_url}/contacts/): Direct public inquiries and collaboration channels.
"""
    if catalog.has_projects:
        llms_txt += f"\n## Projects\n- [Projects Index]({base_url}/projects/): Open-source hardware and software engineering builds.\n"
        for p in catalog.public_projects:
            llms_txt += f"- [{p.title}]({base_url}/projects/{p.slug}/): {p.summary}\n"

    if catalog.has_talks:
        llms_txt += f"\n## Talks\n- [Talks & Presentations]({base_url}/talks/): Technical presentations on weird computing and cyberdecks.\n"
        for t in catalog.public_talks:
            llms_txt += f"- [{t.title}]({base_url}/talks/): {t.description}\n"
    return llms_txt


def generate_llms_full(catalog: Any, base_url: str) -> str:
    """Generate llms-full.txt content as extended companion document."""
    llms_full = f"""# {catalog.site.author_display_name} — Complete Overview

> Extended companion document for AI systems. Contains structured project details, public presentations, and core philosophies.

Site URL: {base_url}
Public Contact: {catalog.site.email.address}
FOSS Motto: REBEL against corporate greed. REVEL in Free and Open Source Software!

---

## Technical Summary
Lyra Phasma is a software developer, cyberdeck builder, and FOSS advocate specializing in Python, FastAPI, Linux environments, and unconventional computing hardware. Notable achievements include winning the CodeKada hackathon with an offline-first cyberdeck build.

---

## Active Projects
"""
    for p in catalog.public_projects:
        tags_str = ", ".join(p.tags) if p.tags else "None"
        repo_str = f"Repository: {p.repo_url}" if p.repo_url else ""
        llms_full += f"""
### {p.title}
- Slug: {p.slug}
- Year: {p.year}
- Tags: {tags_str}
- Summary: {p.summary}
- {repo_str}
"""
        if p.body:
            llms_full += f"\n{p.body}\n"

    llms_full += "\n---\n\n## Presentations & Talks\n"
    for t in catalog.public_talks:
        llms_full += f"""
### {t.title}
- Event: {t.event} ({t.date})
- Description: {t.description}
"""

    llms_full += f"""
---

## Navigation & Contact
- Home: {base_url}/
- Resume: {base_url}/resume/
- Contacts: {base_url}/contacts/
- GitHub: https://github.com/whinee
"""
    return llms_full


def generate_llms_files() -> None:
    """Generate root-published /llms.txt and /llms-full.txt."""
    catalog = load_all_content()
    base_url = catalog.site.url.rstrip("/")

    (DIST_DIR / "llms.txt").write_text(generate_llms_txt(catalog, base_url), encoding="utf-8")
    print("  Generated dist/llms.txt")

    (DIST_DIR / "llms-full.txt").write_text(generate_llms_full(catalog, base_url), encoding="utf-8")
    print("  Generated dist/llms-full.txt")


def _collect_content_routes(catalog: Any) -> list[tuple[str, str]]:
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


def _collect_writing_routes(catalog: Any) -> list[tuple[str, str]]:
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
        DIST_DIR / "llms.txt",
        DIST_DIR / "llms-full.txt",
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
    generate_llms_files()

    if not verify_dist():
        return 1

    total_size = sum(f.stat().st_size for f in DIST_DIR.rglob("*") if f.is_file())
    print(f"\nStatic freeze successful! Total size: {total_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
