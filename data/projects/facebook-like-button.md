---
id: facebook-like-button
name: Facebook Like button
description: One-click social interaction feature that let users express approval of posts, photos, and pages across the web.
domain: social
tags: [social-network, engagement, web]
event:
  name: Facebook internal hackathon
  year: 2007
links:
  official: https://en.wikipedia.org/wiki/Like_button
evidence:
  - url: https://www.fastcompany.com/90780140/the-full-story-of-the-like-button
    supports: "The Like button originated at a Facebook internal hackathon in summer 2007; Justin Rosenstein built the prototype codenamed 'Props'"
deep_dive: true
key_idea: >-
  Reduce approval to one bit and one click, then make that click available on any page on the web.
learn_from: >-
  The most portable interaction is the smallest one. A single bit can cross every surface you own.
verified_at: 2026-10-24
---

## What it does

The Like button is a one-click signal of approval attached to posts, photos, pages, and eventually other sites. It turned a private bookmark-style action into a public, countable metric.

## The key insight

Justin Rosenstein built a prototype called "Props" at a Facebook internal hackathon in 2007. It sat unused for roughly two years. When it launched in 2009, the important decision was not the icon. It was scope: one bit of feedback, applied to everything, with the count visible to everyone.

A five-point rating would have carried more information and spread less. One bit is cheap to give, cheap to display, and comparable across objects of different kinds.

## How it works

On Facebook, a Like is a row in a social graph with a user, an object, and a type. Counting is a read over that edge set, which is why the number can be shown on every post without a separate counter to keep in sync.

Off the main site, the button ships as a small snippet that renders a cross-origin frame. The frame isolates the host page's CSS from Facebook's, and it carries the session needed to attribute the click. That isolation is why the same few lines of embed code work on a blog, a news site, and a product page.

Aggregation is the hard part. A popular page can produce far more writes than reads, and the count has to survive that ratio. Caching and precomputed totals absorb most of the load, with the exact value reconciled in the background.

The visual language mattered as much as the mechanism. A thumb, a count, and a consistent position trained users across unrelated sites. The button became recognizable before it became useful on any particular page.

## Build something similar

Add one-bit feedback to something you already run. A row with a user id, an object id, and a timestamp is enough.

Show the count next to the control, and make the control work on a second surface, such as an embed or a second client. The moment two surfaces share the same edge table, you have the core of the system.

Then measure the ratio of writes to reads on a popular item. That number decides whether you need a cache, a queue, or nothing at all.

## Sources

Origin and prototype details are linked in the evidence field.
