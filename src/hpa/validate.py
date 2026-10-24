"""Automated validation: schemas, references, duplicates, labels, gates, markdown."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import jsonschema
import yaml

from hpa.gates import evaluate_gates
from hpa.ids import canonical_repo_url, slugify
from hpa.label import HIGH_STARS, MODERATE_STARS
from hpa.store import ENTITY_DIRS, SCHEMA_FILES, DataStore

VALID_CATEGORIES = {"award-winning", "community-notable"}
VALID_POPULARITY = {"high", "moderate", "limited", "unknown"}
VALID_DOC_QUALITY = {"strong", "partial", "limited", "unknown"}
VALID_REPRO = {"tested", "documented-not-tested", "not-assessed"}
VALID_VERIFICATION = {"verified", "partially-verified", "unverified", "disputed"}
VALID_EDU = {"high", "moderate", "low", "unknown"}


class ValidationReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings}


def _load_schemas(schemas_dir: Path) -> dict[str, Any]:
    schemas: dict[str, Any] = {}
    for entity, filename in SCHEMA_FILES.items():
        path = schemas_dir / filename
        schemas[entity] = json.loads(path.read_text(encoding="utf-8"))
    return schemas


def _valid_url(value: str | None) -> bool:
    if value is None:
        return True
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def validate_datastore(store: DataStore, check_markdown: bool = True) -> ValidationReport:
    report = ValidationReport()
    data = store.load_everything()
    schemas = _load_schemas(store.schemas_dir)

    # 1. YAML parsing + schema compliance
    for entity, records in data.items():
        schema = schemas[entity]
        validator = jsonschema.Draft202012Validator(schema)
        for rid, record in records.items():
            problems = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
            for err in problems:
                path = "/".join(str(p) for p in err.path)
                report.error(f"{entity}/{rid}: schema: {path}: {err.message}")
            # filename must match id
            if record.get("id") != rid:
                report.error(f"{entity}/{rid}: file name does not match record id {record.get('id')}")
            # URL syntax beyond schema format (schema format needs format checker)
            for url_field in ("url", "official_url", "demo_url", "source_url", "base_url"):
                if url_field in record and not _valid_url(record[url_field]):
                    report.error(f"{entity}/{rid}: invalid URL in {url_field}: {record[url_field]}")

    projects = data["projects"]
    repositories = data["repositories"]
    events = data["events"]
    participations = data["participations"]
    evidence = data["evidence"]
    metrics = data["metrics"]
    guides = data["guides"]

    # 2. Referential integrity
    for pid, proj in projects.items():
        for rid in proj.get("repository_ids", []):
            if rid not in repositories:
                report.error(f"projects/{pid}: unknown repository_ids entry {rid}")
        for part_id in proj.get("participation_ids", []):
            if part_id not in participations:
                report.error(f"projects/{pid}: unknown participation_ids entry {part_id}")
        for eid in proj.get("evidence_ids", []):
            if eid not in evidence:
                report.error(f"projects/{pid}: unknown evidence_ids entry {eid}")
        for mid in proj.get("metrics_ids", []):
            if mid not in metrics:
                report.error(f"projects/{pid}: unknown metrics_ids entry {mid}")
        for gid in proj.get("guide_ids", []):
            if gid not in guides:
                report.error(f"projects/{pid}: unknown guide_ids entry {gid}")
    for rid, repo in repositories.items():
        if repo["project_id"] not in projects:
            report.error(f"repositories/{rid}: unknown project_id {repo['project_id']}")
    for part_id, part in participations.items():
        if part["project_id"] not in projects:
            report.error(f"participations/{part_id}: unknown project_id {part['project_id']}")
        if part["event_id"] not in events:
            report.error(f"participations/{part_id}: unknown event_id {part['event_id']}")
        for eid in part.get("evidence_ids", []):
            if eid not in evidence:
                report.error(f"participations/{part_id}: unknown evidence_ids entry {eid}")
    for mid, snap in metrics.items():
        if snap["repository_id"] not in repositories:
            report.error(f"metrics/{mid}: unknown repository_id {snap['repository_id']}")
    for gid, guide in guides.items():
        if guide["project_id"] not in projects:
            report.error(f"guides/{gid}: unknown project_id {guide['project_id']}")
        for eid in guide.get("evidence_ids", []):
            if eid not in evidence:
                report.error(f"guides/{gid}: unknown evidence_ids entry {eid}")

    # 3. Duplicate repositories (same canonical URL owned by different ids)
    url_to_repo: dict[str, str] = {}
    for rid, repo in repositories.items():
        key = canonical_repo_url(repo["url"])
        if key in url_to_repo and url_to_repo[key] != rid:
            report.error(f"repositories/{rid}: duplicate URL with {url_to_repo[key]} ({key})")
        url_to_repo[key] = rid

    # 4. Duplicate participations (same project + event)
    seen_part: dict[tuple[str, str], str] = {}
    for part_id, part in participations.items():
        key = (part["project_id"], part["event_id"])
        if key in seen_part:
            report.error(
                f"participations/{part_id}: duplicate participation {seen_part[key]} "
                f"for project {key[0]} at event {key[1]}"
            )
        seen_part[key] = part_id

    # 5. Duplicate project names (slug collisions across different ids)
    name_map: dict[str, str] = {}
    for pid, proj in projects.items():
        key = slugify(proj["name"])
        if key in name_map and name_map[key] != pid:
            report.error(f"projects/{pid}: duplicate project name slug with {name_map[key]}")
        name_map[key] = pid

    # 6. Qualitative label validity + metrics consistency
    for pid, proj in projects.items():
        if not proj["categories"]:
            report.error(f"projects/{pid}: categories must not be empty")
        if not set(proj["categories"]) <= VALID_CATEGORIES:
            report.error(f"projects/{pid}: invalid category value")
        if proj["popularity"] not in VALID_POPULARITY:
            report.error(f"projects/{pid}: invalid popularity label")
        if proj["documentation_quality"] not in VALID_DOC_QUALITY:
            report.error(f"projects/{pid}: invalid documentation_quality label")
        if proj["reproducibility"] not in VALID_REPRO:
            report.error(f"projects/{pid}: invalid reproducibility label")
        if proj["verification_status"] not in VALID_VERIFICATION:
            report.error(f"projects/{pid}: invalid verification_status label")
        if proj["educational_value"] not in VALID_EDU:
            report.error(f"projects/{pid}: invalid educational_value label")
        if proj["reproducibility"] == "tested":
            report.warn(
                f"projects/{pid}: reproducibility 'tested' — ensure a recorded test exists; "
                "schema cannot verify this"
            )
        # popularity must match star thresholds when metrics exist
        stars = [
            metrics[m]["stars"]
            for m in proj.get("metrics_ids", [])
            if m in metrics and metrics[m].get("stars") is not None
        ]
        if stars:
            top = max(stars)
            expected = "high" if top >= HIGH_STARS else "moderate" if top >= MODERATE_STARS else "limited"
            if proj["popularity"] != expected:
                report.error(
                    f"projects/{pid}: popularity '{proj['popularity']}' inconsistent with "
                    f"{top} stars (expected '{expected}')"
                )
        # award-winning requires a verified award participation
        if "award-winning" in proj["categories"]:
            parts = [participations[p] for p in proj.get("participation_ids", []) if p in participations]
            if not any(p.get("award_name") and p.get("verified") for p in parts):
                report.error(f"projects/{pid}: award-winning without a verified award participation")
        if not proj.get("evidence_ids"):
            report.warn(f"projects/{pid}: no evidence records")

    # 7. Guide publication gates
    for gid, guide in guides.items():
        proj = projects.get(guide["project_id"])
        if proj is None:
            continue
        repos = [
            repositories[r]
            for r in proj.get("repository_ids", [])
            if r in repositories
        ]
        gates = evaluate_gates(proj, repos)
        gate = gates.get(guide["type"])
        if guide["status"] == "published" and gate and not gate["passed"]:
            report.error(
                f"guides/{gid}: published but fails {guide['type']} gate: {gate['reason']}"
            )
        if guide["status"] == "blocked" and not guide.get("gate_reason"):
            report.error(f"guides/{gid}: blocked without gate_reason")
        # guide path must exist on disk for published guides
        if guide["status"] == "published":
            path = store.root / guide["path"]
            if not path.is_file():
                report.error(f"guides/{gid}: published but file missing: {guide['path']}")

    # 8. Markdown consistency for generated overviews
    if check_markdown:
        from hpa.generate import overview_markdown

        for gid, guide in guides.items():
            if guide["type"] != "overview" or guide["status"] != "published":
                continue
            proj = projects[guide["project_id"]]
            repos = [repositories[r] for r in proj.get("repository_ids", []) if r in repositories]
            parts = [participations[p] for p in proj.get("participation_ids", []) if p in participations]
            evs = [evidence[e] for e in proj.get("evidence_ids", []) if e in evidence]
            mets = [metrics[m] for m in proj.get("metrics_ids", []) if m in metrics]
            expected = overview_markdown(proj, repos, parts, events, evs, mets)
            path = store.root / guide["path"]
            if path.is_file() and path.read_text(encoding="utf-8") != expected:
                report.error(
                    f"guides/{gid}: markdown out of sync with structured data; "
                    "run `python -m hpa generate`"
                )

    # 9. Orphan entity checks (records not referenced by any project)
    referenced_repos = {r for p in projects.values() for r in p.get("repository_ids", [])}
    for rid in repositories:
        if rid not in referenced_repos:
            report.warn(f"repositories/{rid}: not referenced by any project")
    referenced_parts = {p for proj in projects.values() for p in proj.get("participation_ids", [])}
    for part_id in participations:
        if part_id not in referenced_parts:
            report.warn(f"participations/{part_id}: not referenced by any project")
    referenced_ev = {e for proj in projects.values() for e in proj.get("evidence_ids", [])}
    for proj in projects.values():
        for part_id in proj.get("participation_ids", []):
            if part_id in participations:
                referenced_ev.update(participations[part_id].get("evidence_ids", []))
    for eid in evidence:
        if eid not in referenced_ev:
            report.warn(f"evidence/{eid}: not referenced by any project or participation")

    return report


def check_links(store: DataStore, timeout: float = 10.0) -> dict[str, Any]:
    """Optional network link check. Never deletes records.

    Distinguishes: ok, missing (404), restricted (401/403), rate-limited (429),
    redirect, network-error.
    """
    import requests

    results: list[dict[str, Any]] = []
    data = store.load_everything()
    seen: set[str] = set()
    urls: list[tuple[str, str]] = []
    for entity, records in data.items():
        for rid, record in records.items():
            for field in ("url", "official_url", "demo_url", "source_url"):
                value = record.get(field)
                if isinstance(value, str) and value.startswith("http") and value not in seen:
                    seen.add(value)
                    urls.append((f"{entity}/{rid}:{field}", value))

    for label, url in urls:
        entry: dict[str, Any] = {"ref": label, "url": url}
        try:
            resp = requests.head(
                url,
                allow_redirects=False,
                timeout=timeout,
                headers={"User-Agent": "hackathon-project-archive-linkcheck"},
            )
            code = resp.status_code
            if code == 404 or code == 410:
                entry["status"] = "missing"
            elif code in (401, 403):
                entry["status"] = "restricted"
            elif code == 429:
                entry["status"] = "rate-limited"
            elif 300 <= code < 400:
                entry["status"] = "redirect"
                entry["location"] = resp.headers.get("Location")
            elif 200 <= code < 300:
                entry["status"] = "ok"
            else:
                entry["status"] = f"http-{code}"
        except requests.RequestException as exc:
            entry["status"] = "network-error"
            entry["error"] = str(exc)
        results.append(entry)
    return {"checked": len(results), "results": results}
