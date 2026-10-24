"""Publication gates (docs/verification-policy.md).

A guide is written only when its gate passes. Failures are recorded with a
reason; the basic profile may still be published.
"""

from __future__ import annotations

from typing import Any


def overview_gate(project: dict[str, Any]) -> tuple[bool, str | None]:
    """Overview: sufficient evidence for purpose and documented capabilities."""
    if project.get("verification_status") not in ("verified", "partially-verified"):
        return False, "verification_status is not verified/partially-verified"
    if not project.get("description"):
        return False, "no description available to summarize"
    if not project.get("evidence_ids"):
        return False, "no evidence records support the profile"
    return True, None


def case_study_gate(project: dict[str, Any], repositories: list[dict[str, Any]]) -> tuple[bool, str | None]:
    """Case study: needs architectural/technical evidence, not just existence."""
    if project.get("verification_status") not in ("verified",):
        return False, "case study requires verified evidence status"
    if not repositories:
        return False, "no repository available for engineering analysis"
    if project.get("documentation_quality") not in ("strong", "partial"):
        return False, "documentation quality too weak for architectural claims"
    if project.get("reproducibility") == "not-assessed" and project.get("documentation_quality") != "strong":
        return False, "insufficient technical documentation for architecture analysis"
    return True, None


def reconstruction_gate(project: dict[str, Any], evidence_count: int) -> tuple[bool, str | None]:
    """Reconstruction: enough evidence to build an honest similar project."""
    if project.get("verification_status") == "unverified":
        return False, "evidence status unverified"
    if evidence_count < 2:
        return False, "fewer than two evidence records; scope would be guesswork"
    has_repo = bool(project.get("repository_ids"))
    has_docs = project.get("documentation_quality") == "strong"
    if not has_repo and not has_docs:
        return False, "no original repository and only weak documentation to reconstruct from"
    if project.get("verification_status") == "disputed":
        return False, "disputed claims block an honest reconstruction guide"
    return True, None


def evaluate_gates(
    project: dict[str, Any],
    repositories: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Return gate results for all three guide types."""
    overview_ok, overview_reason = overview_gate(project)
    case_ok, case_reason = case_study_gate(project, repositories)
    recon_ok, recon_reason = reconstruction_gate(project, len(project.get("evidence_ids", [])))
    return {
        "overview": {"passed": overview_ok, "reason": overview_reason},
        "case-study": {"passed": case_ok, "reason": case_reason},
        "reconstruction": {"passed": recon_ok, "reason": recon_reason},
    }
