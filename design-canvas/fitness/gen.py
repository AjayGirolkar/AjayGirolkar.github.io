import math, random, sys, os, json

# ---------- curve helpers (harness reuse from fintech/gen.py) ----------
def smooth(pts, w, h, pad=2, lo=None, hi=None):
    n = len(pts)
    lo = min(pts) if lo is None else lo
    hi = max(pts) if hi is None else hi
    rng = (hi - lo) or 1
    P = [(i*(w/(n-1)), pad + (1-(y-lo)/rng)*(h-2*pad)) for i, y in enumerate(pts)]
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in range(n-1):
        p0 = P[i-1] if i > 0 else P[0]; p1 = P[i]; p2 = P[i+1]
        p3 = P[i+2] if i+2 < n else P[-1]
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d, P

def area(d, P, h):
    return f"{d} L{P[-1][0]:.1f},{h} L{P[0][0]:.1f},{h} Z"

def hr(n, seed, base, warm=0.0, drift=0.0, vol=3.2):
    """Heart-rate walk in a believable band: warm-up ramp + surges, 118-178."""
    r = random.Random(seed); v = base; out = []
    for i in range(n):
        t = i/(n-1)
        target = base + warm*min(t/0.22, 1.0) + drift*t
        v += (target - v)*0.14 + r.gauss(0, vol)
        if r.random() < 0.05: v += r.uniform(-7, 11)      # surge / recovery
        out.append(max(112, min(181, v)))
    return out

def ring(r, frac, gap_deg=0.0):
    """dasharray for a stroked arc of `frac` of the circle."""
    C = 2*math.pi*r
    return f"{C*frac:.2f} {C*(1-frac)+C:.2f}", C

T = {}

# ---- s1 : Move ring 612 / 750 kcal ----------------------------------------
for name, rad, frac in (("MOVE", 104, 612/750), ("TRAIN", 24, 41/45), ("STAND", 24, 9/12)):
    da, C = ring(rad, frac)
    T[f"RING_{name}"] = da
    T[f"RINGC_{name}"] = f"{C:.2f}"

# ---- s1 : last-session HR trace, small ------------------------------------
d, P = smooth(hr(70, 12, 122, warm=34, drift=14), 361, 62, 5, lo=108, hi=182)
T["S1_HR_D"] = d; T["S1_HR_A"] = area(d, P, 62)

# ---- s2 : per-row HR traces that bleed behind each history row ------------
for k, (sd, b, w, dr) in {"R1": (31, 124, 30, 10), "R2": (7, 118, 40, 4),
                          "R3": (19, 126, 34, 12), "R4": (44, 121, 36, 6),
                          "R5": (55, 120, 44, 2),  "R6": (63, 127, 28, 9),
                          "R7": (71, 123, 33, 7)}.items():
    d, P = smooth(hr(46, sd, b, warm=w, drift=dr), 393, 74, 8, lo=104, hi=186)
    T[f"S2_{k}_D"] = d; T[f"S2_{k}_A"] = area(d, P, 74)

# ---- s3 : live HR trace, 42:07 elapsed ------------------------------------
d, P = smooth(hr(96, 90, 120, warm=38, drift=18), 393, 126, 10, lo=106, hi=184)
T["S3_HR_D"] = d; T["S3_HR_A"] = area(d, P, 126)
T["S3_HR_X"] = f"{min(P[-1][0],378):.1f}"; T["S3_HR_Y"] = f"{P[-1][1]:.1f}"

# ---- s4 : depleting rest ring (72s of 120s left) --------------------------
da, C = ring(15, 72/120); T["RING_REST"] = da

# ---- s4 : weight ruler, centred on 72.5 kg --------------------------------
# 2.5 kg per major tick, 0.5 kg per minor; 14px per minor step
ticks = []
for i in range(-9, 10):                     # 2.5 kg per minor step, 5 kg per major
    x = 196.5 + i*22
    major = (i % 2 == 0)
    h = 30 if major else 15
    op = ".55" if major else ".22"
    ticks.append(f'<rect x="{x-1:.1f}" y="{4 if major else 12}" width="2" height="{h}" rx="1" '
                 f'fill="var(--ink)" opacity="{op}"/>')
    if major:
        kg = 72.5 + i*2.5
        ticks.append(f'<text x="{x:.1f}" y="52" text-anchor="middle" font-size="11" '
                     f'fill="var(--ink)" opacity=".40">{kg:g}</text>')
T["RULER"] = "".join(ticks)

# ---- s6 : 26-week training-consistency matrix -----------------------------
r = random.Random(2026)
# rows = Mon..Sun, cols = weeks. Base split is Push/Pull/Lower + a run, ~4x/week.
PATTERNS = [(0,1,3,5), (0,2,4,5), (0,1,3,4,6), (0,2,4), (1,2,4,5), (0,1,4,6)]
cells = []
for c in range(26):
    if c >= 23:                       # the 18-day streak: weeks 23-24 full, week 25 Mon-Thu
        days = set(range(7)) if c < 25 else {0, 1, 2, 3}
    else:
        days = set(r.choice(PATTERNS))
    for row in range(7):
        if c == 25 and row > 3:                      # rest of this week hasn't happened
            fill, op = "var(--ink)", ".06"
        elif row in days:
            fill, op = "var(--accent)", ("1" if r.random() < 0.55 else ".62")
        else:
            fill, op = "var(--ink)", ".09"
        cells.append(f'<rect x="{c*13.6:.1f}" y="{row*13.6:.1f}" width="10.4" height="10.4" '
                     f'rx="3" fill="{fill}" opacity="{op}"/>')
T["MATRIX"] = "".join(cells)

# Exercise demo frames: lime-duotoned from yuhonas/free-exercise-db (public
# domain, The Unlicense). Two frames per exercise = start and end of the rep;
# the screens crossfade them, so the movement reads without shipping a GIF.
T.update(json.load(open("exercise_imgs.json")))

T["SB"] = open("_sb.frag").read()

# ---- build ----------------------------------------------------------------
if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>FitnessPro</title>'
            '<style>html,body{margin:0;padding:0;background:#07090A}</style>'
            + kit + app + src)
        print("built", out)
