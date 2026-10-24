from hpa.verify import verify_project


def _ev(eid, reliability):
    return {"id": eid, "reliability": reliability}


def _project(**over):
    base = {
        "id": "p",
        "repository_ids": ["r"],
        "official_url": None,
        "evidence_ids": ["ev1"],
        "limitations": [],
    }
    base.update(over)
    return base


def test_unverified_without_evidence():
    evidence = {}
    assert verify_project(_project(evidence_ids=[]), evidence, []) == "unverified"


def test_unverified_tertiary_only():
    evidence = {"ev1": _ev("ev1", "tertiary")}
    assert verify_project(_project(), evidence, []) == "unverified"


def test_verified_with_primary_repo_evidence_no_award():
    evidence = {"ev1": _ev("ev1", "primary")}
    assert verify_project(_project(), evidence, []) == "verified"


def test_verified_with_secondary_and_official_page():
    evidence = {"ev1": _ev("ev1", "secondary")}
    proj = _project(repository_ids=[], official_url="https://example.com")
    assert verify_project(proj, evidence, []) == "verified"


def test_verified_award_participation():
    evidence = {"ev1": _ev("ev1", "primary")}
    parts = [{"award_name": "Grand Prize", "verified": True}]
    assert verify_project(_project(), evidence, parts) == "verified"


def test_unverified_award_partial():
    evidence = {"ev1": _ev("ev1", "primary")}
    parts = [{"award_name": "Best UI", "verified": False}]
    assert verify_project(_project(), evidence, parts) == "partially-verified"


def test_disputed_via_limitation():
    evidence = {"ev1": _ev("ev1", "primary")}
    proj = _project(limitations=["Sources disputed over the founding year."])
    assert verify_project(proj, evidence, []) == "disputed"
