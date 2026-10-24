# Contributing

This archive is curated. Entries are added on request and only after human review - there is no automated ingestion or scheduled discovery.

## What belongs here

A project qualifies if it:

- Is a notable, wild, or surprising idea with a documented origin story - preferably a hackathon, game jam, hack week, internal build sprint, Startup Weekend, or comparable rapid-build event, but strong non-event origin stories are also eligible.
- Has lasting technical, educational, practical, social, or cautionary value. Winners and non-winners both qualify; spectacular failures with clear evidence qualify as cautionary tales.
- Has credible public evidence establishing its identity and (when claimed) its connection to the event. A public source repository is welcome but not required.

`event` is optional in the schema. Omit it when the origin is real but not a formal event (lab prototype, internal research build, weekend side project). Do not invent an event to force eligibility.

It does not qualify if the only evidence is a single low-quality mention, a repository creation date, or popularity metrics (GitHub stars, upvotes) with no credible origin story.

## Evidence rules

- Every factual claim - event participation, year, award, authors - needs at least one evidence URL in the `evidence` field.
- Prefer primary sources: official event pages, Devpost, organizer announcements, original project pages or repos, reputable press.
- Never invent awards, dates, authors, technical details, or URLs. If a detail is unknown, omit the field. Omission means "unverified", not "none".
- Do not infer an event year from a repository creation date.
- A syntactically valid URL does not prove a claim is true.

## Adding a project

1. Create `data/projects/<id>.md` - `<id>` is kebab-case and must match the `id` field (e.g. `superhot-prototype.md`).
2. Fill the YAML frontmatter:

```yaml
---
id: my-project            # required, kebab-case, matches filename
name: My Project          # required
description: One or two sentences on what it is.   # required
domain: games             # required, must be in data/taxonomy.json
tags: [game-jam, unity]   # optional, lowercase kebab-case, max 12
event:                    # optional; omit for non-event origin stories
  name: Some Hackathon    # required if `event` is present
  organizer: Org Name     # optional
  year: 2019              # optional, 1900-2100
  award: Winner           # optional - only if evidence-backed
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
deep_dive: true           # optional; marks a written breakdown
key_idea: One sentence on the central idea.          # required when deep_dive
learn_from: One sentence on the transferable lesson. # required when deep_dive
verified_at: 2026-01-01   # optional, last time you checked the evidence
---
```

3. Markdown after the frontmatter is notes. When `deep_dive: true`, that body is the published breakdown and must contain at least one section.

## Choosing a domain and tags

- `domain` is the single primary category - pick from `data/taxonomy.json`. If nothing fits, use `other`; propose a taxonomy change in your PR description rather than inventing a domain.
- `tags` describe technologies, use cases, or themes (e.g. `game-jam`, `unity`). Lowercase kebab-case, max 12. The eight `discovery_tags` in `data/taxonomy.json` are reserved ids described below.

## Discovery tags

`data/taxonomy.json` defines eight tags that drive the filters on the site. Use these exact ids; do not invent new ones without a taxonomy change.

| Tag | Meaning | Check |
|---|---|---|
| `open-source` | Source code is public | Requires `links.source` |
| `playable` | A demo runs now | Requires `links.demo` |
| `free` | Free to use | Editorial |
| `beginner-friendly` | A reasonable first project to study | Editorial |
| `starter-build` | Good template for building something similar | Editorial |
| `became-startup` | Turned into a funded company | Editorial |
| `used-by-millions` | Mass adoption | Editorial |
| `weekend-build` | Shipped in about 48 hours | Editorial |

The two linked tags are validated: a record tagged `open-source` without a source link fails `validate`. The editorial tags are judgement calls, so back them in the `supports` text of an evidence entry when the claim is not obvious from the description.

Free-form tags still cover technology and theme. The 12 tag limit counts both kinds.

## Deep dives

A deep dive is an optional technical breakdown of how a project works. Seventeen entries have one. The bar is source material, not enthusiasm: a deep dive needs public code, an engineering writeup, or documentation specific enough to describe the architecture without guessing.

Add one only when you can answer three questions from sources:

1. What does it actually do?
2. What was the decision that made it work?
3. Where would a reader start if they built something similar?

Set `deep_dive: true`, add `key_idea` and `learn_from`, and write the body with these sections:

```markdown
## What it does

## The key insight

## How it works

## Build something similar

## Sources
```

Keep every technical claim traceable to the `evidence` list or a source named in the body. If a mechanism is not documented, describe it at the level the sources support or leave it out. A thin deep dive is worse than none, because it looks authoritative.

`key_idea` appears on the card in the index. `learn_from` and the body appear on the project's detail page.

## Running the tools

```bash
pip install -r requirements-dev.txt
python -m archive validate   # must pass
python -m archive generate   # build site + update README stats
python -m archive check      # CI runs this; fails if README, index, data, or any detail page is stale
python -m pytest             # test suite (offline)
python scripts/linkcheck.py  # optional, online; never run as a gate
```

Link checking is best-effort. A timeout or 5xx does not mean a resource is gone - do not delete or "fix" records based on a single failed request.

## Updating existing entries

Edit the existing `.md` file in place. Keep the same `id`. Add evidence for any new claims, re-run `validate` and `generate`, and note what changed and why.

## Review

Maintainers review additions for evidence quality, domain fit, and duplicates before they become part of the archive. Pull requests are welcome; maintainers may also add entries directly - either way, validation and human review come first.
