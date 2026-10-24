# Hackathon Project Archive

A curated directory of notable hackathon projects across all domains and eras — from weekend prototypes at local Startup Weekend events to internal company hack weeks that turned into products used by millions.

This is an archive, not a database. Entries are chosen for technical, educational, practical, or social value. Award winners are included, and so are notable non-winners and lesser-known projects with genuine merit. Coverage favors quality and reliability over volume.

## What you'll find

Each entry answers:

- **What** the project is and does
- **Where** it was built — the hackathon, game jam, or internal hack event, when verifiable
- **Any awards or distinctions**, only when backed by evidence
- **Links** to official pages, source code, demos, and videos when they exist
- **Evidence** — public sources backing the claims in the entry

## How to browse

The [project index](#project-index) below is organized by domain. Awards appear next to the relevant entry. Every entry links out to primary resources.

Entries are curated and depend on available evidence. If a detail is unknown, it is left out rather than guessed. A missing field means the information was not verified, not that the project lacked it.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for eligibility, evidence requirements, and how to add or update entries. Research happens on request only; new entries are reviewed and approved by a human before they join the archive.

## Maintenance

Project data lives in `data/projects/*.md` (YAML frontmatter + optional notes). The index below is generated — never edit it by hand.

```bash
pip install -r requirements-dev.txt
python -m archive validate   # check all project records
python -m archive generate   # regenerate the project index below
python -m archive check      # verify the index is current (read-only, CI)
python -m archive export     # optional JSON export for integrations
python -m pytest             # run the test suite
```

## Project index

<!-- BEGIN GENERATED PROJECT INDEX -->

## Accessibility

### JARVIS

AI assistant app that uses computer vision to describe surroundings and non-verbal cues for blind and visually impaired users; won Best Hack for Health at Cal Hacks 10.0.

- **Event:** Cal Hacks 10.0 — UC Berkeley HKN — 2023 — **Award:** Best Hack for Health
- **Team:** Arnav Chintawar, Dhruv Roongta, Sahibpreet Singh
- **Links:** [Official](https://news.gatech.edu/news/2023/12/11/cs-majors-win-best-hack-health-app-visually-impaired)

### Microsoft Immersive Reader

Accessibility tool built into Microsoft Office that helps people with dyslexia and learning differences read and write more effectively.

- **Event:** Microsoft company-wide hackathon — 2015
- **Links:** [Official](https://www.microsoft.com/en-us/education/immersive-reader)

## AI & Machine Learning

### OpenAI Gym

Toolkit for reinforcement learning research; described by OpenAI as not a formal hackathon project but built with rapid-iteration hackathon culture in mind.

- **Links:** [Official](https://github.com/openai/gym)

### Waddle

AI-powered digital clone and sales strategy simulation system for ecommerce; won first place among 93 global teams at the OpenAI GPT-5 Hackathon 2025.

- **Event:** OpenAI GPT-5 Hackathon — OpenAI and Cerebral Valley — 2025 — **Award:** first place
- **Links:** [Official](https://waddle.ai)

## Civic Tech

### g0v (g0v)

Taiwan civic-tech movement that builds open-source tools for government transparency, including crowd-sourced dashboards and legislative trackers.

- **Event:** g0v hackathon — 2012
- **Links:** [Official](https://g0v.tw)

### Ushahidi

Open-source crisis-mapping platform that crowdsources and maps eyewitness reports via SMS and the web.

- **Event:** Kenya post-election crisis rapid build — 2008 — **Award:** NetSquared Mashup Challenge winner
- **Team:** Ory Okolloh, Erik Hersman, Juliana Rotich, David Kobia
- **Links:** [Official](https://www.ushahidi.com) · [Source](https://github.com/ushahidi/platform)

### Witness

Crisis-reporting mobile app built to win the TechCrunch Disrupt New York 2015 Hackathon; used Twilio and crowd-sourced field reports for real-time safety data.

- **Event:** TechCrunch Disrupt New York Hackathon — TechCrunch — 2015 — **Award:** winner
- **Team:** Marinos
- **Links:** [Official](https://techcrunch.com/2015/05/06/witness-wins-the-techcrunch-disrupt-ny-2015-hackathon/)

## Climate & Environment

### Eco Laundry (Water-Saving Washing Machine)

Water-saving washing machine concept by Joanna Power and Paramveer Bhachu; won Red Bull Basement 2020 for the UK and went on to a hardware accelerator and TEDx talks.

- **Event:** Red Bull Basement — Red Bull — 2020 — **Award:** UK winner / global finalist
- **Team:** Joanna Power, Paramveer Bhachu
- **Links:** [Official](https://www.redbull.com/za-en/red-bull-basement-winners-catch-up)

### NASA Space Apps Colombia agriculture platform

Web-app prototype connecting smallholder farmers with local buyers and monitoring agricultural land-use via satellite imagery.

- **Event:** NASA Space Apps Challenge — 2021
- **Links:** [Official](https://spaceappschallenge.org)

### Scintilla

Real-time air quality visualization platform built at NASA Space Apps 2016; won Best Use of Data for turning open sensor feeds into actionable maps.

- **Event:** NASA Space Apps Challenge — NASA — 2016 — **Award:** Best Use of Data
- **Links:** [Official](https://www.spaceappschallenge.org/2016/challenge/scintilla/)

## Developer Tools

### Grafana

Open-source analytics and interactive visualization platform for metrics, logs, and dashboards.

- **Event:** Christmas hackathon — 2013
- **Team:** Torkel Ödegaard
- **Links:** [Official](https://grafana.com) · [Source](https://github.com/grafana/grafana) · [Demo](https://play.grafana.org)

### PostHog Session Replay

Product analytics session-replay feature built during an early PostHog internal hackathon; grew into a core multi-product pillar with tens of thousands of daily active users.

- **Event:** PostHog Internal Hackathon — PostHog
- **Links:** [Official](https://posthog.com/session-replay)

### Sabre Concierge AI

AI travel concierge prototype built during an internal Sabre hackathon; scaled into production-facing assistant tooling for travel agents.

- **Event:** Sabre Internal Hackathon — Sabre
- **Links:** [Official](https://www.sabre.com)

### Superblocks

AI-powered internal tools platform; co-founder Brad Menezes came through the Red Bull Basement student innovation program before scaling the company.

- **Event:** Red Bull Basement — Red Bull — 2021 — **Award:** program alumnus
- **Team:** Brad Menezes
- **Links:** [Official](https://www.superblocks.com)

### Zapier

Workflow automation platform that connects web apps so users can move data between services without writing code.

- **Event:** Startup Weekend Columbia — Startup Weekend — 2011 — **Award:** Winner
- **Team:** Wade Foster, Bryan Helmig, Mike Knoop
- **Links:** [Official](https://zapier.com)

## Education

### ChatEDU

Study assistant that turns PDFs, slides, notes and lecture video into citation-grounded chat, practice sets and flashcards; built by Vanderbilt students for a Microsoft AI hackathon.

- **Event:** Microsoft AI for Students Hackathon — Microsoft — 2023 — **Award:** first place Technical Project Prize
- **Team:** Vasco Singh
- **Links:** [Official](https://www.sofarbot.com/stories/chatedu-vasco-singh-6704-mrr)

### InstructAI

Generative-AI programming tutor built by Georgia Tech students; won the 2024 Klaus Startup Challenge with a $100K seed offer at a $1M valuation.

- **Event:** Klaus Startup Challenge — Georgia Tech College of Computing — 2024 — **Award:** winner
- **Links:** [Official](https://www.cc.gatech.edu/news/students-win-klaus-startup-challenge-dive-5b-market-ai-driven-teaching-tool)

### Jotted

Automated study tool by Arizona State University students Brinlee Kidd and Sylvia Lopez; won the Red Bull Basement 2021 Global Final in Istanbul.

- **Event:** Red Bull Basement — Red Bull — 2021 — **Award:** Global Final winner
- **Team:** Brinlee Kidd, Sylvia Lopez
- **Links:** [Official](https://www.prnewswire.com/news-releases/automated-study-tool-wins-best-idea-at-innovation-program-for-university-students-301513791.html)

### Wayground Anti-Cheat "Eye See You"

Browser-based quiz anti-cheat built during a Wayground internal hackathon; deployed across millions of quiz sessions to deter tab-switching and second-screen cheating.

- **Event:** Wayground Internal Hackathon — Wayground
- **Links:** [Official](https://www.wayground.com)

## Fintech

### 1inch

Decentralized exchange aggregator that finds the best token swap rates across DEX liquidity sources.

- **Event:** ETHGlobal New York — ETHGlobal — 2019
- **Team:** Sergej Kunz, Anton Bukov
- **Links:** [Official](https://1inch.io) · [Source](https://github.com/1inch)

### Agriconnect

Startup addressing agricultural credit access in the Philippines; won Red Bull Basement 2024 with a blockchain-based farming credit marketplace prototype.

- **Event:** Red Bull Basement — Red Bull — 2024 — **Award:** global winner
- **Team:** Soj Gamayon
- **Links:** [Official](https://www.redbull.com/us-en/event-series/basement/red-bull-basement-past-winners)

### Chainlink for Swift

Blockchain oracle integration selected as winner of the Swift Hackathon 2025 Business Challenge; Chainlink co-founder showcased the work at Sibos.

- **Event:** Swift Hackathon — Swift — 2025 — **Award:** Business Challenge winner
- **Links:** [Official](https://chain.link/blog/chainlink-wins-swift-hackathon)

### InstaDApp

Decentralized finance middleware platform that simplifies interactions with lending protocols like MakerDAO through a unified interface.

- **Event:** ETHIndia — 2018
- **Links:** [Official](https://instadapp.io)

### Metaloot

Launchpad connecting games to the Flow blockchain; named a top winner at the ETHGlobal Bangkok 2024 hackathon following Devcon.

- **Event:** ETHGlobal Bangkok — ETHGlobal — 2024 — **Award:** finalist winner
- **Links:** [Official](https://ethglobal.com/showcase)

### PDFi

Turns static PDFs into live financial tools with embedded cryptocurrency transactions; won Best Finance App at ETHGlobal New York 2025.

- **Event:** ETHGlobal New York — ETHGlobal — 2025 — **Award:** Best Finance App on Fern
- **Links:** [Official](https://ethglobal.com/showcase/pdfi-z99gp)

### Quick Insurance

Tap-to-insure mobile prototype for short-term valuable-item coverage; won the TechCrunch Disrupt Berlin 2017 Hackathon Grand Prize and €4,200.

- **Event:** TechCrunch Disrupt Berlin Hackathon — TechCrunch — 2017 — **Award:** Grand Prize
- **Links:** [Official](https://techcrunch.com/2017/12/03/quick-insurance-wins-the-disrupt-berlin-2017-hackathon-grand-prize)

### SolanaFM

Solana blockchain explorer and data platform from Singapore Management University's innovation ecosystem; raised US$4.5M seed and was acquired by Jupiter Exchange in 2024.

- **Event:** SMU Innovation — Singapore Management University — 2023 — **Award:** project origin
- **Links:** [Official](https://solanafm.com)

### Unrugable

Solana-native hardware wallet with companion app; crowned grand champion of the Colosseum Cypherpunk Hackathon at Breakpoint 2025 after four prior hackathon attempts.

- **Event:** Colosseum Cypherpunk Hackathon — Colosseum — 2025 — **Award:** grand champion
- **Links:** [Official](https://solanacompass.com/learn/breakpoint-25/winners-of-the-colosseum-cypherpunk-hackathon)

## Games

### A Little to the Left

Cozy tidying puzzle game about sorting household messes; began as a GMTK Game Jam 2020 entry and became a multi-platform commercial release.

- **Event:** GMTK Game Jam 2020 — Game Maker's Toolkit — 2020
- **Team:** Max Inferno
- **Links:** [Official](https://store.steampowered.com/app/1629520/A_Little_to_the_Left/) · [Demo](https://maxinferno.itch.io/a-little-to-the-left)

### Boomerang X

Momentum-based first-person shooter built around a single teleporting boomerang; started as a 48-hour GMTK Game Jam entry and shipped via Devolver Digital in 2021.

- **Event:** GMTK Game Jam — Game Maker's Toolkit
- **Team:** DANG!
- **Links:** [Official](https://store.steampowered.com/app/1256000/Boomerang_X/) · [Demo](https://dangstudios.itch.io/boomerang-x)

### Broforce

Side-scrolling run-and-gun action game starring hyper-masculine action movie homages, born from a Ludum Dare prototype called Rambros.

- **Event:** Ludum Dare 23 — 2012
- **Links:** [Official](https://www.broforcegame.com)

### Bullion - The Curse of the Cut-Throat Cattle

Project where a coder and a 3D artist met at Global Game Jam 2016 and later developed the concept with Leda Entertainment, recognized at Big Indie Pitch in 2022.

- **Event:** Global Game Jam 2016 — Global Game Jam — 2016
- **Team:** Leda Entertainment

### Die in Dungeon

Roguelike built for the Spooktober game jam; expanded into a full Steam release with a demo that drew large wishlist numbers.

- **Event:** Spooktober Game Jam — Spooktober — 2022 — **Award:** jam prototype
- **Team:** Team Gummy
- **Links:** [Official](https://store.steampowered.com/app/1898250/Die_in_Dungeon/)

### Dome Keeper

Mining-and-defense roguelite where players dig for resources under a dome while defending against waves of enemies.

- **Event:** Ludum Dare 48 — 2021
- **Links:** [Official](https://domekeeper.com)

### Evoland

Action-adventure game where players unlock graphical and mechanical upgrades that evolve the game from monochrome Game Boy style to full 3D.

- **Event:** Ludum Dare 24 — 2012
- **Links:** [Official](https://evoland.shirogames.com)

### Friday Night Funkin'

Open-source rhythm game where a boyfriends battles ex-rockstar dads in rap-battle-style musical face-offs.

- **Event:** Ludum Dare 47 — 2020
- **Links:** [Official](https://www.newgrounds.com/portal/view/770371)

### Galaxiga

Space shooter built during a Global Game Jam; expanded into a polished mobile and Steam release with retro arcade aesthetics.

- **Event:** Global Game Jam — Global Game Jam — 2018 — **Award:** jam prototype
- **Links:** [Official](https://store.steampowered.com/app/875240/Galaxiga/)

### Galcon

Real-time strategy game where players flood planets with fleets using a simple one-click interface.

- **Event:** Ludum Dare 8 — 2006
- **Links:** [Official](https://www.galcon.com)

### Garden Buddies

Cozy game made during the May Day Mental Health game jam run by Global Game Jam with DeepWell DTx in 2022; featured at Wholesome Direct 2023 and shipped on Steam in October 2023.

- **Event:** May Day Mental Health Game Jam — Global Game Jam with DeepWell DTx — 2022
- **Links:** [Official](https://store.steampowered.com)

### Gods Will Be Watching

Point-and-click thriller where a stranded crew faces impossible ethical choices with limited resources.

- **Event:** Ludum Dare 26 — 2013
- **Links:** [Official](https://www.deconstructeam.com/games/gods-will-be-watching/)

### Immortal's Way

Game first created at Global Game Jam 2024 that was later expanded into a full commercial release on Steam.

- **Event:** Global Game Jam 2024 — Global Game Jam — 2024
- **Links:** [Official](https://store.steampowered.com/app/2986350/Immortals_Way/)

### Keep Talking and Nobody Explodes

Cooperative VR bomb-defusal game born from a Global Game Jam 2015 prototype; became one of the best-selling VR titles on Steam.

- **Event:** Global Game Jam — Global Game Jam — 2015 — **Award:** jam prototype
- **Team:** Steel Crate Games
- **Links:** [Official](https://store.steampowered.com/app/341800/Keep_Talking_and_Nobody_Explodes/)

### Loop Hero

Idle-RPG about a hero walking an endless loop against monsters, grown from a non-playable Ludum Dare 2019 prototype into Four Quarters' Devolver-published hit.

- **Event:** Ludum Dare 45 — Ludum Dare — 2019
- **Team:** Four Quarters
- **Links:** [Official](https://fourquarterslab.com) · [Demo](https://ldjam.com/events/ludum-dare/45/loopathero)

### Lullaby of Life

Musical exploration game that started as a Global Game Jam prototype and later shipped on Apple Arcade and Steam.

- **Event:** Global Game Jam — Global Game Jam — 2016 — **Award:** jam prototype
- **Team:** 1 Simple Idea
- **Links:** [Official](https://apps.apple.com/app/lullaby-of-life/id1503210927)

### Officially Dead

Fast-paced zombie-survival action game from Ludum Dare 59; being expanded into a full commercial Steam release by Erebus Games.

- **Event:** Ludum Dare 59 — Ludum Dare — 2025 — **Award:** jam prototype
- **Links:** [Official](https://ldjam.com/events/ludum-dare/59/officially-dead)

### Peak

Physics co-op climbing game jammed in early 2025 by Aggro Crab and Landfall; shipped on Steam months later and sold over 2 million copies.

- **Event:** Peak Jam — Aggro Crab and Landfall — 2025 — **Award:** jam prototype
- **Team:** Aggro Crab, Landfall Games
- **Links:** [Official](https://store.steampowered.com/app/2527290/PEAK/)

### Pony Island

Metafictional puzzle game disguised as a broken arcade machine designed by the devil.

- **Event:** Ludum Dare 31 — 2014
- **Links:** [Official](https://store.steampowered.com/app/405640/Pony_Island/)

### Rollerdrome

Third-person action-shooter that blends rollerskating tricks with gunplay in a dystopian retrofuture arena sport.

- **Event:** GMTK Game Jam — 2017
- **Links:** [Official](https://rollerdromegame.com)

### RV There Yet

Cooperative RV road-trip game developed during an eight-week summer game jam; hit 1.2 million sales in its first week on Steam in October 2025.

- **Event:** Eight-Week Summer Game Jam — Independent collective — 2025 — **Award:** jam prototype
- **Links:** [Official](https://store.steampowered.com/app/2518530/RV_There_Yet/)

### SUPERHOT Prototype

First-person shooter prototype where time moves only when the player moves, built during a seven-day game jam.

- **Event:** 7 Day FPS — 2013
- **Team:** SUPERHOT Team
- **Links:** [Official](https://superhotgame.com) · [Demo](https://superhotgame.com/prototype.html)

### Surgeon Simulator

Darkly comic physics-based surgery simulator that started as a Global Game Jam 2013 prototype; became a multi-platform commercial hit.

- **Event:** Global Game Jam — Global Game Jam — 2013 — **Award:** jam prototype
- **Team:** Bossa Studios
- **Links:** [Official](https://store.steampowered.com/app/233720/Surgeon_Simulator/)

### Swirl W@tch

Game made in 48 hours at Global Game Jam 2021; the full polished version shipped on Steam in April 2023 with a positive review rating.

- **Event:** Global Game Jam 2021 — Global Game Jam — 2021

### The Roottrees are Dead

Deduction puzzle game where players research a 1998 candy-company inheritance to fill in an intricate family tree.

- **Event:** Global Game Jam 2023 — 2023
- **Links:** [Official](https://store.steampowered.com/app/2754380/The_Roottrees_are_Dead/)

### The Secret of Tremendous Corporation

Free point-and-click adventure where a gamedev intern infiltrates a corporation that controls the entire gaming industry.

- **Event:** Global Game Jam 2015 — 2015
- **Links:** [Official](https://store.steampowered.com/app/380140/The_Secret_of_Tremendous_Corporation/)

### The Sun and Moon

Puzzle platformer with a unique mechanic letting the player dive into and travel through the ground.

- **Event:** Ludum Dare 29 — 2014
- **Links:** [Official](https://managore.itch.io/the-sun-and-moon)

### The Textorcist

Typing-action game where you fight demons by typing scripture; born from a Global Game Jam 2016 prototype, later shipped on Steam and Switch.

- **Event:** Global Game Jam — Global Game Jam — 2016 — **Award:** jam prototype
- **Team:** Matteo Nitto, Dario Fazio
- **Links:** [Official](https://store.steampowered.com/app/774361/The_Textorcist/)

### Titan Souls

Minimalist boss-rush action game where the player has one arrow and one life, inspired by Shadow of the Colossus and Dark Souls.

- **Event:** Ludum Dare 28 — 2013
- **Links:** [Official](https://store.steampowered.com/app/297130/Titan_Souls/)

### Townseek

Relaxing exploration-trading game where players fly an airship across a world discovering towns and trading goods.

- **Event:** Global Game Jam 2021 — 2021
- **Links:** [Official](https://store.steampowered.com/app/1659360/Townseek/)

### Wasteland Kings (Nuclear Throne)

Top-down roguelike shooter where mutants fight through procedurally generated levels to claim the Nuclear Throne.

- **Event:** Mojam 2013 — 2013
- **Links:** [Official](https://vlambeer.itch.io/wasteland-kings)

### Yesterday's News

Game that started as a Global Game Jam entry and was later developed into a Steam release.

- **Event:** Global Game Jam — Global Game Jam
- **Links:** [Official](https://store.steampowered.com/app/2850560/Yesterdays_News/)

## Hardware

### OpenGlass

Open-source AI smart-glasses attachment built in about 36 hours for roughly $20 of off-the-shelf parts, pairing a camera with Llama 3 for live scene description.

- **Event:** Cerebral Valley Hackathon — Cerebral Valley — 2024 — **Award:** hackathon winner
- **Team:** Scott Fitsimones, Nik Shevchenko, Stepan Korshakov, Arash Ramanan, Jatin Gupta
- **Links:** [Official](https://github.com/BurgerKing6668/OpenGlass2) · [Demo](https://github.com/not-important-vr/openglass)

### Shower With Friends

Hardware plus mobile app that monitors shower flow rate and gamifies shorter showers against friends; won the TechCrunch Disrupt SF 2014 hackathon grand prize.

- **Event:** TechCrunch Disrupt SF Hackathon — TechCrunch — 2014 — **Award:** grand prize
- **Links:** [Demo](https://techcrunch.com/2014/09/07/shower-with-friends-lets-you-gamify-water-consumption/)

## Healthcare

### Airocide

NASA-derived air purification technology commercialized after Space Apps-adjacent open innovation work; turned spacecraft-grade catalytic oxidation into consumer air cleaners.

- **Event:** NASA Innovation — NASA — 2014 — **Award:** technology transfer
- **Links:** [Official](https://www.airocide.com)

### MedLink

Healthcare connectivity app developed at SF State's civic hackathon; featured at a White House Champions of Change event for open government and civic hacking.

- **Event:** San Francisco Day of Civic Hacking — Code for America / SF State — 2014 — **Award:** White House featured project
- **Links:** [Official](https://commons.sfsu.edu/hackathon-sf-state)

### OpenVent

Open-source ventilator design produced during Infineon Technologies' COVID-era hackathon; one of several rapid-build emergency respiratory device projects in 2020.

- **Event:** Infineon Technologies Hackathon — Infineon Technologies — 2020 — **Award:** hackathon project
- **Links:** [Official](https://www.medicaldesignandoutsourcing.com/can-an-open-source-ventilator-hackathon-help-fight-the-coronavirus)

### Project M

Emotional AI platform detecting micro-facial expressions for clinical use; won the Texas Children's Hospital Healthcare Hackathon Touchless Experience category in 2021.

- **Event:** Texas Children's Hospital Healthcare Hackathon — Texas Children's Hospital — 2021 — **Award:** Touchless Experience category winner
- **Links:** [Official](https://developer.nvidia.com/blog/emotional-ai-solution-won-texas-childrens-hospital-healthcare-hackathon)

### Project Prometheus

COVID-era NASA Space Apps global winner building low-cost open ventilator and respiratory support designs for crisis conditions.

- **Event:** NASA Space Apps Challenge — NASA — 2020 — **Award:** global winner
- **Links:** [Official](https://www.spaceappschallenge.org/2020/challenge/project-prometheus/)

### Strados Labs

RESP Biosensor wearable for real-time lung health monitoring; team formed at a 2016 Independence Blue Cross and Thomas Jefferson University health hackathon, later received FDA 510(k) clearance.

- **Event:** Independence Blue Cross Health Hackathon — Independence Blue Cross and Thomas Jefferson University — 2016 — **Award:** project origin
- **Links:** [Official](https://www.stradoslabs.com)

## Media & Arts

### Frame (Walters Art Museum)

Smartphone app that frames museum artworks by photo; co-winner of the first Walters Art Museum Art Bytes hackathon in 2012 with Tanzaku, taking a $1,000 prize.

- **Event:** Art Bytes — Walters Art Museum — 2012 — **Award:** co-winner ($1,000)
- **Links:** [Official](https://technical.ly/software-development/art-bytes-these-are-the-eight-projects-from-the-first-ever-walters-art-museum-hackathon)

### Museum Wakes

AI-powered narrative mystery transforming the Met's Egyptian Wing into an interactive voice experience; built at the Gemini 3 NYC Hackathon in February 2026.

- **Event:** Gemini 3 NYC Hackathon — Cerebral Valley — 2026 — **Award:** gallery project
- **Links:** [Official](https://museum-wakes.onrender.com/)

### Tanzaku

Smartphone museum exploration app; co-winner of the Walters Art Museum's first Art Bytes hackathon in 2012 with a $1,000 prize.

- **Event:** Art Bytes — Walters Art Museum — 2012 — **Award:** co-winner ($1,000)
- **Links:** [Official](https://technical.ly/baltimore/2012/07/27/art-bytes-brings-technologists-others-to-walters-art-museum-for-art-inspired-hackathon/)

## Robotics

### DroneStalker

Real-time drone tracking and prediction system; winner at Junction 2025, Europe's largest hackathon, placing top 5 of 300 teams and 1,500 participants in Espoo, Finland.

- **Event:** Junction — Junction / AaltoES — 2025 — **Award:** Winner (top 5)
- **Links:** [Official](https://github.com/takara-ai/DroneStalker)

### GROWBOT

Robot-assisted tree growth optimization system; named Hackathon Champion at robo.innovate 2025 in Munich with a €2,500 prize.

- **Event:** robo.innovate Hackathon — MIRMI / Technical University of Munich — 2025 — **Award:** Hackathon Champion
- **Links:** [Official](https://www.mirmi.tum.de/en/mirmi/news/article/roboinnovate-hackathon-2025-advancing-robotics-and-ai-solutions)

### HEXDOC

Collision-avoidance robot for construction and excavation in tunnels and caves; won Smart India Hackathon 2023 Hardware Edition Student Innovation in Robotics and Drones.

- **Event:** Smart India Hackathon — Government of India / AICTE — 2023 — **Award:** Hardware Edition Student Innovation winner (Robotics and Drones)
- **Team:** Team Innovortex, LPU
- **Links:** [Official](https://happenings.lpu.in/lpu-innovortex-triumphs-smart-india-hackathon-2023)

### Lily Robotics

UC Berkeley robotics-lab prototype for a throw-and-shoot follow-me camera drone that drew huge pre-orders, then collapsed amid fraud allegations and bankruptcy.

- **Team:** Antoine Balaresque, Henry Bradlow
- **Links:** [Official](https://en.wikipedia.org/wiki/Lily_Robotics)

### Rubble Busters

Autonomous search-and-report drone system; won first place at Kent State's 2023 SkyHack for disaster rubble navigation.

- **Event:** SkyHack — Kent State University — 2023 — **Award:** first place
- **Links:** [Official](https://www.kent.edu/today/news/rubble-busters-skyhack-team-creates-lifesaving-drone-fly)

## Science

### Android Base Station

Smartphone turned into a satellite ground station at NASA Space Apps 2014; won Best Use of Hardware for turning commodity phones into radio receivers for open satellite data.

- **Event:** NASA Space Apps Challenge — NASA — 2014 — **Award:** Best Use of Hardware
- **Links:** [Official](https://www.spaceappschallenge.org/2014/challenge/android-base-station/)

### SkyWatch

Space data mashup that won NASA Space Apps 2014 Best Use of Data; combined Earth observation feeds into a single accessible interface.

- **Event:** NASA Space Apps Challenge — NASA — 2014 — **Award:** Best Use of Data
- **Links:** [Official](https://www.spaceappschallenge.org/2014/challenge/skywatch/)

### SongSat

Satellites that transmit data as audible songs for citizen listening; won the 2019 NASA Space Apps global award for Best Scientific Achievement.

- **Event:** NASA Space Apps Challenge — NASA — 2019 — **Award:** Best Scientific Achievement (global winner)
- **Team:** SongSat team
- **Links:** [Official](https://www.spaceappschallenge.org/2019/challenge/songsat/)

### Space Canary (Canaria)

Radiation and environment sensor network originally developed at NASA Space Apps 2016 as Canaria; evolved into Lunar Outpost's Space Canary product line with NASA Spinoff recognition.

- **Event:** NASA Space Apps Challenge — NASA — 2016 — **Award:** Best Use of Hardware
- **Team:** Lunar Outpost
- **Links:** [Official](https://spinoff.nasa.gov/Spinoff2020/ch_5.html)

## Social Impact

### Facebook Like button

One-click social interaction feature that let users express approval of posts, photos, and pages across the web.

- **Event:** Facebook internal hackathon — 2007
- **Links:** [Official](https://en.wikipedia.org/wiki/Like_button)

### Noonlight

Personal safety platform that began as a Startup Weekend project; became a widely integrated panic-button service used by dating apps and smart devices.

- **Event:** Startup Weekend — Startup Weekend — 2013 — **Award:** project origin
- **Links:** [Official](https://www.noonlight.com)

### Shaker

Virtual bar/lounge environment built on Facebook Open Graph; won TechCrunch Disrupt San Francisco 2011 and raised significant venture funding.

- **Event:** TechCrunch Disrupt San Francisco — TechCrunch — 2011 — **Award:** Disrupt Battlefield finalist
- **Links:** [Official](https://en.wikipedia.org/wiki/Shaker_(social_network))

## Web & Mobile

### Appreciate

Profit-sharing property management platform for property owners that won Columbia Startup Weekend 2022 and raised a $750K seed round.

- **Event:** Columbia Startup Weekend — Startup Weekend — 2022 — **Award:** winner
- **Team:** Nick Farquhar
- **Links:** [Official](https://www.appreciate.io/)

### Audvice

Startup that won Red Bull Basement 2019; later raised more than $3 million in venture capital, worked with Fortune 500 companies, and was acquired.

- **Event:** Red Bull Basement — Red Bull — 2019 — **Award:** global winner
- **Team:** Sophie Bolzer, Nadine Szentivanyi
- **Links:** [Official](https://www.redbull.com/us-en/red-bull-basement-2019-winner-audvice-interview)

### Carousell

Mobile-first classifieds marketplace where selling an item takes about a minute with a photo.

- **Event:** Startup Weekend Singapore — Startup Weekend — 2012 — **Award:** First place
- **Team:** Quek Siu Rui, Lucas Ngoo, Marcus Tan
- **Links:** [Official](https://carousell.com)

### Docracy

Open-source legal document platform billed as a GitHub for contracts; won a TechCrunch Disrupt hackathon and raised a $650K seed round.

- **Event:** TechCrunch Disrupt Hackathon — TechCrunch — 2011 — **Award:** hackathon winner
- **Team:** Matt Hall, John Watkinson
- **Links:** [Official](https://www.docracy.com)

### Easy Taxi

Mobile ride-hailing app that connected passengers with taxi drivers across Latin America and other emerging markets.

- **Event:** Startup Weekend Rio — 2011
- **Links:** [Official](https://en.wikipedia.org/wiki/Easy_Taxi)

### Figma Slides

Presentation design tool built on Figma's collaborative canvas, letting teams create and present slide decks together in real time.

- **Event:** Figma Maker Week — 2023
- **Links:** [Official](https://www.figma.com/slides)

### Foodspotting

Visual food discovery app that emerged from the Startup Weekend ecosystem; became a widely covered example of hackathon-to-startup success.

- **Event:** Startup Weekend — Startup Weekend — 2009 — **Award:** project origin
- **Team:** Alexa Andrzejewski
- **Links:** [Official](https://en.wikipedia.org/wiki/Foodspotting)

### GroupMe

Free group messaging app that works over SMS and smartphone apps, built as a hackathon project.

- **Event:** TechCrunch Disrupt New York hackathon — TechCrunch — 2010
- **Team:** Jared Hecht, Steve Martocci
- **Links:** [Official](https://groupme.com)

### Pointshop Space

Augmented-reality shopping prototype that won the TechCrunch Disrupt San Francisco 2016 Hackathon grand prize.

- **Event:** TechCrunch Disrupt San Francisco Hackathon — TechCrunch — 2016 — **Award:** grand prize
- **Links:** [Official](https://techcrunch.com/2016/09/13/pointshop-space-wins-disrupt-sf-2016-hackathon/)

### Talkdesk

Cloud-based contact center platform that lets businesses handle customer calls over the internet instead of traditional phone systems.

- **Event:** TwilioCon hackathon — 2011
- **Links:** [Official](https://www.talkdesk.com)

### Trello

Visual collaboration tool that organizes projects into boards, lists, and cards.

- **Event:** Fog Creek Creek Week — Fog Creek Software — 2011
- **Links:** [Official](https://trello.com)

### Twitter

Microblogging service for short public status updates, prototyped inside the podcasting company Odeo.

- **Event:** Odeo internal brainstorming session — Odeo — 2006
- **Team:** Jack Dorsey, Florian Weber
- **Links:** [Official](https://twitter.com)

### Vurb

Contextual search and discovery app that won the TechCrunch Disrupt 2014 Battlestage; later acquired by Rakuten for approximately $300 million.

- **Event:** TechCrunch Disrupt — TechCrunch — 2014 — **Award:** Battlestage winner
- **Team:** Ricky Wong
- **Links:** [Official](https://en.wikipedia.org/wiki/Vurb)

### Zaarly

Hyperlocal real-time buyer-powered marketplace; prototyped and pitched at Startup Weekend Los Angeles in 2011, then raised a $14M Series A led by Kleiner Perkins.

- **Event:** Startup Weekend Los Angeles — Startup Weekend — 2011 — **Award:** winner
- **Team:** Bo Fishback, Eric Koester, Ian Hunter
- **Links:** [Official](https://en.wikipedia.org/wiki/Zaarly)

## Other

### Caius

AI-based mapping system that automatically identifies road and trail networks; grew from a CASSINI Hackathon concept into a rural digitisation startup with ESA incubation and a 2025 consumer app.

- **Event:** CASSINI Hackathon — European Union / ESA
- **Team:** Giorgos Mendrinos
- **Links:** [Official](https://www.euspa.europa.eu/newsroom-events/success-stories/caius-hackathon-idea-rural-digitisation-startup)

### EquipmentShare

Construction equipment rental and jobsite technology company that began as a Columbia Startup Weekend winning idea and later listed on Nasdaq.

- **Event:** Columbia Startup Weekend — Startup Weekend — 2014 — **Award:** winner
- **Team:** Jabbok Schlacks, Willy Schlacks
- **Links:** [Official](https://www.equipmentshare.com)

### Getaround

Peer-to-peer car-sharing marketplace with a hardware car-kit for phone unlock; won TechCrunch Disrupt NYC 2011, later NYSE-listed, wound down in 2026.

- **Event:** TechCrunch Disrupt NYC Startup Battlefield — TechCrunch — 2011 — **Award:** winner
- **Team:** Sam Zaid, Jessica Scorpio, Elliot Kroo
- **Links:** [Official](https://www.getaround.com)

### YourMechanic

Marketplace connecting car owners with mobile mechanics; won the TechCrunch Disrupt SF 2012 Startup Battlefield after pitching earlier as HiretoFix.

- **Event:** TechCrunch Disrupt SF Startup Battlefield — TechCrunch — 2012 — **Award:** winner
- **Team:** Art Agrawal, Dongyi Liao
- **Links:** [Official](https://www.yourmechanic.com)

<!-- END GENERATED PROJECT INDEX -->

## License

MIT — see [LICENSE](LICENSE). Project names and linked resources remain the property of their respective owners; this repository only catalogs them with attribution.
