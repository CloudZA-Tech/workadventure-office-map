#!/usr/bin/env python3
"""Build the CloudZA plex: lobby + 3 team floors + townhall.
Geometry is fixed here; per-floor CONTENT comes from specs (produced by the
design polecats). Shared tile art: office_base.tmj + townhall_base.tmj."""
import json, os, shutil, sys

S = "/tmp/claude-1000/-home-jono-gt-workadv-polecats-furiosa-workadv/6a54c0ef-c851-4128-8f9f-e2481d45850c/scratchpad"
SRC = f"{S}/map-starter-kit"
OUT = f"{S}/plex"
T = 32
def px(c): return c * T

ENTITY_COLLECTIONS = [
    {"url": "http://play.workadventure.localhost/collections/FurnitureCollection.json", "type": "file"},
    {"url": "http://play.workadventure.localhost/collections/OfficeCollection.json", "type": "file"},
]

def clean_tmj(name):
    m = json.load(open(os.path.join(SRC, name)))
    m["properties"] = [p for p in m.get("properties", []) if p["name"] != "script"]
    def strip(layers):
        for l in layers:
            if l["type"] == "objectgroup":
                l["objects"] = []
            elif l["type"] == "group":
                strip(l["layers"])
    strip(m["layers"])
    return m

def prop(pid, **kw):
    d = {"id": pid}; d.update(kw); return d
def area(aid, name, x, y, w, h, props):
    return {"id": aid, "x": px(x), "y": px(y), "width": px(w), "height": px(h),
            "visible": True, "name": name, "properties": props}
def wam(map_url, name, description, areas, thumbnail=None, copyright_=None):
    return {"version": "2.1.0", "mapUrl": map_url, "areas": areas, "entities": {},
            "entityCollections": ENTITY_COLLECTIONS,
            "settings": {"megaphone": {"enabled": True, "title": name}},
            "metadata": {"name": name, "description": description,
                         "thumbnail": thumbnail, "copyright": copyright_}}

# ---------- TEAM FLOOR layout (on office_base.tmj, 31x21) ----------
# room rectangles are (x,y,w,h) in TILES
FLOOR_ROOMS = {
    "leader":  (1, 3, 6, 4),     # top-left enclosed room
    "m1":      (8, 3, 4, 4),     # central grid
    "m2":      (13, 3, 4, 4),
    "m3":      (8, 8, 4, 4),
    "m4":      (13, 8, 4, 4),
    "meeting": (24, 8, 6, 5),    # right enclosed room -> Jitsi
    "breakout":(20, 17, 7, 4),   # bottom-right
    "board":   (1, 3, 3, 1),     # notice board strip in leader room doorway
    "lift":    (1, 17, 2, 2),    # bottom-left -> lift to lobby
    "arrive":  (5, 19, 1, 1),    # arrival from lobby (separated from lift)
}

def build_floor(spec):
    k = spec["teamKey"]; tn = spec["teamName"]; accent = spec["accentColor"]
    R = FLOOR_ROOMS
    a = []
    x,y,w,h = R["leader"]
    a.append(area(f"{k}-leader", f"{spec['leader']['name']} — {spec['leader']['title']} ({tn} Lead)", x,y,w,h, [
        prop(f"{k}-leader-focus", type="focusable", zoom_margin=0.4),
        prop(f"{k}-leader-hl", type="highlight", color=accent, opacity=0.35),
        prop(f"{k}-leader-desc", type="areaDescriptionProperties",
             description=f"{tn} team-leader office — {spec['leader']['name']}, {spec['leader']['title']}.", searchable=True),
    ]))
    for i, mkey in enumerate(["m1","m2","m3","m4"], start=1):
        m = spec["members"][i-1]
        x,y,w,h = R[mkey]
        a.append(area(f"{k}-{mkey}", f"{m['name']} — {m['role']}", x,y,w,h, [
            prop(f"{k}-{mkey}-focus", type="focusable", zoom_margin=0.5),
            prop(f"{k}-{mkey}-desc", type="areaDescriptionProperties",
                 description=f"{m['name']}'s office ({m['role']}, {tn}).", searchable=True),
        ]))
    x,y,w,h = R["meeting"]
    a.append(area(f"{k}-meeting", spec["meetingRoom"]["name"], x,y,w,h, [
        prop(f"{k}-meeting-focus", type="focusable", zoom_margin=0.4),
        prop(f"{k}-meeting-hl", type="highlight", color=accent, opacity=0.3),
        prop(f"{k}-meeting-jitsi", type="jitsiRoomProperty", roomName=spec["meetingRoom"]["jitsiSlug"],
             trigger="onaction", closable=True,
             jitsiRoomConfig={"startWithAudioMuted": True, "startWithVideoMuted": False},
             triggerMessage=f"Press SPACE to join {spec['meetingRoom']['name']}"),
    ]))
    x,y,w,h = R["breakout"]
    a.append(area(f"{k}-breakout", spec["breakout"]["name"], x,y,w,h, [
        prop(f"{k}-breakout-desc", type="areaDescriptionProperties",
             description=spec["breakout"]["blurb"], searchable=True),
    ]))
    x,y,w,h = R["board"]
    a.append(area(f"{k}-board", spec["noticeBoard"]["label"], x,y,w,h, [
        prop(f"{k}-board-web", type="openWebsite", link=spec["noticeBoard"]["placeholderUrl"],
             trigger="onaction", newTab=False, closable=True, width=50,
             buttonLabel=f"Open {tn} board", application="website"),
    ]))
    x,y,w,h = R["lift"]
    a.append(area(f"{k}-lift", "🛗 Lift → Lobby", x,y,w,h, [
        prop(f"{k}-lift-exit", type="exit", url="lobby.wam", areaName=f"from-{k}"),
    ]))
    x,y,w,h = R["arrive"]
    a.append(area(f"{k}-arrive", "from-lobby", x,y,w,h, [
        prop(f"{k}-arrive-start", type="start", isDefault=True),
    ]))
    return wam("./office_base.tmj", f"{tn} — Floor", spec.get("floorDescription", f"{tn} team floor."), a,
               thumbnail="office.png")

# ---------- LOBBY layout (on office_base.tmj) ----------
def build_lobby(spec, floor_specs):
    a = []
    # default spawn / reception
    a.append(area("lobby-start", "reception-start", 3, 4, 2, 2, [
        prop("lobby-start-p", type="start", isDefault=True)]))
    a.append(area("lobby-reception", "CloudZA Plex — Reception", 1, 3, 6, 4, [
        prop("lobby-reception-desc", type="areaDescriptionProperties",
             description=spec["directoryBlurb"], searchable=True)]))
    a.append(area("lobby-board", spec["welcome"]["label"], 1, 3, 3, 1, [
        prop("lobby-board-web", type="openWebsite", link=spec["welcome"]["placeholderUrl"],
             trigger="onaction", newTab=False, closable=True, width=50,
             buttonLabel="Open the plex welcome board", application="website")]))
    # Lift bank -> each floor + townhall (in the right-hand room), stacked
    lifts = [
        ("alpha", floor_specs[0]["accentColor"], spec["liftLabels"]["alpha"], 24, 8),
        ("bravo", floor_specs[1]["accentColor"], spec["liftLabels"]["bravo"], 24, 10),
        ("charlie", floor_specs[2]["accentColor"], spec["liftLabels"]["charlie"], 24, 12),
    ]
    for key, accent, label, lx, ly in lifts:
        a.append(area(f"lobby-lift-{key}", label, lx, ly, 6, 1, [
            prop(f"lobby-lift-{key}-hl", type="highlight", color=accent, opacity=0.35),
            prop(f"lobby-lift-{key}-exit", type="exit", url=f"floor_{key}.wam", areaName="from-lobby")]))
    # Townhall lift (bottom area)
    a.append(area("lobby-lift-townhall", spec["liftLabels"]["townhall"], 20, 17, 7, 2, [
        prop("lobby-lift-townhall-hl", type="highlight", color="#8a6d3b", opacity=0.3),
        prop("lobby-lift-townhall-exit", type="exit", url="townhall.wam", areaName="from-lobby")]))
    # arrival starts back from each floor + townhall (clustered near reception, away from lifts)
    for key, ax, ay in [("alpha", 9, 4), ("bravo", 11, 4), ("charlie", 13, 4), ("townhall", 15, 4)]:
        a.append(area(f"lobby-from-{key}", f"from-{key}", ax, ay, 1, 1, [
            prop(f"lobby-from-{key}-p", type="start")]))
    return wam("./office_base.tmj", "CloudZA Plex — Lobby", spec["directoryBlurb"], a, thumbnail="office.png")

# ---------- TOWNHALL layout (on townhall_base.tmj, 24x14) ----------
def build_townhall(copyright_):
    a = [
        area("th-stage", "All-hands Stage", 1, 3, 6, 2, [
            prop("th-stage-focus", type="focusable", zoom_margin=0.3),
            prop("th-stage-spk", type="speakerMegaphone", name="cloudza-townhall", chatEnabled=True, seeAttendees=True)]),
        area("th-audience", "All-hands Audience", 1, 5, 6, 8, [
            prop("th-aud-lst", type="listenerMegaphone", speakerZoneName="cloudza-townhall", chatEnabled=True)]),
        area("th-board", "All-hands Notice Board", 8, 3, 3, 2, [
            prop("th-board-web", type="openWebsite", link="https://REPLACE-ME.example.com/cloudza-allhands-agenda",
                 trigger="onaction", newTab=False, closable=True, width=50,
                 buttonLabel="Open all-hands agenda", application="website")]),
        area("th-mr-a", "Overflow Room — Green", 12, 3, 5, 5, [
            prop("th-mra-focus", type="focusable", zoom_margin=0.4),
            prop("th-mra-jitsi", type="jitsiRoomProperty", roomName="cloudza-overflow-green",
                 trigger="onaction", closable=True,
                 jitsiRoomConfig={"startWithAudioMuted": True, "startWithVideoMuted": False},
                 triggerMessage="Press SPACE to join the Green overflow room")]),
        area("th-mr-b", "Overflow Room — Purple", 17, 6, 5, 6, [
            prop("th-mrb-focus", type="focusable", zoom_margin=0.4),
            prop("th-mrb-jitsi", type="jitsiRoomProperty", roomName="cloudza-overflow-purple",
                 trigger="onaction", closable=True,
                 jitsiRoomConfig={"startWithAudioMuted": True, "startWithVideoMuted": False},
                 triggerMessage="Press SPACE to join the Purple overflow room")]),
        area("th-lift", "🛗 Lift → Lobby", 19, 3, 3, 2, [
            prop("th-lift-exit", type="exit", url="lobby.wam", areaName="from-townhall")]),
        area("th-arrive", "from-lobby", 20, 6, 1, 1, [
            prop("th-arrive-start", type="start", isDefault=True)]),
    ]
    return wam("./townhall_base.tmj", "CloudZA Plex — Townhall", "All-hands townhall & event space.", a,
               thumbnail="conference.png", copyright_=copyright_)

def render(specs):
    lobby_spec = specs["lobby"]; floors = specs["floors"]
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(SRC, "tilesets"), os.path.join(OUT, "tilesets"))
    if os.path.exists(os.path.join(OUT, "tilesets", "README.md")):
        os.remove(os.path.join(OUT, "tilesets", "README.md"))
    # shared base art
    office = clean_tmj("office.tmj"); townhall = clean_tmj("conference.tmj")
    json.dump(office, open(f"{OUT}/office_base.tmj", "w"))
    json.dump(townhall, open(f"{OUT}/townhall_base.tmj", "w"))
    shutil.copy(f"{SRC}/office.png", f"{OUT}/office.png")
    shutil.copy(f"{SRC}/conference.png", f"{OUT}/conference.png")
    def mapmeta(m, key):
        for p in m.get("properties", []):
            if p["name"] == key: return p["value"]
    th_copy = mapmeta(townhall, "mapCopyright")
    # wams
    json.dump(build_lobby(lobby_spec, floors), open(f"{OUT}/lobby.wam", "w"), indent=2)
    for fs in floors:
        json.dump(build_floor(fs), open(f"{OUT}/floor_{fs['teamKey']}.wam", "w"), indent=2)
    json.dump(build_townhall(th_copy), open(f"{OUT}/townhall.wam", "w"), indent=2)
    print("Rendered plex to", OUT)
    print(sorted(os.listdir(OUT)))

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1]))
    render(specs)
    # summary
    for fs in specs["floors"]:
        print(f"  {fs['teamName']}: leader {fs['leader']['name']}, members {[m['name'] for m in fs['members']]}, jitsi {fs['meetingRoom']['jitsiSlug']}")
