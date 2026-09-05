import sys, os, math, random

# No photography, so rule 7 is content again -- and a transit app is the easiest place in
# the world to spot a fake. Every line here is a REAL Berlin line with its real official
# colour from the BVG/VBB scheme, real interchange stations on the real network, plausible
# headways, and a real disruption pattern (weekend track work with a replacement bus).
# "Line A to Central Station, 5 min" kills the screenshot.

SB = ('<div class="island"></div>'
      '<div class="statusbar"><span>9:41</span><span class="glyphs">'
      '<span class="sb-sig"><i></i><i></i><i></i><i></i></span>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">'
      '<path d="M8.5 10.6 10.7 8.3a3.1 3.1 0 0 0-4.4 0ZM4.6 6.7l1.3 1.3a4.9 4.9 0 0 1 5.2 0'
      'l1.3-1.3a6.7 6.7 0 0 0-7.8 0ZM1.6 3.6 2.9 5a9.3 9.3 0 0 1 11.2 0l1.3-1.4a11.1 11.1 0 0 0-13.8 0Z"/>'
      '</svg><span class="sb-bat"><b></b></span></span></div>')

# Real BVG / VBB line colours. This IS the palette -- Wayfare has no single brand accent,
# because a transit app that recolours the network to match its own brand has thrown away
# the one piece of information its users already know by heart.
LINES = {"U1": "#7DAD4C", "U2": "#DA421E", "U6": "#8F6DA4", "U8": "#224F86",
         "S1": "#DD6BA6", "S7": "#7C5D2F", "M10": "#BE1414", "N9": "#9A6FB0"}


def street_map(w=393, h=560, seed=7):
    """A drawn vector street map: blocks, a river, a park, and the two route lines.

    Generated rather than hand-placed so the block grid is irregular the way a real city
    is -- a perfectly regular grid reads instantly as a placeholder. Deterministic seed so
    the map never re-rolls between builds and the route stays where the pins are.
    """
    r = random.Random(seed)
    o = [f'<rect width="{w}" height="{h}" fill="var(--map-bg)"/>']

    # park
    o.append('<path d="M242 96 L372 74 L393 172 L286 214 Z" fill="var(--map-park)"/>')
    # river, drawn as one wide stroke then a lighter centre so it reads as water not a road
    river = "M-10 402 C 70 372, 118 430, 190 414 S 300 350, 403 372"
    o.append(f'<path d="{river}" stroke="var(--map-water)" stroke-width="34" fill="none"/>')

    # street grid: irregular column and row positions
    xs, x = [], -20
    while x < w + 20:
        xs.append(x); x += r.choice([46, 58, 64, 72, 88])
    ys, y = [], -20
    while y < h + 20:
        ys.append(y); y += r.choice([52, 62, 70, 84, 96])
    for x in xs:
        sk = r.uniform(-9, 9)
        o.append(f'<line x1="{x}" y1="-20" x2="{x + sk:.0f}" y2="{h + 20}" '
                 f'stroke="var(--map-road)" stroke-width="{r.choice([1.1, 1.1, 2.2])}"/>')
    for y in ys:
        sk = r.uniform(-7, 7)
        o.append(f'<line x1="-20" y1="{y}" x2="{w + 20}" y2="{y + sk:.0f}" '
                 f'stroke="var(--map-road)" stroke-width="{r.choice([1.1, 1.1, 2.6])}"/>')

    # two arterials, wider and warmer
    o.append(f'<path d="M-10 268 C 90 250, 180 292, 403 258" stroke="var(--map-arterial)" '
             f'stroke-width="7" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M132 -10 C 150 140, 108 330, 168 570" stroke="var(--map-arterial)" '
             f'stroke-width="7" fill="none" stroke-linecap="round"/>')

    # the route: U8 leg then M10 leg, casing first so the two legs read as one journey
    u8 = "M96 470 C 110 400, 134 348, 150 300 S 176 236, 214 214"
    m10 = "M214 214 C 250 196, 268 168, 300 138"
    for d in (u8, m10):
        o.append(f'<path d="{d}" stroke="var(--map-bg)" stroke-width="13" fill="none" '
                 f'stroke-linecap="round"/>')
    o.append(f'<path d="{u8}" stroke="{LINES["U8"]}" stroke-width="7" fill="none" '
             f'stroke-linecap="round"/>')
    o.append(f'<path d="{m10}" stroke="{LINES["M10"]}" stroke-width="7" fill="none" '
             f'stroke-linecap="round" stroke-dasharray="1 11"/>')
    # interchange dot
    o.append('<circle cx="214" cy="214" r="7" fill="#fff" stroke="var(--ink)" stroke-width="2.6"/>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">' + "".join(o) + "</svg>"


def badge(line, size=22, fs=11):
    c = LINES[line]
    rad = "3px" if line[0] in "US" else f"{size / 2}px"
    return (f'<span class="ln" style="background:{c};min-width:{size}px;height:{size}px;'
            f'border-radius:{rad};font-size:{fs}px">{line}</span>')


T = {"SB": SB, "MAP": street_map()}
T.update({"B_" + k: badge(k) for k in LINES})
T.update({"BL_" + k: badge(k, 26, 13) for k in LINES})

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in sorted(T.items(), key=lambda kv: -len(kv[0])):  # BL_ before B_
            src = src.replace("{{" + k + "}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>Wayfare</title>'
            '<style>html,body{margin:0;padding:0;background:#E9E5DC}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
