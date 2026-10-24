# Hackathon Project Archive

Notable hackathon projects, with evidence.

A curated archive of projects built at hackathons, game jams, internal hack weeks, and similar rapid-build events. From weekend prototypes to products used by millions.

**[Browse the archive](https://heyncth.github.io/Hackathon-Project-Archive/)**

## What you'll find

Each entry answers:

- **What** the project is and does
- **Where** it was built: the hackathon, game jam, or internal hack event, when verifiable
- **Any awards or distinctions**, only when backed by evidence
- **Links** to official pages, source code, demos, and videos when they exist
- **Evidence**: public sources backing the claims in the entry

Award winners are included, and so are notable non-winners and lesser-known projects with genuine merit. If a detail is unknown, it is left out rather than guessed. A missing field means the information was not verified, not that the project lacked it.

## Browse

**[heyncth.github.io/Hackathon-Project-Archive](https://heyncth.github.io/Hackathon-Project-Archive/)**

Search and filter by domain, year, tags, and award status.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for eligibility, evidence requirements, and how to add or update entries. Research happens on request only; new entries are reviewed and approved by a human before they join the archive.

## Data

Project data lives in `data/projects/*.md` (YAML frontmatter + optional notes). The site and stats below are generated. Never edit them by hand.

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
**171 projects** across 16 domains · 91 with documented awards

Games (46) · Web & Mobile (23) · Science (15) · Fintech (13) · Developer Tools (10) · Hardware (8) · Healthcare (8) · Media & Arts (8) · Social Impact (7) · Accessibility (6) · Climate & Environment (6) · Education (5) · Robotics (5) · Civic Tech (4) · Other (4) · AI & Machine Learning (3)
<!-- END GENERATED STATS -->

## License

MIT. See [LICENSE](LICENSE). Project names and linked resources remain the property of their respective owners. This repository catalogs them with attribution.
