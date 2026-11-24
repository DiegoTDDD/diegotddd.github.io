"""Build the static site into _site/ from projects.py, projects_pt.py and content.py.

    python build.py            # fails if a project lacks results, a translation or media files

Portuguese is the default language (/), English lives under /en/. The résumé pages
(cv/pt.html, cv/en.html) and the social preview page (og.html) are turned into PDF/PNG by
scripts/render_assets.py in the Pages workflow. Standard library only.
"""

from __future__ import annotations

import json
import shutil
import sys
from html import escape
from pathlib import Path

from content import (
    AVATAR, CATEGORIES, EDUCATION, EXPERIENCE, GITHUB_PROFILE, LANGUAGES, META, PERSON, SKILLS, UI,
)  # fmt: skip
from projects import AI, DATA, GH, PROJECTS
from projects_pt import PT

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
SITE = "https://diegotddd.github.io"
LANGS = ("pt", "en")
PREFIX = {"pt": "", "en": "en/"}
CV_FILE = {"pt": "curriculo-diego-alves.pdf", "en": "resume-diego-alves.pdf"}
FONTS = (
    "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap"
)
THEME_BOOT = (
    "<script>try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')"
    "document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"
)


def e(text: str) -> str:
    return escape(text, quote=True)


def code_url(p: dict) -> str:
    return GH + p.get("repo", p["slug"])


def local(p: dict, lang: str) -> dict:
    """The project's text in one language (English entries are the base)."""
    if lang == "en":
        return p
    return {**p, **PT[p["slug"]]}


def page(lang: str, title: str, description: str, path: str, body: str, depth: int,
         alternate: str, extra_head: str = "") -> str:  # fmt: skip
    u = UI[lang]
    up = "../" * depth
    other = "en" if lang == "pt" else "pt"
    # pt pages live at the root, en pages under en/: the twin page is one level away.
    other_href = up + ("en/" if lang == "pt" else "../") + alternate
    return f"""<!doctype html>
<html lang="{u["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{"pt_BR" if lang == "pt" else "en_US"}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{SITE}/{PREFIX[lang]}{path}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<link rel="canonical" href="{SITE}/{PREFIX[lang]}{path}">
<link rel="alternate" hreflang="pt-BR" href="{SITE}/{alternate}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{alternate}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{alternate}">
<link rel="icon" href="{up}{"../" if lang == "en" else ""}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}{"../" if lang == "en" else ""}assets/style.css">
{THEME_BOOT}
{extra_head}
</head>
<body>
<a class="skip" href="#main">{u["skip"]}</a>
<header class="top">
  <a class="wordmark" href="{up}index.html">{PERSON["name"]}</a>
  <nav aria-label="Site">
    <a href="{up}index.html#projects">{u["nav_projects"]}</a>
    <a href="{up}index.html#experience">{u["nav_experience"]}</a>
    <a href="{up}index.html#skills">{u["nav_skills"]}</a>
    <a href="{up}index.html#contact">{u["nav_contact"]}</a>
    <a class="lang" href="{other_href}" hreflang="{"en" if other == "en" else "pt-BR"}" lang="{"en" if other == "en" else "pt-BR"}" aria-label="{u["other_lang_label"]}">{u["other_lang"]}</a>
    <button class="theme" type="button" aria-label="{u["theme"]}" title="{u["theme"]}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z"/></svg>
    </button>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <p>{u["footer"]} <a href="{GH}diegotddd.github.io">{u["source"]}</a>.</p>
</footer>
<script src="{up}{"../" if lang == "en" else ""}assets/site.js" defer></script>
</body>
</html>
"""


def video(slug: str, caption: str, up: str, hero: bool = False) -> str:
    cls = "media media-hero" if hero else "media"
    return f"""<figure class="{cls}">
  <video controls muted loop playsinline preload="metadata" data-autoplay
         poster="{up}assets/media/{slug}-poster.webp" aria-label="{e(caption)}">
    <source src="{up}assets/media/{slug}.mp4" type="video/mp4">
  </video>
  <figcaption>{e(caption)}</figcaption>
</figure>"""


def links(p: dict, u: dict, case_href: str | None) -> str:
    out = []
    if case_href:
        out.append(f'<a href="{case_href}">{u["case"]}</a>')
    out.append(f'<a href="{code_url(p)}">{u["code"]}</a>')
    if p.get("demo"):
        out.append(f'<a href="{e(p["demo"])}">{u["demo"]}</a>')
    for label, url in p.get("extra_links", []):
        out.append(f'<a href="{e(url)}">{e(label)}</a>')
    return '<p class="links">' + "".join(out) + "</p>"


def row(p: dict, lang: str) -> str:
    u = UI[lang]
    lp = local(p, lang)
    value, label = lp["headline"]
    tags = " ".join(META[p["slug"]][0])
    return f"""<article class="row" data-tags="{tags}">
  <p class="measure"><span class="value">{e(value)}</span><span class="label">{e(label)}</span></p>
  <div class="what">
    <h3><a href="projects/{p["slug"]}.html">{e(lp["name"])}</a></h3>
    <p>{e(lp["line"])}</p>
    <p class="stack">{e(", ".join(p["stack"]))}</p>
    {links(lp, u, f"projects/{p['slug']}.html")}
  </div>
</article>"""


def json_ld(lang: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": PERSON["name"],
        "jobTitle": PERSON["role"][lang],
        "url": f"{SITE}/{PREFIX[lang]}",
        "image": AVATAR,
        "sameAs": [GITHUB_PROFILE],
        "address": {"@type": "PostalAddress", "addressLocality": "Novo Horizonte", "addressRegion": "SP",
                    "addressCountry": "BR"},
        "knowsLanguage": ["pt-BR", "en", "es"],
        "alumniOf": sorted({ed["school"] for ed in EDUCATION}),
    }  # fmt: skip
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def home(lang: str) -> str:
    u = UI[lang]
    hero = local(next(p for p in PROJECTS if p["slug"] == "fraud-investigation-agents"), lang)
    n_ai = sum(p["group"] == AI for p in PROJECTS)
    chips = [f'<button type="button" class="chip" data-filter="all" aria-pressed="true">{u["all"]}</button>']
    used = {t for tags, _ in META.values() for t in tags}
    for key, names in CATEGORIES.items():
        if key in used:
            chips.append(f'<button type="button" class="chip" data-filter="{key}" aria-pressed="false">{names[lang]}</button>')
    groups = []
    for group, anchor, title in ((AI, "ai", u["group_ai"]), (DATA, "data", u["group_data"])):
        rows = "\n".join(row(p, lang) for p in PROJECTS if p["group"] == group)
        groups.append(f'<section class="group" id="{anchor}" aria-labelledby="{anchor}-h">\n'
                      f'<h3 class="group-h" id="{anchor}-h">{title}</h3>\n{rows}\n</section>')  # fmt: skip
    experience = "\n".join(
        f'<li><p class="xp-role">{e(x["role"][lang])}</p><p class="xp-org">{e(x["org"])}, {e(x["place"][lang])}</p>'
        f'<p class="xp-when">{e(x["period"][lang])}</p></li>'
        for x in EXPERIENCE
    )
    education = "\n".join(
        f'<li><p class="xp-role">{e(x["course"][lang])}</p><p class="xp-org">{e(x["school"])}</p>'
        f'<p class="xp-when">{e(x["when"][lang])}</p></li>'
        for x in EDUCATION
    )
    skills = "\n".join(
        f'<div class="skill"><h3>{e(s["group"][lang])}</h3><p>{e(", ".join(s["items"]))}</p></div>' for s in SKILLS
    )
    about = "\n".join(f"<p>{e(par)}</p>" for par in PERSON["about"][lang])
    up_root = "" if lang == "pt" else "../"
    body = f"""<section class="hero">
  <div class="intro">
    <div class="who">
      <img class="avatar" src="{AVATAR}" alt="{PERSON["name"]}" width="88" height="88">
      <p><strong>{PERSON["name"]}</strong><br>{e(PERSON["role"][lang])}<br>{e(PERSON["location"][lang])}</p>
    </div>
    <h1>{e(PERSON["headline"][lang])}</h1>
    <p class="lead">{e(PERSON["intro"][lang])}</p>
    <p class="cta">
      <a class="button" href="#projects">{u["see_projects"]}</a>
      <a class="button button-quiet" href="{up_root}cv/{CV_FILE[lang]}">{u["cv"]}</a>
      <a class="button button-quiet" href="{GITHUB_PROFILE}">{u["github"]}</a>
    </p>
    <dl class="stats">
      <div><dt>{len(PROJECTS)}</dt><dd>{u["stat_projects"]}</dd></div>
      <div><dt>{n_ai}</dt><dd>{u["stat_ai"]}</dd></div>
      <div><dt>{len(PROJECTS)}</dt><dd>{u["stat_ci"]}</dd></div>
      <div><dt>5</dt><dd>{u["stat_books"]}</dd></div>
    </dl>
  </div>
  {video(hero["video"], hero["video_caption"], up_root, hero=True)}
</section>
<section class="projects" id="projects" aria-labelledby="projects-h">
  <h2 id="projects-h">{u["projects"]}</h2>
  <div class="chips" role="group" aria-label="{u["filter_label"]}">{"".join(chips)}</div>
  <p class="empty" hidden>{u["none"]}</p>
  {"".join(groups)}
</section>
<section class="split" aria-label="{u["about"]}">
  <section class="block" id="experience" aria-labelledby="experience-h">
    <h2 id="experience-h">{u["experience"]}</h2>
    <ul class="xp">{experience}</ul>
  </section>
  <section class="block" id="education" aria-labelledby="education-h">
    <h2 id="education-h">{u["education"]}</h2>
    <ul class="xp">{education}</ul>
  </section>
</section>
<section class="block" id="skills" aria-labelledby="skills-h">
  <h2 id="skills-h">{u["skills"]}</h2>
  <div class="skills">{skills}
    <div class="skill"><h3>{u["languages"]}</h3><p>{e(", ".join(LANGUAGES[lang]))}</p></div>
  </div>
</section>
<section class="split">
  <section class="block" id="about" aria-labelledby="about-h">
    <h2 id="about-h">{u["about"]}</h2>
    <div class="prose-sm">{about}</div>
  </section>
  <section class="block" id="contact" aria-labelledby="contact-h">
    <h2 id="contact-h">{u["contact"]}</h2>
    <p class="prose-sm">{u["contact_text"]}</p>
    <p class="cta">
      <a class="button" href="{up_root}cv/{CV_FILE[lang]}">{u["cv"]}</a>
      <a class="button button-quiet" href="{GITHUB_PROFILE}">{u["github"]}</a>
    </p>
  </section>
</section>"""
    title = f"{PERSON['name']}: {u['title_suffix']}"
    return page(lang, title, u["description"], "", body, 0, "", json_ld(lang))


def project_page(p: dict, i: int, lang: str) -> str:
    u = UI[lang]
    lp = local(p, lang)
    up = "../"
    assets = up + ("../" if lang == "en" else "")
    media = ""
    if lp.get("video"):
        media = video(lp["video"], lp["video_caption"], assets)
    elif lp.get("image"):
        media = (f'<figure class="media"><img src="{assets}assets/media/{lp["image"]}.webp" '
                 f'alt="{e(lp["image_alt"])}" loading="lazy"></figure>')  # fmt: skip
    value, label = lp["headline"]
    results = "\n".join(f'<tr><td class="value">{e(v)}</td><td>{e(lbl)}</td></tr>' for v, lbl in lp["results"])
    how = "\n".join(f"<li>{e(h)}</li>" for h in lp["how"])
    prev_p, next_p = local(PROJECTS[i - 1], lang), local(PROJECTS[(i + 1) % len(PROJECTS)], lang)
    limits = f"<h2>{u['limits']}</h2>\n<p>{e(lp['limits'])}</p>" if lp.get("limits") else ""
    repo = p.get("repo", p["slug"])
    ci = META[p["slug"]][1]
    badge = (f'<a class="ci" href="{GH}{repo}/actions/workflows/{ci}">'
             f'<img src="{GH}{repo}/actions/workflows/{ci}/badge.svg" alt="{u["ci"]}" height="20"></a>')  # fmt: skip
    anchor = "ai" if p["group"] == AI else "data"
    body = f"""<article class="case">
  <p class="back"><a href="{up}index.html#{anchor}">{u["back"]}</a></p>
  <h1>{e(lp["name"])}</h1>
  <p class="lede">{e(lp["line"])}</p>
  {links(lp, u, None)}
  {badge}
  <p class="measure measure-lg"><span class="value">{e(value)}</span><span class="label">{e(label)}</span></p>
  {media}
  <div class="prose">
    <h2>{u["problem"]}</h2>
    <p>{e(lp["problem"])}</p>
    <h2>{u["solution"]}</h2>
    <p>{e(lp["solution"])}</p>
    <h2>{u["how"]}</h2>
    <ul>{how}</ul>
    <h2>{u["results"]}</h2>
    <table class="results"><caption>{u["results_caption"]}</caption>
    <tbody>{results}</tbody></table>
    {limits}
    <h2>{u["stack"]}</h2>
    <p>{e(", ".join(p["stack"]))}</p>
  </div>
  <nav class="pager" aria-label="{u["projects"]}">
    <a href="{prev_p["slug"]}.html"><span>{u["prev"]}</span>{e(prev_p["name"])}</a>
    <a href="{next_p["slug"]}.html"><span>{u["next"]}</span>{e(next_p["name"])}</a>
  </nav>
</article>"""
    path = f"projects/{p['slug']}.html"
    return page(lang, f"{lp['name']}: {PERSON['name']}", lp["line"], path, body, 1, path)


def not_found(lang: str) -> str:
    u = UI[lang]
    body = f"""<article class="case">
  <h1>{u["notfound_title"]}</h1>
  <p class="lede">{u["notfound_text"]}</p>
  <p class="links"><a href="{SITE}/{PREFIX[lang]}">{u["notfound_link"]}</a></p>
</article>"""
    # 404 is served at any depth, so it uses absolute asset URLs.
    html = page(lang, f"{u['notfound_title']}: {PERSON['name']}", u["description"], "404.html", body, 0, "")
    for attr in ('href="assets/', 'src="assets/', 'href="index.html', 'href="en/'):
        html = html.replace(attr, attr.replace('"', f'"{SITE}/', 1))
    return html


def cv_page(lang: str) -> str:
    """A print-ready résumé built from the same data; render_assets.py turns it into a PDF."""
    u = UI[lang]
    top = [local(p, lang) for p in PROJECTS if p["slug"] in (
        "fraud-investigation-agents", "sec-mcp-agent", "llm-guardrails-redteam", "finetune-and-serve",
        "llm-evals-observability", "freight-intelligence", "realtime-fraud-detection-ml", "supply-chain-risk-intelligence",
    )]  # fmt: skip
    projects = "\n".join(
        f'<li><strong>{e(p["name"])}</strong>: {e(p["line"])} <em>{e(p["headline"][0])} {e(p["headline"][1])}.</em> '
        f'<span class="url">{code_url(p).replace("https://", "")}</span></li>'
        for p in top
    )
    xp = "\n".join(f'<li><strong>{e(x["role"][lang])}</strong>, {e(x["org"])} ({e(x["place"][lang])}), '
                   f'{e(x["period"][lang])}</li>' for x in EXPERIENCE)  # fmt: skip
    ed = "\n".join(f'<li><strong>{e(x["course"][lang])}</strong>, {e(x["school"])}, {e(x["when"][lang])}</li>'
                   for x in EDUCATION)  # fmt: skip
    sk = "\n".join(f'<li><strong>{e(s["group"][lang])}:</strong> {e(", ".join(s["items"]))}</li>' for s in SKILLS)
    heads = {
        "pt": ("Resumo", "Projetos selecionados", "Experiência", "Formação", "Habilidades", "Idiomas", "Publicações"),
        "en": ("Summary", "Selected projects", "Experience", "Education", "Skills", "Languages", "Publications"),
    }[lang]
    return f"""<!doctype html>
<html lang="{u["lang"]}"><head><meta charset="utf-8"><title>{PERSON["name"]}</title>
<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="../assets/cv.css"></head>
<body><main>
<header><h1>{PERSON["name"]}</h1><p class="role">{e(PERSON["role"][lang])}</p>
<p class="contact">{e(PERSON["location"][lang])} | diegotddd.github.io{"" if lang == "pt" else "/en"} | github.com/DiegoTDDD</p></header>
<h2>{heads[0]}</h2><p>{e(PERSON["cv_summary"][lang].format(n=len(PROJECTS)))}</p>
<h2>{heads[1]}</h2><ul>{projects}</ul>
<h2>{heads[2]}</h2><ul>{xp}</ul>
<h2>{heads[3]}</h2><ul>{ed}</ul>
<h2>{heads[4]}</h2><ul>{sk}</ul>
<h2>{heads[5]}</h2><p>{e(", ".join(LANGUAGES[lang]))}</p>
<h2>{heads[6]}</h2><p>{u["books"]}</p>
</main></body></html>
"""


def og_page() -> str:
    """1200x630 social preview, rendered to assets/og.png."""
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="assets/og.css"></head>
<body><div class="og"><img src="{AVATAR}" alt=""><div>
<p class="name">{PERSON["name"]}</p>
<p class="role">{e(PERSON["role"]["pt"])} | {e(PERSON["role"]["en"])}</p>
<p class="head">{e(PERSON["headline"]["pt"])}</p>
<p class="nums"><span>{len(PROJECTS)}</span> projetos, todos com CI <span>0,82</span> F1 do modelo ajustado <span>23/23</span> ataques bloqueados</p>
<p class="url">diegotddd.github.io</p></div></div></body></html>
"""


def check() -> list[str]:
    problems = []
    slugs = [p["slug"] for p in PROJECTS]
    if len(set(slugs)) != len(slugs):
        problems.append("duplicate slugs")
    for p in PROJECTS:
        s = p["slug"]
        if p["group"] not in (AI, DATA):
            problems.append(f"{s}: unknown group")
        if not p.get("headline") or not p.get("results"):
            problems.append(f"{s}: no measured results")
        for key in ("problem", "solution", "line", "how", "stack"):
            if not p.get(key):
                problems.append(f"{s}: missing {key}")
        if s not in META:
            problems.append(f"{s}: no categories / CI workflow in content.META")
        if s not in PT:
            problems.append(f"{s}: no Portuguese text")
        else:
            pt = PT[s]
            for key in ("name", "line", "headline", "problem", "solution", "how", "results"):
                if key not in pt:
                    problems.append(f"{s}: Portuguese text missing {key}")
            if len(pt.get("results", [])) != len(p["results"]) or len(pt.get("how", [])) != len(p["how"]):
                problems.append(f"{s}: Portuguese results/how differ in length from English")
            if p.get("video") and "video_caption" not in pt:
                problems.append(f"{s}: Portuguese video caption missing")
            if p.get("image") and "image_alt" not in pt:
                problems.append(f"{s}: Portuguese image alt missing")
            if p.get("extra_links") and len(pt.get("extra_links", [])) != len(p["extra_links"]):
                problems.append(f"{s}: Portuguese extra links missing")
        for f in [f"{p['video']}.mp4", f"{p['video']}-poster.webp"] if p.get("video") else []:
            if not (ROOT / "assets" / "media" / f).exists():
                problems.append(f"{s}: missing assets/media/{f}")
        if p.get("image") and not (ROOT / "assets" / "media" / f"{p['image']}.webp").exists():
            problems.append(f"{s}: missing image {p['image']}")
    for key in UI["pt"]:
        if key not in UI["en"]:
            problems.append(f"UI key {key} missing in English")
    return problems


def main() -> None:
    problems = check()
    if problems:
        sys.exit("site content problems:\n" + "\n".join(problems))
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for lang in LANGS:
        base = OUT / PREFIX[lang]
        (base / "projects").mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(home(lang), encoding="utf-8")
        for i, p in enumerate(PROJECTS):
            (base / "projects" / f"{p['slug']}.html").write_text(project_page(p, i, lang), encoding="utf-8")
    (OUT / "404.html").write_text(not_found("pt"), encoding="utf-8")
    (OUT / "cv").mkdir()
    for lang in LANGS:
        (OUT / "cv" / f"{lang}.html").write_text(cv_page(lang), encoding="utf-8")
    (OUT / "og.html").write_text(og_page(), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    urls = []
    for lang in LANGS:
        urls += [f"{SITE}/{PREFIX[lang]}"] + [f"{SITE}/{PREFIX[lang]}projects/{p['slug']}.html" for p in PROJECTS]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {2 * (len(PROJECTS) + 1)} pages in two languages into {OUT}")


if __name__ == "__main__":
    main()
