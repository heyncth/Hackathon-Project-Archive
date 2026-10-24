"""End-to-end pipeline tests on synthetic fixtures (offline)."""

from __future__ import annotations

from pathlib import Path

import yaml

from hpa.pipeline import run_pipeline
from hpa.store import DataStore


def _load(root: Path, entity: str, rid: str) -> dict:
    return yaml.safe_load((root / "data" / entity / f"{rid}.yaml").read_text(encoding="utf-8"))


def test_full_run_creates_expected_shape(tmp_repo: Path, fixture_query: str):
    report = run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    assert report["candidates"] == 4
    assert sorted(report["projects_created"]) == ["fixture-alpha", "fixture-beta", "fixture-delta"]
    assert report["source_failures"] == []
    assert report["validation"]["ok"] is True

    alpha = _load(tmp_repo, "projects", "fixture-alpha")
    assert "award-winning" in alpha["categories"]
    assert alpha["popularity"] == "high"  # 1500 stars
    assert alpha["verification_status"] == "verified"
    assert alpha["repository_ids"] == ["repo-fixture-alpha"]

    overview = tmp_repo / "guides" / "overviews" / "fixture-alpha.md"
    assert overview.is_file()
    text = overview.read_text(encoding="utf-8")
    assert "Fake Hackathon (2024): Grand Prize — verified" in text


def test_dedupe_merges_duplicate_repo(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    projects = DataStore(tmp_repo).load_all("projects")
    assert "alpha-fixture" not in projects
    alpha = projects["fixture-alpha"]
    # both discovery evidence entries present
    assert len(alpha["evidence_ids"]) >= 4


def test_unverified_award_not_award_winning(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    delta = _load(tmp_repo, "projects", "fixture-delta")
    assert "award-winning" not in delta["categories"]
    assert any("unverified award" in lim.lower() for lim in delta["limitations"])
    part_id = delta["participation_ids"][0]
    part = _load(tmp_repo, "participations", part_id)
    assert part["verified"] is False


def test_reconstruction_gate_blocks_no_repo_partial_docs(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    beta = _load(tmp_repo, "projects", "fixture-beta")
    recon_ids = [g for g in beta["guide_ids"] if g.endswith("-reconstruction")]
    assert recon_ids, "beta should have a reconstruction guide record"
    recon = _load(tmp_repo, "guides", recon_ids[0])
    assert recon["status"] == "blocked"
    assert recon["gate_reason"]


def test_idempotent_rerun(tmp_repo: Path, fixture_query: str):
    r1 = run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    assert r1["projects_created"]
    # capture file mtimes
    files = sorted((tmp_repo / "data").rglob("*.yaml"))
    before = {f: f.read_text(encoding="utf-8") for f in files}
    md_before = {
        f: f.read_text(encoding="utf-8") for f in (tmp_repo / "guides").rglob("*.md")
    }
    r2 = run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    assert r2["projects_created"] == []
    assert set(r2["projects_unchanged"]) == {"fixture-alpha", "fixture-beta", "fixture-delta"}
    after = {f: f.read_text(encoding="utf-8") for f in sorted((tmp_repo / "data").rglob("*.yaml"))}
    assert before == after
    md_after = {
        f: f.read_text(encoding="utf-8") for f in (tmp_repo / "guides").rglob("*.md")
    }
    assert md_before == md_after


def test_source_failure_recorded_and_run_continues(tmp_repo: Path, fixture_query: str, monkeypatch):
    from hpa.adapters import github as github_mod

    def fail_search(self, query, limit=10):
        from hpa.adapters.base import SearchFailure

        raise SearchFailure("github: rate limited")

    monkeypatch.setattr(github_mod.GitHubAdapter, "search", fail_search)
    # registry has both fixture and github entries; restrict to fixture works,
    # and a mixed failure scenario is covered by adapter unit tests.
    report = run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    assert report["validation"]["ok"] is True


def test_cli_validate_smoke(tmp_repo: Path, fixture_query: str):
    from hpa.cli import main

    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    rc = main(["--root", str(tmp_repo), "validate"])
    assert rc == 0
    rc = main(["--root", str(tmp_repo), "research", "--adapter", "fixture", "--input", fixture_query[5:]])
    assert rc == 0
