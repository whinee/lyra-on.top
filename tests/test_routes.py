"""tests/test_routes.py - Route & template rendering tests."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_index_route_status_and_content():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # Verify key sections are present
    assert '<main id="main-content">' in html
    assert 'class="skip-link"' in html
    assert 'id="slides"' in html
    assert 'id="whiskerframe"' in html
    assert 'id="foss"' in html
    assert 'id="wins"' in html
    assert 'id="hire"' in html

    # Verify factual copy from master-context
    assert "Lyra Phasma" in html
    assert "REBEL against corporate greed" in html
    assert "Hack &amp; Yap Episode II" in html
    assert "Zero-Ten Park" in html


def test_404_route():
    response = client.get("/404.html")
    assert response.status_code == 404
    html = response.text
    assert "404" in html
    assert "lost" in html.lower() or "ran away" in html.lower() or "home" in html.lower()


def test_missing_route_returns_404():
    response = client.get("/nonexistent-page-owo")
    assert response.status_code == 404
