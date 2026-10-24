"""Shared test helpers: build a temporary repository root with schemas/sources."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "candidates.json"


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """A minimal repo root: schemas + sources + empty data/."""
    shutil.copytree(REPO_ROOT / "schemas", tmp_path / "schemas")
    shutil.copytree(REPO_ROOT / "sources", tmp_path / "sources")
    (tmp_path / "data").mkdir()
    return tmp_path


@pytest.fixture
def fixture_query() -> str:
    return f"file:{FIXTURES}"
