---
id: buck-build-system
name: Buck
description: Fast modular Android build system used at Facebook. Prototype built in one hackathon.
domain: developer-tools
tags: [android, build-tools, facebook, internal-hack-week]
event:
  name: Camp Hack-a-Thona
  organizer: Facebook
  year: 2012
evidence:
  - url: https://engineering.fb.com/2013/05/14/android/buck-how-we-build-android-apps-at-facebook/
    supports: "Hack-a-Thona July 2012 prototype origin"
deep_dive: true
key_idea: >-
  Describe a build as a graph of declared targets, then execute and cache each node independently.
learn_from: >-
  Find the bottleneck you can measure, then remove the mechanism that causes it. Build tools win on correctness and speed, not features.
verified_at: 2026-10-24
---

## What it does

Buck is a build system for large codebases, built at Facebook for Android. It reads declarative build files, constructs a dependency graph, and executes independent work in parallel with caching.

## The key insight

The prototype came out of a Facebook hackathon in 2012 because the Android build had become the slowest part of the developer loop. The fix was not a faster compiler. It was removing hidden dependencies so that work could be parallelized and reused.

A build that recompiles the world on every change cannot be made fast by optimizing the compiler. It has to be restructured.

## How it works

Build files declare targets: a library, a binary, a test, each with sources, dependencies, and rules. The declarations are explicit, so the tool can compute the full graph without scanning the filesystem for implicit inputs.

From the graph, Buck derives the work. Independent nodes run concurrently. A node whose inputs and rule have not changed is skipped entirely, which is why incremental builds are fast even when the graph is large.

Caching extends the skip across machines. If a target's inputs hash to a known value, the output can be fetched instead of rebuilt. This turns a build into a lookup for most nodes and a compile for the few that changed.

Correctness depends on the dependency declarations being complete. An undeclared dependency produces a build that works locally and fails in a clean checkout, so the tool enforces strictness rather than tolerating implicit inputs.

For Android specifically, the system also split application packaging from code compilation. Resources and code can be updated independently, which shortens the install cycle during development.

## Build something similar

Write a build file format with three fields: inputs, outputs, and a command. Parse it into a graph.

Run the graph in topological order, skipping any node whose inputs are unchanged. Time a rebuild after touching one file. That number is the whole point of the tool.

Then add a content hash for each output and a cache directory keyed by hash. If a clean build can reuse entries from a previous one, you have the core of a modern build system.

## Sources

Facebook engineering writeup and hackathon origin are linked in the evidence field.
