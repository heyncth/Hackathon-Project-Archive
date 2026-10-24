"""Deterministic Markdown generation from structured data.

Overviews are fully generated from canonical records; regenerating with
unchanged data yields byte-identical output. Case studies and reconstruction
guides are hand-authored research products; this module only writes guide
registry records and refuses to invent content for them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hpa.ids import slugify


def overview_markdown(
    project: dict[str, Any],
    repositories: list[dict[str, Any]],
    participations: list[dict[str, Any]],
    events_by_id: dict[str, dict[str, Any]],
    evidence: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
) -> str:
    lines: list[str] = []
    lines.append(f"# {project['name']}")
    lines.append("")
    lines.append("<!-- Generated from canonical structured data by `python -m hpa generate`. Do not edit by hand; edit data/ instead. -->")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(project.get("description") or "_No description available._")
    lines.append("")
    lines.append(f"**Categories:** {', '.join(project['categories'])}")
    lines.append(f"**Verification status:** {project['verification_status']}")
    lines.append(f"**Popularity:** {project['popularity']}")
    lines.append(f"**Documentation quality:** {project['documentation_quality']}")
    lines.append(f"**Reproducibility:** {project['reproducibility']}")
    lines.append(f"**Educational value:** {project['educational_value']}")
    lines.append("")
    lines.append("## Links")
    lines.append("")
    if project.get("official_url"):
        lines.append(f"- Official page: {project['official_url']}")
    if project.get("demo_url"):
        lines.append(f"- Demo: {project['demo_url']}")
    for repo in repositories:
        lines.append(f"- Repository ({repo['relationship']}): {repo['url']}")
    if not project.get("official_url") and not project.get("demo_url") and not repositories:
        lines.append("- _No public links recorded._")
    lines.append("")
    lines.append("## Hackathon participation")
    lines.append("")
    if participations:
        for part in participations:
            event = events_by_id.get(part["event_id"], {})
            award = part.get("award_name") or "no award recorded"
            verified = "verified" if part.get("verified") else "unverified"
            lines.append(
                f"- {event.get('name', part['event_id'])} ({event.get('year', '?')}): "
                f"{award} — {verified}"
            )
    else:
        lines.append("- _No event participation recorded._")
    lines.append("")
    lines.append("## Verified technologies")
    lines.append("")
    if project.get("technologies"):
        lines.append(", ".join(project["technologies"]))
    else:
        lines.append("_None verified._")
    lines.append("")
    if metrics:
        lines.append("## Popularity indicators")
        lines.append("")
        for snap in metrics:
            captured = snap["captured_at"]
            stars = snap.get("stars")
            forks = snap.get("forks")
            parts = []
            if stars is not None:
                parts.append(f"{stars} stars")
            if forks is not None:
                parts.append(f"{forks} forks")
            summary = ", ".join(parts) if parts else "no metrics captured"
            lines.append(f"- {summary} (captured {captured}, source: {snap['source_url']})")
        lines.append("")
    lines.append("## Sources")
    lines.append("")
    for ev in evidence:
        lines.append(f"- [{ev['reliability']}] {ev['claim']} — {ev['url']}")
    if not evidence:
        lines.append("- _No evidence recorded._")
    lines.append("")
    if project.get("limitations"):
        lines.append("## Known limitations")
        lines.append("")
        for lim in project["limitations"]:
            lines.append(f"- {lim}")
        lines.append("")
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- Project ID: `{project['id']}`")
    lines.append(f"- First seen: {project['first_seen']}")
    lines.append(f"- Last checked: {project['last_checked']}")
    lines.append("")
    return "\n".join(lines)


def guide_record_id(project_id: str, guide_type: str) -> str:
    return f"guide-{project_id}-{slugify(guide_type)}"


def overview_path(project_id: str) -> str:
    return f"guides/overviews/{project_id}.md"


def write_if_changed(path: Path, content: str) -> bool:
    """Write content only when different. Returns True if written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True
