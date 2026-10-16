"""tests/test_freeze.py - Static freeze output verification."""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"


def test_freeze_script_generates_valid_dist():
    # Run freeze script
    result = subprocess.run(
        ["uv", "run", "python", "scripts/freeze.py"],  # noqa: S607
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"Freeze failed: {result.stderr}"

    # Verify critical files exist and have non-zero content
    index_file = DIST_DIR / "index.html"
    not_found_file = DIST_DIR / "404.html"
    qr_file = DIST_DIR / "static" / "assets" / "images" / "slides-qr.svg"
    og_file = DIST_DIR / "static" / "assets" / "images" / "meta" / "og-card.png"
    llms_file = DIST_DIR / "llms.txt"
    llms_full_file = DIST_DIR / "llms-full.txt"

    assert index_file.exists() and index_file.stat().st_size > 0
    assert not_found_file.exists() and not_found_file.stat().st_size > 0
    assert qr_file.exists() and qr_file.stat().st_size > 0
    assert og_file.exists() and og_file.stat().st_size > 0
    assert llms_file.exists() and llms_file.stat().st_size > 0
    assert llms_full_file.exists() and llms_full_file.stat().st_size > 0

    # Verify llms content
    llms_content = llms_file.read_text(encoding="utf-8")
    assert "Lyra Phasma" in llms_content
    assert "lyraphasma@gmail.com" in llms_content
