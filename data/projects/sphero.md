---
id: sphero
name: Sphero
description: Connected robot toys including the BB-8 droid. Raised over $120 million.
domain: hardware
tags: [robotics, consumer, startup-weekend]
event:
  name: Startup Weekend Boulder
  year: 2010
links:
  official: https://www.sphero.com/
evidence:
  - url: https://startupweekend.boston/alumni
    supports: "Startup Weekend Boulder 2010 origin and funding"
deep_dive: true
key_idea: >-
  Keep the robot simple and put the intelligence in the phone, so the hardware can stay cheap and the behavior can keep changing.
learn_from: >-
  Split a hardware product at the boundary that changes fastest. Ship the update to the app, not the device.
verified_at: 2026-10-24
---

## What it does

Sphero makes connected rolling robots, including the BB-8 toy. The product is a sealed sphere that drives, lights up, and is controlled from a phone.

## The key insight

The robot is deliberately dumb. It contains motors, a battery, a radio, and enough firmware to execute commands. The phone holds the interface, the games, and the behavior logic.

That split means new behavior ships as an app update. The hardware does not need to be redesigned when someone invents a new way to use it, and the bill of materials stays low because the device carries no display and no general-purpose compute.

## How it works

Inside the sphere, two wheels drive against the inner shell. Steering comes from the difference in wheel speeds, and the center of mass sits low so the robot self-rights. A sphere with two driven wheels has no front, which is why the robot can move in any direction without turning first.

An inertial measurement unit reports orientation and acceleration. The firmware uses it to hold a heading and to report collisions. The phone uses it to render motion and to score games.

The radio link carries short commands: set speed, set color, play a sound, read sensors. The protocol is small because the device is not streaming video or running a language runtime. Latency matters more than bandwidth, since the user is steering.

The SDK exposes those commands to third-party developers. Sphero's educational line leans on the same idea: the robot is an output device, and the programming happens in an app or a block-based editor.

## Build something similar

Build a two-wheeled robot in a clear sphere, or simulate one. Expose three commands over a wireless link: drive with a heading and speed, set an LED color, read the IMU.

Put the control loop on the phone. Draw a joystick, map it to a heading and speed, and send the command at a fixed rate.

Then add one behavior that lives entirely in the app, such as a patrol route or a reaction to being picked up. If you can change that behavior without touching firmware, the split is working.

## Sources

Startup Weekend origin and funding are linked in the evidence field.
