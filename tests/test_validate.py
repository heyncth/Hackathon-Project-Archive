"""Validation tests."""

from __future__ import annotations

import textwrap

from archive.validate import validate_repo
from helpers import VALID_PROJECT, load, make_repo


def _errors(tmp_path, content: str, filename: str = "example-project.md") -> list[str]:
    make_repo(tmp_path, {filename: content})
    return validate_repo(load(tmp_path))


def test_valid_project(tmp_path):
    errors = _errors(tmp_path, VALID_PROJECT)
    assert errors == []


def test_minimal_optional_fields_absent(tmp_path):
    minimal = textwrap.dedent(
        """\
        ---
        id: bare
        name: Bare
        description: Minimal record.
        domain: other
        evidence:
          - url: https://example.com/proof
        ---
        """
    )
    assert _errors(tmp_path, minimal, "bare.md") == []


def test_missing_required_fields(tmp_path):
    content = textwrap.dedent(
        """\
        ---
        id: incomplete
        ---
        """
    )
    errors = _errors(tmp_path, content, "incomplete.md")
    joined = "\n".join(errors)
    assert "missing required field 'name'" in joined
    assert "missing required field 'description'" in joined
    assert "missing required field 'domain'" in joined
    assert "evidence" in joined


def test_invalid_types(tmp_path):
    content = textwrap.dedent(
        """\
        ---
        id: badtypes
        name: 123
        description: [a, list]
        domain: other
        evidence:
          - url: https://example.com/proof
        """
    ) + "---\n"
    errors = _errors(tmp_path, content, "badtypes.md")
    joined = "\n".join(errors)
    assert "'name' must be a non-empty string" in joined
    assert "'description' must be a non-empty string" in joined


def test_malformed_yaml(tmp_path):
    content = "id: broken\nname: [unclosed\ndomain: other\n"
    errors = _errors(tmp_path, content, "broken.md")
    assert any("invalid YAML frontmatter" in e or "malformed" in e for e in errors)


def test_missing_frontmatter(tmp_path):
    errors = _errors(tmp_path, "just prose, no frontmatter\n", "plain.md")
    assert any("missing or malformed" in e for e in errors)


def test_invalid_domain(tmp_path):
    content = VALID_PROJECT.replace("domain: games", "domain: not-a-domain")
    errors = _errors(tmp_path, content)
    assert any("not in taxonomy" in e for e in errors)


def test_invalid_tags(tmp_path):
    content = VALID_PROJECT.replace("tags: [demo, fixture]", "tags: [Bad_Tag, ok]")
    errors = _errors(tmp_path, content)
    assert any("invalid tag" in e for e in errors)


def test_too_many_tags(tmp_path):
    tags = ", ".join(f"tag{i}" for i in range(9))
    content = VALID_PROJECT.replace("tags: [demo, fixture]", f"tags: [{tags}]")
    errors = _errors(tmp_path, content)
    assert any("too many tags" in e for e in errors)


def test_id_filename_mismatch(tmp_path):
    errors = _errors(tmp_path, VALID_PROJECT, "wrong-name.md")
    assert any("does not match filename" in e for e in errors)


def test_non_kebab_id(tmp_path):
    content = VALID_PROJECT.replace("id: example-project", "id: Example_Project")
    errors = _errors(tmp_path, content, "Example_Project.md")
    assert any("kebab-case" in e for e in errors)


def test_duplicate_ids(tmp_path):
    a = VALID_PROJECT
    b = VALID_PROJECT.replace("https://example.com", "https://example.org").replace(
        "https://github.com/example/example", "https://github.com/example/other"
    ).replace("https://example.com/evidence", "https://example.org/evidence")
    make_repo(tmp_path, {"one.md": a, "two.md": b})
    errors = validate_repo(load(tmp_path))
    # second file's id won't match filename, plus duplicate id error
    assert any("duplicate id" in e for e in errors)


def test_duplicate_official_link(tmp_path):
    a = VALID_PROJECT
    b = textwrap.dedent(
        """\
        ---
        id: second
        name: Second
        description: Another project.
        domain: web-mobile
        links:
          official: https://example.com/
        evidence:
          - url: https://example.com/proof2
        ---
        """
    )
    make_repo(tmp_path, {"example-project.md": a, "second.md": b})
    errors = validate_repo(load(tmp_path))
    assert any("duplicate official link" in e for e in errors)


def test_malformed_url(tmp_path):
    content = VALID_PROJECT.replace("official: https://example.com", "official: not a url")
    errors = _errors(tmp_path, content)
    assert any("not a valid http(s) URL" in e for e in errors)


def test_bad_evidence_structure(tmp_path):
    content = VALID_PROJECT.replace(
        '  - url: https://example.com/evidence\n    supports: "Award and participation claims"',
        '  - supports: "no url though"',
    )
    errors = _errors(tmp_path, content)
    assert any("evidence[0]" in e and "url" in e for e in errors)


def test_empty_evidence_list(tmp_path):
    content = VALID_PROJECT.replace(
        'evidence:\n  - url: https://example.com/evidence\n    supports: "Award and participation claims"',
        "evidence: []",
    )
    errors = _errors(tmp_path, content)
    assert any("non-empty list" in e for e in errors)


def test_bad_event_year(tmp_path):
    content = VALID_PROJECT.replace("year: 2020", "year: 99999")
    errors = _errors(tmp_path, content)
    assert any("event.year" in e for e in errors)


def test_bad_verified_at(tmp_path):
    content = VALID_PROJECT.replace("verified_at: 2026-01-01", "verified_at: last tuesday")
    errors = _errors(tmp_path, content)
    assert any("verified_at" in e for e in errors)


def test_unknown_field(tmp_path):
    content = VALID_PROJECT.replace("domain: games", "domain: games\nrank: 1")
    errors = _errors(tmp_path, content)
    assert any("unknown field 'rank'" in e for e in errors)


def test_empty_dataset_is_valid(tmp_path):
    make_repo(tmp_path, {})
    assert validate_repo(load(tmp_path)) == []


DEEP_DIVE = textwrap.dedent(
    """\
    ---
    id: deep-dive
    name: Deep Dive
    description: A project with a written breakdown.
    domain: games
    tags: [open-source]
    links:
      source: https://github.com/example/deep-dive
    deep_dive: true
    key_idea: One sentence about the idea.
    learn_from: One sentence about the lesson.
    evidence:
      - url: https://example.com/deep-dive
    ---

    ## What it does

    Body text.
    """
)


def test_deep_dive_valid(tmp_path):
    assert _errors(tmp_path, DEEP_DIVE, "deep-dive.md") == []


def test_deep_dive_requires_body(tmp_path):
    content = DEEP_DIVE.split("## What it does")[0].rstrip() + "\n"
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("no body content" in e for e in errors)


def test_deep_dive_requires_key_idea(tmp_path):
    content = DEEP_DIVE.replace("key_idea: One sentence about the idea.\n", "")
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("missing 'key_idea'" in e for e in errors)


def test_deep_dive_requires_learn_from(tmp_path):
    content = DEEP_DIVE.replace("learn_from: One sentence about the lesson.\n", "")
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("missing 'learn_from'" in e for e in errors)


def test_deep_dive_flag_must_be_boolean(tmp_path):
    content = DEEP_DIVE.replace("deep_dive: true", "deep_dive: yes please")
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("'deep_dive' must be a boolean" in e for e in errors)


def test_key_idea_must_be_non_empty(tmp_path):
    content = DEEP_DIVE.replace("key_idea: One sentence about the idea.", 'key_idea: ""')
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("'key_idea' must be a non-empty string" in e for e in errors)


def test_open_source_tag_requires_source_link(tmp_path):
    content = DEEP_DIVE.replace("  source: https://github.com/example/deep-dive\n", "")
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("requires links.source" in e for e in errors)


def test_playable_tag_requires_demo_link(tmp_path):
    content = DEEP_DIVE.replace("tags: [open-source]", "tags: [playable]").replace(
        "  source: https://github.com/example/deep-dive\n", ""
    )
    errors = _errors(tmp_path, content, "deep-dive.md")
    assert any("requires links.demo" in e for e in errors)


def test_editorial_discovery_tag_needs_no_link(tmp_path):
    content = DEEP_DIVE.replace("tags: [open-source]", "tags: [weekend-build]").replace(
        "  source: https://github.com/example/deep-dive\n", ""
    )
    assert _errors(tmp_path, content, "deep-dive.md") == []
