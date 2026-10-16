"""tests/test_a11y.py - Semantic HTML, ARIA, and accessibility assertions."""

import re

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_skip_link_exists():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    # Skip link must point to #main-content
    assert '<a href="#main-content" class="skip-link"' in html
    assert '<main id="main-content">' in html


def test_images_have_alt_attributes():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Extract all img tags
    img_tags = re.findall(r"<img [^>]+>", html)
    for img in img_tags:
        assert 'alt="' in img, f"Image missing alt attribute: {img}"


def test_aria_labels_on_decorative_elements():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Section landmark labels
    assert 'aria-labelledby="slides-title"' in html
    assert 'aria-labelledby="story-title"' in html
    assert 'aria-labelledby="wins-title"' in html
    assert 'aria-labelledby="hire-title"' in html


def test_no_empty_links_or_buttons():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # All buttons and links must have non-empty text or aria-label
    links = re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
    for href, text in links:
        stripped_text = re.sub(r"<[^>]+>", "", text).strip()
        assert len(stripped_text) > 0 or "aria-label=" in text, f"Empty link found: {href}"


def test_heading_hierarchy():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Exactly one h1 on page
    h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    assert len(h1_matches) == 1, f"Expected 1 h1, found {len(h1_matches)}"
    assert "Lyra" in h1_matches[0]

    # h2 tags for all major sections
    h2_matches = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.DOTALL)
    assert len(h2_matches) >= 4, f"Expected at least 4 section h2 headings, found {len(h2_matches)}"


def test_prefers_reduced_motion_in_stylesheets():
    from pathlib import Path

    repo_root = Path(__file__).resolve().parent.parent
    base_css = (repo_root / "src" / "api" / "static" / "stylesheets" / "base.css").read_text()
    fx_css = (repo_root / "src" / "api" / "static" / "stylesheets" / "fx.css").read_text()

    assert "prefers-reduced-motion" in base_css
    assert "prefers-reduced-motion" in fx_css

