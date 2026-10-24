"""Deterministic README stats generation."""

from __future__ import annotations

import re
from pathlib import Path

from .loader import ProjectDoc, RepoData

BEGIN_MARK = "<!-- BEGIN GENERATED STATS -->"
END_MARK = "<!-- END GENERATED STATS -->"


def _valid_projects(repo: RepoData) -> list[ProjectDoc]:
    return [d for d in repo.projects if d.data and not d.parse_error]


def _domain_counts(repo: RepoData) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for doc in _valid_projects(repo):
        domain = (doc.data or {}).get("domain", "other")
        counts[domain] = counts.get(domain, 0) + 1
    domain_order = {d["id"]: i for i, d in enumerate(repo.taxonomy.get("domains", []))}
    return sorted(counts.items(), key=lambda kv: (-kv[1], domain_order.get(kv[0], 99), kv[0]))


def render_stats(repo: RepoData) -> str:
    projects = _valid_projects(repo)
    n = len(projects)
    awarded = sum(
        1
        for d in projects
        if isinstance((d.data or {}).get("event"), dict)
        and (d.data or {}).get("event", {}).get("award")
    )
    lines = [f"**{n} projects** across {len(repo.taxonomy.get('domains', []))} domains"]
    if awarded:
        lines[0] += f" · {awarded} with documented awards"
    lines.append("")
    parts = []
    for domain_id, count in _domain_counts(repo):
        name = next(
            (d["name"] for d in repo.taxonomy.get("domains", []) if d["id"] == domain_id),
            domain_id,
        )
        parts.append(f"{name} ({count})")
    lines.append(" · ".join(parts))
    return "\n".join(lines)


def splice_stats(readme_text: str, stats: str) -> str:
    begin = readme_text.find(BEGIN_MARK)
    end = readme_text.find(END_MARK)
    if begin == -1 or end == -1 or end < begin:
        raise ValueError(f"README must contain '{BEGIN_MARK}' and '{END_MARK}' markers")
    head = readme_text[: begin + len(BEGIN_MARK)]
    tail = readme_text[end:]
    return f"{head}\n{stats}\n{tail}"


def generate_readme(repo: RepoData) -> str:
    readme_path = repo.root / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    return splice_stats(current, render_stats(repo))


def write_readme(repo: RepoData) -> None:
    (repo.root / "README.md").write_text(generate_readme(repo), encoding="utf-8")


def check_readme(repo: RepoData) -> str | None:
    readme_path = repo.root / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    try:
        expected = generate_readme(repo)
    except ValueError as exc:
        return str(exc)
    if current != expected:
        return "README.md is stale: run 'python -m archive generate' and commit the result"
    return None
