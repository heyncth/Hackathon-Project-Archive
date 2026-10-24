from hpa.dedupe import content_equal_ignoring_timestamps, find_match, merge_project


def _proj(pid="p1", name="Alpha", **over):
    base = {
        "id": pid,
        "name": name,
        "description": "d",
        "categories": ["community-notable"],
        "tags": [],
        "status": "unknown",
        "repository_ids": [],
        "official_url": None,
        "demo_url": None,
        "participation_ids": [],
        "technologies": [],
        "evidence_ids": [],
        "metrics_ids": [],
        "popularity": "unknown",
        "documentation_quality": "unknown",
        "reproducibility": "not-assessed",
        "verification_status": "unverified",
        "educational_value": "unknown",
        "guide_ids": [],
        "first_seen": "2026-01-01T00:00:00Z",
        "last_checked": "2026-01-01T00:00:00Z",
        "limitations": [],
        "notes": None,
    }
    base.update(over)
    return base


def test_find_match_by_repo_url():
    projects = {"p1": _proj()}
    repos = {"repo-p1": {"id": "repo-p1", "project_id": "p1", "url": "https://github.com/a/b"}}
    incoming = _proj(pid="other", name="Different")
    assert find_match(incoming, "https://github.com/A/B/", projects, repos) == "p1"


def test_find_match_by_name_slug():
    projects = {"p1": _proj(name="Fixture Alpha")}
    assert find_match(_proj(pid="x", name="fixture  alpha"), None, projects, {}) == "p1"


def test_find_match_none():
    assert find_match(_proj(), "https://github.com/none/none", {}, {}) is None


def test_merge_preserves_union_of_ids_and_first_seen():
    existing = _proj(evidence_ids=["ev-a"], tags=["x"], first_seen="2025-01-01T00:00:00Z")
    incoming = _proj(pid="p1", evidence_ids=["ev-b"], tags=["y"], first_seen="2026-01-01T00:00:00Z")
    merged = merge_project(existing, incoming, "2026-06-01T00:00:00Z")
    assert merged["evidence_ids"] == ["ev-a", "ev-b"]
    assert merged["tags"] == ["x", "y"]
    assert merged["first_seen"] == "2025-01-01T00:00:00Z"
    assert merged["last_checked"] == "2026-06-01T00:00:00Z"


def test_merge_fills_missing_description():
    existing = _proj(description=None)
    incoming = _proj(description="new desc")
    merged = merge_project(existing, incoming, "2026-06-01T00:00:00Z")
    assert merged["description"] == "new desc"


def test_content_equal_ignoring_timestamps():
    a = _proj()
    b = _proj(last_checked="2027-01-01T00:00:00Z")
    assert content_equal_ignoring_timestamps(a, b)
    b["name"] = "changed"
    assert not content_equal_ignoring_timestamps(a, b)
