"""Build the static site into _site/ from projects.py, projects_pt.py and content.py.

    python build.py            # fails if a project lacks results, a translation or media files

Portuguese is the default language (/), English lives under /en/. The social preview
page (og.html) is turned into a PNG by scripts/render_assets.py in the Pages workflow. Standard library only.
"""

from __future__ import annotations

import json
import shutil
import sys
from html import escape
from pathlib import Path

from content import (
    AVATAR, CATEGORIES, EDUCATION, EMAIL, FEATURED, GITHUB_PROFILE, LANGUAGES, META, PERSON, PHONE, SKILLS, UI,
    WHATSAPP,
)  # fmt: skip
from books import BOOKS, CANONE, CANONE_END, DECISION, METHOD, TITLE_EN, TOOLS, UI_BOOKS
from business import BUSINESS, LABELS
from projects import AI, DATA, GH, PROJECTS, TEAM
from projects_pt import PT

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
SITE = "https://diegoalves.vercel.app"
LANGS = ("pt", "en")
PREFIX = {"pt": "", "en": "en/"}
FONTS = (
    "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap"
)
THEME_BOOT = (
    "<script>document.documentElement.classList.add('js');try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')"
    "document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>"
)


def lang_boot(lang: str, english_href: str) -> str:
    """One link for everyone: the Portuguese pages send visitors whose browser is not in
    Portuguese to the English twin, unless they already chose a language with the switch.
    Crawlers are never redirected, so both versions stay indexed."""
    if lang != "pt":
        return ""
    return (
        "<script>try{var c=localStorage.getItem('lang');"
        "if(c!=='pt'&&(c==='en'||!/^pt/i.test(navigator.language||'pt'))"
        "&&!/bot|crawl|spider|slurp|preview|facebookexternalhit|whatsapp/i.test(navigator.userAgent))"
        f"location.replace('{english_href}'+location.hash)}}catch(e){{}}</script>"
    )


def e(text: str) -> str:
    return escape(text, quote=True)


def code_url(p: dict) -> str | None:
    """None for team projects whose code is not public."""
    repo = p.get("repo", p["slug"])
    return GH + repo if repo else None


ANCHOR = {AI: "ai", DATA: "data", TEAM: "team"}
WITH_CI = [p for p in PROJECTS if META[p["slug"]][1]]


def contact_buttons(u: dict, primary: bool = False) -> str:
    """Email and WhatsApp (filled in the contact section, quiet next to "See projects"), then GitHub."""
    cls = "button" if primary else "button button-quiet"
    return (f'<a class="{cls}" href="mailto:{EMAIL}">{u["email"]}</a>'
            f'<a class="{cls}" href="{WHATSAPP}" rel="noopener">{u["whatsapp"]}</a>'
            f'<a class="button button-quiet" href="{GITHUB_PROFILE}">{u["github"]}</a>')  # fmt: skip


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
{lang_boot(lang, up + "en/" + alternate)}
{extra_head}
</head>
<body>
<a class="skip" href="#main">{u["skip"]}</a>
<header class="top">
  <a class="wordmark" href="{up}index.html">{PERSON["name"]}</a>
  <nav aria-label="Site">
    <a href="{up}index.html#projects">{u["nav_projects"]}</a>
    <a href="{up}books.html">{UI_BOOKS[lang]["nav"]}</a>
    <a href="{up}index.html#skills">{u["nav_skills"]}</a>
    <a href="{up}index.html#contact">{u["nav_contact"]}</a>
    <a class="lang" data-lang="{other}" href="{other_href}" hreflang="{"en" if other == "en" else "pt-BR"}" lang="{"en" if other == "en" else "pt-BR"}" aria-label="{u["other_lang_label"]}">{u["other_lang"]}</a>
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


def media_name(slug: str, lang: str) -> str:
    """A video may have one version per language (<slug>-pt.mp4, <slug>-en.mp4)."""
    return f"{slug}-{lang}" if (ROOT / "assets" / "media" / f"{slug}-{lang}.mp4").exists() else slug


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
    url = code_url(p)
    out.append(f'<a href="{url}">{u["code"]}</a>' if url else f'<span class="no-code">{u["no_code"]}</span>')
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
        "email": f"mailto:{EMAIL}",
        "address": {"@type": "PostalAddress", "addressLocality": "Novo Horizonte", "addressRegion": "SP",
                    "addressCountry": "BR"},
        "knowsLanguage": ["pt-BR", "en", "es"],
        "alumniOf": sorted({ed["school"] for ed in EDUCATION}),
    }  # fmt: skip
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def home(lang: str) -> str:
    u = UI[lang]
    n_team = sum(p["group"] == TEAM for p in PROJECTS)
    by_slug = {p["slug"]: p for p in PROJECTS}
    featured = []
    for slug in FEATURED:
        fp = local(by_slug[slug], lang)
        value, _ = fp["headline"]
        featured.append(f'<li><a class="feat" href="projects/{slug}.html"><span class="value">{e(value)}</span>'
                        f'<span class="feat-name">{e(fp["name"])}</span>'
                        f'<span class="feat-proof">{e(u["featured_proof"][slug])}</span></a></li>')  # fmt: skip
    chips = [f'<button type="button" class="chip" data-filter="all" aria-pressed="true">{u["all"]}</button>']
    used = {t for tags, _ in META.values() for t in tags}
    for key, names in CATEGORIES.items():
        if key in used:
            chips.append(f'<button type="button" class="chip" data-filter="{key}" aria-pressed="false">{names[lang]}</button>')
    groups = []
    for group, anchor, title in ((DATA, "data", u["group_data"]), (TEAM, "team", u["group_team"]),
                                 (AI, "ai", u["group_ai"])):  # fmt: skip
        rows = "\n".join(row(p, lang) for p in PROJECTS if p["group"] == group)
        groups.append(f'<section class="group" id="{anchor}" aria-labelledby="{anchor}-h">\n'
                      f'<h3 class="group-h" id="{anchor}-h">{title}</h3>\n{rows}\n</section>')  # fmt: skip
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
      <span class="avatar" aria-hidden="true">DA<img src="{AVATAR}" alt="" width="88" height="88" onerror="this.remove()"></span>
      <p><strong>{PERSON["name"]}</strong><br>{e(PERSON["role"][lang])}<br>{e(PERSON["location"][lang])}</p>
    </div>
    <h1>{e(PERSON["headline"][lang])}</h1>
    <p class="lead">{e(PERSON["intro"][lang])}</p>
    <p class="cta">
      <a class="button" href="#projects">{u["see_projects"]}</a>
      {contact_buttons(u)}
    </p>
    <dl class="stats">
      <div><dt>{len(PROJECTS)}</dt><dd>{u["stat_projects"]}</dd></div>
      <div><dt>{n_team}</dt><dd>{u["stat_team"]}</dd></div>
      <div><dt>{len(WITH_CI)}</dt><dd>{u["stat_ci"]}</dd></div>
      <div><dt>5</dt><dd>{u["stat_books"]}</dd></div>
    </dl>
  </div>
  <section class="featured" aria-labelledby="featured-h">
    <h2 id="featured-h">{u["featured"]}</h2>
    <ol class="feats">{"".join(featured)}</ol>
  </section>
</section>
<section class="projects" id="projects" aria-labelledby="projects-h">
  <h2 id="projects-h">{u["projects"]}</h2>
  <div class="chips" role="group" aria-label="{u["filter_label"]}">{"".join(chips)}</div>
  <p class="empty" hidden>{u["none"]}</p>
  {"".join(groups)}
</section>
<section class="block" id="books" aria-labelledby="books-h">
  <h2 id="books-h">{UI_BOOKS[lang]["title"]}</h2>
  <p class="prose-sm">{UI_BOOKS[lang]["lead"]}</p>
  {shelf(lang, up_root, "books.html")}
  <p class="links"><a href="books.html">{UI_BOOKS[lang]["open"]}</a></p>
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
  <section class="block" id="education" aria-labelledby="education-h">
    <h2 id="education-h">{u["education"]}</h2>
    <ul class="xp">{education}</ul>
  </section>
</section>
<section class="block" id="contact" aria-labelledby="contact-h">
    <h2 id="contact-h">{u["contact"]}</h2>
    <p class="prose-sm">{u["contact_text"]}</p>
    <p class="cta">{contact_buttons(u, primary=True)}</p>
    <p class="contact-lines"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{WHATSAPP}" rel="noopener">{PHONE[lang]}</a></p>
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
        media = video(media_name(lp["video"], lang), lp["video_caption"], assets)
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
             f'<img src="{GH}{repo}/actions/workflows/{ci}/badge.svg" alt="{u["ci"]}" height="20"></a>') if ci else ""  # fmt: skip
    anchor = ANCHOR[p["group"]]
    lab = LABELS[lang]
    view = (f'<div class="view" role="group" aria-label="{lab["view"]}">'
            f'<button type="button" data-view="tech" aria-pressed="true">{lab["tech"]}</button>'
            f'<button type="button" data-view="manager" aria-pressed="false">{lab["manager"]}</button></div>')  # fmt: skip
    body = f"""<article class="case" data-view="tech">
  <p class="back"><a href="{up}index.html#{anchor}">{u["back"]}</a></p>
  <h1>{e(lp["name"])}</h1>
  <p class="lede">{e(lp["line"])}</p>
  {links(lp, u, None)}
  {badge}
  {view}
  <p class="measure measure-lg"><span class="value">{e(value)}</span><span class="label">{e(label)}</span></p>
  {media}
  {business_panel(p["slug"], lang)}
  <div class="prose">
    <h2>{u["problem"]}</h2>
    <p>{e(lp["problem"])}</p>
    <h2>{u["solution"]}</h2>
    <p>{e(lp["solution"])}</p>
    <h2>{u["how"]}</h2>
    <ul>{how}</ul>
    <h2>{u["results"]}</h2>
    <table class="results"><caption>{u["results_caption_team" if p["group"] == TEAM else "results_caption"]}</caption>
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


def num(n: float, lang: str, digits: int = 0) -> str:
    """1,042 in English, 1.042 in Portuguese."""
    text = f"{n:,.{digits}f}"
    return text.translate(str.maketrans(",.", ".,")) if lang == "pt" else text


def book_title(b: dict, lang: str) -> str:
    """Portuguese books get their English translation on the English pages, so the language stays clear."""
    if lang == "en" and b["slug"] in TITLE_EN:
        return f'{e(b["title"])} <span class="tr">({e(TITLE_EN[b["slug"]])})</span>'
    return e(b["title"])


def cover(b: dict, lang: str, assets: str, href: str, size: str = "") -> str:
    ub = UI_BOOKS[lang]
    return (f'<a class="cover {size}" href="{href}">'
            f'<img src="{assets}assets/media/books/{b["slug"]}.webp" width="440" height="660" loading="lazy" '
            f'alt="{e(b["title"])}">'
            f'<span class="flag" lang="{b["lang"]}" title="{ub["written_in"][b["lang"]]}">{b["lang"].upper()}</span></a>')  # fmt: skip


def shelf(lang: str, assets: str, link: str, size: str = "") -> str:
    """Two shelves, one per language the books are written in."""
    ub = UI_BOOKS[lang]
    out = []
    for book_lang, label in (("en", ub["shelf_en"]), ("pt", ub["shelf_pt"])):
        items = []
        for b in BOOKS:
            if b["lang"] != book_lang:
                continue
            items.append(f'<li>{cover(b, lang, assets, f"{link}#{b["slug"]}", size)}'
                         f'<p class="book-name">{book_title(b, lang)}</p>'
                         f'<p class="book-meta">{num(b["pages"], lang)} {ub["pages"]}</p></li>')  # fmt: skip
        note = f'<span class="shelf-note">{ub["trilogy"]}</span>' if book_lang == "en" else ""
        out.append(f'<div class="shelf shelf-{book_lang}"><p class="shelf-h"><span class="lang-tag" lang="{book_lang}">'
                   f'{book_lang.upper()}</span>{label}{note}</p><ul>{"".join(items)}</ul></div>')  # fmt: skip
    return f'<div class="shelves">{"".join(out)}</div>'


def book_entry(b: dict, lang: str, assets: str, extra: str = "") -> str:
    ub = UI_BOOKS[lang]
    series = f'<p class="book-series">{ub["book_n"]} {b["series"]} {ub["of_trilogy"]}</p>' if b.get("series") else ""
    chapters = ""
    if b["chapters"]:
        items = "".join(f"<li>{e(c)}</li>" for c in b["chapters"])
        chapters = (f'<details class="toc"><summary>{ub["chapters"]} ({len(b["chapters"])})</summary>'
                    f'<ol lang="{b["lang"]}">{items}</ol></details>')  # fmt: skip
    return f"""<article class="book" id="{b["slug"]}">
  <div class="book-cover">{cover(b, lang, assets, f"#{b['slug']}", "cover-lg")}</div>
  <div class="book-body">
    <p class="book-tags"><span class="lang-tag" lang="{b["lang"]}">{b["lang"].upper()}</span>{ub["written_in"][b["lang"]]}</p>
    <h2>{book_title(b, lang)}</h2>
    <p class="book-sub" lang="{b["lang"]}">{e(b["subtitle"])}</p>
    {series}
    <p>{e(b["thesis"][lang])}</p>
    <blockquote lang="{b["lang"]}"><p>{e(b["quote"])}</p></blockquote>
    <p class="book-meta">{num(b["pages"], lang)} {ub["pages"]}</p>
    {chapters}
  </div>
</article>{extra}"""


def decision_block(lang: str) -> str:
    d, ub = DECISION[lang], UI_BOOKS[lang]
    tabs, panels = [], []
    for i, t in enumerate(TOOLS):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button type="button" role="tab" id="tab-{t["key"]}" aria-controls="panel-{t["key"]}" '
                    f'aria-selected="{sel}"{"" if i == 0 else " tabindex=\"-1\""}>{t["name"]}</button>')  # fmt: skip
        panels.append(f"""<div class="tool" role="tabpanel" id="panel-{t["key"]}" aria-labelledby="tab-{t["key"]}"{"" if i == 0 else " data-off"}>
  <p class="tool-src"><a href="#{t["key"]}">{e(t["book"])}</a>, {t["where"][lang]}</p>
  <pre lang="en"><code>{e(t["code"])}</code></pre>
  <p class="tool-out">{e(t["result"][lang])}</p>
</div>""")
    steps = "".join(
        f'<li><p class="step-h">{e(m[lang])}</p><p>{e(m["how"][lang])}</p>'
        f'<p class="step-link"><a href="projects/{m["slug"]}.html">{e(local(next(p for p in PROJECTS if p["slug"] == m["slug"]), lang)["name"])}</a></p></li>'
        for m in METHOD
    )  # fmt: skip
    return f"""<section class="decision" aria-labelledby="decision-h">
  <h2 id="decision-h">{d["title"]}</h2>
  <p class="decision-intro">{e(d["intro"])}</p>
  <div class="tabs" role="tablist" aria-label="{ub["tabs"]}">{"".join(tabs)}</div>
  {"".join(panels)}
  <p class="verdict">{e(d["verdict"])}</p>
</section>
<section class="method" aria-labelledby="method-h">
  <h2 id="method-h">{ub["method_title"]}</h2>
  <p>{ub["method_lead"]}</p>
  <ol class="steps">{steps}</ol>
</section>"""


def canone_map(lang: str) -> str:
    ub = UI_BOOKS[lang]
    rows = []
    for i, part in enumerate(CANONE):
        end = (CANONE[i + 1]["start"] - 1) if i + 1 < len(CANONE) else CANONE_END
        left = (part["start"] - 1) / CANONE_END * 100
        width = (end - part["start"] + 1) / CANONE_END * 100
        name = e(part["name"]) if lang == "pt" else f'{e(part["en"])} <span class="tr" lang="pt">{e(part["name"])}</span>'
        chapters = "".join(
            f'<li><span class="ch-n">{n}</span><span lang="pt">{e(t)}</span><span class="ch-p">{ub["page"]} {num(pg, lang)}</span></li>'
            for n, t, pg in part["chapters"]
        )  # fmt: skip
        label = part["part"]
        inner = f'<ol class="chs">{chapters}</ol>' if chapters else ""
        summary = (f'<span class="part-n">{label}</span><span class="part-name">{name}</span>'
                   f'<span class="part-pages">{ub["page"]} {num(part["start"], lang)}–{num(end, lang)}</span>'
                   f'<span class="track" aria-hidden="true"><span style="left:{left:.2f}%;width:{width:.2f}%"></span></span>')  # fmt: skip
        if inner:
            rows.append(f"<li><details><summary>{summary}</summary>{inner}</details></li>")
        else:
            rows.append(f'<li><div class="part-row">{summary}</div></li>')
    return f"""<section class="canon-map" aria-labelledby="map-h">
  <h3 id="map-h">{ub["map_title"]}</h3>
  <p>{ub["map_lead"]}</p>
  <ol class="parts">{"".join(rows)}</ol>
</section>"""


def books_page(lang: str) -> str:
    ub = UI_BOOKS[lang]
    assets = "" if lang == "pt" else "../"
    by = {b["slug"]: b for b in BOOKS}
    trilogy = "".join(book_entry(by[s], lang, assets) for s in ("sql", "powerbi", "python"))
    body = f"""<article class="books-page">
  <h1>{ub["title"]}</h1>
  <p class="lede">{ub["lead"]}</p>
  {shelf(lang, assets, "")}
  <section class="trilogy" aria-label="{ub["trilogy"]}">
  {trilogy}
  </section>
  {decision_block(lang)}
  {book_entry(by["negocios"], lang, assets)}
  {book_entry(by["canone"], lang, assets, canone_map(lang))}
</article>"""
    return page(lang, f"{ub['page_title']}: {PERSON['name']}", ub["description"], "books.html", body, 0, "books.html")


def business_panel(slug: str, lang: str) -> str:
    b, lab = BUSINESS[slug], LABELS[lang]
    rows = "".join(f"<div><dt>{lab[k]}</dt><dd>{e(b[lang][k])}</dd></div>"
                   for k in ("decision", "users", "error", "value", "risk"))  # fmt: skip
    calc = calculator(b["calc"], lang) if b.get("calc") else ""
    return f'<section class="biz" aria-label="{lab["manager"]}"><dl class="biz-list">{rows}</dl>{calc}</section>'


# Numbers behind the calculators, all from the projects' own result files.
FRAUD_TEST = {"precision": 0.9575, "recall": 0.9655, "frauds": 2147, "rows": 30000}
FT_COST = {"vm_month": 147.17, "capacity": 4217940, "apis": [
    ("Claude Haiku 5.5, few-shot", 91.11), ("Claude Haiku 5.5, zero-shot", 44.76),
    ("GPT-5.4 mini, few-shot", 705.98), ("GPT-5.4 mini, zero-shot", 343.88)]}
SUPPLY = {"top": 0.948, "base": 0.548, "share": 0.10}

CALC_TEXT = {
    "fraud": {
        "pt": {"title": "Quanto o modelo pega no seu volume", "inputs": [
            ("tx", "Transações por mês", 1000000, 1000), ("rate", "Taxa de fraude (%)", 0.5, 0.1),
            ("ticket", "Valor médio de uma fraude (R$)", 600, 10), ("review", "Custo de revisar um alerta (R$)", 8, 1)],
            "outputs": [("caught", "Fraudes pegas por mês"), ("saved", "Valor protegido por mês (R$)"),
                        ("false", "Alertas falsos por mês"), ("prec", "Precisão no seu cenário"),
                        ("net", "Saldo: valor protegido menos custo de revisar todos os alertas (R$)")],
            "note": "Taxa de detecção (96,6%) e de alarme falso medidas no conjunto de teste, em dados sintéticos. Os "
            "outros números são premissas suas. A precisão muda com a taxa de fraude, e a conta mostra isso."},
        "en": {"title": "What the model catches at your volume", "inputs": [
            ("tx", "Transactions per month", 1000000, 1000), ("rate", "Fraud rate (%)", 0.5, 0.1),
            ("ticket", "Average fraud amount ($)", 120, 5), ("review", "Cost to review one alert ($)", 2, 0.5)],
            "outputs": [("caught", "Frauds caught per month"), ("saved", "Amount protected per month ($)"),
                        ("false", "False alerts per month"), ("prec", "Precision in your scenario"),
                        ("net", "Net: amount protected minus the cost of reviewing every alert ($)")],
            "note": "Detection rate (96.6%) and false-alarm rate measured on the test set, on synthetic data. The other "
            "numbers are your assumptions. Precision changes with the fraud rate, and the numbers show it."},
    },
    "finetune": {
        "pt": {"title": "Máquina própria ou API, no seu volume", "inputs": [
            ("req", "Requisições por mês", 3000000, 100000)],
            "outputs": [], "own": "Modelo ajustado, VM própria", "vm": "VM", "vms": "VMs",
            "note": "Custo da VM (US$ 147,17/mês) e capacidade medida (4,2 milhões de requisições por mês por VM) vêm "
            "do benchmark do projeto; preços de API são os de tabela. A precisão das APIs nesta tarefa não foi medida.",
            "cheapest": "mais barato", "month": "por mês"},
        "en": {"title": "Own machine or API, at your volume", "inputs": [
            ("req", "Requests per month", 3000000, 100000)],
            "outputs": [], "own": "Fine-tuned model, own VM", "vm": "VM", "vms": "VMs",
            "note": "VM cost ($147.17/month) and measured capacity (4.2 million requests a month per VM) come from the "
            "project's benchmark; API prices are list prices. The APIs' accuracy on this task was not measured.",
            "cheapest": "cheapest", "month": "per month"},
    },
    "supply": {
        "pt": {"title": "Agir nos 10% de pedidos mais arriscados", "inputs": [
            ("orders", "Pedidos por mês", 10000, 500), ("late_cost", "Custo de um atraso (R$)", 40, 5),
            ("act_cost", "Custo de agir num pedido (R$)", 5, 1), ("fix", "Atrasos evitados quando a equipe age (%)", 30, 5)],
            "outputs": [("model", "Atrasos alcançados com o modelo"), ("random", "Atrasos alcançados escolhendo ao acaso"),
                        ("net", "Saldo com o modelo por mês (R$)"), ("net_random", "Saldo escolhendo ao acaso (R$)")],
            "note": "94,8% dos pedidos no topo de risco atrasaram no teste, contra 54,8% de atraso na base inteira. "
            "Custos e eficácia da ação são premissas suas."},
        "en": {"title": "Acting on the riskiest 10% of orders", "inputs": [
            ("orders", "Orders per month", 10000, 500), ("late_cost", "Cost of one late order ($)", 10, 1),
            ("act_cost", "Cost to act on one order ($)", 1, 0.5), ("fix", "Delays prevented when the team acts (%)", 30, 5)],
            "outputs": [("model", "Late orders reached with the model"), ("random", "Late orders reached picking at random"),
                        ("net", "Net with the model per month ($)"), ("net_random", "Net picking at random ($)")],
            "note": "94.8% of the orders at the top of the risk ranking were late in the test, against 54.8% late across "
            "the whole dataset. Costs and how well the action works are your assumptions."},
    },
}


def calculator(kind: str, lang: str) -> str:
    t = CALC_TEXT[kind][lang]
    data = {"fraud": FRAUD_TEST, "finetune": FT_COST, "supply": SUPPLY}[kind]
    inputs = "".join(
        f'<label><span>{e(label)}</span><input type="number" name="{name}" value="{value}" min="0" step="{step}" '
        f'inputmode="decimal"></label>'
        for name, label, value, step in t["inputs"]
    )  # fmt: skip
    if kind == "finetune":
        outs = '<table class="calc-table"><tbody data-out="table"></tbody></table>'
    else:
        outs = '<dl class="calc-out">' + "".join(
            f'<div><dt>{e(label)}</dt><dd><output data-out="{name}">–</output></dd></div>' for name, label in t["outputs"]
        ) + "</dl>"  # fmt: skip
    extra = {k: t[k] for k in ("own", "vm", "vms", "cheapest", "month") if k in t}
    payload = e(json.dumps({"kind": kind, "lang": lang, "data": data, "text": extra}, ensure_ascii=False))
    return f"""<form class="calc" data-calc="{payload}" onsubmit="return false">
  <h3>{LABELS[lang]["calc"]}: {e(t["title"])}</h3>
  <div class="calc-in">{inputs}</div>
  <div aria-live="polite">{outs}</div>
  <p class="calc-note">{e(t["note"])}</p>
</form>"""


def not_found(lang: str) -> str:
    u = UI[lang]
    body = f"""<article class="case">
  <h1>{u["notfound_title"]}</h1>
  <p class="lede">{u["notfound_text"]}</p>
  <p class="links"><a href="{SITE}/{PREFIX[lang]}">{u["notfound_link"]}</a></p>
</article>"""
    # 404 is served at any depth, so it uses absolute asset URLs.
    html = page(lang, f"{u['notfound_title']}: {PERSON['name']}", u["description"], "404.html", body, 0, "")
    html = html.replace("location.replace('en/", f"location.replace('{SITE}/en/")
    for attr in ('href="assets/', 'src="assets/', 'href="index.html', 'href="books.html', 'href="en/'):
        html = html.replace(attr, attr.replace('"', f'"{SITE}/', 1))
    # Not a page to index: no canonical or language alternates, and robots told so.
    html = "\n".join(l for l in html.split("\n") if 'rel="canonical"' not in l and 'rel="alternate"' not in l)
    return html.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)


def og_page() -> str:
    """1200x630 social preview, rendered to assets/og.png."""
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="assets/og.css"></head>
<body><div class="og"><img src="{AVATAR}" alt=""><div>
<p class="name">{PERSON["name"]}</p>
<p class="role">{e(PERSON["role"]["pt"])} | {e(PERSON["role"]["en"])}</p>
<p class="head">{e(PERSON["headline"]["pt"])}</p>
<p class="nums"><span>97,6M</span> linhas no pipeline <span>92%</span> menos bytes lidos <span>{sum(p["group"] == TEAM for p in PROJECTS)}</span> sistemas em uso real</p>
<p class="url">diegoalves.vercel.app</p></div></div></body></html>
"""


def check() -> list[str]:
    problems = []
    slugs = [p["slug"] for p in PROJECTS]
    if len(set(slugs)) != len(slugs):
        problems.append("duplicate slugs")
    for p in PROJECTS:
        s = p["slug"]
        if p["group"] not in ANCHOR:
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
        for lang in LANGS if p.get("video") else []:
            name = media_name(p["video"], lang)
            for f in (f"{name}.mp4", f"{name}-poster.webp"):
                if not (ROOT / "assets" / "media" / f).exists():
                    problems.append(f"{s}: missing assets/media/{f}")
        if p.get("image") and not (ROOT / "assets" / "media" / f"{p['image']}.webp").exists():
            problems.append(f"{s}: missing image {p['image']}")
    for p in PROJECTS:
        b = BUSINESS.get(p["slug"])
        if not b:
            problems.append(f"{p['slug']}: no manager view in business.py")
            continue
        for lang in LANGS:
            for key in ("decision", "users", "error", "value", "risk"):
                if not b.get(lang, {}).get(key):
                    problems.append(f"{p['slug']}: manager view missing {lang}.{key}")
        if b.get("calc") and b["calc"] not in CALC_TEXT:
            problems.append(f"{p['slug']}: unknown calculator {b['calc']}")
    for b in BOOKS:
        if not (ROOT / "assets" / "media" / "books" / f"{b['slug']}.webp").exists():
            problems.append(f"book {b['slug']}: missing cover")
        if b["lang"] not in ("pt", "en"):
            problems.append(f"book {b['slug']}: unknown language")
    for m in METHOD:
        if m["slug"] not in {p["slug"] for p in PROJECTS}:
            problems.append(f"method step {m['en']}: unknown project {m['slug']}")
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
        (base / "books.html").write_text(books_page(lang), encoding="utf-8")
        for i, p in enumerate(PROJECTS):
            (base / "projects" / f"{p['slug']}.html").write_text(project_page(p, i, lang), encoding="utf-8")
    (OUT / "404.html").write_text(not_found("pt"), encoding="utf-8")
    (OUT / "og.html").write_text(og_page(), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    urls = []
    for lang in LANGS:
        urls += [f"{SITE}/{PREFIX[lang]}", f"{SITE}/{PREFIX[lang]}books.html"] + [f"{SITE}/{PREFIX[lang]}projects/{p['slug']}.html" for p in PROJECTS]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {2 * (len(PROJECTS) + 2)} pages in two languages into {OUT}")


if __name__ == "__main__":
    main()
