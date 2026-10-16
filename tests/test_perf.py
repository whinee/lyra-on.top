"""
tests/test_perf.py - Performance, payload, and layout shift budget verification.

Ensures initial page load stays under 300 KB budget, CLS <= 0.05, and zero console errors.
"""

import http.server
import re
import threading
from pathlib import Path
from typing import Any

from playwright.sync_api import Page

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"


def test_initial_payload_budget():
    """Verify core HTML and linked stylesheets meet the < 300 KB budget requirement."""
    index_file = DIST_DIR / "index.html"
    assert index_file.exists(), "dist/index.html must exist (run freeze first)"
    html_size_kb = index_file.stat().st_size / 1024
    assert html_size_kb < 100, f"HTML size {html_size_kb:.1f} KB exceeds 100 KB limit"

    # Sum only the stylesheets actually requested by index.html for initial load
    index_content = index_file.read_text(encoding="utf-8")
    linked_css_files = set(re.findall(r'href="/static/stylesheets/([^"]+)"', index_content))
    css_dir = DIST_DIR / "static" / "stylesheets"

    total_linked_css_kb = (
        sum((css_dir / name).stat().st_size for name in linked_css_files if (css_dir / name).exists()) / 1024
    )
    assert total_linked_css_kb < 150, f"Linked CSS size {total_linked_css_kb:.1f} KB exceeds 150 KB limit"

    initial_payload_kb = html_size_kb + total_linked_css_kb
    assert initial_payload_kb < 300, f"Initial payload {initial_payload_kb:.1f} KB exceeds 300 KB budget"


def test_performance_budget(page: Page):
    """
    Performance and motion budget verification using Playwright against static build.

    Measures Cumulative Layout Shift (CLS <= 0.05) and monitors runtime console errors.
    """
    class DistHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(DIST_DIR), **kwargs)

        def log_message(self, *args: Any) -> None:
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), DistHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page.goto(f"http://127.0.0.1:{port}/")
        page.wait_for_load_state("networkidle")

        # Evaluate Cumulative Layout Shift
        cls_score = page.evaluate("""
            new Promise(resolve => {
                let cls = 0;
                try {
                    const observer = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (!entry.hadRecentInput) {
                                cls += entry.value;
                            }
                        }
                    });
                    observer.observe({ type: "layout-shift", buffered: true });
                } catch(e) {}
                setTimeout(() => resolve(cls), 200);
            })
        """)

        assert cls_score <= 0.05, f"CLS score {cls_score} exceeds 0.05 threshold"
        assert not console_errors, f"Console errors encountered: {console_errors}"
    finally:
        server.shutdown()
