---
id: hollow-knight
name: Hollow Knight
description: Metroidvania set in a ruined insect kingdom. Team Cherry's jam prototype seeded the full game.
domain: games
tags: [game-jam, metroidvania, indie, unity, open-source]
event:
  name: Ludum Dare 27
  year: 2013
  award: Theme "Ten seconds" entry
links:
  official: https://hollowknightgame.com/
  source: https://github.com/teamcherry/HollowKnight
evidence:
  - url: https://gamemaker.io/en/blog/best-game-jam-games
    supports: "Ludum Dare 27 origin and Team Cherry development history"
deep_dive: true
key_idea: >-
  Keep the tone and movement from the jam build, and rebuild everything around them at full scale.
learn_from: >-
  A jam is a test of feel, not a test of content. Ship the smallest thing that proves the mood, then start over on systems.
verified_at: 2026-10-24
---

## What it does

Hollow Knight is a metroidvania set in a ruined underground kingdom. You play a small knight with a nail, explore interconnected rooms, and unlock movement abilities that open routes you could see but not reach earlier.

## The key insight

The project started as a Ludum Dare 27 entry in 2013, built in a weekend around the theme "ten seconds." What survived from that build was not its content. It was the feel: a small figure moving through a dark, hand-drawn space.

Team Cherry kept that and rebuilt the rest over several years. The jam version proved the tone cheaply. The commercial game needed a much larger map, a combat system, and a save structure, and none of those fit in a weekend.

## How it works

The map is a graph. Each room is a node, each exit is an edge, and most edges are gated by either an ability or a key item. Designers place gates so that the player passes a locked route early and remembers it. Later, a new ability turns the remembered route into progress.

Combat is built on spacing and timing rather than combos. The nail has a short range, the dash moves a fixed distance, and healing takes time during which the player is vulnerable. Every fight is a negotiation between dealing damage and buying the moment to heal.

The charm system is a loadout constraint. Charms modify health, damage, movement, or summon behavior, but you can only equip as many as your notch count allows. The constraint turns a large set of upgrades into a build decision instead of a checklist.

Saving happens at benches. A bench restores health and respawns enemies, so progress and risk are tied to a physical location rather than a menu.

## Build something similar

Start with one room and one movement verb. Make the character move, jump, and attack. Tune the acceleration, the jump arc, and the attack recovery until moving through an empty room feels good on its own.

Then build three rooms with one gate. Put an item behind the gate that the player can see but not reach. Add the ability that opens it. If the return trip feels like a reward rather than a chore, the core loop works.

Add a bench before adding a boss. Saving is the pacing device that makes the rest tolerable.

## Sources

Jam origin and development history are linked in the evidence field.
