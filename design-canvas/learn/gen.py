import sys, os

# Lingo has no photography either, so rule 7 is again CONTENT -- and for a language app
# the content is the single easiest thing to fake and the single most obvious when faked.
# Every Spanish string here is real and correct, the distractors are plausible rather than
# random, and the grammar note on s4 explains an actual error (preterite vs imperfect)
# rather than saying "Not quite!". "Translate: the cat is red" kills the screenshot.

SB = ('<div class="island"></div>'
      '<div class="statusbar"><span>9:41</span><span class="glyphs">'
      '<span class="sb-sig"><i></i><i></i><i></i><i></i></span>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">'
      '<path d="M8.5 10.6 10.7 8.3a3.1 3.1 0 0 0-4.4 0ZM4.6 6.7l1.3 1.3a4.9 4.9 0 0 1 5.2 0'
      'l1.3-1.3a6.7 6.7 0 0 0-7.8 0ZM1.6 3.6 2.9 5a9.3 9.3 0 0 1 11.2 0l1.3-1.4a11.1 11.1 0 0 0-13.8 0Z"/>'
      '</svg><span class="sb-bat"><b></b></span></span></div>')


def path(nodes, w=353, step=104):
    """The lesson path: nodes on an alternating serpentine with a drawn spine.

    Positions are computed, not hand-placed, so adding a unit cannot desync the spine from
    the nodes -- which is the failure every hand-built version of this screen has.
    `nodes` is a list of (state, glyph) where state is done | now | locked.
    """
    xs = [.5, .74, .84, .68, .40, .22, .16, .34]
    out, pts = [], []
    for i, (state, glyph) in enumerate(nodes):
        x, y = xs[i % len(xs)] * w, 30 + i * step
        pts.append((x, y))
    spine = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    out.append(f'<svg class="spine" width="{w}" height="{30 + len(nodes) * step}" fill="none">'
               f'<polyline points="{spine}" stroke="var(--ink-3)" stroke-width="3.5" '
               f'stroke-dasharray="1 13" stroke-linecap="round"/></svg>')
    for (state, glyph), (x, y) in zip(nodes, pts):
        out.append(f'<div class="node n-{state}" style="left:{x - 37:.0f}px;top:{y - 37:.0f}px">'
                   f'<span class="node-face">{glyph}</span></div>')
    return "".join(out)


T = {"SB": SB,
     "PATH": path([("done", "&#161;Hola!"), ("done", "Caf&eacute;"), ("done", "Familia"),
                   ("now", "Ayer"), ("locked", "Viajes"), ("locked", "Trabajo")])}

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>Lingo</title>'
            '<style>html,body{margin:0;padding:0;background:#FFF6E9}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
