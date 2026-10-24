"""Shared test helpers: build throwaway repo trees in tmp dirs."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from archive.loader import load_repo

TAXONOMY = {
    "domains": [
        {"id": "games", "name": "Games"},
        {"id": "web-mobile", "name": "Web & Mobile"},
        {"id": "other", "name": "Other"},
    ],
    "tag_pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
    "max_tags_per_project": 8,
}

VALID_PROJECT = textwrap.dedent(
    """\
    ---
    id: example-project
    name: Example Project
    description: A short description.
    domain: games
    tags: [demo, fixture]
    event:
      name: Example Hackathon
      organizer: Example Org
      year: 2020
      award: Winner
    links:
      official: https://example.com
      source: https://github.com/example/example
    authors:
      - Ada Lovelace
    evidence:
      - url: https://example.com/evidence
        supports: "Award and participation claims"
    notes: A note.
    verified_at: 2026-01-01
    ---
    """
)

README_TEMPLATE = textwrap.dedent(
    """\
    # Test Archive

    Intro text.

    <!-- BEGIN GENERATED STATS -->
    <!-- END GENERATED STATS -->

    Outro text.
    """
)


def make_repo(tmp: Path, projects: dict[str, str] | None = None, readme: bool = True) -> Path:
    """Create a minimal repo tree. `projects` maps filename -> file content."""
    (tmp / "data" / "projects").mkdir(parents=True, exist_ok=True)
    (tmp / "data" / "taxonomy.json").write_text(json.dumps(TAXONOMY), encoding="utf-8")
    for name, content in (projects or {}).items():
        (tmp / "data" / "projects" / name).write_text(content, encoding="utf-8")
    if readme:
        (tmp / "README.md").write_text(README_TEMPLATE, encoding="utf-8")
    return tmp


def load(tmp: Path):
    return load_repo(tmp)
