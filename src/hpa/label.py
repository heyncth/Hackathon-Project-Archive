"""Qualitative label rules (docs/labeling-methodology.md).

No numeric overall score. Labels only when definitions are satisfied.
"""

from __future__ import annotations

from typing import Any

HIGH_STARS = 1000
MODERATE_STARS = 100


def popularity_from_stars(stars: int | None) -> str:
    if stars is None:
        return "unknown"
    if stars >= HIGH_STARS:
        return "high"
    if stars >= MODERATE_STARS:
        return "moderate"
    return "limited"


def apply_labels(
    project: dict[str, Any],
    participations: list[dict[str, Any]],
    metrics_snapshots: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return project with categories/popularity refined from evidence."""
    out = dict(project)

    stars = None
    for snap in metrics_snapshots:
        if snap.get("stars") is not None:
            stars = snap["stars"] if stars is None else max(stars, snap["stars"])
    out["popularity"] = popularity_from_stars(stars)

    categories: set[str] = set(out.get("categories") or [])
    award_won = any(p.get("award_name") and p.get("verified") for p in participations)
    if award_won:
        categories.add("award-winning")
    # community-notable: popularity or education or any discovery record default
    if out["popularity"] in ("high", "moderate") or out.get("educational_value") in ("high", "moderate"):
        categories.add("community-notable")
    if not categories:
        # a discovered project without an award still enters the archive
        # as community-notable with honest unknown/limited labels
        categories.add("community-notable")
    out["categories"] = sorted(categories)

    # An unverified award must not sit under award-winning.
    if not award_won:
        out["categories"] = [c for c in out["categories"] if c != "award-winning"]

    # Unverified award claims become an explicit limitation.
    unverified_awards = [
        p for p in participations if p.get("award_name") and not p.get("verified")
    ]
    if unverified_awards and not any("unverified award" in lim.lower() for lim in out.get("limitations", [])):
        out["limitations"] = sorted(
            set(out.get("limitations", []))
            | {"Unverified award claim(s) present; not confirmed by an official results page."}
        )
    return out
