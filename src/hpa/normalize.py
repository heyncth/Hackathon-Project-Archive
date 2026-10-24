"""Normalize raw candidates into structured entity drafts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from hpa.adapters.base import RawCandidate
from hpa.ids import canonical_repo_url, slugify


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _evidence_id(prefix: str, url: str, claim: str) -> str:
    key = slugify(f"{prefix} {url} {claim}", max_length=80)
    return f"ev-{key}"


def normalize_candidate(
    candidate: RawCandidate,
    run_timestamp: str,
) -> dict[str, Any]:
    """Build entity drafts from one candidate.

    Returns a bundle:
      project, repository|None, event|None, participation|None,
      evidence list, metrics|None
    Unknown values become explicit None / [] — never invented.
    """
    project_id = slugify(candidate.name)
    evidence_records: list[dict[str, Any]] = []

    for ev in candidate.evidence:
        eid = _evidence_id(project_id, ev.get("url", ""), ev.get("claim", ""))
        evidence_records.append(
            {
                "id": eid,
                "claim": ev["claim"],
                "url": ev["url"],
                "source_type": ev.get("source_type", "other"),
                "reliability": ev.get("reliability", "tertiary"),
                "accessed_at": run_timestamp,
                "notes": ev.get("notes"),
            }
        )

    # Always record where the candidate came from as evidence of discovery.
    discovery_claim = f"Project '{candidate.name}' was discovered via {candidate.source_id}."
    discovery_eid = _evidence_id(project_id, candidate.source_url, discovery_claim)
    evidence_records.append(
        {
            "id": discovery_eid,
            "claim": discovery_claim,
            "url": candidate.source_url,
            "source_type": "other",
            "reliability": "tertiary",
            "accessed_at": run_timestamp,
            "notes": "Discovery provenance; not sufficient alone for awards or architecture claims.",
        }
    )

    repository = None
    metrics = None
    if candidate.repo_url:
        repo_id = f"repo-{project_id}"
        repository = {
            "id": repo_id,
            "project_id": project_id,
            "url": canonical_repo_url(candidate.repo_url),
            "relationship": "original",
            "primary_language": candidate.language,
            "license": None,
            "last_checked": run_timestamp,
        }
        if candidate.stars is not None or candidate.forks is not None:
            metrics = {
                "id": f"metrics-{repo_id}",
                "repository_id": repo_id,
                "stars": candidate.stars,
                "forks": candidate.forks,
                "watchers": None,
                "captured_at": run_timestamp,
                "source_url": candidate.source_url,
            }

    event = None
    participation = None
    if candidate.event_name and candidate.event_year:
        event_id = f"event-{slugify(candidate.event_name)}-{candidate.event_year}"
        event = {
            "id": event_id,
            "name": candidate.event_name,
            "year": int(candidate.event_year),
            "platform": "unknown",
            "url": candidate.event_url,
            "location": None,
        }
        participation = {
            "id": f"part-{project_id}-{event_id}",
            "project_id": project_id,
            "event_id": event_id,
            "award_name": candidate.award_name,
            "award_category": candidate.award_category,
            "evidence_ids": [
                r["id"]
                for r in evidence_records
                if candidate.award_verified and candidate.award_name
            ]
            or [],
            "verified": bool(candidate.award_verified and candidate.award_name),
        }
        if candidate.award_verified and candidate.award_name and candidate.event_url:
            award_claim = (
                f"{candidate.name} won {candidate.award_name} at "
                f"{candidate.event_name} {candidate.event_year}."
            )
            award_eid = _evidence_id(project_id, candidate.event_url, award_claim)
            evidence_records.append(
                {
                    "id": award_eid,
                    "claim": award_claim,
                    "url": candidate.event_url,
                    "source_type": "official-results",
                    "reliability": "primary",
                    "accessed_at": run_timestamp,
                    "notes": "Award evidence supplied by the discovery source.",
                }
            )
            participation["evidence_ids"] = [award_eid]

    evidence_ids = sorted({r["id"] for r in evidence_records})

    project = {
        "id": project_id,
        "name": candidate.name,
        "description": candidate.description,
        # provisional; label.py refines once metrics/evidence are known
        "categories": ["community-notable"],
        "tags": sorted(set(candidate.topics)),
        "status": "unknown",
        "repository_ids": [repository["id"]] if repository else [],
        "official_url": candidate.official_url,
        "demo_url": candidate.demo_url,
        "participation_ids": [participation["id"]] if participation else [],
        "technologies": [candidate.language] if candidate.language else [],
        "evidence_ids": evidence_ids,
        "metrics_ids": [metrics["id"]] if metrics else [],
        "popularity": "unknown",
        "documentation_quality": candidate.documentation_quality or "unknown",
        "reproducibility": "not-assessed",
        "verification_status": "unverified",
        "educational_value": candidate.educational_value or "unknown",
        "guide_ids": [],
        "first_seen": run_timestamp,
        "last_checked": run_timestamp,
        "limitations": [],
        "notes": None,
    }

    return {
        "project": project,
        "repository": repository,
        "event": event,
        "participation": participation,
        "evidence": evidence_records,
        "metrics": metrics,
    }
