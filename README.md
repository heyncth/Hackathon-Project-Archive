# Hackathon Project Archive

A curated directory of notable hackathon projects across all domains and eras — from weekend prototypes at local Startup Weekend events to internal company hack weeks that turned into products used by millions.

This is an archive, not a database. Entries are chosen for technical, educational, practical, or social value. Award winners are included, and so are notable non-winners and lesser-known projects with genuine merit. Coverage favors quality and reliability over volume.

## What you'll find

Each entry answers:

- **What** the project is and does
- **Where** it was built — the hackathon, game jam, or internal hack event, when verifiable
- **Any awards or distinctions**, only when backed by evidence
- **Links** to official pages, source code, demos, and videos when they exist
- **Evidence** — public sources backing the claims in the entry

## How to browse

The [project index](#project-index) below is organized by domain. Awards appear next to the relevant entry. Every entry links out to primary resources.

Entries are curated and depend on available evidence. If a detail is unknown, it is left out rather than guessed. A missing field means the information was not verified, not that the project lacked it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for eligibility, evidence requirements, and how to add or update entries. Research happens on request only; new entries are reviewed and approved by a human before they join the archive.

## Maintenance

Project data lives in `data/projects/*.md` (YAML frontmatter + optional notes). The index below is generated — never edit it by hand.

```bash
pip install -r requirements-dev.txt
python -m archive validate   # check all project records
python -m archive generate   # regenerate the project index below
python -m archive check      # verify the index is current (read-only, CI)
python -m archive export     # optional JSON export for integrations
python -m pytest             # run the test suite
```

## Project index

<!-- BEGIN GENERATED PROJECT INDEX -->

## Civic Tech

### Ushahidi

Open-source crisis-mapping platform that crowdsources and maps eyewitness reports via SMS and the web.

- **Event:** Kenya post-election crisis rapid build — 2008 — **Award:** NetSquared Mashup Challenge winner
- **Team:** Ory Okolloh, Erik Hersman, Juliana Rotich, David Kobia
- **Links:** [Official](https://www.ushahidi.com) · [Source](https://github.com/ushahidi/platform)

## Developer Tools

### Grafana

Open-source analytics and interactive visualization platform for metrics, logs, and dashboards.

- **Event:** Christmas hackathon — 2013
- **Team:** Torkel Ödegaard
- **Links:** [Official](https://grafana.com) · [Source](https://github.com/grafana/grafana) · [Demo](https://play.grafana.org)

### Zapier

Workflow automation platform that connects web apps so users can move data between services without writing code.

- **Event:** Startup Weekend Columbia — Startup Weekend — 2011 — **Award:** Winner
- **Team:** Wade Foster, Bryan Helmig, Mike Knoop
- **Links:** [Official](https://zapier.com)

## Fintech

### 1inch

Decentralized exchange aggregator that finds the best token swap rates across DEX liquidity sources.

- **Event:** ETHGlobal New York — ETHGlobal — 2019
- **Team:** Sergej Kunz, Anton Bukov
- **Links:** [Official](https://1inch.io) · [Source](https://github.com/1inch)

## Games

### SUPERHOT Prototype

First-person shooter prototype where time moves only when the player moves, built during a seven-day game jam.

- **Event:** 7 Day FPS — 2013
- **Team:** SUPERHOT Team
- **Links:** [Official](https://superhotgame.com) · [Demo](https://superhotgame.com/prototype.html)

## Web & Mobile

### Carousell

Mobile-first classifieds marketplace where selling an item takes about a minute with a photo.

- **Event:** Startup Weekend Singapore — Startup Weekend — 2012 — **Award:** First place
- **Team:** Quek Siu Rui, Lucas Ngoo, Marcus Tan
- **Links:** [Official](https://carousell.com)

### GroupMe

Free group messaging app that works over SMS and smartphone apps, built as a hackathon project.

- **Event:** TechCrunch Disrupt New York hackathon — TechCrunch — 2010
- **Team:** Jared Hecht, Steve Martocci
- **Links:** [Official](https://groupme.com)

### Trello

Visual collaboration tool that organizes projects into boards, lists, and cards.

- **Event:** Fog Creek Creek Week — Fog Creek Software — 2011
- **Links:** [Official](https://trello.com)

### Twitter

Microblogging service for short public status updates, prototyped inside the podcasting company Odeo.

- **Event:** Odeo internal brainstorming session — Odeo — 2006
- **Team:** Jack Dorsey, Florian Weber
- **Links:** [Official](https://twitter.com)

<!-- END GENERATED PROJECT INDEX -->

## License

MIT — see [LICENSE](LICENSE). Project names and linked resources remain the property of their respective owners; this repository only catalogs them with attribution.
