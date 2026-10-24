"""Generator and consistency-check tests."""

from __future__ import annotations

import textwrap

from archive.generate import check_readme, generate_index, write_readme
from helpers import VALID_PROJECT, load, make_repo


def _repo(tmp_path, projects: dict[str, str]):
    make_repo(tmp_path, projects)
    return load(tmp_path)


def test_generation_is_deterministic(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    assert generate_index(repo) == generate_index(repo)


def test_ordering_by_domain_then_name(tmp_path):
    a = VALID_PROJECT
    b = textwrap.dedent(
        """\
        ---
        id: aaa-first
        name: AAA First
        description: Sorts before in same domain.
        domain: games
        evidence:
          - url: https://example.com/b
        ---
        """
    )
    c = textwrap.dedent(
        """\
        ---
        id: web-one
        name: Web One
        description: Different domain.
        domain: web-mobile
        evidence:
          - url: https://example.com/c
        ---
        """
    )
    repo = _repo(tmp_path, {"example-project.md": a, "aaa-first.md": b, "web-one.md": c})
    index = generate_index(repo)
    # taxonomy order: games before web-mobile; within games, AAA First before Example Project
    assert index.index("AAA First") < index.index("Example Project") < index.index("Web One")


def test_award_rendered_when_present(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    assert "**Award:** Winner" in generate_index(repo)


def test_award_not_invented_when_absent(tmp_path):
    no_award = textwrap.dedent(
        """\
        ---
        id: quiet
        name: Quiet Project
        description: No award recorded.
        domain: games
        evidence:
          - url: https://example.com/q
        ---
        """
    )
    repo = _repo(tmp_path, {"quiet.md": no_award})
    index = generate_index(repo)
    assert "Award" not in index
    assert "Winner" not in index


def test_optional_fields_rendered_safely(tmp_path):
    bare = textwrap.dedent(
        """\
        ---
        id: bare
        name: Bare
        description: Only required fields.
        domain: other
        evidence:
          - url: https://example.com/proof
        ---
        """
    )
    repo = _repo(tmp_path, {"bare.md": bare})
    index = generate_index(repo)
    assert "### Bare" in index
    assert "Event" not in index
    assert "Links" not in index
    assert "Team" not in index


def test_empty_dataset(tmp_path):
    repo = _repo(tmp_path, {})
    assert "No projects yet" in generate_index(repo)


def test_unusual_characters_in_name(tmp_path):
    weird = textwrap.dedent(
        """\
        ---
        id: weird-name
        name: 'Café & Crème — the "best" <hack> project 🚀'
        description: Handles unicode and markup-ish characters.
        domain: other
        evidence:
          - url: https://example.com/w
        ---
        """
    )
    repo = _repo(tmp_path, {"weird-name.md": weird})
    index = generate_index(repo)
    assert "Café & Crème" in index


def test_write_and_check_roundtrip(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    write_readme(repo)
    assert check_readme(repo) is None


def test_stale_readme_detected(tmp_path):
    repo = _repo(tmp_path, {"example-project.md": VALID_PROJECT})
    write_readme(repo)
    readme = tmp_path / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("Example Project", "Renamed"), encoding="utf-8")
    assert check_readme(repo) is not None


def test_missing_markers(tmp_path):
    make_repo(tmp_path, {"example-project.md": VALID_PROJECT}, readme=False)
    (tmp_path / "README.md").write_text("# No markers here\n", encoding="utf-8")
    repo = load(tmp_path)
    assert check_readme(repo) is not None


def test_body_text_ignored_by_index(tmp_path):
    with_body = VALID_PROJECT + "\nExtra body prose not in frontmatter.\n"
    repo = _repo(tmp_path, {"example-project.md": with_body})
    assert "Extra body prose" not in generate_index(repo)
