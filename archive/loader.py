"""Load taxonomy and project records from the repository."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)


@dataclass
class ProjectDoc:
    path: Path
    data: dict | None = None
    body: str = ""
    parse_error: str | None = None


@dataclass
class RepoData:
    root: Path
    taxonomy: dict = field(default_factory=dict)
    projects: list[ProjectDoc] = field(default_factory=list)
    load_errors: list[tuple[Path, str]] = field(default_factory=list)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_taxonomy(root: Path) -> dict:
    path = root / "data" / "taxonomy.json"
    import json

    with path.open(encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (data, body, error)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text, "missing or malformed YAML frontmatter"
    raw, body = m.group(1), m.group(2)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, body, "frontmatter must be a YAML mapping"
    return data, body, None


def load_project(path: Path) -> ProjectDoc:
    text = path.read_text(encoding="utf-8")
    data, body, err = parse_frontmatter(text)
    return ProjectDoc(path=path, data=data, body=body, parse_error=err)


def load_repo(root: Path) -> RepoData:
    repo = RepoData(root=root)
    repo.taxonomy = load_taxonomy(root)
    projects_dir = root / "data" / "projects"
    if projects_dir.is_dir():
        for path in sorted(projects_dir.glob("*.md")):
            repo.projects.append(load_project(path))
    return repo
