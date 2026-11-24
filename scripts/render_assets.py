"""Render the social preview image (assets/og.png) inside _site/.

    python scripts/render_assets.py      # after build.py; needs Playwright with Chromium

The HTML source (og.html) is removed afterwards, so only the image is published.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[1] / "_site"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        og = browser.new_page(viewport={"width": 1200, "height": 630})
        og.goto((SITE / "og.html").as_uri(), wait_until="networkidle")
        og.evaluate("document.fonts.ready")
        if not og.evaluate("[...document.images].every(i => i.complete && i.naturalWidth > 0)"):
            sys.exit("social preview: the profile photo did not load")
        og.screenshot(path=str(SITE / "assets" / "og.png"))
        (SITE / "og.html").unlink()
        browser.close()
    print(f"assets/og.png: {(SITE / 'assets' / 'og.png').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
