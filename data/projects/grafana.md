---
id: grafana
name: Grafana
description: Open-source analytics and interactive visualization platform for metrics, logs, and dashboards.
domain: developer-tools
tags: [observability, dashboards, open-source, monitoring, playable]
event:
  name: Christmas hackathon
  year: 2013
links:
  official: https://grafana.com
  source: https://github.com/grafana/grafana
  demo: https://play.grafana.org
authors:
  - Torkel Ödegaard
evidence:
  - url: https://kubernetespodcast.com/episode/122-grafana
    supports: "Creator Torkel Ödegaard: \"it started as a Christmas hackathon\""
  - url: https://grafana.com/blog/the-story-of-grafana-documentary-from-one-developers-dream-to-20-million-users-worldwide
    supports: "First commit December 25, 2013 by Torkel Ödegaard"
deep_dive: true
key_idea: >-
  Separate the visualization layer from the data source so any backend can plug in.
learn_from: >-
  Solve your own pain point first, then abstract the interface when you add the second integration.
verified_at: 2026-10-24
---

## What it does

Grafana renders time-series data from multiple backends into dashboards. It connects to Prometheus, InfluxDB, Elasticsearch, and dozens of other data sources through a plugin model.

## The key insight

Torkel Odegaard built it during a Christmas hackathon in 2013 because he wanted to see his own metrics. The architectural decision that made it succeed: separate the visualization layer from the data source. Any backend can be a plugin.

## How it works

Grafana has three main pieces: the panel, the data source, and the dashboard.

A **panel** is a single visualization (a graph, a table, a stat). It knows how to draw itself but not where the data comes from. It asks a data source for a query result, then renders whatever comes back.

A **data source** is a plugin that knows how to talk to one backend. Prometheus has one, InfluxDB has one, and you can write your own. Each implements the same interface: take a query, return time-series data in a standard format.

A **dashboard** is a collection of panels with shared time ranges and variables. Change the time picker and every panel re-queries its data source with the new range.

The plugin model is the leverage. Adding support for a new database does not require changing any visualization code. You write one adapter, and every panel type works with it.

## Build something similar

Start with a web app that renders a chart from one data source. Define a simple interface: `query(range)` returns a list of `(timestamp, value)` pairs.

Add a second data source behind the same interface. The moment you have two, you have the core of Grafana. The third and tenth take the same effort as the second.

The hard part is not the charting. It is designing the query interface wide enough that different backends can implement it without contorting their natural query language.

## Sources

Origin story and architecture are described in the Grafana documentary and podcast interviews linked in the evidence field.
