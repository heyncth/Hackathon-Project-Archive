from hpa.label import apply_labels, popularity_from_stars


def test_popularity_thresholds():
    assert popularity_from_stars(None) == "unknown"
    assert popularity_from_stars(10) == "limited"
    assert popularity_from_stars(99) == "limited"
    assert popularity_from_stars(100) == "moderate"
    assert popularity_from_stars(999) == "moderate"
    assert popularity_from_stars(1000) == "high"
    assert popularity_from_stars(5000) == "high"


def _project(**over):
    base = {
        "id": "p",
        "name": "P",
        "categories": ["community-notable"],
        "popularity": "unknown",
        "educational_value": "unknown",
        "limitations": [],
    }
    base.update(over)
    return base


def test_apply_labels_high_popularity_from_metrics():
    metrics = [{"stars": 2500, "forks": 10}]
    out = apply_labels(_project(), [], metrics)
    assert out["popularity"] == "high"
    assert "community-notable" in out["categories"]


def test_apply_labels_verified_award_adds_award_winning():
    parts = [{"award_name": "Grand Prize", "verified": True}]
    out = apply_labels(_project(), parts, [])
    assert "award-winning" in out["categories"]


def test_apply_labels_unverified_award_excluded_and_flagged():
    parts = [{"award_name": "Best UI", "verified": False}]
    out = apply_labels(_project(categories=["award-winning", "community-notable"]), parts, [])
    assert "award-winning" not in out["categories"]
    assert any("unverified award" in lim.lower() for lim in out["limitations"])


def test_apply_labels_never_empty_categories():
    out = apply_labels(_project(categories=[]), [], [])
    assert out["categories"] == ["community-notable"]
