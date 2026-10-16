"""tests/test_interactive_polish.py - Tests for typography, boss-fight, email, and cursor."""

from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_public_email_updated():
    response = client.get("/contacts")
    assert response.status_code == 200
    assert 'data-user="lyraphasma"' in response.text
    assert 'data-domain="gmail.com"' in response.text
    assert "lyraphasma [at] gmail.com" in response.text


def test_boss_fight_markup_and_js_present():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "whisker-boss-arena" in html
    assert "OVERDRIVE MODE" in html


def test_terminal_tagline_font_family():
    repo_root = Path(__file__).resolve().parent.parent
    hero_b_css = (repo_root / "src" / "api" / "static" / "stylesheets" / "hero_b.css").read_text()
    assert "--font-mono" in hero_b_css
    assert "hero-tagline" in hero_b_css
