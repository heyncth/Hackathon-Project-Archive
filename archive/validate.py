"""Validation rules for project records."""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from urllib.parse import urlparse

from .loader import ProjectDoc, RepoData

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URL_SCHEMES = {"http", "https"}
ALLOWED_LINK_KEYS = {"official", "source", "demo", "video"}
ALLOWED_TOP_LEVEL = {
    "id",
    "name",
    "description",
    "domain",
    "tags",
    "event",
    "links",
    "authors",
    "evidence",
    "notes",
    "verified_at",
}
ALLOWED_EVENT_KEYS = {"name", "organizer", "year", "award"}
ALLOWED_EVIDENCE_KEYS = {"url", "supports"}


def _valid_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in URL_SCHEMES and bool(parsed.netloc)


def _check_str(data: dict, key: str, where: str, errors: list[str], required: bool = False) -> None:
    if key not in data:
        if required:
            errors.append(f"{where}: missing required field '{key}'")
        return
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}: field '{key}' must be a non-empty string")


def validate_project(doc: ProjectDoc, repo: RepoData) -> list[str]:
    errors: list[str] = []
    rel = doc.path.relative_to(repo.root).as_posix()
    where = rel

    if doc.parse_error:
        return [f"{where}: {doc.parse_error}"]

    data = doc.data or {}

    unknown = sorted(set(data) - ALLOWED_TOP_LEVEL)
    for key in unknown:
        errors.append(f"{where}: unknown field '{key}'")

    for key in ("id", "name", "description", "domain"):
        _check_str(data, key, where, errors, required=True)

    pid = data.get("id")
    if isinstance(pid, str) and pid:
        if not ID_RE.match(pid):
            errors.append(f"{where}: field 'id' must be kebab-case, got '{pid}'")
        if pid != doc.path.stem:
            errors.append(f"{where}: field 'id' '{pid}' does not match filename '{doc.path.stem}'")

    domain = data.get("domain")
    if isinstance(domain, str) and domain:
        allowed = {d["id"] for d in repo.taxonomy.get("domains", [])}
        if domain not in allowed:
            errors.append(f"{where}: domain '{domain}' not in taxonomy (allowed: {sorted(allowed)})")

    tags = data.get("tags")
    if tags is not None:
        pattern = repo.taxonomy.get("tag_pattern", "^[a-z0-9]+(-[a-z0-9]+)*$")
        max_tags = repo.taxonomy.get("max_tags_per_project", 8)
        if not isinstance(tags, list):
            errors.append(f"{where}: field 'tags' must be a list")
        else:
            if len(tags) > max_tags:
                errors.append(f"{where}: too many tags ({len(tags)} > {max_tags})")
            if len(tags) != len(set(tags)):
                errors.append(f"{where}: duplicate tags")
            for tag in tags:
                if not isinstance(tag, str) or not re.match(pattern, tag):
                    errors.append(f"{where}: invalid tag {tag!r} (must match {pattern})")

    event = data.get("event")
    if event is not None:
        if not isinstance(event, dict):
            errors.append(f"{where}: field 'event' must be a mapping")
        else:
            for key in sorted(set(event) - ALLOWED_EVENT_KEYS):
                errors.append(f"{where}: unknown event key '{key}'")
            _check_str(event, "name", f"{where}: event", errors, required=True)
            year = event.get("year")
            if year is not None and (not isinstance(year, int) or not 1900 <= year <= 2100):
                errors.append(f"{where}: event.year must be an integer 1900-2100, got {year!r}")
            for key in ("organizer", "award"):
                _check_str(event, key, f"{where}: event", errors)

    links = data.get("links")
    if links is not None:
        if not isinstance(links, dict):
            errors.append(f"{where}: field 'links' must be a mapping")
        else:
            for key in sorted(set(links) - ALLOWED_LINK_KEYS):
                errors.append(f"{where}: unknown link key '{key}'")
            for key, value in links.items():
                if not isinstance(value, str) or not _valid_url(value):
                    errors.append(f"{where}: link '{key}' is not a valid http(s) URL: {value!r}")

    authors = data.get("authors")
    if authors is not None:
        if not isinstance(authors, list) or any(not isinstance(a, str) or not a.strip() for a in authors):
            errors.append(f"{where}: field 'authors' must be a list of non-empty strings")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{where}: field 'evidence' must be a non-empty list")
    else:
        for i, item in enumerate(evidence):
            ewhere = f"{where}: evidence[{i}]"
            if not isinstance(item, dict):
                errors.append(f"{ewhere}: must be a mapping")
                continue
            for key in sorted(set(item) - ALLOWED_EVIDENCE_KEYS):
                errors.append(f"{ewhere}: unknown key '{key}'")
            url = item.get("url")
            if not isinstance(url, str) or not _valid_url(url):
                errors.append(f"{ewhere}: 'url' must be a valid http(s) URL, got {url!r}")
            supports = item.get("supports")
            if supports is not None and (not isinstance(supports, str) or not supports.strip()):
                errors.append(f"{ewhere}: 'supports' must be a non-empty string")

    notes = data.get("notes")
    if notes is not None and (not isinstance(notes, str) or not notes.strip()):
        errors.append(f"{where}: field 'notes' must be a non-empty string")

    verified_at = data.get("verified_at")
    if verified_at is not None:
        if isinstance(verified_at, datetime.date):
            pass
        elif isinstance(verified_at, str):
            try:
                datetime.date.fromisoformat(verified_at)
            except ValueError:
                errors.append(f"{where}: field 'verified_at' must be ISO date YYYY-MM-DD, got {verified_at!r}")
        else:
            errors.append(f"{where}: field 'verified_at' must be ISO date YYYY-MM-DD, got {verified_at!r}")

    return errors


def validate_repo(repo: RepoData) -> list[str]:
    errors: list[str] = []
    for path, err in repo.load_errors:
        errors.append(f"{path.relative_to(repo.root).as_posix()}: {err}")

    seen_ids: dict[str, Path] = {}
    seen_official: dict[str, str] = {}
    seen_source: dict[str, str] = {}

    for doc in repo.projects:
        errors.extend(validate_project(doc, repo))
        if not doc.data:
            continue
        pid = doc.data.get("id")
        if isinstance(pid, str):
            if pid in seen_ids:
                errors.append(
                    f"{doc.path.relative_to(repo.root).as_posix()}: duplicate id '{pid}' "
                    f"(also in {seen_ids[pid].relative_to(repo.root).as_posix()})"
                )
            else:
                seen_ids[pid] = doc.path
        links = doc.data.get("links")
        if isinstance(links, dict):
            rel = doc.path.relative_to(repo.root).as_posix()
            official = links.get("official")
            if isinstance(official, str):
                norm = official.rstrip("/")
                if norm in seen_official:
                    errors.append(f"{rel}: duplicate official link '{official}' (also in {seen_official[norm]})")
                else:
                    seen_official[norm] = rel
            source = links.get("source")
            if isinstance(source, str):
                norm = source.rstrip("/")
                if norm in seen_source:
                    errors.append(f"{rel}: duplicate source link '{source}' (also in {seen_source[norm]})")
                else:
                    seen_source[norm] = rel

    return errors
