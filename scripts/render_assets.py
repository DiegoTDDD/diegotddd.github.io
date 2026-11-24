"""Render the résumé pages to PDF and the social preview to PNG, inside _site/.

    python scripts/render_assets.py      # after build.py; needs Playwright with Chromium

The HTML sources (cv/pt.html, cv/en.html, og.html) are removed afterwards, so only the
finished files are published.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[1] / "_site"
PDF = {"pt": "curriculo-diego-alves.pdf", "en": "resume-diego-alves.pdf"}


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for lang, name in PDF.items():
            src = SITE / "cv" / f"{lang}.html"
            page.goto(src.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.pdf(path=str(SITE / "cv" / name), format="A4", print_background=True, prefer_css_page_size=True)
            src.unlink()
        og = browser.new_page(viewport={"width": 1200, "height": 630})
        og.goto((SITE / "og.html").as_uri(), wait_until="networkidle")
        og.evaluate("document.fonts.ready")
        if not og.evaluate("[...document.images].every(i => i.complete && i.naturalWidth > 0)"):
            sys.exit("social preview: the profile photo did not load")
        og.screenshot(path=str(SITE / "assets" / "og.png"))
        (SITE / "og.html").unlink()
        browser.close()
    for name in PDF.values():
        size = (SITE / "cv" / name).stat().st_size
        if size < 20_000:
            sys.exit(f"{name} is suspiciously small ({size} bytes)")
        print(f"cv/{name}: {size // 1024} KB")
    print(f"assets/og.png: {(SITE / 'assets' / 'og.png').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
