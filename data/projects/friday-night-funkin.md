---
id: friday-night-funkin
name: Friday Night Funkin'
description: Open-source rhythm game where a boyfriends battles ex-rockstar dads in rap-battle-style musical face-offs.
domain: games
tags: [rhythm, open-source, viral]
event:
  name: Ludum Dare 47
  year: 2020
links:
  official: https://www.newgrounds.com/portal/view/770371
  source: https://github.com/ninjamuffin99/Funkin
evidence:
  - url: https://en.wikipedia.org/wiki/Friday_Night_Funkin%27
    supports: "Initially created for the Ludum Dare 47 game jam on October 5, 2020"
  - url: https://github.com/FunkinCrew/Funkin/blob/v0.2.7.1/README.md
    supports: "Official repo states the game was originally made for Ludum Dare 47 'Stuck In a Loop'"
  - url: https://ninja-muffin24.itch.io/friday-night-funkin/devlog/184825/friday-night-funkin-going-forward
    supports: "Developer ninjamuffin99's devlog describing the Ludum Dare 47 release and its rapid viral spread"
deep_dive: true
key_idea: >-
  A rhythm game is a chart plus a clock. Everything else is presentation, and presentation can be replaced.
learn_from: >-
  Keep the core loop tiny and the content format open, and a community will build the rest.
verified_at: 2026-10-24
---

## What it does

Friday Night Funkin' is a rhythm game where you press arrow keys in time with music while a opponent sings against you. It started as a Ludum Dare 47 entry in October 2020 and became a viral hit with a large modding scene.

## The key insight

Rhythm games have a small mechanical core: notes arrive on a timeline, the player hits them within a timing window, and the game scores the difference. The jam build implemented that core and wrapped it in characters and music.

The team open-sourced the game. The chart format and the asset layout were readable, so modders could add songs and characters without reverse-engineering the engine. Most of the game's long tail came from that decision.

## How it works

Audio position is the clock. The game tracks the current playback time of the song and spawns notes whose timestamps fall inside the visible window. Judgement compares the time of the key press against the note's timestamp and assigns a rating from the offset.

A chart is a sequence of notes with timestamps, lanes, and lengths for holds. Splitting the chart from the song file means a new track is data, not code.

The engine is written in Haxe and targets multiple platforms through OpenFL. That choice gives one codebase for desktop and web, which matters when the audience arrives through a browser game portal.

Modding works because assets and charts are loaded from a known directory structure. A mod is a folder with a song, a chart, and sprites. The game reads the folder and plays it, with no plugin API required.

## Build something similar

Build the clock first. Load an audio file, display its playback time, and draw a marker that moves with it.

Add notes with timestamps. Spawn each note a fixed number of seconds before its time and move it toward a hit line. On a key press, compare the current time to the nearest note's timestamp and print the offset.

Then move the notes into a JSON file. When you can add a song by editing data instead of code, you have the same extension point that made modding possible.

## Sources

Ludum Dare origin, repository, and developer devlog are linked in the evidence field.
