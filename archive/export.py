"""JSON export of project records for future integrations."""

from __future__ import annotations

import datetime
import json

from .loader import RepoData


def _default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"not JSON serializable: {type(obj)}")


def export_projects(repo: RepoData) -> list[dict]:
    out = []
    for doc in repo.projects:
        if not doc.data:
            continue
        out.append(doc.data)
    return out


def export_json(repo: RepoData, indent: int = 2) -> str:
    return json.dumps(export_projects(repo), indent=indent, ensure_ascii=False, sort_keys=True, default=_default) + "\n"
