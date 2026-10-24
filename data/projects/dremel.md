---
id: dremel
name: Dremel
description: Interactive ad-hoc analysis over big data. Became the foundation for Google BigQuery.
domain: developer-tools
tags: [bigdata, google, internal-hack-week]
event:
  name: Google 20% Time
  organizer: Google
  year: 2006
notes: Built by Andrey Gubarev as a 20% project
evidence:
  - url: https://en.wikipedia.org/wiki/20%25_Project
    supports: "Google 20% project origin and BigQuery connection"
verified_at: 2026-10-24
---

## What it is

Dremel is a system for interactive ad-hoc analysis over very large datasets. It stores data in a columnar format and evaluates queries across many machines.

## The problem

Analysts wanted answers in seconds from tables too large for one machine. Batch systems could do the work but not at the speed of a question.

## What makes it interesting

It started as a Google 20% project in 2006 and became the foundation for BigQuery. The design choice that mattered was treating a query as a tree that can be pushed down to many servers, rather than moving the data to one.

## What you can learn

Interactive analysis is an architecture decision, not a UI one. If the query cannot be split, no interface will make it fast.

## Limitations of this analysis

The record does not cover the paper's design details, the query language, or the path from internal system to Cloud product.
