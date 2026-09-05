import sys, os, math

# Nocturne has NO photography -- a sleep app that shows you a stock photo of a bed is
# advertising, not a product. So rule 7 lands entirely on the content, and the content is
# real sleep science: 4-7-8 breathing (Weil), sleep latency, the four-stage hypnogram with
# plausible cycle lengths, the nocturnal heart-rate dip, and a real 90-minute cycle count.
# "Good night! Sweet dreams :)" kills the screenshot.

SB = ('<div class="island"></div>'
      '<div class="statusbar"><span>9:41</span><span class="glyphs">'
      '<span class="sb-sig"><i></i><i></i><i></i><i></i></span>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">'
      '<path d="M8.5 10.6 10.7 8.3a3.1 3.1 0 0 0-4.4 0ZM4.6 6.7l1.3 1.3a4.9 4.9 0 0 1 5.2 0'
      'l1.3-1.3a6.7 6.7 0 0 0-7.8 0ZM1.6 3.6 2.9 5a9.3 9.3 0 0 1 11.2 0l1.3-1.4a11.1 11.1 0 0 0-13.8 0Z"/>'
      '</svg><span class="sb-bat"><b></b></span></span></div>')

def qr(seed="GATE-ANTIPODES-14MAR26-A7F2", n=21):
    """A 21x21 block matrix with real finder squares, alignment block and quiet timing
    rows, filled deterministically from a hash of the order id.

    Drawn rather than shipped as an image on purpose: a random noise square reads as
    placeholder art the second anyone looks at the screenshot, and a REAL scannable code
    in a portfolio is a live payload pointing at nothing. Structure without a payload is
    the honest middle."""
    import hashlib
    h = hashlib.sha256(seed.encode()).digest() * 12
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            g[i][j] = (h[(i * n + j) % len(h)] >> ((i + j) % 7)) & 1
    def finder(r, c):
        for i in range(7):
            for j in range(7):
                g[r + i][c + j] = 1 if (i in (0, 6) or j in (0, 6)
                                        or (2 <= i <= 4 and 2 <= j <= 4)) else 0
        for i in range(-1, 8):                      # quiet separator
            for j in range(-1, 8):
                if 0 <= r + i < n and 0 <= c + j < n and (i in (-1, 7) or j in (-1, 7)):
                    g[r + i][c + j] = 0
    finder(0, 0); finder(0, n - 7); finder(n - 7, 0)
    for i in range(8, n - 8):                       # timing rows
        g[6][i] = g[i][6] = (i + 1) % 2
    for i in range(5):                              # alignment block
        for j in range(5):
            g[n - 9 + i][n - 9 + j] = 1 if (i in (0, 4) or j in (0, 4) or (i == 2 and j == 2)) else 0
    return "".join('<s style="grid-area:%d/%d"></s>' % (i + 1, j + 1)
                   for i in range(n) for j in range(n) if g[i][j])


def hypnogram(w=337, h=104):
    """A real four-stage hypnogram as an SVG polyline.

    Drawn from an actual night rather than a pretty wave: sleep opens with a fast descent
    to N3, the first two cycles carry most of the deep sleep, REM periods LENGTHEN toward
    morning while deep sleep disappears, and there are three brief wakes. A sine wave
    would be smoother and would also be a lie about how sleep works.
    Rows: 0 awake, 1 REM, 2 light (N1/N2), 3 deep (N3).
    """
    night = [(0, 0, .04), (2, .04, .10), (3, .10, .21), (2, .21, .25), (1, .25, .29),
             (2, .29, .34), (3, .34, .44), (2, .44, .48), (1, .48, .54), (0, .54, .55),
             (2, .55, .60), (3, .60, .66), (2, .66, .70), (1, .70, .78), (2, .78, .82),
             (0, .82, .83), (2, .83, .87), (1, .87, .95), (2, .95, .98), (0, .98, 1.0)]
    row = lambda r: 6 + r * (h - 12) / 3
    pts = []
    for r, a, b in night:
        pts += [f"{a*w:.1f},{row(r):.1f}", f"{b*w:.1f},{row(r):.1f}"]
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="none">'
            '<polyline points="%s" stroke="var(--ink-2)" stroke-width="1.6" '
            'stroke-linejoin="round" stroke-linecap="round"/></svg>') % (w, h, w, h, " ".join(pts))


def mixer(level, w=337, h=26, n=44):
    """A soundscape level as a row of ticks. Deterministic, so the three rows differ from
    each other but never re-roll between builds."""
    out = []
    for i in range(n):
        on = (i / (n - 1)) <= level
        hh = 5 + (h - 10) * (0.35 + 0.65 * abs(math.sin(i * 1.7 + level * 9)))
        out.append('<i style="height:%.0f%%;opacity:%s"></i>' % (
            100 * hh / h, ".92" if on else ".16"))
    return "".join(out)


T = {"SB": SB, "HYPNO": hypnogram(),
     "MIX_RAIN": mixer(.72), "MIX_WIND": mixer(.34), "MIX_HUM": mixer(.55)}

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>Nocturne</title>'
            '<style>html,body{margin:0;padding:0;background:#07060F}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
