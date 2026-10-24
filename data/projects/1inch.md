---
id: 1inch
name: 1inch
description: Decentralized exchange aggregator that finds the best token swap rates across DEX liquidity sources.
domain: fintech
tags: [defi, ethereum, dex, web3, open-source]
event:
  name: ETHGlobal New York
  organizer: ETHGlobal
  year: 2019
links:
  official: https://1inch.io
  source: https://github.com/1inch
authors:
  - Sergej Kunz
  - Anton Bukov
evidence:
  - url: https://1inch.io/press-room
    supports: "History began at the ETHGlobal hackathon in New York, May 2019; 56-hour prototype"
  - url: https://1inch.com/blog/post/looking-back-on-5-years-of-innovation-1inch-in-2019-2
    supports: "Built the first DEX aggregation protocol prototype at ETHGlobal NYC, May 19, 2019"
  - url: https://en.wikipedia.org/wiki/1inch
    supports: "Founded May 2019 at the ETHGlobal hackathon in New York City"
deep_dive: true
key_idea: >-
  Split one swap across multiple exchanges to get a better average price than any single venue offers.
learn_from: >-
  A hackathon prototype that solves one measurable problem (price slippage) can become infrastructure when the measurement matters to everyone.
verified_at: 2026-10-24
---

## What it does

1inch is a decentralized exchange (DEX) aggregator. When you swap tokens, it splits the order across multiple liquidity sources to get a better average rate than any single exchange offers.

## The key insight

Sergej Kunz and Anton Bukov built the first prototype in 56 hours at ETHGlobal New York in May 2019. The insight: on any single DEX, a large order moves the price against you (slippage). Splitting the same order across three DEXes with different liquidity pools produces a better average rate.

The math is simple. If exchange A holds 60% of the liquidity and exchange B holds 40%, sending 60% of your trade to A and 40% to B minimizes total slippage. The hard part is computing that split in real time across dozens of pools with changing reserves.

## How it works

The system has three layers.

**Routing.** Given a token pair and an amount, find all available pools (Uniswap, SushiSwap, Curve, and others). For each pool, compute the output amount given the input. Uniswap-style pools use a constant-product formula: x times y equals k.

**Splitting.** Decide how to divide the input across pools. The original algorithm split the order iteratively, testing each split against the others. Later versions use on-chain optimization.

**Execution.** Submit one transaction that performs all the sub-swaps atomically. If any leg fails, the whole transaction reverts. The user signs once; the contract handles the routing.

The aggregator takes a small fee (0.1% to 0.3%) from the price improvement it delivers. If it cannot beat the best single venue, it routes there instead.

## Build something similar

Start with two Uniswap V2-style pools for the same token pair, each with different reserves.

Write a function that, given an input amount, computes the output for pool A, pool B, and three split ratios (all A, 50/50, all B). Print the results.

The split that wins depends on the reserves. With equal reserves, 50/50 wins. With 80/20 reserves, the split roughly matches. This is the entire insight in ten lines of code.

Then add a third pool. The number of split combinations grows, but the principle holds: more pools means more opportunities to beat any single venue.

## Sources

Origin and prototype details are from the 1inch press room and blog posts linked in the evidence field.
