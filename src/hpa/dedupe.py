"""Duplicate detection and record merging."""

from __future__ import annotations

from typing import Any

from hpa.ids import canonical_repo_url, slugify


def project_identity_keys(project: dict[str, Any], repo_urls: list[str]) -> set[str]:
    keys = {f"name:{slugify(project['name'])}"}
    for url in repo_urls:
        keys.add(f"repo:{canonical_repo_url(url)}")
    return keys


def find_match(
    candidate_project: dict[str, Any],
    candidate_repo_url: str | None,
    existing_projects: dict[str, dict[str, Any]],
    repositories: dict[str, dict[str, Any]],
) -> str | None:
    """Return existing project id matching this candidate, or None."""
    if candidate_repo_url:
        target = canonical_repo_url(candidate_repo_url)
        for repo in repositories.values():
            if canonical_repo_url(repo["url"]) == target:
                return repo["project_id"]
    name_key = slugify(candidate_project["name"])
    for pid, proj in existing_projects.items():
        if slugify(proj["name"]) == name_key:
            return pid
    return None


def merge_project(
    existing: dict[str, Any],
    incoming: dict[str, Any],
    run_timestamp: str,
) -> dict[str, Any]:
    """Merge incoming candidate data into an existing project record.

    Never removes existing evidence. Adds new ids. Keeps the earliest
    first_seen. Updates last_checked only when content changed.
    """
    merged = dict(existing)
    for field in ("repository_ids", "participation_ids", "evidence_ids", "metrics_ids", "guide_ids"):
        merged[field] = sorted(set(existing.get(field, [])) | set(incoming.get(field, [])))
    for field in ("tags", "technologies", "limitations"):
        merged[field] = sorted(set(existing.get(field, []) or []) | set(incoming.get(field, []) or []))
    for field in ("categories",):
        merged[field] = sorted(set(existing.get(field, [])) | set(incoming.get(field, [])))
    if not merged.get("description") and incoming.get("description"):
        merged["description"] = incoming["description"]
    if not merged.get("official_url") and incoming.get("official_url"):
        merged["official_url"] = incoming["official_url"]
    if not merged.get("demo_url") and incoming.get("demo_url"):
        merged["demo_url"] = incoming["demo_url"]
    if merged.get("status") == "unknown" and incoming.get("status") != "unknown":
        merged["status"] = incoming["status"]
    # keep the stronger (later in list order) verification placeholder; verify.py re-runs later
    merged["first_seen"] = min(existing.get("first_seen", run_timestamp), incoming.get("first_seen", run_timestamp))
    merged["last_checked"] = run_timestamp
    return merged


def content_equal_ignoring_timestamps(a: dict[str, Any], b: dict[str, Any]) -> bool:
    ignore = {"last_checked", "first_seen"}
    keys = (set(a) | set(b)) - ignore
    return all(a.get(k) == b.get(k) for k in keys)
