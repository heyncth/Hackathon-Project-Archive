"""Evidence-status assignment."""

from __future__ import annotations

from typing import Any

_RELIABILITY_RANK = {"tertiary": 0, "secondary": 1, "primary": 2}


def _strongest(evidence: list[dict[str, Any]]) -> int:
    if not evidence:
        return -1
    return max(_RELIABILITY_RANK.get(e.get("reliability", "tertiary"), 0) for e in evidence)


def verify_project(
    project: dict[str, Any],
    evidence_by_id: dict[str, dict[str, Any]],
    participations: list[dict[str, Any]],
) -> str:
    """Return one of verified | partially-verified | unverified | disputed.

    Rules (docs/verification-policy.md):
    - disputed if limitations mention a dispute marker.
    - verified: existence/purpose evidence at primary/secondary level AND
      every verified-claim participation has award evidence; no unverified
      award claims attached.
    - partially-verified: some core claims evidenced, others weak.
    - unverified: no evidence or only tertiary.
    """
    project_evidence = [evidence_by_id[eid] for eid in project["evidence_ids"] if eid in evidence_by_id]
    strength = _strongest(project_evidence)

    if any("disputed" in lim.lower() for lim in project.get("limitations", [])):
        return "disputed"

    has_repo = bool(project.get("repository_ids"))
    has_official = bool(project.get("official_url"))
    has_award_part = any(p.get("award_name") for p in participations)
    award_parts_ok = all(p.get("verified") for p in participations if p.get("award_name"))
    award_parts_unverified = any(
        p.get("award_name") and not p.get("verified") for p in participations
    )

    if strength <= 0:
        return "unverified"
    if strength == 1 and not (has_repo or has_official):
        return "unverified"

    if strength >= 1 and (has_repo or has_official) and not has_award_part:
        # community-notable path: existence + purpose evidenced
        return "verified" if strength >= 1 else "unverified"

    if has_award_part:
        if award_parts_ok and strength >= 1:
            return "verified"
        if award_parts_unverified:
            return "partially-verified"

    if strength >= 1:
        return "partially-verified"
    return "unverified"
