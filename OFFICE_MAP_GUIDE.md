# CloudZA Virtual Office — Map Guide

A rich, functional WorkAdventure office built on the official
[map-starter-kit](https://github.com/workadventure/map-starter-kit). It ships as **two
linked maps** joined by exit zones, with all functional areas defined in the `.wam`
files so they are editable live in the **in-app Map Editor**.

```
office.wam / office.tmj      ── main office hub (spawn here)
        │  exit "To Townhall" ⇄ exit "To Office"
conference.wam / conference.tmj ── all-hands townhall + event space
```

## Rooms & zones

### `office` (main hub — visitors spawn here)

| Area | Type | Notes |
|------|------|-------|
| Reception & Lobby | `start` (default) + description | Spawn point + welcome area |
| Welcome Notice Board | `openWebsite` | **Placeholder URL — change me** (see below) |
| Open-plan Desks | description | Large shared work area |
| Meeting Room — Orange | `jitsiRoomProperty` + `focusable` | Jitsi room `office-orange`, press SPACE to join |
| Meeting Room — Blue | `jitsiRoomProperty` + `focusable` | Jitsi room `office-blue` |
| 1:1 Booth A / B | `focusable` | Small private booths for 1:1s |
| Café & Break Area | description | Social / break space |
| Library — Quiet Zone | `silent` | Mic + camera muted automatically |
| To Townhall & Event Space | `exit` → `conference.wam#from-office` | Walk in to travel |
| from-conference | `start` | Where you land when returning from the townhall |

### `conference` (townhall & event space)

| Area | Type | Notes |
|------|------|-------|
| Townhall Stage | `speakerMegaphone` (`townhall`) + `focusable` | Speak to the whole audience |
| Townhall Audience | `listenerMegaphone` (`townhall`) | Hear the speaker on stage |
| Event Notice Board | `openWebsite` | **Placeholder URL — change me** |
| Meeting Room — Green | `jitsiRoomProperty` + `focusable` | Jitsi room `conf-green` |
| Meeting Room — Purple | `jitsiRoomProperty` + `focusable` | Jitsi room `conf-purple` |
| To Office | `exit` → `office.wam#from-conference` | Walk in to travel |
| from-office | `start` (default) | Where you land when arriving from the office |

## 🔧 Placeholder URLs to customise

The two notice boards embed a website via the `openWebsite` area property. They point at
obvious placeholders — replace them with your real intranet page / Google Doc:

| Area | File | Current placeholder |
|------|------|---------------------|
| Welcome Notice Board | `office.wam` | `https://REPLACE-ME.example.com/office-welcome-board` |
| Event Notice Board | `conference.wam` | `https://REPLACE-ME.example.com/townhall-agenda` |

Easiest way to change them: **edit live in the Map Editor** (below). Or edit the `link`
field of the relevant `openWebsite` property in the `.wam` and re-upload.

> To embed arbitrary external sites, the self-hosted stack may need the target host added
> to `WHITELISTED_RESOURCE_URLS` (map-storage env). Google Docs/Sheets embed URLs work
> once whitelisted.

## ✏️ Editing the map live (in-app Map Editor)

The map is served from **map-storage**, so the Map Editor is enabled (`canEdit: true`).

1. Walk into the office in your browser.
2. Click the **Map Editor** icon (🔧 / pencil) in the room toolbar (top toolbar).
3. Select an area to change its properties (Jitsi room, website URL, silent, etc.), drag
   to resize/move, or add new areas, entities and furniture.
4. Changes are saved straight back to map-storage — no redeploy needed.

## 🚀 How it is wired into the local stack

Uploaded to the running `workadv-local` map-storage under the `office/` directory:

```
http://map-storage.workadventure.localhost/office/office.wam
http://map-storage.workadventure.localhost/office/conference.wam
```

`START_ROOM_URL` in `local/.env` points at the office hub:

```
START_ROOM_URL=/~/office/office.wam
```

## 🔁 Re-uploading after local edits

This repo uses the starter-kit upload flow. Configure `.env` / `.env.secret`
(see `.env`) then:

```bash
npm install
npm run upload          # builds + uploads to MAP_STORAGE_URL / UPLOAD_DIRECTORY
```

For the local `workadv-local` stack the equivalent raw upload is:

```bash
zip -r office-map.zip office.tmj conference.tmj office.wam conference.wam tilesets
curl -u john.doe:password -F "directory=office" -F "file=@office-map.zip" \
  http://map-storage.workadventure.localhost/upload
```

Areas live in the `.wam` files; visuals/collision live in the `.tmj`; art is in
`tilesets/`. Keep the `.wam` next to its `.tmj` so map-storage serves your areas instead
of generating an empty one.
