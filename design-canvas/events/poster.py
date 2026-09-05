#!/usr/bin/env python3
"""Poster plates + the per-event theme extracted FROM the plate.

GATE's identity lock is "the poster art is the ground". That only works if the ground,
the accent and the rim are DERIVED from each event's artwork rather than picked by hand
-- otherwise it is seven screens with a photo on them, which every ticketing app already
is. So this file does two jobs and they are the same job:

  1. crop each source frame to the box a layout needs, at 2x, as WEBP data URIs;
  2. read the dominant chroma back out of that crop and emit its --ev-* token block.

Screen 02 is the proof: eight events stacked in one list, eight different palettes, none
of them chosen by a designer. Change the poster, change the app.

Crop boxes are FRACTIONAL, never pixel. Sources here run 1920x1272 to 1920x1554 and
absolute boxes silently mis-crop the taller ones. (Same trap the fitness session hit.)
"""
import base64, colorsys, io, json
from PIL import Image

SRC = "src"

# The bill. key -> (source slug, fractional crop box, artist, meta)
# Fictional artists on purpose: a real name over a stock photo of a different band is
# an impersonation, not a mockup.
EVENTS = {
    "antipodes": ("guitarist-bathed-in-red-light-unsplash",       (.13, .00, .60, 1.0),
                  "Antipodes",      "The Foundry, Sheffield"),
    "halflight": ("silhouettes-against-pale-stage-smoke-unsplas", (.10, .04, .90, .96),
                  "Half Light",     "Band on the Wall, Manchester"),
    "meridian":  ("musicians-at-velour-live-music-gallery-unspl", (.08, .02, .92, .94),
                  "Meridian Bloom", "The Hare & Hounds, Birmingham"),
    "kestrel":   ("smoke-and-light-beams-unsplash",               (.06, .06, .94, .98),
                  "Kestrel Down",   "Corsica Studios, London"),
    "northsea":  ("rock-concert-in-intense-light-unsplash",       (.04, .02, .96, .96),
                  "North Sea Radio","Sub Club, Glasgow"),
    "saltpine":  ("singer-in-concert-unsplash",                   (.10, .00, .90, .94),
                  "Salt & Pine",    "Whelan's, Dublin"),
    "sinfonia":  ("rehearsing-for-the-violin-concert-unsplash",   (.14, .04, .88, .96),
                  "City Sinfonia",  "St George's, Bristol"),
    "lowtide":   ("put-your-hands-in-the-air-unsplash",           (.05, .05, .95, .98),
                  "Low Tide Choir", "Green Man, Brecon Beacons"),
    "crowd":     ("looking-into-festival-crowd-unsplash",         (.08, .00, .92, .96),
                  "Field Day",      "Victoria Park, London"),
    "silhouette":("performing-for-the-crowd-unsplash-xudii04ohp", (.16, .00, .84, .94),
                  "Ghost Signal",   "Berghain, Berlin"),
}

# key -> (event, out size). One event can appear at several sizes; each is its own token.
PLATES = {
    "HERO":     ("antipodes",  (786, 1120)),   # s1 poster ground
    "TKT":      ("antipodes",  (720,  420)),   # s5 ticket band
    "CHK":      ("antipodes",  (200,  260)),   # s4 checkout thumb
    "SUP1":     ("halflight",  (208,  208)),
    "SUP2":     ("meridian",   (208,  208)),
    "SUP3":     ("kestrel",    (208,  208)),
    # s2 discover strips
    "R_KESTREL":  ("kestrel",   (786, 300)),
    "R_NORTHSEA": ("northsea",  (786, 300)),
    "R_SALTPINE": ("saltpine",  (786, 300)),
    "R_SINFONIA": ("sinfonia",  (786, 300)),
    "R_LOWTIDE":  ("lowtide",   (786, 300)),
    # s3 artist
    "ART_HERO": ("silhouette", (786,  760)),
    "ART_1":    ("crowd",      (360,  360)),
    "ART_2":    ("lowtide",    (360,  360)),
    "ART_3":    ("northsea",   (360,  360)),
    # s6 sold out
    "SOLD":     ("halflight",  (786,  620)),
    # s7 wallet stubs
    "W1":       ("saltpine",   (300,  220)),
    "W2":       ("sinfonia",   (300,  220)),
    "W3":       ("crowd",      (300,  220)),
}


def crop(slug, box, size):
    im = Image.open(f"{SRC}/{slug}.jpg").convert("RGB")
    l, t, r, b = box
    im = im.crop((round(l * im.width), round(t * im.height),
                  round(r * im.width), round(b * im.height)))
    s = max(size[0] / im.width, size[1] / im.height)      # cover-fit
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x, y = (im.width - size[0]) // 2, (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))


def uri(im, q=78):
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def _lum(hexrgb):
    """WCAG relative luminance from a #RRGGBB string."""
    c = [int(hexrgb[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def _cr(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def _hex(h, l, s):
    return "#%02X%02X%02X" % tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))


def _solve(h, s, bg, target, lo=.30, hi=.86):
    """Lightness at which hue h / saturation s hits `target` contrast against bg.

    The first cut of this file used fixed HLS constants -- ground at L.055/S.46 and accent
    at L.505/S.86 -- and both were wrong in the same direction. The ground came out a
    near-black blood colour and the accent came out max-chroma neon sitting on it at 11:1,
    which is glare, not hierarchy: the exact failure the fitness session hit with lime at
    near-max luminance AND chroma on pure black. Contrast is a RATIO, so solve for it
    instead of guessing a lightness that only happens to work for one hue.
    """
    for _ in range(30):
        mid = (lo + hi) / 2
        if _cr(_hex(h, mid, s), bg) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def theme(im):
    """Dominant chroma of the plate -> that event's ground, accent and scrim.

    Mean colour is useless here: a red-lit stage averages to mud. What reads as "the
    colour of this poster" is the most saturated populated hue, so quantize, drop the
    near-greys, and weight what survives by pixel count * saturation^1.5.

    The RAMP is then solved, not chosen:
      ground   a tinted charcoal, not a black -- L .105 at S .20, so the hue is present
               but the screen is never a hole. Photography reads against it; pure black
               makes every plate look like it is floating in a void.
      accent   saturation held at .66 (NOT the .86 the plate actually contains -- source
               chroma is a stage light, not a UI token) and lightness solved to ~4.6:1
               against that event's own ground. Same perceived weight on every hue, which
               a fixed lightness never gives you: #ED8114 amber at L.505 is nearly twice
               as bright as #1461ED blue at the same L.
      on-accent picked, not assumed -- whichever of ink/paper actually clears 4.5:1.
    """
    q = im.convert("RGB").resize((120, 120)).quantize(colors=24, method=Image.MEDIANCUT)
    best, score = None, -1
    for n, rgb in sorted(q.convert("RGB").getcolors(14400), reverse=True):
        h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in rgb])
        if s < .25 or l < .12 or l > .90:
            continue
        w = n * (s ** 1.5)
        if w > score:
            best, score = (h, l, s), w
    # A black-and-white plate has no chroma to extract and must NOT fall through to
    # hue 0 -- that silently themes a mono poster bright red.
    h, sat = (best[0], 1.0) if best else (0.0, 0.0)

    ink = _hex(h, .105, .20 * sat)
    ink2 = _hex(h, .165, .17 * sat)
    a_s = .66 * sat
    # A chroma-free event has no hue to carry the accent, so it has to buy the same
    # "this is the accent" signal with lightness instead. At 4.6:1 grey lands on #838383,
    # which reads as disabled text; silver at ~7.5:1 reads as a decision.
    a_l = _solve(h, a_s, ink, 4.6 if sat else 7.5)
    accent = _hex(h, a_l, a_s)
    on = "#0C0A0B" if _cr(accent, "#0C0A0B") >= _cr(accent, "#FFFFFF") else "#FFFFFF"
    return dict(hue=round(h * 360), chroma=round(sat * 100),
                ink=ink, ink2=ink2, accent=accent,
                accent_lo=_hex(h, .30, .40 * sat),
                scrim=_hex(h, .085, .24 * sat), on=on,
                cr=round(_cr(accent, ink), 2), cr_on=round(_cr(accent, on), 2))


def build():
    """-> (token table, {event: theme}). One quantize per EVENT, not per plate."""
    th = {}
    for k, (slug, box, _a, _v) in EVENTS.items():
        th[k] = theme(crop(slug, box, (420, 420)))

    tok = {}
    for k, (ev, size) in PLATES.items():
        slug, box = EVENTS[ev][0], EVENTS[ev][1]
        tok["IMG_" + k] = uri(crop(slug, box, size))

    # BOTH selectors, every time. A theme class lands on the .ios root on the
    # single-event screens and on a DESCENDANT strip on the discover screen, and
    # ".ios .ev-x" silently matches only the second: five screens rendered with every
    # --ev-* token undefined, which is invisible rather than broken -- the grounds fell
    # through to body black and the accent fills to transparent. Cost a full render pass.
    rules = "\n".join(
        ".ios.ev-%s,.ios .ev-%s{--ev-ink:%s;--ev-ink-2:%s;--ev:%s;--ev-lo:%s;--ev-scrim:%s;--on-ev:%s}" % (
            k, k, t["ink"], t["ink2"], t["accent"], t["accent_lo"], t["scrim"], t["on"])
        for k, t in th.items())
    # MUST be wrapped in <style>. Emitted bare it becomes a TEXT NODE at the top of
    # .stack -- invisible (ink on ink) but it still takes a line box, which shoves the
    # status bar ~90pt down the screen while no colour applies anywhere. Cost a render.
    tok["EVTHEME"] = ("<style>/* extracted per event by poster.theme(). Nothing below was\n"
                      "   picked by hand -- the palettes are read out of the artwork. */\n"
                      ".ios{--on-ev:#0C0A0B}\n" + rules + "</style>")
    return tok, th


if __name__ == "__main__":
    t, th = build()
    for k, v in th.items():
        print(f"{k:11s} hue {v['hue']:3d}  ink {v['ink']}  accent {v['accent']}"
              f"  {v['cr']:>5}:1 on ground  {v['cr_on']:>5}:1 for its label")
    tot = sum(len(v) for k, v in t.items() if k.startswith("IMG"))
    print(f"\n{len([k for k in t if k.startswith('IMG')])} plates, {tot//1024} KB of data URIs")
