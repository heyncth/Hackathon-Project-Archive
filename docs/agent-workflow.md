# Agent Workflow

How an autonomous agent (or a human) runs research and updates the archive.

## When research runs

Research is **on-demand only**. No scheduled or continuous discovery jobs in
the MVP. A run is triggered by an explicit user request or command.

## Pipeline stages

1. **Request** — user invokes `python -m hpa research ...` with a query and
   adapter selection.
2. **Registry** — load `sources/sources.yaml`.
3. **Discovery** — adapters search configured sources; failures are recorded
   per source and do not abort the run.
4. **Normalize** — raw candidates become structured fields with explicit
   nulls for unknowns.
5. **Verify** — important claims are checked against evidence; evidence
   status is assigned.
6. **Deduplicate** — candidates are matched against existing records by
   normalized name and repository URL.
7. **Persist** — canonical records are created or updated idempotently under
   `data/`.
8. **Label** — qualitative labels assigned per `docs/labeling-methodology.md`.
9. **Gates** — publication gates decide which guides may be written.
10. **Generate** — Markdown overviews/guides generated deterministically from
    structured data.
11. **Validate** — schema, referential integrity, duplicate, label, and
    guide-gate checks run.
12. **Report** — a run summary is printed; a branch/PR is prepared when the
    environment supports it.

## Entry point

```bash
# Fixture-driven run (no network; used by tests and offline demos)
python -m hpa research --adapter fixture --input tests/fixtures/candidates.json

# Live GitHub search (uses GITHUB_TOKEN if set)
python -m hpa research --adapter github --query "topic:hackathon stars:>500" --limit 5

# Standalone validation of the current data/ tree
python -m hpa validate

# Regenerate Markdown from structured data
python -m hpa generate
```

## Module layout

| Module | Responsibility |
|---|---|
| `hpa.registry` | Load and index the source registry. |
| `hpa.adapters.base` | `SearchAdapter` interface. |
| `hpa.adapters.github` | GitHub repository search. |
| `hpa.adapters.devpost` | Devpost public gallery search (best-effort HTML parsing). |
| `hpa.adapters.fixture` | Reads candidates from a local JSON file (tests/offline). |
| `hpa.normalize` | Candidate → structured record fields. |
| `hpa.verify` | Evidence status assignment. |
| `hpa.dedupe` | Duplicate detection and matching. |
| `hpa.label` | Qualitative label rules. |
| `hpa.gates` | Publication gate checks. |
| `hpa.generate` | Deterministic Markdown generation. |
| `hpa.validate` | All automated checks. |
| `hpa.pipeline` | Orchestrates the stages above. |
| `hpa.cli` | Command-line interface. |

## Failure handling

- A source that cannot be accessed is recorded in the run report with the
  error. The pipeline continues with other sources.
- Inaccessible ≠ non-existent. Never delete a record solely because a URL
  could not be checked.
- Re-running the pipeline with unchanged inputs must not create duplicate
  records or unnecessary diffs.

## Security

External pages and repositories are untrusted data. Never execute third-party
project code during discovery or validation. Never place secrets in repo
files or logs.
