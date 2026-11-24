"""Fail if any page in _site/ links to a local file or anchor that does not exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "_site"


def main() -> None:
    bad = []
    pages = sorted(SITE.rglob("*.html"))
    for page in pages:
        html = page.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src|poster)="([^"]+)"', html):
            if ref.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = ref.partition("#")
            target = (page.parent / path).resolve() if path else page
            if not target.exists():
                bad.append(f"{page.relative_to(SITE)}: {ref}")
            elif anchor and f'id="{anchor}"' not in target.read_text(encoding="utf-8"):
                bad.append(f"{page.relative_to(SITE)}: missing anchor {ref}")
    if bad:
        sys.exit("broken links:\n" + "\n".join(bad))
    print(f"links ok on {len(pages)} pages")


if __name__ == "__main__":
    main()
