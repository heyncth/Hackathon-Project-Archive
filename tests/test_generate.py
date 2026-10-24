from hpa.generate import overview_markdown, write_if_changed


def _project(**over):
    base = {
        "id": "fixture-alpha",
        "name": "Fixture Alpha",
        "description": "A fixture.",
        "categories": ["award-winning", "community-notable"],
        "verification_status": "verified",
        "popularity": "high",
        "documentation_quality": "strong",
        "reproducibility": "documented-not-tested",
        "educational_value": "moderate",
        "official_url": "https://example.invalid/alpha",
        "demo_url": None,
        "technologies": ["Python"],
        "evidence_ids": ["ev1"],
        "limitations": ["Demo unavailable."],
        "first_seen": "2026-01-01T00:00:00Z",
        "last_checked": "2026-01-02T00:00:00Z",
    }
    base.update(over)
    return base


REPOS = [{"id": "repo-1", "url": "https://github.com/o/a", "relationship": "original"}]
PARTS = [
    {
        "id": "part1",
        "event_id": "event-x-2024",
        "award_name": "Grand Prize",
        "verified": True,
    }
]
EVENTS = {"event-x-2024": {"id": "event-x-2024", "name": "Fake Jam", "year": 2024}}
EVIDENCE = [
    {
        "id": "ev1",
        "claim": "Won grand prize.",
        "url": "https://example.invalid/results",
        "reliability": "primary",
    }
]
METRICS = [
    {
        "id": "m1",
        "stars": 1500,
        "forks": 10,
        "captured_at": "2026-01-01T00:00:00Z",
        "source_url": "https://api.github.com/o/a",
    }
]


def test_overview_contains_core_sections():
    md = overview_markdown(_project(), REPOS, PARTS, EVENTS, EVIDENCE, METRICS)
    assert md.startswith("# Fixture Alpha")
    assert "Fake Jam (2024): Grand Prize — verified" in md
    assert "1500 stars" in md
    assert "https://github.com/o/a" in md
    assert "## Known limitations" in md


def test_overview_deterministic():
    a = overview_markdown(_project(), REPOS, PARTS, EVENTS, EVIDENCE, METRICS)
    b = overview_markdown(_project(), REPOS, PARTS, EVENTS, EVIDENCE, METRICS)
    assert a == b


def test_overview_handles_missing_everything():
    md = overview_markdown(
        _project(
            description=None,
            official_url=None,
            technologies=[],
            limitations=[],
        ),
        [],
        [],
        {},
        [],
        [],
    )
    assert "_No description available._" in md
    assert "_No public links recorded._" in md
    assert "_No event participation recorded._" in md


def test_write_if_changed(tmp_path):
    path = tmp_path / "sub" / "file.md"
    assert write_if_changed(path, "hello") is True
    assert write_if_changed(path, "hello") is False
    assert write_if_changed(path, "hello2") is True
