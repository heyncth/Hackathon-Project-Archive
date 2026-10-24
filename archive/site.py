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


# --- detail page ---

_DETAIL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} - Hackathon Project Archive</title>
<meta name="description" content="{desc_attr}">
<style>
:root {{
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --badge-bg: #1f6feb22;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6;
  max-width: 760px; margin: 0 auto; padding: 2rem 1.25rem;
}}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.back {{ font-size: 0.9rem; margin-bottom: 1.5rem; display: inline-block; }}
h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; }}
.desc {{ font-size: 1.05rem; color: var(--muted); margin-bottom: 1rem; }}
.badges {{ display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 1rem; }}
.badge {{
  font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 999px;
  background: var(--badge-bg); color: var(--accent); border: 1px solid var(--border);
}}
.badge.award {{ background: #d2992222; color: #d29922; }}
.badge.learn {{ background: #23863622; color: #3fb950; }}
.meta {{ font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem; }}
.links {{ font-size: 0.9rem; margin-bottom: 1.5rem; }}
.links a {{ margin-right: 1rem; }}
.callout {{
  background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--accent);
  border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1.25rem;
}}
.callout .label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent); margin-bottom: 0.25rem; }}
.callout p {{ font-size: 0.95rem; }}
.content h2 {{ font-size: 1.25rem; margin: 1.5rem 0 0.5rem; }}
.content h3 {{ font-size: 1.1rem; margin: 1.25rem 0 0.4rem; }}
.content p {{ margin-bottom: 0.75rem; font-size: 0.95rem; }}
.content ul {{ margin: 0 0 0.75rem 1.25rem; }}
.content li {{ font-size: 0.95rem; margin-bottom: 0.25rem; }}
.content pre {{ background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; overflow-x: auto; margin-bottom: 0.75rem; }}
.content code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85rem; }}
.content a {{ color: var(--accent); }}
.kicker {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 0.75rem; }}
.evidence {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }}
.evidence h2 {{ font-size: 1rem; color: var(--muted); }}
.evidence li {{ font-size: 0.85rem; color: var(--muted); }}
footer {{ margin-top: 2rem; font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--border); padding-top: 1rem; }}
</style>
</head>
<body>
<a class="back" href="../index.html">&larr; Back to archive</a>
<h1>{name}</h1>
<p class="desc">{desc}</p>
{badges}
{meta}
{links}
{callout_idea}
{callout_learn}
{content}
{evidence}
<footer>
  <a href="../index.html">Archive</a> &middot;
  <a href="https://github.com/heyncth/Hackathon-Project-Archive">GitHub</a> &middot;
  <a href="../data.json">JSON</a>
</footer>
</body>
</html>
"""


def _detail_badges(p: dict, domain_name: str, discovery_ids: set[str]) -> str:
    badges = [f'<span class="badge">{html.escape(domain_name)}</span>']
    if p.get("deep_dive"):
        badges.append('<span class="badge learn">Learn</span>')
    event = p.get("event") or {}
    if event.get("award"):
        badges.append(f'<span class="badge award">{html.escape(str(event["award"]))}</span>')
    for t in p.get("tags", []):
        cls = "badge"
        if t in discovery_ids:
            cls += " discover"
        badges.append(f'<span class="{cls}">{html.escape(t)}</span>')
    return f'<div class="badges">{"".join(badges)}</div>'


def _detail_meta(p: dict) -> str:
    event = p.get("event")
    if not event:
        return ""
    bits = [event.get("name"), event.get("organizer"), event.get("year")]
    text = " - ".join(str(b) for b in bits if b)
    return f'<p class="meta">{html.escape(text)}</p>' if text else ""


def _detail_links(p: dict) -> str:
    links = p.get("links") or {}
    parts = []
    for key, label in (("official", "Official"), ("source", "Source"), ("demo", "Demo"), ("video", "Video")):
        url = links.get(key)
        if url:
            parts.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{label}</a>')
    return f'<div class="links">{"".join(parts)}</div>' if parts else ""


def _detail_evidence(p: dict) -> str:
    items = p.get("evidence") or []
    if not items:
        return ""
    lis = []
    for ev in items:
        url = ev.get("url", "")
        supports = ev.get("supports", "")
        text = f"{supports}: " if supports else ""
        lis.append(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener">{text}{html.escape(url)}</a></li>')
    return f'<div class="evidence"><h2>Evidence</h2><ul>{"".join(lis)}</ul></div>'


def _build_detail_page(p: dict, domain_name: str, discovery_ids: set[str]) -> str:
    callout_idea = ""
    if p.get("key_idea"):
        callout_idea = (
            f'<div class="callout"><div class="label">Key idea</div>'
            f"<p>{html.escape(p['key_idea'])}</p></div>"
        )
    callout_learn = ""
    if p.get("learn_from"):
        callout_learn = (
            f'<div class="callout"><div class="label">Learn from this</div>'
            f"<p>{html.escape(p['learn_from'])}</p></div>"
        )
    content = ""
    if p.get("body") and p.get("body").strip():
        label = "Deep dive" if p.get("deep_dive") else "Profile"
        content = (
            f'<div class="content"><div class="kicker">{label}</div>'
            f'{render_markdown(p["body"])}</div>'
        )
    return _DETAIL_TEMPLATE.format(
        name=html.escape(p.get("name", "")),
        desc=html.escape(p.get("description", "")),
        desc_attr=html.escape(p.get("description", ""), quote=True),
        badges=_detail_badges(p, domain_name, discovery_ids),
        meta=_detail_meta(p),
        links=_detail_links(p),
        callout_idea=callout_idea,
        callout_learn=callout_learn,
        content=content,
        evidence=_detail_evidence(p),
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
    discovery_ids = {d["id"] for d in _discovery_tags(repo)}
    for p in payload["projects"]:
        pid = p.get("id")
        if not pid:
            continue
        page = _build_detail_page(p, domains.get(p.get("domain", ""), p.get("domain", "")), discovery_ids)
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
    discovery_ids = {d["id"] for d in _discovery_tags(repo)}
    for p in payload["projects"]:
        pid = p.get("id")
        if not pid:
            continue
        page = site / "p" / f"{pid}.html"
        if not page.exists():
            return f"site/p/{pid}.html is missing: run 'python -m archive generate'"
        domain = domains.get(p.get("domain", ""), p.get("domain", ""))
        if page.read_text(encoding="utf-8") != _build_detail_page(p, domain, discovery_ids):
            return f"site/p/{pid}.html is stale: run 'python -m archive generate'"
    return None


_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hackathon Project Archive</title>
<meta name="description" content="Notable hackathon projects, with evidence.">
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --badge-bg: #1f6feb22; --green: #3fb950;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.5;
  max-width: 960px; margin: 0 auto; padding: 2rem 1rem;
}
header { margin-bottom: 1.5rem; }
h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
.subtitle { color: var(--muted); font-size: 0.95rem; }
.stats { color: var(--muted); font-size: 0.85rem; margin-top: 0.5rem; }
.controls {
  display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.25rem;
  position: sticky; top: 0; background: var(--bg); padding: 0.75rem 0; z-index: 10;
  border-bottom: 1px solid var(--border);
}
input[type="search"], select {
  background: var(--surface); color: var(--text); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.9rem;
}
input[type="search"] { flex: 1; min-width: 200px; }
select { min-width: 130px; }
label.chk {
  display: flex; align-items: center; gap: 0.35rem; font-size: 0.85rem;
  color: var(--muted); cursor: pointer; white-space: nowrap; padding: 0 0.25rem;
}
.count { color: var(--muted); font-size: 0.85rem; margin-bottom: 0.75rem; }
.card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  padding: 1rem 1.25rem; margin-bottom: 0.75rem; cursor: pointer;
  transition: border-color 0.15s;
}
.card:hover { border-color: var(--accent); }
.card h2 { font-size: 1.1rem; margin-bottom: 0.35rem; }
.card h2 a { color: var(--accent); text-decoration: none; }
.card h2 a:hover { text-decoration: underline; }
.card .desc { font-size: 0.9rem; margin-bottom: 0.5rem; color: var(--muted); }
.card .idea {
  font-size: 0.85rem; color: var(--text); margin-bottom: 0.5rem;
  padding-left: 0.6rem; border-left: 2px solid var(--accent);
}
.meta { font-size: 0.8rem; color: var(--muted); margin-bottom: 0.4rem; }
.badges { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.4rem; }
.badge {
  font-size: 0.7rem; padding: 0.15rem 0.5rem; border-radius: 999px;
  background: var(--badge-bg); color: var(--accent); border: 1px solid var(--border);
}
.badge.award { background: #d2992222; color: #d29922; }
.badge.learn { background: #23863622; color: var(--green); border-color: #23863655; }
.badge.hot-badge { background: #da363322; color: #f85149; border-color: #da363355; }
.links { font-size: 0.8rem; }
.links a { color: var(--accent); text-decoration: none; margin-right: 0.75rem; }
.links a:hover { text-decoration: underline; }
.empty { color: var(--muted); text-align: center; padding: 3rem 0; }
footer { margin-top: 2rem; font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--border); padding-top: 1rem; }
footer a { color: var(--accent); text-decoration: none; }
</style>
</head>
<body>
<header>
  <h1>Hackathon Project Archive</h1>
  <p class="subtitle">Notable hackathon projects, with evidence.</p>
  <p class="stats" id="stats"></p>
</header>

<div class="controls">
  <input type="search" id="q" placeholder="Search name, description, tags..." autocomplete="off">
  <select id="domain"><option value="">All domains</option></select>
  <select id="discovery"><option value="">All tags</option></select>
  <select id="sort">
    <option value="hot">Sort: Hot</option>
    <option value="name">Sort: Name</option>
    <option value="year-desc">Sort: Newest</option>
    <option value="year-asc">Sort: Oldest</option>
    <option value="domain">Sort: Domain</option>
  </select>
  <label class="chk"><input type="checkbox" id="awarded"> Awarded</label>
  <label class="chk"><input type="checkbox" id="deeponly"> Deep dives</label>
</div>

<p class="count" id="count"></p>
<main id="results"></main>

<footer>
  <a href="https://github.com/heyncth/Hackathon-Project-Archive">GitHub</a> &middot;
  <a href="https://github.com/heyncth/Hackathon-Project-Archive/blob/main/CONTRIBUTING.md">Contribute</a> &middot;
  Data <a href="data.json">JSON</a>
</footer>

<script>
let DATA = null;
let DISCOVERY = new Set();

async function init() {
  const res = await fetch('data.json');
  DATA = await res.json();
  DISCOVERY = new Set(DATA.discovery_tags || []);
  populateDomains();
  populateDiscovery();
  render();
  document.getElementById('q').addEventListener('input', render);
  document.getElementById('domain').addEventListener('change', render);
  document.getElementById('discovery').addEventListener('change', render);
  document.getElementById('sort').addEventListener('change', render);
  document.getElementById('awarded').addEventListener('change', render);
  document.getElementById('deeponly').addEventListener('change', render);
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
  const n = DATA.projects.length;
  const awarded = DATA.projects.filter(p => p.event && p.event.award).length;
  const deep = DATA.projects.filter(p => p.deep_dive).length;
  document.getElementById('stats').textContent =
    n + ' projects / ' + awarded + ' awarded / ' + deep + ' deep dives';
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

function render() {
  const q = document.getElementById('q').value.toLowerCase();
  const domain = document.getElementById('domain').value;
  const disc = document.getElementById('discovery').value;
  const sort = document.getElementById('sort').value;
  const awardedOnly = document.getElementById('awarded').checked;
  const deepOnly = document.getElementById('deeponly').checked;

  let items = DATA.projects.filter(p => {
    if (domain && (p.domain || 'other') !== domain) return false;
    if (awardedOnly && !(p.event && p.event.award)) return false;
    if (deepOnly && !p.deep_dive) return false;
    if (disc && (p.tags || []).indexOf(disc) === -1) return false;
    if (q) {
      const hay = [
        p.name, p.description, p.key_idea, ...(p.tags || []),
        p.event && p.event.name, p.event && p.event.organizer,
      ].filter(Boolean).join(' ').toLowerCase();
      if (hay.indexOf(q) === -1) return false;
    }
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

  const main = document.getElementById('results');
  if (!items.length) {
    main.innerHTML = '<p class="empty">No projects match.</p>';
    return;
  }

  main.innerHTML = items.map(p => {
    const links = [];
    if (p.links) {
      if (p.links.official) links.push('<a href="' + esc(p.links.official) + '" target="_blank" rel="noopener" onclick="event.stopPropagation()">Official</a>');
      if (p.links.source) links.push('<a href="' + esc(p.links.source) + '" target="_blank" rel="noopener" onclick="event.stopPropagation()">Source</a>');
      if (p.links.demo) links.push('<a href="' + esc(p.links.demo) + '" target="_blank" rel="noopener" onclick="event.stopPropagation()">Demo</a>');
      if (p.links.video) links.push('<a href="' + esc(p.links.video) + '" target="_blank" rel="noopener" onclick="event.stopPropagation()">Video</a>');
    }
    const domainName = DATA.domains[p.domain] || p.domain || '';
    const badges = ['<span class="badge">' + esc(domainName) + '</span>'];
    if (p.deep_dive) badges.push('<span class="badge learn">Learn</span>');
    if (p.hot >= 60) badges.push('<span class="badge hot-badge">Hot ' + p.hot + '</span>');
    if (p.event && p.event.award) badges.push('<span class="badge award">' + esc(p.event.award) + '</span>');
    for (const t of (p.tags || [])) {
      const cls = DISCOVERY.has(t) ? 'badge discover' : 'badge';
      badges.push('<span class="' + cls + '">' + esc(t) + '</span>');
    }

    let meta = '';
    if (p.event) {
      const bits = [p.event.name, p.event.organizer, p.event.year].filter(Boolean);
      meta = bits.map(esc).join(' - ');
    }

    const idea = p.key_idea ? '<p class="idea">' + esc(p.key_idea) + '</p>' : '';
    const detail = 'p/' + esc(p.id) + '.html';

    return '<div class="card" onclick="location.href=\'' + detail + '\'">' +
      '<h2><a href="' + detail + '" onclick="event.stopPropagation()">' + esc(p.name) + '</a></h2>' +
      '<p class="desc">' + esc(p.description || '') + '</p>' +
      idea +
      (meta ? '<p class="meta">' + meta + '</p>' : '') +
      '<div class="badges">' + badges.join('') + '</div>' +
      (links.length ? '<div class="links">' + links.join('') + '</div>' : '') +
      '</div>';
  }).join('');
}

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

init();
</script>
</body>
</html>
"""

