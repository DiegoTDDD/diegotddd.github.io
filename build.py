"""Build the static site into _site/ from projects.py.

    python build.py            # fails if a project lacks results, code or media files

No dependencies beyond the standard library, so the Pages workflow needs only Python.
"""

from __future__ import annotations

import shutil
import sys
from html import escape
from pathlib import Path

from projects import AI, DATA, GH, GROUPS, PROJECTS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
SITE = "https://diegotddd.github.io"
NAME = "Diego Alves"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap"
)


def e(text: str) -> str:
    return escape(text, quote=True)


def code_url(p: dict) -> str:
    return GH + p.get("repo", p["slug"])


def page(title: str, description: str, path: str, body: str, depth: int) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<link rel="canonical" href="{SITE}/{path}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="wordmark" href="{up}index.html">{NAME}</a>
  <nav aria-label="Site">
    <a href="{up}index.html#ai">Projects</a>
    <a href="{up}index.html#about">About</a>
    <a href="{GH}">GitHub</a>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <p>Every number on this site comes from the project's own repository, where the code that
  produced it runs in CI. <a href="{GH}diegotddd.github.io">Source of this site</a>.</p>
</footer>
<script src="{up}assets/video.js" defer></script>
</body>
</html>
"""


def video(slug: str, caption: str, up: str, hero: bool = False) -> str:
    cls = "media media-hero" if hero else "media"
    return f"""<figure class="{cls}">
  <video controls muted loop playsinline preload="metadata" data-autoplay
         poster="{up}assets/media/{slug}-poster.webp"
         aria-label="{e(caption)}">
    <source src="{up}assets/media/{slug}.mp4" type="video/mp4">
  </video>
  <figcaption>{e(caption)}</figcaption>
</figure>"""


def links(p: dict, up: str, with_case: bool) -> str:
    out = []
    if with_case:
        out.append(f'<a href="{up}projects/{p["slug"]}.html">Case study</a>')
    out.append(f'<a href="{code_url(p)}">Code</a>')
    if p.get("demo"):
        out.append(f'<a href="{e(p["demo"])}">Live demo</a>')
    for label, url in p.get("extra_links", []):
        out.append(f'<a href="{e(url)}">{e(label)}</a>')
    return '<p class="links">' + "".join(out) + "</p>"


def row(p: dict) -> str:
    value, label = p["headline"]
    return f"""<article class="row">
  <p class="measure"><span class="value">{e(value)}</span><span class="label">{e(label)}</span></p>
  <div class="what">
    <h3><a href="projects/{p["slug"]}.html">{e(p["name"])}</a></h3>
    <p>{e(p["line"])}</p>
    <p class="stack">{e(", ".join(p["stack"]))}</p>
    {links(p, "", with_case=True)}
  </div>
</article>"""


def home() -> str:
    hero = next(p for p in PROJECTS if p["slug"] == "fraud-investigation-agents")
    sections = []
    for group, anchor in ((AI, "ai"), (DATA, "data")):
        rows = "\n".join(row(p) for p in PROJECTS if p["group"] == group)
        sections.append(f'<section class="group" id="{anchor}" aria-labelledby="{anchor}-h">\n'
                        f'<h2 id="{anchor}-h">{e(GROUPS[group])}</h2>\n{rows}\n</section>')  # fmt: skip
    body = f"""<section class="hero">
  <div class="intro">
    <h1>Data and AI systems, with the measurements that show whether they work.</h1>
    <p>I'm Diego Alves, a data professional in São Paulo state, Brazil. I build data platforms,
    machine learning systems and LLM agents. Each project here runs its tests and evaluations in CI,
    documents its design decisions, and reports what it measured, including what did not work.</p>
  </div>
  {video(hero["video"], hero["video_caption"], "", hero=True)}
</section>
{chr(10).join(sections)}
<section class="about" id="about" aria-labelledby="about-h">
  <h2 id="about-h">About</h2>
  <div class="about-body">
    <p>I came to engineering from data analysis: SQL, dashboards and the question of whether a
    number can be trusted. That question shapes how I build. Pipelines check their data before it
    reaches anyone, models are measured on data they never saw, and agents are evaluated, traced
    and attacked before they are called finished.</p>
    <p>I'm the author of five published books, technical, business and literary. I speak
    Portuguese (native), English (C2) and Spanish (C1).</p>
    <dl class="edu">
      <dt>Postgraduate, Data Science and Big Data Analytics</dt><dd>Faculdade IMES, 2026</dd>
      <dt>BSc, Information Technology</dt><dd>UNIVESP, expected 2026</dd>
      <dt>AI Technician</dt><dd>IFNMG, expected 2027</dd>
      <dt>Technologist, Business Management</dt><dd>Fatec Catanduva, 2023</dd>
    </dl>
    <p class="links"><a href="{GH}">GitHub profile</a></p>
  </div>
</section>"""
    description = "Data engineering, machine learning and AI engineering projects by Diego Alves, each with measured results."
    return page(f"{NAME}: data and AI engineering", description, "", body, 0)


def project_page(p: dict, i: int) -> str:
    up = "../"
    media = ""
    if p.get("video"):
        media = video(p["video"], p["video_caption"], up)
    elif p.get("image"):
        media = (f'<figure class="media"><img src="{up}assets/media/{p["image"]}.webp" '
                 f'alt="{e(p["image_alt"])}" loading="lazy"></figure>')  # fmt: skip
    value, label = p["headline"]
    results = "\n".join(
        f'<tr><td class="value">{e(v)}</td><td>{e(lbl)}</td></tr>' for v, lbl in p["results"]
    )
    how = "\n".join(f"<li>{e(h)}</li>" for h in p["how"])
    prev_p, next_p = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    limits = f"<h2>Limits</h2>\n<p>{e(p['limits'])}</p>" if p.get("limits") else ""
    body = f"""<article class="case">
  <p class="back"><a href="{up}index.html#{"ai" if p["group"] == AI else "data"}">All projects</a></p>
  <h1>{e(p["name"])}</h1>
  <p class="lede">{e(p["line"])}</p>
  {links(p, up, with_case=False)}
  <p class="measure measure-lg"><span class="value">{e(value)}</span><span class="label">{e(label)}</span></p>
  {media}
  <div class="prose">
    <h2>Problem</h2>
    <p>{e(p["problem"])}</p>
    <h2>Solution</h2>
    <p>{e(p["solution"])}</p>
    <h2>How it works</h2>
    <ul>{how}</ul>
    <h2>Results</h2>
    <table class="results"><caption>Measured results, from the repository</caption>
    <tbody>{results}</tbody></table>
    {limits}
    <h2>Stack</h2>
    <p>{e(", ".join(p["stack"]))}</p>
  </div>
  <nav class="pager" aria-label="Other projects">
    <a href="{prev_p["slug"]}.html"><span>Previous</span>{e(prev_p["name"])}</a>
    <a href="{next_p["slug"]}.html"><span>Next</span>{e(next_p["name"])}</a>
  </nav>
</article>"""
    return page(f"{p['name']}: {NAME}", p["line"], f"projects/{p['slug']}.html", body, 1)


def check() -> list[str]:
    problems = []
    slugs = [p["slug"] for p in PROJECTS]
    if len(set(slugs)) != len(slugs):
        problems.append("duplicate slugs")
    for p in PROJECTS:
        if p["group"] not in (AI, DATA):
            problems.append(f"{p['slug']}: unknown group")
        if not p.get("headline") or not p.get("results"):
            problems.append(f"{p['slug']}: no measured results")
        for key in ("problem", "solution", "line", "how", "stack"):
            if not p.get(key):
                problems.append(f"{p['slug']}: missing {key}")
        for f in [f"{p['video']}.mp4", f"{p['video']}-poster.webp"] if p.get("video") else []:
            if not (ROOT / "assets" / "media" / f).exists():
                problems.append(f"{p['slug']}: missing assets/media/{f}")
        if p.get("image") and not (ROOT / "assets" / "media" / f"{p['image']}.webp").exists():
            problems.append(f"{p['slug']}: missing image {p['image']}")
    return problems


def main() -> None:
    problems = check()
    if problems:
        sys.exit("site content problems:\n" + "\n".join(problems))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "projects").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / "index.html").write_text(home(), encoding="utf-8")
    for i, p in enumerate(PROJECTS):
        (OUT / "projects" / f"{p['slug']}.html").write_text(project_page(p, i), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    urls = [f"{SITE}/"] + [f"{SITE}/projects/{p['slug']}.html" for p in PROJECTS]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    print(f"built {len(PROJECTS) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
