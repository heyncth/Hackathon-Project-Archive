"""Search adapter interface.

Adapters turn a query into RawCandidate dicts. Provider-specific parsing
stays inside each adapter. Failures raise SearchFailure and are recorded in
the run report; they never abort the whole pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class SearchFailure(Exception):
    """A source could not be searched. Not evidence of absence."""


@dataclass
class RawCandidate:
    """Minimal shape every adapter must produce.

    Unknown fields stay None; normalize.py turns them into explicit nulls.
    """

    source_id: str
    source_url: str
    name: str
    description: str | None = None
    repo_url: str | None = None
    stars: int | None = None
    forks: int | None = None
    language: str | None = None
    topics: list[str] = field(default_factory=list)
    official_url: str | None = None
    demo_url: str | None = None
    event_name: str | None = None
    event_year: int | None = None
    event_url: str | None = None
    award_name: str | None = None
    award_category: str | None = None
    award_verified: bool = False
    documentation_quality: str | None = None  # curated hint only (fixtures)
    educational_value: str | None = None  # curated hint only (fixtures)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_url": self.source_url,
            "name": self.name,
            "description": self.description,
            "repo_url": self.repo_url,
            "stars": self.stars,
            "forks": self.forks,
            "language": self.language,
            "topics": list(self.topics),
            "official_url": self.official_url,
            "demo_url": self.demo_url,
            "event_name": self.event_name,
            "event_year": self.event_year,
            "event_url": self.event_url,
            "award_name": self.award_name,
            "award_category": self.award_category,
            "award_verified": self.award_verified,
            "documentation_quality": self.documentation_quality,
            "educational_value": self.educational_value,
            "evidence": list(self.evidence),
        }


class SearchAdapter(ABC):
    """Base interface for discovery providers."""

    name: str = "base"

    def __init__(self, source: dict[str, Any]):
        self.source = source
        self.source_id = source["id"]

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> list[RawCandidate]:
        """Search the source. Raises SearchFailure on unrecoverable errors."""
