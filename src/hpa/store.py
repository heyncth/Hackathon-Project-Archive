"""Load and save canonical entity records under data/."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ENTITY_DIRS = {
    "projects": "projects",
    "repositories": "repositories",
    "events": "events",
    "participations": "participations",
    "evidence": "evidence",
    "metrics": "metrics",
    "guides": "guides",
}

# map entity key -> schema file name
SCHEMA_FILES = {
    "projects": "project.schema.json",
    "repositories": "repository.schema.json",
    "events": "event.schema.json",
    "participations": "participation.schema.json",
    "evidence": "evidence.schema.json",
    "metrics": "metrics_snapshot.schema.json",
    "guides": "guide.schema.json",
}


def _stringify_datetimes(value: Any) -> Any:
    """YAML parses bare timestamps into datetime; schemas expect ISO strings."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {k: _stringify_datetimes(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_datetimes(v) for v in value]
    return value


class DataStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.data_dir = self.root / "data"
        self.schemas_dir = self.root / "schemas"

    def entity_dir(self, entity: str) -> Path:
        return self.data_dir / ENTITY_DIRS[entity]

    def path_for(self, entity: str, entity_id: str) -> Path:
        return self.entity_dir(entity) / f"{entity_id}.yaml"

    def load_all(self, entity: str) -> dict[str, dict[str, Any]]:
        directory = self.entity_dir(entity)
        out: dict[str, dict[str, Any]] = {}
        if not directory.is_dir():
            return out
        for path in sorted(directory.glob("*.yaml")):
            with path.open(encoding="utf-8") as fh:
                record = yaml.safe_load(fh)
            if isinstance(record, dict):
                record = _stringify_datetimes(record)
            if isinstance(record, dict) and "id" in record:
                out[record["id"]] = record
        return out

    def save(self, entity: str, record: dict[str, Any]) -> Path:
        directory = self.entity_dir(entity)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{record['id']}.yaml"
        # sort keys for deterministic diffs
        text = yaml.safe_dump(record, sort_keys=True, allow_unicode=True, width=100)
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text, encoding="utf-8")
        return path

    def load_everything(self) -> dict[str, dict[str, dict[str, Any]]]:
        return {entity: self.load_all(entity) for entity in ENTITY_DIRS}
