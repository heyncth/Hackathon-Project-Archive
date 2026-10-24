---
id: account-kit
name: Account Kit
description: Phone-number login verification without SMS. Achieved 97% success rate in early tests.
domain: developer-tools
tags: [authentication, facebook, internal-hack-week]
event:
  name: Facebook Seattle Hackathon
  organizer: Facebook
  year: 2016
evidence:
  - url: https://engineering.fb.com/2016/12/29/developer-tools/favorite-hacks-of-2016/
    supports: "Facebook Seattle Platform team hackathon 2016"
verified_at: 2026-10-24
---

## What it is

Account Kit was a Facebook login product that verified a phone number without sending an SMS. Early tests reported a 97% success rate.

## The problem

SMS verification fails for reasons the developer cannot see: delayed messages, wrong country codes, shared phones, and carrier filtering. Each failure is a user who does not get into the app.

## What makes it interesting

It came out of the Facebook Seattle Platform team hackathon in 2016. The interesting choice is the constraint: prove the number without relying on a text message arriving.

## What you can learn

When a verification step has a high failure rate, the fix may be a different channel rather than a better error message. Measure the step, then remove its weakest dependency.

## Limitations of this analysis

The record does not explain the verification mechanism, the markets it targeted, or how the 97% figure was measured.
