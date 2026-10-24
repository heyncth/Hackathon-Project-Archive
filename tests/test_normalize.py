from hpa.adapters.base import RawCandidate
from hpa.normalize import normalize_candidate


def _candidate(**overrides):
    base = dict(
        source_id="local-fixtures",
        source_url="https://example.invalid/p",
        name="My Project",
        description="desc",
        repo_url="https://github.com/o/r",
        stars=50,
        forks=2,
        language="Go",
        topics=["web"],
    )
    base.update(overrides)
    return RawCandidate(**base)


def test_normalize_full_bundle():
    bundle = normalize_candidate(_candidate(), "2026-01-01T00:00:00Z")
    project = bundle["project"]
    assert project["id"] == "my-project"
    assert project["repository_ids"] == ["repo-my-project"]
    assert project["metrics_ids"] == ["metrics-repo-my-project"]
    assert project["popularity"] == "unknown"  # labels applied later
    assert bundle["repository"]["url"] == "https://github.com/o/r"
    assert bundle["metrics"]["stars"] == 50
    # discovery provenance evidence always present
    assert any("discovered via" in e["claim"] for e in bundle["evidence"])


def test_normalize_no_repo_no_metrics():
    bundle = normalize_candidate(_candidate(repo_url=None, stars=None, forks=None), "2026-01-01T00:00:00Z")
    assert bundle["repository"] is None
    assert bundle["metrics"] is None
    assert bundle["project"]["repository_ids"] == []


def test_normalize_verified_award_creates_participation():
    bundle = normalize_candidate(
        _candidate(
            event_name="Cool Jam",
            event_year=2024,
            event_url="https://example.invalid/results",
            award_name="Best Bot",
            award_verified=True,
        ),
        "2026-01-01T00:00:00Z",
    )
    part = bundle["participation"]
    assert part["verified"] is True
    assert part["award_name"] == "Best Bot"
    assert len(part["evidence_ids"]) == 1
    assert bundle["event"]["id"] == "event-cool-jam-2024"


def test_normalize_unverified_award_has_no_award_evidence():
    bundle = normalize_candidate(
        _candidate(
            event_name="Rumor Jam",
            event_year=2023,
            event_url="https://example.invalid/rumor",
            award_name="Best UI",
            award_verified=False,
        ),
        "2026-01-01T00:00:00Z",
    )
    assert bundle["participation"]["verified"] is False
    assert bundle["participation"]["evidence_ids"] == []
