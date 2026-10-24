---
id: openai-gym
name: OpenAI Gym
description: Toolkit for reinforcement learning research; described by OpenAI as not a formal hackathon project but built with rapid-iteration hackathon culture in mind.
domain: ai-ml
tags: [reinforcement-learning, open-source, research, rapid-build]
links:
  official: https://github.com/openai/gym
  source: https://github.com/openai/gym
evidence:
  - url: https://github.com/openai/gym
    supports: "OpenAI Gym repository and docs; OpenAI has stated it was not a formal hackathon project but embodied rapid-build research culture"
deep_dive: true
key_idea: >-
  Give every environment the same small interface, so one algorithm runs everywhere without adaptation.
learn_from: >-
  A boring, fixed contract creates an ecosystem. Five methods beat a clever framework.
verified_at: 2026-10-24
---

## What it does

OpenAI Gym is a standard interface for reinforcement learning environments. An agent sees an observation, picks an action, and receives a reward and a new observation. Gym defines the shape of that exchange so the same training loop can drive a cart-pole simulation, an Atari game, or a robot arm.

## The key insight

Before Gym, most papers shipped their own environment code and their own training harness. Results were hard to compare because the loop itself differed between implementations. Gym standardized the environment side of the loop and left the algorithm side alone. That is a much smaller surface than a full framework, and it was enough.

## How it works

Every environment implements the same contract:

- `reset()` returns the first observation.
- `step(action)` returns observation, reward, done, and an info dictionary.
- `action_space` and `observation_space` describe legal actions and observations.

Spaces are typed. `Discrete(4)` is a set of four actions. `Box(low, high, shape)` is a continuous array with bounds. Because the shapes are declared, an algorithm can build the right input and output layers without knowing which environment it is talking to.

Wrappers modify an environment while keeping the contract. Frame stacking, reward scaling, and time limits are all wrappers: they take an environment and return an environment. This is composition instead of configuration, and it is why third-party modifications do not require changes to the core.

Registration maps a string like `CartPole-v1` to a constructor. `gym.make` builds the environment and wraps it. Versioning in the name matters: `v0` and `v1` can differ in reward definition or episode length, and published results cite the version.

## Build something similar

Define the contract first, in fewer than ten lines. Two methods and two space objects are enough.

Build one environment with a trivial dynamic, then write a random agent that samples from the action space and prints the episode return. If the agent can run without importing anything specific to that environment, the interface works.

Then add a wrapper that changes one thing, such as stacking the last four observations. If the wrapper needs no change to the agent, the composition boundary is in the right place.

## Sources

The interface and repository are linked in the evidence field.
