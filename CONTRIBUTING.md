# Contributing

This archive is curated. Entries are added on request and only after human review — there is no automated ingestion or scheduled discovery.

## What belongs here

A project qualifies if it:

- Was built at, or demonstrably originated from, a hackathon, game jam, hack week, or comparable rapid-build event.
- Has lasting technical, educational, practical, or social value. Winners and non-winners both qualify.
- Has credible public evidence establishing its identity and connection to the event. A public source repository is welcome but not required.

It does not qualify if the only evidence is a single low-quality mention, a repository creation date, or popularity metrics (GitHub stars, upvotes) with no event connection.

## Evidence rules

- Every factual claim — event participation, year, award, authors — needs at least one evidence URL in the `evidence` field.
- Prefer primary sources: official event pages, Devpost, organizer announcements, original project pages or repos, reputable press.
- Never invent awards, dates, authors, technical details, or URLs. If a detail is unknown, omit the field. Omission means "unverified", not "none".
- Do not infer an event year from a repository creation date.
- A syntactically valid URL does not prove a claim is true.

## Adding a project

1. Create `data/projects/<id>.md` — `<id>` is kebab-case and must match the `id` field (e.g. `superhot-prototype.md`).
2. Fill the YAML frontmatter:

```yaml
---
id: my-project            # required, kebab-case, matches filename
name: My Project          # required
description: One or two sentences on what it is.   # required
domain: games             # required, must be in data/taxonomy.json
tags: [game-jam, unity]   # optional, lowercase kebab-case, max 8
event:                    # optional, but required for archive eligibility
  name: Some Hackathon    # required if `event` is present
  organizer: Org Name     # optional
  year: 2019              # optional, 1900-2100
  award: Winner           # optional — only if evidence-backed
links:                    # optional
  official: https://...
  source: https://...
  demo: https://...
  video: https://...
authors:                  # optional, only verifiable names
  - Name One
evidence:                 # required, at least one entry
  - url: https://...
    supports: "Which claim this source backs"
notes: Any caveats (e.g. "rapid build, not a formal hackathon").  # optional
verified_at: 2026-01-01   # optional, last time you checked the evidence
---
```

3. Any Markdown body after the frontmatter is free-form notes; it is not shown in the generated index.

## Choosing a domain and tags

- `domain` is the single primary category — pick from `data/taxonomy.json`. If nothing fits, use `other`; propose a taxonomy change in your PR description rather than inventing a domain.
- `tags` describe technologies, use cases, or themes (e.g. `game-jam`, `open-source`). Lowercase kebab-case, max 8.

## Running the tools

```bash
pip install -r requirements-dev.txt
python -m archive validate   # must pass
python -m archive generate   # regenerate the README index
python -m archive check      # CI runs this; fails if index is stale
python -m pytest             # test suite (offline)
python scripts/linkcheck.py  # optional, online; never run as a gate
```

Link checking is best-effort. A timeout or 5xx does not mean a resource is gone — do not delete or "fix" records based on a single failed request.

## Updating existing entries

Edit the existing `.md` file in place. Keep the same `id`. Add evidence for any new claims, re-run `validate` and `generate`, and note what changed and why.

## Review

Maintainers review additions for evidence quality, domain fit, and duplicates before they become part of the archive. Pull requests are welcome; maintainers may also add entries directly — either way, validation and human review come first.
