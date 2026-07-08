# CloudZAPlex

Sourced from [workadventure/brainfinger-map](https://github.com/workadventure/brainfinger-map), rebranded as "CloudZAPlex". Deployed to map-storage under the `cloudzaplex/` directory, served at `/~/cloudzaplex/cloudzaplex.wam`.

This is **not** wired into `.github/workflows/build-and-deploy.yml`. That pipeline's `getMaps()` only picks up `*.tmj` files, and this directory's source map is `map.json` (brainfinger's own convention), so it's invisible to the existing scanner — committing this folder does not trigger or affect the main office-map deploy. Deployment here is manual, because this map's build has quirks the shared pipeline doesn't handle (see below).

## Build

Uses an older `wa-map-optimizer-vite@^1.0.2`, incompatible with this repo's root `^1.2.5` — hence its own `package.json`/`vite.config.ts` in this folder rather than sharing the root build.

```sh
cd cloudzaplex
npm install
npm run build
```

The build **will error** on `Cannot find ./dist/assets assets build folder` from the optimizer's `closeBundle` hook — this is a known bug in `wa-map-optimizer-vite@1.0.2`. The actual map/tileset chunking (`dist/map.json`, `dist/map-chunk-1.png`) completes successfully *before* that error fires, so the build output is usable despite the non-zero exit.

## Post-build fixes (required every build, not automated)

1. Strip the `script` property from `dist/map.json` (references an unbundled `script.js` that isn't part of the output).
2. Rename `dist/map.json` → `dist/map.tmj` (map-storage requires the `.tmj` extension).
3. Re-apply `exitSouth` layer's `exitUrl` property — the build resets it to the placeholder `{{{ exitSouthURL }}}` every time. Set it to `https://workadventure.dev.cloudza.tech/~/plex/lobby.wam`.
4. Strip the `collides` custom property from tileset entries for GIDs `1,2,3,4,6,7,8,26,157` in the built `dist/map.tmj`. **This is a real bug in the optimizer's tileset deduplication** — it merges visually-similar-but-semantically-different source tiles into the same consolidated GID and incorrectly carries over the `collides` property from the real wall-marker tile onto unrelated tiles used by the Jitsi zone layer, CoWebsite zone layer, and some floor decoration layers. Left unfixed, this makes every room's interior (not just doorways) solid and unwalkable. Only GID `5` (the real collision-layer marker) and `1560-1563` (door-frame decorations, legitimately collide since they sit on real walls) should keep `collides: true`.
5. Upload via `upload-wa-map` (zip-based upload) — **not** raw individual `curl PUT`s. Raw PUTs trigger the map-storage validator's unauthenticated `HEAD` existence check against each tileset image, which always 401s against our Basic+Bearer-auth-protected instance and falsely reports tilesets as missing.

```sh
npx upload-wa-map --directory cloudzaplex \
  --mapStorageUrl "https://workadventure.dev.cloudza.tech/map-storage" \
  --mapStorageApiKey "<MAP_STORAGE_API_KEY>"
```

## Map-data fixes already applied (baked into `map.json`, survive rebuilds)

- `mapName` → `"CloudZAPlex"`, `mapLink` → this repo.
- All 12 door "...Closed" tile layers (10 room doors + `exitSouthClosed`/`exitWestClosed`) have their tile data zeroed — not just hidden. WorkAdventure applies collision to every tile layer at scene load regardless of visibility (`GameScene.ts` `createCollisionWithPlayer()`), so a hidden-but-populated layer still blocks movement; removing the tile data entirely is the only real fix.
- All 22 Tiled objects with `"type": "variable"` (10 door variables + 12 room/exit config variables) also have `"class": "variable"` set. WorkAdventure's front-end (`SharedVariablesManager.ts`) only recognizes the modern `class` field, not the legacy `type` field the source map used — without this, the front-end never registers these as real variables and any script write to them silently no-ops.
- Brainfinger branding removed: 4 logo tilesets + PNGs deleted, ~167 individual logo tile placements zeroed across Floor/Wall/Details/Above layers.
- Jitsi video-call zones removed from all 10 private offices (proximity chat still works normally). Meeting rooms elsewhere on the map (`CrucialConference`, etc.) are untouched.
- Each office's legacy `CoWebsite` layer-property whiteboard trigger (`openWebsite`/`openWebsitePolicy`/`openWebsiteTrigger`) is stripped — that mechanism only supports embedding and has no "open in new tab" option. Replaced by Area-based `openWebsite` properties (`newTab: true`) in `cloudzaplex.wam` instead.

## `cloudzaplex.wam`

Wraps `map.tmj` so the room can be addressed via `/~/cloudzaplex/cloudzaplex.wam` (required for the in-game Map Editor, which needs a `.wam` file to persist edits into — a raw `.tmj`-addressed room has nowhere to save to). Contains:

- A `speakerMegaphone` area ("Podium") at the courtyard stage (near the piano/drum kit), paired with a map-wide `listenerMegaphone` area — anyone standing at the podium can broadcast audio/video to the whole map.
- 10 `openWebsite` areas (one per office), each opening a shared ClickUp link in a new tab (`newTab: true`) when clicked. ClickUp's main app blocks iframe embedding via CSP (`frame-ancestors`), so embedding wasn't an option; opening in a new tab sidesteps that entirely since CSP `frame-ancestors` only restricts framing, not top-level navigation.

The Map Editor auto-saves live edits directly to this file on the server. **The copy in `dist/cloudzaplex.wam` in this repo is a point-in-time snapshot, not authoritative** — always pull the live version from map-storage before rebuilding/re-uploading to avoid clobbering in-game edits:

```sh
curl -u admin:<MAP_STORAGE_AUTH_PASSWORD> \
  https://workadventure.dev.cloudza.tech/map-storage/cloudzaplex/cloudzaplex.wam \
  -o cloudzaplex/dist/cloudzaplex.wam
```
