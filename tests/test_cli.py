"""CLI-level tests for python -m archive."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from helpers import VALID_PROJECT, make_repo

ROOT = Path(__file__).resolve().parent.parent


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "archive", "--root", str(root), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_validate_ok(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT})
    r = _run(tmp_path, "validate")
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout


def test_cli_validate_fails_on_bad_data(tmp_path):
    make_repo(tmp_path, {"bad.md": "not yaml frontmatter"})
    r = _run(tmp_path, "validate")
    assert r.returncode == 1
    assert "bad.md" in r.stderr


def test_cli_generate_then_check(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT})
    r = _run(tmp_path, "generate")
    assert r.returncode == 0, r.stderr
    r = _run(tmp_path, "check")
    assert r.returncode == 0, r.stderr


def test_cli_check_stale_fails(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT})
    r = _run(tmp_path, "check")  # never generated
    assert r.returncode == 1
    assert "stale" in r.stderr


def test_cli_generate_refuses_invalid(tmp_path):
    make_repo(tmp_path, {"bad.md": "no frontmatter"})
    r = _run(tmp_path, "generate")
    assert r.returncode == 1
    assert "refusing" in r.stderr


def test_cli_export_json(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT})
    r = _run(tmp_path, "export")
    assert r.returncode == 0, r.stderr
    assert '"example-project"' in r.stdout


def test_cli_real_repo_validates():
    """The actual repository data must stay valid."""
    r = _run(ROOT, "validate")
    assert r.returncode == 0, r.stderr


def test_cli_real_repo_readme_fresh():
    r = _run(ROOT, "check")
    assert r.returncode == 0, r.stderr
