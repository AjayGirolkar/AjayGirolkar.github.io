#!/usr/bin/env python3
"""SocialFlow content model + image tokens.

Social's identity lock says the content IS the colour, so the whole app is one hot
accent on mono and everything else is photography. That makes this file, not the CSS,
the place the app's character actually lives: the cast, the captions, the counts.

Two jobs:
  1. CAST / POSTS / GRID -- plausible-specific data (rule 4). Handles that read real,
     captions with a voice, likes >> comments > shares, relative timestamps that agree
     with each other.
  2. Image tokens -- cover-crop to the slot, apply ONE shared grade, encode WEBP base64.

Why the shared grade: 137 CC0 files from 137 different shoots have 137 different
black points and white balances. Dropped edge-to-edge on one black ground they read as
a scrapbook of found images. `grade()` lifts every black to the same cool 6/255, warms
every highlight the same amount and pulls saturation back 8%, which is what makes them
read as one feed. It is deliberately mild -- social is the one register where the
photography must stay louder than the treatment.

NOTE, recorded so the next session does not lose an hour: Openverse's anonymous API
starts returning **HTTP 403** after a few hundred requests from one IP. It is a quota,
not a ban -- it clears -- but it means the imagery pull is a hard dependency to finish
BEFORE layout, exactly as real-imagery.md says. Register for a client id if a session
needs more than ~150 files.

    python3 feed.py build      # -> media.json
    python3 feed.py sheet      # -> _graded.png, check the grade at final scale
"""
import base64, io, json, os, sys
from PIL import Image, ImageEnhance

SRC = "src"

# ---------------------------------------------------------------- the cast
# avatar = a src id whose face survives a 1:1 crop. `y` biases the crop up to the head.
CAST = {
    "maya":  ("Maya Rehani",   "maya.builds",   "54c6102e-a7bd-46c1-a65e-cc0e71da1188", .34),
    "tarek": ("Tarek Osman",   "tarek.frames",  "2f90eca1-984c-4e5e-a8fc-c2d463f5c38e", .40),
    "juno":  ("Juno Park",     "juno.clay",     "ae2d14d8-cd19-4ad1-bd1f-f18f11b124a5", .38),
    "dhruv": ("Dhruv Kale",    "dhruv.rides",   "94865ff9-25be-4711-8558-3f3c951fe727", .38),
    "lise":  ("Lise Kaufmann", "lise.k",        "4242b028-8a16-4c02-b9c7-24a4b019ec90", .34),
    "ana":   ("Ana Nkosi",     "ana.market",    "c79e32d2-84fc-4a60-bfd7-62f610d0aea8", .30),
    "sam":   ("Sam Whitlock",  "sam.offgrid",   "8ad56f4d-62be-4493-bff8-2d0b76f7ccfd", .36),
    "noor":  ("Noor Haddad",   "noor.ceramics", "f02bd930-f832-4787-bb16-8e2c6d51e4da", .34),
    "rin":   ("Rin Sato",      "rin.eats",      "d9a39e1e-e09e-432e-a1e0-bbd0e5bf1857", .30),
    "priya": ("Priya Menon",   "pri.skates",    "b7ef98f8-2cf2-4e02-9fe9-2f72d77aebfb", .32),
    "elena": ("Elena Marin",   "elena.surf",    "2c105df8-3b6e-4db1-a1e0-28b2100fdd47", .30),
    "theo":  ("Theo Baptiste", "theo.trail",    "05d03c60-b8b3-49bc-a216-6b6df7f73ebd", .26),
    "you":   ("Ajay Girolkar", "ajay",          "f10dc851-544c-46cc-a4f3-c1ed6c1f7ff2", .34),
}

# ---------------------------------------------------------------- the feed
# key: (author, src id, aspect, crop-y, caption, likes, comments, shares, when, place)
POSTS = {
 "air":   ("priya", "befd289b-81d6-4f21-9c07-03bedba61cdf", (1, 1), .52,
           "Forty minutes on one kerb for four inches of air. Would do it again tomorrow.",
           4218, 96, 31, "2h", "Lower Parel"),
 "wheel": ("juno", "5af743d5-6438-46fa-8328-ca0092e728b0", (4, 5), .50,
           "Centring is ninety percent of it and nobody tells you that for a year.",
           1874, 143, 12, "5h", "Studio 12"),
 "bike":  ("dhruv", "62e6cf88-ec1f-475b-b3b4-e238a8336a9c", (4, 5), .50,
           "Whole city from up here and the only thing moving is one guy on a Sunday.",
           9042, 211, 340, "8h", "Copenhagen"),
 "cart":  ("rin", "dbc82ee8-2fb3-4732-9d99-c6884d6b31e5", (4, 5), .46,
           "Same cart, same aunty, eleven years. She still charges me student price.",
           2610, 74, 19, "1d", "Bangkok"),
}

# post-detail hero -- one immersive full-bleed screen
HERO = ("elena", "716b5435-6913-447c-b71f-a007a7955d2c", (393, 852), .44,
        "Nobody caught anything after six. We stayed in until the light went anyway. "
        "Best session of the year and there is no wave in it.",
        12480, 318, 512, "4h", "Soorts-Hossegor")

# explore mosaic -- one 2x2 anchor, the rest 1x1, 1pt gutters
EXPLORE = [
 ("c454a960-7b14-4ee0-b8ad-f0fa350817e5", 2), ("1aad938a-8c00-4389-a914-99beb9ce2a22", 1),
 ("77279cf1-ae9d-4f02-9e95-39eaf645c11d", 1), ("53b4cf79-e669-4dc9-a42e-e3b602b7512c", 1),
 ("ed9d164d-7dba-41e3-875f-59340d5b901c", 1), ("87f6fe8a-8732-4f0d-be33-bec21cd7c420", 1),
 ("7b861544-b6b1-4856-a93b-810e97d2a9ac", 1), ("e56084bb-58fe-48d8-81c5-1b99937601ce", 1),
 ("f7033903-d0b9-438d-abf0-5c9ece758f85", 1), ("151b4fba-e9ca-45a8-ade8-64716b39dccd", 1),
 ("3d1a0af7-ca6e-494c-a96a-90a1d9c82615", 1), ("a01ecc5c-176b-4d1f-a445-655ff2184e3a", 1),
 ("17673283-81e8-4432-8bd3-13dd928a2fe0", 1), ("73fa8de8-0e25-4903-b220-5e7012645d4a", 1),
]

# profile 3-up -- Elena's own grid, so it must read as one person's eye: water, board, coast
GRID = ["befd289b-81d6-4f21-9c07-03bedba61cdf", "4e251b3d-2d54-4bd0-928b-ba4c645c9f40",
        "8c5e01e2-4bf7-4209-9ed4-f81c1c10691c", "2cf7bca1-07b7-4666-92a7-b74d93620fa6",
        "3e01adf1-a18b-44bd-821a-3b13d22dfa44", "5c2a6986-e912-4824-9014-275d4f665e0e",
        "c84a0a5a-29eb-4d86-b436-af730f5c72d0", "0dae16d7-1eb0-4cfb-b5ca-15cafcd1c618",
        "e8d61457-21ff-4180-a2d5-78d9bd07bb06"]

# compose tray -- camera roll recents
TRAY = ["3e01adf1-a18b-44bd-821a-3b13d22dfa44", "5c2a6986-e912-4824-9014-275d4f665e0e",
        "2cf7bca1-07b7-4666-92a7-b74d93620fa6", "c84a0a5a-29eb-4d86-b436-af730f5c72d0",
        "e8d61457-21ff-4180-a2d5-78d9bd07bb06", "0dae16d7-1eb0-4cfb-b5ca-15cafcd1c618",
        "4e251b3d-2d54-4bd0-928b-ba4c645c9f40", "87f6fe8a-8732-4f0d-be33-bec21cd7c420"]


# ---------------------------------------------------------------- treatment
def _lut(shadow, high, gamma=1.0):
    """One channel: lift the black point to `shadow`, pull the white down to `high`."""
    return [max(0, min(255, round(shadow + (high - shadow) * (i / 255) ** gamma)))
            for i in range(256)]


def grade(im):
    """The one shared grade. Cool lifted blacks, faintly warm highs, -8% saturation.

    Mild on purpose. Turn it up and the feed starts looking like a filter demo, which is
    the opposite of the brief: in social the photography is the design."""
    im = im.convert("RGB")
    r = _lut(4, 252, .96)      # red    -- neutral
    g = _lut(5, 250, .97)
    b = _lut(9, 247, .99)      # blue   -- highest black lift = cool shadows
    im = im.point(r + g + b)
    im = ImageEnhance.Color(im).enhance(.92)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im


def cover(im, w, h, y=.5, x=.5):
    """Cover-crop to an exact slot. A wide slot is composed wide, never a tall plate
    cropped -- `object-fit:cover` on a tall source cuts the subject's feet off."""
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((max(w, int(sw * s + .5)), max(h, int(sh * s + .5))), Image.LANCZOS)
    sw, sh = im.size
    return im.crop((int((sw - w) * x), int((sh - h) * y),
                    int((sw - w) * x) + w, int((sh - h) * y) + h))


def uri(im, q=72):
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=q, method=5)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def load(i):
    return Image.open(f"{SRC}/{i}.jpg")


# ---------------------------------------------------------------- token table
def build():
    T = {}
    for k, (name, handle, sid, y) in CAST.items():
        T[f"AV_{k.upper()}"] = uri(cover(grade(load(sid)), 168, 168, y), 74)
        T[f"NM_{k.upper()}"] = name
        T[f"HD_{k.upper()}"] = handle

    for k, (who, sid, (aw, ah), y, cap, li, co, sh, when, place) in POSTS.items():
        W = 1000
        T[f"IM_{k.upper()}"] = uri(cover(grade(load(sid)), W, round(W * ah / aw), y))
        T[f"CAP_{k.upper()}"] = cap
        T[f"LI_{k.upper()}"] = f"{li:,}"
        T[f"CO_{k.upper()}"] = str(co)
        T[f"SH_{k.upper()}"] = str(sh)
        T[f"WH_{k.upper()}"] = when
        T[f"PL_{k.upper()}"] = place
        T[f"AU_{k.upper()}"] = CAST[who][1]
        T[f"AUA_{k.upper()}"] = T[f"AV_{who.upper()}"]

    who, sid, (w, h), y, cap, li, co, sh, when, place = HERO
    T["IM_HERO"] = uri(cover(grade(load(sid)), 1000, round(1000 * h / w), y), 76)
    T["CAP_HERO"], T["WH_HERO"], T["PL_HERO"] = cap, when, place
    T["LI_HERO"], T["CO_HERO"], T["SH_HERO"] = f"{li:,}", str(co), str(sh)

    for n, (sid, span) in enumerate(EXPLORE, 1):
        px = 520 if span == 2 else 260
        T[f"EX{n}"] = uri(cover(grade(load(sid)), px, px), 70)
    for n, sid in enumerate(GRID, 1):
        T[f"GR{n}"] = uri(cover(grade(load(sid)), 390, 390), 70)
    for n, sid in enumerate(TRAY, 1):
        T[f"TR{n}"] = uri(cover(grade(load(sid)), 240, 240), 68)
    # composed WIDE for a wide slot -- a 296pt-tall composer slot fed a tall plate would
    # show the middle of the frame and cut the skater's board off (real-imagery.md 4)
    T["IM_PICK"] = uri(cover(grade(load(TRAY[0])), 1000, 760, .52), 74)
    return T


def sheet():
    """Graded, at the size each one actually ships at. Cutout and grade defects are
    invisible on a thumbnail sheet and glaring at final scale."""
    T = build()
    keys = [k for k in T if k.startswith(("IM_", "EX", "GR", "AV_"))]
    cells = "".join(f'<figure><img src="{T[k]}"><figcaption>{k}</figcaption></figure>'
                    for k in sorted(keys))
    open("_graded.html", "w").write(
        '<!doctype html><meta charset="utf-8"><style>body{background:#000;color:#888;'
        'font:11px system-ui;display:flex;flex-wrap:wrap;gap:8px;margin:8px}'
        'figure{margin:0;width:180px}img{width:180px;display:block}</style>' + cells)
    print(f"{len(keys)} images -> _graded.html")
    print("bytes:", sum(len(v) for v in T.values()) // 1024, "KB of base64")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "build"
    if c == "sheet":
        sheet()
    else:
        json.dump(build(), open("media.json", "w"))
        print("media.json", os.path.getsize("media.json") // 1024, "KB")
