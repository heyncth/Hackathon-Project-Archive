"""Generator and consistency-check tests."""

from __future__ import annotations

import textwrap

from archive.generate import check_readme, render_stats, splice_stats, write_readme
from archive.site import build_site, check_site
from helpers import VALID_PROJECT, load, make_repo


def _repo(tmp_path, projects: dict[str, str]):
    make_repo(tmp_path, projects)
    return load(tmp_path)


def test_stats_deterministic(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    assert render_stats(repo) == render_stats(repo)


def test_stats_counts_projects(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    stats = render_stats(repo)
    assert "1 projects" in stats
    assert "Games (1)" in stats


def test_stats_counts_awards(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    assert "1 with documented awards" in render_stats(repo)


def test_stats_no_awards(tmp_path):
    no_award = textwrap.dedent(
        """\
        ---
        id: quiet
        name: Quiet
        description: No award.
        domain: games
        evidence:
          - url: https://example.com/q
        ---
        """
    )
    repo = _repo(tmp_path, {"quiet.md": no_award})
    stats = render_stats(repo)
    assert "documented awards" not in stats


def test_splice_stats(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    result = splice_stats("head\n<!-- BEGIN GENERATED STATS -->\n<!-- END GENERATED STATS -->\ntail", render_stats(repo))
    assert "1 projects" in result
    assert "head" in result
    assert "tail" in result


def test_write_and_check_roundtrip(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    write_readme(repo)
    assert check_readme(repo) is None


def test_stale_readme_detected(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    write_readme(repo)
    readme = tmp_path / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("1 projects", "99 projects"),
        encoding="utf-8",
    )
    assert check_readme(repo) is not None


def test_missing_markers(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT}, readme=False)
    (tmp_path / "README.md").write_text("# No markers here\n", encoding="utf-8")
    repo = load(tmp_path)
    assert check_readme(repo) is not None


def test_build_site(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    assert (site / "index.html").exists()
    assert (site / "data.json").exists()


def test_check_site_fresh(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    build_site(repo)
    assert check_site(repo) is None


def test_check_site_stale(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    build_site(repo)
    (tmp_path / "site" / "data.json").write_text("[]", encoding="utf-8")
    assert check_site(repo) is not None


def test_check_site_detects_missing_detail_page(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    (site / "p" / "example-project.html").unlink()
    message = check_site(repo)
    assert message is not None
    assert "example-project.html is missing" in message


def test_check_site_detects_stale_detail_page(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    (site / "p" / "example-project.html").write_text("old page", encoding="utf-8")
    message = check_site(repo)
    assert message is not None
    assert "example-project.html is stale" in message


def test_site_data_contains_project(tmp_path):
    import json

    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    payload = json.loads((site / "data.json").read_text(encoding="utf-8"))
    assert len(payload["projects"]) == 1
    assert payload["projects"][0]["name"] == "Example Project"
    assert "domains" in payload
    assert payload["discovery_tags"] == ["open-source", "playable", "weekend-build"]
    assert payload["projects"][0]["hot"] == 48


DEEP_DIVE_PROJECT = textwrap.dedent(
    """\
    ---
    id: example-project
    name: Example Project
    description: A project with a breakdown.
    domain: games
    tags: [open-source]
    event:
      name: Example Hackathon
      year: 2020
    links:
      source: https://github.com/example/example
    deep_dive: true
    key_idea: The one idea that made it work.
    learn_from: The lesson worth copying.
    evidence:
      - url: https://example.com/evidence
    ---

    ## What it does

    Rendered fixture text.
    """
)


def test_site_builds_detail_page(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    page = site / "p" / "example-project.html"
    assert page.exists()
    text = page.read_text(encoding="utf-8")
    assert "Example Project" in text
    assert 'href="../index.html"' in text


def test_detail_page_renders_deep_dive(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": DEEP_DIVE_PROJECT})
    site = build_site(repo)
    text = (site / "p" / "example-project.html").read_text(encoding="utf-8")
    assert "Rendered fixture text." in text
    assert "<h2>What it does</h2>" in text
    assert '<span class="pill">Deep dive</span>' in text
    assert "The one idea that made it work." in text
    assert "The lesson worth copying." in text


def test_detail_page_labels_profile(tmp_path):
    content = VALID_PROJECT.rstrip() + "\n\n## What it is\n\nA profile fixture.\n"
    repo = _repo(tmp_path, {"example-project.md": content})
    site = build_site(repo)
    text = (site / "p" / "example-project.html").read_text(encoding="utf-8")
    assert '<span class="pill">Profile</span>' in text
    assert "A profile fixture." in text


def test_index_links_to_detail_pages(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    site = build_site(repo)
    index = (site / "index.html").read_text(encoding="utf-8")
    assert "p/" in index
    assert "Sort: Hot" in index
