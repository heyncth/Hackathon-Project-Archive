"""Fixture adapter: reads candidates from a local JSON file.

Used by tests and offline demos. Data is synthetic unless the fixture file
explicitly embeds real public URLs; it is never treated as a live discovery.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hpa.adapters.base import RawCandidate, SearchAdapter, SearchFailure


class FixtureAdapter(SearchAdapter):
    name = "fixture"

    def search(self, query: str, limit: int = 10) -> list[RawCandidate]:
        path = self.source.get("base_url") or self.source.get("fixture_path")
        if not path:
            raise SearchFailure("fixture: source entry lacks base_url/fixture_path")
        file_path = Path(path)
        if not file_path.is_file():
            # allow absolute path override via query prefix "file:"
            if query.startswith("file:"):
                file_path = Path(query[5:].strip())
            if not file_path.is_file():
                raise SearchFailure(f"fixture: file not found: {path}")
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SearchFailure(f"fixture: cannot read {file_path}: {exc}") from exc

        items: list[dict[str, Any]] = data.get("candidates", data if isinstance(data, list) else [])
        if not isinstance(items, list):
            raise SearchFailure("fixture: expected a list of candidates")

        out: list[RawCandidate] = []
        for item in items[:limit]:
            if not item.get("name"):
                continue
            out.append(
                RawCandidate(
                    source_id=item.get("source_id", self.source_id),
                    source_url=item.get("source_url", "https://example.invalid/fixture"),
                    name=item["name"],
                    description=item.get("description"),
                    repo_url=item.get("repo_url"),
                    stars=item.get("stars"),
                    forks=item.get("forks"),
                    language=item.get("language"),
                    topics=list(item.get("topics") or []),
                    official_url=item.get("official_url"),
                    demo_url=item.get("demo_url"),
                    event_name=item.get("event_name"),
                    event_year=item.get("event_year"),
                    event_url=item.get("event_url"),
                    award_name=item.get("award_name"),
                    award_category=item.get("award_category"),
                    award_verified=bool(item.get("award_verified", False)),
                    documentation_quality=item.get("documentation_quality"),
                    educational_value=item.get("educational_value"),
                    evidence=list(item.get("evidence") or []),
                )
            )
        return out
