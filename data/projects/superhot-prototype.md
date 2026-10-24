---
id: superhot-prototype
name: SUPERHOT Prototype
description: First-person shooter prototype where time moves only when the player moves, built during a seven-day game jam.
domain: games
tags: [game-jam, fps, unity, prototype, playable]
event:
  name: 7 Day FPS
  year: 2013
links:
  official: https://superhotgame.com
  demo: https://superhotgame.com/prototype.html
authors:
  - SUPERHOT Team
evidence:
  - url: https://superhotgame.com/our-story
    supports: "Prototype created August 10-17, 2013 during the 7 Day First Person Shooter game jam"
  - url: https://superhotgame.com
    supports: "Original 2013 prototype still playable on the official site"
deep_dive: true
key_idea: >-
  Time advances only when the player moves, turning a first-person shooter into a puzzle game.
learn_from: >-
  One mechanical constraint can replace an entire design document. Find the constraint first.
verified_at: 2026-10-24
---

## What it does

SUPERHOT is a first-person shooter where time moves only when the player moves. Stand still and bullets hang in the air. Move and the world resumes. The 2013 jam prototype introduced this mechanic; the full game shipped in 2016.

## The key insight

The team did not set out to build a shooter. They set out to make something in seven days. The time-movement mechanic emerged from a jam constraint: make one interesting rule and build everything around it.

The mechanic does double duty. It is a puzzle rule (position yourself before time advances) and a difficulty dial (move less, survive longer). Every level design problem becomes "what does the player need to do while frozen?"

## How it works

The simulation runs on a fixed timestep, but the timestep only advances when the player provides input. The engine has two states: frozen (delta time = 0) and running (delta time = normal).

When frozen, physics does not integrate, AI does not tick, and particles pause. Bullets keep their positions because velocity integrates against delta time. Zero delta time freezes them in place.

When the player moves (WASD or mouse look), the engine switches to running. One frame of input produces one frame of simulation. When the player stops, the engine drops back to frozen.

The bullet freezing comes for free. No special-casing required: the mechanic falls out of the physics loop.

Level design is the real work. Each arena is laid out so the optimal solution involves specific movement sequences: dodge here, shoot there, reposition. The levels teach the mechanic through geometry, not tutorials.

## Build something similar

Start with a simple FPS scene: a player controller, a few enemies that shoot, and bullets that travel.

Add a pause system. When the player is not pressing movement keys, set time scale to 0. When they press a key, set it back to 1.

Test it: fire a shot, release all keys, watch the bullet stop mid-air.

Then design three arenas around the mechanic. The first should be trivial (stand still, aim, move to shoot). The second should require repositioning between shots. The third should punish standing still (enemies close in over time).

## Sources

Prototype origin and development timeline are documented at superhotgame.com/our-story, linked in the evidence field.
