# Contributing

Thanks for helping improve the Hackathon Project Archive.

## Ground rules

1. **Evidence before claims.** Every award, technology, metric, and architectural claim must be backed by a traceable source recorded in `data/evidence/`.
2. **No fabrication.** Never invent awards, repositories, metrics, or capabilities. If you cannot verify it, mark it unknown or unverified.
3. **One canonical record per project.** A project that appears at multiple events is one project with multiple participations, not multiple projects.
4. **Popularity is not quality.** Keep popularity metrics separate from documentation quality and educational value.
5. **Reviewable changes.** Open a pull request; do not push to `main`.

## Adding or updating a project

1. Read `docs/data-model.md` and `docs/verification-policy.md`.
2. Create or edit the structured record under `data/projects/`, plus any related `data/repositories/`, `data/events/`, `data/participations/`, `data/evidence/`, and `data/metrics/` files.
3. Add evidence records for important claims. Each evidence record names the claim it supports and links a source URL.
4. Assign qualitative labels only when the definitions in `docs/labeling-methodology.md` are satisfied.
5. Run the validators:

   ```bash
   python -m hpa validate
   python -m pytest
   ```

6. If a guide is added, make sure it passes its publication gate (`docs/verification-policy.md`). Guides that fail the gate must not be published.

## Discovery / research runs

Research is on-demand only. To run the pipeline:

```bash
python -m hpa research --adapter fixture --input tests/fixtures/candidates.json
python -m hpa research --adapter github --query "topic:hackathon stars:>500" --limit 5
```

See `docs/agent-workflow.md` for the full workflow.

## Pull request checklist

- [ ] Structured records pass `python -m hpa validate`.
- [ ] Tests pass (`python -m pytest`).
- [ ] Every important claim has an evidence record with a real, traceable URL.
- [ ] No secrets, tokens, or credentials are included.
- [ ] No external source code is copied into this repository.
- [ ] Qualitative labels follow `docs/labeling-methodology.md`.
