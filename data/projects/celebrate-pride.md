---
id: celebrate-pride
name: Celebrate Pride
description: Rainbow profile picture filter. 26 million users in the first weekend. Intern hackathon project shipped globally in 72 hours.
domain: social
tags: [facebook, lgbtq, internal-hack-week]
event:
  name: Facebook Hackathon
  organizer: Facebook
  year: 2015
evidence:
  - url: https://engineering.fb.com/2015/07/02/android/72-hours-to-launch-celebrate-pride/
    supports: "Facebook hackathon origin, 26M users, 72-hour ship"
deep_dive: true
key_idea: >-
  Ship one gesture, a rainbow overlay on a profile photo, and let users supply the meaning.
learn_from: >-
  When the moment is the deadline, cut scope to a single action and make it work at full traffic.
verified_at: 2026-10-24
---

## What it does

Celebrate Pride let Facebook users apply a rainbow filter to their profile picture. It shipped in 72 hours around a hackathon and reached roughly 26 million users in its first weekend.

## The key insight

The feature is a filter, not a campaign site. It reused a surface every user already had, the profile photo, and changed one property of it. There was no new page to visit and no new account to create.

That is why it could spread in a weekend. The action was one tap, and the result was visible to everyone who looked at the profile.

## How it works

The client offers a toggle on the existing profile picture flow. Choosing it sends the image reference to a service that composites the overlay and returns a new image. The original photo stays intact, so the change is reversible.

The image work is the bottleneck. Millions of users applying the same overlay within hours means the compositing step has to be cheap and the result has to be cacheable. The overlay is a fixed asset, so the output can be produced once per photo and served from cache rather than recomputed per view.

Client support is the second constraint. The feature has to appear on every platform that shows a profile picture, which means the toggle and the result must be represented in the shared profile model rather than in one client's local state.

Timeboxing shaped the architecture. A 72-hour window rules out new infrastructure, so the team built on existing image and profile services. The constraint produced a simpler design than a greenfield build would have.

## Build something similar

Pick a surface every user already has, such as an avatar, a banner, or a display name. Add one reversible variant of it.

Precompute the variant as a static asset and serve it from cache. Then add the toggle to the shared user model so every client sees the same state.

Measure how long it takes a new user to reach the changed state. If it is more than a couple of taps, the feature is too expensive to spread.

## Sources

Engineering writeup, user count, and 72-hour timeline are linked in the evidence field.
