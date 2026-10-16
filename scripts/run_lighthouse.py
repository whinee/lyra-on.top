#!/usr/bin/env python3
"""
scripts/run_lighthouse.py - Run Lighthouse audits on frozen static site build.

Spawns a local HTTP server, runs Lighthouse via npx on key routes, and saves reports.
"""

import http.server
import json
import pathlib
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from typing import Any

PORT = 8940
DIST_DIR = pathlib.Path("dist").resolve()
REPORTS_DIR = pathlib.Path("reports/lighthouse").resolve()

ROUTES = [
    ("homepage", f"http://localhost:{PORT}/"),
    ("projects", f"http://localhost:{PORT}/projects/"),
    ("resume", f"http://localhost:{PORT}/resume/"),
    ("contacts", f"http://localhost:{PORT}/contacts/"),
    ("talks", f"http://localhost:{PORT}/talks/"),
]

DEVICES: list[tuple[str, list[str]]] = [
    ("mobile", ["--form-factor=mobile", "--screen-emulation.mobile=true"]),
    ("desktop", ["--preset=desktop"]),
]


class SingleFileHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving the frozen dist directory."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        pass


def run_server(server: http.server.HTTPServer) -> None:
    """Run the HTTP server until shutdown."""
    server.serve_forever()


def wait_for_server(port: int) -> bool:
    """Poll until the local HTTP server responds with HTTP 200."""
    url = f"http://localhost:{port}/"
    for _ in range(50):
        try:
            req = urllib.request.Request(url)  # noqa: S310
            with urllib.request.urlopen(req) as resp:  # noqa: S310
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, ConnectionRefusedError, OSError):
            time.sleep(0.2)
    return False


def parse_scores(json_path: str) -> dict[str, int] | None:
    """Extract category scores from a Lighthouse report JSON file."""
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
            cats = data.get("categories", {})
            return {
                cat: int((cats[cat].get("score") or 0) * 100)
                for cat in ["performance", "accessibility", "best-practices", "seo"]
                if cat in cats
            }
    except (json.JSONDecodeError, OSError) as e:
        print(f"    Could not parse report json: {e}")
        return None


def audit_single_route(
    name: str,
    url: str,
    dev_name: str,
    dev_flags: list[str],
) -> tuple[bool, dict[str, int] | None]:
    """Run Lighthouse for a specific route and device configuration."""
    report_base = str(REPORTS_DIR / f"{name}-{dev_name}")
    json_path = f"{report_base}.report.json"

    cmd = [
        "npx",
        "lighthouse",
        url,
        "--output",
        "json",
        "--output",
        "html",
        "--output-path",
        report_base,
        "--chrome-flags=--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage",
        *dev_flags,
        "--quiet",
    ]

    print(f"  Auditing {name} ({dev_name})...")
    res = subprocess.run(cmd, check=False)  # noqa: S603
    if res.returncode != 0:
        print(f"    Warning: Lighthouse audit for {name} ({dev_name}) exited with {res.returncode}")
        return False, None

    scores = parse_scores(json_path)
    if scores:
        print(
            f"    Scores -> Perf: {scores.get('performance')}, "
            f"A11y: {scores.get('accessibility')}, "
            f"BP: {scores.get('best-practices')}, "
            f"SEO: {scores.get('seo')}",
        )
        return True, scores
    return False, None


def execute_audits() -> tuple[bool, dict[str, dict[str, dict[str, int]]]]:
    """Iterate over all configured routes and device targets."""
    all_success = True
    summary: dict[str, dict[str, dict[str, int]]] = {}

    for name, url in ROUTES:
        summary[name] = {}
        for dev_name, dev_flags in DEVICES:
            ok, scores = audit_single_route(name, url, dev_name, dev_flags)
            if not ok or not scores:
                all_success = False
            else:
                summary[name][dev_name] = scores

    return all_success, summary


def main() -> int:
    """Run full Lighthouse suite across key routes and devices."""
    if not DIST_DIR.exists():
        print("Error: dist/ directory not found. Run 'just freeze' first.")
        return 1

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    server = http.server.HTTPServer(("127.0.0.1", PORT), SingleFileHandler)
    server_thread = threading.Thread(target=run_server, args=(server,), daemon=True)
    server_thread.start()

    if not wait_for_server(PORT):
        print("Error: Local static server failed to start.")
        return 1

    print(f"Running Lighthouse audits against local server on port {PORT}...")
    all_success, summary = execute_audits()
    server.shutdown()

    summary_path = REPORTS_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nLighthouse audits completed. Reports saved in {REPORTS_DIR}/")
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
