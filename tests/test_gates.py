from hpa.gates import case_study_gate, evaluate_gates, overview_gate, reconstruction_gate


def _project(**over):
    base = {
        "id": "p",
        "verification_status": "verified",
        "description": "something",
        "evidence_ids": ["ev1", "ev2"],
        "repository_ids": ["r1"],
        "documentation_quality": "strong",
        "reproducibility": "documented-not-tested",
    }
    base.update(over)
    return base


def test_overview_gate_pass():
    ok, reason = overview_gate(_project())
    assert ok and reason is None


def test_overview_gate_fails_unverified():
    ok, reason = overview_gate(_project(verification_status="unverified"))
    assert not ok and "verification_status" in reason


def test_overview_gate_fails_no_description():
    ok, reason = overview_gate(_project(description=None))
    assert not ok


def test_case_study_gate_requires_verified_and_repo():
    ok, _ = case_study_gate(_project(), [{"id": "r1"}])
    assert ok
    ok, reason = case_study_gate(_project(verification_status="partially-verified"), [{"id": "r1"}])
    assert not ok
    ok, reason = case_study_gate(_project(), [])
    assert not ok and "repository" in reason


def test_reconstruction_gate_fails_without_repo_and_docs():
    ok, reason = reconstruction_gate(
        _project(repository_ids=[], documentation_quality="limited"), 3
    )
    assert not ok


def test_reconstruction_gate_fails_few_evidence():
    ok, reason = reconstruction_gate(_project(evidence_ids=["ev1"]), 1)
    assert not ok and "evidence" in reason


def test_reconstruction_gate_fails_disputed():
    ok, reason = reconstruction_gate(_project(verification_status="disputed"), 3)
    assert not ok


def test_reconstruction_gate_passes_with_docs_only():
    ok, reason = reconstruction_gate(
        _project(repository_ids=[], documentation_quality="strong"), 3
    )
    assert ok


def test_evaluate_gates_keys():
    gates = evaluate_gates(_project(), [{"id": "r1"}])
    assert set(gates) == {"overview", "case-study", "reconstruction"}
    assert gates["overview"]["passed"] is True
