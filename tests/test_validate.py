"""Validation tests: good data passes; broken data fails with useful errors."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from hpa.pipeline import run_pipeline
from hpa.store import DataStore
from hpa.validate import validate_datastore

from conftest import FIXTURES, REPO_ROOT


def _write_entity(root: Path, entity: str, record: dict) -> None:
    directory = root / "data" / entity
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{record['id']}.yaml").write_text(
        yaml.safe_dump(record, sort_keys=True), encoding="utf-8"
    )


def test_repo_seed_data_validates():
    """The checked-in seed data under data/ must validate cleanly."""
    store = DataStore(REPO_ROOT)
    report = validate_datastore(store)
    assert report.ok, report.errors


def test_pipeline_output_validates(tmp_repo: Path, fixture_query: str):
    report = run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    assert report["validation"]["ok"] is True
    assert "fixture-alpha" in report["projects_created"]
    # dedupe: Alpha Fixture merges into fixture-alpha
    assert "alpha-fixture" not in report["projects_created"]
    assert len(report["projects_created"]) == 3  # alpha, beta, delta


def test_broken_reference_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    proj_path = tmp_repo / "data" / "projects" / "fixture-beta.yaml"
    proj = yaml.safe_load(proj_path.read_text(encoding="utf-8"))
    proj["evidence_ids"] = ["ev-does-not-exist"]
    proj_path.write_text(yaml.safe_dump(proj, sort_keys=True), encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert not report.ok
    assert any("ev-does-not-exist" in e for e in report.errors)


def test_award_winning_without_verified_participation_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    proj_path = tmp_repo / "data" / "projects" / "fixture-beta.yaml"
    proj = yaml.safe_load(proj_path.read_text(encoding="utf-8"))
    proj["categories"] = ["award-winning", "community-notable"]
    proj_path.write_text(yaml.safe_dump(proj, sort_keys=True), encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert any("award-winning without a verified award participation" in e for e in report.errors)


def test_popularity_inconsistent_with_stars_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    proj_path = tmp_repo / "data" / "projects" / "fixture-alpha.yaml"
    proj = yaml.safe_load(proj_path.read_text(encoding="utf-8"))
    proj["popularity"] = "limited"  # stars are 1500 -> high
    proj_path.write_text(yaml.safe_dump(proj, sort_keys=True), encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert any("inconsistent with 1500 stars" in e for e in report.errors)


def test_schema_violation_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    proj_path = tmp_repo / "data" / "projects" / "fixture-beta.yaml"
    proj = yaml.safe_load(proj_path.read_text(encoding="utf-8"))
    proj["bogus_field"] = "not allowed"
    proj_path.write_text(yaml.safe_dump(proj, sort_keys=True), encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert any("bogus_field" in e or "Additional properties" in e for e in report.errors)


def test_published_guide_missing_file_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    guide_path = tmp_repo / "data" / "guides" / "guide-fixture-alpha-overview.yaml"
    guide = yaml.safe_load(guide_path.read_text(encoding="utf-8"))
    (tmp_repo / guide["path"]).unlink()
    report = validate_datastore(DataStore(tmp_repo))
    assert any("file missing" in e for e in report.errors)


def test_markdown_out_of_sync_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    md_path = tmp_repo / "guides" / "overviews" / "fixture-alpha.md"
    md_path.write_text(md_path.read_text(encoding="utf-8") + "\nmanual edit\n", encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert any("out of sync" in e for e in report.errors)


def test_guide_blocked_without_reason_fails(tmp_repo: Path, fixture_query: str):
    run_pipeline(tmp_repo, "fixture", fixture_query, limit=10)
    guide_path = tmp_repo / "data" / "guides" / "guide-fixture-delta-overview.yaml"
    guide = yaml.safe_load(guide_path.read_text(encoding="utf-8"))
    guide["status"] = "blocked"
    guide["gate_reason"] = None
    guide_path.write_text(yaml.safe_dump(guide, sort_keys=True), encoding="utf-8")
    report = validate_datastore(DataStore(tmp_repo))
    assert any("blocked without gate_reason" in e for e in report.errors)
