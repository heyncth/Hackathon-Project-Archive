---
id: figma-slides
name: Figma Slides
description: Presentation design tool built on Figma's collaborative canvas, letting teams create and present slide decks together in real time.
domain: web-mobile
tags: [design, collaboration, presentations]
event:
  name: Figma Maker Week
  year: 2023
links:
  official: https://www.figma.com/slides
evidence:
  - url: https://newsletter.pragmaticengineer.com/p/building-figma-slides-with-noah-finer
    supports: "Figma Slides started as a hackathon project; initial development took about 6 months starting at a hackathon in late 2023"
  - url: https://review.firstround.com/how-to-make-your-product-idea-go-viral-inside-your-company-lessons-from-figma-slides
    supports: "Figma Slides originated at Maker Week, Figma's internal hackathon"
deep_dive: true
key_idea: >-
  Reuse the canvas, the document model, and the multiplayer engine, then add only the slide layer.
learn_from: >-
  The fastest new product borrows an existing engine. Ship the delta, not a second platform.
verified_at: 2026-10-24
---

## What it does

Figma Slides is a presentation tool built on Figma's design canvas. Teams design slides with the same tools they use for interfaces, then present them in the same file.

## The key insight

The team did not build a presentation editor from scratch. It built a slide layer on top of the editor that already existed: same canvas, same document, same multiplayer session, same component system.

That reuse set the schedule. The hackathon project at Figma's Maker Week in late 2023 became a shipped product in about two years, which is short for a new surface with its own editing model.

## How it works

A deck is a Figma document. Each slide is a frame, and the slide grid is a layout constraint over those frames rather than a separate data structure. Because slides are frames, every existing design tool works on them: auto layout, components, styles, images.

Editing is shared state. Multiple cursors and selections already work because the multiplayer layer operates on the document, not on a screen. Adding a presenter view means adding a way to read the same document, not a new sync protocol.

The slide-specific parts are narrow: a grid that arranges frames in order, a presenter mode that advances through them, and transitions between them. Those are additions on top of the existing model rather than a parallel implementation.

The hard part is the constraint. A design canvas is free-form, and a slide deck is sequential. The grid has to enforce order and alignment without taking away the freedom that makes the canvas useful.

## Build something similar

Take an editor you already have, or a simple canvas with draggable rectangles. Add a grid that arranges frames in reading order.

Add a presenter mode that shows one frame at a time and advances on a key press. That is a slide deck.

Then add one feature that only makes sense because the frames are editable, such as a shared component for a footer. The product becomes more than a slideshow at the point where the design tools carry over.

## Sources

Hackathon origin and development timeline are linked in the evidence field.
