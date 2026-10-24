"""End-to-end research pipeline orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hpa.adapters import RawCandidate, SearchAdapter, SearchFailure, build_adapter
from hpa.dedupe import content_equal_ignoring_timestamps, find_match, merge_project
from hpa.gates import evaluate_gates
from hpa.generate import (
    guide_record_id,
    overview_markdown,
    overview_path,
    write_if_changed,
)
from hpa.label import apply_labels
from hpa.normalize import normalize_candidate, utcnow_iso
from hpa.registry import load_registry, sources_for_adapter
from hpa.store import DataStore
from hpa.validate import validate_datastore
from hpa.verify import verify_project


class PipelineRun:
    def __init__(self, root: Path, run_timestamp: str | None = None):
        self.root = Path(root)
        self.store = DataStore(self.root)
        self.ts = run_timestamp or utcnow_iso()
        self.report: dict[str, Any] = {
            "started_at": self.ts,
            "sources_searched": [],
            "source_failures": [],
            "candidates": 0,
            "projects_created": [],
            "projects_updated": [],
            "projects_unchanged": [],
            "guides_written": [],
            "guides_blocked": [],
            "validation": None,
        }

    # -- discovery ---------------------------------------------------------

    def discover(self, adapter_name: str, query: str, limit: int, source_id: str | None = None) -> list[RawCandidate]:
        sources = load_registry(self.root)
        chosen = [s for s in sources_for_adapter(sources, adapter_name) if source_id in (None, s["id"])]
        if not chosen:
            self.report["source_failures"].append(
                {"source": adapter_name, "error": "no registry entry for this adapter"}
            )
            return []
        candidates: list[RawCandidate] = []
        for source in chosen:
            adapter: SearchAdapter = build_adapter(adapter_name, source)
            try:
                found = adapter.search(query, limit=limit)
                candidates.extend(found)
                self.report["sources_searched"].append(
                    {"source": source["id"], "adapter": adapter_name, "results": len(found)}
                )
            except SearchFailure as exc:
                # Inaccessible source: record and continue. Not evidence of absence.
                self.report["source_failures"].append({"source": source["id"], "error": str(exc)})
        return candidates

    # -- processing --------------------------------------------------------

    def process(self, candidates: list[RawCandidate]) -> None:
        self.report["candidates"] = len(candidates)
        projects = self.store.load_all("projects")
        repositories = self.store.load_all("repositories")
        events = self.store.load_all("events")
        participations = self.store.load_all("participations")
        evidence = self.store.load_all("evidence")
        metrics = self.store.load_all("metrics")
        guides = self.store.load_all("guides")

        for candidate in candidates:
            bundle = normalize_candidate(candidate, self.ts)
            incoming_project = bundle["project"]
            match = find_match(
                incoming_project,
                bundle["repository"]["url"] if bundle["repository"] else None,
                projects,
                repositories,
            )
            created = match is None
            if match is None:
                pid = incoming_project["id"]
                # avoid slug collision with a different project name
                while pid in projects:
                    pid = f"{pid}-2"
                incoming_project["id"] = pid
                if bundle["repository"]:
                    bundle["repository"]["project_id"] = pid
                    bundle["repository"]["id"] = f"repo-{pid}"
                    incoming_project["repository_ids"] = [bundle["repository"]["id"]]
                if bundle["metrics"]:
                    bundle["metrics"]["repository_id"] = bundle["repository"]["id"]
                    bundle["metrics"]["id"] = f"metrics-{bundle['repository']['id']}"
                    incoming_project["metrics_ids"] = [bundle["metrics"]["id"]]
                if bundle["event"]:
                    events[bundle["event"]["id"]] = bundle["event"]
                    self.store.save("events", bundle["event"])
                if bundle["participation"]:
                    bundle["participation"]["project_id"] = pid
                    bundle["participation"]["id"] = f"part-{pid}-{bundle['event']['id']}"
                    incoming_project["participation_ids"] = [bundle["participation"]["id"]]
                    participations[bundle["participation"]["id"]] = bundle["participation"]
                    self.store.save("participations", bundle["participation"])
                if bundle["repository"]:
                    repositories[bundle["repository"]["id"]] = bundle["repository"]
                    self.store.save("repositories", bundle["repository"])
                if bundle["metrics"]:
                    metrics[bundle["metrics"]["id"]] = bundle["metrics"]
                    self.store.save("metrics", bundle["metrics"])
                for ev in bundle["evidence"]:
                    evidence[ev["id"]] = ev
                    self.store.save("evidence", ev)
                project = incoming_project
            else:
                pid = match
                existing = projects[pid]
                # remap incoming entity ids to the existing project id
                if bundle["event"]:
                    events.setdefault(bundle["event"]["id"], bundle["event"])
                    self.store.save("events", bundle["event"])
                if bundle["repository"]:
                    new_id = f"repo-{pid}"
                    bundle["repository"]["id"] = new_id
                    bundle["repository"]["project_id"] = pid
                    incoming_project["repository_ids"] = [new_id]
                    if bundle["metrics"]:
                        bundle["metrics"]["id"] = f"metrics-{new_id}"
                        bundle["metrics"]["repository_id"] = new_id
                        incoming_project["metrics_ids"] = [bundle["metrics"]["id"]]
                    existing_repo_ids = existing.get("repository_ids", [])
                    same = any(
                        repositories.get(rid, {}).get("url") == bundle["repository"]["url"]
                        for rid in existing_repo_ids
                    )
                    if not same:
                        bundle["repository"]["relationship"] = "related"
                        repositories[bundle["repository"]["id"]] = bundle["repository"]
                        self.store.save("repositories", bundle["repository"])
                    else:
                        bundle["repository"] = None
                        incoming_project["repository_ids"] = []
                        if bundle["metrics"]:
                            incoming_project["metrics_ids"] = []
                            bundle["metrics"] = None
                if bundle["metrics"] and bundle["repository"]:
                    metrics.setdefault(bundle["metrics"]["id"], bundle["metrics"])
                    self.store.save("metrics", bundle["metrics"])
                if bundle["participation"] and bundle["event"]:
                    new_part_id = f"part-{pid}-{bundle['event']['id']}"
                    bundle["participation"]["id"] = new_part_id
                    bundle["participation"]["project_id"] = pid
                    bundle["participation"]["event_id"] = bundle["event"]["id"]
                    incoming_project["participation_ids"] = [new_part_id]
                    participations.setdefault(new_part_id, bundle["participation"])
                    self.store.save("participations", bundle["participation"])
                for ev in bundle["evidence"]:
                    if ev["id"] not in evidence:
                        evidence[ev["id"]] = ev
                        self.store.save("evidence", ev)
                project = merge_project(existing, incoming_project, self.ts)

            # labels + verification (run on merged state)
            project_participations = [
                participations[part_id]
                for part_id in project.get("participation_ids", [])
                if part_id in participations
            ]
            project_metrics = [
                metrics[mid] for mid in project.get("metrics_ids", []) if mid in metrics
            ]
            project = apply_labels(project, project_participations, project_metrics)
            project["verification_status"] = verify_project(
                project, evidence, project_participations
            )

            # guide evaluation + overview generation
            project_repos = [
                repositories[rid] for rid in project.get("repository_ids", []) if rid in repositories
            ]
            gates = evaluate_gates(project, project_repos)
            project = self._apply_guides(project, gates, evidence, project_repos, project_participations, events, project_metrics)

            # idempotent save
            prev = projects.get(project["id"])
            if prev is None:
                self.store.save("projects", project)
                projects[project["id"]] = project
                self.report["projects_created"].append(project["id"])
            elif content_equal_ignoring_timestamps(prev, project):
                self.report["projects_unchanged"].append(project["id"])
            else:
                self.store.save("projects", project)
                projects[project["id"]] = project
                self.report["projects_updated"].append(project["id"])

    def _apply_guides(
        self,
        project: dict[str, Any],
        gates: dict[str, dict[str, Any]],
        evidence: dict[str, dict[str, Any]],
        repos: list[dict[str, Any]],
        parts: list[dict[str, Any]],
        events: dict[str, dict[str, Any]],
        metrics: list[dict[str, Any]],
    ) -> dict[str, Any]:
        guides = self.store.load_all("guides")
        guide_ids = set(project.get("guide_ids", []))

        overview = gates["overview"]
        gid = guide_record_id(project["id"], "overview")
        if overview["passed"]:
            md = overview_markdown(project, repos, parts, events,
                                   [evidence[e] for e in project["evidence_ids"] if e in evidence],
                                   metrics)
            rel = overview_path(project["id"])
            written = write_if_changed(self.root / rel, md)
            record = {
                "id": gid,
                "project_id": project["id"],
                "type": "overview",
                "path": rel,
                "status": "published",
                "gate_reason": None,
                "evidence_ids": sorted(project["evidence_ids"]),
                "generated_at": guides.get(gid, {}).get("generated_at", self.ts),
            }
            # only bump generated_at when file content changed
            if written:
                record["generated_at"] = self.ts
            self.store.save("guides", record)
            guides[gid] = record
            guide_ids.add(gid)
            if written:
                self.report["guides_written"].append(rel)
        else:
            record = guides.get(gid) or {
                "id": gid,
                "project_id": project["id"],
                "type": "overview",
                "path": overview_path(project["id"]),
                "status": "blocked",
                "gate_reason": overview["reason"],
                "evidence_ids": [],
                "generated_at": self.ts,
            }
            record["status"] = "blocked"
            record["gate_reason"] = overview["reason"]
            self.store.save("guides", record)
            guides[gid] = record
            guide_ids.add(gid)
            self.report["guides_blocked"].append({"guide": gid, "reason": overview["reason"]})

        # case-study / reconstruction: evaluate and record blocked reasons;
        # never auto-author deep guides (they require human research)
        for gtype in ("case-study", "reconstruction"):
            g = gates[gtype]
            gid = guide_record_id(project["id"], gtype)
            existing = guides.get(gid)
            if g["passed"]:
                if existing is None:
                    # gate passed but guide not yet authored: record as draft
                    record = {
                        "id": gid,
                        "project_id": project["id"],
                        "type": gtype,
                        "path": f"guides/{'case-studies' if gtype == 'case-study' else 'rebuild'}/{project['id']}.md",
                        "status": "draft",
                        "gate_reason": None,
                        "evidence_ids": sorted(project["evidence_ids"]),
                        "generated_at": self.ts,
                    }
                    self.store.save("guides", record)
                    guides[gid] = record
            else:
                record = existing or {
                    "id": gid,
                    "project_id": project["id"],
                    "type": gtype,
                    "path": f"guides/{'case-studies' if gtype == 'case-study' else 'rebuild'}/{project['id']}.md",
                    "status": "blocked",
                    "gate_reason": g["reason"],
                    "evidence_ids": [],
                    "generated_at": self.ts,
                }
                record["status"] = "blocked"
                record["gate_reason"] = g["reason"]
                self.store.save("guides", record)
                guides[gid] = record
            guide_ids.add(gid)

        project = dict(project)
        project["guide_ids"] = sorted(guide_ids)
        return project

    # -- validation --------------------------------------------------------

    def validate(self) -> dict[str, Any]:
        report = validate_datastore(self.store)
        self.report["validation"] = report.to_dict()
        return report.to_dict()


def run_pipeline(
    root: Path,
    adapter: str,
    query: str,
    limit: int = 10,
    source_id: str | None = None,
) -> dict[str, Any]:
    run = PipelineRun(root)
    candidates = run.discover(adapter, query, limit, source_id=source_id)
    run.process(candidates)
    run.validate()
    return run.report


def write_report(root: Path, report: dict[str, Any]) -> Path:
    path = Path(root) / "scripts" / "last-run-report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
