"""Static site generation for GitHub Pages."""

from __future__ import annotations

import datetime
import html
import json
import re
from pathlib import Path

from .export import export_projects
from .loader import RepoData

SITE_DIR = "site"

_MARK = (
    '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">'
    '<rect width="18" height="3" y="2" rx="1.5" fill="#c6f24e"/>'
    '<rect width="12" height="3" y="7.5" rx="1.5" fill="#c6f24e"/>'
    '<rect width="6" height="3" y="13" rx="1.5" fill="#c6f24e"/>'
    "</svg>"
)

_FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" '
    'rel="stylesheet">'
)


def _default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"not JSON serializable: {type(obj)}")


def _domain_map(repo: RepoData) -> dict[str, str]:
    return {d["id"]: d["name"] for d in repo.taxonomy.get("domains", [])}


def _discovery_tags(repo: RepoData) -> list[dict]:
    return repo.taxonomy.get("discovery_tags", [])


def _payload(repo: RepoData) -> dict:
    return {
        "projects": export_projects(repo),
        "domains": _domain_map(repo),
        "discovery_tags": [d["id"] for d in _discovery_tags(repo)],
    }


# --- minimal markdown renderer for deep-dive bodies ---

def _md_escape(text: str) -> str:
    return html.escape(text, quote=False)


def _inline(text: str) -> str:
    text = _md_escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(
        r"\[(.+?)\]\((.+?)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def render_markdown(body: str) -> str:
    lines = body.split("\n")
    out: list[str] = []
    in_list = False
    in_code = False
    para: list[str] = []

    def flush_para():
        nonlocal para
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para = []

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in lines:
        if line.startswith("```"):
            flush_para()
            flush_list()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        stripped = line.strip()
        if not stripped:
            flush_para()
            flush_list()
            continue
        if stripped.startswith("#### "):
            flush_para()
            flush_list()
            out.append(f"<h4>{_inline(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            flush_para()
            flush_list()
            out.append(f"<h3>{_inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            flush_para()
            flush_list()
            out.append(f"<h2>{_inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            flush_para()
            flush_list()
            out.append(f"<h1>{_inline(stripped[2:])}</h1>")
        elif stripped.startswith(("- ", "* ")):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(stripped[2:])}</li>")
        else:
            flush_list()
            para.append(stripped)

    flush_para()
    flush_list()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


# --- shared tokens and shell (true-black flat, app sheet seed 1731133658) ---

_BASE_CSS = """
:root {
  color-scheme: dark;
  --ground: #000000; --surface: #111111; --raised: #2a2a2a;
  --rule: #161616; --edge: #1a1a1a; --control: #444444;
  --text: #ffffff; --muted: #b4b4b4; --faint: #949494;
  --accent: #c6f24e; --warning: #e5a93b;
  --pill-neutral-bg: #222222; --pill-neutral-ink: #ffffff;
  --pill-warning-bg: #2b2414; --pill-warning-ink: #e5a93b;
  --radius-card: 20px; --radius-control: 999px;
  --gap: 14px; --pad: 22px; --control-h: 36px;
  --fs-title: 20px; --fs-section: 16px; --fs-kpi: 24px;
  --fs-body: 14px; --fs-small: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--ground); color: var(--text);
  font: 400 var(--fs-body)/1.5 "Inter", system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
:focus-visible { outline: 2px solid var(--text); outline-offset: 2px; }
.wrap { max-width: 1150px; margin: 0 auto; padding: 0 28px; }
.topbar { border-bottom: 1px solid var(--edge); }
.topbar-in {
  max-width: 1150px; margin: 0 auto; padding: 0 28px; height: 64px;
  display: flex; align-items: center; gap: 16px;
}
.brand {
  display: flex; align-items: center; gap: 10px;
  font: 600 var(--fs-title)/1.2 "Inter", system-ui, sans-serif;
  letter-spacing: -0.01em;
}
.brand svg { display: block; flex: none; }
a.brand:hover { color: var(--muted); }
.pill {
  display: inline-block; max-width: 24em; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;
  background: var(--pill-neutral-bg); color: var(--pill-neutral-ink);
  border-radius: var(--radius-control); padding: 1px 10px;
  font-size: var(--fs-small); line-height: 1.7;
}
.pill.warn { background: var(--pill-warning-bg); color: var(--pill-warning-ink); }
.pill-group { display: inline-flex; gap: 6px; flex-wrap: wrap; }
.state { color: var(--muted); padding: 32px 0; font-size: var(--fs-body); }
.btn {
  background: var(--surface); color: var(--text); border: 1px solid var(--control);
  border-radius: var(--radius-control); height: var(--control-h); padding: 0 18px;
  font: 500 var(--fs-body)/1 "Inter", system-ui, sans-serif; cursor: pointer;
}
.btn:hover { background: var(--raised); }
footer {
  max-width: 1150px; margin: 0 auto; padding: 36px 28px 48px;
  color: var(--faint); font-size: var(--fs-small);
  display: flex; gap: 18px; flex-wrap: wrap;
}
footer a:hover { color: var(--text); }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

_INDEX_CSS = """
.lede { color: var(--muted); font-size: var(--fs-body); padding-top: 22px; }
.filters {
  display: flex; flex-wrap: wrap; gap: var(--gap); align-items: center;
  padding-top: 18px;
}
select {
  height: var(--control-h); padding: 0 12px; border: 0;
  border-radius: var(--radius-control); background: var(--surface);
  color: var(--text); font: 400 13px/1 "Inter", system-ui, sans-serif;
}
select:hover { background: var(--raised); }
.count {
  margin-left: auto; color: var(--faint); font-size: var(--fs-small);
  font-variant-numeric: tabular-nums;
}
.search { margin-left: auto; }
.search input {
  width: 340px; max-width: 100%; height: var(--control-h);
  border: 0; border-radius: var(--radius-control);
  background: #ffffff; color: #000000; padding: 0 18px;
  font: 400 var(--fs-body)/1 "Inter", system-ui, sans-serif;
}
.search input::placeholder { color: #6b6b6b; }
.cards { display: flex; gap: var(--gap); padding-top: var(--gap); }
.card-q {
  flex: 1 1 0; min-width: 0; height: 61px; padding: 12px;
  background: var(--surface); border: 1.5px solid transparent;
  border-radius: var(--radius-card); color: var(--text);
  text-align: left; font: inherit; cursor: pointer;
}
.card-q:hover { background: #171717; }
.card-q .lab { display: block; color: var(--muted); font-size: 13px; }
.card-q .val {
  display: block; margin-top: 2px; font-size: 16px; font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.card-q[aria-pressed="true"] {
  border-color: var(--accent); background: rgba(198, 242, 78, 0.08);
}
.card-q[aria-pressed="true"] .lab { color: var(--accent); }
.list {
  background: var(--surface); border-radius: var(--radius-card);
  margin-top: var(--gap); overflow: hidden;
}
.row {
  display: grid; grid-template-columns: 1fr 132px; gap: var(--gap);
  padding: 16px var(--pad); border-top: 1px solid var(--rule);
  cursor: pointer; transition: background 0.15s;
}
.row:first-child { border-top: 0; }
.row:hover { background: #171717; }
.row-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; }
.row-name { font-size: 16px; font-weight: 600; }
.row-name:hover { text-decoration: underline; }
.row-desc {
  color: var(--muted); font-size: 13px; margin-top: 5px; max-width: 90ch;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden;
}
.row-meta { color: var(--faint); font-size: var(--fs-small); margin-top: 7px; }
.row-tags { color: var(--faint); font-size: var(--fs-small); margin-top: 3px; }
.row-links { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 9px; font-size: var(--fs-small); }
.row-links a { color: var(--muted); text-decoration: underline; text-underline-offset: 2px; }
.row-links a:hover { color: var(--text); }
.hot { text-align: right; }
.hot .n {
  font-size: 16px; font-weight: 600; font-variant-numeric: tabular-nums;
}
.bar { display: block; height: 3px; background: var(--rule); margin-top: 8px; }
.bar i { display: block; height: 3px; background: var(--accent); }
@media (max-width: 767px) {
  .topbar-in { height: auto; padding: 12px 20px; flex-wrap: wrap; }
  .search { margin-left: 0; width: 100%; }
  .search input { width: 100%; }
  .wrap, footer { padding-left: 20px; padding-right: 20px; }
  .count { margin-left: 0; width: 100%; }
  .cards { overflow-x: auto; padding-bottom: 4px; }
  .card-q { flex: 0 0 150px; }
  .row { grid-template-columns: 1fr 96px; padding: 14px 16px; }
}
"""

_DETAIL_CSS = """
.grid6 {
  display: grid; grid-template-columns: repeat(6, 1fr);
  gap: var(--gap); padding-top: 22px; padding-bottom: 8px;
}
.s2 { grid-column: span 2; }
.s3 { grid-column: span 3; }
.s6 { grid-column: span 6; }
.card { background: var(--surface); border-radius: var(--radius-card); padding: var(--pad); }
.head { display: flex; gap: var(--gap); align-items: flex-start; justify-content: space-between; }
.head-main { min-width: 0; }
.head h1 {
  display: inline; font-size: var(--fs-title); font-weight: 600;
  letter-spacing: -0.01em;
}
.head-pills { margin-left: 10px; white-space: nowrap; }
.head-meta { color: var(--muted); font-size: 13px; margin-top: 8px; }
.head-desc { color: var(--muted); font-size: 13px; margin-top: 6px; max-width: 78ch; }
.head-tags { color: var(--faint); font-size: var(--fs-small); margin-top: 7px; }
.head-actions { display: flex; gap: 8px; flex: none; flex-wrap: wrap; justify-content: flex-end; }
.act {
  display: inline-flex; align-items: center; height: var(--control-h);
  padding: 0 15px; border: 1px solid var(--control);
  border-radius: var(--radius-control); font-size: 13px;
  transition: background 0.15s;
}
.act:hover { background: var(--raised); }
.kpi .lab { color: var(--muted); font-size: 13px; }
.kpi .val {
  margin-top: 5px; font-size: var(--fs-kpi); font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.kpi.hot-kpi .val { color: var(--accent); }
.sect h2 { font-size: var(--fs-section); font-weight: 600; margin-bottom: 9px; }
.sect p { font-size: var(--fs-body); }
.content { max-width: 76ch; }
.content h2 { font-size: var(--fs-section); font-weight: 600; margin: 26px 0 9px; }
.content h2:first-child { margin-top: 0; }
.content h3 { font-size: var(--fs-body); font-weight: 600; margin: 20px 0 7px; }
.content h4 { font-size: 13px; font-weight: 600; margin: 16px 0 6px; color: var(--muted); }
.content p { margin-bottom: 11px; }
.content ul { margin: 0 0 11px 22px; }
.content li { margin-bottom: 5px; }
.content a { color: var(--muted); text-decoration: underline; text-underline-offset: 2px; }
.content a:hover { color: var(--text); }
.content strong { font-weight: 600; }
.content pre { background: var(--raised); padding: 13px; overflow-x: auto; margin-bottom: 12px; }
.content code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
.evi li { margin-bottom: 7px; font-size: 13px; word-break: break-all; }
.evi a { color: var(--muted); text-decoration: underline; text-underline-offset: 2px; }
.evi a:hover { color: var(--text); }
.evi .sup { color: var(--faint); }
@media (max-width: 767px) {
  .grid6 { grid-template-columns: 1fr; }
  .s2, .s3, .s6 { grid-column: span 1; }
  .head { flex-direction: column; }
  .head-actions { justify-content: flex-start; }
  .head-pills { display: block; margin: 8px 0 0; }
}
"""

# --- detail page ---

def _detail_pills(p: dict, domain_name: str) -> str:
    pills = []
    event = p.get("event") or {}
    award = event.get("award")
    if award:
        pills.append(
            f'<span class="pill warn" title="{html.escape(str(award), quote=True)}">'
            f"{html.escape(str(award))}</span>"
        )
    body = p.get("body") or ""
    if p.get("deep_dive"):
        pills.append('<span class="pill">Deep dive</span>')
    elif body.strip():
        pills.append('<span class="pill">Profile</span>')
    if domain_name:
        pills.insert(0, f'<span class="pill">{html.escape(domain_name)}</span>')
    return f'<span class="head-pills">{"".join(pills)}</span>'


def _detail_meta(p: dict) -> str:
    event = p.get("event") or {}
    bits = [event.get("name"), event.get("organizer"), event.get("year")]
    text = " · ".join(str(b) for b in bits if b)
    return f'<p class="head-meta">{html.escape(text)}</p>' if text else ""


def _detail_actions(p: dict) -> str:
    links = p.get("links") or {}
    parts = []
    for key, label in (("official", "Official"), ("source", "Source"), ("demo", "Demo"), ("video", "Video")):
        url = links.get(key)
        if url:
            parts.append(
                f'<a class="act" href="{html.escape(url)}" target="_blank" rel="noopener">{label}</a>'
            )
    return f'<div class="head-actions">{"".join(parts)}</div>' if parts else ""


def _detail_kpis(p: dict) -> str:
    tiles = []
    hot = p.get("hot")
    if isinstance(hot, (int, float)):
        pct = max(0, min(100, hot))
        tiles.append(
            f'<div class="card s2 kpi hot-kpi"><div class="lab">Hot score</div>'
            f'<div class="val">{hot}</div>'
            f'<span class="bar"><i style="width:{pct}%"></i></span></div>'
        )
    else:
        tiles.append(
            '<div class="card s2 kpi hot-kpi"><div class="lab">Hot score</div>'
            '<div class="val">&mdash;</div></div>'
        )
    year = (p.get("event") or {}).get("year")
    tiles.append(
        f'<div class="card s2 kpi"><div class="lab">Year</div>'
        f'<div class="val">{html.escape(str(year)) if year else "&mdash;"}</div></div>'
    )
    evidence = len(p.get("evidence") or [])
    tiles.append(
        f'<div class="card s2 kpi"><div class="lab">Evidence</div>'
        f'<div class="val">{evidence}</div></div>'
    )
    return "".join(tiles)


def _detail_evidence(p: dict) -> str:
    items = p.get("evidence") or []
    if not items:
        return ""
    lis = []
    for ev in items:
        url = ev.get("url", "")
        supports = ev.get("supports", "")
        text = f"{supports}: " if supports else ""
        lis.append(
            f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener">'
            f'<span class="sup">{html.escape(text)}</span>{html.escape(url)}</a></li>'
        )
    return (
        '<div class="card s6 sect evi"><h2>Evidence</h2>'
        f'<ul>{"".join(lis)}</ul></div>'
    )


def _build_detail_page(p: dict, domain_name: str) -> str:
    name = html.escape(p.get("name", ""))
    desc = html.escape(p.get("description", ""))
    desc_attr = html.escape(p.get("description", ""), quote=True)

    tags = p.get("tags") or []
    tags_html = (
        f'<p class="head-tags">{" · ".join(html.escape(t) for t in tags)}</p>'
        if tags
        else ""
    )

    idea = p.get("key_idea") or ""
    learn = p.get("learn_from") or ""
    idea_html = ""
    learn_html = ""
    if idea and learn:
        idea_html = f'<div class="card s3 sect"><h2>Key idea</h2><p>{html.escape(idea)}</p></div>'
        learn_html = f'<div class="card s3 sect"><h2>Learn from this</h2><p>{html.escape(learn)}</p></div>'
    elif idea:
        idea_html = f'<div class="card s6 sect"><h2>Key idea</h2><p>{html.escape(idea)}</p></div>'
    elif learn:
        learn_html = f'<div class="card s6 sect"><h2>Learn from this</h2><p>{html.escape(learn)}</p></div>'

    content = ""
    if (p.get("body") or "").strip():
        content = (
            f'<div class="card s6"><div class="content">{render_markdown(p["body"])}</div></div>'
        )

    head_open = (
        '<div class="card s6"><div class="head"><div class="head-main">'
        f"<h1>{name}</h1>{_detail_pills(p, domain_name)}"
        f"{_detail_meta(p)}"
        f'<p class="head-desc">{desc}</p>{tags_html}'
        "</div>"
        f"{_detail_actions(p)}"
        "</div></div>"
    )

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{name} - Hackathon Project Archive</title>\n"
        f'<meta name="description" content="{desc_attr}">\n'
        f"{_FONT_LINKS}\n"
        "<style>\n"
        f"{_BASE_CSS}\n{_DETAIL_CSS}"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        '<header class="topbar"><div class="topbar-in">'
        f'<a class="brand" href="../index.html">{_MARK}Archive</a>'
        "</div></header>\n"
        f'<main class="wrap grid6">\n{head_open}\n{_detail_kpis(p)}'
        f"\n{idea_html}\n{learn_html}\n{content}\n{_detail_evidence(p)}\n"
        "</main>\n"
        '<footer>\n'
        '  <a href="../index.html">Archive</a>\n'
        '  <a href="https://github.com/heyncth/Hackathon-Project-Archive">GitHub</a>\n'
        '  <a href="../data.json">Data JSON</a>\n'
        "</footer>\n"
        "</body>\n"
        "</html>\n"
    )


def build_site(repo: RepoData) -> Path:
    site = repo.root / SITE_DIR
    site.mkdir(exist_ok=True)
    pdir = site / "p"
    pdir.mkdir(exist_ok=True)

    payload = _payload(repo)

    (site / "data.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True, default=_default) + "\n",
        encoding="utf-8",
    )
    (site / "index.html").write_text(_HTML, encoding="utf-8")
    (site / ".nojekyll").write_text("", encoding="utf-8")

    domains = _domain_map(repo)
    for p in payload["projects"]:
        pid = p.get("id")
        if not pid:
            continue
        page = _build_detail_page(p, domains.get(p.get("domain", ""), p.get("domain", "")))
        (pdir / f"{pid}.html").write_text(page, encoding="utf-8")

    return site


def check_site(repo: RepoData) -> str | None:
    site = repo.root / SITE_DIR
    index = site / "index.html"
    data = site / "data.json"
    if not index.exists() or not data.exists() or not (site / ".nojekyll").exists():
        return "site/ missing: run 'python -m archive generate'"
    payload = _payload(repo)
    expected = json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
        default=_default,
    ) + "\n"
    actual = data.read_text(encoding="utf-8")
    if actual != expected:
        return "site/data.json is stale: run 'python -m archive generate'"

    if index.read_text(encoding="utf-8") != _HTML:
        return "site/index.html is stale: run 'python -m archive generate'"

    domains = _domain_map(repo)
    for p in payload["projects"]:
        pid = p.get("id")
        if not pid:
            continue
        page = site / "p" / f"{pid}.html"
        if not page.exists():
            return f"site/p/{pid}.html is missing: run 'python -m archive generate'"
        domain = domains.get(p.get("domain", ""), p.get("domain", ""))
        if page.read_text(encoding="utf-8") != _build_detail_page(p, domain):
            return f"site/p/{pid}.html is stale: run 'python -m archive generate'"
    return None


_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hackathon Project Archive</title>
<meta name="description" content="Notable hackathon projects, with evidence.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  color-scheme: dark;
  --ground: #000000; --surface: #111111; --raised: #2a2a2a;
  --rule: #161616; --edge: #1a1a1a; --control: #444444;
  --text: #ffffff; --muted: #b4b4b4; --faint: #949494;
  --accent: #c6f24e; --warning: #e5a93b;
  --pill-neutral-bg: #222222; --pill-neutral-ink: #ffffff;
  --pill-warning-bg: #2b2414; --pill-warning-ink: #e5a93b;
  --radius-card: 20px; --radius-control: 999px;
  --gap: 14px; --pad: 22px; --control-h: 36px;
  --fs-title: 20px; --fs-section: 16px; --fs-kpi: 24px;
  --fs-body: 14px; --fs-small: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--ground); color: var(--text);
  font: 400 var(--fs-body)/1.5 "Inter", system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
:focus-visible { outline: 2px solid var(--text); outline-offset: 2px; }
.wrap { max-width: 1150px; margin: 0 auto; padding: 0 28px; }
.topbar { border-bottom: 1px solid var(--edge); }
.topbar-in {
  max-width: 1150px; margin: 0 auto; padding: 0 28px; height: 64px;
  display: flex; align-items: center; gap: 16px;
}
.brand {
  display: flex; align-items: center; gap: 10px;
  font: 600 var(--fs-title)/1.2 "Inter", system-ui, sans-serif;
  letter-spacing: -0.01em;
}
.brand svg { display: block; flex: none; }
a.brand:hover { color: var(--muted); }
.pill {
  display: inline-block; max-width: 24em; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;
  background: var(--pill-neutral-bg); color: var(--pill-neutral-ink);
  border-radius: var(--radius-control); padding: 1px 10px;
  font-size: var(--fs-small); line-height: 1.7;
}
.pill.warn { background: var(--pill-warning-bg); color: var(--pill-warning-ink); }
.pill-group { display: inline-flex; gap: 6px; flex-wrap: wrap; }
.state { color: var(--muted); padding: 32px 0; font-size: var(--fs-body); }
.btn {
  background: var(--surface); color: var(--text); border: 1px solid var(--control);
  border-radius: var(--radius-control); height: var(--control-h); padding: 0 18px;
  font: 500 var(--fs-body)/1 "Inter", system-ui, sans-serif; cursor: pointer;
}
.btn:hover { background: var(--raised); }
footer {
  max-width: 1150px; margin: 0 auto; padding: 36px 28px 48px;
  color: var(--faint); font-size: var(--fs-small);
  display: flex; gap: 18px; flex-wrap: wrap;
}
footer a:hover { color: var(--text); }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
.lede { color: var(--muted); font-size: var(--fs-body); padding-top: 22px; }
.filters {
  display: flex; flex-wrap: wrap; gap: var(--gap); align-items: center;
  padding-top: 18px;
}
select {
  height: var(--control-h); padding: 0 12px; border: 0;
  border-radius: var(--radius-control); background: var(--surface);
  color: var(--text); font: 400 13px/1 "Inter", system-ui, sans-serif;
}
select:hover { background: var(--raised); }
.count {
  margin-left: auto; color: var(--faint); font-size: var(--fs-small);
  font-variant-numeric: tabular-nums;
}
.search { margin-left: auto; }
.search input {
  width: 340px; max-width: 100%; height: var(--control-h);
  border: 0; border-radius: var(--radius-control);
  background: #ffffff; color: #000000; padding: 0 18px;
  font: 400 var(--fs-body)/1 "Inter", system-ui, sans-serif;
}
.search input::placeholder { color: #6b6b6b; }
.cards { display: flex; gap: var(--gap); padding-top: var(--gap); }
.card-q {
  flex: 1 1 0; min-width: 0; height: 61px; padding: 12px;
  background: var(--surface); border: 1.5px solid transparent;
  border-radius: var(--radius-card); color: var(--text);
  text-align: left; font: inherit; cursor: pointer;
}
.card-q:hover { background: #171717; }
.card-q .lab { display: block; color: var(--muted); font-size: 13px; }
.card-q .val {
  display: block; margin-top: 2px; font-size: 16px; font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.card-q[aria-pressed="true"] {
  border-color: var(--accent); background: rgba(198, 242, 78, 0.08);
}
.card-q[aria-pressed="true"] .lab { color: var(--accent); }
.list {
  background: var(--surface); border-radius: var(--radius-card);
  margin-top: var(--gap); overflow: hidden;
}
.row {
  display: grid; grid-template-columns: 1fr 132px; gap: var(--gap);
  padding: 16px var(--pad); border-top: 1px solid var(--rule);
  cursor: pointer; transition: background 0.15s;
}
.row:first-child { border-top: 0; }
.row:hover { background: #171717; }
.row-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; }
.row-name { font-size: 16px; font-weight: 600; }
.row-name:hover { text-decoration: underline; }
.row-desc {
  color: var(--muted); font-size: 13px; margin-top: 5px; max-width: 90ch;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden;
}
.row-meta { color: var(--faint); font-size: var(--fs-small); margin-top: 7px; }
.row-tags { color: var(--faint); font-size: var(--fs-small); margin-top: 3px; }
.row-links { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 9px; font-size: var(--fs-small); }
.row-links a { color: var(--muted); text-decoration: underline; text-underline-offset: 2px; }
.row-links a:hover { color: var(--text); }
.hot { text-align: right; }
.hot .n {
  font-size: 16px; font-weight: 600; font-variant-numeric: tabular-nums;
}
.bar { display: block; height: 3px; background: var(--rule); margin-top: 8px; }
.bar i { display: block; height: 3px; background: var(--accent); }
@media (max-width: 767px) {
  .topbar-in { height: auto; padding: 12px 20px; flex-wrap: wrap; }
  .search { margin-left: 0; width: 100%; }
  .search input { width: 100%; }
  .wrap, footer { padding-left: 20px; padding-right: 20px; }
  .count { margin-left: 0; width: 100%; }
  .cards { overflow-x: auto; padding-bottom: 4px; }
  .card-q { flex: 0 0 150px; }
  .row { grid-template-columns: 1fr 96px; padding: 14px 16px; }
}
</style>
</head>
<body>
<header class="topbar"><div class="topbar-in">
  <h1 class="brand"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><rect width="18" height="3" y="2" rx="1.5" fill="#c6f24e"/><rect width="12" height="3" y="7.5" rx="1.5" fill="#c6f24e"/><rect width="6" height="3" y="13" rx="1.5" fill="#c6f24e"/></svg>Hackathon Project Archive</h1>
  <div class="search"><input type="search" id="q" placeholder="Search name, description, tags..." autocomplete="off" aria-label="Search projects"></div>
</div></header>

<main class="wrap">
  <p class="lede">Notable hackathon projects, with evidence.</p>

  <div class="filters">
    <select id="domain" aria-label="Filter by domain"><option value="">All domains</option></select>
    <select id="discovery" aria-label="Filter by tag"><option value="">All tags</option></select>
    <select id="sort" aria-label="Sort projects">
      <option value="hot">Sort: Hot</option>
      <option value="name">Sort: Name</option>
      <option value="year-desc">Sort: Newest</option>
      <option value="year-asc">Sort: Oldest</option>
      <option value="domain">Sort: Domain</option>
    </select>
    <p class="count" id="count"></p>
  </div>

  <div class="cards" role="group" aria-label="Quick filters">
    <button class="card-q" type="button" data-q="awarded" aria-pressed="false"><span class="lab">Awarded</span><span class="val">0</span></button>
    <button class="card-q" type="button" data-q="deep" aria-pressed="false"><span class="lab">Deep dives</span><span class="val">0</span></button>
    <button class="card-q" type="button" data-q="open-source" aria-pressed="false"><span class="lab">Open source</span><span class="val">0</span></button>
    <button class="card-q" type="button" data-q="playable" aria-pressed="false"><span class="lab">Playable</span><span class="val">0</span></button>
  </div>

  <div class="list" id="results"><p class="state">Loading projects...</p></div>
</main>

<noscript><p class="state wrap">This page needs JavaScript to load data.json.</p></noscript>

<footer>
  <a href="https://github.com/heyncth/Hackathon-Project-Archive">GitHub</a>
  <a href="https://github.com/heyncth/Hackathon-Project-Archive/blob/main/CONTRIBUTING.md">Contribute</a>
  <a href="data.json">Data JSON</a>
</footer>

<script>
let DATA = null;
let DISCOVERY = new Set();
let quick = { awarded: false, deep: false };

const QF = [
  { id: 'awarded', t: function (p) { return !!(p.event && p.event.award); } },
  { id: 'deep', t: function (p) { return !!p.deep_dive; } },
  { id: 'open-source', tag: true, t: function (p) { return (p.tags || []).indexOf('open-source') > -1; } },
  { id: 'playable', tag: true, t: function (p) { return (p.tags || []).indexOf('playable') > -1; } }
];

function qf(id) {
  for (const c of QF) if (c.id === id) return c;
  return null;
}

async function init() {
  const out = document.getElementById('results');
  out.innerHTML = '<p class="state">Loading projects...</p>';
  try {
    const res = await fetch('data.json');
    if (!res.ok) throw new Error('HTTP ' + res.status);
    DATA = await res.json();
  } catch (err) {
    out.innerHTML = '<p class="state">Could not load the archive data.</p>' +
      '<button class="btn" id="retry" type="button">Try again</button>';
    document.getElementById('retry').addEventListener('click', init);
    return;
  }
  DISCOVERY = new Set(DATA.discovery_tags || []);
  populateDomains();
  populateDiscovery();
  document.getElementById('q').addEventListener('input', render);
  document.getElementById('domain').addEventListener('change', render);
  document.getElementById('discovery').addEventListener('change', render);
  document.getElementById('sort').addEventListener('change', render);
  document.querySelectorAll('.card-q').forEach(function (btn) {
    btn.addEventListener('click', function () { toggle(btn.getAttribute('data-q')); });
  });
  document.getElementById('results').addEventListener('click', function (e) {
    if (e.target.closest('a')) return;
    const row = e.target.closest('.row');
    if (row) location.href = row.getAttribute('data-go');
  });
  render();
}

function toggle(id) {
  if (id === 'awarded' || id === 'deep') {
    quick[id] = !quick[id];
  } else {
    const sel = document.getElementById('discovery');
    sel.value = sel.value === id ? '' : id;
  }
  render();
}

function populateDomains() {
  const sel = document.getElementById('domain');
  const counts = {};
  for (const p of DATA.projects) {
    const d = p.domain || 'other';
    counts[d] = (counts[d] || 0) + 1;
  }
  const ids = Object.keys(counts).sort((a, b) =>
    (DATA.domains[a] || a).localeCompare(DATA.domains[b] || b)
  );
  for (const id of ids) {
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = (DATA.domains[id] || id) + ' (' + counts[id] + ')';
    sel.appendChild(opt);
  }
}

function populateDiscovery() {
  const sel = document.getElementById('discovery');
  const counts = {};
  for (const p of DATA.projects) {
    for (const t of (p.tags || [])) {
      if (DISCOVERY.has(t)) counts[t] = (counts[t] || 0) + 1;
    }
  }
  for (const id of Array.from(DISCOVERY).sort()) {
    if (!counts[id]) continue;
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = id + ' (' + counts[id] + ')';
    sel.appendChild(opt);
  }
}

function matchBase(p) {
  const q = document.getElementById('q').value.toLowerCase();
  const domain = document.getElementById('domain').value;
  if (domain && (p.domain || 'other') !== domain) return false;
  if (q) {
    const hay = [
      p.name, p.description, p.key_idea, ...(p.tags || []),
      p.event && p.event.name, p.event && p.event.organizer
    ].filter(Boolean).join(' ').toLowerCase();
    if (hay.indexOf(q) === -1) return false;
  }
  return true;
}

function countQuick(card) {
  const disc = document.getElementById('discovery').value;
  let n = 0;
  for (const p of DATA.projects) {
    if (!matchBase(p)) continue;
    if (disc && disc !== card.id && (p.tags || []).indexOf(disc) === -1) continue;
    if (card.id !== 'awarded' && quick.awarded && !qf('awarded').t(p)) continue;
    if (card.id !== 'deep' && quick.deep && !qf('deep').t(p)) continue;
    if (!card.t(p)) continue;
    n++;
  }
  return n;
}

function render() {
  const disc = document.getElementById('discovery').value;
  const sort = document.getElementById('sort').value;

  document.querySelectorAll('.card-q').forEach(function (btn) {
    const id = btn.getAttribute('data-q');
    const card = qf(id);
    btn.querySelector('.val').textContent = String(countQuick(card));
    const on = card.tag ? disc === id : !!quick[id];
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
  });

  let items = DATA.projects.filter(p => {
    if (!matchBase(p)) return false;
    if (disc && (p.tags || []).indexOf(disc) === -1) return false;
    if (quick.awarded && !(p.event && p.event.award)) return false;
    if (quick.deep && !p.deep_dive) return false;
    return true;
  });

  items.sort((a, b) => {
    if (sort === 'hot') return (b.hot || 0) - (a.hot || 0) || (a.name || '').localeCompare(b.name || '');
    if (sort === 'year-desc') return ((b.event && b.event.year) || 0) - ((a.event && a.event.year) || 0);
    if (sort === 'year-asc') return ((a.event && a.event.year) || 9999) - ((b.event && b.event.year) || 9999);
    if (sort === 'domain') {
      const da = DATA.domains[a.domain] || a.domain || '';
      const db = DATA.domains[b.domain] || b.domain || '';
      return da.localeCompare(db) || (a.name || '').localeCompare(b.name || '');
    }
    return (a.name || '').localeCompare(b.name || '');
  });

  document.getElementById('count').textContent =
    items.length + ' of ' + DATA.projects.length + ' projects';

  const out = document.getElementById('results');
  if (!items.length) {
    out.innerHTML = '<p class="state">No projects match.</p>';
    return;
  }
  out.innerHTML = items.map(row).join('');
}

function lnk(url, label) {
  return '<a href="' + esc(url) + '" target="_blank" rel="noopener">' + label + '</a>';
}

function row(p) {
  const links = [];
  if (p.links) {
    if (p.links.official) links.push(lnk(p.links.official, 'Official'));
    if (p.links.source) links.push(lnk(p.links.source, 'Source'));
    if (p.links.demo) links.push(lnk(p.links.demo, 'Demo'));
    if (p.links.video) links.push(lnk(p.links.video, 'Video'));
  }

  const pills = [];
  if (p.event && p.event.award) {
    pills.push('<span class="pill warn" title="' + esc(p.event.award) + '">' + esc(p.event.award) + '</span>');
  }
  if (p.deep_dive) pills.push('<span class="pill">Deep dive</span>');

  const meta = [];
  if (DATA.domains[p.domain]) meta.push(DATA.domains[p.domain]);
  if (p.event) {
    if (p.event.name) meta.push(p.event.name);
    if (p.event.organizer) meta.push(p.event.organizer);
    if (p.event.year) meta.push(String(p.event.year));
  }

  const detail = 'p/' + esc(p.id) + '.html';
  const hot = typeof p.hot === 'number' ? p.hot : 0;
  const pct = Math.max(0, Math.min(100, hot));

  return '<article class="row" data-go="' + detail + '">' +
    '<div class="row-main">' +
      '<div class="row-head"><a class="row-name" href="' + detail + '">' + esc(p.name || '') + '</a>' +
      (pills.length ? '<span class="pill-group">' + pills.join('') + '</span>' : '') + '</div>' +
      (p.description ? '<p class="row-desc">' + esc(p.description) + '</p>' : '') +
      (meta.length ? '<p class="row-meta">' + meta.map(esc).join(' &middot; ') + '</p>' : '') +
      ((p.tags || []).length ? '<p class="row-tags">' + p.tags.map(esc).join(' &middot; ') + '</p>' : '') +
      (links.length ? '<div class="row-links">' + links.join('') + '</div>' : '') +
    '</div>' +
    '<div class="hot"><div class="n">' + hot + '</div>' +
    '<span class="bar"><i style="width:' + pct + '%"></i></span></div>' +
    '</article>';
}

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

init();
</script>
</body>
</html>
"""
