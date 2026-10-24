---
id: screencheat
name: Screencheat
description: Split-screen first-person shooter where all players are invisible, so you must cheat by looking at their screens. Released on Steam, PS4, Xbox One.
domain: games
tags: [game-jam, local-multiplayer, fps]
event:
  name: Global Game Jam 2014
  organizer: Melbourne site
links:
  official: https://screencheatgame.com/
evidence:
  - url: https://globalgamejam.org/ggj-success-stories
    supports: "GGJ 2014 Melbourne origin and console releases"
verified_at: 2026-10-24
---

## What it is

Screencheat is a split-screen shooter where every player is invisible. You find opponents by looking at their quarter of the screen.

## The problem

Split-screen shooters assume each player sees only their own view. Screen looking is treated as cheating, and games hide information to prevent it.

## How the experience works

Four players share one screen. Since no one is visible, the only way to locate a target is to read the other panels: map geometry, weapon fire, the position of the camera.

## What makes it interesting

It was built at Global Game Jam 2014 in Melbourne, then released on Steam, PlayStation 4, and Xbox One. The design turns an unsolvable hardware constraint into the rule of the game. You cannot stop players from looking at each other's screens, so the game is built on it.

## What you can learn

When a limitation cannot be removed, make it the mechanic. The cheapest fix is often a rule change rather than a technical one.

## Limitations of this analysis

The record does not describe the netcode or how the console versions handle four-player split-screen performance.
