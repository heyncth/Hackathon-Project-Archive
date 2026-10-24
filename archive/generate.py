"""Deterministic README index generation."""

from __future__ import annotations

import re
from pathlib import Path

from .loader import ProjectDoc, RepoData

BEGIN_MARK = "<!-- BEGIN GENERATED PROJECT INDEX -->"
END_MARK = "<!-- END GENERATED PROJECT INDEX -->"


def _sorted_projects(repo: RepoData) -> list[ProjectDoc]:
    domain_order = {d["id"]: i for i, d in enumerate(repo.taxonomy.get("domains", []))}

    def key(doc: ProjectDoc):
        data = doc.data or {}
        return (
            domain_order.get(data.get("domain", ""), len(domain_order)),
            data.get("name", "").casefold(),
            data.get("id", ""),
        )

    valid = [d for d in repo.projects if d.data and not d.parse_error]
    return sorted(valid, key=key)


def _fmt_links(data: dict) -> str:
    labels = {"official": "Official", "source": "Source", "demo": "Demo", "video": "Video"}
    links = data.get("links")
    if not isinstance(links, dict):
        return ""
    parts = [f"[{labels[k]}]({links[k]})" for k in ("official", "source", "demo", "video") if k in links]
    return " · ".join(parts)


def _fmt_event(data: dict) -> str:
    event = data.get("event")
    if not isinstance(event, dict):
        return ""
    bits = [event.get("name", "")]
    if event.get("organizer"):
        bits.append(event["organizer"])
    if event.get("year") is not None:
        bits.append(str(event["year"]))
    line = " — ".join(b for b in bits if b)
    if event.get("award"):
        line += f" — **Award:** {event['award']}"
    return line


def render_project(doc: ProjectDoc) -> str:
    data = doc.data or {}
    name = data.get("name", doc.path.stem)
    desc = re.sub(r"\s+", " ", data.get("description", "").strip())
    lines = [f"### {name}", "", desc, ""]
    event = _fmt_event(data)
    if event:
        lines.append(f"- **Event:** {event}")
    authors = data.get("authors")
    if isinstance(authors, list) and authors:
        lines.append(f"- **Team:** {', '.join(authors)}")
    links = _fmt_links(data)
    if links:
        lines.append(f"- **Links:** {links}")
    notes = data.get("notes")
    if isinstance(notes, str) and notes.strip():
        lines.append(f"- **Notes:** {re.sub(r'\s+', ' ', notes.strip())}")
    return "\n".join(lines)


def generate_index(repo: RepoData) -> str:
    """Render the full generated index section (without markers)."""
    domain_names = {d["id"]: d["name"] for d in repo.taxonomy.get("domains", [])}
    projects = _sorted_projects(repo)

    by_domain: dict[str, list[ProjectDoc]] = {}
    for doc in projects:
        by_domain.setdefault((doc.data or {}).get("domain", "other"), []).append(doc)

    out: list[str] = []
    for domain in repo.taxonomy.get("domains", []):
        domain_id = domain["id"]
        docs = by_domain.get(domain_id)
        if not docs:
            continue
        out.append(f"## {domain_names[domain_id]}")
        out.append("")
        for doc in docs:
            out.append(render_project(doc))
            out.append("")
    if not out:
        out.append("_No projects yet._")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def splice_index(readme_text: str, index: str) -> str:
    begin = readme_text.find(BEGIN_MARK)
    end = readme_text.find(END_MARK)
    if begin == -1 or end == -1 or end < begin:
        raise ValueError(f"README must contain '{BEGIN_MARK}' and '{END_MARK}' markers")
    head = readme_text[: begin + len(BEGIN_MARK)]
    tail = readme_text[end:]
    return f"{head}\n\n{index}\n{tail}"


def generate_readme(repo: RepoData) -> str:
    readme_path = repo.root / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    return splice_index(current, generate_index(repo))


def write_readme(repo: RepoData) -> None:
    (repo.root / "README.md").write_text(generate_readme(repo), encoding="utf-8")


def check_readme(repo: RepoData) -> str | None:
    """Return an error message if README is stale, else None."""
    readme_path = repo.root / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    try:
        expected = generate_readme(repo)
    except ValueError as exc:
        return str(exc)
    if current != expected:
        return "README.md is stale: run 'python -m archive generate' and commit the result"
    return None
