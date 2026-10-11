#!/usr/bin/env python3
"""scripts/screenshot_heroes.py - Capture 360px and 1280px screenshots of Hero A, B, C."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from jinja2 import Environment, FileSystemLoader  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

from src.api.config.content import get_slot, load_content  # noqa: E402

TEMPLATES_DIR = REPO_ROOT / "src" / "api" / "templates"
REPORTS_DIR = REPO_ROOT / "reports" / "screenshots"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def render_hero_html(variant: str) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    content = load_content()
    env.globals.update(content=content, get_slot=lambda s: get_slot(content, s))

    # Render with selected hero variant
    hero_include = f'{{% include "sections/hero_{variant}.html" %}}'
    custom_template = env.from_string(
        f"""
        {{% extends "base.html" %}}
        {{% block styles %}}
            <link rel="stylesheet" href="/static/stylesheets/hero_{variant}.css">
            <link rel="stylesheet" href="/static/stylesheets/whisker.css">
            <link rel="stylesheet" href="/static/stylesheets/fx.css">
        {{% endblock %}}
        {{% block content %}}
            {hero_include}
        {{% endblock %}}
        """,
    )
    return custom_template.render(content=content, get_slot=lambda s: get_slot(content, s))


def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for variant in ["a", "b", "c"]:
            html_content = render_hero_html(variant)
            tmp_html = REPO_ROOT / f"tmp_hero_{variant}.html"

            # Local static server path replacement for file:// loading
            static_abs = (REPO_ROOT / "src" / "api" / "static").as_uri()
            fixed_html = html_content.replace('href="/static/', f'href="{static_abs}/')
            fixed_html = fixed_html.replace('src="/static/', f'src="{static_abs}/')
            tmp_html.write_text(fixed_html, encoding="utf-8")

            # Capture 360px (mobile)
            context_360 = browser.new_context(viewport={"width": 360, "height": 780})
            page_360 = context_360.new_page()
            page_360.goto(tmp_html.as_uri())
            page_360.wait_for_timeout(500)
            dest_360 = REPORTS_DIR / f"hero_{variant}_360.png"
            page_360.screenshot(path=str(dest_360), full_page=True)
            print(f"Captured {dest_360}")
            context_360.close()

            # Capture 1280px (desktop)
            context_1280 = browser.new_context(viewport={"width": 1280, "height": 800})
            page_1280 = context_1280.new_page()
            page_1280.goto(tmp_html.as_uri())
            page_1280.wait_for_timeout(500)
            dest_1280 = REPORTS_DIR / f"hero_{variant}_1280.png"
            page_1280.screenshot(path=str(dest_1280), full_page=True)
            print(f"Captured {dest_1280}")
            context_1280.close()

            tmp_html.unlink(missing_ok=True)

        browser.close()


if __name__ == "__main__":
    capture_screenshots()
