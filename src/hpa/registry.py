"""Source registry loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class RegistryError(Exception):
    pass


def load_registry(root: Path) -> list[dict[str, Any]]:
    path = Path(root) / "sources" / "sources.yaml"
    if not path.is_file():
        raise RegistryError(f"source registry not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "sources" not in data:
        raise RegistryError("sources.yaml must contain a top-level 'sources' list")
    sources = data["sources"]
    if not isinstance(sources, list):
        raise RegistryError("'sources' must be a list")
    required = {"id", "name", "type", "base_url", "adapter", "limitations", "requires_auth"}
    for src in sources:
        missing = required - set(src)
        if missing:
            raise RegistryError(f"source {src.get('id', '?')}: missing fields {sorted(missing)}")
    return sources


def get_source(sources: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
    for src in sources:
        if src["id"] == source_id:
            return src
    raise RegistryError(f"unknown source id: {source_id}")


def sources_for_adapter(sources: list[dict[str, Any]], adapter: str) -> list[dict[str, Any]]:
    return [s for s in sources if s.get("adapter") == adapter]
