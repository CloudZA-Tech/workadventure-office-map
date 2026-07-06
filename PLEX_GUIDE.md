# 🏙️ CloudZA Plex — Map Guide

A multi-floor WorkAdventure virtual HQ for CloudZA. A ground-floor **Lobby** (where you
spawn) connects via a central **lift bank** to three **team floors** and an all-hands
**Townhall**. Every functional zone lives in a `.wam` file, so the whole plex is editable
live in the in-app **Map Editor**.

```
             ┌───────────────── CloudZA Plex ─────────────────┐
  spawn ►    │  LOBBY / Reception  ──lift──►  Floor 1  Team Alpha   (blue)
             │        │             ──lift──►  Floor 2  Team Bravo   (green)
             │        │             ──lift──►  Floor 3  Team Charlie (amber)
             │        └─────────────lift──►  Townhall / All-Hands
             └─────────────────────────────────────────────────┘
  every lift is two-way; each floor's 🛗 returns you to the Lobby
```

## 🛗 Lobby (spawn)

> Welcome to CloudZA, dankie for popping in! Grab a spot in the central lift bank and ride up to any of our team floors, or head to the Townhall for all-hands gatherings.

- **Default spawn** — you arrive here.
- **📋 Welcome to CloudZA — Sign In & Say Hello** — `openWebsite` placeholder: `https://REPLACE-ME.example.com/cloudza-lobby-welcome`
- **Lift bank** — four lifts (each an `exit` zone, colour-tinted per destination):
  - 🛗 Lift → Team Alpha (Floor 1)
  - 🛗 Lift → Team Bravo (Floor 2)
  - 🛗 Lift → Team Charlie (Floor 3)
  - 🛗 Lift → Townhall (All-Hands)

## 🔵 blue Team Alpha — Floor

*Ship it, scale it, own it.*  
accent `#2f6fed`

> The blue-lit Team Alpha floor where CloudZA's product and platform engineers turn ideas into shipping software, ringed by focus offices, a war room, and a coffee-fuelled breakout nook.

- **Team Leader office** (focusable, team-colour highlight): **Thandeka Mabaso** — Head of Platform Engineering
- **Member offices** (4 × private focusable offices):
  - **Sipho Ndlovu** — Senior Backend Engineer
  - **Charl van der Merwe** — Site Reliability Engineer
  - **Aisha Patel** — Frontend Engineer
  - **Lerato Mokoena** — Product Designer
- **Alpha War Room** — Jitsi meeting room `cloudza-alpha-war-room` (press SPACE to join)
- **The Rooibos Lounge** — Grab a cuppa, swap war stories, and rubber-duck your gnarliest bug with a teammate.
- **Alpha Notice Board** — `openWebsite` placeholder: `https://REPLACE-ME.example.com/alpha-notice-board`
- **🛗 Lift → Lobby**

## 🟢 green Team Bravo — Floor

*Keep it up, keep it green.*  
accent `#1f9d55`

> The green-lit Team Bravo floor where CloudZA's SRE crew keeps the platform humming, tames incidents, and turns 3am pages into boring dashboards.

- **Team Leader office** (focusable, team-colour highlight): **Thandeka Mokoena** — Head of Site Reliability Engineering
- **Member offices** (4 × private focusable offices):
  - **Ruan Pretorius** — Senior Platform Engineer
  - **Naledi Dlamini** — Incident & On-Call Lead
  - **Yusuf Adams** — Cloud Infrastructure Engineer
  - **Lerato Nkosi** — Observability & Reliability Engineer
- **The War Room (Incident Bridge)** — Jitsi meeting room `cloudza-bravo-war-room` (press SPACE to join)
- **The Green Room** — Grab a rooibos, decompress after a deploy, and swap war stories where nothing is on fire.
- **Bravo Ops Board — runbooks, on-call roster & incident retros** — `openWebsite` placeholder: `https://REPLACE-ME.example.com/bravo-ops-board`
- **🛗 Lift → Lobby**

## 🟡 amber Team Charlie — Floor

*Turning raw data into gold.*  
accent `#e0a800`

> The amber-lit Charlie floor where CloudZA's data and AI crew mine insight from noise, ship models, and keep the pipelines humming.

- **Team Leader office** (focusable, team-colour highlight): **Naledi Khumalo** — Head of Data & AI
- **Member offices** (4 × private focusable offices):
  - **Tumelo Sithole** — Machine Learning Engineer
  - **Anja van Rensburg** — Data Engineer
  - **Rudzani Mahlangu** — Analytics Engineer
  - **Kayleigh Naidoo** — Data Scientist
- **The Feature Store** — Jitsi meeting room `cloudza-charlie-feature-store` (press SPACE to join)
- **The Data Lake Lounge** — Grab a coffee, dip into the data lake, and let your best ideas float to the surface.
- **Charlie Model Board** — `openWebsite` placeholder: `https://REPLACE-ME.example.com/charlie-model-board`
- **🛗 Lift → Lobby**

## 🎤 Townhall / All-Hands

- **All-hands Stage** — `speakerMegaphone` (`cloudza-townhall`): speak to the whole audience.
- **All-hands Audience** — `listenerMegaphone`: hear the speaker on stage.
- **All-hands Notice Board** — `openWebsite` placeholder: `https://REPLACE-ME.example.com/cloudza-allhands-agenda`
- **Overflow Room — Green / Purple** — two Jitsi rooms `cloudza-overflow-green` / `cloudza-overflow-purple`.
- **🛗 Lift → Lobby**

## 🔧 Placeholder URLs to customise

All notice boards embed a website via the `openWebsite` area property and point at obvious
placeholders — replace with your real intranet / Google Doc. Easiest: edit live in the Map
Editor, or change the `link` field in the relevant `.wam` and re-upload.

| Where | File | Placeholder |
|-------|------|-------------|
| Lobby welcome board | `lobby.wam` | `https://REPLACE-ME.example.com/cloudza-lobby-welcome` |
| Team Alpha board | `floor_alpha.wam` | `https://REPLACE-ME.example.com/alpha-notice-board` |
| Team Bravo board | `floor_bravo.wam` | `https://REPLACE-ME.example.com/bravo-ops-board` |
| Team Charlie board | `floor_charlie.wam` | `https://REPLACE-ME.example.com/charlie-model-board` |
| Townhall agenda | `townhall.wam` | `https://REPLACE-ME.example.com/cloudza-allhands-agenda` |

## ✏️ Editing live (in-app Map Editor)

The plex is served from **map-storage** (`canEdit: true`). In your browser, click the
**Map Editor** (🔧) icon in the room toolbar to move/resize areas, change website URLs and
Jitsi rooms, rename offices, or add furniture. Changes save straight back — no redeploy.

## 🗂️ Files

- `office_base.tmj` — shared tile art for the Lobby + 3 team floors.
- `townhall_base.tmj` — tile art for the Townhall.
- `lobby.wam`, `floor_alpha.wam`, `floor_bravo.wam`, `floor_charlie.wam`, `townhall.wam` — the five rooms (areas/zones).
- `tilesets/` — WorkAdventure tileset art.

## 🚀 Wired into the running stack

Uploaded to map-storage under `plex/`; `START_ROOM_URL=/~/plex/lobby.wam`. Re-upload after edits:

```bash
zip -r plex.zip office_base.tmj townhall_base.tmj *.wam tilesets
curl -u john.doe:password -F "directory=plex" -F "file=@plex.zip" \
  http://map-storage.workadventure.localhost/upload
```
