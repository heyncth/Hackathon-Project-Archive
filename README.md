# Hackathon Project Archive

A public, English-language archive of hackathon projects that either won an
award or became notable through community interest, technical merit, or
educational value.

This is more than a link list: every record is structured, evidence-tracked,
classified with documented qualitative labels, and validated automatically.

## What you can do here

- Discover noteworthy hackathon projects by event, category, technology,
  award, and educational value.
- Understand what each project does and why it matters.
- Find original repositories, demos, and documentation.
- Learn about verified technologies and, where evidence supports it,
  engineering design.
- Recreate similar projects via reconstruction guides when no original
  repository exists.

## Repository layout

```
hackathon-project-archive/
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE                    # licensing decision intentionally open
├── docs/                      # policies and methodology
├── sources/sources.yaml       # editable discovery-source registry
├── data/                      # canonical structured records (source of truth)
│   ├── projects/
│   ├── repositories/
│   ├── events/
│   ├── participations/
│   ├── evidence/
│   ├── metrics/
│   └── guides/
├── guides/                    # generated / authored Markdown
│   ├── overviews/
│   ├── case-studies/
│   └── rebuild/
├── schemas/                   # JSON Schemas for every entity
├── templates/                 # guide templates
├── scripts/
├── src/hpa/                   # pipeline package
├── tests/                     # offline tests (mocks/fixtures)
└── .github/                   # issue and PR templates
```

## Quick start

```bash
# Install (editable) — or just run from the repo with PYTHONPATH=src
pip install -e ".[dev]"

# Validate all structured data
python -m hpa validate

# Run the pipeline on offline fixtures (no network needed)
python -m hpa research --adapter fixture --input tests/fixtures/candidates.json

# Run tests
python -m pytest
```

## Core principles

- **Evidence before claims** — important claims link to traceable sources.
- **No fabrication** — awards, metrics, and capabilities are never invented.
- **One canonical record per project** — multi-event projects are not duplicated.
- **Popularity is not quality** — tracked separately from documentation and
  educational value.
- **Explicit uncertainty** — missing or disputed information is represented
  honestly.

## Documentation

- [Data model](docs/data-model.md)
- [Source policy](docs/source-policy.md)
- [Verification policy & publication gates](docs/verification-policy.md)
- [Labeling methodology](docs/labeling-methodology.md)
- [Agent / research workflow](docs/agent-workflow.md)
- [Contributing](CONTRIBUTING.md)

## Licensing

See [LICENSE](LICENSE). The licensing of repository code, curated data, and
authored guides is intentionally **undecided**; components will be licensed
separately once maintainers decide. External projects remain under their own
licenses; this archive links to original sources and does not redistribute
their code.
