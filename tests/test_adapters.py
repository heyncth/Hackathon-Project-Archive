"""Adapter tests with mocks; no real network access."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from hpa.adapters import build_adapter
from hpa.adapters.base import RawCandidate, SearchFailure
from hpa.adapters.devpost import DevpostAdapter
from hpa.adapters.fixture import FixtureAdapter
from hpa.adapters.github import GitHubAdapter

from conftest import FIXTURES


class FakeResponse:
    def __init__(self, status_code: int, payload=None, text: str = ""):
        self.status_code = status_code
        self._payload = payload
        self.text = text or (json.dumps(payload) if payload is not None else "")

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


def test_build_adapter_unknown():
    with pytest.raises(SearchFailure):
        build_adapter("nope", {"id": "x"})


def test_fixture_adapter_reads_candidates():
    adapter = FixtureAdapter({"id": "local-fixtures", "base_url": str(FIXTURES)})
    found = adapter.search("anything", limit=10)
    assert len(found) == 4
    assert found[0].name == "Fixture Alpha"
    assert found[0].award_verified is True
    assert found[1].repo_url is None


def test_fixture_adapter_file_query_override(tmp_path: Path):
    adapter = FixtureAdapter({"id": "local-fixtures", "base_url": "missing/relative.json"})
    found = adapter.search(f"file:{FIXTURES}", limit=2)
    assert len(found) == 2


def test_fixture_adapter_missing_file():
    adapter = FixtureAdapter({"id": "local-fixtures", "base_url": "nope.json"})
    with pytest.raises(SearchFailure):
        adapter.search("q")


def test_github_adapter_success(monkeypatch):
    payload = {
        "items": [
            {
                "html_url": "https://github.com/foo/bar",
                "name": "bar",
                "description": "demo project",
                "stargazers_count": 1200,
                "forks_count": 10,
                "language": "Python",
                "topics": ["ai"],
                "homepage": "https://example.com",
            }
        ]
    }

    def fake_get(url, params=None, headers=None, timeout=None):
        assert "GITHUB_TOKEN" not in str(headers)  # token header name may exist only if env set
        return FakeResponse(200, payload)

    monkeypatch.setattr("hpa.adapters.github.requests.get", fake_get)
    adapter = GitHubAdapter({"id": "github-search"})
    found = adapter.search("topic:hackathon", limit=5)
    assert len(found) == 1
    assert found[0].stars == 1200
    assert found[0].evidence[0]["source_type"] == "repository"
    assert found[0].evidence[0]["reliability"] == "primary"


def test_github_adapter_rate_limited(monkeypatch):
    monkeypatch.setattr(
        "hpa.adapters.github.requests.get",
        lambda *a, **k: FakeResponse(403, text="API rate limit exceeded"),
    )
    adapter = GitHubAdapter({"id": "github-search"})
    with pytest.raises(SearchFailure, match="rate limited"):
        adapter.search("q")


def test_github_adapter_network_error(monkeypatch):
    import requests as req

    def boom(*a, **k):
        raise req.ConnectionError("down")

    monkeypatch.setattr("hpa.adapters.github.requests.get", boom)
    adapter = GitHubAdapter({"id": "github-search"})
    with pytest.raises(SearchFailure, match="network error"):
        adapter.search("q")


DEVPOST_HTML = """
<html><body>
<ul>
  <li class="software locked">ignored</li>
  <li class="software">
    <a class="title" href="https://devpost.com/software/sample-app">Sample App</a>
    <p class="tagline">A sample tagline</p>
  </li>
</ul>
</body></html>
"""


def test_devpost_adapter_parses_cards(monkeypatch):
    monkeypatch.setattr(
        "hpa.adapters.devpost.requests.get",
        lambda *a, **k: FakeResponse(200, text=DEVPOST_HTML),
    )
    adapter = DevpostAdapter({"id": "devpost-galleries", "base_url": "https://devpost.com/software/search"})
    found = adapter.search("sample", limit=5)
    assert len(found) == 1
    assert found[0].name == "Sample App"
    assert found[0].description == "A sample tagline"
    assert found[0].repo_url is None  # awards/repos never inferred from listings


def test_devpost_adapter_blocked(monkeypatch):
    monkeypatch.setattr(
        "hpa.adapters.devpost.requests.get",
        lambda *a, **k: FakeResponse(403, text="forbidden"),
    )
    adapter = DevpostAdapter({"id": "devpost-galleries", "base_url": "https://devpost.com/software/search"})
    with pytest.raises(SearchFailure, match="access restricted"):
        adapter.search("q")


def test_devpost_adapter_markup_change(monkeypatch):
    monkeypatch.setattr(
        "hpa.adapters.devpost.requests.get",
        lambda *a, **k: FakeResponse(200, text="<html><body>new layout</body></html>"),
    )
    adapter = DevpostAdapter({"id": "devpost-galleries", "base_url": "https://devpost.com/software/search"})
    with pytest.raises(SearchFailure, match="no software cards"):
        adapter.search("q")


def test_raw_candidate_to_dict_roundtrip():
    c = RawCandidate(source_id="s", source_url="https://x.example", name="X")
    d = c.to_dict()
    assert d["name"] == "X"
    assert d["evidence"] == []
