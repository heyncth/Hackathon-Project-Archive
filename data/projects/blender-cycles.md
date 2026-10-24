---
id: blender-cycles
name: Blender Cycles
description: Physically based render engine built into Blender. Creator Brecht Van Lommel worked on Blender via early Google Summer of Code.
domain: media-arts
tags: [rendering, blender, open-source, gsoc]
event:
  name: Google Summer of Code
  organizer: Google
  year: 2009
links:
  official: https://www.blender.org/features/rendering/
  source: https://projects.blender.org/blender/blender
evidence:
  - url: https://www.blendernation.com/2019/09/30/see-the-neat-new-blender-features-from-google-summer-of-code-2019/
    supports: "GSoC connection, Brecht Van Lommel, 100+ Blender projects funded"
deep_dive: true
key_idea: >-
  Simulate light transport instead of approximating it with shader tricks, and let samples trade time for accuracy.
learn_from: >-
  A physically based core can ship inside an existing tool if the integration is one engine behind an existing interface.
verified_at: 2026-10-24
---

## What it does

Cycles is a physically based render engine inside Blender. It traces light paths from the camera through the scene and produces images where reflections, shadows, and indirect light come from the same simulation instead of separate fakes.

## The key insight

Rasterizers approximate light with shortcuts: shadow maps, reflection probes, ambient terms. Cycles does the opposite. It samples paths and averages them. Noise is not a bug, it is the visible cost of sampling, and it falls as the sample count rises.

That choice makes the engine predictable. A material that looks right in one scene tends to look right in another, because the same physical rules apply.

## How it works

A path tracer shoots rays from the camera. At each surface it chooses a bounce direction, weights the contribution, and continues. When a ray reaches a light or the background, the path contributes to the pixel. Many paths per pixel produce the estimate.

Importance sampling decides where to send rays. Instead of sampling uniformly, the integrator samples directions that are likely to matter, such as toward a light or along a glossy lobe. Good sampling means fewer paths for the same noise level.

Acceleration structures make ray traversal practical. A bounding volume hierarchy groups geometry so a ray can skip most of the scene. Without it, every bounce would test every triangle.

Materials are node graphs compiled into shader code. The graph describes the surface, and the renderer evaluates it at each hit. Because the description is procedural, the same material works in Cycles and, where supported, in the real-time engine.

GPU rendering splits the same work across many cores. The integrator is data-parallel by design, which is why the same engine runs on CPU and GPU with different performance rather than different output.

## Build something similar

Write a path tracer for spheres and a plane. Camera ray, intersect, bounce, accumulate. Render at one sample per pixel and look at the noise.

Add importance sampling for the light. The image should get cleaner without more samples.

Then add one material property, such as roughness, and watch the highlight widen. The whole engine is an accumulation of these small physical decisions, which is why a minimal version teaches more than a feature-complete one.

## Sources

GSoC connection and project history are linked in the evidence field.
