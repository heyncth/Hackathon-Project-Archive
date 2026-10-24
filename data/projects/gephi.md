---
id: gephi
name: Gephi
description: Open-source network analysis and visualization tool. Described as Photoshop for network data. Google Summer of Code from 2009 to 2011 accelerated its growth.
domain: science
tags: [visualization, open-source, graph, gsoc]
event:
  name: Google Summer of Code
  organizer: Google
  year: 2009
links:
  official: https://gephi.org/
  source: https://github.com/gephi/gephi
evidence:
  - url: https://opensource.googleblog.com/2012/03/gephi-how-3-years-of-google-summer-of.html
    supports: "GSoC 2009-2011 participation and community growth"
deep_dive: true
key_idea: >-
  Treat layout as the first operation on network data, not the last step of a report.
learn_from: >-
  A visualization tool lives on its layout algorithms and its ability to open other people's data formats.
verified_at: 2026-10-24
---

## What it does

Gephi is an open-source tool for exploring and visualizing graphs. You load a network, run a layout, color and size nodes by a metric, and filter the result interactively.

## The key insight

Most graph tools at the time produced static output: compute a layout, render an image, publish it. Gephi made layout interactive. You can start a force-directed layout, watch it settle, stop it, and change a parameter while looking at the result.

That changes the work. Exploration becomes a loop of adjusting and observing rather than a batch job with a preview at the end.

## How it works

The data model is a graph with nodes, edges, and attributes, plus a separate attribute table. Metrics such as degree, betweenness, and modularity are computed into columns that can drive visual properties.

Layout algorithms are iterative. Force-directed layouts treat edges as springs and nodes as repelling charges, then repeatedly move each node by the net force. The result is a position for every node, refined over many steps rather than solved once.

Rendering is the constraint. A graph with hundreds of thousands of edges cannot be drawn naively at interactive rates, so the view culls, batches, and uses the GPU for the heavy drawing. The layout runs in the background while the view stays responsive.

Importers are the adoption path. Gephi reads edge lists, matrix formats, and database queries, because a visualization tool is only as useful as the data it can open. Google Summer of Code support from 2009 to 2011 funded much of that connector and plugin work.

## Build something similar

Load a small edge list and compute a force-directed layout yourself. Springs for edges, repulsion for all pairs, and a damping factor. Run a hundred iterations and draw the result.

Then make it interactive: a slider for repulsion, a button to stop and restart. The tool becomes useful when you can see the effect of a parameter without re-running a pipeline.

Add one metric, such as degree, and map it to node size. That single mapping turns a picture of a graph into an explanation of it.

## Sources

GSoC history and project description are linked in the evidence field.
