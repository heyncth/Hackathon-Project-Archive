---
id: adsense
name: AdSense
description: Contextual advertising platform for publishers. Generated approximately 15% of Google revenue within two years of launch.
domain: web-mobile
tags: [advertising, google, internal-hack-week]
event:
  name: Google 20% Time
  organizer: Google
  year: 2003
notes: Started by Susan Wojcicki as a 20% project, launched June 2003
links:
  official: https://adsense.google.com/
evidence:
  - url: https://en.wikipedia.org/wiki/20%25_Project
    supports: "Google 20% project origin, Susan Wojcicki, revenue contribution"
deep_dive: true
key_idea: >-
  Match text ads to page content automatically, so publishers earn revenue without selling inventory themselves.
learn_from: >-
  A 20% time project won because it solved a real distribution problem: thousands of small sites had content but no sales team.
verified_at: 2026-10-24
---

## What it does

AdSense places contextual text and display ads on websites. Publishers paste a snippet of JavaScript; the script requests ads that match the page content and earns revenue when visitors click.

## The key insight

Susan Wojcicki proposed the idea in 2002 as a Google 20% project. The problem: Google had AdWords (advertisers bidding on keywords) but no way to place those ads on the millions of small websites that had content but no sales force. AdSense closed that gap by automating the match between page content and ad inventory.

The revenue number tells the story. Within two years of launch in June 2003, AdSense generated roughly 15% of Google's total revenue.

## How it works

**Content analysis.** The script sends the page URL (and sometimes extracted text) to Google's servers. An algorithm determines the page's topics: the words, the category, the context.

**Ad selection.** Google matches those topics against keywords that advertisers are bidding on. Advertisers set bids per keyword in AdWords; AdSense surfaces the highest-bidding ads relevant to the page.

**Auction.** Multiple ads compete for the slot. Google runs a second-price auction: the winner pays one cent more than the second-highest bidder. This keeps bids honest.

**Rendering.** The script receives ad code (HTML and CSS) and injects it into the page. The publisher never sees the auction logic; they get a div that fills with ads.

**Revenue share.** Google keeps a percentage (reported around 68%) and pays the publisher the rest (32%). The exact split is not public and has changed over time.

## Build something similar

Build a page that displays a sponsored link based on the page's own content.

Start with a static mapping: define five topics (cooking, finance, travel, fitness, technology) and one ad creative for each. Write a function that reads the page title and tags, scores each topic by word overlap, and picks the highest.

This gives you the core loop: analyze content, select an ad, render it. The difference between this and production AdSense is scale (millions of pages, real-time auction) and quality (advertisers actually paying).

Then add a simple auction: two advertisers bidding on the same keyword, winner pays second-highest bid plus one cent. This is the AdWords mechanism.

## Sources

Origin and revenue figures are documented in Wikipedia's 20% Project article, linked in the evidence field.
