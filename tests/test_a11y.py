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
