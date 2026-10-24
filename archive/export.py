"""JSON export of project records for future integrations."""

from __future__ import annotations

import datetime
import json
import re

from .loader import RepoData

RAPID_RE = re.compile(
    r"hackathon|game jam|jam|hack week|hackathon|sprint|weekend|startup weekend|7 day|ld\d+|ludum dare",
    re.IGNORECASE,
)


def _default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"not JSON serializable: {type(obj)}")


def hot_score(data: dict) -> int:
    """Compute hotness from objective signals. Deterministic, never stored."""
    score = 0
    if (data.get("event") or {}).get("award"):
        score += 20
    links = data.get("links") or {}
    if links.get("source"):
        score += 15
    if links.get("demo"):
        score += 15
    tags = set(data.get("tags") or [])
    if tags & {"used-by-millions", "became-startup"}:
        score += 15
    if data.get("deep_dive"):
        score += 20
    event_name = (data.get("event") or {}).get("name", "")
    if RAPID_RE.search(event_name):
        score += 10
    year = (data.get("event") or {}).get("year")
    if isinstance(year, int):
        if year >= 2024:
            score += 5
        elif year >= 2020:
            score += 3
        elif year >= 2015:
            score += 1
    return min(score, 100)


def export_projects(repo: RepoData) -> list[dict]:
    out = []
    for doc in repo.projects:
        if not doc.data:
            continue
        entry = dict(doc.data)
        entry["hot"] = hot_score(doc.data)
        entry["body"] = doc.body
        out.append(entry)
    return out


def export_json(repo: RepoData, indent: int = 2) -> str:
    return json.dumps(export_projects(repo), indent=indent, ensure_ascii=False, sort_keys=True, default=_default) + "\n"
