# Hackathon Project Archive

Notable hackathon projects, with evidence.

A curated archive of projects built at hackathons, game jams, internal hack weeks, and similar rapid-build events — from weekend prototypes to products used by millions.

**[Browse the archive →](https://heyncth.github.io/Hackathon-Project-Archive/)**

## What you'll find

Each entry answers:

- **What** the project is and does
- **Where** it was built — the hackathon, game jam, or internal hack event, when verifiable
- **Any awards or distinctions**, only when backed by evidence
- **Links** to official pages, source code, demos, and videos when they exist
- **Evidence** — public sources backing the claims in the entry

Award winners are included, and so are notable non-winners and lesser-known projects with genuine merit. If a detail is unknown, it is left out rather than guessed. A missing field means the information was not verified, not that the project lacked it.

## Browse

**[→ heyncth.github.io/Hackathon-Project-Archive](https://heyncth.github.io/Hackathon-Project-Archive/)**

Search and filter by domain, year, tags, and award status.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for eligibility, evidence requirements, and how to add or update entries. Research happens on request only; new entries are reviewed and approved by a human before they join the archive.

## Data

Project data lives in `data/projects/*.md` (YAML frontmatter + optional notes). The site and stats below are generated — never edit them by hand.

```bash
pip install -r requirements-dev.txt
python -m archive validate   # check all project records
python -m archive generate   # build site + update stats
python -m archive check      # verify output is current (read-only, CI)
python -m archive export     # JSON export
python -m pytest             # run the test suite
```

## Stats

<!-- BEGIN GENERATED STATS -->
**101 projects** across 16 domains · 59 with documented awards

Games (32) · Web & Mobile (14) · Fintech (9) · Healthcare (6) · Developer Tools (5) · Robotics (5) · Education (4) · Science (4) · Other (4) · Civic Tech (3) · Climate & Environment (3) · Media & Arts (3) · Social Impact (3) · Accessibility (2) · AI & Machine Learning (2) · Hardware (2)
<!-- END GENERATED STATS -->

## License

MIT — see [LICENSE](LICENSE). Project names and linked resources remain the property of their respective owners; this repository only catalogs them with attribution.
