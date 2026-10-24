# Skill: Hackathon Project Archive

Context and rules for working on this repository. Read this before changing project data or tooling.

## Purpose and boundaries

A curated, browsable GitHub archive of notable and wild rapid-build / origin-story projects - hackathons, game jams, hack weeks, Startup Weekend, internal sprints, and similar. Event linkage is preferred but optional when the origin story is strong and evidence-backed. Not a database, not a web app, not an AI platform.

Never build: dynamic web apps, backends, autonomous research agents, scheduled discovery/crawlers, ingestion pipelines, ranking engines, automatic award inference, or mandatory online link checking in CI. The static site under `site/` is generated output, not an application.

## Confirmed product decisions

- **Canonical data**: one Markdown file per project at `data/projects/<id>.md` with YAML frontmatter as the single source of truth. Body Markdown is free-form notes, never indexed. (User overrode the original JSON-per-file idea - do not reopen without asking.)
- **JSON**: produced only via `python -m archive export` for future integrations. Never a second canonical store.
- **Taxonomy**: controlled domains in `data/taxonomy.json`; one primary domain per project; tags are lowercase kebab-case, max 12. Validator rejects unknown domains/tags.
- **Discovery tags**: eight controlled ids in `data/taxonomy.json` (`open-source`, `playable`, `free`, `beginner-friendly`, `starter-build`, `became-startup`, `used-by-millions`, `weekend-build`). `open-source` requires `links.source`; `playable` requires `links.demo`. The other six are editorial. They drive the discovery filter on the site.
- **Hot sort**: `hot_score()` in `export.py` computes a 0-100 score at export time from award (20), source link (15), demo link (15), adoption tag (15), deep dive (20), rapid-build event name (10), and recency (5/3/1/0 by year). Never stored in project files. Hot is the default sort.
- **Detail pages**: `archive/site.py` renders one page per record at `site/p/<id>.html` from the same export that feeds `site/index.html`. Pages are generated; never edit them by hand. `archive check` verifies index, data, and every detail page.
- **Deep dives**: optional `deep_dive: true` plus `key_idea`, `learn_from`, and a body with the sections What it does / The key insight / How it works / Build something similar / Sources. The validator requires the body and both sentences when the flag is set. Seventeen entries carry one; add more only where public sources can support the technical claims.
- **README**: generated index between `<!-- BEGIN GENERATED PROJECT INDEX -->` / `<!-- END GENERATED PROJECT INDEX -->` markers. Deterministic order: taxonomy domain order, then name (case-insensitive), then id. Awards render only when present in data - never inferred. Hand-edit only the sections outside the markers.
- **Evidence**: every entry needs a non-empty `evidence` list (url + optional `supports`). Awards, years, authors, and event links must be evidence-backed. Unknown fields are omitted, never guessed.
- **Research is request-driven**: no scheduled or autonomous discovery. When asked to research/add projects: multi-source research → validate → generate → present to user for approval → only then add to the archive.
- **CI** (`ci.yml`): runs pytest, `archive validate`, `archive check`. Read-only. Must never commit, rewrite files, publish, or do live URL checks.

## Repository structure

```
README.md            # intro + generated index (markers)
CONTRIBUTING.md      # editorial process
LICENSE              # MIT
SKILL.md             # this file
data/taxonomy.json   # domains + tag rules
data/projects/*.md   # canonical project records
archive/             # CLI package: loader, validate, generate, export, site, __main__
scripts/linkcheck.py # optional online check, never in CI
tests/               # pytest, offline, fixtures in helpers.py (never mixed with real data)
site/                # generated: index.html, data.json, p/<id>.html
.github/workflows/ci.yml
```

## CLI (run from repo root)

```bash
pip install -r requirements-dev.txt
python -m archive validate   # schema, ids, domains, tags, URLs, duplicates, evidence
python -m archive generate   # refuses invalid data; rewrites README index
python -m archive check      # fails if README stale; never writes
python -m archive export     # JSON to stdout, for integrations only
python -m pytest             # offline test suite
python scripts/linkcheck.py  # optional, online, best-effort; failures ≠ deleted resources
```

## Safely inspecting and modifying

1. `git status` first; never overwrite uncommitted work.
2. Edit `data/projects/*.md` in place; keep `id` stable and equal to the filename stem.
3. After any data or generator change: `validate` → `generate` → `check` → `pytest`.
4. Taxonomy changes: edit `data/taxonomy.json` only; the schema does not need redesign.
5. No force-push, history rewrite, or destructive git operations without explicit user authorization.

## Session handoff

A future agent resuming work must:

1. Read this SKILL.md before making project or tooling changes.
2. Inspect the repository and `git status`.
3. Summarize current state and any unresolved decisions - do not reopen settled ones (Markdown+YAML canonical, marker-based README, request-driven research, minimal CLI).
4. Follow the confirmed specification above.
5. Ask the user one question at a time if a material product decision remains unresolved.
6. Never generate or add project entries without the user's explicit request and approval of the proposed records and evidence.
7. Never replace this architecture without explicit authorization.
