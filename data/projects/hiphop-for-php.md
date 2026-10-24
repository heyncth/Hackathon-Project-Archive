---
id: hiphop-for-php
name: HipHop for PHP
description: PHP to C++ compiler that reduced CPU usage by approximately 50%. Open-sourced in February 2010.
domain: developer-tools
tags: [php, compiler, facebook, internal-hack-week]
event:
  name: Facebook Hackathon
  organizer: Facebook
  year: 2010
notes: Built by Haiping Zhao
evidence:
  - url: https://techcrunch.com/2010/02/02/facebook-hiphop-presentation/
    supports: "Facebook hackathon origin, Haiping Zhao, CPU savings"
deep_dive: true
key_idea: >-
  Translate PHP into C++ ahead of time, so the same code runs without paying interpreter cost per request.
learn_from: >-
  A code generator plus a compatibility layer can buy years of headroom while you build the real runtime.
verified_at: 2026-10-24
---

## What it does

HipHop for PHP converts PHP source into C++ and compiles the result. Facebook ran its PHP web tier through it and reported roughly half the CPU usage for the same work.

## The key insight

Facebook did not want to rewrite the site. The team wanted the existing PHP codebase to run faster without a language migration. HipHop keeps PHP as the source language and moves the cost from request time to build time.

That trade is the whole idea. Compilation is slow and awkward, but it happens once. Interpretation happens on every request.

## How it works

The compiler parses PHP, builds an abstract syntax tree, and generates C++ that calls a runtime library for dynamic behavior. PHP is dynamically typed, so the generated code cannot assume types. The runtime provides the operations that need them: array access, string conversion, method dispatch.

Static analysis recovers what it can. Where a variable's type is provable, the generated C++ uses a concrete type. Where it is not, the code falls back to a generic path. The ratio between the two determines how much speed the build actually buys.

The output is compiled with a normal C++ toolchain and linked against the HipHop runtime. Deployment ships a binary instead of a directory of scripts, which changes the release process as much as it changes performance.

Compatibility is the long tail. PHP's behavior in edge cases is defined by its interpreter, and a reimplementation has to match it closely enough that production code does not change meaning. Each mismatch is a bug that only appears on a specific code path.

The project later gave way to HHVM, a virtual machine with a JIT. That design keeps the dynamic language and recovers speed at runtime, which removed the build step that made HipHop expensive to operate.

## Build something similar

Take a small language or a configuration format and compile it to a language you already run. Start with arithmetic, variables, and function calls.

Generate code, compile it, and compare the output against an interpreter for the same program. Then add one dynamic feature, such as a dictionary with mixed value types, and watch the generated code lose its static types.

That moment shows where the real work lives. The compiler is straightforward. Matching the dynamic semantics is the project.

## Sources

Origin, author, and CPU savings are linked in the evidence field.
