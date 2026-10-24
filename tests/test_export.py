"""Hot-score and JSON export tests."""

from __future__ import annotations

import textwrap

from archive.export import export_projects, hot_score
from helpers import VALID_PROJECT, load, make_repo


def _repo(tmp_path, projects: dict[str, str]):
    make_repo(tmp_path, projects)
    return load(tmp_path)


def test_empty_record_scores_zero():
    assert hot_score({}) == 0


def test_award_adds_twenty():
    assert hot_score({"event": {"name": "Quiet Meetup", "award": "Winner"}}) == 20


def test_source_and_demo_add_fifteen_each():
    assert hot_score({"links": {"source": "https://example.com/s"}}) == 15
    assert hot_score({"links": {"demo": "https://example.com/d"}}) == 15
    assert hot_score({"links": {"source": "https://example.com/s", "demo": "https://example.com/d"}}) == 30


def test_adoption_tags_add_fifteen():
    assert hot_score({"tags": ["used-by-millions"]}) == 15
    assert hot_score({"tags": ["became-startup"]}) == 15


def test_deep_dive_adds_twenty():
    assert hot_score({"deep_dive": True}) == 20


def test_rapid_event_adds_ten():
    assert hot_score({"event": {"name": "Startup Weekend Boulder"}}) == 10
    assert hot_score({"event": {"name": "Ludum Dare 47"}}) == 10
    assert hot_score({"event": {"name": "Google Summer of Code"}}) == 0


def test_recency_buckets():
    assert hot_score({"event": {"name": "Quiet Week", "year": 2024}}) == 5
    assert hot_score({"event": {"name": "Quiet Week", "year": 2020}}) == 3
    assert hot_score({"event": {"name": "Quiet Week", "year": 2015}}) == 1
    assert hot_score({"event": {"name": "Quiet Week", "year": 2014}}) == 0


def test_score_is_capped_at_one_hundred():
    record = {
        "event": {"name": "Ludum Dare 47", "year": 2025, "award": "Winner"},
        "links": {"source": "https://example.com/s", "demo": "https://example.com/d"},
        "tags": ["used-by-millions", "became-startup"],
        "deep_dive": True,
    }
    assert hot_score(record) == 100


def test_export_includes_hot_and_body(tmp_path):
    body = "## What it does\n\nA short note.\n"
    content = VALID_PROJECT.rstrip() + "\n\n" + body
    repo = _repo(tmp_path, {"example-project.md": content})
    entry = export_projects(repo)[0]
    assert entry["name"] == "Example Project"
    assert entry["hot"] == 48
    assert entry["body"].strip() == body.strip()


def test_export_does_not_mutate_source_data(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    entry = export_projects(repo)[0]
    assert "hot" in entry
    assert "hot" not in repo.projects[0].data
